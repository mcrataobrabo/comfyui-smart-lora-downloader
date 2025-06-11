import os
import json
import requests
import hashlib
import time
import logging
import folder_paths
from server import PromptServer
try:
    from .lora_name_matcher import LoRANameMatcher
    HAS_NAME_MATCHER = True
except ImportError:
    HAS_NAME_MATCHER = False

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
                }),                "check_missing": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Check for missing LoRAs and report them"
                }),
                "test_mode": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Test download with common missing LoRAs"
                }),
            },
            "optional": {
                "trigger_input": ("*", {"tooltip": "Connect any input to trigger the check"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING", "*")
    RETURN_NAMES = ("status_report", "missing_loras_list", "downloaded_loras_list", "passthrough")
    FUNCTION = "detect_and_handle_loras"
    OUTPUT_NODE = True
    CATEGORY = "loaders/lora"
    DESCRIPTION = "Detects missing LoRAs and can download them from CivitAI"
    
    def get_missing_loras_from_error(self, error_message):
        """Extract missing LoRA names from ComfyUI validation error messages"""
        missing_loras = []
        
        # Look for the pattern in error messages like:
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
        """Search for and download a specific LoRA from CivitAI using enhanced matching"""
        if not civitai_token:
            return False, "No CivitAI token provided"
            
        try:
            headers = {"Authorization": f"Bearer {civitai_token}"}
            search_url = "https://civitai.com/api/v1/models"
            
            if HAS_NAME_MATCHER:
                # Use enhanced matching
                name_matcher = LoRANameMatcher()
                search_results, used_queries = name_matcher.search_civitai_with_multiple_strategies(
                    lora_name, civitai_token
                )
                
                if not search_results:
                    return False, f"No LoRAs found for '{lora_name}' using multiple search strategies."
                
                best_match, similarity = name_matcher.find_best_match_from_search_results(
                    lora_name, search_results
                )
                
                if not best_match or similarity < 0.2:  # Lower threshold for better coverage
                    suggestion_text = f"No good match found for '{lora_name}' (best similarity: {similarity:.2f})"
                    if search_results:
                        suggestion_text += f"\nSearched using: {', '.join(used_queries)}"
                        suggestion_text += f"\nTop result: '{search_results[0].get('name', 'Unknown')}'"
                    return False, suggestion_text
                
                print(f"Enhanced matching found: '{best_match.get('name')}' (similarity: {similarity:.2f})")
                
            else:
                # Fallback to original simple matching
                params = {
                    "query": lora_name,
                    "types": "LORA", 
                    "sort": "Highest Rated",
                    "limit": 5
                }
                
                response = requests.get(search_url, headers=headers, params=params, timeout=30)
                if response.status_code != 200:
                    return False, f"Search failed: HTTP {response.status_code}"
                
                data = response.json()
                items = data.get("items", [])
                
                if not items:
                    return False, f"No matching LoRAs found for '{lora_name}'"
                
                # Try to find the best match using simple logic
                best_match = None
                for item in items:
                    item_name = item.get("name", "").lower()
                    if lora_name.lower() in item_name or item_name in lora_name.lower():
                        best_match = item
                        break
                
                if not best_match:
                    best_match = items[0]  # Use first result if no exact match
                    print(f"No exact match found for '{lora_name}', using: '{best_match.get('name')}'")
            
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
    
    def detect_and_handle_loras(self, civitai_token="", auto_download=True, check_missing=True, test_mode=False, trigger_input=None):
        """Main function to detect and handle missing LoRAs"""
        
        status_lines = []
        missing_loras = []
        downloaded_loras = []  # Track successfully downloaded LoRAs
          # Get the current LoRA directory info
        lora_files = [f for f in os.listdir(self.lora_path) 
                     if f.endswith(('.safetensors', '.ckpt', '.pt'))]
        
        status_lines.append(f"LoRA Directory: {self.lora_path}")
        status_lines.append(f"Current LoRA count: {len(lora_files)}")
        
        if check_missing:
            if test_mode:
                # Test mode: Try to download specific LoRAs for testing
                test_loras = ["example_lora_name"]  # Replace with actual LoRA names for testing
                status_lines.append("\\n🧪 TEST MODE: Attempting to download test LoRAs...")
                
                for lora_name in test_loras:
                    exists = self.check_lora_exists(lora_name)
                    
                    if not exists:
                        missing_loras.append(lora_name)
                        status_lines.append(f"\\n❌ Missing: {lora_name}")
                        
                        if auto_download and civitai_token:
                            status_lines.append(f"  🔍 Searching CivitAI for {lora_name}...")
                            success, message = self.search_and_download_lora(lora_name, civitai_token)
                            
                            if success:
                                downloaded_loras.append(lora_name)
                                status_lines.append(f"  ✅ {message}")
                            else:
                                status_lines.append(f"  ❌ {message}")
                        elif auto_download and not civitai_token:
                            status_lines.append(f"  ⚠️ CivitAI token required for download")
                        else:
                            status_lines.append(f"  ⚠️ Auto download disabled")
                    else:
                        status_lines.append(f"✅ Found: {lora_name}")
            else:
                # Normal mode: Show information and wait for workflow errors
                status_lines.append("\\nReady to detect missing LoRAs from workflow validation errors.")
                status_lines.append("To use: Connect this node and run a workflow with missing LoRAs.")
                status_lines.append("💡 Enable 'test_mode' to test with known LoRAs.")
                
                # Show current LoRA directory info
                status_lines.append("\\nCurrent LoRA directory contains:")
                if len(lora_files) == 0:
                    status_lines.append("  No LoRA files found")
                else:
                    # Show first few LoRAs as examples
                    shown_files = lora_files[:5]
                    for lora_file in shown_files:
                        status_lines.append(f"  ✓ {lora_file}")
                    if len(lora_files) > 5:
                        status_lines.append(f"  ... and {len(lora_files) - 5} more files")
          # Summary
        if downloaded_loras:
            status_lines.append(f"\\n✅ Successfully downloaded {len(downloaded_loras)} LoRA(s)")
        
        if missing_loras:
            remaining_missing = len(missing_loras) - len(downloaded_loras)
            if remaining_missing > 0:
                status_lines.append(f"\\n⚠ {remaining_missing} LoRA(s) still missing")
            if not auto_download:
                status_lines.append("Enable auto_download to download missing LoRAs")
            elif not civitai_token:
                status_lines.append("Provide CivitAI token to enable downloads")
        else:
            status_lines.append("\\n✅ LoRA directory ready!")
            status_lines.append("💡 This node detects missing LoRAs from workflow validation errors.")
            status_lines.append("💡 Run a workflow with missing LoRAs to trigger automatic detection.")
        
        return (
            "\\n".join(status_lines),
            json.dumps(missing_loras, indent=2),
            json.dumps(downloaded_loras, indent=2),  # New output for downloaded LoRAs
            trigger_input
        )
    
    def process_workflow_error(self, error_message, civitai_token="", auto_download=True):
        """Process a workflow validation error and handle missing LoRAs"""
        missing_loras = self.get_missing_loras_from_error(error_message)
        downloaded_loras = []
        status_lines = []
        
        if not missing_loras:
            return "No missing LoRAs detected in error message", "[]", "[]"
        
        status_lines.append(f"Detected {len(missing_loras)} missing LoRA(s): {', '.join(missing_loras)}")
        
        for lora_name in missing_loras:
            if auto_download and civitai_token:
                status_lines.append(f"\\nAttempting to download: {lora_name}")
                success, message = self.search_and_download_lora(lora_name, civitai_token)
                
                if success:
                    downloaded_loras.append(lora_name)
                    status_lines.append(f"✓ {message}")
                else:
                    status_lines.append(f"✗ {message}")
            else:
                status_lines.append(f"\\n⚠ {lora_name} - Auto download disabled or no token provided")
        
        if downloaded_loras:
            status_lines.append(f"\\n✅ Successfully downloaded {len(downloaded_loras)} LoRA(s)")
            status_lines.append("🔄 Please restart your workflow to use the new LoRAs")
        
        return (
            "\\n".join(status_lines),
            json.dumps(missing_loras, indent=2),
            json.dumps(downloaded_loras, indent=2)
        )



