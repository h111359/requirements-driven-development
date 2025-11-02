#!/bin/bash

# change-utils.sh
# Utility script for change workflow management in the RDD framework
# Orchestrates complete change creation and wrap-up workflows

# Prevent multiple sourcing
[[ -n "${CHANGE_UTILS_SOURCED:-}" ]] && return
readonly CHANGE_UTILS_SOURCED=1

# Source dependencies
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/core-utils.sh"
source "$SCRIPT_DIR/git-utils.sh"
source "$SCRIPT_DIR/branch-utils.sh"
source "$SCRIPT_DIR/workspace-utils.sh"
source "$SCRIPT_DIR/clarify-utils.sh"

# Get repository root and paths
REPO_ROOT=$(get_repo_root)
WORKSPACE_DIR="$REPO_ROOT/.rdd-docs/workspace"
TEMPLATE_DIR="$REPO_ROOT/.rdd/templates"

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHANGE CREATION WORKFLOW
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Create a new change with complete workflow
# Orchestrates: validation, ID generation, branch creation, workspace initialization
# Arguments:
#   $1 - change_name: The name of the change (kebab-case)
#   $2 - change_type: Type of change ('enh' or 'fix', default: 'enh')
# Returns:
#   0 on success
#   1 on error (invalid name/type, branch exists, etc.)
# Output:
#   Success messages and next steps
create_change() {
    local change_name="$1"
    local change_type="${2:-enh}"
    
    # Validate required parameters
    if [ -z "$change_name" ]; then
        print_error "Change name is required"
        echo "Usage: create_change <change-name> [type]"
        echo "  type: enh (default) or fix"
        return 1
    fi
    
    # Validate change type
    if [[ "$change_type" != "enh" && "$change_type" != "fix" ]]; then
        print_error "Invalid change type '$change_type'"
        echo "Valid types: enh, fix"
        return 1
    fi
    
    # Validate change name (kebab-case, max 5 words)
    if ! validate_name "$change_name"; then
        return 1
    fi
    
    # Generate change ID (YYYYMMDD-HHmm format)
    local date_time=$(date +"%Y%m%d-%H%M")
    local change_id="${date_time}-${change_name}"
    local branch_name="${change_type}/${change_id}"
    
    # Check if branch already exists
    if branch_exists "$branch_name" "local"; then
        print_error "Branch '$branch_name' already exists"
        return 1
    fi
    
    print_step "Creating change: $change_name ($change_type)"
    
    # Ensure .rdd-docs folder exists
    if [ ! -d "$REPO_ROOT/.rdd-docs" ]; then
        mkdir -p "$REPO_ROOT/.rdd-docs"
        print_success "Created .rdd-docs folder"
    fi
    
    # Check for required files in .rdd-docs/ and copy templates if missing
    local required_files=(requirements.md tech-spec.md data-model.md folder-structure.md version-control.md clarity-checklist.md)
    for file in "${required_files[@]}"; do
        if [ ! -f "$REPO_ROOT/.rdd-docs/$file" ]; then
            if [ -f "$TEMPLATE_DIR/$file" ]; then
                cp "$TEMPLATE_DIR/$file" "$REPO_ROOT/.rdd-docs/$file"
                print_success "Copied template for missing $file to .rdd-docs/$file"
            else
                print_warning "Template not found: $TEMPLATE_DIR/$file"
            fi
        fi
    done
    
    # Switch to main, pull latest, create new branch
    print_info "Switching to main branch..."
    local default_branch=$(get_default_branch)
    git checkout "$default_branch" || return 1
    
    print_info "Pulling latest changes..."
    git pull || return 1
    
    print_info "Creating branch: $branch_name"
    git checkout -b "$branch_name" || return 1
    print_success "Created and checked out branch: $branch_name"
    
    # Initialize workspace
    print_info "Initializing workspace..."
    init_workspace "$change_type" || return 1
    
    # Initialize change tracking files
    print_info "Initializing change tracking..."
    init_change_tracking "$change_id" "$branch_name" "$change_type" || return 1
    
    # Create change configuration
    print_info "Creating change configuration..."
    create_change_config "$change_name" "$change_id" "$branch_name" "$change_type" || return 1
    
    echo ""
    print_success "Change workspace initialized successfully!"
    echo "  - Branch: ${branch_name}"
    echo "  - Change ID: ${change_id}"
    echo "  - Workspace: .rdd-docs/workspace/"
    echo ""
    print_info "Next steps:"
    echo "  1. Edit .rdd-docs/workspace/change.md with your change details"
    echo "  2. Run clarification prompt: Use .github/prompts/rdd.02-clarify-requirements.prompt.md"
    
    return 0
}

# Export function
export -f create_change

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHANGE TRACKING INITIALIZATION
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Initialize change tracking files
# Creates: clarification-log.jsonl, open-questions.md, requirements-changes.md
# Arguments:
#   $1 - change_id: The change ID (YYYYMMDD-HHmm-name format)
#   $2 - branch_name: The branch name (enh/fix/change-id)
#   $3 - change_type: Type of change ('enh' or 'fix')
# Returns:
#   0 on success
#   1 on error
init_change_tracking() {
    local change_id="$1"
    local branch_name="$2"
    local change_type="$3"
    local change_name="${change_id#*-*-}" # Extract name from YYYYMMDD-HHmm-name
    
    # Validate parameters
    if [ -z "$change_id" ] || [ -z "$branch_name" ] || [ -z "$change_type" ]; then
        print_error "Missing required parameters for change tracking initialization"
        echo "Usage: init_change_tracking <change-id> <branch-name> <change-type>"
        return 1
    fi
    
    # Initialize clarification-log.jsonl
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    cat > "$WORKSPACE_DIR/clarification-log.jsonl" << EOF
{"timestamp":"$timestamp","question":"Change created","answer":"New change '${change_name}' (${change_type}) initialized in workspace","answeredBy":"system","sessionId":"init-${change_id}"}
EOF
    print_success "Initialized clarification-log.jsonl"
    
    # Initialize open-questions.md using clarify-utils
    create_open_questions_template || return 1
    
    # Initialize requirements-changes.md
    cat > "$WORKSPACE_DIR/requirements-changes.md" << 'EOFREQ'
# Requirements Changes

> This file documents changes to be made to the main requirements.md file.
> Each statement is prefixed with [ADDED|MODIFIED|DELETED] to indicate the type of change.
>
> **For detailed formatting guidelines, see:** `.rdd/templates/requirements-format.md`

## Format Guidelines

- **[ADDED]**: New requirement not present in current requirements.md
- **[MODIFIED]**: Change to an existing requirement (include the old requirement ID/text for reference)
- **[DELETED]**: Requirement to be removed from requirements.md

---

## General Functionalities

<!-- Add general functionality changes here -->

---

## Functional Requirements

<!-- Add functional requirement changes here -->

---

## Non-Functional Requirements

<!-- Add non-functional requirement changes here -->

---

## Technical Requirements

<!-- Add technical requirement changes here -->

EOFREQ
    print_success "Created requirements-changes.md template"
    
    # Copy clarity-checklist.md to workspace if available
    if [ -f "$REPO_ROOT/.rdd-docs/clarity-checklist.md" ]; then
        cp "$REPO_ROOT/.rdd-docs/clarity-checklist.md" "$WORKSPACE_DIR/clarity-checklist.md"
        print_success "Copied clarity-checklist.md to workspace"
    fi
    
    return 0
}

# Export function
export -f init_change_tracking

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHANGE CONFIGURATION
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Create change configuration file
# Writes .current-change JSON with all required fields
# Arguments:
#   $1 - change_name: The name of the change
#   $2 - change_id: The change ID (YYYYMMDD-HHmm-name format)
#   $3 - branch_name: The branch name (enh/fix/change-id)
#   $4 - change_type: Type of change ('enh' or 'fix')
# Returns:
#   0 on success
#   1 on error
# Output:
#   Creates .rdd-docs/workspace/.current-change JSON file
create_change_config() {
    local change_name="$1"
    local change_id="$2"
    local branch_name="$3"
    local change_type="$4"
    
    # Validate parameters
    if [ -z "$change_name" ] || [ -z "$change_id" ] || [ -z "$branch_name" ] || [ -z "$change_type" ]; then
        print_error "Missing required parameters for change config"
        echo "Usage: create_change_config <change-name> <change-id> <branch-name> <change-type>"
        return 1
    fi
    
    # Create config file
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    cat > "$WORKSPACE_DIR/.current-change" << EOF
{
  "changeName": "${change_name}",
  "changeId": "${change_id}",
  "branchName": "${branch_name}",
  "changeType": "${change_type}",
  "startedAt": "${timestamp}",
  "phase": "init",
  "status": "in-progress"
}
EOF
    
    print_success "Created .current-change config file"
    return 0
}

# Export function
export -f create_change_config

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHANGE WRAP-UP WORKFLOW
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Wrap up a change with complete workflow
# Orchestrates: archive, commit, push, PR creation
# Returns:
#   0 on success
#   1 on error
# Output:
#   Success messages and PR information
wrap_up_change() {
    local current_branch=$(git branch --show-current)
    
    # Validate we're on an enh/fix branch
    if [[ ! "$current_branch" =~ ^(enh|fix)/ ]]; then
        print_error "Wrap-up can only be executed from an enh or fix branch"
        print_error "Current branch: $current_branch"
        return 1
    fi
    
    print_banner "CHANGE WRAP-UP WORKFLOW"
    
    # Extract change type and name from branch
    local change_type="${current_branch%%/*}"
    local change_info="${current_branch#*/}"
    
    # Archive workspace
    print_step "1. Archiving workspace contents"
    local archive_relative
    if ! archive_relative=$(archive_workspace "$current_branch" false); then
        print_error "Failed to archive workspace"
        return 1
    fi
    print_success "Workspace archived to $archive_relative"
    
    # Create wrap-up commit
    print_step "2. Creating wrap-up commit"
    local commit_message="${change_type}: ${change_info} wrap-up"
    
    git add -A
    if git diff --cached --quiet; then
        print_warning "No changes staged for commit - skipping commit creation"
    else
        if git commit -m "$commit_message"; then
            print_success "Wrap-up commit created"
        else
            print_error "Failed to create wrap-up commit"
            return 1
        fi
    fi
    
    # Push to remote
    print_step "3. Pushing branch to remote"
    if push_to_remote "$current_branch"; then
        print_success "Branch pushed to remote"
    else
        print_error "Failed to push branch to remote"
        return 1
    fi
    
    # Provide manual PR creation instructions
    echo ""
    print_banner "NEXT STEPS"
    local default_branch=$(get_default_branch)
    local pr_title="${change_type}: ${change_info} wrap-up"
    echo ""
    print_info "Changes have been archived and pushed to remote."
    print_info "Create a pull request manually using one of these methods:"
    echo ""
    echo "  Option 1 - GitHub CLI:"
    echo "    gh pr create --base $default_branch --head $current_branch \\"
    echo "                 --title \"$pr_title\" \\"
    echo "                 --body \"Wrap-up for $current_branch. Archive: $archive_relative\""
    echo ""
    echo "  Option 2 - GitHub Web UI:"
    echo "    Visit: https://github.com/[owner]/[repo]/compare/$current_branch"
    echo ""
    
    print_success "Change wrap-up completed!"
    
    return 0
}

# Export function
export -f wrap_up_change
