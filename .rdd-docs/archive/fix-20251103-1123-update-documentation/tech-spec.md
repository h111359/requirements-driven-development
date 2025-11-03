# Technical Specification

> [EDITED] This document describes the technical architecture and implementation details of the Requirements-Driven Development (RDD) framework.

## System Overview
- [EDITED] The RDD framework is a bash-based system integrating with VS Code and GitHub Copilot
- [EDITED] Core functionality provided through modular shell scripts in `.rdd/scripts/`
- [EDITED] Prompts stored in `.github/prompts/` guide user through workflow phases
- [EDITED] Workspace management via `.rdd-docs/workspace/` for active development
- [EDITED] Git-integrated workflow with branch-based change isolation

## Technology Stack
- [EDITED] **Shell**: Bash 4.0+ for scripting automation
- [EDITED] **Version Control**: Git with GitHub integration
- **Documentation**: Markdown format
- [EDITED] **Configuration**: JSON for structured data (.current-change config)
- [EDITED] **Optional Tools**: jq for JSON processing (with fallback), gh CLI for PR operations
- [EDITED] **IDE Integration**: VS Code with GitHub Copilot

## Architecture Patterns
- [EDITED] **Modular Script Design**: Separate utility scripts by functional domain (git, branch, workspace, requirements, clarify, prompt, pr, change)
- [EDITED] **Domain-Based Routing**: Main rdd.sh script routes commands to domain-specific handlers
- [EDITED] **Template-Based Generation**: File templates in `.rdd/templates/` for consistency
- [EDITED] **Workspace Pattern**: Single active workspace at `.rdd-docs/workspace/` aligned with current branch
- [EDITED] **Archive Pattern**: Completed work archived to `.rdd-docs/archive/<change-id>/`
- [EDITED] **Prompt-Driven Workflow**: Structured prompts guide users through each phase

## Component Architecture

### Main Entry Point: rdd.sh
- [ADDED] **Purpose**: Central command router and interactive menu system
- [ADDED] **Responsibilities**: Command-line parsing, domain routing, interactive menu display, help system
- [ADDED] **Dependencies**: Sources all utility scripts (core, git, branch, workspace, requirements, clarify, prompt, pr, change)
- [ADDED] **Interface**: CLI with domain-action pattern, interactive menu when no arguments provided

### Core Utility Scripts
- [ADDED] **core-utils.sh**: Base functions (print, validate, normalize, timestamp, confirm)
- [ADDED] **git-utils.sh**: Git operations (branch info, diff, push, commit, compare with main)
- [ADDED] **branch-utils.sh**: Branch management (create, delete, list, merge status)
- [ADDED] **workspace-utils.sh**: Workspace operations (init, archive, backup, restore, clear, template copy)
- [ADDED] **change-utils.sh**: Change workflow orchestration (create, track, wrap-up)
- [ADDED] **clarify-utils.sh**: Clarification workflow (init, log Q&A, taxonomy)
- [ADDED] **requirements-utils.sh**: Requirements operations (validate, merge, ID assignment, preview)
- [ADDED] **prompt-utils.sh**: Stand-alone prompt management (mark completed, log execution, list)
- [ADDED] **pr-utils.sh**: Pull request operations (create, update, workflow)
- [ADDED] **fix-management.sh**: Fix-specific workflow (init, wrap-up, cleanup)
- [ADDED] **general.sh**: Standalone general operations (compare, merge, analyze)

### Prompt Files (.github/prompts/)
- [ADDED] **rdd.01-initiate.prompt.md**: Change/fix initiation workflow
- [ADDED] **rdd.02-clarify-requirements.prompt.md**: Iterative requirements clarification
- [ADDED] **rdd.03-tech-design.prompt.md**: Technical design phase
- [ADDED] **rdd.04-prompt-generator.prompt.md**: Generate stand-alone prompts for implementation
- [ADDED] **rdd.06-execute.prompt.md**: Execute stand-alone prompts from copilot-prompts.md
- [ADDED] **rdd.G1-update-backlog.prompt.md**: Update backlog from GitHub issues
- [ADDED] **rdd.G2-merge-requirements-changes.prompt.md**: Merge requirements without full wrap-up
- [ADDED] **rdd.G3-detect-requirements-changes.prompt.md**: Detect requirements changes from code diff

### Template Files (.rdd/templates/)
- [ADDED] **change.md**: Enhancement change template (What, Why, Acceptance Criteria)
- [ADDED] **fix.md**: Fix change template (similar structure to change.md)
- [ADDED] **copilot-prompts.md**: Stand-alone prompts tracking template
- [ADDED] **clarity-checklist.md**: Requirements clarity taxonomy checklist
- [ADDED] **requirements-format.md**: Requirements formatting guidelines
- [ADDED] **questions-formatting.md**: User question formatting standards
- [ADDED] **requirements.md**: Main requirements document template
- [ADDED] **tech-spec.md**: Technical specification template
- [ADDED] **folder-structure.md**: Project structure documentation template
- [ADDED] **data-model.md**: Data model documentation template
- [ADDED] **version-control.md**: Version control strategy template
- [ADDED] **backlog.md**: Backlog tracking template

## Data Architecture

### Configuration Files
- [ADDED] **.current-change (JSON)**: Tracks active change with fields: changeName, changeId, branchName, changeType, startedAt, phase, status
- [ADDED] **requirements-changes.md**: Documents [ADDED|MODIFIED|DELETED] requirements with proper prefixes
- [ADDED] **open-questions.md**: Tracks questions with [ ] open, [?] partial, [x] answered markers
- [ADDED] **.archive-info (JSON)**: Archive metadata with archivedAt, changeId, archivedBy fields
- [ADDED] **.id-mapping.txt**: Maps workspace placeholder IDs to final assigned IDs after wrap-up

### Data Flow Patterns
- [ADDED] **Change Creation**: User input → Normalization → Branch creation → Workspace initialization → .current-change creation
- [ADDED] **Clarification**: Questions from taxonomy → User answers → Log to open-questions.md → Requirements changes to requirements-changes.md
- [ADDED] **Requirements Merge**: workspace/requirements-changes.md → Validation → ID assignment → Merge to .rdd-docs/requirements.md → Backup created
- [ADDED] **Archiving**: Workspace files → Copy to archive/<change-id>/ → Create .archive-info → Optional workspace clear

### Logging
- [ADDED] **log.jsonl (JSONL format)**: Stand-alone prompt execution logs with timestamp, promptId, executionDetails, sessionId per line

## Deployment Architecture

### Repository Structure
```
repo-root/
├── .github/
│   ├── prompts/                  # Workflow prompts
│   └── copilot-instructions.md   # Copilot configuration
├── .rdd/
│   ├── scripts/                  # All bash scripts
│   └── templates/                # File templates
├── .rdd-docs/
│   ├── workspace/                # Active workspace (aligned with current branch)
│   ├── archive/                  # Completed changes archive
│   ├── requirements.md           # Main requirements (always reflects latest from main)
│   ├── tech-spec.md              # Technical specification
│   ├── folder-structure.md       # Repository structure docs
│   ├── data-model.md             # Data model
│   ├── version-control.md        # Version control strategy
│   ├── clarity-checklist.md      # Clarity taxonomy
│   └── backlog.md                # Backlog tracking
├── .vscode/
│   └── settings.json             # VS Code configuration (auto-approval, prompts, etc.)
└── scripts/                      # User/project-specific scripts
```

### Git Branch Strategy
- [ADDED] **main/master**: Default branch with latest stable state
- [ADDED] **enh/<YYYYMMDD-HHmm>-<name>**: Enhancement branches with timestamp and kebab-case name
- [ADDED] **fix/<YYYYMMDD-HHmm>-<name>**: Fix branches with timestamp and kebab-case name
- [ADDED] Workspace cleared when on main/master branch
- [ADDED] Workspace populated when on enh/fix branch with .current-change tracking

## Performance
- [ADDED] **Script Execution**: Bash scripts execute in milliseconds for typical operations
- [ADDED] **Git Operations**: Performance depends on repository size and network for remote operations
- [ADDED] **Interactive Menu**: Instant response for user selections
- [ADDED] **File Operations**: Efficient file copy/backup operations using native bash commands

## Security
- [ADDED] **No Credentials in Code**: Scripts do not store or handle credentials directly
- [ADDED] **Git Authentication**: Relies on user's configured git credentials (SSH/HTTPS)
- [ADDED] **GitHub CLI**: Uses gh CLI authentication when available for PR operations
- [ADDED] **File Permissions**: Scripts respect system file permissions
- [ADDED] **Safe Defaults**: Confirmation prompts before destructive operations (branch delete, workspace clear)

## Infrastructure

### Prerequisites
- [ADDED] Bash 4.0+ (Linux, macOS, WSL on Windows)
- [ADDED] Git (version control)
- [ADDED] VS Code (recommended IDE)
- [ADDED] Optional: jq (JSON processing, fallback available)
- [ADDED] Optional: gh CLI (GitHub operations, alternative instructions provided if unavailable)

### Folder Organization
- [ADDED] **Scripts Directory**: .rdd/scripts/ contains all automation bash scripts (executable with chmod +x)
- [ADDED] **Templates Directory**: .rdd/templates/ contains markdown and configuration templates
- [ADDED] **Prompts Directory**: .github/prompts/ contains structured prompt files for Copilot
- [ADDED] **Documentation Root**: .rdd-docs/ contains all project documentation and workspace
- [ADDED] **VS Code Settings**: .vscode/settings.json for IDE integration and auto-approval

### Dependencies
- [ADDED] **No External Package Managers**: Pure bash implementation with no npm, pip, or similar dependencies
- [ADDED] **Graceful Fallbacks**: Scripts detect missing optional tools (jq, gh) and provide alternative approaches
- [ADDED] **Self-Contained**: All required files included in repository

### Third-Party Service Integration
- [ADDED] **GitHub**: Repository hosting, pull requests, issues (via gh CLI or web UI)
- [ADDED] **VS Code + Copilot**: AI-assisted development, prompt execution
- [ADDED] No other external services required
