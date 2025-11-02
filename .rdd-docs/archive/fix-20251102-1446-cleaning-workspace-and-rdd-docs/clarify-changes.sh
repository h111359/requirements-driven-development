#!/bin/bash
# Script to manage the requirements clarification process
# Part of RDD (Requirements-Driven Development) framework

set -e  # Exit on error

WORKSPACE_DIR=".rdd-docs/workspace"
CURRENT_CHANGE_FILE="$WORKSPACE_DIR/.current-change"
CLARIFICATION_LOG="$WORKSPACE_DIR/clarification-log.jsonl"
BACKUP_DIR="$WORKSPACE_DIR/.backups"

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
  init                  Initialize workspace for clarification phase
  log-clarification     Log a clarification Q&A entry
  copy-taxonomy         Copy clarity-taxonomy.md to workspace
  backup                Create backup of workspace files before re-run
  restore               Restore workspace from latest backup
  get-current           Output current change information
  clear                 Clear workspace (for main branch)
  validate              Validate requirements-changes.md format
  help                  Show this help message

Examples:
  $(basename "$0") init
  $(basename "$0") log-clarification "Question text" "Answer text" "user"
  $(basename "$0") get-current
  $(basename "$0") backup
  $(basename "$0") restore

For log-clarification:
  Arguments: <question> <answer> [answeredBy] [sessionId]
  answeredBy defaults to "user"
  sessionId defaults to current timestamp
EOF
}

# Action: init - Initialize workspace for clarification phase
action_init() {
    print_info "Initializing workspace for clarification phase..."
    
    # Ensure workspace directory exists
    mkdir -p "$WORKSPACE_DIR"
    
    # Copy clarity-taxonomy.md if it doesn't exist
    if [ ! -f "$WORKSPACE_DIR/clarity-taxonomy.md" ]; then
        if [ -f ".rdd-docs/clarity-taxonomy.md" ]; then
            cp ".rdd-docs/clarity-taxonomy.md" "$WORKSPACE_DIR/clarity-taxonomy.md"
            print_success "Copied clarity-taxonomy.md to workspace"
        else
            print_warning "clarity-taxonomy.md not found in .rdd-docs/"
        fi
    fi
    
    # Create open-questions.md if it doesn't exist
    if [ ! -f "$WORKSPACE_DIR/open-questions.md" ]; then
        cat > "$WORKSPACE_DIR/open-questions.md" << 'EOFQ'
# Open Questions - Requirements Clarification

> This file tracks open questions and clarifications needed for the current change.
> Questions are inspired by the clarity-taxonomy.md but can include any critical questions for execution.

## Status Legend
- [ ] Open / Not answered
- [?] Partially answered / Needs more detail
- [x] Answered / Resolved

---

## Questions

<!-- Add questions below. Use the taxonomy as inspiration but feel free to add custom questions -->

EOFQ
        print_success "Created open-questions.md template"
    fi
    
    # Create requirements-changes.md if it doesn't exist
    if [ ! -f "$WORKSPACE_DIR/requirements-changes.md" ]; then
        cat > "$WORKSPACE_DIR/requirements-changes.md" << 'EOFREQ'
# Requirements Changes

> This file documents changes to be made to the main requirements.md file.
> Each statement is prefixed with [ADDED|MODIFIED|DELETED] to indicate the type of change.

## Format Guidelines

- **[ADDED]**: New requirement not present in current requirements.md
  - **Format**: `[ADDED] Title: Description` (NO ID - will be auto-assigned during wrap-up)
  - IDs are auto-assigned from highest existing ID per section during wrap-up
  - Example: `- **[ADDED] User Authentication**: System shall require OAuth2 login`
  - **Do NOT specify IDs for ADDED requirements** - prevents conflicts with parallel development

- **[MODIFIED]**: Change to an existing requirement from requirements.md
  - **Format**: `[MODIFIED] [EXISTING-ID] Title: New description`
  - MUST include the existing requirement ID from requirements.md (e.g., [FR-05])
  - Example: `- **[MODIFIED] [FR-05] Data Export**: Change from "CSV only" to "CSV, JSON, and XML formats"`

- **[DELETED]**: Requirement to be removed from requirements.md
  - **Format**: `[DELETED] [EXISTING-ID] Title: Reason for deletion`
  - MUST include the existing requirement ID from requirements.md
  - Example: `- **[DELETED] [NFR-03] Legacy Support**: No longer needed after v2.0 migration`

**Important**: During wrap-up, an ID mapping file (.id-mapping.txt) will be created documenting final assigned IDs

---

## General Functionalities

<!-- Add general functionality changes here -->

---

## Functional Requirements

<!-- Add functional requirement changes here -->

---

## Non-Functional Requirements

<!-- Add non-functional requirement changes here -->

---

## Technical Requirements

<!-- Add technical requirement changes here -->

EOFREQ
        print_success "Created requirements-changes.md template"
    fi
    
    # Initialize clarification log if it doesn't exist
    if [ ! -f "$CLARIFICATION_LOG" ]; then
        touch "$CLARIFICATION_LOG"
        print_success "Initialized clarification log"
    fi
    
    # Update phase in .current-change if it exists
    if [ -f "$CURRENT_CHANGE_FILE" ]; then
        # Use jq to update the phase field
        if command -v jq &> /dev/null; then
            tmp=$(mktemp)
            jq '.phase = "clarify"' "$CURRENT_CHANGE_FILE" > "$tmp"
            mv "$tmp" "$CURRENT_CHANGE_FILE"
            print_success "Updated phase to 'clarify' in .current-change"
        fi
    fi
    
    print_success "Workspace initialized for clarification phase"
}

# Action: log-clarification - Log a Q&A entry
action_log_clarification() {
    local question="$1"
    local answer="$2"
    local answered_by="${3:-user}"
    local session_id="${4:-clarify-$(date +%Y%m%d-%H%M)}"
    
    if [ -z "$question" ] || [ -z "$answer" ]; then
        print_error "Question and answer are required"
        echo "Usage: $(basename "$0") log-clarification \"<question>\" \"<answer>\" [answeredBy] [sessionId]"
        exit 1
    fi
    
    # Ensure log file exists
    mkdir -p "$WORKSPACE_DIR"
    touch "$CLARIFICATION_LOG"
    
    # Escape special characters for JSON
    question_escaped=$(echo "$question" | sed 's/"/\\"/g' | sed "s/'/\\'/g")
    answer_escaped=$(echo "$answer" | sed 's/"/\\"/g' | sed "s/'/\\'/g")
    
    # Create JSON line
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    echo "{\"timestamp\":\"$timestamp\",\"question\":\"$question_escaped\",\"answer\":\"$answer_escaped\",\"answeredBy\":\"$answered_by\",\"sessionId\":\"$session_id\"}" >> "$CLARIFICATION_LOG"
    
    print_success "Logged clarification entry"
}

# Action: copy-taxonomy - Copy clarity taxonomy to workspace
action_copy_taxonomy() {
    if [ ! -f ".rdd-docs/clarity-taxonomy.md" ]; then
        print_error "clarity-taxonomy.md not found in .rdd-docs/"
        exit 1
    fi
    
    mkdir -p "$WORKSPACE_DIR"
    cp ".rdd-docs/clarity-taxonomy.md" "$WORKSPACE_DIR/clarity-taxonomy.md"
    print_success "Copied clarity-taxonomy.md to workspace"
}

# Action: backup - Create backup of workspace files
action_backup() {
    print_info "Creating backup of workspace files..."
    
    # Create backup directory with timestamp
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local backup_path="$BACKUP_DIR/$timestamp"
    mkdir -p "$backup_path"
    
    # Backup key files
    local files_to_backup=("change.md" "open-questions.md" "requirements-changes.md" "clarification-log.jsonl" "clarity-taxonomy.md")
    
    for file in "${files_to_backup[@]}"; do
        if [ -f "$WORKSPACE_DIR/$file" ]; then
            cp "$WORKSPACE_DIR/$file" "$backup_path/$file"
            print_success "Backed up $file"
        fi
    done
    
    print_success "Backup created at $backup_path"
    echo "$backup_path"
}

# Action: restore - Restore from latest backup
action_restore() {
    if [ ! -d "$BACKUP_DIR" ] || [ -z "$(ls -A "$BACKUP_DIR")" ]; then
        print_error "No backups found"
        exit 1
    fi
    
    # Get latest backup directory
    local latest_backup=$(ls -t "$BACKUP_DIR" | head -n 1)
    local backup_path="$BACKUP_DIR/$latest_backup"
    
    print_info "Restoring from backup: $latest_backup"
    
    # Restore files
    for file in "$backup_path"/*; do
        if [ -f "$file" ]; then
            local filename=$(basename "$file")
            cp "$file" "$WORKSPACE_DIR/$filename"
            print_success "Restored $filename"
        fi
    done
    
    print_success "Workspace restored from backup"
}

# Action: get-current - Output current change information
action_get_current() {
    if [ ! -f "$CURRENT_CHANGE_FILE" ]; then
        print_error "No current change found (.current-change file missing)"
        exit 1
    fi
    
    if command -v jq &> /dev/null; then
        cat "$CURRENT_CHANGE_FILE" | jq .
    else
        cat "$CURRENT_CHANGE_FILE"
    fi
}

# Action: clear - Clear workspace for main branch
action_clear() {
    print_warning "This will clear the workspace. Are you sure? (y/N)"
    read -r response
    
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        print_info "Operation cancelled"
        exit 0
    fi
    
    print_info "Clearing workspace..."
    
    # Remove workspace files but keep directory structure
    local files_to_remove=("change.md" "open-questions.md" "requirements-changes.md" "clarification-log.jsonl" "clarity-taxonomy.md" ".current-change")
    
    for file in "${files_to_remove[@]}"; do
        if [ -f "$WORKSPACE_DIR/$file" ]; then
            rm "$WORKSPACE_DIR/$file"
            print_success "Removed $file"
        fi
    done
    
    # Keep backups but inform user
    if [ -d "$BACKUP_DIR" ]; then
        print_info "Backups preserved in $BACKUP_DIR"
    fi
    
    print_success "Workspace cleared"
}

# Action: validate - Validate requirements-changes.md format
action_validate() {
    local req_file="$WORKSPACE_DIR/requirements-changes.md"
    
    if [ ! -f "$req_file" ]; then
        print_error "requirements-changes.md not found in workspace"
        exit 1
    fi
    
    print_info "Validating requirements-changes.md format..."
    
    # Check for proper prefixes
    local has_errors=0
    local line_num=0
    
    while IFS= read -r line; do
        ((line_num++))
        # Skip empty lines, comments, and markdown headers
        if [[ -z "$line" ]] || [[ "$line" =~ ^#.* ]] || [[ "$line" =~ ^[[:space:]]*$ ]] || [[ "$line" =~ ^\>.* ]] || [[ "$line" =~ ^--.* ]]; then
            continue
        fi
        
        # Check if line starts with a list marker (- or *)
        if [[ "$line" =~ ^[[:space:]]*[-\*][[:space:]].* ]]; then
            # Extract the content after the list marker
            local content=$(echo "$line" | sed 's/^[[:space:]]*[-*][[:space:]]*//')
            
            # Check if it starts with a valid prefix
            if [[ ! "$content" =~ ^\[ADDED\].*$ ]] && [[ ! "$content" =~ ^\[MODIFIED\].*$ ]] && [[ ! "$content" =~ ^\[DELETED\].*$ ]]; then
                print_warning "Line $line_num: Missing or invalid prefix [ADDED|MODIFIED|DELETED]"
                echo "  → $line"
                has_errors=1
            fi
        fi
    done < "$req_file"
    
    if [ $has_errors -eq 0 ]; then
        print_success "Validation passed: requirements-changes.md format is correct"
    else
        print_warning "Validation completed with warnings. Please review the format."
        exit 1
    fi
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
        init)
            action_init
            ;;
        log-clarification)
            action_log_clarification "$@"
            ;;
        copy-taxonomy)
            action_copy_taxonomy
            ;;
        backup)
            action_backup
            ;;
        restore)
            action_restore
            ;;
        get-current)
            action_get_current
            ;;
        clear)
            action_clear
            ;;
        validate)
            action_validate
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
