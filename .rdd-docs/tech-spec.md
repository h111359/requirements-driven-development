# Technical Specification

## System Overview

The RDD (Requirements-Driven Development) framework is a structured workflow automation system designed to guide developers through requirement clarification, implementation, and documentation processes. The system consists of:

- **Prompt-driven workflows**: Structured markdown prompts that guide AI agents and developers through RDD phases
- **Script automation**: Bash (Linux) and PowerShell (Windows) scripts that automate repetitive tasks
- **Documentation management**: Structured documentation files that track requirements, changes, and project state
- **Workspace management**: Isolated workspace for active development with archiving capabilities

## Technology Stack

### Programming Languages & Scripts
- **Python**: Primary scripting language for cross-platform automation (`.py` files)
- **Bash**: Legacy scripting language for Linux/macOS (archived, replaced by Python)
- **PowerShell**: Legacy Windows-compatible scripting language (in `src/windows/`)
- **Markdown**: Documentation format for prompts, requirements, and guides
- **JSON/JSONL**: Configuration and logging data format

### Development Tools
- **Git**: Version control and branch management
- **VS Code**: Recommended IDE with GitHub Copilot integration
- **GitHub Copilot**: AI assistant configured for RDD workflow execution

### Dependencies
- **Python 3.7+**: Required for running all RDD scripts
- **Git 2.23+**: Required for version control operations
- **python-is-python3** (Linux only): Optional package to make `python` command available on older Linux systems

## Architecture Patterns

### Domain-Driven Script Organization
The framework uses a domain-based architecture where functionality is organized into specialized utility scripts:

- **Core utilities**: Common functions (logging, validation, configuration)
- **Git utilities**: Git operations and comparisons
- **Branch utilities**: Branch creation, deletion, and management
- **Workspace utilities**: Workspace initialization, archiving, and cleanup
- **Requirements utilities**: Requirements validation and merging
- **Change utilities**: Change workflow orchestration
- **Clarify utilities**: Clarification phase management
- **Prompt utilities**: Prompt execution tracking

### Command Routing Pattern
The main entry point (`rdd.py`) uses a domain-based routing pattern:
```
python .rdd/scripts/rdd.py <domain> <action> [options]
```
Examples:
- `python .rdd/scripts/rdd.py branch create enh my-feature`
- `python .rdd/scripts/rdd.py workspace init change`
- `python .rdd/scripts/rdd.py requirements merge`

**Cross-Platform Compatibility**: The framework uses the `python` command (not `python3`) to ensure compatibility across Windows, Linux, and macOS. On older Linux systems where the `python` command is not available, users can install the `python-is-python3` package or create an alias/symlink.

This Python implementation replaced the previous bash scripts (`rdd.sh`) which are now archived.

### Template-Based File Generation
All workspace files are generated from templates stored in `.rdd/templates/` or `src/{platform}/.rdd/templates/`, ensuring consistency across projects and changes.

### Phase-Based Workflow
The framework follows a sequential phase workflow:
1. **Initiate**: Create branch and initialize workspace
2. **Clarify**: Iteratively clarify requirements using structured questions
3. **Execute**: Implement changes following clarified requirements
4. **Update Docs**: Synchronize documentation with implementation
5. **Wrap-Up**: Archive workspace, merge requirements, prepare for PR
6. **Clean-Up**: After PR merge, clean up local environment and remove merged branches

## Component Architecture

### Script Components

#### Main Entry Point
- **File**: `.rdd/scripts/rdd.py`
- **Purpose**: Unified command interface with domain routing
- **Responsibilities**:
  - Parse command-line arguments
  - Route commands to appropriate domain handlers
  - Display help and version information
  - Execute workflow operations

**Note**: Legacy bash implementation (rdd.sh and utility scripts) archived in workspace during migration to Python.

#### Utility Scripts (Domain-Specific)
The Python implementation (`rdd_utils.py`) provides utility functions organized by domain:

1. **Core utilities**: Foundation functions
   - Color output (print_success, print_error, print_info, print_warning)
   - Validation (validate_name, normalize_to_kebab_case)
   - Configuration management (get_config, set_config)
   - Timestamp generation

2. **Git utilities**: Git operations
   - Repository validation
   - Branch operations
   - Stashing and merging
   - Diff and comparison

3. **Branch utilities**: Branch lifecycle
   - Branch creation with naming conventions
   - Branch deletion (single and bulk)
   - Merge status checking
   - Post-merge cleanup

4. **Workspace utilities**: Workspace management
   - Workspace initialization
   - Archiving with metadata
   - Backup and restore
   - Complete workspace clearing

5. **Requirements utilities**: Requirements handling
   - Format validation
   - Requirements merging
   - ID assignment for new requirements
   - Impact analysis

6. **Change utilities**: Change workflow
   - Change creation
   - Change tracking
   - Workflow orchestration
   - Completion and wrap-up

7. **Clarify utilities**: Clarification phase
   - Clarification initialization
   - Question logging
   - Clarification status tracking

8. **Prompt utilities**: Prompt management
   - Prompt completion marking
   - Execution logging
   - Status checking

**Legacy Note**: Previous bash implementation (branch-utils.sh, change-utils.sh, etc.) has been archived.

### Cross-Platform Implementation

**Current Implementation**: Python-based (`rdd.py` and `rdd_utils.py`)
- Cross-platform compatible (Windows, Linux, macOS)
- Single codebase for all platforms
- Native Python libraries for file operations, JSON handling, and subprocess management

**Legacy Implementation**: Bash and PowerShell scripts (archived)
- Previously maintained separate implementations for Linux (bash) and Windows (PowerShell)
- Located in `src/linux/.rdd/scripts/` and `src/windows/.rdd/scripts/`
- Bash scripts from `.rdd/scripts/` archived to workspace during Python migration

## Data Architecture

### Configuration Files
- **Change config**: `.rdd.[fix|enh].<branch-name>` - JSON file tracking current change
- **Archive metadata**: `.archive-metadata` - JSON file documenting archived changes
- **Execution log**: `log.jsonl` - JSONL file logging prompt executions

### Documentation Files
- **Requirements**: `.rdd-docs/requirements.md` - Structured requirements with IDs
- **Technical spec**: `.rdd-docs/tech-spec.md` - Technical architecture and design
- **Data model**: `.rdd-docs/data-model.md` - Configuration and file schemas
- **Folder structure**: `.rdd-docs/folder-structure.md` - Project organization

### Workspace Files
- **Stand-alone prompts**: `.rdd.copilot-prompts.md` - Checklist of executable prompts
- **Open questions**: `open-questions.md` - Clarification questions and answers
- **Requirements changes**: `requirements-changes.md` - Requirements modifications for merge

Note: The `change.md` template has been **removed** from the framework and is no longer created in workspace.

## Deployment Architecture

### Build System
The RDD framework uses a Python-based build system to create release packages:

#### Build Script (scripts/build.py)
- **Purpose**: Creates cross-platform release archives with all necessary files
- **Version Management**: Extracts version from `RDD_VERSION` constant in rdd.py
- **Archive Creation**: Generates single `rdd-v{version}.zip` file containing:
  - Framework files (.rdd/scripts/, .rdd/templates/)
  - Prompt files (.github/prompts/)
  - Installation scripts (install.py, install.sh, install.ps1)
  - Documentation (README.md, LICENSE)
  - VS Code settings template (.vscode/settings.json)
- **Verification**: Generates SHA256 checksum file for archive integrity verification
- **Cleanup**: Removes temporary build directories, keeping only archive and checksum

#### Build Process Steps
1. Extract version from rdd.py and validate SemVer format
2. Create build directory structure
3. Copy framework files (prompts, scripts, templates, LICENSE, settings)
4. Generate README.md with platform-specific installation instructions
5. Generate install.py (cross-platform Python installer)
6. Generate install.sh (interactive Bash installer for Linux/macOS)
7. Generate install.ps1 (interactive PowerShell installer for Windows)
8. Create ZIP archive with nested directory structure
9. Generate SHA256 checksum file
10. Clean up temporary staging directories

### Installation System
The RDD framework provides three installation methods to accommodate different user preferences:

#### Option 1: Interactive Shell Installers (Recommended)
Platform-specific interactive installers with visual folder navigation:

**Linux/macOS (install.sh)**:
- Visual folder navigation using arrow keys
- Current directory display with parent/subfolder navigation
- Git repository validation before installation
- Confirmation prompts for existing installations
- Calls Python installer with selected directory

**Windows (install.ps1)**:
- Identical functionality to Bash installer
- PowerShell-native key handling and UI
- Cross-platform consistent user experience

**Navigation Features**:
- Arrow keys (↑↓) for menu navigation
- Enter to select directory or enter subfolder
- [..] option for parent directory navigation
- [SELECT THIS DIRECTORY] option to install in current location
- Q key to quit installation
- Real-time path display

#### Option 2: Direct Python Installation
**Python Installer (install.py)**:
- Cross-platform installer using Python standard library only
- Pre-flight checks:
  - Python version verification (≥ 3.7)
  - Git installation check
  - Target directory validation (must be Git repository)
- Existing installation detection with upgrade warnings
- Interactive prompts for target directory
- Automated file operations:
  - Copy prompts to `.github/prompts/`
  - Copy framework to `.rdd/`
  - Intelligent VS Code settings merge
  - .gitignore update with workspace exclusion
- Post-installation verification:
  - File existence checks
  - RDD command test (`python .rdd/scripts/rdd.py --version`)
- Clear success/error messages with next steps

**Settings Merge Logic**:
- **Array settings** (chat.promptFilesRecommendations, chat.tools.terminal.autoApprove):
  - Handles both object and array formats
  - Appends unique values without duplicates
- **Object settings** (files.associations):
  - Merges keys, RDD values overwrite existing
- **Editor settings** (editor.rulers):
  - Replaces with RDD requirements (80, 120 character columns)

#### Option 3: Manual Installation
For users who prefer manual control:
- Step-by-step file copying instructions
- Platform-specific commands (PowerShell/Bash)
- Manual VS Code settings merge guidance
- Manual .gitignore update steps

### Platform Compatibility
- **Python-based**: Single implementation works on all platforms (Windows, Linux, macOS)
- **No platform-specific scripts needed**: Python provides cross-platform compatibility
- **Python command**: Uses `python` (not `python3`) for universal compatibility
- **Interactive installers**: Platform-specific scripts provide optimal user experience

### VS Code Integration
The framework integrates with VS Code through:
- **Chat prompt recommendations**: `.vscode/settings.json` configures `chat.promptFilesRecommendations`
- **Script auto-approval**: Auto-approves script execution for `.rdd/scripts/` directory
- **JSONL file association**: Associates `*.jsonl` files with jsonlines language

## Performance

### Script Execution
- **Startup time**: < 1 second for command routing
- **Workspace initialization**: < 5 seconds
- **Requirements merge**: < 10 seconds for typical changes

### Scalability
- Supports unlimited concurrent changes (via separate branches)
- Archive storage scales linearly with number of completed changes
- No performance degradation with large requirements files (< 1000 requirements)

## Security

### Script Execution Safety
- Scripts use `set -e` (Bash) or `$ErrorActionPreference = 'Stop'` (PowerShell) to fail fast
- No arbitrary code execution from user input
- Git operations use local repository only (no remote credential handling)

### Data Protection
- All data stored in local git repository
- No external service dependencies
- Workspace files cleared after archiving (no sensitive data retention)

### Access Control
- Relies on OS-level file permissions
- Git credentials managed by user's git configuration
- No authentication or authorization system within framework

## Infrastructure

### Project Folder Structure
```
repo-root/
├── .github/                      # GitHub-specific files
│   ├── prompts/                  # Shared prompt templates
│   └── copilot-instructions.md   # Copilot configuration
├── .rdd/                         # Legacy scripts (deprecated)
│   ├── scripts/                  # To be migrated to src/{platform}
│   └── templates/                # Shared templates
├── src/                          # Platform-specific implementations
│   ├── linux/                    # Linux/macOS scripts
│   └── windows/                  # Windows scripts
├── .rdd-docs/                    # Documentation and workspace
│   ├── workspace/                # Active development workspace
│   ├── archive/                  # Completed change archives
│   └── *.md                      # Project documentation
├── build/                        # Build artifacts (gitignored)
└── scripts/                      # Project-specific automation
```

### Database & Storage
- **No database required**: All data in text files (Markdown, JSON, JSONL)
- **Git as storage**: Version history and branching managed by git
- **Archive storage**: Filesystem-based archives in `.rdd-docs/archive/`

### Third-Party Dependencies
- **GitHub Copilot**: AI assistant for executing prompts (optional but recommended)
- **Git**: Required for version control operations
- **Python 3.8+**: Required for running RDD scripts

## Migration Notes

### Recent Changes
1. **Python migration**: All bash scripts migrated to Python for true cross-platform compatibility
2. **Bash scripts archived**: Legacy bash implementation (9 scripts) moved to workspace archive
3. **Unified codebase**: Single Python implementation replaces separate bash/PowerShell codebases
4. **fix-management.sh removal**: All fix management functionality consolidated into `rdd.py` with domain routing
5. **change.md template removal**: The `change.md` template file removed from `.rdd/templates/`; workspace no longer includes this file during initialization
6. **Cross-platform command standardization**: All prompt files updated to use `python` command instead of `python3` for Windows/Linux/macOS compatibility
7. **Python setup documentation**: README.md updated with clear instructions for installing `python` command on Linux systems using `python-is-python3` package

### Deprecated Components
- ~~All bash scripts (.sh)~~ - Replaced by Python implementation (`rdd.py` and `rdd_utils.py`); archived in workspace
- ~~`fix-management.sh`~~ - Replaced by `rdd.py` commands
- ~~`.rdd/templates/change.md`~~ - Template removed; no longer used in workspace
- ~~PowerShell scripts (.ps1) in `src/windows/`~~ - No longer needed with Python implementation
