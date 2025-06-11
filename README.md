# 🚀 ComfyUI LoRA Auto Downloader

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![ComfyUI](https://img.shields.io/badge/ComfyUI-Compatible-green.svg)](https://github.com/comfyanonymous/ComfyUI)

> **Automatically detect and download missing LoRAs for your ComfyUI workflows!** 🎯

Never again struggle with "LoRA not found" errors! This extension automatically detects missing LoRAs in your workflows and downloads them from CivitAI with a single click.

## ⚡ Quick Start

1. **Install** → Copy to `ComfyUI/custom_nodes/`
2. **Restart** → Restart ComfyUI
3. **Add Node** → Find "Auto LoRA Detector" under `loaders` > `lora`
4. **Add Token** → Get your [CivitAI API token](https://civitai.com/user/account)
5. **Run** → Missing LoRAs download automatically! 🎉

## 🚨 Important Usage Notes

### 🔄 **RESTART REQUIRED** After Downloads
⚠️ **After LoRAs are downloaded, you MUST restart ComfyUI** to see them in your Load LoRA nodes. ComfyUI only scans the LoRA directory on startup.

### 🎯 **Recommended Workflow Setup**
For best results, use **both nodes together**:
- **Auto LoRA Detector** (for manual testing with `test_mode=True`)
- **Workflow LoRA Interceptor** (for automatic background processing)

This provides both manual control and automatic detection.

⚠️ **Note**: You may need to **run the Workflow LoRA Interceptor twice** after ComfyUI startup to properly initialize it.

### 📝 **Check for Name Variations**
Downloaded LoRAs may have **slightly different names** than expected:
- Different versions, author conventions, or CivitAI naming

**Always check your Load LoRA dropdown** after download to select the newly available file!

## 🎯 Perfect For

- ✅ **Fixing "LoRA not found" errors** instantly
- ✅ **Sharing workflows** without worrying about missing files
- ✅ **Trying new workflows** from the community
- ✅ **Managing large LoRA collections** efficiently

## 📦 Included Nodes

This package includes **4 custom nodes** for different use cases:

| Node | Purpose | Best For | Key Feature |
|------|---------|----------|-------------|
| 🎯 **Auto LoRA Detector** ⭐ | One-click missing LoRA detection & download | Beginners & quick fixes | Simple one-click LoRA detection & download |
| 🔧 **LoRA Auto Downloader** | Advanced workflow scanning with JSON input | Power users | Manual workflow JSON scanning |
| 🔄 **Workflow Interceptor** | Automatic background processing | Set-and-forget automation | Automatic background processing |
| 📁 **Directory Manager** | LoRA collection organization | Collection management | Directory management & cleanup |

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

## 🔥 Key Features

- **🤖 Automatic Detection** - Scans workflows for LoRA usage
- **📥 Smart Downloads** - Finds and downloads from CivitAI automatically  
- **🛡️ Safe & Secure** - Filename sanitization and error handling
- **📊 Progress Reports** - Detailed status and download progress
- **🎨 Multiple Formats** - Supports .safetensors, .ckpt, .pt
- **🔧 Flexible Usage** - 4 different nodes for different needs
- **🗂️ Directory Management** - Tools for managing and organizing your LoRA collection
- **🔄 Workflow Interception** - Can hook into the execution system to automatically process all workflows

## 🚀 Installation

### Method 1: Manual Installation (Recommended)

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/LargeModGames/comfyui-lora-auto-downloader.git
# Restart ComfyUI
```

### Method 2: ComfyUI Manager

*Coming soon - will be available through ComfyUI Manager*

### Method 3: Download ZIP

1. Download the [latest release](https://github.com/LargeModGames/comfyui-lora-auto-downloader/releases)
2. Extract to `ComfyUI/custom_nodes/`
3. Restart ComfyUI

### Manual Installation Steps

1. Copy the `lora_auto_downloader_package` folder to your ComfyUI custom_nodes directory:
   ```
   ComfyUI/custom_nodes/lora_auto_downloader_package/
   ```

2. **Dependencies are automatically handled** - The `requests` library is typically included with ComfyUI
   - If you encounter import errors, use your ComfyUI's Python environment:
   ```bash
   # For portable ComfyUI installations:
   ComfyUI/python_embeded/python.exe -m pip install requests
   
   # For regular Python installations with ComfyUI:
   python -m pip install requests
   ```

3. Restart ComfyUI

## 🎮 Usage Examples

### Quick Start for Missing LoRAs

**The simplest way to handle your missing LoRAs:**

1. Add the **Auto LoRA Detector** node to your workflow
2. Add your CivitAI API token  
3. Enable `auto_download` and `test_mode` for testing
4. Execute the node - it will detect and download missing LoRAs

### Advanced Usage with Workflow JSON
```
1. Add "LoRA Auto Downloader" node
2. Enter your CivitAI token
3. Paste workflow JSON into the text field
4. Run → Scans and downloads all missing LoRAs
```

## 🔍 Smart Matching Features

The extension uses **enhanced name matching** to find LoRAs even when names don't match exactly:

- ✅ Handles version differences, case variations, and naming conventions


### Manual LoRA Scanning

Use the **LoRA Auto Downloader** node:

1. Add the node to your workflow
2. Paste your workflow JSON into the `workflow_data` input
3. Add your CivitAI API token
4. Enable `auto_download` to automatically download missing LoRAs
5. Execute the node to scan and download

### Advanced - Workflow JSON Scanning
```
1. Add "LoRA Auto Downloader" node  
2. Paste your workflow JSON
3. Configure download settings
4. Execute to scan and download
```

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

## 🎯 Which Node Should I Use?

- **Just want to fix missing LoRAs quickly?** → Use `AutoLoRADetector` ⭐
- **Have a specific workflow JSON to scan?** → Use `LoRAAutoDownloader`
- **Want automatic processing for all workflows?** → Use `WorkflowLoRAInterceptor`
- **Need to manage your LoRA collection?** → Use `LoRADirectoryManager`

## 🔑 CivitAI API Token

Get your free API token:
1. Visit [CivitAI](https://civitai.com)
2. Go to Account Settings → API Keys
3. Generate new API key
4. Copy and paste into the node

To download LoRAs from CivitAI, you need an API token:

1. Go to [CivitAI](https://civitai.com)
2. Sign in to your account
3. Go to Account Settings > API Keys
4. Generate a new API key
5. Copy the token and paste it into the node's `civitai_token` field

## 📋 Requirements

- **ComfyUI** (latest version recommended)
- **Python 3.8+**
- **requests** library (usually included with ComfyUI)
- **CivitAI account** (free) for downloads

## 📁 Supported Formats

- `.safetensors` (preferred)
- `.ckpt`
- `.pt`

## 💾 Download Location

LoRAs are downloaded to your ComfyUI LoRA directory, which is automatically detected using ComfyUI's folder system. This is typically the `models/loras/` folder within your ComfyUI installation, but the exact path depends on your ComfyUI setup and configuration.

## 🌟 Why This Extension?

| Problem | Solution |
|---------|----------|
| ❌ "LoRA not found" errors break workflows | ✅ Automatic detection and download |
| ❌ Manual searching and downloading is tedious | ✅ One-click automation |
| ❌ Sharing workflows requires bundling files | ✅ Recipients can auto-download missing LoRAs |
| ❌ Managing large collections is messy | ✅ Built-in organization tools |

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Nodes don't appear | Restart ComfyUI after installation |
| **Downloaded LoRAs not visible** | **⚠️ RESTART ComfyUI after downloads** |
| Download fails | Check CivitAI token and internet connection |
| **LoRA has different name** | **Check Load LoRA dropdown for variations** |
| Permission errors | Ensure ComfyUI can write to the LoRA directory |
| "requests" import error | Use ComfyUI's Python: `ComfyUI/python_embeded/python.exe -m pip install requests` |

### ⚠️ Critical: Restart After Downloads
**ComfyUI only scans the LoRA directory on startup.** After downloading new LoRAs:
1. **Stop ComfyUI completely**
2. **Restart ComfyUI** 
3. **Check your Load LoRA nodes** for the new files

### 🔍 Finding Downloaded LoRAs
Downloaded LoRAs may have different names than expected:
- Look for **similar names** in your Load LoRA dropdown
- Check for **version differences** (v1.5, v2.0, etc.)
- Search for **author names** or keywords from the original name

1. **"Permission denied" errors**: Ensure ComfyUI has write permissions to the LoRA directory
2. **Download failures**: Check your internet connection and CivitAI token
3. **Node not appearing**: Restart ComfyUI after installation
4. **Import errors**: If you get "No module named 'requests'", install it using ComfyUI's Python environment (see installation instructions above)

### Logging

Check the ComfyUI console for detailed logs during downloading and scanning operations.

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
git clone https://github.com/LargeModGames/comfyui-lora-auto-downloader.git
cd comfyui-lora-auto-downloader
# Copy to ComfyUI custom_nodes directory
# Make changes and test
```

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) for the amazing framework
- [CivitAI](https://civitai.com) for providing the LoRA repository
- The ComfyUI community for inspiration and feedback

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=LargeModGames/comfyui-lora-auto-downloader&type=Date)](https://star-history.com/#LargeModGames/comfyui-lora-auto-downloader&Date)

---

<div align="center">

**Made with ❤️ for the ComfyUI community**

[Report Bug](https://github.com/LargeModGames/comfyui-lora-auto-downloader/issues) • [Request Feature](https://github.com/LargeModGames/comfyui-lora-auto-downloader/issues) • [Discussions](https://github.com/LargeModGames/comfyui-lora-auto-downloader/discussions)

</div>
