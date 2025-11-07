# Requirements-Driven Development (RDD) 🚀

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/h111359/requirements-driven-development)](https://github.com/h111359/requirements-driven-development/releases)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

> A structured workflow framework for AI-assisted software development that keeps your requirements, code, and documentation in perfect sync.

## 📖 Overview

Requirements-Driven Development (RDD) is a comprehensive framework that transforms how you work with AI coding assistants like GitHub Copilot. It provides:

- **📝 Structured Documentation** - Keep requirements, technical specs, and architecture docs organized and up-to-date
- **🔄 Guided Workflows** - Step-by-step prompts guide you through requirement clarification, implementation, and documentation
- **🤖 AI-Optimized** - Designed specifically for GitHub Copilot and other AI assistants
- **🎯 Change Management** - Track every change from inception through completion with built-in archiving
- **⚡ Cross-Platform** - Pure Python implementation works seamlessly on Windows, Linux, and macOS

**Why RDD?** Traditional development often struggles with keeping documentation synchronized with code changes. RDD solves this by providing automated workflows that ensure your documentation always reflects reality, while leveraging AI to accelerate development.

## ✨ Key Features

### 🎨 Interactive Command Interface
- **Arrow-key navigation menus** for intuitive interaction
- **Domain-based commands** (`change`, `branch`, `workspace`, `requirements`, `config`)
- **Visual feedback** with colors and progress indicators
- **Smart defaults** with configuration management

### 📦 Complete Workflow Automation
- **Initiate** - Create branches with proper naming conventions
- **Clarify** - Structured requirement clarification process
- **Execute** - Guided implementation with stand-alone prompts
- **Update** - Synchronize documentation with code changes
- **Wrap-Up** - Archive workspace and prepare pull requests
- **Clean-Up** - Remove merged branches automatically

### 🛠️ Developer-Friendly Tools
- **Workspace management** - Isolated workspaces per change with automatic archiving
- **Requirements tracking** - Structured format with automatic ID assignment
- **Git integration** - Branch management, conflict detection, sync with main
- **Build system** - Create release packages with installers and checksums
- **VS Code integration** - Prompt recommendations and script auto-approval

### 🌍 Cross-Platform Support
- **Single codebase** - Python implementation works everywhere
- **Python installer only** - Cross-platform installation with intelligent settings merge
- **Consistent experience** - Same commands and workflows on all platforms

## 📋 System Requirements

- **Python 3.7+** - Cross-platform runtime for RDD scripts
- **Git 2.23+** - Version control operations
- **VS Code** - Recommended editor (optional but enhances experience)
- **GitHub Copilot** - AI assistant (optional but recommended)

### Python Command Setup

The RDD framework uses the `python` command (not `python3`) to ensure compatibility across all platforms.

**Windows & macOS**: The `python` command is available by default with modern Python installations.

**Linux**: Most modern distributions include `python` pointing to Python 3. If not available:

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

**Verify installation**:
```bash
python --version  # Should show Python 3.7+
```

## 🚀 Installation

### Option 1: From Release (Recommended)

1. **Download the latest release** from [GitHub Releases](https://github.com/h111359/requirements-driven-development/releases)
   - Download `rdd-v{version}.zip`
   - Verify with `rdd-v{version}.zip.sha256`

2. **Extract the archive**
   ```bash
   # Linux/macOS
   unzip rdd-v1.0.0.zip -d ~/downloads/rdd
   
   # Windows PowerShell
   Expand-Archive rdd-v1.0.0.zip -DestinationPath C:\Downloads\rdd
   ```

3. **Navigate to your target project**
   ```bash
   # Linux/macOS
   cd /path/to/your/project
   
   # Windows
   cd C:\path\to\your\project
   ```

4. **Run the Python installer**
   ```bash
   python ~/downloads/rdd/rdd-v1.0.0/install.py
   ```
   
   Or on Windows:
   ```powershell
   python C:\Downloads\rdd\rdd-v1.0.0\install.py
   ```
   
   The installer provides:
   - ✅ Prerequisites checking (Python 3.7+, Git)
   - ✅ Git repository validation
   - ✅ Automatic VS Code settings merge
   - ✅ .gitignore update
   - ✅ Installation verification

5. **Verify installation**
   ```bash
   python .rdd/scripts/rdd.py --version
   # Output: RDD Framework v1.0.0
   ```

### Option 2: Build from Source

For contributors or those wanting the latest development version:

```bash
# Clone the repository
git clone https://github.com/h111359/requirements-driven-development.git
cd requirements-driven-development

# Build the release package
python scripts/build.py

# Install from the generated build
cd build
# Follow the installation steps from Option 1
```

## 🎯 Quick Start

### 1️⃣ Initialize Your First Change

```bash
cd /path/to/your/project
python .rdd/scripts/rdd.py change create
```

This launches an interactive menu:
- Choose change type (Fix or Enhancement)
- Enter a descriptive name
- Automatically creates a branch and initializes workspace

### 2️⃣ Work on Your Change

The framework uses **GitHub Copilot prompts** to guide you through each phase:

```bash
# In VS Code, use these prompts:
# @workspace /rdd.01-initiate      - Initialize workspace
# @workspace /rdd.02-clarify       - Clarify requirements  
# @workspace /rdd.06-execute       - Implement changes
# @workspace /rdd.07-update-docs   - Update documentation
# @workspace /rdd.08-wrap-up       - Finalize and archive
```

### 3️⃣ Complete Your Change

```bash
# Wrap up and prepare for PR
python .rdd/scripts/rdd.py change wrap-up

# Create pull request on GitHub
# After PR is merged:
python .rdd/scripts/rdd.py branch cleanup
```

## 💻 Usage

### Command Structure

```bash
python .rdd/scripts/rdd.py <domain> <action> [options]
```

### Core Commands

#### Change Management
```bash
# Create new change (interactive)
python .rdd/scripts/rdd.py change create

# Create new change (non-interactive)
python .rdd/scripts/rdd.py change create fix "Login button not working"
python .rdd/scripts/rdd.py change create enh "Add dark mode support"

# Wrap up current change
python .rdd/scripts/rdd.py change wrap-up
```

#### Branch Management
```bash
# Clean up merged branches
python .rdd/scripts/rdd.py branch cleanup

# Clean up specific branch
python .rdd/scripts/rdd.py branch cleanup fix/20251106-login-bug
```

#### Workspace Management
```bash
# Initialize workspace for current change
python .rdd/scripts/rdd.py workspace init change

# Archive workspace
python .rdd/scripts/rdd.py workspace archive

# Clear workspace
python .rdd/scripts/rdd.py workspace clear
```

#### Configuration
```bash
# Show all configuration
python .rdd/scripts/rdd.py config show

# Get specific value
python .rdd/scripts/rdd.py config get defaultBranch

# Set value
python .rdd/scripts/rdd.py config set defaultBranch dev
```

#### Git Operations
```bash
# Update current branch from main
python .rdd/scripts/rdd.py git update-from-main
```

### Workflow Phases

The RDD framework guides you through six phases:

1. **🎬 Initiate** - Clean merged branches and create branch and workspace
   - Use: `python .rdd/scripts/rdd.py change create`
   - Prompt: `/rdd.01-initiate`

2. **❓ Clarify** - Iteratively clarify requirements
   - Prompt: `/rdd.02-clarify`
   - Creates: `open-questions.md`, `requirements-changes.md`

3. **⚙️ Execute** - Implement changes
   - Prompt: `/rdd.06-execute`
   - Uses: Stand-alone prompts from `.rdd.copilot-prompts.md`

4. **📄 Update Docs** - Synchronize documentation
   - Prompt: `/rdd.07-update-docs`
   - Updates: `requirements.md`, `tech-spec.md`, etc.

5. **📦 Wrap-Up** - Archive and finalize
   - Use: `python .rdd/scripts/rdd.py change wrap-up`
   - Prompt: `/rdd.08-wrap-up`
   - Archives workspace, commits changes, pushes to remote


## 📁 Project Structure

After installation, your project will have:

```
your-project/
├── .github/
│   └── prompts/                    # RDD workflow prompts
│       ├── rdd.01-initiate.prompt.md
│       ├── rdd.06-execute.prompt.md
│       ├── rdd.08-wrap-up.prompt.md
│       └── ...
├── .rdd/
│   ├── scripts/                    # RDD automation scripts
│   │   ├── rdd.py                  # Main entry point
│   │   └── rdd_utils.py            # Utility functions
│   └── templates/                  # File templates
│       ├── requirements.md
│       ├── tech-spec.md
│       ├── config.json
│       └── ...
├── .rdd-docs/                      # Your documentation
│   ├── config.json                 # RDD configuration
│   ├── requirements.md             # Project requirements
│   ├── tech-spec.md                # Technical specifications
│   ├── folder-structure.md         # Project structure
│   ├── data-model.md               # Data models
│   ├── workspace/                  # Active work (gitignored)
│   │   ├── .rdd.[fix|enh].[branch-name]
│   │   ├── .rdd.copilot-prompts.md
│   │   └── ...
│   └── archive/                    # Completed changes
│       ├── fix-20251106-login-bug/
│       └── enh-20251107-dark-mode/
└── .vscode/
    └── settings.json               # VS Code settings (merged)
```

### Documentation Files

- **`requirements.md`** - Structured requirements with unique IDs (GF, FR, NFR, TR)
- **`tech-spec.md`** - Architecture, technology stack, and technical decisions
- **`folder-structure.md`** - Repository organization and file locations
- **`data-model.md`** - Configuration schemas and data structures
- **`config.json`** - Framework configuration (default branch, version, timestamps)

### Workspace Lifecycle

1. **Empty** - Clean state when on main branch
2. **Initialized** - Created when starting a change
3. **Active** - Contains work-in-progress files
4. **Archived** - Copied to `.rdd-docs/archive/[branch-name]/` on wrap-up
5. **Cleared** - Workspace emptied after archiving

## 🔧 Building from Source

### Prerequisites
- Python 3.7+
- Git
- All RDD system requirements

### Build Process

```bash
# Clone repository
git clone https://github.com/h111359/requirements-driven-development.git
cd requirements-driven-development

# Run build script
python scripts/build.py
```

The build script:
1. ✅ Extracts version from `rdd.py`
2. ✅ Creates build directory structure
3. ✅ Copies framework files (prompts, scripts, templates)
4. ✅ Generates README with installation instructions
5. ✅ Creates Python installer (install.py)
6. ✅ Packages into `rdd-v{version}.zip`
7. ✅ Generates SHA256 checksum
8. ✅ Cleans up temporary files

**Output**: `build/rdd-v{version}.zip` and `build/rdd-v{version}.zip.sha256`

### Testing the Build

Extract the build archive and run the installer:

```bash
# Extract
cd build
unzip rdd-v1.0.0.zip -d /tmp/rdd-test

# Navigate to your test project
cd /path/to/test/project

# Run installer
python /tmp/rdd-test/rdd-v1.0.0/install.py
```

On Windows:
```powershell
# Extract
cd build
Expand-Archive rdd-v1.0.0.zip -DestinationPath C:\Temp\rdd-test

# Navigate to your test project
cd C:\path\to\test\project

# Run installer
python C:\Temp\rdd-test\rdd-v1.0.0\install.py
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/requirements-driven-development.git
cd requirements-driven-development
```

### 2. Install RDD in the Project

```bash
# The project uses RDD for its own development
python .rdd/scripts/rdd.py --version
```

### 3. Create a Change

```bash
# Use RDD's own workflow
python .rdd/scripts/rdd.py change create enh "your-enhancement-description"
```

### 4. Follow RDD Workflow

- Update requirements in `.rdd-docs/requirements.md`
- Document technical changes in `.rdd-docs/tech-spec.md`
- Use GitHub Copilot prompts to guide implementation
- Keep documentation synchronized with code

### 5. Submit Pull Request

```bash
# Wrap up your change
python .rdd/scripts/rdd.py change wrap-up

# Push and create PR on GitHub
```

### Branch Naming Conventions

- **Fixes**: `fix/YYYYMMDD-HHMM-description`
- **Enhancements**: `enh/YYYYMMDD-HHMM-description`

Examples:
- `fix/20251106-1234-login-button-broken`
- `enh/20251107-0915-add-dark-mode`

### Code Style

- **Python**: Follow PEP 8 style guide
- **Docstrings**: Use Google-style docstrings
- **Type hints**: Use where applicable
- **Comments**: Explain "why", not "what"

### Testing

```bash
# Run tests (when available)
python -m pytest tests/

# Test RDD commands
python .rdd/scripts/rdd.py --version
python .rdd/scripts/rdd.py --help
```

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
