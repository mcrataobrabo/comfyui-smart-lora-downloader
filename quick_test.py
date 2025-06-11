#!/usr/bin/env python3
"""
Quick test to check if the LoRA Auto Downloader nodes can be imported
"""

import sys
import os

# Add the ComfyUI path
current_dir = os.path.dirname(__file__)
comfyui_path = os.path.join(current_dir, "..", "..", "..")
sys.path.append(comfyui_path)

def test_node_imports():
    """Test if all nodes can be imported"""
    try:
        # Import the package
        from lora_auto_downloader_package import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
        
        print("✓ Package imported successfully")
        print(f"✓ Found {len(NODE_CLASS_MAPPINGS)} nodes:")
        
        for node_name, display_name in NODE_DISPLAY_NAME_MAPPINGS.items():
            print(f"  - {display_name} ({node_name})")
        
        # Test instantiation of the main nodes
        auto_detector = NODE_CLASS_MAPPINGS["AutoLoRADetector"]()
        print("✓ AutoLoRADetector instantiated successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_lora_directory():
    """Test LoRA directory access"""
    try:
        import folder_paths
        lora_paths = folder_paths.get_folder_paths("loras")
        if lora_paths:
            lora_path = lora_paths[0]
            print(f"✓ LoRA directory found: {lora_path}")
            
            if os.path.exists(lora_path):
                lora_files = [f for f in os.listdir(lora_path) 
                             if f.endswith(('.safetensors', '.ckpt', '.pt'))]
                print(f"✓ Directory accessible, {len(lora_files)} LoRA files found")
                return True
            else:
                print(f"✗ LoRA directory does not exist: {lora_path}")
                return False
        else:
            print("✗ No LoRA paths configured")
            return False
    except Exception as e:
        print(f"✗ LoRA directory test failed: {e}")
        return False

if __name__ == "__main__":
    print("LoRA Auto Downloader - Quick Test")
    print("=" * 40)
    
    success = True
    
    # Test imports
    if not test_node_imports():
        success = False
    
    print()
    
    # Test directory access
    if not test_lora_directory():
        success = False
    
    print()
    
    if success:
        print("✓ All tests passed! The nodes should be available in ComfyUI.")
        print()
        print("Next steps:")
        print("1. Restart ComfyUI")
        print("2. Look for 'Auto LoRA Detector' under loaders > lora")
        print("3. Add your CivitAI token and test with a workflow")
    else:
        print("✗ Some tests failed. Check the errors above.")
    
    print("\nPress Enter to continue...")
    input()
