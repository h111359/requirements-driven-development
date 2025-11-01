#!/bin/bash

# delete-branch.sh
# Script to delete a branch locally and remotely after checking prerequisites
# Checks: 1) No uncommitted changes, 2) Branch is merged to main
# Usage: ./delete-branch.sh [branch-name]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

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
    echo "║                      DELETE BRANCH                         ║"
    echo "║       Delete branch locally and remotely (with checks)     ║"
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
        print_info "Please commit or stash your changes before deleting the branch:"
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

# Function to check if branch is merged to main
check_if_merged() {
    local branch_name="$1"
    local base_branch="${2:-main}"
    local current_branch=$(git branch --show-current)
    
    # Fetch latest from remote to ensure we have up-to-date info
    print_info "Fetching latest changes from remote..."
    git fetch origin >/dev/null 2>&1
    
    # Check if base branch exists, try master if main doesn't exist
    if ! git show-ref --verify --quiet "refs/heads/$base_branch"; then
        if git show-ref --verify --quiet "refs/heads/master"; then
            base_branch="master"
        else
            print_error "Cannot find base branch (tried 'main' and 'master')"
            return 2
        fi
    fi
    
    # Update local base branch to match remote
    print_info "Updating local '$base_branch' branch..."
    git checkout "$base_branch" >/dev/null 2>&1
    git pull origin "$base_branch" >/dev/null 2>&1
    git checkout "$current_branch" >/dev/null 2>&1
    print_success "Local '$base_branch' updated from remote"
    
    # Check if branch is merged using git branch --merged
    # Now that local main is up-to-date, this check will be accurate
    if git branch --merged "$base_branch" | grep -q "^\*\? *${branch_name}$"; then
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
    local force_delete="$3"
    
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
    echo ""
    
    # Delete local branch
    print_info "Deleting local branch '$branch_name'..."
    if [ "$force_delete" = true ]; then
        git branch -D "$branch_name"
        print_success "Local branch force-deleted"
    else
        if git branch -d "$branch_name" 2>/dev/null; then
            print_success "Local branch deleted"
        else
            print_error "Could not delete local branch (it might not be fully merged)"
            return 1
        fi
    fi
    echo ""
    
    # Check if remote branch exists
    if git ls-remote --heads origin "$branch_name" 2>/dev/null | grep -q "$branch_name"; then
        print_info "Deleting remote branch 'origin/$branch_name'..."
        if git push origin --delete "$branch_name" 2>/dev/null; then
            print_success "Remote branch deleted"
        else
            print_warning "Could not delete remote branch (check permissions)"
            return 1
        fi
    else
        print_info "Remote branch does not exist (or was already deleted)"
    fi
    
    return 0
}

# Main workflow
main() {
    local branch_name=""
    local force=false
    local skip_checks=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --force|-f)
                force=true
                shift
                ;;
            --skip-checks)
                skip_checks=true
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [branch-name] [--force] [--skip-checks]"
                echo ""
                echo "Delete a branch locally and remotely after checking prerequisites"
                echo ""
                echo "Arguments:"
                echo "  branch-name        Name of the branch to delete (defaults to current branch)"
                echo ""
                echo "Options:"
                echo "  --force, -f       Force delete even if not merged"
                echo "  --skip-checks     Skip uncommitted changes and merge status checks"
                echo "  --help, -h        Show this help message"
                echo ""
                exit 0
                ;;
            *)
                if [ -z "$branch_name" ]; then
                    branch_name="$1"
                else
                    print_error "Unknown option: $1"
                    echo "Use --help for usage information"
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    print_banner
    
    # Check prerequisites
    check_git_repo
    
    # Get current branch if not specified
    if [ -z "$branch_name" ]; then
        branch_name=$(git branch --show-current)
        print_info "Will delete current branch: $branch_name"
    else
        print_info "Will delete branch: $branch_name"
    fi
    echo ""
    
    # Check if trying to delete main/master
    if [[ "$branch_name" == "main" || "$branch_name" == "master" ]]; then
        print_error "Cannot delete main/master branch"
        exit 1
    fi
    
    # Check for uncommitted changes (unless skipped)
    if [ "$skip_checks" = false ]; then
        print_info "Checking for uncommitted changes..."
        if ! check_uncommitted_changes; then
            exit 1
        fi
        echo ""
    fi
    
    # Check if branch is merged (unless skipped or forced)
    local is_merged=false
    if [ "$skip_checks" = false ] && [ "$force" = false ]; then
        print_info "Checking if branch is merged to main..."
        local merge_status=0
        check_if_merged "$branch_name"
        merge_status=$?
        
        if [ $merge_status -eq 0 ]; then
            is_merged=true
        elif [ $merge_status -eq 2 ]; then
            print_error "Cannot determine merge status (base branch not found)"
            exit 1
        fi
        echo ""
    fi
    
    # Confirm deletion
    if [ "$is_merged" = true ] || [ "$skip_checks" = true ]; then
        if [ "$skip_checks" = false ]; then
            echo -e "${GREEN}${BOLD}Branch is merged and can be safely deleted${NC}"
        fi
        read -p "$(echo -e ${YELLOW}Delete branch '$branch_name' locally and remotely? [Y/n]: ${NC})" -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            print_info "Deletion cancelled by user"
            exit 0
        fi
    elif [ "$force" = true ]; then
        echo -e "${RED}${BOLD}Branch is NOT merged to main${NC}"
        echo -e "${YELLOW}${BOLD}Force delete is enabled${NC}"
        read -p "$(echo -e ${RED}Delete unmerged branch '$branch_name'? [y/N]: ${NC})" -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Deletion cancelled by user"
            exit 0
        fi
    else
        echo -e "${YELLOW}${BOLD}Branch is NOT merged to main${NC}"
        print_error "Cannot delete unmerged branch without --force flag"
        echo ""
        print_info "To delete anyway, use: $0 $branch_name --force"
        exit 1
    fi
    echo ""
    
    # Delete the branch
    if delete_branch "$branch_name" "main" "$force"; then
        echo ""
        print_success "Branch '$branch_name' deleted successfully"
    else
        echo ""
        print_error "Failed to delete branch '$branch_name'"
        exit 1
    fi
    echo ""
}

# Run main function
main "$@"
