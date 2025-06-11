import os
import json
import logging
import folder_paths
from server import PromptServer
import execution
from typing import Dict, Any, List
import threading
import time

class WorkflowLoRAInterceptor:
    """
    Advanced node that hooks into ComfyUI's execution system
    to automatically detect and download missing LoRAs
    """
    
    def __init__(self):
        self.lora_path = folder_paths.get_folder_paths("loras")[0]
        self.auto_mode = False
        self.civitai_token = ""
        self.setup_hooks()
        
    def setup_hooks(self):
        """Setup hooks into the ComfyUI execution system"""
        try:
            # Hook into the prompt queue to intercept workflows
            original_put = PromptServer.instance.prompt_queue.put
            
            def hooked_put(item):
                """Intercept workflow execution to scan for LoRAs"""
                if self.auto_mode:
                    try:
                        number, prompt_id, prompt, extra_data, outputs_to_execute = item
                        self.scan_and_download_loras(prompt)
                    except Exception as e:
                        logging.error(f"Error in LoRA interceptor: {e}")
                
                return original_put(item)
            
            PromptServer.instance.prompt_queue.put = hooked_put
            logging.info("LoRA Auto Downloader hooks installed successfully")
            
        except Exception as e:
            logging.error(f"Failed to setup LoRA auto downloader hooks: {e}")
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "enable_auto_mode": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Enable automatic LoRA detection and downloading for all workflows"
                }),
                "civitai_token": ("STRING", {
                    "default": "",
                    "tooltip": "CivitAI API token for downloading models"
                }),
                "download_missing": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Automatically download missing LoRAs"
                }),
                "scan_current_workflow": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Scan the current workflow for LoRA usage"
                }),
            },
            "optional": {
                "manual_workflow_json": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Manually provide workflow JSON to scan"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("status", "missing_loras_report")
    FUNCTION = "configure_interceptor"
    OUTPUT_NODE = True
    CATEGORY = "loaders/lora"
    DESCRIPTION = "Automatically intercepts workflows to detect and download missing LoRAs"
    
    def scan_and_download_loras(self, workflow_prompt: Dict[str, Any]) -> Dict[str, Any]:
        """Scan workflow and download missing LoRAs"""
        try:
            from .lora_auto_downloader import LoRAAutoDownloader
        except ImportError:
            # Fallback for direct execution
            import sys
            current_dir = os.path.dirname(__file__)
            sys.path.append(current_dir)
            from lora_auto_downloader import LoRAAutoDownloader
        
        missing_loras = []
        downloaded_loras = []
        
        try:
            # Convert workflow prompt to JSON string for the downloader
            workflow_json = json.dumps(workflow_prompt)
            
            # Create downloader instance
            downloader = LoRAAutoDownloader()
            
            # Extract LoRAs from workflow
            loras_found = downloader.extract_loras_from_workflow(workflow_json)
            
            for lora_info in loras_found:
                lora_name = lora_info.get("name", "")
                if not lora_name:
                    continue
                    
                # Check if LoRA exists
                exists = downloader.check_lora_exists(lora_name)
                
                if not exists:
                    missing_loras.append(lora_name)
                    
                    if self.civitai_token:
                        # Try to download
                        model_info = downloader.search_civitai_model(lora_name, self.civitai_token)
                        if model_info:
                            if downloader.download_civitai_model(model_info, self.civitai_token):
                                downloaded_loras.append(lora_name)
                                logging.info(f"Auto-downloaded LoRA: {lora_name}")
            
            return {
                "missing": missing_loras,
                "downloaded": downloaded_loras,
                "total_found": len(loras_found)
            }
            
        except Exception as e:
            logging.error(f"Error in automatic LoRA scanning: {e}")
            return {"error": str(e)}
    
    def configure_interceptor(self, enable_auto_mode, civitai_token, download_missing, 
                            scan_current_workflow, manual_workflow_json=""):
        """Configure the interceptor settings"""
        
        self.auto_mode = enable_auto_mode
        self.civitai_token = civitai_token
        
        status_lines = []
        missing_report = []
        
        # Status update
        if enable_auto_mode:
            status_lines.append("✓ Auto-mode enabled - will scan all future workflows")
            if civitai_token:
                status_lines.append("✓ CivitAI token provided - will download missing LoRAs")
            else:
                status_lines.append("⚠ No CivitAI token - will only detect missing LoRAs")
        else:            status_lines.append("○ Auto-mode disabled")
        
        # Manual workflow scanning
        if scan_current_workflow or manual_workflow_json:
            status_lines.append("\\nScanning workflow for LoRAs...")
            
            try:
                try:
                    from .lora_auto_downloader import LoRAAutoDownloader
                except ImportError:
                    # Fallback for direct execution
                    import sys
                    current_dir = os.path.dirname(__file__)
                    sys.path.append(current_dir)
                    from lora_auto_downloader import LoRAAutoDownloader
                    
                downloader = LoRAAutoDownloader()
                
                workflow_data = manual_workflow_json if manual_workflow_json else "{}"
                
                # Process the workflow
                result = downloader.process_workflow(
                    workflow_data, 
                    civitai_token, 
                    download_missing, 
                    check_only=not download_missing
                )
                
                status_lines.append(result[0])  # Status report
                missing_report = result[1]      # Missing LoRAs JSON
                
            except Exception as e:
                status_lines.append(f"Error scanning workflow: {e}")
        
        # LoRA directory info
        lora_count = len([f for f in os.listdir(self.lora_path) 
                         if f.endswith(('.safetensors', '.ckpt', '.pt'))])
        status_lines.append(f"\\nLoRA directory: {self.lora_path}")
        status_lines.append(f"Current LoRA count: {lora_count}")
        
        return ("\\n".join(status_lines), missing_report)


class LoRADirectoryManager:
    """
    Utility node for managing the LoRA directory
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "action": (["list_loras", "check_directory", "cleanup_duplicates"], {
                    "default": "list_loras"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("report",)
    FUNCTION = "manage_directory"
    OUTPUT_NODE = True
    CATEGORY = "loaders/lora"
    DESCRIPTION = "Manage and organize the LoRA directory"
    
    def manage_directory(self, action):
        """Manage the LoRA directory"""
        
        lora_path = folder_paths.get_folder_paths("loras")[0]
        report_lines = []
        
        if action == "list_loras":
            lora_files = [f for f in os.listdir(lora_path) 
                         if f.endswith(('.safetensors', '.ckpt', '.pt'))]
            
            report_lines.append(f"LoRA Directory: {lora_path}")
            report_lines.append(f"Total LoRA files: {len(lora_files)}")
            report_lines.append("\\nFiles:")
            
            for lora_file in sorted(lora_files):
                file_path = os.path.join(lora_path, lora_file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                report_lines.append(f"  {lora_file} ({file_size:.1f} MB)")
                
        elif action == "check_directory":
            if not os.path.exists(lora_path):
                report_lines.append(f"❌ LoRA directory does not exist: {lora_path}")
            else:
                is_writable = os.access(lora_path, os.W_OK)
                report_lines.append(f"📁 Directory: {lora_path}")
                report_lines.append(f"✓ Exists: Yes")
                report_lines.append(f"✓ Writable: {'Yes' if is_writable else 'No'}")
                
                # Check space
                try:
                    import shutil
                    total, used, free = shutil.disk_usage(lora_path)
                    report_lines.append(f"💾 Free space: {free / (1024**3):.1f} GB")
                except:
                    report_lines.append("💾 Could not check disk space")
                    
        elif action == "cleanup_duplicates":
            # Find potential duplicates (same name with different extensions)
            lora_files = os.listdir(lora_path)
            base_names = {}
            
            for lora_file in lora_files:
                if lora_file.endswith(('.safetensors', '.ckpt', '.pt')):
                    base_name = os.path.splitext(lora_file)[0]
                    if base_name not in base_names:
                        base_names[base_name] = []
                    base_names[base_name].append(lora_file)
            
            duplicates = {k: v for k, v in base_names.items() if len(v) > 1}
            
            if duplicates:
                report_lines.append("🔍 Potential duplicates found:")
                for base_name, files in duplicates.items():
                    report_lines.append(f"  {base_name}:")
                    for file in files:
                        report_lines.append(f"    - {file}")
            else:
                report_lines.append("✓ No obvious duplicates found")
        
        return ("\n".join(report_lines),)
