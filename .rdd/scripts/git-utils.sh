#!/bin/bash

# git-utils.sh
# Git operations utility functions for RDD framework
# Provides git-related operations used across all RDD scripts

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source core-utils.sh for common functions
if [ -f "$SCRIPT_DIR/core-utils.sh" ]; then
    source "$SCRIPT_DIR/core-utils.sh"
else
    echo "ERROR: core-utils.sh not found. Please ensure it exists in the same directory."
    exit 1
fi

# Prevent multiple sourcing
if [ -n "$GIT_UTILS_LOADED" ]; then
    return 0
fi
GIT_UTILS_LOADED=1

# ============================================================================
# GIT REPOSITORY CHECKS
# ============================================================================

# Check if we're in a git repository
# Usage: check_git_repo
# Returns: 0 if in git repo, exits with error if not
check_git_repo() {
    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        print_error "Not a git repository. Please run this from within a git repository."
        exit 1
    fi
    debug_print "Git repository verified"
    return 0
}

# ============================================================================
# UNCOMMITTED CHANGES DETECTION
# ============================================================================

# Check for uncommitted changes (modified, staged, or untracked files)
# Usage: check_uncommitted_changes
# Returns: 0 if no changes, 1 if changes exist
check_uncommitted_changes() {
    local has_changes=false
    
    # Check for modified or staged files
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        has_changes=true
    fi
    
    # Check for untracked files
    if [ -n "$(git ls-files --others --exclude-standard)" ]; then
        has_changes=true
    fi
    
    if [ "$has_changes" = true ]; then
        print_error "There are uncommitted changes in the repository."
        print_error "Please commit or stash your changes before proceeding."
        echo ""
        print_info "Uncommitted changes:"
        git status --short
        return 1
    fi
    
    debug_print "No uncommitted changes found"
    return 0
}

# ============================================================================
# BRANCH OPERATIONS
# ============================================================================

# Get the default branch name (main or master)
# Usage: get_default_branch
# Returns: "main" or "master" depending on what exists
get_default_branch() {
    local default_branch="main"
    
    # Check if main branch exists
    if ! git show-ref --verify --quiet "refs/heads/main" 2>/dev/null; then
        # Check if master branch exists
        if git show-ref --verify --quiet "refs/heads/master" 2>/dev/null; then
            default_branch="master"
        fi
    fi
    
    echo "$default_branch"
}

# Fetch latest changes from remote default branch
# Usage: fetch_main
# Returns: 0 on success, 1 on failure
fetch_main() {
    local default_branch=$(get_default_branch)
    
    print_step "Fetching latest from origin/${default_branch}..."
    
    if git fetch origin "$default_branch" --quiet 2>/dev/null; then
        debug_print "Successfully fetched origin/${default_branch}"
        return 0
    else
        print_warning "Failed to fetch from origin/${default_branch}"
        return 1
    fi
}

# ============================================================================
# FILE COMPARISON AND DIFFS
# ============================================================================

# Compare current branch with main branch
# Usage: compare_with_main
# Returns: 0 on success
compare_with_main() {
    fetch_main
    
    local default_branch=$(get_default_branch)
    local current_branch=$(git branch --show-current)
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  COMPARISON: ${current_branch} vs ${default_branch}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Show commit differences
    print_step "Commit differences:"
    local commit_count=$(git rev-list --count "origin/${default_branch}..HEAD" 2>/dev/null || echo "0")
    echo "  This branch is $commit_count commit(s) ahead of ${default_branch}"
    echo ""
    
    if [ "$commit_count" -gt 0 ]; then
        git log --oneline --graph --max-count=10 "origin/${default_branch}..HEAD"
        echo ""
    fi
    
    # Show file changes
    print_step "File changes:"
    get_modified_files
    echo ""
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return 0
}

# Get list of modified files compared to main branch
# Usage: get_modified_files
# Returns: 0 on success, prints modified files list
get_modified_files() {
    local default_branch=$(get_default_branch)
    local current_branch=$(git branch --show-current)
    
    print_info "Comparing ${current_branch} with ${default_branch}..."
    echo ""
    
    # Get list of modified files
    local modified_files=$(git diff --name-only "origin/${default_branch}...HEAD" 2>/dev/null)
    
    if [ -z "$modified_files" ]; then
        print_warning "No files modified compared to ${default_branch}"
        return 0
    fi
    
    echo "Modified files:"
    echo "$modified_files" | while read -r file; do
        local status=$(git diff --name-status "origin/${default_branch}...HEAD" 2>/dev/null | grep "^[AMDRC].*${file}$" | cut -f1)
        case "$status" in
            A) echo -e "  ${GREEN}+${NC} $file (added)" ;;
            M) echo -e "  ${YELLOW}~${NC} $file (modified)" ;;
            D) echo -e "  ${RED}-${NC} $file (deleted)" ;;
            R*) echo -e "  ${CYAN}→${NC} $file (renamed)" ;;
            C*) echo -e "  ${CYAN}©${NC} $file (copied)" ;;
            *) echo -e "  ${BLUE}?${NC} $file" ;;
        esac
    done
    
    echo ""
    local file_count=$(echo "$modified_files" | wc -l)
    print_success "Found $file_count modified file(s)"
    
    return 0
}

# Get diff for a specific file compared to main branch
# Usage: get_file_diff "/path/to/file"
# Returns: 0 on success, 1 if file not found
get_file_diff() {
    local file_path="$1"
    
    if [ -z "$file_path" ]; then
        print_error "File path is required"
        echo "Usage: get_file_diff <file_path>"
        return 1
    fi
    
    if [ ! -f "$file_path" ]; then
        print_error "File not found: $file_path"
        return 1
    fi
    
    local default_branch=$(get_default_branch)
    print_info "Showing changes in: $file_path"
    echo ""
    
    # Check if file exists in main branch
    if ! git cat-file -e "origin/${default_branch}:${file_path}" 2>/dev/null; then
        print_warning "File is new (doesn't exist in ${default_branch})"
        echo ""
        echo "Full content:"
        cat "$file_path"
        return 0
    fi
    
    # Show the diff
    git diff "origin/${default_branch}...HEAD" -- "$file_path"
    
    if [ $? -eq 0 ]; then
        echo ""
        print_success "Changes displayed for $file_path"
    fi
    
    return 0
}

# ============================================================================
# PUSH AND COMMIT OPERATIONS
# ============================================================================

# Push current branch to remote with upstream tracking
# Usage: push_to_remote [branch_name]
# If branch_name not provided, uses current branch
# Returns: 0 on success, 1 on failure
push_to_remote() {
    local branch_name="${1:-$(git branch --show-current)}"
    
    if [ -z "$branch_name" ]; then
        print_error "No branch name provided and could not determine current branch"
        return 1
    fi
    
    print_info "Pushing branch '$branch_name' to remote..."
    
    if git push -u origin "$branch_name" 2>&1; then
        print_success "Branch pushed to remote with upstream tracking"
        return 0
    else
        print_error "Failed to push branch to remote"
        return 1
    fi
}

# Auto-commit all changes with a message
# Usage: auto_commit "commit message"
# Returns: 0 on success, 1 on failure, 2 if no changes to commit
auto_commit() {
    local message="$1"
    
    if [ -z "$message" ]; then
        print_error "Commit message is required"
        echo "Usage: auto_commit <message>"
        return 1
    fi
    
    print_info "Staging changes..."
    git add -A
    
    # Check if there are changes to commit
    if git diff --cached --quiet; then
        print_warning "No changes to commit"
        return 2
    fi
    
    print_info "Committing changes..."
    if git commit -m "$message" 2>&1; then
        print_success "Changes committed: $message"
        return 0
    else
        print_error "Failed to commit changes"
        return 1
    fi
}

# ============================================================================
# MERGE STATUS CHECKS
# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

# Get current branch name
# Usage: get_current_branch
# Returns: current branch name
get_current_branch() {
    git branch --show-current
}

# Get git user information
# Usage: get_git_user
# Returns: "Name <email>"
get_git_user() {
    local name=$(git config user.name)
    local email=$(git config user.email)
    echo "$name <$email>"
}

# Get last commit SHA
# Usage: get_last_commit_sha
# Returns: commit SHA
get_last_commit_sha() {
    git rev-parse HEAD
}

# Get last commit message (first line only)
# Usage: get_last_commit_message
# Returns: commit message
get_last_commit_message() {
    git log -1 --pretty=%B | head -n 1
}

# ============================================================================
# EXPORT ALL FUNCTIONS
# ============================================================================

# Export all functions so they can be used by scripts that source this file
export -f check_git_repo
export -f check_uncommitted_changes
export -f get_default_branch
export -f fetch_main
export -f compare_with_main
export -f get_modified_files
export -f get_file_diff
export -f push_to_remote
export -f auto_commit
export -f get_current_branch
export -f get_git_user
export -f get_last_commit_sha
export -f get_last_commit_message

debug_print "git-utils.sh loaded successfully"
