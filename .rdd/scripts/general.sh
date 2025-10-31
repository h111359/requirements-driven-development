#!/bin/bash
# General utility script for RDD framework
# Provides common operations that can be called from prompts
# Part of RDD (Requirements-Driven Development) framework

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions for colored output
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_step() {
    echo -e "${CYAN}▶${NC} $1"
}

# Function to display usage
usage() {
    cat << EOF
Usage: $(basename "$0") <action> [options]

Actions:
  get-modified-files            Get list of modified files compared to main
  get-file-changes <file>       Get diff of a specific file compared to main
  analyze-requirements-impact   Analyze how changes affect requirements
  compare-with-main            Show comprehensive comparison with main branch
  help                          Show this help message

Examples:
  $(basename "$0") get-modified-files
  $(basename "$0") get-file-changes src/parser.py
  $(basename "$0") analyze-requirements-impact
  $(basename "$0") compare-with-main

EOF
}

# Function to get the default branch (usually main or master)
get_default_branch() {
    local default_branch="main"
    if git rev-parse --verify master >/dev/null 2>&1; then
        default_branch="master"
    fi
    echo "$default_branch"
}

# Function to ensure we have latest from remote
fetch_main() {
    local default_branch=$(get_default_branch)
    print_step "Fetching latest from origin/${default_branch}..."
    git fetch origin "$default_branch" --quiet
}

# Action: Get list of modified files compared to main
action_get_modified_files() {
    fetch_main
    
    local default_branch=$(get_default_branch)
    local current_branch=$(git branch --show-current)
    
    print_info "Comparing ${current_branch} with ${default_branch}..."
    echo ""
    
    # Get list of modified files
    local modified_files=$(git diff --name-only "origin/${default_branch}...HEAD")
    
    if [ -z "$modified_files" ]; then
        print_warning "No files modified compared to ${default_branch}"
        return 0
    fi
    
    echo "Modified files:"
    echo "$modified_files" | while read -r file; do
        local status=$(git diff --name-status "origin/${default_branch}...HEAD" | grep "^[AMDRC].*${file}$" | cut -f1)
        case "$status" in
            A) echo "  ${GREEN}+${NC} $file (added)" ;;
            M) echo "  ${YELLOW}~${NC} $file (modified)" ;;
            D) echo "  ${RED}-${NC} $file (deleted)" ;;
            R*) echo "  ${CYAN}→${NC} $file (renamed)" ;;
            C*) echo "  ${CYAN}©${NC} $file (copied)" ;;
            *) echo "  ${BLUE}?${NC} $file" ;;
        esac
    done
    
    echo ""
    print_success "Found $(echo "$modified_files" | wc -l) modified file(s)"
}

# Action: Get changes for a specific file
action_get_file_changes() {
    local file="$1"
    
    if [ -z "$file" ]; then
        print_error "File path required"
        echo "Usage: $(basename "$0") get-file-changes <file>"
        return 1
    fi
    
    if [ ! -f "$file" ]; then
        print_error "File not found: $file"
        return 1
    fi
    
    fetch_main
    
    local default_branch=$(get_default_branch)
    print_info "Showing changes in: $file"
    echo ""
    
    # Check if file exists in main branch
    if ! git cat-file -e "origin/${default_branch}:${file}" 2>/dev/null; then
        print_warning "File is new (doesn't exist in ${default_branch})"
        echo ""
        echo "Full content:"
        cat "$file"
        return 0
    fi
    
    # Show the diff
    git diff "origin/${default_branch}...HEAD" -- "$file"
    
    if [ $? -eq 0 ]; then
        echo ""
        print_success "Changes displayed for $file"
    fi
}

# Action: Analyze requirements impact
action_analyze_requirements_impact() {
    fetch_main
    
    local default_branch=$(get_default_branch)
    local requirements_file=".rdd-docs/requirements.md"
    
    print_info "Analyzing impact on requirements..."
    echo ""
    
    # Check if requirements.md has been modified
    local req_modified=$(git diff --name-only "origin/${default_branch}...HEAD" | grep "^${requirements_file}$" || true)
    
    if [ -n "$req_modified" ]; then
        print_warning "requirements.md has been directly modified in this branch"
        echo ""
        echo "Requirements changes:"
        git diff "origin/${default_branch}...HEAD" -- "$requirements_file" | grep "^[+-]\s*-\s*\*\*\[" || echo "  (No requirement line changes detected)"
        echo ""
    fi
    
    # Check if requirements-changes.md exists in workspace
    local req_changes_file=".rdd-docs/workspace/requirements-changes.md"
    if [ -f "$req_changes_file" ]; then
        print_info "Found requirements-changes.md in workspace"
        echo ""
        
        # Count changes by type
        local added=$(grep -c "^\- \*\*\[ADDED\]" "$req_changes_file" 2>/dev/null || echo "0")
        local modified=$(grep -c "^\- \*\*\[MODIFIED\]" "$req_changes_file" 2>/dev/null || echo "0")
        local deleted=$(grep -c "^\- \*\*\[DELETED\]" "$req_changes_file" 2>/dev/null || echo "0")
        
        echo "Requirements changes pending:"
        echo "  ${GREEN}+${NC} Added: $added"
        echo "  ${YELLOW}~${NC} Modified: $modified"
        echo "  ${RED}-${NC} Deleted: $deleted"
        echo ""
        
        if [ "$added" -gt 0 ] || [ "$modified" -gt 0 ] || [ "$deleted" -gt 0 ]; then
            print_success "Total: $((added + modified + deleted)) requirement changes"
        else
            print_warning "No requirement changes detected"
        fi
    else
        print_info "No requirements-changes.md found in workspace"
    fi
}

# Action: Comprehensive comparison with main
action_compare_with_main() {
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
    local commit_count=$(git rev-list --count "origin/${default_branch}..HEAD")
    echo "  This branch is $commit_count commit(s) ahead of ${default_branch}"
    echo ""
    
    if [ "$commit_count" -gt 0 ]; then
        git log --oneline --graph --max-count=10 "origin/${default_branch}..HEAD"
        echo ""
    fi
    
    # Show file changes
    print_step "File changes:"
    action_get_modified_files
    echo ""
    
    # Show requirements impact
    print_step "Requirements impact:"
    action_analyze_requirements_impact
    echo ""
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Main script logic
main() {
    local action="${1:-help}"
    
    case "$action" in
        get-modified-files)
            action_get_modified_files
            ;;
        get-file-changes)
            action_get_file_changes "$2"
            ;;
        analyze-requirements-impact)
            action_analyze_requirements_impact
            ;;
        compare-with-main)
            action_compare_with_main
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            print_error "Unknown action: $action"
            echo ""
            usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
