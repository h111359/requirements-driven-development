#!/bin/bash

# workspace-utils.sh
# Workspace management utility functions for RDD framework
# Provides workspace initialization, archiving, backup/restore, and template management

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
if [ -n "$WORKSPACE_UTILS_LOADED" ]; then
    return 0
fi
WORKSPACE_UTILS_LOADED=1

# ============================================================================
# CONSTANTS AND CONFIGURATION
# ============================================================================

WORKSPACE_DIR=".rdd-docs/workspace"
ARCHIVE_BASE_DIR=".rdd-docs/archive"
BACKUP_DIR="$WORKSPACE_DIR/.backups"
TEMPLATES_DIR=".rdd/templates"

# ============================================================================
# WORKSPACE INITIALIZATION
# ============================================================================

# Initialize workspace with templates based on type (change or fix)
# Usage: init_workspace "change|fix"
# Returns: 0 on success, 1 on failure
init_workspace() {
    local workspace_type="${1:-change}"
    
    if [[ ! "$workspace_type" =~ ^(change|fix)$ ]]; then
        print_error "Invalid workspace type: $workspace_type"
        print_info "Valid types: change, fix"
        return 1
    fi
    
    print_step "Initializing workspace for type: $workspace_type..."
    
    # Ensure workspace directory exists
    ensure_dir "$WORKSPACE_DIR"
    
    # Copy main template based on type
    if [ "$workspace_type" = "fix" ]; then
        copy_template "fix.md" "$WORKSPACE_DIR/fix.md"
    fi
    
    # Copy copilot-prompts.md template to workspace with new name
    copy_template "copilot-prompts.md" "$WORKSPACE_DIR/.rdd.copilot-prompts.md"
    
    print_success "Workspace initialized successfully for $workspace_type"
    return 0
}

# ============================================================================
# WORKSPACE ARCHIVING
# ============================================================================

# Archive workspace to branch-specific folder
# Usage: archive_workspace "branch_name" [keep_workspace]
# keep_workspace: "true" to keep workspace after archiving, "false" to remove (default: false)
# Returns: 0 on success, 1 on failure
archive_workspace() {
    local branch_name="$1"
    local keep_workspace="${2:-false}"
    
    if [ -z "$branch_name" ]; then
        print_error "Branch name is required"
        echo "Usage: archive_workspace <branch_name> [keep_workspace]"
        return 1
    fi
    
    # Check if workspace exists and has content
    if [ ! -d "$WORKSPACE_DIR" ]; then
        print_error "Workspace directory does not exist: $WORKSPACE_DIR"
        return 1
    fi
    
    if [ -z "$(ls -A "$WORKSPACE_DIR" 2>/dev/null)" ]; then
        print_error "Workspace directory is empty: $WORKSPACE_DIR"
        return 1
    fi
    
    # Create archive directory named after the branch
    # Remove any slashes and replace with hyphens
    local safe_branch_name="${branch_name//\//-}"
    local archive_dir="$ARCHIVE_BASE_DIR/$safe_branch_name"
    
    # Check if archive already exists
    if [ -d "$archive_dir" ]; then
        print_warning "Archive directory already exists: $archive_dir"
        if ! confirm_action "Overwrite existing archive?"; then
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
    local git_user=$(get_git_user)
    local last_commit=$(get_last_commit_sha)
    local last_message=$(get_last_commit_message)
    
    cat > "$archive_dir/.archive-metadata" << EOF
{
  "archivedAt": "$(get_timestamp)",
  "branch": "$branch_name",
  "archivedBy": "$git_user",
  "lastCommit": "$last_commit",
  "lastCommitMessage": "$last_message"
}
EOF
    
    print_success "Workspace archived to: $archive_dir"
    
    # Clean up workspace unless keep_workspace is true
    if [ "$keep_workspace" = "false" ]; then
        clear_workspace_forced
        print_info "Workspace directory cleared"
    else
        print_info "Workspace directory kept as requested"
    fi
    
    return 0
}

# ============================================================================
# BACKUP AND RESTORE
# ============================================================================

# Create backup of workspace files with timestamp
# Usage: backup_workspace
# Returns: 0 on success, 1 on failure
# Outputs: backup path on stdout
backup_workspace() {
    print_step "Creating backup of workspace files..."
    
    if [ ! -d "$WORKSPACE_DIR" ]; then
        print_error "Workspace directory does not exist: $WORKSPACE_DIR"
        return 1
    fi
    
    # Create backup directory with timestamp
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local backup_path="$BACKUP_DIR/$timestamp"
    mkdir -p "$backup_path"
    
    # Backup key files
    local files_to_backup=(
        "fix.md"
        "open-questions.md"
        "clarity-checklist.md"
    )
    
    # Add config files (.rdd.fix.* or .rdd.enh.*)
    local config_file=$(find_change_config "$WORKSPACE_DIR")
    if [ -n "$config_file" ]; then
        files_to_backup+=("$(basename "$config_file")")
    fi
    
    local backed_up_count=0
    for file in "${files_to_backup[@]}"; do
        if [ -f "$WORKSPACE_DIR/$file" ]; then
            cp "$WORKSPACE_DIR/$file" "$backup_path/$file"
            debug_print "Backed up $file"
            ((backed_up_count++))
        fi
    done
    
    if [ $backed_up_count -eq 0 ]; then
        print_warning "No files found to backup"
        rm -rf "$backup_path"
        return 1
    fi
    
    print_success "Backup created at $backup_path ($backed_up_count files)"
    echo "$backup_path"
    return 0
}

# Restore workspace from latest backup
# Usage: restore_workspace [backup_path]
# If backup_path not provided, uses latest backup
# Returns: 0 on success, 1 on failure
restore_workspace() {
    local backup_path="$1"
    
    # If no backup path provided, find latest
    if [ -z "$backup_path" ]; then
        if [ ! -d "$BACKUP_DIR" ] || [ -z "$(ls -A "$BACKUP_DIR" 2>/dev/null)" ]; then
            print_error "No backups found in $BACKUP_DIR"
            return 1
        fi
        
        # Get latest backup directory
        local latest_backup=$(ls -t "$BACKUP_DIR" | head -n 1)
        backup_path="$BACKUP_DIR/$latest_backup"
        print_info "Using latest backup: $latest_backup"
    fi
    
    if [ ! -d "$backup_path" ]; then
        print_error "Backup directory not found: $backup_path"
        return 1
    fi
    
    print_step "Restoring from backup: $(basename "$backup_path")"
    
    # Ensure workspace directory exists
    ensure_dir "$WORKSPACE_DIR"
    
    # Restore files
    local restored_count=0
    for file in "$backup_path"/*; do
        if [ -f "$file" ]; then
            local filename=$(basename "$file")
            cp "$file" "$WORKSPACE_DIR/$filename"
            debug_print "Restored $filename"
            ((restored_count++))
        fi
    done
    
    if [ $restored_count -eq 0 ]; then
        print_warning "No files found in backup to restore"
        return 1
    fi
    
    print_success "Workspace restored from backup ($restored_count files)"
    return 0
}

# ============================================================================
# WORKSPACE CLEARING
# ============================================================================

# Clear workspace with safety confirmation
# Usage: clear_workspace
# Returns: 0 on success, 1 if cancelled
clear_workspace() {
    print_warning "This will clear all workspace files."
    
    if [ -d "$WORKSPACE_DIR" ] && [ -n "$(ls -A "$WORKSPACE_DIR" 2>/dev/null)" ]; then
        print_info "Current workspace contains:"
        ls -lh "$WORKSPACE_DIR" | tail -n +2 | awk '{print "  - " $9}'
        echo ""
    fi
    
    if ! confirm_action "Are you sure you want to clear the workspace?"; then
        print_info "Operation cancelled"
        return 1
    fi
    
    clear_workspace_forced
    return 0
}

# Clear workspace without confirmation (internal use)
# Usage: clear_workspace_forced
# Returns: 0 on success
clear_workspace_forced() {
    if [ ! -d "$WORKSPACE_DIR" ]; then
        debug_print "Workspace directory does not exist"
        return 0
    fi
    
    # Remove all files and subdirectories in workspace, but keep the workspace directory itself
    # This ensures everything is cleaned up, not just a hardcoded list
    find "$WORKSPACE_DIR" -mindepth 1 -delete
    debug_print "Removed all contents from $WORKSPACE_DIR"
    
    # Remove backup directory if it exists
    if [ -d "$BACKUP_DIR" ]; then
        rm -rf "$BACKUP_DIR"
        debug_print "Removed backup directory"
    fi
    
    print_success "Workspace cleared"
    return 0
}

# ============================================================================
# TEMPLATE MANAGEMENT
# ============================================================================

# Copy template file to destination with validation
# Usage: copy_template "template_name" "destination_path"
# Returns: 0 on success, 1 on failure
copy_template() {
    local template_name="$1"
    local destination="$2"
    
    if [ -z "$template_name" ] || [ -z "$destination" ]; then
        print_error "Template name and destination are required"
        echo "Usage: copy_template <template_name> <destination>"
        return 1
    fi
    
    local template_path="$TEMPLATES_DIR/$template_name"
    
    # Validate template exists
    if [ ! -f "$template_path" ]; then
        print_error "Template not found: $template_path"
        return 1
    fi
    
    # Create destination directory if needed
    local dest_dir=$(dirname "$destination")
    ensure_dir "$dest_dir"
    
        # Check if destination already exists
    if [ -f "$destination" ]; then
        print_warning "Destination file already exists: $destination"
        if ! confirm_action "Overwrite existing file?"; then
            print_info "Copy cancelled by user"
            return 1
        fi
    fi
    
    # Copy template
    cp "$template_path" "$destination"
    print_success "Copied template $template_name to $destination"
    return 0
}

# ============================================================================
# WORKSPACE STATUS AND INFORMATION
# ============================================================================

# ============================================================================
# WORKSPACE INSPECTION
# ============================================================================

# Check if workspace exists and has content
# Usage: check_workspace_exists
# Returns: 0 if workspace exists with content, 1 otherwise
check_workspace_exists() {
    if [ ! -d "$WORKSPACE_DIR" ]; then
        print_error "Workspace directory does not exist: $WORKSPACE_DIR"
        return 1
    fi
    
    if [ -z "$(ls -A "$WORKSPACE_DIR" 2>/dev/null)" ]; then
        print_error "Workspace directory is empty: $WORKSPACE_DIR"
        return 1
    fi
    
    debug_print "Workspace directory found with content"
    return 0
}

# List workspace files
# Usage: list_workspace_files
# Returns: 0 on success
list_workspace_files() {
    if ! check_workspace_exists; then
        return 1
    fi
    
    print_info "Workspace files:"
    ls -lh "$WORKSPACE_DIR" | tail -n +2 | while read -r line; do
        local filename=$(echo "$line" | awk '{print $9}')
        local size=$(echo "$line" | awk '{print $5}')
        echo "  - $filename ($size)"
    done
    
    return 0
}

# Get workspace status
# Usage: get_workspace_status
# Returns: 0 on success
get_workspace_status() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  WORKSPACE STATUS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    if [ -d "$WORKSPACE_DIR" ]; then
        print_success "Workspace directory exists: $WORKSPACE_DIR"
        
        local file_count=$(find "$WORKSPACE_DIR" -maxdepth 1 -type f | wc -l)
        print_info "Files in workspace: $file_count"
        
        if [ $file_count -gt 0 ]; then
            echo ""
            list_workspace_files
        fi
        
        # Check for current change config
        local config_file=$(find_change_config "$WORKSPACE_DIR")
        if [ -n "$config_file" ] && [ -f "$config_file" ]; then
            echo ""
            print_info "Current change configuration:"
            if command -v jq &> /dev/null; then
                cat "$config_file" | jq .
            else
                cat "$config_file"
            fi
        fi
    else
        print_warning "Workspace directory does not exist: $WORKSPACE_DIR"
    fi
    
    # Check for backups
    if [ -d "$BACKUP_DIR" ]; then
        local backup_count=$(find "$BACKUP_DIR" -maxdepth 1 -type d | wc -l)
        ((backup_count--)) # Subtract the backup directory itself
        if [ $backup_count -gt 0 ]; then
            echo ""
            print_info "Backups available: $backup_count"
            print_info "Latest backup: $(ls -t "$BACKUP_DIR" | head -n 1)"
        fi
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return 0
}

# ============================================================================
# EXPORT ALL FUNCTIONS
# ============================================================================

# Export all functions so they can be used by scripts that source this file
export -f init_workspace
export -f archive_workspace
export -f backup_workspace
export -f restore_workspace
export -f clear_workspace
export -f clear_workspace_forced
export -f copy_template
export -f check_workspace_exists
export -f list_workspace_files
export -f get_workspace_status

debug_print "workspace-utils.sh loaded successfully"
