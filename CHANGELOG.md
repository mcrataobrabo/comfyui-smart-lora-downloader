# Changelog

All notable changes to the LoRA Auto Downloader will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-06-12

### 🛠️ **Bug Fixes & Improvements**

#### Fixed
- Indentation issues in `auto_lora_detector.py` that were causing import failures
- Problems preventing extension from loading correctly in ComfyUI

#### Improved
- Code structure and readability
- Removed unused debug code

## [1.0.1] - 2025-06-11

### 🚀 **Enhanced Matching & Reliability**

#### Added
- **LoRANameMatcher** utility class for advanced name matching algorithms
- **Test Mode** in Auto LoRA Detector for manual testing with specific LoRA names
- **Multi-strategy search approach** with improved result ranking
- **Enhanced name normalization** with better word boundary detection
- **Keyword extraction** from LoRA names for improved matching
- **Real-world test cases** validation with problematic LoRA names

#### Improved
- **Similarity threshold lowered** from 0.3 to 0.2 for better coverage
- **Search result processing** with duplicate removal and better ranking
- **Error messages** now show search strategies used and similarity scores
- **camelCase word splitting**
- **Version pattern removal** for better matching across different versions
- **Case sensitivity handling** in name comparison
- **Fallback mechanisms** when enhanced matching is unavailable

#### Fixed
- **Name matching accuracy** for LoRAs with different naming conventions between ComfyUI and CivitAI
- **Fuzzy matching reliability** with Levenshtein distance calculations
- **Search strategy ordering** to prioritize more accurate matches
- **Edge cases** in name normalization and keyword extraction

#### Documentation
- ✅ Added restart requirement after downloads
- ✅ Added recommended dual-node setup instructions  
- ✅ Added name variation warnings for users
- ✅ Added Workflow Interceptor initialization notes
- ✅ Enhanced troubleshooting section with matching examples

#### Technical
- **Graceful degradation** when optional dependencies are missing
- **Backward compatibility** with fallback to simple string matching
- **Comprehensive logging** for debugging matching issues
- **Performance optimizations** in search and matching algorithms

---

## [1.0.0] - 2025-06-11

### 🎉 **Initial Public Release**

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

#### Enhanced Matching Features
- **Similarity threshold**: 0.2 for better coverage
- **Multiple search strategies**: Original name, normalized, keyword-based
- **Fuzzy matching**: Levenshtein distance algorithm
- **Name normalization**: camelCase splitting, punctuation handling
- **Version pattern removal**: Better matching across version differences
- **Duplicate result filtering**: Improved result ranking

---
