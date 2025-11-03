# Technical Specification

## System Overview

The RDD (Requirements-Driven Development) framework is a structured workflow automation system designed to guide developers through requirement clarification, implementation, and documentation processes. The system consists of:

- **Prompt-driven workflows**: Structured markdown prompts that guide AI agents and developers through RDD phases
- **Script automation**: Bash (Linux) and PowerShell (Windows) scripts that automate repetitive tasks
- **Documentation management**: Structured documentation files that track requirements, changes, and project state
- **Workspace management**: Isolated workspace for active development with archiving capabilities

## Technology Stack

### Programming Languages & Scripts
- **Bash**: Primary scripting language for Linux/macOS automation (`.sh` files)
- **PowerShell**: Windows-compatible scripting language with identical functionality to Bash scripts (`.ps1` files)
- **Markdown**: Documentation format for prompts, requirements, and guides
- **JSON/JSONL**: Configuration and logging data format

### Development Tools
- **Git**: Version control and branch management
- **jq**: JSON parsing and manipulation in Bash scripts (with fallback to basic text processing)
- **VS Code**: Recommended IDE with GitHub Copilot integration
- **GitHub Copilot**: AI assistant configured for RDD workflow execution

### Dependencies
- Git 2.x+
- Bash 4.x+ (for Linux scripts)
- PowerShell 5.1+ or PowerShell Core 7.x+ (for Windows scripts)
- jq (optional, improves JSON handling)

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
The main entry point (`rdd.sh` or `rdd.ps1`) uses a domain-based routing pattern:
```
rdd.sh <domain> <action> [options]
```
Examples:
- `rdd.sh branch create enh my-feature`
- `rdd.sh workspace init change`
- `rdd.sh requirements merge`

This replaces the previous standalone script approach (e.g., `fix-management.sh`) with a unified command interface.

### Template-Based File Generation
All workspace files are generated from templates stored in `.rdd/templates/` or `src/{platform}/.rdd/templates/`, ensuring consistency across projects and changes.

### Phase-Based Workflow
The framework follows a sequential phase workflow:
1. **Initiate**: Create branch and initialize workspace
2. **Clarify**: Iteratively clarify requirements using structured questions
3. **Execute**: Implement changes following clarified requirements
4. **Update Docs**: Synchronize documentation with implementation
5. **Wrap-Up**: Archive workspace, merge requirements, prepare for PR

## Component Architecture

### Script Components

#### Main Entry Point
- **File**: `src/{linux|windows}/.rdd/scripts/rdd.{sh|ps1}`
- **Purpose**: Unified command interface with domain routing
- **Responsibilities**:
  - Parse command-line arguments
  - Route commands to appropriate domain handlers
  - Display help and version information
  - Source utility scripts

#### Utility Scripts (Domain-Specific)
Each utility script exports functions for a specific domain:

1. **core-utils**: Foundation functions
   - Color output (Print-Success, Print-Error, Print-Info, Print-Warning)
   - Validation (Validate-Name, Normalize-ToKebabCase)
   - Configuration management (Get-Config, Set-Config)
   - Timestamp generation

2. **git-utils**: Git operations
   - Repository validation
   - Branch operations
   - Stashing and merging
   - Diff and comparison

3. **branch-utils**: Branch lifecycle
   - Branch creation with naming conventions
   - Branch deletion (single and bulk)
   - Merge status checking
   - Post-merge cleanup

4. **workspace-utils**: Workspace management
   - Workspace initialization
   - Archiving with metadata
   - Backup and restore
   - Complete workspace clearing

5. **requirements-utils**: Requirements handling
   - Format validation
   - Requirements merging
   - ID assignment for new requirements
   - Impact analysis

6. **change-utils**: Change workflow
   - Change creation
   - Change tracking
   - Workflow orchestration
   - Completion and wrap-up

7. **clarify-utils**: Clarification phase
   - Clarification initialization
   - Question logging
   - Clarification status tracking

8. **prompt-utils**: Prompt management
   - Prompt completion marking
   - Execution logging
   - Status checking

### Cross-Platform Implementation

#### File Structure
```
src/
├── linux/
│   ├── .rdd/
│   │   ├── scripts/         # Bash scripts (.sh)
│   │   ├── templates/       # Template files
│   ├── .github/
│   │   └── prompts/         # Linux-specific prompts
│   └── ...
└── windows/
    ├── .rdd/
    │   ├── scripts/         # PowerShell scripts (.ps1)
    │   ├── templates/       # Template files
│   ├── .github/    
    │   └── prompts/         # Windows-specific prompts
    └── ...
```

#### Script Equivalence
Each Bash script has a PowerShell equivalent with:
- Identical function names and signatures
- Same command-line interface
- Equivalent functionality
- Platform-appropriate syntax

Example mapping:
- `src/linux/.rdd/scripts/rdd.sh` ↔ `src/windows/.rdd/scripts/rdd.ps1`
- `src/linux/.rdd/scripts/core-utils.sh` ↔ `src/windows/.rdd/scripts/core-utils.ps1`

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

### Installation
The RDD framework is installed by:
1. Cloning the repository
2. Ensuring script execution permissions (`chmod +x src/{platform}/.rdd/scripts/*.{sh|ps1}`)
3. Configuring VS Code settings for auto-approval and prompt recommendations

### Platform Selection
Users select the appropriate script platform:
- **Linux/macOS**: Use scripts in `src/linux/.rdd/scripts/*.sh`
- **Windows**: Use scripts in `src/windows/.rdd/scripts/*.ps1`

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
- **jq**: Optional JSON processor (improves script functionality)

## Migration Notes

### Recent Changes
1. **fix-management.sh removal**: All fix management functionality consolidated into `rdd.sh` with domain routing
2. **change.md template removal**: The `change.md` template file removed from `.rdd/templates/`; workspace no longer includes this file during initialization
3. **PowerShell script addition**: Complete PowerShell implementation added for Windows compatibility in `src/windows/.rdd/scripts/`

### Deprecated Components
- ~~`fix-management.sh`~~ - Replaced by `rdd.sh fix` commands
- ~~`.rdd/templates/change.md`~~ - Template removed; no longer used in workspace
