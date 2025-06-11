# Changelog

All notable changes to the LoRA Auto Downloader will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0-beta] - 2025-06-11

### 🧪 **Initial Beta Release (Private Testing)**

#### Added
- **AutoLoRADetector** node for simple LoRA detection and downloading
- **LoRAAutoDownloader** node for manual workflow scanning
- **WorkflowLoRAInterceptor** node for automatic workflow processing
- **LoRADirectoryManager** node for LoRA collection management
- CivitAI integration for automatic LoRA downloads
- Support for multiple LoRA formats (.safetensors, .ckpt, .pt)
- Comprehensive error handling and logging
- Filename sanitization for safe downloads
- Progress reporting for downloads
- Duplicate detection in LoRA directory
- Directory permission and disk space checking

#### Features
- ✅ Automatic detection of missing LoRAs from validation errors
- ✅ CivitAI API integration with token authentication
- ✅ Multiple node types for different use cases and skill levels
- ✅ Comprehensive workflow JSON parsing
- ✅ Background processing capabilities
- ✅ Directory management and organization tools
- ✅ Cross-platform compatibility (Windows, macOS, Linux)
- ✅ Detailed status reporting and user feedback

#### Documentation
- Complete README with node specifications
- Quick start guide for immediate problem solving
- Detailed installation instructions
- Troubleshooting guide
- Contributing guidelines
- Security policy
- Example workflow files

#### Technical
- Python 3.8+ compatibility
- Requests library dependency
- Integration with ComfyUI's node system
- Proper error handling and validation
- Type hints and documentation
- Modular code structure

### 🔧 Technical Details

#### Supported LoRA Loaders
- `LoraLoader` (standard ComfyUI)
- `LoraLoaderModelOnly`
- `JsonLoraLoader`
- Custom LoRA loader variations

#### File Formats
- `.safetensors` (preferred)
- `.ckpt` (legacy)
- `.pt` (PyTorch)

#### Download Sources
- CivitAI (primary)
- Extensible architecture for additional sources

---

## [Unreleased]

### 🎯 **Public Release (v1.0.0)**
*Planned after thorough private testing*

#### Will Include
- Stable version of all 4 nodes
- Verified CivitAI integration  
- Complete documentation
- Community release and sharing

### Future Planned Features
- HuggingFace integration
- Local model scanning improvements
- Batch download capabilities
- Custom download source configuration
- Advanced matching algorithms
- UI improvements

---

**Note**: This project is currently in **private beta testing**. Public release will come after thorough testing and validation.
