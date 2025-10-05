# SCATED

A project template for **SCATED** (Spec-Controlled Arranged Tasks Execution Development) - an automated, task-driven development methodology powered by GitHub Copilot.

## Overview

This template provides a complete project scaffolding system that automatically generates prompts, instructions, folder structures, and documentation to establish a systematic development workflow. It enables structured task creation, execution tracking, and comprehensive project documentation through GitHub Copilot integration.

### Key Features

- 🚀 **Automated Project Setup** - Complete project structure generation with one command
- 📋 **Task-Driven Development** - Structured task creation and execution workflow
- 📖 **Auto-Documentation** - Automatic generation and maintenance of project documentation
- 🔄 **Progress Tracking** - Comprehensive task status monitoring and execution logging
- 🎯 **Copilot Integration** - Optimized prompts and instructions for GitHub Copilot

## Prerequisites

- **Visual Studio Code** with GitHub Copilot extension enabled
- **GitHub Copilot** subscription (required for template functionality)

## Quick Start

### 1. Clone and Setup

```bash
# Clone this template to your new project directory
git clone https://github.com/h111359/github-copilot-template.git your-project-name
cd your-project-name

# Remove the original git history (optional)
rm -rf .git
git init
```

### 2. Initialize Project Structure

1. Open the project folder in **Visual Studio Code**
2. Open **GitHub Copilot Chat** (Ctrl+Shift+I / Cmd+Shift+I)
3. Execute the setup command:
   ```
   /setup-project
   ```

### 3. Project Ready

Once the setup completes, your project will contain:
- Complete folder structure with documentation templates
- Configured GitHub Copilot instructions and prompts
- Task management system
- Development guidelines and architecture documentation

**📖 Important:** After setup completion, open the newly generated `README.md` file for detailed usage instructions and workflow documentation.

## What Gets Generated

The setup process creates a comprehensive project structure including:

- **`.vscode/`** - VS Code workspace configuration
- **`.github/`** - Copilot instructions and automated prompts
- **`docs/`** - Complete documentation suite (requirements, architecture, guides)
- **`src/`** - Source code directory structure
- **Task Management System** - Automated task creation and execution workflow

## Support

For questions, issues, or contributions, please refer to the project's GitHub repository or documentation generated after setup.

---
