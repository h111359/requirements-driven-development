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
- **Git 2.23+** - Version control operations
- **VS Code** - Recommended editor (optional but enhances experience)
- **GitHub Copilot** - AI assistant (optional but recommended)

## 🚀 Installation

### Option 1: From Release (Recommended)

1. **Download the latest release** from [GitHub Releases](https://github.com/h111359/requirements-driven-development/releases)
   - Download `rdd-v{version}.zip`
   - Verify with `rdd-v{version}.zip.sha256` (optional)

2. **Extract the archive**
   Extract the archive in a folder

3. **Run the install scripts**
   
   - For Linux - run install.sh
   - For Windows - run install.bat

4. **Choose target folder**
   Follow the instructions to install RDD in the desired destination

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


## 🎯 Quick Start

### 0. Prerequisites

- It is assumed you have installed VS Code
- It is assumed you have GitHub Copilot license
- It is assumed you have set VS Code with GitHub Copilot using your license
- Open .rdd-docs/config.json and ensure the setup is what you expect to be
- Populate the files:
  - .rdd-docs/requirements.md
  - .rdd-docs/tech-spec.md

### 1. Create New Work Iteration

- Run RDD app with terminal menu by executing rdd.bat for Windows or rdd.sh for Linux from the root of the project folder
- Execute the option "Create new iteration" and follow the process to create itteration.


### 2. Define Copilot Prompts

- Open and edit the file `.rdd-docs/workspace/.rdd.copilot-prompts.md` by defining new prompts on the placeholders. Prompts should be as detail as possible, telling the agent what you want to achieve
- After each prompt (or after several prompts defined) - open Copilot chat
- Choose Agent mode and choose some modern model (Claude Sonne 4.5, GPT-5 or similar as capabilities model)
- Execute in the chat `/rdd.06-execute P01` where you should replace P01 with the identifier of the prompt you want the copilot to work on.

### 3. Update Documentation 

- (Optional) You can update your branch with the changes from other developers (if you work simultaneously) from the default branch by running the option "Update from default" in the terminal menu of RDD application.
- When all prompts in `.rdd-docs/workspace/.rdd.copilot-prompts.md` that you want to be executed in this work iteration are done - execute `/rdd.08-document` prompt in the chat without any parameters so the changes to be reflected in the documentation files

### 4. Complete Work Itteration

- Go back to the terminal where the RDD app is running and execute the option "Complete current iteration"
- If you are connected to github repo - make a pull request if needed (RDD intentionally is not making rull requests)
- When the current branch is merged to a permanent branch (like dev or main), you can (optionally) execute "Delete merged branches"
- After completion of the itteration is done, you should be checkouted to the default branch and you can start a new itteration.


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

1. **Check the documentation** in `.rdd-docs/` after installation
2. **Use `--help` flag** for command usage: `python .rdd/scripts/rdd.py --help`
3. **Search existing issues** on GitHub
4. **Create a new issue** with detailed description and error messages

## 🙏 Acknowledgments

- Inspired by **Spec-Kit** and **OpenSpec** projects
- Built for use with **GitHub Copilot** and AI-assisted development
- Thanks to all contributors and early adopters

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ for developers who value clear requirements and maintainable code

</div>
