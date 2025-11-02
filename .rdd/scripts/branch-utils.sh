#!/bin/bash

# branch-utils.sh
# Branch management utility functions for RDD framework
# Provides branch creation, deletion, merge checking, and listing operations

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source core-utils.sh for common functions
if [ -f "$SCRIPT_DIR/core-utils.sh" ]; then
    source "$SCRIPT_DIR/core-utils.sh"
else
    echo "ERROR: core-utils.sh not found. Please ensure it exists in the same directory."
    exit 1
fi

# Source git-utils.sh for git operations
if [ -f "$SCRIPT_DIR/git-utils.sh" ]; then
    source "$SCRIPT_DIR/git-utils.sh"
else
    echo "ERROR: git-utils.sh not found. Please ensure it exists in the same directory."
    exit 1
fi

# Prevent multiple sourcing
if [ -n "$BRANCH_UTILS_LOADED" ]; then
    return 0
fi
BRANCH_UTILS_LOADED=1

# ============================================================================
# BRANCH CREATION
# ============================================================================

# Create a new branch with format validation
# Usage: create_branch "enh|fix" "branch-name"
# Returns: 0 on success, 1 on failure
create_branch() {
    local branch_type="$1"
    local branch_name="$2"
    
    if [ -z "$branch_type" ] || [ -z "$branch_name" ]; then
        print_error "Branch type and name are required"
        echo "Usage: create_branch <enh|fix> <branch_name>"
        return 1
    fi
    
    # Validate branch type
    if [[ ! "$branch_type" =~ ^(enh|fix)$ ]]; then
        print_error "Invalid branch type: $branch_type"
        print_info "Valid types: enh, fix"
        return 1
    fi
    
    # Validate branch name format (kebab-case, max 5 words)
    if ! validate_name "$branch_name"; then
        return 1
    fi
    
    # Generate branch ID with timestamp
    local date_time=$(date +"%Y%m%d-%H%M")
    local branch_id="${date_time}-${branch_name}"
    local full_branch_name="${branch_type}/${branch_id}"
    
    # Check if branch already exists
    if git show-ref --verify --quiet "refs/heads/$full_branch_name"; then
        print_error "Branch '$full_branch_name' already exists"
        return 1
    fi
    
    # Get default branch
    local default_branch=$(get_default_branch)
    
    print_step "Creating new branch: $full_branch_name"
    
    # Switch to default branch and pull latest
    print_info "Switching to '$default_branch' and pulling latest changes..."
    git checkout "$default_branch" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        print_error "Failed to checkout '$default_branch'"
        return 1
    fi
    
    git pull origin "$default_branch" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        print_warning "Failed to pull from origin (continuing anyway)"
    fi
    
    # Create and checkout new branch
    print_info "Creating branch '$full_branch_name'..."
    if git checkout -b "$full_branch_name" 2>&1; then
        print_success "Created and checked out branch: $full_branch_name"
        echo ""
        print_info "Branch details:"
        echo "  Type: $branch_type"
        echo "  Name: $branch_name"
        echo "  ID: $branch_id"
        echo "  Full: $full_branch_name"
        return 0
    else
        print_error "Failed to create branch"
        return 1
    fi
}

# ============================================================================
# BRANCH DELETION
# ============================================================================

# Delete a branch locally and remotely with safety checks
# Usage: delete_branch "branch_name" [force] [skip_checks]
# force: "true" to force delete (bypass merge check), "false" otherwise (default: false)
# skip_checks: "true" to skip uncommitted changes check, "false" otherwise (default: false)
# Returns: 0 on success, 1 on failure
delete_branch() {
    local branch_name="$1"
    local force="${2:-false}"
    local skip_checks="${3:-false}"
    
    if [ -z "$branch_name" ]; then
        print_error "Branch name is required"
        echo "Usage: delete_branch <branch_name> [force] [skip_checks]"
        return 1
    fi
    
    # Check if we're in a git repository
    check_git_repo
    
    # Check for uncommitted changes unless skipped
    if [ "$skip_checks" = "false" ]; then
        print_info "Checking for uncommitted changes..."
        if ! check_uncommitted_changes; then
            print_error "Please commit or stash changes before deleting branch"
            return 1
        fi
        echo ""
    fi
    
    # Check if branch exists locally
    if ! git show-ref --verify --quiet "refs/heads/$branch_name"; then
        print_error "Local branch '$branch_name' does not exist"
        return 1
    fi
    
    # Check if branch is merged (unless force delete)
    if [ "$force" = "false" ]; then
        print_info "Checking if branch is merged..."
        local merge_status=$(check_merge_status "$branch_name")
        local merge_result=$?
        
        if [ $merge_result -eq 1 ]; then
            print_warning "Branch is not merged into default branch"
            if ! confirm_action "Delete anyway? (This will use force delete)"; then
                print_info "Deletion cancelled"
                return 1
            fi
            force="true"
        elif [ $merge_result -gt 1 ]; then
            print_error "Failed to check merge status"
            return 1
        fi
        echo ""
    fi
    
    # Get default branch to switch to
    local default_branch=$(get_default_branch)
    
    # Switch to default branch
    print_info "Switching to branch '$default_branch'..."
    git checkout "$default_branch" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        print_error "Failed to checkout '$default_branch'"
        return 1
    fi
    echo ""
    
    # Delete local branch
    print_info "Deleting local branch '$branch_name'..."
    if [ "$force" = "true" ]; then
        if git branch -D "$branch_name" 2>&1; then
            print_success "Local branch force-deleted"
        else
            print_error "Failed to delete local branch"
            return 1
        fi
    else
        if git branch -d "$branch_name" 2>&1; then
            print_success "Local branch deleted"
        else
            print_error "Failed to delete local branch (not fully merged)"
            return 1
        fi
    fi
    echo ""
    
    # Check if remote branch exists and delete
    if git ls-remote --heads origin "$branch_name" 2>/dev/null | grep -q "$branch_name"; then
        print_info "Deleting remote branch 'origin/$branch_name'..."
        if git push origin --delete "$branch_name" 2>&1; then
            print_success "Remote branch deleted"
        else
            print_warning "Failed to delete remote branch (check permissions)"
            return 1
        fi
    else
        print_info "Remote branch does not exist (or was already deleted)"
    fi
    
    echo ""
    print_success "Branch '$branch_name' deleted successfully"
    return 0
}

# ============================================================================
# BATCH BRANCH DELETION
# ============================================================================

# Delete all merged branches with confirmation
# Usage: delete_merged_branches
# Returns: 0 on success, 1 on failure
delete_merged_branches() {
    check_git_repo
    
    local default_branch=$(get_default_branch)
    
    print_banner "DELETE MERGED BRANCHES"
    echo ""
    
    # Fetch latest changes
    print_info "Fetching latest changes from remote..."
    git fetch --all >/dev/null 2>&1
    echo ""
    
    # Update local default branch
    print_info "Updating local '$default_branch' to match remote..."
    git checkout "$default_branch" >/dev/null 2>&1
    git pull origin "$default_branch" >/dev/null 2>&1
    print_success "Local '$default_branch' updated"
    echo ""
    
    # Get list of remote branches merged into default branch
    print_info "Finding branches merged into '$default_branch'..."
    local merged_remote_branches=$(git branch -r --merged "origin/$default_branch" | \
        grep -v "origin/$default_branch" | \
        grep -v 'origin/HEAD' | \
        sed 's/^[[:space:]]*//')
    
    local merged_local_branches=$(git branch --merged "$default_branch" | \
        grep -vE "^\*|^[[:space:]]*${default_branch}$|^[[:space:]]*HEAD$" | \
        sed 's/^[[:space:]]*//')
    
    # Check if there are any branches to delete
    if [ -z "$merged_remote_branches" ] && [ -z "$merged_local_branches" ]; then
        print_info "No merged branches found"
        return 0
    fi
    
    # Display branches to be deleted
    if [ -n "$merged_remote_branches" ]; then
        echo ""
        print_info "Remote branches to delete:"
        echo "$merged_remote_branches" | while read -r branch; do
            echo "  - $branch"
        done
    fi
    
    if [ -n "$merged_local_branches" ]; then
        echo ""
        print_info "Local branches to delete:"
        echo "$merged_local_branches" | while read -r branch; do
            echo "  - $branch"
        done
    fi
    
    echo ""
    
    # Count branches
    local remote_count=$(echo "$merged_remote_branches" | grep -c . 2>/dev/null || echo "0")
    local local_count=$(echo "$merged_local_branches" | grep -c . 2>/dev/null || echo "0")
    local total_count=$((remote_count + local_count))
    
    print_warning "Total branches to delete: $total_count ($remote_count remote, $local_count local)"
    echo ""
    
    # Ask for confirmation
    if ! confirm_action "Delete all these branches?"; then
        print_info "Deletion cancelled"
        return 0
    fi
    
    echo ""
    
    # Delete remote branches
    if [ -n "$merged_remote_branches" ]; then
        print_step "Deleting remote branches..."
        echo "$merged_remote_branches" | sed 's/origin\///' | while read -r branch; do
            print_info "Deleting origin/$branch..."
            if git push origin --delete "$branch" 2>&1; then
                print_success "Deleted origin/$branch"
            else
                print_error "Failed to delete origin/$branch"
            fi
        done
        echo ""
    fi
    
    # Delete local branches
    if [ -n "$merged_local_branches" ]; then
        print_step "Deleting local branches..."
        echo "$merged_local_branches" | while read -r branch; do
            print_info "Deleting $branch..."
            if git branch -d "$branch" 2>&1; then
                print_success "Deleted $branch"
            else
                print_error "Failed to delete $branch"
            fi
        done
        echo ""
    fi
    
    print_success "Branch cleanup completed"
    return 0
}

# ============================================================================
# MERGE STATUS CHECKING
# ============================================================================

# Check if a branch is merged into the base branch
# Usage: check_merge_status "branch_name" ["base_branch"]
# Returns: 0 if merged, 1 if not merged, 2+ for errors
# Note: This function is also available in git-utils.sh, but included here for convenience
check_merge_status() {
    local branch_name="$1"
    local base_branch="${2:-$(get_default_branch)}"
    
    if [ -z "$branch_name" ]; then
        print_error "Branch name is required"
        echo "Usage: check_merge_status <branch_name> [base_branch]"
        return 2
    fi
    
    # Check if branch exists
    if ! git show-ref --verify --quiet "refs/heads/$branch_name"; then
        print_error "Branch '$branch_name' does not exist"
        return 3
    fi
    
    local current_branch=$(get_current_branch)
    
    # Fetch latest from remote
    debug_print "Fetching latest changes from remote..."
    git fetch origin >/dev/null 2>&1
    
    # Check if base branch exists
    if ! git show-ref --verify --quiet "refs/heads/$base_branch"; then
        print_error "Base branch '$base_branch' not found"
        return 4
    fi
    
    # Update local base branch to match remote
    debug_print "Updating local '$base_branch' branch..."
    git checkout "$base_branch" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        print_error "Failed to checkout '$base_branch'"
        return 5
    fi
    
    git pull origin "$base_branch" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        print_error "Failed to pull latest changes for '$base_branch'"
        return 6
    fi
    
    # Return to original branch
    git checkout "$current_branch" >/dev/null 2>&1
    debug_print "Local '$base_branch' updated from remote"
    
    # Check if branch is merged using git branch --merged
    if git branch --merged "$base_branch" | grep -q "^\*\? *${branch_name}$"; then
        print_success "Branch '$branch_name' is merged into '$base_branch'"
        return 0
    else
        print_warning "Branch '$branch_name' is NOT merged into '$base_branch'"
        return 1
    fi
}

# ============================================================================
# BRANCH LISTING
# ============================================================================

# List branches with optional filtering
# Usage: list_branches [filter]
# filter: "local", "remote", "merged", "unmerged", "all" (default: "local")
# Returns: 0 on success
list_branches() {
    local filter="${1:-local}"
    
    check_git_repo
    
    local default_branch=$(get_default_branch)
    
    case "$filter" in
        local)
            print_info "Local branches:"
            git branch --list | while read -r line; do
                echo "  $line"
            done
            ;;
        remote)
            print_info "Remote branches:"
            git branch -r | while read -r line; do
                echo "  $line"
            done
            ;;
        merged)
            print_info "Branches merged into '$default_branch':"
            git branch --merged "$default_branch" | while read -r line; do
                echo "  $line"
            done
            ;;
        unmerged)
            print_info "Branches NOT merged into '$default_branch':"
            git branch --no-merged "$default_branch" | while read -r line; do
                echo "  $line"
            done
            ;;
        all)
            print_info "All branches (local and remote):"
            git branch -a | while read -r line; do
                echo "  $line"
            done
            ;;
        *)
            print_error "Invalid filter: $filter"
            print_info "Valid filters: local, remote, merged, unmerged, all"
            return 1
            ;;
    esac
    
    return 0
}

# ============================================================================
# BRANCH INSPECTION
# ============================================================================

# Get information about a specific branch
# Usage: get_branch_info "branch_name"
# Returns: 0 on success, 1 on failure
get_branch_info() {
    local branch_name="$1"
    
    if [ -z "$branch_name" ]; then
        print_error "Branch name is required"
        echo "Usage: get_branch_info <branch_name>"
        return 1
    fi
    
    # Check if branch exists
    if ! git show-ref --verify --quiet "refs/heads/$branch_name"; then
        print_error "Branch '$branch_name' does not exist"
        return 1
    fi
    
    local default_branch=$(get_default_branch)
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  BRANCH INFO: $branch_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Last commit on branch
    print_info "Last commit:"
    git log -1 --pretty=format:"  %h - %s (%cr) <%an>" "$branch_name"
    echo ""
    echo ""
    
    # Commit count ahead/behind default branch
    local ahead=$(git rev-list --count "origin/${default_branch}..${branch_name}" 2>/dev/null || echo "0")
    local behind=$(git rev-list --count "${branch_name}..origin/${default_branch}" 2>/dev/null || echo "0")
    print_info "Compared to '$default_branch':"
    echo "  Ahead: $ahead commit(s)"
    echo "  Behind: $behind commit(s)"
    echo ""
    
    # Merge status
    print_info "Merge status:"
    if git branch --merged "$default_branch" | grep -q "^\*\? *${branch_name}$"; then
        echo "  ✓ Merged into '$default_branch'"
    else
        echo "  ✗ Not merged into '$default_branch'"
    fi
    echo ""
    
    # Remote tracking
    local remote_branch=$(git rev-parse --abbrev-ref "${branch_name}@{upstream}" 2>/dev/null)
    print_info "Remote tracking:"
    if [ -n "$remote_branch" ]; then
        echo "  Tracking: $remote_branch"
    else
        echo "  No remote tracking configured"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return 0
}

# Check if branch exists (local or remote)
# Usage: branch_exists "branch_name" ["local|remote|any"]
# Returns: 0 if exists, 1 if not
branch_exists() {
    local branch_name="$1"
    local location="${2:-any}"
    
    if [ -z "$branch_name" ]; then
        return 1
    fi
    
    case "$location" in
        local)
            git show-ref --verify --quiet "refs/heads/$branch_name"
            return $?
            ;;
        remote)
            git ls-remote --heads origin "$branch_name" 2>/dev/null | grep -q "$branch_name"
            return $?
            ;;
        any)
            if git show-ref --verify --quiet "refs/heads/$branch_name"; then
                return 0
            fi
            git ls-remote --heads origin "$branch_name" 2>/dev/null | grep -q "$branch_name"
            return $?
            ;;
        *)
            print_error "Invalid location: $location"
            return 1
            ;;
    esac
}

# ============================================================================
# EXPORT ALL FUNCTIONS
# ============================================================================

# Export all functions so they can be used by scripts that source this file
export -f create_branch
export -f delete_branch
export -f delete_merged_branches
export -f check_merge_status
export -f list_branches
export -f get_branch_info
export -f branch_exists

debug_print "branch-utils.sh loaded successfully"
