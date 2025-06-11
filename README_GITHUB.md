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

## 🎯 Perfect For

- ✅ **Fixing "LoRA not found" errors** instantly
- ✅ **Sharing workflows** without worrying about missing files
- ✅ **Trying new workflows** from the community
- ✅ **Managing large LoRA collections** efficiently

## 📦 What's Included

| Node | Purpose | Best For |
|------|---------|----------|
| 🎯 **Auto LoRA Detector** ⭐ | One-click missing LoRA detection & download | Beginners & quick fixes |
| 🔧 **LoRA Auto Downloader** | Advanced workflow scanning with JSON input | Power users |
| 🔄 **Workflow Interceptor** | Automatic background processing | Set-and-forget automation |
| 📁 **Directory Manager** | LoRA collection organization | Collection management |

## 🔥 Key Features

- **🤖 Automatic Detection** - Scans workflows for LoRA usage
- **📥 Smart Downloads** - Finds and downloads from CivitAI automatically  
- **🛡️ Safe & Secure** - Filename sanitization and error handling
- **📊 Progress Reports** - Detailed status and download progress
- **🎨 Multiple Formats** - Supports .safetensors, .ckpt, .pt
- **🔧 Flexible Usage** - 4 different nodes for different needs

## 📸 Screenshots

*Coming soon - add screenshots of the nodes in action*

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

## 🎮 Usage Examples

### Basic Usage - Fix Missing LoRAs
```
1. Add "Auto LoRA Detector" node
2. Enter your CivitAI token
3. Enable "auto_download"
4. Run workflow → Missing LoRAs download automatically!
```

### Advanced - Workflow JSON Scanning
```
1. Add "LoRA Auto Downloader" node  
2. Paste your workflow JSON
3. Configure download settings
4. Execute to scan and download
```

## 🔑 CivitAI API Token

Get your free API token:
1. Visit [CivitAI](https://civitai.com)
2. Go to Account Settings → API Keys
3. Generate new API key
4. Copy and paste into the node

## 🌟 Why This Extension?

| Problem | Solution |
|---------|----------|
| ❌ "LoRA not found" errors break workflows | ✅ Automatic detection and download |
| ❌ Manual searching and downloading is tedious | ✅ One-click automation |
| ❌ Sharing workflows requires bundling files | ✅ Recipients can auto-download missing LoRAs |
| ❌ Managing large collections is messy | ✅ Built-in organization tools |

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
git clone https://github.com/LargeModGames/comfyui-lora-auto-downloader.git
cd comfyui-lora-auto-downloader
# Copy to ComfyUI custom_nodes directory
# Make changes and test
```

## 📋 Requirements

- **ComfyUI** (latest version recommended)
- **Python 3.8+**
- **requests** library (usually included with ComfyUI)
- **CivitAI account** (free) for downloads

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Nodes don't appear | Restart ComfyUI after installation |
| Download fails | Check CivitAI token and internet connection |
| Permission errors | Ensure ComfyUI can write to the LoRA directory |

See [full troubleshooting guide](README.md#troubleshooting) for more details.

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
