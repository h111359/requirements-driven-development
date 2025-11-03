#!/bin/bash

# requirements-utils.sh
# Requirements management utility functions for RDD framework
# Provides validation, merging, ID assignment, and analysis for requirements

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
if [ -n "$REQUIREMENTS_UTILS_LOADED" ]; then
    return 0
fi
REQUIREMENTS_UTILS_LOADED=1

# ============================================================================
# CONSTANTS
# ============================================================================

REQUIREMENTS_FILE=".rdd-docs/requirements.md"
WORKSPACE_REQUIREMENTS=".rdd-docs/workspace/requirements-changes.md"
ID_MAPPING_FILE=".rdd-docs/workspace/.id-mapping.txt"

# Section names and their ID prefixes
declare -A SECTION_PREFIXES=(
    ["General Functionalities"]="GF"
    ["Functional Requirements"]="FR"
    ["Non-Functional Requirements"]="NFR"
    ["Technical Requirements"]="TR"
)

# ============================================================================
# VALIDATION
# ============================================================================

# Validate requirements-changes.md format
# Usage: validate_requirements [file_path]
# Returns: 0 if valid, 1 if invalid
validate_requirements() {
    local req_file="${1:-$WORKSPACE_REQUIREMENTS}"
    
    if [ ! -f "$req_file" ]; then
        print_error "Requirements file not found: $req_file"
        return 1
    fi
    
    print_step "Validating requirements format: $(basename "$req_file")"
    
    local has_errors=0
    local line_num=0
    
    while IFS= read -r line; do
        ((line_num++))
        
        # Skip empty lines, comments, markdown headers, blockquotes, and horizontal rules
        if [[ -z "$line" ]] || \
           [[ "$line" =~ ^#.* ]] || \
           [[ "$line" =~ ^[[:space:]]*$ ]] || \
           [[ "$line" =~ ^\>.* ]] || \
           [[ "$line" =~ ^--.* ]]; then
            continue
        fi
        
        # Check if line starts with a list marker (- or *)
        if [[ "$line" =~ ^[[:space:]]*[-\*][[:space:]].* ]]; then
            # Extract the content after the list marker
            local content=$(echo "$line" | sed 's/^[[:space:]]*[-*][[:space:]]*//')
            
            # Check if it starts with a valid prefix
            if [[ ! "$content" =~ ^\[ADDED\].*$ ]] && \
               [[ ! "$content" =~ ^\[MODIFIED\].*$ ]] && \
               [[ ! "$content" =~ ^\[DELETED\].*$ ]]; then
                print_warning "Line $line_num: Missing or invalid prefix [ADDED|MODIFIED|DELETED]"
                echo "  → $(echo "$line" | cut -c1-80)"
                has_errors=1
            fi
            
            # Additional validation for MODIFIED and DELETED - must have existing ID
            if [[ "$content" =~ ^\[MODIFIED\].*$ ]] || [[ "$content" =~ ^\[DELETED\].*$ ]]; then
                if [[ ! "$content" =~ \[MODIFIED\][[:space:]]*\[[A-Z]+-[0-9]+\] ]] && \
                   [[ ! "$content" =~ \[DELETED\][[:space:]]*\[[A-Z]+-[0-9]+\] ]]; then
                    print_warning "Line $line_num: MODIFIED/DELETED must include existing ID [PREFIX-##]"
                    echo "  → $(echo "$line" | cut -c1-80)"
                    has_errors=1
                fi
            fi
        fi
    done < "$req_file"
    
    if [ $has_errors -eq 0 ]; then
        print_success "Validation passed: format is correct"
        return 0
    else
        print_warning "Validation completed with warnings"
        return 1
    fi
}

# ============================================================================
# ID MANAGEMENT
# ============================================================================

# Get next available ID for a requirement section
# Usage: get_next_id "PREFIX" [file_path]
# Returns: next ID as string (e.g., "01", "02")
get_next_id() {
    local prefix="$1"
    local file="${2:-$REQUIREMENTS_FILE}"
    
    if [ -z "$prefix" ]; then
        print_error "Prefix is required"
        echo "Usage: get_next_id <PREFIX> [file_path]"
        return 1
    fi
    
    if [ ! -f "$file" ]; then
        # If file doesn't exist, start from 01
        echo "01"
        return 0
    fi
    
    # Find all IDs with this prefix and extract the number
    local max_id=$(grep -oP "\[$prefix-\K[0-9]+" "$file" 2>/dev/null | sort -n | tail -1)
    
    if [ -z "$max_id" ]; then
        echo "01"
    else
        printf "%02d" $((max_id + 1))
    fi
}

# Track ID mapping for requirements
# Usage: track_id_mapping "old_id" "new_id" [mapping_file]
# Returns: 0 on success
track_id_mapping() {
    local old_id="$1"
    local new_id="$2"
    local mapping_file="${3:-$ID_MAPPING_FILE}"
    
    if [ -z "$old_id" ] || [ -z "$new_id" ]; then
        print_error "Both old_id and new_id are required"
        echo "Usage: track_id_mapping <old_id> <new_id> [mapping_file]"
        return 1
    fi
    
    # Ensure directory exists
    local mapping_dir=$(dirname "$mapping_file")
    ensure_dir "$mapping_dir"
    
    # Create file with header if it doesn't exist
    if [ ! -f "$mapping_file" ]; then
        cat > "$mapping_file" << EOF
# ID Mapping Log
# Tracks requirement ID changes during merges
# Format: OLD_ID -> NEW_ID (timestamp)

EOF
    fi
    
    # Append mapping
    echo "$old_id -> $new_id ($(get_timestamp))" >> "$mapping_file"
    debug_print "ID mapping tracked: $old_id -> $new_id"
    
    return 0
}

# ============================================================================
# MERGE PREVIEW
# ============================================================================

# Preview requirements merge without making changes
# Usage: preview_merge
# Returns: 0 on success
preview_merge() {
    if [ ! -f "$WORKSPACE_REQUIREMENTS" ]; then
        print_error "Requirements changes file not found: $WORKSPACE_REQUIREMENTS"
        return 1
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  MERGE PREVIEW"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Count changes by type
    local added_count=$(grep -c "^- \*\*\[ADDED\]" "$WORKSPACE_REQUIREMENTS" 2>/dev/null || echo "0")
    local modified_count=$(grep -c "^- \*\*\[MODIFIED\]" "$WORKSPACE_REQUIREMENTS" 2>/dev/null || echo "0")
    local deleted_count=$(grep -c "^- \*\*\[DELETED\]" "$WORKSPACE_REQUIREMENTS" 2>/dev/null || echo "0")
    
    print_info "Changes to be applied:"
    echo "  ${GREEN}[ADDED]${NC}    : $added_count requirements"
    echo "  ${YELLOW}[MODIFIED]${NC} : $modified_count requirements"
    echo "  ${RED}[DELETED]${NC}  : $deleted_count requirements"
    echo ""
    
    local total=$((added_count + modified_count + deleted_count))
    if [ $total -eq 0 ]; then
        print_warning "No changes detected"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        return 0
    fi
    
    # Show actual changes
    if [ $added_count -gt 0 ]; then
        echo "━━━ ADDED Requirements ━━━"
        grep "^- \*\*\[ADDED\]" "$WORKSPACE_REQUIREMENTS" | while read -r line; do
            echo "  $(echo "$line" | cut -c1-100)"
        done
        echo ""
    fi
    
    if [ $modified_count -gt 0 ]; then
        echo "━━━ MODIFIED Requirements ━━━"
        grep "^- \*\*\[MODIFIED\]" "$WORKSPACE_REQUIREMENTS" | while read -r line; do
            echo "  $(echo "$line" | cut -c1-100)"
        done
        echo ""
    fi
    
    if [ $deleted_count -gt 0 ]; then
        echo "━━━ DELETED Requirements ━━━"
        grep "^- \*\*\[DELETED\]" "$WORKSPACE_REQUIREMENTS" | while read -r line; do
            echo "  $(echo "$line" | cut -c1-100)"
        done
        echo ""
    fi
    
    print_success "Total: $total requirement changes"
    echo ""
    print_info "Run 'merge_requirements' to apply these changes"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return 0
}

# ============================================================================
# REQUIREMENTS MERGING
# ============================================================================

# Merge requirements changes into main requirements file
# Usage: merge_requirements [dry_run] [create_backup]
# dry_run: "true" to preview only, "false" to apply (default: false)
# create_backup: "true" to create backup, "false" otherwise (default: true)
# Returns: 0 on success, 1 on failure
merge_requirements() {
    local dry_run="${1:-false}"
    local create_backup="${2:-true}"
    
    print_banner "MERGE REQUIREMENTS"
    echo ""
    
    # Validate merge readiness
    if [ ! -f "$WORKSPACE_REQUIREMENTS" ]; then
        print_error "Requirements changes file not found: $WORKSPACE_REQUIREMENTS"
        return 1
    fi
    
    # If dry run, just show preview
    if [ "$dry_run" = "true" ]; then
        print_info "DRY RUN - No changes will be made"
        echo ""
        preview_merge
        return 0
    fi
    
    # Validate format first
    if ! validate_requirements "$WORKSPACE_REQUIREMENTS"; then
        print_error "Validation failed - cannot proceed with merge"
        return 1
    fi
    echo ""
    
    # Create backup if requested
    if [ "$create_backup" = "true" ] && [ -f "$REQUIREMENTS_FILE" ]; then
        local backup_file="${REQUIREMENTS_FILE}.backup.$(date +%Y%m%d-%H%M%S)"
        cp "$REQUIREMENTS_FILE" "$backup_file"
        print_success "Created backup: $backup_file"
        echo ""
    fi
    
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

# Functional Requirements

# Non-Functional Requirements

# Technical Requirements

EOFREQ
        fi
        print_success "Created requirements.md"
        echo ""
    fi
    
    # Create temporary file for merged content
    local temp_file=$(mktemp)
    cp "$REQUIREMENTS_FILE" "$temp_file"
    
    # Process each section
    local sections=("General Functionalities" "Functional Requirements" "Non-Functional Requirements" "Technical Requirements")
    
    for section in "${sections[@]}"; do
        local prefix="${SECTION_PREFIXES[$section]}"
        
        if [ -z "$prefix" ]; then
            debug_print "No prefix found for section: $section"
            continue
        fi
        
        # Get next available ID for this section
        local next_id=$(get_next_id "$prefix" "$temp_file")
        
        # Extract changes for this section
        local section_changes=$(mktemp)
        awk -v section="$section" '
            /^## / { 
                current_section = substr($0, 4)
                gsub(/^[[:space:]]+|[[:space:]]+$/, "", current_section)
                in_section = (current_section == section)
                next 
            }
            in_section && /^- \*\*\[/ { print }
        ' "$WORKSPACE_REQUIREMENTS" > "$section_changes"
        
        if [ -s "$section_changes" ]; then
            # Process ADDED items
            while IFS= read -r line; do
                if [[ "$line" =~ ^\-[[:space:]]\*\*\[ADDED\] ]]; then
                    local workspace_id=""
                    local req_text=""
                    
                    # Check if line has a workspace ID
                    if [[ "$line" =~ \[ADDED\][[:space:]]*\[($prefix-[0-9]+)\] ]]; then
                        workspace_id="${BASH_REMATCH[1]}"
                        req_text=$(echo "$line" | sed "s/^- \*\*\[ADDED\] \[$workspace_id\]/- **[$prefix-$next_id]/")
                    else
                        req_text=$(echo "$line" | sed "s/^- \*\*\[ADDED\]/- **[$prefix-$next_id]/")
                    fi
                    
                    # Track ID mapping
                    if [ -n "$workspace_id" ]; then
                        track_id_mapping "$workspace_id" "$prefix-$next_id"
                        print_info "ID mapping: $workspace_id -> $prefix-$next_id"
                    fi
                    
                    # Add to appropriate section
                    awk -v section="$section" -v req="$req_text" '
                        /^# / {
                            if (in_section && !req_added) {
                                print req
                                req_added = 1
                                in_section = 0
                            }
                            if ($0 ~ "^# " section "$") {
                                in_section = 1
                            }
                            print
                            next
                        }
                        { print }
                        END {
                            if (in_section && !req_added) {
                                print req
                            }
                        }
                    ' "$temp_file" > "${temp_file}.new"
                    mv "${temp_file}.new" "$temp_file"
                    
                    print_success "Added [$prefix-$next_id]: $(echo "$req_text" | sed 's/^- \*\*\[[^]]*\]//' | cut -c1-60)..."
                    
                    # Increment ID
                    next_id=$(printf "%02d" $((10#$next_id + 1)))
                fi
            done < "$section_changes"
            
            # Warn about MODIFIED and DELETED
            local modified_in_section=$(grep -c "^\- \*\*\[MODIFIED\]" "$section_changes" 2>/dev/null || echo "0")
            local deleted_in_section=$(grep -c "^\- \*\*\[DELETED\]" "$section_changes" 2>/dev/null || echo "0")
            
            if [ $modified_in_section -gt 0 ]; then
                print_warning "$section: $modified_in_section MODIFIED items require manual review"
            fi
            
            if [ $deleted_in_section -gt 0 ]; then
                print_warning "$section: $deleted_in_section DELETED items require manual review"
            fi
        fi
        
        rm "$section_changes"
    done
    
    # Move temp file to final location
    mv "$temp_file" "$REQUIREMENTS_FILE"
    
    echo ""
    print_success "Requirements merge completed"
    print_info "ID mappings saved to: $ID_MAPPING_FILE"
    print_warning "Please review MODIFIED and DELETED items manually"
    
    return 0
}

# ============================================================================
# REQUIREMENTS ANALYSIS
# ============================================================================

# Analyze requirements impact comparing with main branch
# Usage: analyze_requirements_impact
# Returns: 0 on success
analyze_requirements_impact() {
    check_git_repo
    
    local default_branch=$(get_default_branch)
    
    print_banner "REQUIREMENTS IMPACT ANALYSIS"
    echo ""
    
    # Fetch latest
    fetch_main
    
    # Check if requirements.md has been directly modified
    local req_modified=$(git diff --name-only "origin/${default_branch}...HEAD" | grep "^${REQUIREMENTS_FILE}$" || true)
    
    if [ -n "$req_modified" ]; then
        print_warning "requirements.md has been directly modified in this branch"
        echo ""
        print_info "Requirements changes:"
        git diff "origin/${default_branch}...HEAD" -- "$REQUIREMENTS_FILE" | grep "^[+-]\s*-\s*\*\*\[" || echo "  (No requirement line changes detected)"
        echo ""
    else
        print_info "requirements.md has NOT been directly modified"
        echo ""
    fi
    
    # Check if requirements-changes.md exists in workspace
    if [ -f "$WORKSPACE_REQUIREMENTS" ]; then
        print_info "Found requirements-changes.md in workspace"
        echo ""
        
        # Count changes by type
        local added=$(grep -c "^- \*\*\[ADDED\]" "$WORKSPACE_REQUIREMENTS" 2>/dev/null || echo "0")
        local modified=$(grep -c "^- \*\*\[MODIFIED\]" "$WORKSPACE_REQUIREMENTS" 2>/dev/null || echo "0")
        local deleted=$(grep -c "^- \*\*\[DELETED\]" "$WORKSPACE_REQUIREMENTS" 2>/dev/null || echo "0")
        
        print_info "Requirements changes pending:"
        echo "  ${GREEN}+${NC} Added: $added"
        echo "  ${YELLOW}~${NC} Modified: $modified"
        echo "  ${RED}-${NC} Deleted: $deleted"
        echo ""
        
        local total=$((added + modified + deleted))
        if [ $total -gt 0 ]; then
            print_success "Total: $total requirement changes"
        else
            print_warning "No requirement changes detected"
        fi
    else
        print_info "No requirements-changes.md found in workspace"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return 0
}

# ============================================================================
# EXPORT ALL FUNCTIONS
# ============================================================================

# Export all functions
export -f validate_requirements
export -f get_next_id
export -f track_id_mapping
export -f preview_merge
export -f merge_requirements
export -f analyze_requirements_impact

debug_print "requirements-utils.sh loaded successfully"
