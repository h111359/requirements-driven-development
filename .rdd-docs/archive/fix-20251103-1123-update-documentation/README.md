# Requirements-Driven Development (RDD)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/h111359/requirements-driven-development)](https://github.com/h111359/requirements-driven-development/releases)
[![Build Status](https://img.shields.io/github/actions/workflow/status/h111359/requirements-driven-development/ci.yml?branch=main)](https://github.com/h111359/requirements-driven-development/actions)

A structured methodology and framework for software development with GitHub Copilot, emphasizing clear requirements documentation, systematic change management, and maintainable codebases.

## Overview

[EDITED] Requirements-Driven Development (RDD) is a methodology that combines traditional requirements engineering principles with modern AI-assisted development practices. It provides a systematic approach to manage requirements, technical specifications, and changes throughout the software development lifecycle using bash-based automation scripts, structured prompts, and Git-integrated workflows.

## Features

- **Structured Documentation**: Organized approach to maintain requirements, technical specifications, and architectural decisions
- **Change Management**: Systematic tracking of changes from inception to archive with timestamped branches
- **Clarity Checklist**: Standardized framework for requirement clarification and refinement through iterative questioning
- **Version Control Integration**: Git-based workflow aligned with development processes using enh/* and fix/* branch patterns
- **AI-Assisted Development**: Optimized for use with GitHub Copilot via structured prompt files in `.github/prompts/`
- **[ADDED] Interactive CLI**: Run `./. rdd/scripts/rdd.sh` without arguments to access an interactive menu system for all operations
- **[ADDED] Modular Scripts**: Domain-specific utility scripts (git, branch, workspace, requirements, clarify, prompt, pr, change) for reusability
- **[ADDED] Workspace Isolation**: Active workspace at `.rdd-docs/workspace/` aligned with current git branch, empty on main
- **[ADDED] Automatic ID Assignment**: Requirements IDs auto-assigned during wrap-up to prevent conflicts in parallel development
- **[ADDED] Archive System**: Completed changes archived to `.rdd-docs/archive/<change-id>/` with metadata

## Installation

```bash
# Clone the repository
git clone https://github.com/h111359/requirements-driven-development.git
cd requirements-driven-development

# Make scripts executable
chmod +x .rdd/scripts/*.sh

# Verify installation
./.rdd/scripts/rdd.sh --version
```

**Prerequisites:**
- Bash 4.0+ (Linux, macOS, WSL on Windows)
- Git
- VS Code (recommended)
- Optional: jq (for JSON processing, fallback available)
- Optional: gh CLI (for GitHub operations, alternative instructions provided)

## Usage

### Quick Start

```bash
# [ADDED] Interactive mode - displays menu with all operations
./.rdd/scripts/rdd.sh

# [ADDED] Or use command-line mode with specific actions:
./.rdd/scripts/rdd.sh change create          # Create new enhancement (interactive)
./.rdd/scripts/rdd.sh change create fix      # Create new fix (interactive)
./.rdd/scripts/rdd.sh branch list            # List branches
./.rdd/scripts/rdd.sh requirements validate  # Validate requirements format
./.rdd/scripts/rdd.sh change wrap-up         # Complete change workflow

# [ADDED] Get help for any domain:
./.rdd/scripts/rdd.sh branch --help
./.rdd/scripts/rdd.sh workspace --help
./.rdd/scripts/rdd.sh requirements --help
```

### [ADDED] Using VS Code with Copilot

1. **Open the project in VS Code**
2. **Use prompt files** from `.github/prompts/`:
   - `rdd.01-initiate.prompt.md` - Start a new change
   - `rdd.02-clarify-requirements.prompt.md` - Clarify requirements
   - `rdd.03-tech-design.prompt.md` - Technical design
   - `rdd.04-prompt-generator.prompt.md` - Generate implementation prompts
   - `rdd.06-execute.prompt.md` - Execute stand-alone prompts
3. **Copilot will guide you** through each workflow phase interactively

### Project Structure

The RDD methodology organizes project documentation in the `.rdd-docs/` directory:

```
.rdd-docs/
├── requirements.md          # Project requirements (reflects latest from main)
├── tech-spec.md            # Technical specifications
├── folder-structure.md     # Repository structure documentation
├── data-model.md           # Data model documentation
├── version-control.md      # Version control strategy
├── clarity-checklist.md    # Requirements clarification checklist
├── backlog.md              # Backlog tracking
├── workspace/              # Current active work (aligned with current branch)
│   ├── change.md / fix.md  # [ADDED] Active change/fix documentation
│   ├── copilot-prompts.md  # [ADDED] Stand-alone prompts tracking
│   ├── open-questions.md   # [ADDED] Clarification questions log
│   ├── requirements-changes.md # [ADDED] Requirements changes to merge
│   ├── .current-change     # [ADDED] JSON config for active change
│   └── log.jsonl           # [ADDED] Prompt execution log
└── archive/                # Historical changes
    ├── <YYYYMMDD-HHmm-change-name>/  # [EDITED] Timestamped archived changes
    └── fixes/              # [ADDED] Bug fixes archive
```

### Core Workflow

1. **[EDITED] Initiate Change**: Use `rdd.sh change create` or prompt `rdd.01-initiate.prompt.md` to create enh/fix branch with workspace
2. **[ADDED] Clarify Requirements**: Use prompt `rdd.02-clarify-requirements.prompt.md` for iterative questioning based on clarity taxonomy
3. **[ADDED] Technical Design**: Use prompt `rdd.03-tech-design.prompt.md` to document technical solution
4. **[ADDED] Generate Implementation Prompts**: Use prompt `rdd.04-prompt-generator.prompt.md` to create stand-alone prompts in `workspace/copilot-prompts.md`
5. **[ADDED] Execute Implementation**: Use prompt `rdd.06-execute.prompt.md` to run stand-alone prompts one by one
6. **[ADDED] Document Changes**: Update `workspace/requirements-changes.md` with [ADDED|MODIFIED|DELETED] prefixes
7. **[ADDED] Wrap-Up**: Use `rdd.sh change wrap-up` to archive workspace, commit, push, and get PR creation instructions
8. **[EDITED] Merge to Main**: Create PR manually or via gh CLI, merge after review, workspace auto-clears when switching back to main

## [ADDED] Available Commands

### Branch Management
```bash
rdd.sh branch create <enh|fix> <name>    # Create new branch
rdd.sh branch delete <name>              # Delete branch
rdd.sh branch delete-merged              # Delete all merged branches
rdd.sh branch status <name>              # Check merge status
rdd.sh branch list [filter]              # List branches
```

### Workspace Management
```bash
rdd.sh workspace init <change|fix>       # Initialize workspace
rdd.sh workspace archive [--keep]        # Archive workspace
rdd.sh workspace backup                  # Create backup
rdd.sh workspace restore                 # Restore from backup
rdd.sh workspace clear                   # Clear workspace
```

### Requirements Management
```bash
rdd.sh requirements validate             # Validate format
rdd.sh requirements merge [--dry-run]    # Merge changes
rdd.sh requirements preview              # Preview merge
rdd.sh requirements analyze              # Analyze impact
```

### Change Workflow
```bash
rdd.sh change create [enh|fix]           # Create new change (interactive)
rdd.sh change wrap-up                    # Complete workflow
```

### Git Operations
```bash
rdd.sh git compare                       # Compare with main
rdd.sh git modified-files                # List modified files
rdd.sh git file-diff <file>              # Show file diff
rdd.sh git push                          # Push current branch
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. [EDITED] Create a feature branch using RDD: `./.rdd/scripts/rdd.sh change create` (interactive)
3. [ADDED] Use the RDD workflow: clarify requirements, design, document changes in `workspace/requirements-changes.md`
4. [ADDED] Wrap up with: `./.rdd/scripts/rdd.sh change wrap-up`
5. Submit a pull request with clear description

[ADDED] **Branch Naming Convention:**
- Enhancements: `enh/YYYYMMDD-HHmm-kebab-case-name`
- Fixes: `fix/YYYYMMDD-HHmm-kebab-case-name`

[ADDED] For detailed contribution guidelines, see `.rdd-docs/version-control.md`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Author**: Hristo M. Hristov
- **Email**: h111359@gmail.com
- **Project Link**: [https://github.com/h111359/requirements-driven-development](https://github.com/h111359/requirements-driven-development)

## Acknowledgments

[EDITED] Inspiration from Spec-Kit and OpenSpec projects. Built with a focus on systematic requirements management, AI-assisted development with GitHub Copilot, and maintainable Git workflows.
