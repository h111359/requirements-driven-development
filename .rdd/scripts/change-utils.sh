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
    
    # Create config file with new naming convention
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    local config_filename=".rdd.${change_type}.${branch_name//\//-}"
    cat > "$WORKSPACE_DIR/$config_filename" << EOF
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
    
    print_success "Created $config_filename config file"
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
    
    # Check for uncommitted changes
    print_step "1. Checking for uncommitted changes"
    if ! check_uncommitted_changes; then
        return 1
    fi
    print_success "No uncommitted changes found"
    echo ""
    
    # Extract change type and name from branch
    local change_type="${current_branch%%/*}"
    local change_info="${current_branch#*/}"
    
    # Display wrap-up plan
    print_info "This will perform the following actions:"
    echo ""
    echo "  1. Move workspace content to .rdd-docs/archive/${current_branch//\//-}"
    echo "  2. Create commit with message: 'archive: moved workspace to archive'"
    echo "  3. Push changes to remote branch"
    echo ""
    
    # Ask for user confirmation
    if ! confirm_action "Proceed with wrap-up?"; then
        print_info "Wrap-up cancelled by user"
        return 0
    fi
    echo ""
    
    # Archive workspace
    print_step "2. Archiving workspace contents"
    local archive_relative
    if ! archive_relative=$(archive_workspace "$current_branch" false); then
        print_error "Failed to archive workspace"
        return 1
    fi
    print_success "Workspace archived to $archive_relative"
    echo ""
    
    # Create wrap-up commit
    print_step "3. Creating wrap-up commit"
    local commit_message="archive: moved workspace to archive"
    
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
    echo ""
    
    # Push to remote
    print_step "4. Pushing branch to remote"
    if push_to_remote "$current_branch"; then
        print_success "Branch pushed to remote"
    else
        print_error "Failed to push branch to remote"
        return 1
    fi
    
    # Display completion summary
    echo ""
    print_banner "WRAP-UP COMPLETE"
    echo ""
    print_success "Workspace archived to: $archive_relative"
    print_success "Commit created with message: '$commit_message'"
    print_success "Changes pushed to remote branch: $current_branch"
    echo ""
    print_info "Next Steps:"
    echo "  1. Create a Pull Request on GitHub to merge your changes"
    echo "  2. Review and complete the PR process"
    echo "  3. After merge, you can delete the local and remote branches"
    echo ""
    
    return 0
}

# Export function
export -f wrap_up_change
