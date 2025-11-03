# RDD Scripts Documentation

This directory contains the bash scripts that power the Requirements-Driven Development (RDD) framework. These scripts automate workflows, manage requirements, handle git operations, and maintain workspace state.

---

## Table of Contents

1. [Overview](#overview)
2. [Main Entry Point](#main-entry-point)
3. [Utility Scripts](#utility-scripts)
4. [Usage Examples](#usage-examples)
5. [Script Architecture](#script-architecture)
6. [Common Patterns](#common-patterns)

---

## Overview

The RDD scripts are organized as modular utilities that can be used independently or orchestrated through the main `rdd.sh` wrapper script. Each utility script focuses on a specific domain (branches, workspace, requirements, etc.).

### Prerequisites

- **Bash 4.0+**
- **Git**
- **jq** (optional, for JSON processing - graceful fallback if missing)
- **gh CLI** (optional, for PR operations)

### Environment Variables

- `DEBUG=1` - Enable debug output for troubleshooting

---

## Main Entry Point

### `rdd.sh`

The main wrapper script that provides domain-based routing to all utility scripts.

**Usage:**
```bash
# Interactive menu (no parameters)
./rdd.sh

# Command-line mode
./rdd.sh <domain> <action> [options]
```

**Interactive Menu:**
When run without parameters, `rdd.sh` displays an interactive ASCII menu with keyboard navigation:
- 14 menu options covering all major RDD operations
- Number-based selection (1-14)
- Visual banner and formatted layout
- Automatic return to menu after operations
- Exit option (14)

**Available Domains:**
- `branch` - Branch management operations
- `workspace` - Workspace initialization and management  
- `requirements` - Requirements validation and merging
- `change` - Change workflow management (enhancements)
- `fix` - Fix workflow management (bug fixes)
- `clarify` - Clarification phase operations
- `prompt` - Stand-alone prompt management
- `pr` - Pull request operations
- `git` - Git operations and comparisons

**Global Options:**
- `--help, -h` - Show help message
- `--version, -v` - Show version information

**Examples:**
```bash
# Show interactive menu
./rdd.sh

# Get help for any domain
./rdd.sh branch --help
./rdd.sh change --help

# Show main help
./rdd.sh --help

# Use specific commands directly
./rdd.sh change create
./rdd.sh branch list
```

---

## Utility Scripts

### `core-utils.sh`

Core utility functions used across all RDD scripts.

**Key Functions:**

#### Output Functions
- `print_success <message>` - Print success message with ✓ symbol
- `print_error <message>` - Print error message with ✗ symbol
- `print_warning <message>` - Print warning message with ⚠ symbol
- `print_info <message>` - Print info message with ℹ symbol
- `print_step <message>` - Print step message with ▶ symbol
- `print_banner <title> [subtitle]` - Print formatted banner

#### Validation Functions
- `validate_name <name>` - Validate kebab-case format (max 5 words)
- `validate_branch_name <branch>` - Validate branch name format
- `validate_file_exists <path> [description]` - Check if file exists
- `validate_dir_exists <path> [description]` - Check if directory exists

#### Utility Functions
- `get_repo_root` - Get git repository root directory
- `ensure_dir <path>` - Create directory if it doesn't exist
- `get_timestamp` - Get ISO 8601 timestamp (UTC)
- `get_timestamp_filename` - Get timestamp for filenames (YYYYMMDD-HHmm)
- `normalize_to_kebab_case <input>` - Convert any string to kebab-case
- `confirm_action <prompt>` - Ask user for confirmation (y/n)

#### Configuration Functions
- `get_config <key> [config_file]` - Get value from JSON config
- `set_config <key> <value> [config_file]` - Set value in JSON config

**Examples:**
```bash
source .rdd/scripts/core-utils.sh

# Print colored messages
print_success "Operation completed"
print_error "Something went wrong"
print_warning "This is a warning"

# Validate names
validate_name "my-enhancement-name"  # Returns 0 (valid)
validate_name "Invalid Name!"    # Returns 1 (invalid)

# Normalize names
normalized=$(normalize_to_kebab_case "Add User Auth")
echo $normalized  # Output: add-user-auth

# Get timestamps
timestamp=$(get_timestamp)
echo $timestamp   # Output: 2025-11-02T14:30:00Z
```

---

### `git-utils.sh`

Git operations and repository management.

**Key Functions:**

#### Repository Checks
- `check_git_repo` - Verify we're in a git repository (exits if not)
- `check_uncommitted_changes` - Check for uncommitted/untracked files

#### Branch Operations
- `get_default_branch` - Get default branch name (main or master)
- `get_current_branch` - Get current branch name
- `fetch_main` - Fetch latest changes from remote default branch

#### File Comparison
- `compare_with_main` - Show comprehensive comparison with main branch
- `get_modified_files` - List files modified compared to main
- `get_file_diff <file>` - Show diff for specific file vs main

#### Push/Commit Operations
- `push_to_remote [branch]` - Push branch to remote with upstream tracking
- `auto_commit <message>` - Stage all changes and commit

#### User Information
- `get_git_user` - Get "Name <email>" from git config
- `get_last_commit_sha` - Get last commit SHA
- `get_last_commit_message` - Get last commit message (first line)

**Examples:**
```bash
source .rdd/scripts/git-utils.sh

# Check repository status
check_git_repo
check_uncommitted_changes

# Get branch information
current=$(get_current_branch)
default=$(get_default_branch)
echo "On $current, default is $default"

# Compare branches
compare_with_main
get_modified_files

# Show file diff
get_file_diff "src/main.py"

# Commit and push
auto_commit "enh: add new enhancement"
push_to_remote
```

---

### `branch-utils.sh`

Branch management operations.

**Key Functions:**

#### Branch Creation
- `create_branch <type> <name>` - Create new branch (type: enh|fix)
  - Auto-generates timestamp ID
  - Validates name format (kebab-case, max 5 words)
  - Format: `{type}/{YYYYMMDD-HHmm}-{name}`

#### Branch Deletion
- `delete_branch <name> [force] [skip_checks]` - Delete branch locally and remotely
  - `force`: "true" to force delete, "false" for safe delete (default: false)
  - `skip_checks`: "true" to skip uncommitted changes check (default: false)
- `delete_merged_branches` - Delete all merged branches with confirmation

#### Branch Inspection
- `check_merge_status <branch> [base]` - Check if branch is merged
- `list_branches [filter]` - List branches (filter: local, remote, merged, unmerged, all)
- `get_branch_info <branch>` - Show detailed branch information
- `branch_exists <branch> [location]` - Check if branch exists (location: local, remote, any)

**Examples:**
```bash
source .rdd/scripts/branch-utils.sh

# Create new enhancement branch
create_branch "enh" "user-authentication"
# Creates: enh/20251102-1430-user-authentication

# Delete a branch
delete_branch "enh/20251101-1200-old-enhancement"

# Delete all merged branches
delete_merged_branches

# Check merge status
check_merge_status "enh/20251102-1430-user-authentication"

# List branches
list_branches "merged"
list_branches "unmerged"
```

---

### `workspace-utils.sh`

Workspace initialization, archiving, and management.

**Key Functions:**

#### Workspace Initialization
- `init_workspace <type>` - Initialize workspace with templates (type: change|fix)
  - Creates workspace directory
  - Copies relevant templates
  - Initializes tracking files

#### Workspace Archiving
- `archive_workspace <branch> [keep]` - Archive workspace to branch-specific folder
  - `keep`: "true" to keep workspace after archiving (default: false)
  - Creates archive in `.rdd-docs/archive/{branch-name}/`
  - Includes metadata (timestamp, user, last commit)

#### Backup/Restore
- `backup_workspace` - Create timestamped backup of workspace
- `restore_workspace [backup_path]` - Restore from backup (latest if path not specified)

#### Workspace Clearing
- `clear_workspace` - Clear workspace with confirmation prompt
- `clear_workspace_forced` - Clear workspace without confirmation (internal use)

#### Template Management
- `copy_template <name> <destination>` - Copy template with validation
- `create_requirements_changes_template` - Create requirements-changes.md template

#### Workspace Inspection
- `check_workspace_exists` - Check if workspace has content
- `list_workspace_files` - List all workspace files
- `get_workspace_status` - Show detailed workspace status

**Examples:**
```bash
source .rdd/scripts/workspace-utils.sh

# Initialize workspace for an enhancement
init_workspace "change"

# Archive workspace
archive_workspace "enh/20251102-1430-my-enhancement" false

# Backup and restore
backup_workspace
restore_workspace  # Restores from latest backup

# Clear workspace
clear_workspace

# Get status
get_workspace_status
```

---

### `change-utils.sh`

Change workflow orchestration (enhancements and fixes).

**Key Functions:**

#### Change Creation
- `create_change <name> <type>` - Create new change with complete workflow
  - `name`: kebab-case name (automatically normalized)
  - `type`: "enh" (default) or "fix"
  - Creates branch with timestamp ID
  - Initializes workspace
  - Sets up tracking files

#### Change Tracking
- `init_change_tracking <id> <branch> <type>` - Initialize tracking files
  - Creates open-questions.md
  - Creates requirements-changes.md
  - Copies clarity-checklist.md

#### Change Configuration
- `create_change_config <name> <id> <branch> <type>` - Create .current-change config
  - Stores metadata in JSON format
  - Tracks phase and status

#### Change Wrap-up
- `wrap_up_change` - Complete change workflow
  - Archives workspace
  - Creates wrap-up commit
  - Pushes to remote
  - Provides PR creation instructions

**Examples:**
```bash
source .rdd/scripts/change-utils.sh

# Create new enhancement
create_change "user-authentication" "enh"

# Create new fix
create_change "login-bug" "fix"

# Wrap up current change
wrap_up_change
```

---

### `clarify-utils.sh`

Clarification phase management.

**Key Functions:**

#### Clarification Initialization
- `init_clarification` - Initialize clarification phase
  - Copies taxonomy to workspace
  - Creates open-questions.md
  - Updates phase in .current-change

#### Clarification Logging
- `log_clarification <question> <answer> [answeredBy] [sessionId]` - Log Q&A entry
  - Uses JSONL format
  - Auto-escapes JSON with jq (fallback if unavailable)
  - Default answeredBy: "user"
  - Default sessionId: "clarify-YYYYMMDD-HHmm"

#### Template Management
- `copy_taxonomy` - Copy clarity-checklist.md to workspace

#### Clarification Inspection
- `show_clarifications [sessionId]` - Display clarification log entries
- `count_clarifications [sessionId]` - Count clarification entries
- `get_clarification_status` - Show comprehensive clarification status

**Examples:**
```bash
source .rdd/scripts/clarify-utils.sh

# Initialize clarification phase
init_clarification

# Log a clarification
log_clarification "What is the max file size?" "100MB limit" "John Doe"

# Show all clarifications
show_clarifications

# Show clarifications for specific session
show_clarifications "clarify-20251102-1430"

# Get status
get_clarification_status
```

---

### `requirements-utils.sh`

Requirements validation, merging, and ID management.

**Key Functions:**

#### Validation
- `validate_requirements [file]` - Validate requirements-changes.md format
  - Checks for proper prefixes: [ADDED], [MODIFIED], [DELETED]
  - Validates that MODIFIED/DELETED have existing IDs
  - Returns 0 if valid, 1 with warnings if issues found

#### ID Management
- `get_next_id <prefix> [file]` - Get next available ID for section
  - Prefixes: GF, FR, NFR, TR
  - Returns formatted ID like "01", "02", etc.
- `track_id_mapping <old_id> <new_id> [file]` - Track ID changes
  - Logs to .id-mapping.txt
  - Includes timestamp

#### Merge Operations
- `preview_merge` - Preview requirements merge (no changes)
- `merge_requirements [dry_run] [backup]` - Merge requirements-changes.md into requirements.md
  - `dry_run`: "true" for preview only (default: false)
  - `backup`: "true" to create backup (default: false)
  - Auto-assigns IDs to [ADDED] requirements
  - Tracks ID mappings

#### Analysis
- `analyze_requirements_impact` - Analyze impact on requirements

**Examples:**
```bash
source .rdd/scripts/requirements-utils.sh

# Validate requirements format
validate_requirements

# Preview merge
preview_merge

# Merge with backup
merge_requirements false true

# Merge (dry run)
merge_requirements true false

# Analyze impact
analyze_requirements_impact
```

---

### `prompt-utils.sh`

Stand-alone prompt management.

**Key Functions:**

#### Prompt Completion
- `mark_prompt_completed <id> [journal_file]` - Mark prompt as completed
  - Changes `- [ ]` to `- [x]` in copilot-prompts.md
  - Validates prompt exists before marking

#### Prompt Execution Logging
- `log_prompt_execution <id> <details> [sessionId]` - Log execution details
  - Creates JSONL entry in log.jsonl
  - Auto-escapes JSON properly (uses jq if available)
  - Format: `{"timestamp":"...","promptId":"...","executionDetails":"...","sessionId":"..."}`

#### Prompt Listing
- `list_prompts [status] [journal_file]` - List prompts filtered by status
  - Status options: "unchecked", "checked", "all" (default: "all")
  - Displays prompt IDs and titles

**Examples:**
```bash
source .rdd/scripts/prompt-utils.sh

# Mark prompt as completed
mark_prompt_completed "P001"

# Log execution details
log_prompt_execution "P001" "Created user authentication module"

# List unchecked prompts
list_prompts "unchecked"

# List all prompts
list_prompts "all"
```

---


## Interactive Menu

### Overview

Running `rdd.sh` without parameters launches an interactive terminal menu that provides easy access to all RDD operations.

### Features

- **Keyboard Navigation**: Select options using numbers (1-14) and press Enter
- **Visual Layout**: Formatted ASCII banner and organized menu options
- **Interactive Prompts**: Some options will prompt for additional input when needed
- **Return to Menu**: After each operation, press Enter to return to the menu
- **Exit Option**: Choose option 14 to exit the menu

### Menu Options

The interactive menu provides access to:

1. **Create a new change (enhancement)** - Interactive change creation workflow
2. **Create a new fix** - Create a bug fix with prompts for details
3. **Wrap up current change/fix** - Complete and archive the current work
4. **Initialize workspace** - Set up workspace for change or fix
5. **Archive workspace** - Archive current workspace with options
6. **Create a new branch** - Create enhancement or fix branch
7. **List branches** - Display all local branches
8. **Delete branch** - Remove a branch with optional force flag
9. **Validate requirements** - Check requirements-changes.md format
10. **Merge requirements** - Merge changes with optional dry-run
11. **Compare with main branch** - Show detailed comparison
12. **Show version** - Display RDD Framework version
13. **View help** - Show main help documentation
14. **Exit** - Exit the interactive menu

### Usage Example

```bash
# Launch interactive menu
./rdd.sh

# You'll see:
# ╔════════════════════════════════════════════════════════════╗
# ║              RDD Framework - Interactive Menu              ║
# ╚════════════════════════════════════════════════════════════╝
#
# Select an action to perform:
#
# 1) Create a new change (enhancement)    8) Delete branch
# 2) Create a new fix                     9) Validate requirements
# 3) Wrap up current change/fix          10) Merge requirements
# 4) Initialize workspace                11) Compare with main branch
# 5) Archive workspace                   12) Show version
# 6) Create a new branch                 13) View help
# 7) List branches                       14) Exit
#
# ▶ Enter your choice (1-14):

# Enter a number (e.g., 12 for version)
# The corresponding action will execute
# Press Enter to return to the menu
```

### Interactive Options

Some menu options will prompt for additional information:

- **Option 2 (Create a new fix)**: Prompts for fix name
- **Option 4 (Initialize workspace)**: Prompts to select "change" or "fix"
- **Option 6 (Create a new branch)**: Prompts for branch type and name
- **Option 8 (Delete branch)**: Prompts for branch name (optional)
- **Option 10 (Merge requirements)**: Asks if dry-run should be performed

### Compatibility

The interactive menu is compatible with:
- **Bash 4.0+**
- **Zsh** (common terminal emulators)
- **Linux**, **macOS**, and **WSL** environments

---

## Usage Examples

### Complete Change Workflow

```bash
# 1. Create a new enhancement
./rdd.sh change create enh
# Interactive prompts will guide you through:
# - Providing description
# - Entering name (auto-normalized to kebab-case)
# - Confirming normalized name

# 2. Initialize clarification phase
./rdd.sh clarify init

# 3. Log clarifications as you work
./rdd.sh clarify log "How should errors be handled?" "Display toast notification" "Dev Team"

# 4. Make your code changes...

# 5. Update requirements-changes.md
# Add entries like:
# - **[ADDED] User Notification**: System shall display toast notifications for errors
# - **[MODIFIED] [FR-05] Error Handling**: Update to use toast notifications

# 6. Validate requirements format
./rdd.sh requirements validate

# 7. Preview requirements merge
./rdd.sh requirements preview

# 8. Wrap up change (archive, commit, push)
./rdd.sh change wrap-up

# 9. Create PR manually using provided command
# OR use GitHub CLI:
# gh pr create --base main --head <branch> --title "..." --body "..."
```

### Branch Management

```bash
# List all branches
./rdd.sh branch list all

# List only unmerged branches
./rdd.sh branch list unmerged

# Check if branch is merged
./rdd.sh branch status enh/20251101-1200-old-enhancement

# Delete a specific branch
./rdd.sh branch delete enh/20251101-1200-old-enhancement

# Delete all merged branches
./rdd.sh branch delete-merged
```

### Workspace Management

```bash
# Initialize workspace for a change
./rdd.sh workspace init change

# Get workspace status
./rdd.sh workspace status

# Create backup
./rdd.sh workspace backup

# Archive workspace (keeps it)
./rdd.sh workspace archive --keep

# Clear workspace (with confirmation)
./rdd.sh workspace clear

# Restore from backup
./rdd.sh workspace restore
```

### Git Operations

```bash
# Compare current branch with main
./rdd.sh git compare

# List modified files
./rdd.sh git modified-files

# Show diff for specific file
./rdd.sh git file-diff src/parser.py

# Push current branch
./rdd.sh git push
```

---

## Script Architecture

### Dependency Chain

```
rdd.sh (main entry point)
  ├── core-utils.sh (base functions)
  ├── git-utils.sh (depends on: core-utils.sh)
  ├── branch-utils.sh (depends on: core-utils.sh, git-utils.sh)
  ├── workspace-utils.sh (depends on: core-utils.sh, git-utils.sh)
  ├── clarify-utils.sh (depends on: core-utils.sh, workspace-utils.sh)
  ├── change-utils.sh (depends on: core-utils.sh, git-utils.sh, branch-utils.sh, workspace-utils.sh, clarify-utils.sh)
  ├── requirements-utils.sh (depends on: core-utils.sh, git-utils.sh)
  ├── prompt-utils.sh (depends on: core-utils.sh)
```

### Design Principles

1. **Modular**: Each utility script focuses on a single domain
2. **Reusable**: Functions can be sourced and used independently
3. **Fail-Safe**: Validation checks before destructive operations
4. **Interactive**: Confirmation prompts for critical actions
5. **Informative**: Colored output with clear success/error messages
6. **Defensive**: Graceful fallbacks when optional tools (jq, gh) are unavailable

---

## Common Patterns

### Sourcing Scripts

```bash
# Source a utility script
source .rdd/scripts/core-utils.sh

# Check if already sourced (scripts do this internally)
if [ -n "$CORE_UTILS_LOADED" ]; then
    return 0
fi
```

### Error Handling

```bash
# Check function return codes
if ! validate_name "$name"; then
    print_error "Validation failed"
    return 1
fi

# Exit on error (dangerous operations)
set -e
```

### Debug Mode

```bash
# Enable debug output
export DEBUG=1
./rdd.sh branch create enh my-enhancement

# Debug messages will show:
# [DEBUG] Git repository verified
# [DEBUG] No uncommitted changes found
# etc.
```

### Colored Output

```bash
# Use the print functions from core-utils.sh
print_success "Operation completed successfully"
print_error "Something went wrong"
print_warning "This is a warning"
print_info "This is information"
print_step "Starting process..."
```

### User Confirmation

```bash
# Ask for confirmation before destructive operations
if ! confirm_action "Delete all files?"; then
    print_info "Operation cancelled"
    return 0
fi

# Proceed with operation...
```

### JSON Handling

```bash
# Use jq if available, fallback if not
if command -v jq &> /dev/null; then
    # Use jq for robust JSON handling
    jq -r '.key' config.json
else
    # Fallback to simple grep/sed
    grep '"key"' config.json | sed 's/.*: *"\([^"]*\)".*/\1/'
fi
```

---

## Troubleshooting

### Common Issues

**Issue: Permission denied when running scripts**
```bash
# Make scripts executable
chmod +x .rdd/scripts/*.sh
```

**Issue: "command not found: jq"**
```bash
# Scripts work without jq, but install for better experience
# Ubuntu/Debian:
sudo apt-get install jq

# macOS:
brew install jq
```

**Issue: "GitHub CLI (gh) not found"**
```bash
# PR operations require gh CLI
# Install: https://cli.github.com/
# Or manually create PRs on GitHub web UI
```

**Issue: Debug output is too verbose**
```bash
# Disable debug mode
unset DEBUG
# or
export DEBUG=0
```

---

## Contributing

When adding new scripts or functions:

1. Follow existing naming conventions (kebab-case for files, snake_case for functions)
2. Add proper function headers with usage documentation
3. Include validation for required parameters
4. Add colored output using print_* functions
5. Export functions for reusability
6. Update this README.md with new functionality
7. Test with and without optional dependencies (jq, gh)

---

## Version

RDD Framework v1.0.0

## License

See LICENSE file in repository root.
