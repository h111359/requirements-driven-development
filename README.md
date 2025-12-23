# Requirements-Driven Development (RDD) 🚀

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/h111359/requirements-driven-development)](https://github.com/h111359/requirements-driven-development/releases)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

> A structured workflow framework for AI-assisted software development based on your requirements and documentation.

## 📖 Overview

Requirements-Driven Development (RDD) is a framework for development augmented with GitHub Copilot. It provides:

- **📝 Structured Documentation** - Keep requirements, technical specs, and architecture docs organized and up-to-date
- **🔄 Guided Workflows** - Step-by-step process from requirement clarification, prompts generations, prompts execution and documentation update
- **🤖 AI-Optimized** - Designed specifically for GitHub Copilot
- **🎯 Change Management** - Built in change managemetn and version control using git and github
- **⚡ Cross-Platform** - Pure Python implementation works seamlessly on Windows and Linux

**Why RDD?** To boost and speed the traditional development while keeping documentation synchronized with the code changes. 

## 📋 System Requirements

- **Python 3.7+** - Cross-platform runtime for RDD scripts
- **AI assistant** - (optionally to be GitHub Copilot but recommended)

## Recommended  

- **Git 2.23+** - Version control operations
- **VS Code** - Recommended editor (optional but enhances experience)

## 🚀 Installation

### **Get the Latest Release**

1. **Download the latest release** from [GitHub Releases](https://github.com/h111359/requirements-driven-development/releases)
   - Download `rdd-v{version}.zip`
   - Verify with `rdd-v{version}.zip.sha256` (optional)

2. **Extract the archive**
   Extract the folder `.rdd` from the archive in your repo folder

### Python Command Setup for Linux

The RDD framework uses the `python` command (not `python3`) to ensure compatibility across all platforms. Most modern distributions include `python` pointing to Python 3. If not available:

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install python-is-python3

# Fedora/RHEL/CentOS
sudo dnf install python-unversioned-command

# Arch Linux
sudo pacman -S python
```

**Alternative**: Create an alias or symlink:
```bash
# Add to ~/.bashrc or ~/.zshrc
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc

# Or create a symlink
sudo ln -s /usr/bin/python3 /usr/local/bin/python
```

### Recommended setup for GitHub

The following steps are not included in the installation. They add additional convinience in case you are using GitHub Copilot in Visual Studio Code, but are not mandatory so RDD to work.

#### GitHub execute prompt

For convenience (if you work with GitHub copilot) you can create a file `.github/prompts/rdd.execute.promppt.md` with the following content:

```
Follow the instructions in `.rdd/prompt-snippets/execution.md`
```

#### VSCode shortcuts and script autoapprove

Add in `.vscode/settings.json` the following entries (if not exist already):

```
{
  "chat.promptFilesRecommendations": {
    "rdd.execute": true
  },
  "chat.tools.terminal.autoApprove": {
    "python .rdd/src/": true
  }
}
```


## 🎯 Start RDD

- Start the application running (from the root folder of the repo) 
```
python .rdd/src/rdd.py
```

Alternatively you can run:

Windows:
```
.rdd/src/rdd.bat
```

Linux:
```
.rdd/src/rdd.bat
```

- When you start the application, a Web UI will be opened in your browser. You can find the user guide in the menu of the Web UI.


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for complete details.

## 💬 Support

### Documentation
- **GitHub Repository**: [requirements-driven-development](https://github.com/h111359/requirements-driven-development)
- **Issues**: [Report bugs or request features](https://github.com/h111359/requirements-driven-development/issues)
- **Releases**: [Download latest version](https://github.com/h111359/requirements-driven-development/releases)

### Contact
- **Author**: Hristo M. Hristov
- **Email**: h111359@gmail.com
- **GitHub**: [@h111359](https://github.com/h111359)

### Getting Help

TBD

## 🙏 Acknowledgments

- Inspired by **Spec-Kit** and **OpenSpec** projects
- Built for use with **GitHub Copilot** and AI-assisted development
- Thanks to all contributors and early adopters

---

**⭐ Star this repo if you find it useful!**


