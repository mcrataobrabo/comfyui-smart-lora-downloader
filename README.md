# LoRA Auto Downloader for ComfyUI

A custom node package that automatically detects LoRA usage in workflows, checks if they are already downloaded, and downloads missing ones from CivitAI.

## 📦 Included Nodes

This package includes **4 custom nodes** for different use cases:

### 🎯 AutoLoRADetector ⭐ (Recommended)
**Category**: `loaders` → `lora`  
**Best for**: Beginners and quick fixes  
**Purpose**: Simple detection and downloading of missing LoRAs

### 🔧 LoRAAutoDownloader  
**Category**: `loaders` → `lora`  
**Best for**: Advanced users with workflow JSON  
**Purpose**: Manual workflow scanning and LoRA downloading

### 🔄 WorkflowLoRAInterceptor
**Category**: `loaders` → `lora`  
**Best for**: Power users wanting automation  
**Purpose**: Automatic workflow interception and processing

### 📁 LoRADirectoryManager
**Category**: `loaders` → `lora`  
**Best for**: Managing your LoRA collection  
**Purpose**: Directory management and organization tools

## Quick Start for Missing LoRAs

**The simplest way to handle your missing LoRAs:**

1. Add the **Auto LoRA Detector** node to your workflow
2. Add your CivitAI API token
3. Enable `auto_download` 
4. Execute the node - it will detect and download the missing LoRAs from your error message

The node will specifically look for LoRAs mentioned in validation errors like:
- `breastinClass`
- `GoodHands-vanilla`
- `Addams`
- `zyd232sChineseGirl_v16`
- `GoodHands-beta2`

## Features

- **Automatic LoRA Detection**: Scans workflows for LoRA loader nodes
- **Missing LoRA Detection**: Checks if LoRAs exist in your local directory
- **CivitAI Integration**: Automatically downloads missing LoRAs from CivitAI
- **Workflow Interception**: Can hook into the execution system to automatically process all workflows
- **Directory Management**: Tools for managing and organizing your LoRA collection

## Installation

1. Copy the `lora_auto_downloader_package` folder to your ComfyUI custom_nodes directory:
   ```
   ComfyUI/custom_nodes/lora_auto_downloader_package/
   ```

2. Install the required dependencies:
   ```bash
   pip install requests
   ```

3. Restart ComfyUI

## Usage

### Manual LoRA Scanning

Use the **LoRA Auto Downloader** node:

1. Add the node to your workflow
2. Paste your workflow JSON into the `workflow_data` input
3. Add your CivitAI API token
4. Enable `auto_download` to automatically download missing LoRAs
5. Execute the node to scan and download

### Automatic Workflow Interception

Use the **Workflow LoRA Interceptor** node:

1. Add the node to any workflow
2. Enable `enable_auto_mode`
3. Add your CivitAI API token
4. All future workflows will automatically be scanned for missing LoRAs

### Directory Management

Use the **LoRA Directory Manager** node:

1. Add the node to check your LoRA directory status
2. List all LoRAs with file sizes
3. Check for potential duplicates
4. Verify directory permissions and disk space

## 📋 Detailed Node Reference

### 🎯 AutoLoRADetector ⭐
**Display Name**: "Auto LoRA Detector"  
**Category**: `loaders/lora`  
**Best For**: Quick fixes and beginners

**Inputs**:
- `civitai_token` (STRING): Your CivitAI API token
- `auto_download` (BOOLEAN): Whether to download missing LoRAs automatically (default: true)
- `check_missing` (BOOLEAN): Whether to check for missing LoRAs (default: true)
- `trigger_input` (OPTIONAL): Connect any input to trigger the check

**Outputs**:
- `status_report` (STRING): Detailed status of missing LoRAs and downloads
- `missing_loras_list` (STRING): JSON list of missing LoRAs
- `passthrough` (*): Pass-through for workflow connections

**Features**:
- ✅ Detects common missing LoRAs from validation errors
- ✅ Automatically searches CivitAI for best matches
- ✅ Downloads missing LoRAs with progress reporting
- ✅ Simple to use - just add token and run

---

### 🔧 LoRAAutoDownloader
**Display Name**: "LoRA Auto Downloader"  
**Category**: `loaders/lora`  
**Best For**: Advanced users with workflow JSON

**Inputs**:
- `workflow_data` (STRING): JSON workflow data to scan for LoRA usage
- `civitai_token` (STRING): CivitAI API token for downloading models
- `auto_download` (BOOLEAN): Automatically download missing LoRAs (default: true)
- `check_only` (BOOLEAN): Only check without downloading (default: false)
- `passthrough_model` (OPTIONAL MODEL): Model to pass through
- `passthrough_clip` (OPTIONAL CLIP): CLIP to pass through

**Outputs**:
- `status_report` (STRING): Detailed scanning and download report
- `missing_loras` (STRING): JSON list of missing LoRAs with metadata
- `model` (MODEL): Pass-through model
- `clip` (CLIP): Pass-through CLIP

**Features**:
- ✅ Parses complete workflow JSON for LoRA references
- ✅ Supports multiple LoRA loader types (LoraLoader, JsonLoraLoader, etc.)
- ✅ Detailed metadata extraction (strength, node IDs, etc.)
- ✅ Comprehensive error handling and reporting

---

### 🔄 WorkflowLoRAInterceptor
**Display Name**: "Workflow LoRA Interceptor"  
**Category**: `loaders/lora`  
**Best For**: Power users wanting full automation

**Inputs**:
- `enable_auto_mode` (BOOLEAN): Enable automatic scanning for all workflows (default: false)
- `civitai_token` (STRING): CivitAI API token for downloading models
- `download_missing` (BOOLEAN): Automatically download missing LoRAs (default: true)
- `scan_current_workflow` (BOOLEAN): Scan the current workflow manually (default: false)
- `manual_workflow_json` (OPTIONAL STRING): Manually provide workflow JSON to scan

**Outputs**:
- `status` (STRING): Current status of the interceptor
- `missing_loras_report` (STRING): Report of missing LoRAs

**Features**:
- ✅ Hooks into ComfyUI's execution system
- ✅ Automatically processes ALL workflows when enabled
- ✅ Background downloading without user intervention
- ✅ Persistent settings across workflow runs
- ⚠️ Advanced feature - use with caution

---

### 📁 LoRADirectoryManager
**Display Name**: "LoRA Directory Manager"  
**Category**: `loaders/lora`  
**Best For**: Managing and organizing your LoRA collection

**Inputs**:
- `action` (CHOICE): Choose action
  - `list_loras`: List all LoRA files with sizes
  - `check_directory`: Verify directory status and permissions
  - `cleanup_duplicates`: Find potential duplicate files

**Outputs**:
- `report` (STRING): Detailed report based on selected action

**Features**:
- ✅ Lists all LoRAs with file sizes in MB
- ✅ Checks directory permissions and disk space
- ✅ Identifies potential duplicate LoRA files
- ✅ Provides storage and organization insights
- ✅ No download functionality - purely management

## Node Types

### AutoLoRADetector (Recommended for beginners)
- **Purpose**: Simple detection and downloading of missing LoRAs
- **Inputs**:
  - `civitai_token`: Your CivitAI API token
  - `auto_download`: Whether to download missing LoRAs automatically
  - `check_missing`: Whether to check for missing LoRAs
- **Outputs**:
  - `status_report`: Detailed status of missing LoRAs and downloads
  - `missing_loras_list`: JSON list of missing LoRAs
  - `passthrough`: Pass-through for workflow connections

### LoRAAutoDownloader
- **Purpose**: Manual workflow scanning and LoRA downloading
- **Inputs**: 
  - `workflow_data`: JSON workflow to scan
  - `civitai_token`: Your CivitAI API token
  - `auto_download`: Whether to download missing LoRAs
  - `check_only`: Only check without downloading
- **Outputs**: 
  - `status_report`: Detailed status of the scanning operation
  - `missing_loras`: JSON list of missing LoRAs

### WorkflowLoRAInterceptor
- **Purpose**: Automatic workflow interception and processing
- **Inputs**:
  - `enable_auto_mode`: Enable automatic scanning for all workflows
  - `civitai_token`: Your CivitAI API token
  - `download_missing`: Whether to download missing LoRAs
  - `scan_current_workflow`: Scan the current workflow manually
- **Outputs**:
  - `status`: Current status of the interceptor
  - `missing_loras_report`: Report of missing LoRAs

### LoRADirectoryManager
- **Purpose**: Manage and organize your LoRA collection
- **Inputs**:
  - `action`: Choose action (list_loras, check_directory, cleanup_duplicates)
- **Outputs**:
  - `report`: Detailed report of the directory status

## CivitAI API Token

To download LoRAs from CivitAI, you need an API token:

1. Go to [CivitAI](https://civitai.com)
2. Sign in to your account
3. Go to Account Settings > API Keys
4. Generate a new API key
5. Copy the token and paste it into the node's `civitai_token` field

## Supported LoRA Formats

- `.safetensors` (preferred)
- `.ckpt`
- `.pt`

## Download Location

LoRAs are downloaded to: `E:\\ComfyUI_windows_portable\\ComfyUI\\models\\loras`

## Troubleshooting

### Common Issues

1. **"Permission denied" errors**: Ensure ComfyUI has write permissions to the LoRA directory
2. **Download failures**: Check your internet connection and CivitAI token
3. **Node not appearing**: Restart ComfyUI after installation

### Logging

Check the ComfyUI console for detailed logs during downloading and scanning operations.

## 📋 Quick Reference Table

| Node Name | Display Name | Best For | Key Feature |
|-----------|--------------|----------|-------------|
| `AutoLoRADetector` | Auto LoRA Detector ⭐ | Beginners | Simple one-click LoRA detection & download |
| `LoRAAutoDownloader` | LoRA Auto Downloader | Advanced users | Manual workflow JSON scanning |
| `WorkflowLoRAInterceptor` | Workflow LoRA Interceptor | Power users | Automatic background processing |
| `LoRADirectoryManager` | LoRA Directory Manager | Organization | Directory management & cleanup |

## 🎯 Which Node Should I Use?

- **Just want to fix missing LoRAs quickly?** → Use `AutoLoRADetector` ⭐
- **Have a specific workflow JSON to scan?** → Use `LoRAAutoDownloader`
- **Want automatic processing for all workflows?** → Use `WorkflowLoRAInterceptor`
- **Need to manage your LoRA collection?** → Use `LoRADirectoryManager`

## License

This custom node is provided as-is for educational and personal use.
