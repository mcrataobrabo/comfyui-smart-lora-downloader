# Quick Start Guide - LoRA Auto Downloader

## 1. Basic Setup

1. The custom node is already installed in your ComfyUI
2. Restart ComfyUI to load the new nodes
3. You'll find the new nodes under "loaders" → "lora" category

## 2. Getting a CivitAI Token

1. Go to https://civitai.com
2. Sign in or create an account
3. Go to Account Settings → API Keys
4. Generate a new API key
5. Copy this token - you'll need it for downloading

## 3. Quick Test

### Option A: Manual Workflow Scanning
1. Add "LoRA Auto Downloader" node to your workflow
2. Paste your workflow JSON into the "workflow_data" field
3. Add your CivitAI token
4. Set "auto_download" to true
5. Execute the node

### Option B: Automatic Interception
1. Add "Workflow LoRA Interceptor" node to any workflow
2. Enable "enable_auto_mode"
3. Add your CivitAI token
4. All future workflows will automatically check for missing LoRAs

## 4. Example Workflow JSON

Use the provided `example_workflow.json` file to test the functionality:

```json
{
  "2": {
    "class_type": "LoraLoader",
    "inputs": {
      "lora_name": "example_lora.safetensors",
      "strength_model": 1.0,
      "strength_clip": 1.0
    }
  }
}
```

## 5. Managing Your LoRA Collection

Use the "LoRA Directory Manager" node to:
- List all LoRAs with file sizes
- Check directory permissions and disk space
- Find potential duplicate files

## 6. Troubleshooting

### Node doesn't appear
- Restart ComfyUI
- Check the console for error messages

### Download failures
- Verify your CivitAI token is correct
- Check your internet connection
- Ensure you have write permissions to the LoRA directory

### Permission errors
- Run ComfyUI as administrator (Windows)
- Check that the LoRA directory exists and is writable

## 7. File Locations

- LoRAs are downloaded to: `E:\ComfyUI_windows_portable\ComfyUI\models\loras`
- Custom node files: `E:\ComfyUI_windows_portable\ComfyUI\custom_nodes\lora_auto_downloader_package`

## 8. Support

- Check the README.md for detailed documentation
- Run test.py to verify installation
- Check ComfyUI console for detailed logs during operation
