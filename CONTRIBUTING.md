# Contributing to LoRA Auto Downloader

Thank you for your interest in contributing to the LoRA Auto Downloader for ComfyUI! This document provides guidelines for contributing to the project.

## 🚀 How to Contribute

### Reporting Issues
- Use the issue tracker to report bugs or request features
- Include your ComfyUI version, Python version, and OS
- Provide steps to reproduce the issue
- Include relevant error messages or logs

### Suggesting Features
- Check existing issues to avoid duplicates
- Clearly describe the feature and its use case
- Explain why it would be beneficial to the community

### Code Contributions

#### Setting Up Development Environment
1. Fork the repository
2. Clone your fork locally
3. Install ComfyUI and dependencies
4. Copy the extension to your ComfyUI custom_nodes directory
5. Test your changes thoroughly

#### Pull Request Process
1. Create a feature branch from `main`
2. Make your changes with clear, descriptive commits
3. Test your changes with different workflows
4. Update documentation if needed
5. Submit a pull request with a clear description

## 🔧 Development Guidelines

### Code Style
- Follow PEP 8 for Python code style
- Use meaningful variable and function names
- Add docstrings for classes and functions
- Include type hints where appropriate

### Testing
- Test with various LoRA types (.safetensors, .ckpt, .pt)
- Test with different CivitAI models
- Test error handling scenarios
- Verify compatibility with different ComfyUI versions

### Documentation
- Update README.md for new features
- Add docstrings for new functions/classes
- Include usage examples for new nodes
- Update the node reference table if adding new nodes

## 🏷️ Node Development Guidelines

### Creating New Nodes
- Follow the existing node structure pattern
- Use clear, descriptive names
- Include comprehensive input validation
- Provide helpful tooltips and descriptions
- Add proper error handling

### Node Categories
- Use appropriate categories (loaders/lora recommended)
- Consider backward compatibility
- Test with various input combinations

## 🐛 Bug Reports

When reporting bugs, please include:
- ComfyUI version
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs
- Screenshots if applicable

## 💡 Feature Requests

For feature requests, please provide:
- Clear description of the feature
- Use case and benefits
- Proposed implementation approach (if you have ideas)
- Examples of how it would work

## 📋 Code Review Process

All contributions will be reviewed for:
- Functionality and correctness
- Code quality and style
- Documentation completeness
- Compatibility with existing features
- Security considerations (especially for download functionality)

## 🎯 Priority Areas

We're particularly interested in contributions for:
- Additional LoRA source integrations (HuggingFace, etc.)
- Improved LoRA matching algorithms
- Better error handling and user feedback
- Performance optimizations
- UI/UX improvements
- Cross-platform compatibility

## 📞 Getting Help

- Check existing issues and documentation first
- Create an issue for questions or discussion
- Be respectful and constructive in all interactions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for helping make LoRA Auto Downloader better for the ComfyUI community! 🎉
