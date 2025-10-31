#!/bin/bash
# Script to manage the wrap-up phase - merge requirements and archive workspace
# Part of RDD (Requirements-Driven Development) framework

set -e  # Exit on error

WORKSPACE_DIR=".rdd-docs/workspace"
REQUIREMENTS_FILE=".rdd-docs/requirements.md"
ARCHIVE_DIR=".rdd-docs/archive"
CURRENT_CHANGE_FILE="$WORKSPACE_DIR/.current-change"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper function to print colored messages
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

# Function to display usage
usage() {
    cat << EOF
Usage: $(basename "$0") <action> [options]

Actions:
  sync-main             Fetch and merge latest changes from main branch
  merge-requirements    Merge requirements-changes.md into requirements.md
  archive-workspace     Archive workspace content to archive/<change-id>/
  full-wrap-up          Execute full wrap-up: sync-main + merge + archive
  get-change-id         Get current change ID from .current-change
  validate-merge        Validate merge readiness (check for conflicts)
  preview-merge         Show what would be merged without making changes
  help                  Show this help message

Examples:
  $(basename "$0") sync-main
  $(basename "$0") merge-requirements
  $(basename "$0") archive-workspace
  $(basename "$0") full-wrap-up
  $(basename "$0") preview-merge

Options:
  --dry-run            Preview actions without making changes
  --backup             Create backup before merge

EOF
}

# Function to get current change ID
get_change_id() {
    if [ ! -f "$CURRENT_CHANGE_FILE" ]; then
        print_error "No current change found (.current-change file missing)"
        return 1
    fi
    
    if command -v jq &> /dev/null; then
        jq -r '.changeId' "$CURRENT_CHANGE_FILE"
    else
        # Fallback without jq
        grep -o '"changeId"[[:space:]]*:[[:space:]]*"[^"]*"' "$CURRENT_CHANGE_FILE" | cut -d'"' -f4
    fi
}

# Function to validate merge readiness
action_validate_merge() {
    print_info "Validating merge readiness..."
    
    local has_errors=0
    
    # Check if requirements-changes.md exists
    if [ ! -f "$WORKSPACE_DIR/requirements-changes.md" ]; then
        print_error "requirements-changes.md not found in workspace"
        has_errors=1
    fi
    
    # Check if requirements.md exists
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        print_warning "requirements.md not found - will be created"
    fi
    
    # Validate requirements-changes.md format
    if [ -f "$WORKSPACE_DIR/requirements-changes.md" ]; then
        if ! .rdd/scripts/clarify-changes.sh validate 2>/dev/null; then
            print_warning "requirements-changes.md has format issues - continuing anyway"
        fi
    fi
    
    if [ $has_errors -eq 0 ]; then
        print_success "Validation passed - ready to merge"
        return 0
    else
        print_error "Validation failed - cannot proceed with merge"
        return 1
    fi
}

# Function to sync with main branch
action_sync_main() {
    print_info "Syncing with main branch..."
    
    # Get current branch
    local current_branch=$(git branch --show-current)
    
    if [ "$current_branch" = "main" ]; then
        print_warning "Already on main branch - no sync needed"
        return 0
    fi
    
    print_info "Current branch: $current_branch"
    
    # Check if there are uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        print_warning "Uncommitted changes detected - committing automatically"
        
        # Get change info from .current-change
        local change_name=""
        local change_type=""
        
        if [ -f "$CURRENT_CHANGE_FILE" ]; then
            if command -v jq &> /dev/null; then
                change_name=$(jq -r '.changeName' "$CURRENT_CHANGE_FILE")
                change_type=$(jq -r '.changeType' "$CURRENT_CHANGE_FILE")
            else
                # Fallback without jq
                change_name=$(grep -o '"changeName"[[:space:]]*:[[:space:]]*"[^"]*"' "$CURRENT_CHANGE_FILE" | cut -d'"' -f4)
                change_type=$(grep -o '"changeType"[[:space:]]*:[[:space:]]*"[^"]*"' "$CURRENT_CHANGE_FILE" | cut -d'"' -f4)
            fi
        fi
        
        # Default values if not found
        if [ -z "$change_type" ]; then
            change_type="chore"
        fi
        if [ -z "$change_name" ]; then
            change_name="workspace-changes"
        fi
        
        # Create commit message
        local commit_message="$change_type: $change_name - pre-wrap-up commit"
        
        # Stage all changes
        print_info "Staging all changes..."
        git add -A
        
        # Commit
        print_info "Creating commit: $commit_message"
        if git commit -m "$commit_message"; then
            print_success "Changes committed successfully"
        else
            print_error "Failed to commit changes"
            return 1
        fi
    else
        print_info "No uncommitted changes detected"
    fi
    
    # Fetch latest from origin
    print_info "Fetching latest changes from origin..."
    if ! git fetch origin main; then
        print_error "Failed to fetch from origin/main"
        return 1
    fi
    print_success "Fetched latest changes"
    
    # Merge origin/main into current branch
    print_info "Merging origin/main into $current_branch..."
    if ! git merge origin/main --no-edit; then
        print_error "Merge conflicts detected!"
        echo ""
        print_error "Please resolve conflicts manually:"
        echo "  1. Fix conflicts in the affected files"
        echo "  2. Run: git add <resolved-files>"
        echo "  3. Run: git merge --continue"
        echo "  4. Then re-run wrap-up"
        return 1
    fi
    
    print_success "Successfully merged origin/main into $current_branch"
    print_info "Your branch is now up-to-date with main"
    
    # Display merge summary
    echo ""
    print_info "Recent changes from main:"
    git log --oneline --graph --max-count=5 origin/main
    
    return 0
}

# Function to preview merge
action_preview_merge() {
    print_info "Previewing requirements merge..."
    
    if [ ! -f "$WORKSPACE_DIR/requirements-changes.md" ]; then
        print_error "requirements-changes.md not found"
        return 1
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "   MERGE PREVIEW"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Count changes by type
    local added_count=$(grep -c "^\- \*\*\[ADDED\]" "$WORKSPACE_DIR/requirements-changes.md" || true)
    local modified_count=$(grep -c "^\- \*\*\[MODIFIED\]" "$WORKSPACE_DIR/requirements-changes.md" || true)
    local deleted_count=$(grep -c "^\- \*\*\[DELETED\]" "$WORKSPACE_DIR/requirements-changes.md" || true)
    
    echo "Changes to be applied:"
    echo "  [ADDED]    : $added_count requirements"
    echo "  [MODIFIED] : $modified_count requirements"
    echo "  [DELETED]  : $deleted_count requirements"
    echo ""
    
    # Show actual changes
    echo "━━━ ADDED Requirements ━━━"
    grep "^\- \*\*\[ADDED\]" "$WORKSPACE_DIR/requirements-changes.md" || echo "  (none)"
    echo ""
    
    echo "━━━ MODIFIED Requirements ━━━"
    grep "^\- \*\*\[MODIFIED\]" "$WORKSPACE_DIR/requirements-changes.md" || echo "  (none)"
    echo ""
    
    echo "━━━ DELETED Requirements ━━━"
    grep "^\- \*\*\[DELETED\]" "$WORKSPACE_DIR/requirements-changes.md" || echo "  (none)"
    echo ""
    
    print_info "This is a preview only. Run 'merge-requirements' to apply changes."
}

# Function to merge requirements
action_merge_requirements() {
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
    if ! action_validate_merge; then
        return 1
    fi
    
    # Create backup if requested
    if [ "$create_backup" = true ]; then
        if [ -f "$REQUIREMENTS_FILE" ]; then
            local backup_file="${REQUIREMENTS_FILE}.backup.$(date +%Y%m%d-%H%M%S)"
            cp "$REQUIREMENTS_FILE" "$backup_file"
            print_success "Created backup: $backup_file"
        fi
    fi
    
    if [ "$dry_run" = true ]; then
        print_info "DRY RUN - No changes will be made"
        action_preview_merge
        return 0
    fi
    
    # Create temporary file for merged content
    local temp_file=$(mktemp)
    local id_mapping_file=$(mktemp)
    
    echo "# ID Mapping for merge on $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$id_mapping_file"
    echo "# Old ID (workspace) -> New ID (requirements.md)" >> "$id_mapping_file"
    echo "" >> "$id_mapping_file"
    
    # If requirements.md doesn't exist, create from template
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        print_warning "requirements.md not found - creating from template"
        if [ -f ".rdd/templates/requirements.md" ]; then
            cp ".rdd/templates/requirements.md" "$REQUIREMENTS_FILE"
        else
            # Create minimal template
            cat > "$REQUIREMENTS_FILE" << 'EOFREQ'
# Overview

<OVERVIEW-PLACEHOLDER>

# General Functionalities

# Functional requirements

# Non-functional requirements

# Technical requirements

EOFREQ
        fi
    fi
    
    # Copy current requirements to temp file
    cp "$REQUIREMENTS_FILE" "$temp_file"
    
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
    
    # Process each section: General Functionalities, Functional requirements, Non-functional requirements, Technical requirements
    local sections=("General Functionalities" "Functional requirements" "Non-functional requirements" "Technical requirements")
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
            /^## / { current_section = substr($0, 4); next }
            current_section == section && /^- \*\*\[/ { print }
        ' "$WORKSPACE_DIR/requirements-changes.md" > "$section_changes"
        
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
                    awk -v section="$section" -v req="$req_text" '
                        /^# '"$section"'/ { 
                            print
                            getline
                            print
                            if ($0 !~ /^$/) {
                                # Section has content, add after first line
                                print req
                            } else {
                                # Empty section, just add
                                print req
                            }
                            next 
                        }
                        { print }
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
    mv "$temp_file" "$REQUIREMENTS_FILE"
    
    # Save ID mapping to archive (will be done during archive step)
    if [ -f "$WORKSPACE_DIR/.id-mapping.txt" ]; then
        cat "$id_mapping_file" >> "$WORKSPACE_DIR/.id-mapping.txt"
    else
        mv "$id_mapping_file" "$WORKSPACE_DIR/.id-mapping.txt"
    fi
    
    print_success "Requirements merged successfully"
    print_info "ID mapping saved to workspace/.id-mapping.txt"
    print_info "Review $REQUIREMENTS_FILE for MODIFIED/DELETED items"
}

# Function to archive workspace
action_archive_workspace() {
    print_info "Archiving workspace content..."
    
    # Get change ID
    local change_id=$(get_change_id)
    if [ -z "$change_id" ]; then
        print_error "Could not determine change ID"
        return 1
    fi
    
    print_info "Change ID: $change_id"
    
    # Create archive directory if needed
    mkdir -p "$ARCHIVE_DIR"
    
    # Create change-specific archive directory
    local archive_path="$ARCHIVE_DIR/$change_id"
    
    if [ -d "$archive_path" ]; then
        print_warning "Archive directory already exists: $archive_path"
        print_warning "Files will be overwritten"
    fi
    
    mkdir -p "$archive_path"
    
    # Copy workspace content (excluding .backups and .current-change)
    local files_to_archive=("change.md" "open-questions.md" "requirements-changes.md" "clarification-log.jsonl" "clarity-taxonomy.md" ".id-mapping.txt")
    
    for file in "${files_to_archive[@]}"; do
        if [ -f "$WORKSPACE_DIR/$file" ]; then
            cp "$WORKSPACE_DIR/$file" "$archive_path/$file"
            print_success "Archived: $file"
        else
            if [ "$file" != ".id-mapping.txt" ]; then
                print_warning "File not found: $file (skipped)"
            fi
        fi
    done
    
    # Create archive metadata
    cat > "$archive_path/.archive-info" << EOF
{
  "archivedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "changeId": "$change_id",
  "archivedBy": "wrap-up.sh script"
}
EOF
    
    print_success "Workspace archived to: $archive_path"
}

# Function to perform full wrap-up
action_full_wrap_up() {
    print_info "Starting full wrap-up process..."
    echo ""
    
    # Step 1: Sync with main
    print_info "Step 1/4: Syncing with main branch"
    if ! action_sync_main; then
        print_error "Sync failed - aborting wrap-up"
        print_warning "Please resolve any merge conflicts and try again"
        return 1
    fi
    echo ""
    
    # Step 2: Validate
    print_info "Step 2/4: Validating merge readiness"
    if ! action_validate_merge; then
        print_error "Validation failed - aborting wrap-up"
        return 1
    fi
    echo ""
    
    # Step 3: Merge requirements
    print_info "Step 3/4: Merging requirements"
    if ! action_merge_requirements --backup; then
        print_error "Merge failed - aborting wrap-up"
        return 1
    fi
    echo ""
    
    # Step 4: Archive workspace
    print_info "Step 4/4: Archiving workspace"
    if ! action_archive_workspace; then
        print_error "Archive failed - aborting wrap-up"
        return 1
    fi
    echo ""
    
    print_success "Full wrap-up completed successfully!"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "   WRAP-UP COMPLETE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "✓ Synced with main branch"
    echo "✓ Requirements merged"
    echo "✓ Workspace archived"
    echo ""
    echo "Next steps:"
    echo "  1. Review .rdd-docs/requirements.md"
    echo "  2. Clean workspace (optional): .rdd/scripts/clarify-changes.sh clear"
    echo "  3. Commit changes to repository"
    echo "  4. Merge branch to main"
}

# Main script logic
main() {
    if [ $# -eq 0 ]; then
        usage
        exit 1
    fi
    
    local action="$1"
    shift
    
    case "$action" in
        sync-main)
            action_sync_main
            ;;
        merge-requirements)
            action_merge_requirements "$@"
            ;;
        archive-workspace)
            action_archive_workspace
            ;;
        full-wrap-up)
            action_full_wrap_up
            ;;
        get-change-id)
            get_change_id
            ;;
        validate-merge)
            action_validate_merge
            ;;
        preview-merge)
            action_preview_merge
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

# Run main function
main "$@"
