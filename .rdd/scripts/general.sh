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
  merge-requirements-changes   Merge requirements from workspace to requirements.md
  preview-requirements-merge   Preview what would be merged (no changes)
  help                          Show this help message

Examples:
  $(basename "$0") get-modified-files
  $(basename "$0") get-file-changes src/parser.py
  $(basename "$0") analyze-requirements-impact
  $(basename "$0") compare-with-main
  $(basename "$0") merge-requirements-changes [--dry-run] [--backup]
  $(basename "$0") preview-requirements-merge

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

# Function to get next available ID for a section
get_next_id() {
    local prefix="$1"  # e.g., GF, FR, NFR, TR
    local file="$2"
    
    # Find all IDs with this prefix and extract the number
    local max_id=$(grep -oP "\[$prefix-\K[0-9]+" "$file" 2>/dev/null | sort -n | tail -1)
    
    if [ -z "$max_id" ]; then
        echo "01"
    else
        printf "%02d" $((max_id + 1))
    fi
}

# Function to validate merge readiness
validate_merge_readiness() {
    local has_errors=0
    
    # Check if requirements-changes.md exists
    if [ ! -f ".rdd-docs/workspace/requirements-changes.md" ]; then
        print_error "requirements-changes.md not found in workspace"
        has_errors=1
    fi
    
    # Check if requirements.md exists
    if [ ! -f ".rdd-docs/requirements.md" ]; then
        print_warning "requirements.md not found - will be created"
    fi
    
    if [ $has_errors -eq 0 ]; then
        print_success "Validation passed - ready to merge"
        return 0
    else
        print_error "Validation failed - cannot proceed with merge"
        return 1
    fi
}

# Action: Preview requirements merge
action_preview_requirements_merge() {
    print_info "Previewing requirements merge..."
    
    if [ ! -f ".rdd-docs/workspace/requirements-changes.md" ]; then
        print_error "requirements-changes.md not found in workspace"
        return 1
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "   MERGE PREVIEW"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Count changes by type
    local added_count=$(grep -c "^\- \*\*\[ADDED\]" ".rdd-docs/workspace/requirements-changes.md" || true)
    local modified_count=$(grep -c "^\- \*\*\[MODIFIED\]" ".rdd-docs/workspace/requirements-changes.md" || true)
    local deleted_count=$(grep -c "^\- \*\*\[DELETED\]" ".rdd-docs/workspace/requirements-changes.md" || true)
    
    echo "Changes to be applied:"
    echo "  [ADDED]    : $added_count requirements"
    echo "  [MODIFIED] : $modified_count requirements"
    echo "  [DELETED]  : $deleted_count requirements"
    echo ""
    
    # Show actual changes
    echo "━━━ ADDED Requirements ━━━"
    grep "^\- \*\*\[ADDED\]" ".rdd-docs/workspace/requirements-changes.md" || echo "  (none)"
    echo ""
    
    echo "━━━ MODIFIED Requirements ━━━"
    grep "^\- \*\*\[MODIFIED\]" ".rdd-docs/workspace/requirements-changes.md" || echo "  (none)"
    echo ""
    
    echo "━━━ DELETED Requirements ━━━"
    grep "^\- \*\*\[DELETED\]" ".rdd-docs/workspace/requirements-changes.md" || echo "  (none)"
    echo ""
    
    print_info "This is a preview only. Run 'merge-requirements-changes' to apply changes."
}

# Action: Merge requirements changes
action_merge_requirements_changes() {
    local dry_run=false
    local create_backup=false
    
    # Parse options
    for arg in "$@"; do
        case $arg in
            --dry-run)
                dry_run=true
                ;;
            --backup)
                create_backup=true
                ;;
        esac
    done
    
    print_info "Merging requirements-changes.md into requirements.md..."
    
    # Validate first
    if ! validate_merge_readiness; then
        return 1
    fi
    
    # Create backup if requested
    if [ "$create_backup" = true ]; then
        if [ -f ".rdd-docs/requirements.md" ]; then
            local backup_file=".rdd-docs/requirements.md.backup.$(date +%Y%m%d-%H%M%S)"
            cp ".rdd-docs/requirements.md" "$backup_file"
            print_success "Created backup: $backup_file"
        fi
    fi
    
    if [ "$dry_run" = true ]; then
        print_info "DRY RUN - No changes will be made"
        action_preview_requirements_merge
        return 0
    fi
    
    # Create temporary file for merged content
    local temp_file=$(mktemp)
    local id_mapping_file=$(mktemp)
    
    echo "# ID Mapping for merge on $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$id_mapping_file"
    echo "# Old ID (workspace) -> New ID (requirements.md)" >> "$id_mapping_file"
    echo "" >> "$id_mapping_file"
    
    # If requirements.md doesn't exist, create from template
    if [ ! -f ".rdd-docs/requirements.md" ]; then
        print_warning "requirements.md not found - creating from template"
        if [ -f ".rdd/templates/requirements.md" ]; then
            cp ".rdd/templates/requirements.md" ".rdd-docs/requirements.md"
        else
            # Create minimal template
            cat > ".rdd-docs/requirements.md" << 'EOFREQ'
# Overview

<OVERVIEW-PLACEHOLDER>

# General Functionalities

# Functional Requirements

# Non-Functional Requirements

# Technical Requirements

EOFREQ
        fi
    fi
    
    # Copy current requirements to temp file
    cp ".rdd-docs/requirements.md" "$temp_file"
    
    # Process each section: General Functionalities, Functional Requirements, Non-Functional Requirements, Technical Requirements
    local sections=("General Functionalities" "Functional Requirements" "Non-Functional Requirements" "Technical Requirements")
    local prefixes=("GF" "FR" "NFR" "TR")
    
    for i in "${!sections[@]}"; do
        local section="${sections[$i]}"
        local prefix="${prefixes[$i]}"
        
        # Get next available ID for this section
        local next_id=$(get_next_id "$prefix" "$temp_file")
        
        # Extract changes for this section from requirements-changes.md
        local section_changes=$(mktemp)
        
        # Find section in requirements-changes.md and extract items
        awk -v section="$section" '
            /^## / { 
                # Extract section name (everything after "## ")
                current_section = substr($0, 4)
                # Trim leading/trailing whitespace
                gsub(/^[[:space:]]+|[[:space:]]+$/, "", current_section)
                in_section = (current_section == section)
                next 
            }
            in_section && /^- \*\*\[/ { print }
        ' ".rdd-docs/workspace/requirements-changes.md" > "$section_changes"
        
        if [ -s "$section_changes" ]; then
            # Process ADDED items
            while IFS= read -r line; do
                if [[ "$line" =~ ^\-[[:space:]]\*\*\[ADDED\] ]]; then
                    # Extract the workspace ID and text
                    local workspace_id=""
                    local req_text=""
                    
                    # Check if line has an ID like [FR-01] or [GF-01]
                    if [[ "$line" =~ \[ADDED\][[:space:]]*\[($prefix-[0-9]+)\] ]]; then
                        workspace_id="${BASH_REMATCH[1]}"
                        # Extract text after the workspace ID
                        req_text=$(echo "$line" | sed "s/^- \*\*\[ADDED\] \[$workspace_id\]/- **[$prefix-$next_id]/")
                    else
                        # No workspace ID, just add new ID
                        req_text=$(echo "$line" | sed "s/^- \*\*\[ADDED\]/- **[$prefix-$next_id]/")
                    fi
                    
                    # Log ID mapping if workspace ID existed
                    if [ -n "$workspace_id" ]; then
                        echo "$workspace_id -> $prefix-$next_id" >> "$id_mapping_file"
                        print_info "ID mapping: $workspace_id -> $prefix-$next_id"
                    fi
                    
                    # Add to appropriate section in temp file
                    # Insert before the next section header
                    awk -v section="$section" -v req="$req_text" '
                        /^# / {
                            if (in_section && !req_added) {
                                # Found next section header, insert requirement before it
                                print req
                                req_added = 1
                                in_section = 0
                            }
                            if ($0 ~ "^# " section "$") {
                                # Found our target section
                                in_section = 1
                            }
                            print
                            next
                        }
                        { print }
                        END {
                            # If we reached EOF while still in section, add requirement at end
                            if (in_section && !req_added) {
                                print req
                            }
                        }
                    ' "$temp_file" > "${temp_file}.new"
                    mv "${temp_file}.new" "$temp_file"
                    
                    print_success "Added: $(echo "$req_text" | cut -c1-70)..."
                    
                    # Increment ID for next requirement
                    next_id=$(printf "%02d" $((10#$next_id + 1)))
                fi
            done < "$section_changes"
            
            # Handle MODIFIED and DELETED (flag for manual review)
            if grep -q "^\- \*\*\[MODIFIED\]" "$section_changes"; then
                print_warning "MODIFIED items found in $section - please review manually"
            fi
            
            if grep -q "^\- \*\*\[DELETED\]" "$section_changes"; then
                print_warning "DELETED items found in $section - please review manually"
            fi
        fi
        
        rm "$section_changes"
    done
    
    # Move temp file to final location
    mv "$temp_file" ".rdd-docs/requirements.md"
    
    # Save ID mapping to workspace
    if [ -f ".rdd-docs/workspace/.id-mapping.txt" ]; then
        cat "$id_mapping_file" >> ".rdd-docs/workspace/.id-mapping.txt"
    else
        cp "$id_mapping_file" ".rdd-docs/workspace/.id-mapping.txt"
    fi
    rm "$id_mapping_file"
    
    print_success "Requirements merged successfully"
    print_info "ID mapping saved to .rdd-docs/workspace/.id-mapping.txt"
    print_info "Review .rdd-docs/requirements.md for MODIFIED/DELETED items"
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
        merge-requirements-changes)
            action_merge_requirements_changes "$@"
            ;;
        preview-requirements-merge)
            action_preview_requirements_merge
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
