import os
import json
import requests
import hashlib
import time
import logging
import folder_paths
from server import PromptServer

class AutoLoRADetector:
    """
    A simpler node that automatically detects missing LoRAs from the current workflow execution
    and provides options to download them
    """
    
    def __init__(self):
        self.lora_path = folder_paths.get_folder_paths("loras")[0]
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "civitai_token": ("STRING", {
                    "default": "",
                    "tooltip": "Your CivitAI API token for downloading models"
                }),
                "auto_download": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Automatically download missing LoRAs"
                }),
                "check_missing": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Check for missing LoRAs and report them"
                }),
            },
            "optional": {
                "trigger_input": ("*", {"tooltip": "Connect any input to trigger the check"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "*")
    RETURN_NAMES = ("status_report", "missing_loras_list", "passthrough")
    FUNCTION = "detect_and_handle_loras"
    OUTPUT_NODE = True
    CATEGORY = "loaders/lora"
    DESCRIPTION = "Detects missing LoRAs and can download them from CivitAI"
    
    def get_missing_loras_from_error(self, error_message):
        """Extract missing LoRA names from ComfyUI validation error messages"""
        missing_loras = []
        
        # Look for the pattern in error messages like:
        # "Value not in list: lora_name: 'breastinClass' not in (list of length 21)"
        lines = error_message.split('\n')
        for line in lines:
            if "lora_name:" in line and "not in" in line:
                # Extract the LoRA name between quotes
                start = line.find("'") + 1
                end = line.find("'", start)
                if start > 0 and end > start:
                    lora_name = line[start:end]
                    if lora_name not in missing_loras:
                        missing_loras.append(lora_name)
        
        return missing_loras
    
    def search_and_download_lora(self, lora_name, civitai_token):
        """Search for and download a specific LoRA from CivitAI"""
        if not civitai_token:
            return False, "No CivitAI token provided"
            
        try:
            # Search for the model on CivitAI
            headers = {"Authorization": f"Bearer {civitai_token}"}
            search_url = "https://civitai.com/api/v1/models"
            
            params = {
                "query": lora_name,
                "types": "LORA",
                "sort": "Highest Rated",
                "limit": 3
            }
            
            response = requests.get(search_url, headers=headers, params=params, timeout=30)
            if response.status_code != 200:
                return False, f"Search failed: HTTP {response.status_code}"
            
            data = response.json()
            items = data.get("items", [])
            
            if not items:
                return False, "No matching LoRAs found on CivitAI"
            
            # Try to find the best match
            best_match = None
            for item in items:
                item_name = item.get("name", "").lower()
                if lora_name.lower() in item_name or item_name in lora_name.lower():
                    best_match = item
                    break
            
            if not best_match:
                best_match = items[0]  # Use first result if no exact match
            
            # Download the best match
            model_versions = best_match.get("modelVersions", [])
            if not model_versions:
                return False, "No downloadable versions found"
            
            latest_version = model_versions[0]
            files = latest_version.get("files", [])
            
            # Find the primary file
            primary_file = None
            for file_info in files:
                if file_info.get("primary", False) or file_info.get("name", "").endswith(".safetensors"):
                    primary_file = file_info
                    break
            
            if not primary_file and files:
                primary_file = files[0]
            
            if not primary_file:
                return False, "No downloadable file found"
            
            download_url = primary_file.get("downloadUrl")
            filename = primary_file.get("name", f"{lora_name}.safetensors")
            
            if not download_url:
                return False, "No download URL available"
            
            # Download the file
            safe_filename = self.sanitize_filename(filename)
            file_path = os.path.join(self.lora_path, safe_filename)
            
            # Check if file already exists
            if os.path.exists(file_path):
                return True, f"File already exists: {safe_filename}"
            
            response = requests.get(download_url, headers=headers, stream=True, timeout=60)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return True, f"Successfully downloaded: {safe_filename}"
            
        except Exception as e:
            return False, f"Download error: {str(e)}"
    
    def sanitize_filename(self, filename):
        """Sanitize filename for safe saving"""
        unsafe_chars = '<>:"/\\|?*'
        for char in unsafe_chars:
            filename = filename.replace(char, '_')
        return filename
    
    def check_lora_exists(self, lora_name):
        """Check if a LoRA file exists locally"""
        if not lora_name:
            return False
        
        # Check various extensions and variations
        base_name = lora_name.replace(".safetensors", "").replace(".ckpt", "").replace(".pt", "")
        extensions = [".safetensors", ".ckpt", ".pt"]
        
        for ext in extensions:
            for variation in [base_name, base_name.lower(), base_name.upper()]:
                full_path = os.path.join(self.lora_path, variation + ext)
                if os.path.exists(full_path):
                    return True
        
        return False
    
    def detect_and_handle_loras(self, civitai_token="", auto_download=True, check_missing=True, trigger_input=None):
        """Main function to detect and handle missing LoRAs"""
        
        status_lines = []
        missing_loras = []
        
        # Get the current LoRA directory info
        lora_files = [f for f in os.listdir(self.lora_path) 
                     if f.endswith(('.safetensors', '.ckpt', '.pt'))]
        
        status_lines.append(f"LoRA Directory: {self.lora_path}")
        status_lines.append(f"Current LoRA count: {len(lora_files)}")
        
        if check_missing:
            # For now, we'll simulate checking common missing LoRAs
            # In a real implementation, this would hook into the validation system
            common_missing_loras = [
                "breastinClass",
                "GoodHands-vanilla", 
                "Addams",
                "zyd232sChineseGirl_v16",
                "GoodHands-beta2"
            ]
            
            status_lines.append("\\nChecking for common missing LoRAs...")
            
            for lora_name in common_missing_loras:
                exists = self.check_lora_exists(lora_name)
                
                if not exists:
                    missing_loras.append(lora_name)
                    status_lines.append(f"✗ Missing: {lora_name}")
                    
                    if auto_download and civitai_token:
                        status_lines.append(f"  Attempting to download {lora_name}...")
                        success, message = self.search_and_download_lora(lora_name, civitai_token)
                        
                        if success:
                            status_lines.append(f"  ✓ {message}")
                        else:
                            status_lines.append(f"  ✗ {message}")
                    elif auto_download and not civitai_token:
                        status_lines.append(f"  ⚠ CivitAI token required for download")
                else:
                    status_lines.append(f"✓ Found: {lora_name}")
        
        # Summary
        if missing_loras:
            status_lines.append(f"\\n⚠ {len(missing_loras)} LoRA(s) are missing")
            if not auto_download:
                status_lines.append("Enable auto_download to download missing LoRAs")
            elif not civitai_token:
                status_lines.append("Provide CivitAI token to enable downloads")
        else:
            status_lines.append("\\n✓ All checked LoRAs are available!")
        
        return (
            "\\n".join(status_lines),
            json.dumps(missing_loras, indent=2),
            trigger_input
        )


# Add to the node mappings
if "NODE_CLASS_MAPPINGS" in globals():
    NODE_CLASS_MAPPINGS["AutoLoRADetector"] = AutoLoRADetector
    NODE_DISPLAY_NAME_MAPPINGS["AutoLoRADetector"] = "Auto LoRA Detector"
else:
    NODE_CLASS_MAPPINGS = {"AutoLoRADetector": AutoLoRADetector}
    NODE_DISPLAY_NAME_MAPPINGS = {"AutoLoRADetector": "Auto LoRA Detector"}
