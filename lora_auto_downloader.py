import os
import json
import requests
import hashlib
import time
from urllib.parse import urlparse
import folder_paths
import logging
from server import PromptServer

class LoRAAutoDownloader:
    """
    A custom node that automatically detects LoRA usage in workflows,
    checks if they are downloaded, and downloads missing ones.
    """
    
    def __init__(self):
        self.lora_path = folder_paths.get_folder_paths("loras")[0]
        self.download_cache = {}
        self.civitai_api_base = "https://civitai.com/api/v1"
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "workflow_data": ("STRING", {
                    "multiline": True,
                    "default": "{}",
                    "tooltip": "JSON workflow data to scan for LoRA usage"
                }),
                "civitai_token": ("STRING", {
                    "default": "",
                    "tooltip": "CivitAI API token for downloading models"
                }),
                "auto_download": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Automatically download missing LoRAs"
                }),
                "check_only": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Only check for missing LoRAs without downloading"
                })
            },
            "optional": {
                "passthrough_model": ("MODEL",),
                "passthrough_clip": ("CLIP",),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "MODEL", "CLIP")
    RETURN_NAMES = ("status_report", "missing_loras", "model", "clip")
    FUNCTION = "process_workflow"
    OUTPUT_NODE = True
    CATEGORY = "loaders/lora"
    DESCRIPTION = "Automatically detects and downloads missing LoRAs from workflows"
    
    def extract_loras_from_workflow(self, workflow_data):
        """Extract LoRA information from workflow JSON data"""
        loras_found = []
        
        try:
            if isinstance(workflow_data, str):
                workflow = json.loads(workflow_data)
            else:
                workflow = workflow_data
                
            # Look for LoRA loader nodes in the workflow
            for node_id, node_data in workflow.items():
                if isinstance(node_data, dict):
                    class_type = node_data.get("class_type", "")
                    
                    # Check for various LoRA loader types
                    if any(lora_type in class_type for lora_type in [
                        "LoraLoader", "LoraLoaderModelOnly", "LoRALoader", 
                        "Lora Loader", "JsonLoraLoader"
                    ]):
                        inputs = node_data.get("inputs", {})
                        
                        # Extract LoRA name
                        lora_name = None
                        for key in ["lora_name", "name", "lora", "model_name"]:
                            if key in inputs:
                                lora_name = inputs[key]
                                break
                        
                        if lora_name:
                            loras_found.append({
                                "name": lora_name,
                                "node_id": node_id,
                                "class_type": class_type,
                                "strength_model": inputs.get("strength_model", 1.0),
                                "strength_clip": inputs.get("strength_clip", 1.0)
                            })
                            
                    # Also check for JSON-based LoRA configurations
                    elif "lora_config" in node_data.get("inputs", {}):
                        try:
                            lora_config = json.loads(node_data["inputs"]["lora_config"])
                            for lora in lora_config.get("lora", []):
                                loras_found.append({
                                    "name": lora.get("name", ""),
                                    "modelVersionId": lora.get("modelVersionId", ""),
                                    "strength": lora.get("strength", 1.0),
                                    "node_id": node_id,
                                    "class_type": class_type
                                })
                        except (json.JSONDecodeError, TypeError):
                            continue
                            
        except (json.JSONDecodeError, TypeError) as e:
            logging.warning(f"Error parsing workflow data: {e}")
            
        return loras_found
    
    def check_lora_exists(self, lora_name):
        """Check if a LoRA file exists locally"""
        if not lora_name:
            return False
            
        # Clean up the name and check various extensions
        base_name = lora_name.replace(".safetensors", "").replace(".ckpt", "").replace(".pt", "")
        extensions = [".safetensors", ".ckpt", ".pt"]
        
        for ext in extensions:
            full_path = os.path.join(self.lora_path, base_name + ext)
            if os.path.exists(full_path):
                return True
                
        # Also check with modelVersionId suffix if available
        for lora in self.download_cache.values():
            if lora.get("base_name") == base_name:
                return True
                
        return False
    
    def search_civitai_model(self, lora_name, civitai_token):
        """Search for a model on CivitAI"""
        if not civitai_token:
            return None
            
        headers = {"Authorization": f"Bearer {civitai_token}"}
        search_url = f"{self.civitai_api_base}/models"
        
        params = {
            "query": lora_name,
            "types": "LORA",
            "sort": "Highest Rated",
            "limit": 5
        }
        
        try:
            response = requests.get(search_url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data.get("items"):
                    return data["items"][0]  # Return the first/best match
        except Exception as e:
            logging.error(f"Error searching CivitAI for {lora_name}: {e}")
            
        return None
    
    def download_civitai_model(self, model_info, civitai_token):
        """Download a model from CivitAI"""
        if not model_info or not civitai_token:
            return False
            
        try:
            # Get the latest version
            model_versions = model_info.get("modelVersions", [])
            if not model_versions:
                return False
                
            latest_version = model_versions[0]
            files = latest_version.get("files", [])
            
            # Find the primary file (usually .safetensors)
            primary_file = None
            for file_info in files:
                if file_info.get("primary", False) or file_info.get("name", "").endswith(".safetensors"):
                    primary_file = file_info
                    break
                    
            if not primary_file:
                primary_file = files[0] if files else None
                
            if not primary_file:
                return False
                
            download_url = primary_file.get("downloadUrl")
            filename = primary_file.get("name")
            
            if not download_url or not filename:
                return False
                
            # Prepare download
            headers = {"Authorization": f"Bearer {civitai_token}"}
            safe_filename = self.sanitize_filename(filename)
            file_path = os.path.join(self.lora_path, safe_filename)
            
            # Download with progress
            logging.info(f"Downloading {filename} to {file_path}")
            
            response = requests.get(download_url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Log progress every 10MB
                        if downloaded_size % (10 * 1024 * 1024) == 0:
                            if total_size > 0:
                                progress = (downloaded_size / total_size) * 100
                                logging.info(f"Download progress: {progress:.1f}%")
            
            logging.info(f"Successfully downloaded {filename}")
            return True
            
        except Exception as e:
            logging.error(f"Error downloading model: {e}")
            return False
    
    def sanitize_filename(self, filename):
        """Sanitize filename for safe saving"""
        # Remove or replace unsafe characters
        unsafe_chars = '<>:"/\\|?*'
        for char in unsafe_chars:
            filename = filename.replace(char, '_')
        return filename
    
    def process_workflow(self, workflow_data, civitai_token="", auto_download=True, 
                        check_only=False, passthrough_model=None, passthrough_clip=None):
        """Main processing function"""
        
        status_lines = []
        missing_loras = []
        
        # Extract LoRAs from workflow
        loras_found = self.extract_loras_from_workflow(workflow_data)
        status_lines.append(f"Found {len(loras_found)} LoRA references in workflow")
        
        if not loras_found:
            status_lines.append("No LoRAs detected in workflow")
            return ("\\n".join(status_lines), "[]", passthrough_model, passthrough_clip)
        
        # Check each LoRA
        for lora_info in loras_found:
            lora_name = lora_info.get("name", "")
            if not lora_name:
                continue
                
            exists = self.check_lora_exists(lora_name)
            
            if exists:
                status_lines.append(f"✓ {lora_name} - Found locally")
            else:
                status_lines.append(f"✗ {lora_name} - Missing")
                missing_loras.append(lora_info)
                
                if auto_download and not check_only and civitai_token:
                    status_lines.append(f"  Searching CivitAI for {lora_name}...")
                    
                    # Search for the model
                    model_info = self.search_civitai_model(lora_name, civitai_token)
                    
                    if model_info:
                        status_lines.append(f"  Found model: {model_info.get('name', 'Unknown')}")
                        
                        # Download the model
                        if self.download_civitai_model(model_info, civitai_token):
                            status_lines.append(f"  ✓ Successfully downloaded {lora_name}")
                        else:
                            status_lines.append(f"  ✗ Failed to download {lora_name}")
                    else:
                        status_lines.append(f"  ✗ Could not find {lora_name} on CivitAI")
                elif not civitai_token and auto_download:
                    status_lines.append(f"  ⚠ CivitAI token required for download")
        
        # Summary
        total_missing = len(missing_loras)
        if total_missing == 0:
            status_lines.append("\\n✓ All LoRAs are available locally!")
        else:
            status_lines.append(f"\\n⚠ {total_missing} LoRA(s) missing")
            if not auto_download:
                status_lines.append("Set auto_download=True to download missing LoRAs")
                
        return (
            "\\n".join(status_lines),
            json.dumps(missing_loras, indent=2),
            passthrough_model,
            passthrough_clip
        )


class WorkflowLoRAScanner:
    """
    A simpler node that scans the current workflow automatically
    by hooking into the prompt execution system
    """
    
    def __init__(self):
        self.lora_path = folder_paths.get_folder_paths("loras")[0]
        
    @classmethod  
    def INPUT_TYPES(cls):
        return {
            "required": {
                "trigger": ("STRING", {
                    "default": "scan",
                    "tooltip": "Trigger to start scanning"
                }),
                "civitai_token": ("STRING", {
                    "default": "",
                    "tooltip": "CivitAI API token for downloading models"
                }),
            },
            "optional": {
                "passthrough": ("*",),
            }
        }
    
    RETURN_TYPES = ("STRING", "*")
    RETURN_NAMES = ("scan_result", "passthrough")
    FUNCTION = "scan_current_workflow"
    OUTPUT_NODE = True
    CATEGORY = "loaders/lora"
    DESCRIPTION = "Scans the current executing workflow for LoRA usage"
    
    def scan_current_workflow(self, trigger, civitai_token="", passthrough=None):
        """Scan the current workflow for LoRA usage"""
        
        # This is a simplified version that would need integration with
        # the execution system to get the current workflow
        scan_result = "Workflow scanning would require deeper integration with ComfyUI execution system"
        
        return (scan_result, passthrough)


# Node registration
NODE_CLASS_MAPPINGS = {
    "LoRAAutoDownloader": LoRAAutoDownloader,
    "WorkflowLoRAScanner": WorkflowLoRAScanner,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoRAAutoDownloader": "LoRA Auto Downloader",
    "WorkflowLoRAScanner": "Workflow LoRA Scanner",
}
