#!/usr/bin/env python3
"""
Test script for LoRA Auto Downloader custom node
"""

import os
import sys
import json

# Add current directory to path
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

def test_import():
    """Test if the modules can be imported"""
    try:
        from lora_auto_downloader import LoRAAutoDownloader, WorkflowLoRAScanner
        from workflow_interceptor import WorkflowLoRAInterceptor, LoRADirectoryManager
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    try:
        from lora_auto_downloader import LoRAAutoDownloader
        
        downloader = LoRAAutoDownloader()
        
        # Test with example workflow
        example_workflow_path = os.path.join(current_dir, "example_workflow.json")
        if os.path.exists(example_workflow_path):
            with open(example_workflow_path, 'r') as f:
                workflow_data = f.read()
            
            # Test LoRA extraction
            loras_found = downloader.extract_loras_from_workflow(workflow_data)
            print(f"✓ Found {len(loras_found)} LoRAs in example workflow")
            
            for lora in loras_found:
                print(f"  - {lora.get('name', 'Unknown')}")
        else:
            print("⚠ Example workflow not found, skipping workflow test")
        
        # Test directory checking
        from workflow_interceptor import LoRADirectoryManager
        manager = LoRADirectoryManager()
        result = manager.manage_directory("check_directory")
        print("✓ Directory manager test completed")
        
        return True
        
    except Exception as e:
        print(f"✗ Functionality test error: {e}")
        return False

def main():
    """Main test function"""
    print("LoRA Auto Downloader - Test Script")
    print("=" * 40)
    
    # Test imports
    if not test_import():
        return False
    
    # Test basic functionality
    if not test_basic_functionality():
        return False
    
    print("\n✓ All tests passed! The LoRA Auto Downloader is ready to use.")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
