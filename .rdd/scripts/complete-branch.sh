#!/bin/bash

# complete-branch.sh
# Script to complete a fix/feature branch by archiving workspace and cleaning up
# This script replaces the F6-wrap-up prompt for routine branch completions
# Usage: ./complete-branch.sh [--force-archive]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
WORKSPACE_DIR="$REPO_ROOT/.rdd-docs/workspace"
ARCHIVE_BASE_DIR="$REPO_ROOT/.rdd-docs/archive"

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_banner() {
    echo -e "${CYAN}${BOLD}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                  COMPLETE BRANCH WORKFLOW                  ║"
    echo "║              Archive workspace and cleanup branch          ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Function to check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        print_error "Not a git repository. Please run this from within a git repository."
        exit 1
    fi
}

# Function to check for uncommitted changes
check_uncommitted_changes() {
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        print_error "You have uncommitted changes in your working directory"
        echo ""
        print_info "Please commit or stash your changes before completing the branch:"
        echo "  git add -A"
        echo "  git commit -m \"Your commit message\""
        echo "  OR"
        echo "  git stash"
        echo ""
        return 1
    fi
    
    print_success "No uncommitted changes detected"
    return 0
}

# Function to check if workspace directory exists and has content
check_workspace_exists() {
    if [ ! -d "$WORKSPACE_DIR" ]; then
        print_warning "Workspace directory not found: $WORKSPACE_DIR"
        return 1
    fi
    
    if [ -z "$(ls -A "$WORKSPACE_DIR" 2>/dev/null)" ]; then
        print_warning "Workspace directory is empty: $WORKSPACE_DIR"
        return 1
    fi
    
    print_success "Workspace directory found with content"
    return 0
}

# Function to archive workspace to branch-specific folder
archive_workspace() {
    local branch_name="$1"
    
    # Create archive directory named after the branch
    # Remove any slashes and replace with hyphens
    local safe_branch_name="${branch_name//\//-}"
    local archive_dir="$ARCHIVE_BASE_DIR/$safe_branch_name"
    
    # Check if archive already exists
    if [ -d "$archive_dir" ]; then
        print_warning "Archive directory already exists: $archive_dir"
        read -p "$(echo -e ${YELLOW}Overwrite existing archive? [y/N]: ${NC})" -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Archive cancelled by user"
            return 1
        fi
        rm -rf "$archive_dir"
    fi
    
    # Create archive directory
    mkdir -p "$archive_dir"
    
    # Copy all files from workspace to archive
    cp -R "$WORKSPACE_DIR"/. "$archive_dir"/
    
    # Create metadata file
    cat > "$archive_dir/.archive-metadata" << EOF
{
  "archivedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "branch": "$branch_name",
  "archivedBy": "$(git config user.name) <$(git config user.email)>",
  "lastCommit": "$(git rev-parse HEAD)",
  "lastCommitMessage": "$(git log -1 --pretty=%B | head -n 1)"
}
EOF
    
    print_success "Workspace archived to: $archive_dir"
    echo "$archive_dir"
}

# Function to check if branch is merged to main
check_if_merged() {
    local branch_name="$1"
    local base_branch="${2:-main}"
    
    # Check if base branch exists, try master if main doesn't exist
    if ! git show-ref --verify --quiet "refs/heads/$base_branch"; then
        if git show-ref --verify --quiet "refs/heads/master"; then
            base_branch="master"
        else
            print_error "Cannot find base branch (tried 'main' and 'master')"
            return 2
        fi
    fi
    
    # Check if branch is merged
    if git merge-base --is-ancestor "$branch_name" "$base_branch" 2>/dev/null; then
        print_success "Branch '$branch_name' is merged into '$base_branch'"
        return 0
    else
        print_warning "Branch '$branch_name' is NOT merged into '$base_branch'"
        return 1
    fi
}

# Function to delete branch locally and remotely
delete_branch() {
    local branch_name="$1"
    local base_branch="${2:-main}"
    
    # Check if base branch exists
    if ! git show-ref --verify --quiet "refs/heads/$base_branch"; then
        if git show-ref --verify --quiet "refs/heads/master"; then
            base_branch="master"
        else
            print_error "Cannot find base branch to switch to"
            return 1
        fi
    fi
    
    # Switch to base branch
    print_info "Switching to branch '$base_branch'..."
    git checkout "$base_branch"
    
    # Delete local branch
    print_info "Deleting local branch '$branch_name'..."
    if git branch -d "$branch_name" 2>/dev/null; then
        print_success "Local branch deleted"
    else
        print_warning "Could not delete local branch (it might not be fully merged)"
        read -p "$(echo -e ${YELLOW}Force delete local branch? [y/N]: ${NC})" -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git branch -D "$branch_name"
            print_success "Local branch force-deleted"
        else
            print_info "Local branch kept"
            return 1
        fi
    fi
    
    # Check if remote branch exists
    if git ls-remote --heads origin "$branch_name" | grep -q "$branch_name"; then
        print_info "Deleting remote branch 'origin/$branch_name'..."
        if git push origin --delete "$branch_name" 2>/dev/null; then
            print_success "Remote branch deleted"
        else
            print_warning "Could not delete remote branch (check permissions)"
        fi
    else
        print_info "Remote branch does not exist (or was already deleted)"
    fi
}

# Function to clean up workspace directory
cleanup_workspace() {
    if [ -d "$WORKSPACE_DIR" ]; then
        print_info "Removing workspace directory..."
        rm -rf "$WORKSPACE_DIR"
        print_success "Workspace directory removed"
    else
        print_info "Workspace directory already removed"
    fi
}

# Function to display summary
display_summary() {
    local branch_name="$1"
    local archive_path="$2"
    local branch_deleted="$3"
    
    echo ""
    echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}${BOLD}                        SUMMARY                             ${NC}"
    echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BOLD}Branch:${NC} $branch_name"
    echo -e "${BOLD}Archive:${NC} $archive_path"
    echo -e "${BOLD}Branch deleted:${NC} $branch_deleted"
    echo ""
    print_success "Branch completion workflow finished"
    echo ""
}

# Main workflow
main() {
    local force_archive=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --force-archive)
                force_archive=true
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [--force-archive]"
                echo ""
                echo "Complete a branch by archiving workspace and cleaning up"
                echo ""
                echo "Options:"
                echo "  --force-archive    Archive workspace even if branch is not merged"
                echo "  --help, -h        Show this help message"
                echo ""
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
    
    print_banner
    
    # Check prerequisites
    check_git_repo
    
    # Get current branch
    local current_branch=$(git branch --show-current)
    print_info "Current branch: $current_branch"
    echo ""
    
    # Check for uncommitted changes
    print_info "Checking for uncommitted changes..."
    if ! check_uncommitted_changes; then
        exit 1
    fi
    echo ""
    
    # Check if workspace exists
    print_info "Checking workspace directory..."
    local has_workspace=true
    if ! check_workspace_exists; then
        has_workspace=false
        if [ "$force_archive" = false ]; then
            print_warning "No workspace to archive"
            read -p "$(echo -e ${YELLOW}Continue without archiving? [y/N]: ${NC})" -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_info "Operation cancelled by user"
                exit 0
            fi
        fi
    fi
    echo ""
    
    # Archive workspace if it exists
    local archive_path="N/A"
    if [ "$has_workspace" = true ]; then
        print_info "Archiving workspace..."
        if archive_path=$(archive_workspace "$current_branch"); then
            echo ""
        else
            print_error "Failed to archive workspace"
            exit 1
        fi
    fi
    
    # Check if branch is merged
    print_info "Checking if branch is merged to main..."
    local is_merged=false
    local merge_status=0
    check_if_merged "$current_branch"
    merge_status=$?
    
    if [ $merge_status -eq 0 ]; then
        is_merged=true
    elif [ $merge_status -eq 2 ]; then
        print_error "Cannot determine merge status (base branch not found)"
        exit 1
    fi
    echo ""
    
    # Ask about branch deletion
    local branch_deleted="No"
    if [ "$is_merged" = true ]; then
        echo -e "${GREEN}${BOLD}Branch is merged and can be safely deleted${NC}"
        read -p "$(echo -e ${YELLOW}Delete branch locally and remotely? [Y/n]: ${NC})" -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            if delete_branch "$current_branch"; then
                branch_deleted="Yes"
                echo ""
            else
                print_warning "Branch deletion incomplete"
                branch_deleted="Partial"
                echo ""
            fi
        else
            print_info "Branch kept as requested"
            echo ""
        fi
    else
        echo -e "${YELLOW}${BOLD}Branch is NOT merged to main${NC}"
        print_warning "It is not recommended to delete an unmerged branch"
        read -p "$(echo -e ${RED}Delete branch anyway? [y/N]: ${NC})" -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if delete_branch "$current_branch"; then
                branch_deleted="Yes (forced)"
                echo ""
            else
                print_warning "Branch deletion incomplete"
                branch_deleted="Partial"
                echo ""
            fi
        else
            print_info "Branch kept as requested"
            echo ""
        fi
    fi
    
    # Clean up workspace if we're no longer on the original branch
    if [ "$(git branch --show-current)" != "$current_branch" ] && [ "$has_workspace" = true ]; then
        cleanup_workspace
        echo ""
    fi
    
    # Display summary
    display_summary "$current_branch" "$archive_path" "$branch_deleted"
}

# Run main function
main "$@"
