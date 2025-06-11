"""
LoRA Auto Downloader Custom Node for ComfyUI

This custom node automatically detects LoRA usage in workflows,
checks if they are already downloaded, and downloads missing ones
from CivitAI or other sources.
"""

from .lora_auto_downloader import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
from .workflow_interceptor import WorkflowLoRAInterceptor, LoRADirectoryManager
from .auto_lora_detector import AutoLoRADetector

# Add all nodes to the mappings
NODE_CLASS_MAPPINGS.update({
    "WorkflowLoRAInterceptor": WorkflowLoRAInterceptor,
    "LoRADirectoryManager": LoRADirectoryManager,
    "AutoLoRADetector": AutoLoRADetector,
})

NODE_DISPLAY_NAME_MAPPINGS.update({
    "WorkflowLoRAInterceptor": "Workflow LoRA Interceptor",
    "LoRADirectoryManager": "LoRA Directory Manager", 
    "AutoLoRADetector": "Auto LoRA Detector",
})

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
