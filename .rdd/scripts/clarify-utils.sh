#!/bin/bash

# clarify-utils.sh
# Clarification management utility functions for RDD framework
# Provides initialization, logging, and template management for clarification phase

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source core-utils.sh for common functions
if [ -f "$SCRIPT_DIR/core-utils.sh" ]; then
    source "$SCRIPT_DIR/core-utils.sh"
else
    echo "ERROR: core-utils.sh not found. Please ensure it exists in the same directory."
    exit 1
fi

# Source workspace-utils.sh for workspace operations
if [ -f "$SCRIPT_DIR/workspace-utils.sh" ]; then
    source "$SCRIPT_DIR/workspace-utils.sh"
else
    echo "ERROR: workspace-utils.sh not found. Please ensure it exists in the same directory."
    exit 1
fi

# Prevent multiple sourcing
if [ -n "$CLARIFY_UTILS_LOADED" ]; then
    return 0
fi
CLARIFY_UTILS_LOADED=1

# ============================================================================
# CONSTANTS
# ============================================================================

WORKSPACE_DIR=".rdd-docs/workspace"
CLARIFICATION_LOG="$WORKSPACE_DIR/clarification-log.jsonl"
CLARITY_TAXONOMY_SOURCE=".rdd-docs/clarity-checklist.md"
CLARITY_TAXONOMY_WORKSPACE="$WORKSPACE_DIR/clarity-checklist.md"

# ============================================================================
# CLARIFICATION INITIALIZATION
# ============================================================================

# Initialize clarification phase in workspace
# Usage: init_clarification
# Returns: 0 on success, 1 on failure
init_clarification() {
    print_banner "INITIALIZE CLARIFICATION PHASE"
    echo ""
    
    # Ensure workspace directory exists
    ensure_dir "$WORKSPACE_DIR"
    
    # Copy clarity-checklist.md
    if ! copy_taxonomy; then
        print_warning "Failed to copy checklist, continuing anyway..."
    fi
    echo ""
    
    # Create open-questions.md template
    if ! create_open_questions_template; then
        print_error "Failed to create open-questions template"
        return 1
    fi
    echo ""
    
    # Initialize clarification-log.jsonl
    if [ ! -f "$CLARIFICATION_LOG" ]; then
        touch "$CLARIFICATION_LOG"
        print_success "Initialized clarification-log.jsonl"
        
        # Add initial system entry
        local timestamp=$(get_timestamp)
        echo "{\"timestamp\":\"$timestamp\",\"question\":\"Clarification phase started\",\"answer\":\"Workspace initialized for requirements clarification\",\"answeredBy\":\"system\",\"sessionId\":\"init-$(date +%Y%m%d-%H%M)\"}" >> "$CLARIFICATION_LOG"
    else
        print_info "clarification-log.jsonl already exists"
    fi
    echo ""
    
    # Update phase in .current-change if it exists
    local current_change_file="$WORKSPACE_DIR/.current-change"
    if [ -f "$current_change_file" ]; then
        if command -v jq &> /dev/null; then
            local tmp=$(mktemp)
            jq '.phase = "clarify"' "$current_change_file" > "$tmp"
            mv "$tmp" "$current_change_file"
            print_success "Updated phase to 'clarify' in .current-change"
        else
            debug_print "jq not available, skipping phase update"
        fi
    fi
    
    echo ""
    print_success "Clarification phase initialized successfully"
    echo ""
    print_info "Next steps:"
    echo "  1. Review clarity-checklist.md for question categories"
    echo "  2. Add questions to open-questions.md"
    echo "  3. Log clarifications using log_clarification()"
    
    return 0
}

# ============================================================================
# CLARIFICATION LOGGING
# ============================================================================

# Log a clarification Q&A entry to JSONL file
# Usage: log_clarification "question" "answer" [answered_by] [session_id]
# answered_by defaults to "user"
# session_id defaults to "clarify-YYYYMMDD-HHmm"
# Returns: 0 on success, 1 on failure
log_clarification() {
    local question="$1"
    local answer="$2"
    local answered_by="${3:-user}"
    local session_id="${4:-clarify-$(date +%Y%m%d-%H%M)}"
    
    if [ -z "$question" ] || [ -z "$answer" ]; then
        print_error "Question and answer are required"
        echo "Usage: log_clarification <question> <answer> [answered_by] [session_id]"
        return 1
    fi
    
    # Ensure workspace directory and log file exist
    ensure_dir "$WORKSPACE_DIR"
    touch "$CLARIFICATION_LOG"
    
    # Use jq for proper JSON escaping if available
    if command -v jq &> /dev/null; then
        local timestamp=$(get_timestamp)
        jq -n \
            --arg ts "$timestamp" \
            --arg q "$question" \
            --arg a "$answer" \
            --arg by "$answered_by" \
            --arg sid "$session_id" \
            '{timestamp: $ts, question: $q, answer: $a, answeredBy: $by, sessionId: $sid}' \
            >> "$CLARIFICATION_LOG"
    else
        # Fallback to manual escaping
        local question_escaped=$(echo "$question" | sed 's/"/\\"/g' | sed "s/'/\\'/g")
        local answer_escaped=$(echo "$answer" | sed 's/"/\\"/g' | sed "s/'/\\'/g")
        local timestamp=$(get_timestamp)
        
        echo "{\"timestamp\":\"$timestamp\",\"question\":\"$question_escaped\",\"answer\":\"$answer_escaped\",\"answeredBy\":\"$answered_by\",\"sessionId\":\"$session_id\"}" >> "$CLARIFICATION_LOG"
    fi
    
    print_success "Logged clarification entry"
    debug_print "Session: $session_id, Answered by: $answered_by"
    
    return 0
}

# ============================================================================
# TEMPLATE CREATION
# ============================================================================

# Create open-questions.md template in workspace
# Usage: create_open_questions_template
# Returns: 0 on success, 1 if already exists
create_open_questions_template() {
    local dest_file="$WORKSPACE_DIR/open-questions.md"
    
    if [ -f "$dest_file" ]; then
        print_info "open-questions.md already exists"
        return 0
    fi
    
    ensure_dir "$WORKSPACE_DIR"
    
    cat > "$dest_file" << 'EOFQ'
# Open Questions - Requirements Clarification

> This file tracks open questions and clarifications needed for the current change.
> Questions are inspired by the clarity-checklist.md but can include any critical questions for execution.

## Status Legend
- [ ] Open / Not answered
- [?] Partially answered / Needs more detail
- [x] Answered / Resolved

---

## Questions

<!-- Add questions below. Use the taxonomy as inspiration but feel free to add custom questions -->

EOFQ
    
    print_success "Created open-questions.md template"
    return 0
}

# ============================================================================
# TAXONOMY MANAGEMENT
# ============================================================================

# Copy clarity-checklist.md from .rdd-docs to workspace
# Usage: copy_taxonomy
# Returns: 0 on success, 1 on failure
copy_taxonomy() {
    if [ ! -f "$CLARITY_TAXONOMY_SOURCE" ]; then
        print_error "clarity-checklist.md not found: $CLARITY_TAXONOMY_SOURCE"
        print_info "Please ensure the taxonomy file exists in .rdd-docs/"
        return 1
    fi
    
    ensure_dir "$WORKSPACE_DIR"
    
    # Check if already exists
    if [ -f "$CLARITY_TAXONOMY_WORKSPACE" ]; then
        print_warning "clarity-checklist.md already exists in workspace"
        if ! confirm_action "Overwrite existing taxonomy?"; then
            print_info "Copy cancelled"
            return 0
        fi
    fi
    
    cp "$CLARITY_TAXONOMY_SOURCE" "$CLARITY_TAXONOMY_WORKSPACE"
    print_success "Copied clarity-checklist.md to workspace"
    
    return 0
}

# ============================================================================
# CLARIFICATION INSPECTION
# ============================================================================

# Display clarification log entries
# Usage: show_clarifications [session_id]
# If session_id provided, filters by that session
# Returns: 0 on success
show_clarifications() {
    local session_id="$1"
    
    if [ ! -f "$CLARIFICATION_LOG" ]; then
        print_warning "No clarification log found"
        return 0
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  CLARIFICATION LOG"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    if command -v jq &> /dev/null; then
        # Use jq for pretty display
        if [ -n "$session_id" ]; then
            print_info "Filtering by session: $session_id"
            echo ""
            jq -r --arg sid "$session_id" 'select(.sessionId == $sid) | 
                "[\(.timestamp)] \(.answeredBy)\n  Q: \(.question)\n  A: \(.answer)\n"' \
                "$CLARIFICATION_LOG"
        else
            jq -r '. | 
                "[\(.timestamp)] \(.answeredBy)\n  Q: \(.question)\n  A: \(.answer)\n"' \
                "$CLARIFICATION_LOG"
        fi
    else
        # Fallback: raw display
        if [ -n "$session_id" ]; then
            print_info "Filtering by session: $session_id"
            echo ""
            grep "\"sessionId\":\"$session_id\"" "$CLARIFICATION_LOG" || echo "No entries found"
        else
            cat "$CLARIFICATION_LOG"
        fi
    fi
    
    echo ""
    local entry_count=$(wc -l < "$CLARIFICATION_LOG")
    print_info "Total entries: $entry_count"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return 0
}

# Count clarification entries
# Usage: count_clarifications [session_id]
# Returns: count on stdout
count_clarifications() {
    local session_id="$1"
    
    if [ ! -f "$CLARIFICATION_LOG" ]; then
        echo "0"
        return 0
    fi
    
    if [ -n "$session_id" ]; then
        grep -c "\"sessionId\":\"$session_id\"" "$CLARIFICATION_LOG" 2>/dev/null || echo "0"
    else
        wc -l < "$CLARIFICATION_LOG"
    fi
}

# Get clarification status summary
# Usage: get_clarification_status
# Returns: 0 on success
get_clarification_status() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  CLARIFICATION STATUS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Check if clarification log exists
    if [ -f "$CLARIFICATION_LOG" ]; then
        local entry_count=$(count_clarifications)
        print_success "Clarification log exists"
        print_info "Total entries: $entry_count"
    else
        print_warning "Clarification log not found"
    fi
    echo ""
    
    # Check if open-questions.md exists
    if [ -f "$WORKSPACE_DIR/open-questions.md" ]; then
        print_success "open-questions.md exists"
        
        # Count question statuses
        local open_count=$(grep -c "^- \[ \]" "$WORKSPACE_DIR/open-questions.md" 2>/dev/null || echo "0")
        local partial_count=$(grep -c "^- \[?\]" "$WORKSPACE_DIR/open-questions.md" 2>/dev/null || echo "0")
        local answered_count=$(grep -c "^- \[x\]" "$WORKSPACE_DIR/open-questions.md" 2>/dev/null || echo "0")
        
        print_info "Questions status:"
        echo "  [ ] Open: $open_count"
        echo "  [?] Partial: $partial_count"
        echo "  [x] Answered: $answered_count"
    else
        print_warning "open-questions.md not found"
    fi
    echo ""
    
    # Check if taxonomy exists
    if [ -f "$CLARITY_TAXONOMY_WORKSPACE" ]; then
        print_success "clarity-checklist.md available in workspace"
    else
        print_warning "clarity-checklist.md not found in workspace"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return 0
}

# ============================================================================
# EXPORT ALL FUNCTIONS
# ============================================================================

# Export all functions
export -f init_clarification
export -f log_clarification
export -f create_open_questions_template
export -f copy_taxonomy
export -f show_clarifications
export -f count_clarifications
export -f get_clarification_status

debug_print "clarify-utils.sh loaded successfully"
