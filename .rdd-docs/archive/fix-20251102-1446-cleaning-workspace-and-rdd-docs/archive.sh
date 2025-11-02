#!/bin/bash

# archive.sh
# Script to archive workspace files to branch-specific archive folder
# Usage: ./archive.sh [branch-name]

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
    echo "║                    ARCHIVE WORKSPACE                       ║"
    echo "║           Move workspace files to archive folder           ║"
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
    local has_changes=false
    
    # Check for modified or staged files
    if ! git diff-index --quiet HEAD --; then
        has_changes=true
    fi
    
    # Check for untracked files
    if [ -n "$(git ls-files --others --exclude-standard)" ]; then
        has_changes=true
    fi
    
    if [ "$has_changes" = true ]; then
        print_error "There are uncommitted changes in the repository."
        print_error "Please commit or stash your changes before archiving."
        echo ""
        print_info "Uncommitted changes:"
        git status --short
        return 1
    fi
    
    print_success "No uncommitted changes found"
    return 0
}

# Function to check if workspace directory exists and has content
check_workspace_exists() {
    if [ ! -d "$WORKSPACE_DIR" ]; then
        print_error "Workspace directory not found: $WORKSPACE_DIR"
        return 1
    fi
    
    if [ -z "$(ls -A "$WORKSPACE_DIR" 2>/dev/null)" ]; then
        print_error "Workspace directory is empty: $WORKSPACE_DIR"
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
    return 0
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

# Main workflow
main() {
    local branch_name=""
    local keep_workspace=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --keep-workspace)
                keep_workspace=true
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [branch-name] [--keep-workspace]"
                echo ""
                echo "Archive workspace files to a branch-specific archive folder"
                echo ""
                echo "Arguments:"
                echo "  branch-name        Name of the branch (defaults to current branch)"
                echo ""
                echo "Options:"
                echo "  --keep-workspace   Keep workspace directory after archiving"
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
    
    # Check for uncommitted changes first
    print_info "Checking for uncommitted changes..."
    if ! check_uncommitted_changes; then
        exit 1
    fi
    echo ""
    
    # Get current branch if not specified
    if [ -z "$branch_name" ]; then
        branch_name=$(git branch --show-current)
        print_info "Using current branch: $branch_name"
    else
        print_info "Archiving for branch: $branch_name"
    fi
    echo ""
    
    # Check if workspace exists
    print_info "Checking workspace directory..."
    if ! check_workspace_exists; then
        exit 1
    fi
    echo ""
    
    # Archive workspace
    print_info "Archiving workspace..."
    if ! archive_workspace "$branch_name"; then
        print_error "Failed to archive workspace"
        exit 1
    fi
    echo ""
    
    # Clean up workspace unless --keep-workspace is set
    if [ "$keep_workspace" = false ]; then
        cleanup_workspace
    else
        print_info "Workspace directory kept as requested"
    fi
    echo ""
    
    # Auto-commit the archive changes
    print_info "Committing archive changes..."
    # Stage the archive and the deletion of workspace (if removed)
    git add "$REPO_ROOT/.rdd-docs"
    git commit -m "archiving workspace folder for $branch_name"
    print_success "Changes committed successfully"
    echo ""
    
    print_success "Archive completed successfully"
    echo ""
}

# Run main function
main "$@"
