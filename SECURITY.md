# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 🔒 For Security Issues

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please:

1. **Email**: Send details to [security@yourproject.com] (replace with actual contact)
2. **Include**: 
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if you have one)

### 📧 What to Include

- **Vulnerability Description**: Clear explanation of the issue
- **Reproduction Steps**: How to reproduce the vulnerability
- **Impact Assessment**: What could an attacker do?
- **Environment Details**: ComfyUI version, OS, Python version
- **Proof of Concept**: Code or screenshots (if safe to share)

### ⏰ Response Timeline

- **Initial Response**: Within 48 hours
- **Assessment**: Within 1 week
- **Fix Timeline**: Depends on severity, but we aim for:
  - Critical: 1-3 days
  - High: 1 week
  - Medium: 2 weeks
  - Low: 1 month

### 🛡️ Security Considerations

This extension handles:
- **Network requests** to CivitAI and other sources
- **File downloads** and writes to disk
- **User tokens** for API authentication
- **Workflow data** parsing

### 🔐 Best Practices for Users

1. **Protect Your Tokens**: Never share your CivitAI API tokens
2. **Verify Downloads**: Be cautious with auto-download features
3. **Monitor Directory**: Check what files are being downloaded
4. **Update Regularly**: Keep the extension updated
5. **Review Permissions**: Ensure ComfyUI has appropriate file permissions

### 🚨 Common Security Concerns

- **Malicious LoRAs**: We cannot verify the safety of downloaded LoRA files
- **Token Exposure**: Keep your API tokens secure
- **Directory Traversal**: We sanitize filenames, but always verify
- **Network Security**: Downloads happen over HTTPS when possible

### 📋 Disclosure Policy

- We follow responsible disclosure practices
- Security fixes will be released as soon as possible
- We'll credit researchers who responsibly report issues
- Public disclosure will happen after fixes are available

## 🤝 Acknowledgments

We appreciate security researchers who help keep our project safe for the community.

---

**Note**: This is a community project. While we take security seriously, users should always exercise caution when downloading and using AI models from external sources.
