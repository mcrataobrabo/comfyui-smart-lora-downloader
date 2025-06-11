# 🧪 Testing Checklist

## 🚨 **TESTING PHASE - PRIVATE REPOSITORY**

This extension is currently in **private testing** before public release. Complete all tests below before making the repository public.

## ✅ **Core Functionality Tests**

### AutoLoRADetector Node
- [ ] **Node appears** in ComfyUI under `loaders` > `lora`
- [ ] **Basic functionality** - node loads without errors
- [ ] **Token input** - accepts CivitAI token properly
- [ ] **Missing LoRA detection** - correctly identifies missing LoRAs
- [ ] **CivitAI search** - successfully searches for LoRAs
- [ ] **Download functionality** - actually downloads LoRA files
- [ ] **File saving** - saves to correct directory with proper names
- [ ] **Status reporting** - provides clear feedback to user
- [ ] **Error handling** - gracefully handles network/API errors

### LoRAAutoDownloader Node  
- [ ] **Node appears** and loads properly
- [ ] **Workflow JSON parsing** - correctly extracts LoRA references
- [ ] **Multiple LoRA types** - detects LoraLoader, JsonLoraLoader, etc.
- [ ] **Download functionality** - downloads missing LoRAs
- [ ] **Passthrough inputs** - model/clip inputs work correctly
- [ ] **Status reporting** - detailed scanning reports

### WorkflowLoRAInterceptor Node
- [ ] **Node appears** and loads properly  
- [ ] **Auto-mode toggle** - enable/disable functionality works
- [ ] **Background processing** - doesn't interfere with normal workflows
- [ ] **Token persistence** - remembers settings across runs
- [ ] **Error handling** - doesn't crash ComfyUI if enabled

### LoRADirectoryManager Node
- [ ] **Node appears** and loads properly
- [ ] **List LoRAs** - correctly lists all LoRA files with sizes
- [ ] **Check directory** - reports directory status and permissions
- [ ] **Duplicate detection** - finds potential duplicate files
- [ ] **No download issues** - doesn't attempt downloads (as intended)

## 🌐 **CivitAI Integration Tests**

### API Functionality
- [ ] **Token validation** - handles valid/invalid tokens properly
- [ ] **Search accuracy** - finds relevant LoRAs for search terms
- [ ] **Download speed** - reasonable download performance
- [ ] **File integrity** - downloaded files are not corrupted
- [ ] **Rate limiting** - handles API rate limits gracefully
- [ ] **Network errors** - handles connectivity issues

### Specific LoRA Tests
Test with these known missing LoRAs from your original error:
- [ ] **breastinClass** - search and download
- [ ] **GoodHands-vanilla** - search and download  
- [ ] **Addams** - search and download
- [ ] **zyd232sChineseGirl_v16** - search and download
- [ ] **GoodHands-beta2** - search and download

## 🖥️ **Platform Tests**

- [ ] **Windows 10/11** - full functionality
- [ ] **Different ComfyUI versions** - compatibility check
- [ ] **Different Python versions** - 3.8, 3.9, 3.10, 3.11
- [ ] **Portable vs installed** - works in both setups

## 🔒 **Security & Safety Tests**

- [ ] **Token security** - tokens not logged or exposed
- [ ] **File validation** - downloaded files are safe
- [ ] **Path traversal** - filename sanitization works
- [ ] **Permission handling** - proper file system permissions
- [ ] **Error messages** - no sensitive information leaked

## 🎯 **User Experience Tests**

- [ ] **First-time setup** - easy for new users
- [ ] **Error messages** - clear and helpful
- [ ] **Documentation accuracy** - README matches actual behavior
- [ ] **Node tooltips** - helpful input descriptions
- [ ] **Progress feedback** - users know what's happening

## 🚫 **Edge Case Tests**

- [ ] **No internet connection** - graceful failure
- [ ] **Invalid CivitAI token** - proper error handling
- [ ] **Missing LoRA directory** - creates or reports error
- [ ] **Full disk space** - handles storage issues
- [ ] **Very large LoRAs** - handles big file downloads
- [ ] **Malformed workflow JSON** - doesn't crash
- [ ] **Empty/corrupted LoRA files** - detection and handling

## 📊 **Performance Tests**

- [ ] **Large workflows** - handles complex workflows efficiently
- [ ] **Multiple simultaneous downloads** - no conflicts
- [ ] **Memory usage** - doesn't cause memory leaks
- [ ] **ComfyUI performance** - doesn't slow down normal operation
- [ ] **Startup time** - reasonable load time for nodes

## 🐛 **Known Issues to Fix**

Document any issues found during testing:
- [ ] Issue 1: ___________________________
- [ ] Issue 2: ___________________________
- [ ] Issue 3: ___________________________

## 📝 **Testing Notes**

### Test Environment
- **ComfyUI Version**: _______________
- **Python Version**: _______________
- **Operating System**: _______________
- **Test Date**: _______________

### Test Results Summary
- **Total Tests**: _____ / _____
- **Passed**: _____
- **Failed**: _____
- **Critical Issues**: _____

## 🎯 **Release Readiness Criteria**

Before making the repository public, ensure:
- [ ] **All core functionality** tests pass
- [ ] **No critical bugs** that break ComfyUI
- [ ] **CivitAI integration** works reliably
- [ ] **Documentation** is accurate and complete
- [ ] **Error handling** is robust
- [ ] **User experience** is smooth for beginners

## 🚀 **Post-Testing Actions**

When testing is complete:
- [ ] Update version to `1.0.0` (remove beta)
- [ ] Update CHANGELOG.md with final features
- [ ] Make repository public
- [ ] Create first official release
- [ ] Share with ComfyUI community

---

**Testing Status**: 🚧 **IN PROGRESS** 
**Target Public Release**: TBD after thorough testing
