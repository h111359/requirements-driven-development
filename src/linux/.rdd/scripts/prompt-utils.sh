#!/bin/bash

# prompt-utils.sh
# Utility script for prompt management in the RDD framework
# Handles marking prompts as completed and logging execution details

# Prevent multiple sourcing
[[ -n "${PROMPT_UTILS_SOURCED:-}" ]] && return
readonly PROMPT_UTILS_SOURCED=1

# Source dependencies
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/core-utils.sh"

# Get repository root and workspace directory
REPO_ROOT=$(get_repo_root)
WORKSPACE_DIR="$REPO_ROOT/.rdd-docs/workspace"

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROMPT COMPLETION FUNCTIONS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Mark a stand-alone prompt as completed in .rdd.copilot-prompts.md
# Changes checkbox from "- [ ]" to "- [x]" using sed
# Arguments:
#   $1 - prompt_id: The ID of the prompt (e.g., P001, P002)
#   $2 - journal_file: Path to .rdd.copilot-prompts.md (optional, defaults to workspace .rdd.copilot-prompts.md)
# Returns:
#   0 on success
#   1 on error (missing prompt ID, file not found, prompt not found)
mark_prompt_completed() {
    local prompt_id="$1"
    local journal_file="${2:-$WORKSPACE_DIR/.rdd.copilot-prompts.md}"
    
    # Validate prompt ID is provided
    if [ -z "$prompt_id" ]; then
        print_error "Prompt ID is required"
        echo "Usage: mark_prompt_completed <prompt-id> [journal-file]"
        return 1
    fi
    
    # Check if journal file exists
    if [ ! -f "$journal_file" ]; then
        print_error ".rdd.copilot-prompts.md not found at: $journal_file"
        return 1
    fi
    
    # Check if the prompt exists and is not already completed
    if ! grep -q "^\s*-\s*\[\s*\]\s*\[$prompt_id\]" "$journal_file"; then
        if grep -q "^\s*-\s*\[x\]\s*\[$prompt_id\]" "$journal_file"; then
            print_warning "Prompt $prompt_id is already marked as completed"
            return 0
        else
            print_error "Prompt $prompt_id not found in .rdd.copilot-prompts.md"
            return 1
        fi
    fi
    
    # Mark the prompt as completed using sed
    # This will change "- [ ] [PROMPT_ID]" to "- [x] [PROMPT_ID]"
    # Handle various spacing variations
    if sed -i "s/^\(\s*-\s*\)\[\s*\]\(\s*\[\s*$prompt_id\s*\]\)/\1[x]\2/" "$journal_file"; then
        print_success "Marked prompt $prompt_id as completed"
        return 0
    else
        print_error "Failed to mark prompt $prompt_id as completed"
        return 1
    fi
}

# Export function
export -f mark_prompt_completed

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROMPT EXECUTION LOGGING
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Log prompt execution details to log.jsonl
# Creates a structured JSONL entry with timestamp, promptId, executionDetails, sessionId
# Arguments:
#   $1 - prompt_id: The ID of the executed prompt (e.g., P001, P002)
#   $2 - execution_details: Full content describing what was executed
#   $3 - session_id: Optional session identifier (defaults to exec-YYYYMMDD-HHmm)
# Returns:
#   0 on success
#   1 on error (missing required parameters)
# Format:
#   {"timestamp":"2025-11-02T10:30:00Z","promptId":"P001","executionDetails":"...","sessionId":"exec-20251102-1030"}
log_prompt_execution() {
    local prompt_id="$1"
    local execution_details="$2"
    local session_id="${3:-exec-$(date +%Y%m%d-%H%M)}"
    local log_file="$WORKSPACE_DIR/log.jsonl"
    
    # Validate required parameters
    if [ -z "$prompt_id" ]; then
        print_error "Prompt ID is required for logging"
        echo "Usage: log_prompt_execution <prompt-id> <execution-details> [session-id]"
        return 1
    fi
    
    if [ -z "$execution_details" ]; then
        print_error "Execution details are required for logging"
        echo "Usage: log_prompt_execution <prompt-id> <execution-details> [session-id]"
        return 1
    fi
    
    # Ensure workspace directory exists
    mkdir -p "$WORKSPACE_DIR"
    
    # Create log file if it doesn't exist
    if [ ! -f "$log_file" ]; then
        touch "$log_file"
        print_success "Created log file: $log_file"
    fi
    
    # Robustly escape execution_details for JSON using jq if available.
    # If jq is not available, fallback to basic escaping (double quotes and newlines only).
    # WARNING: The fallback does NOT handle all JSON edge cases (e.g., backslashes, tabs, carriage returns, control characters).
    if command -v jq >/dev/null 2>&1; then
        # Use jq to encode as a JSON string, then strip the surrounding quotes
        details_escaped=$(jq -R <<<"$execution_details")
        # Remove the surrounding quotes for embedding in the larger JSON object
        details_escaped="${details_escaped:1:-1}"
    else
        # Fallback: basic escaping (limited, see warning above)
        details_escaped=$(echo "$execution_details" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g; s/\r/\\r/g' | awk '{printf "%s\\n", $0}' | sed 's/\\n$//')
    fi
    
    # Create JSON line entry with all relevant information
    # Format: JSONL (JSON Lines) - one JSON object per line
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    echo "{\"timestamp\":\"$timestamp\",\"promptId\":\"$prompt_id\",\"executionDetails\":\"$details_escaped\",\"sessionId\":\"$session_id\"}" >> "$log_file"
    
    print_success "Logged execution details for prompt $prompt_id to $log_file"
    return 0
}

# Export function
export -f log_prompt_execution

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROMPT LISTING AND FILTERING
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# List prompts from .rdd.copilot-prompts.md filtered by status
# Arguments:
#   $1 - status: Filter by status ('unchecked', 'checked', 'all')
#   $2 - journal_file: Path to .rdd.copilot-prompts.md (optional, defaults to workspace .rdd.copilot-prompts.md)
# Returns:
#   0 on success
#   1 on error (invalid status, file not found)
# Output:
#   Lists prompt IDs and titles matching the filter
list_prompts() {
    local status="${1:-all}"
    local journal_file="${2:-$WORKSPACE_DIR/.rdd.copilot-prompts.md}"
    
    # Validate status parameter
    if [[ ! "$status" =~ ^(unchecked|checked|all)$ ]]; then
        print_error "Invalid status filter: '$status'"
        echo "Valid options: unchecked, checked, all"
        return 1
    fi
    
    # Check if journal file exists
    if [ ! -f "$journal_file" ]; then
        print_error ".rdd.copilot-prompts.md not found at: $journal_file"
        return 1
    fi
    
    # Print header
    print_banner "PROMPTS LIST ($status)"
    
    # Filter and display based on status
    case "$status" in
        unchecked)
            grep "^\s*-\s*\[\s*\]\s*\[P[0-9]\+\]" "$journal_file" | while IFS= read -r line; do
                # Extract prompt ID and title
                prompt_id=$(echo "$line" | sed -n 's/.*\[\(P[0-9]\+\)\].*/\1/p')
                prompt_title=$(echo "$line" | sed 's/.*\[P[0-9]\+\]\s*\(.*\)/\1/' | cut -c1-80)
                echo "  ☐ [$prompt_id] $prompt_title"
            done
            ;;
        checked)
            grep "^\s*-\s*\[x\]\s*\[P[0-9]\+\]" "$journal_file" | while IFS= read -r line; do
                prompt_id=$(echo "$line" | sed -n 's/.*\[\(P[0-9]\+\)\].*/\1/p')
                prompt_title=$(echo "$line" | sed 's/.*\[P[0-9]\+\]\s*\(.*\)/\1/' | cut -c1-80)
                echo "  ☑ [$prompt_id] $prompt_title"
            done
            ;;
        all)
            grep "^\s*-\s*\[[x ]\]\s*\[P[0-9]\+\]" "$journal_file" | while IFS= read -r line; do
                prompt_id=$(echo "$line" | sed -n 's/.*\[\(P[0-9]\+\)\].*/\1/p')
                prompt_title=$(echo "$line" | sed 's/.*\[P[0-9]\+\]\s*\(.*\)/\1/' | cut -c1-80)
                if echo "$line" | grep -q "\[x\]"; then
                    echo "  ☑ [$prompt_id] $prompt_title"
                else
                    echo "  ☐ [$prompt_id] $prompt_title"
                fi
            done
            ;;
    esac
    
    # Print summary
    local total_count=$(grep -c "^\s*-\s*\[[x ]\]\s*\[P[0-9]\+\]" "$journal_file" 2>/dev/null || echo "0")
    local checked_count=$(grep -c "^\s*-\s*\[x\]\s*\[P[0-9]\+\]" "$journal_file" 2>/dev/null || echo "0")
    local unchecked_count=$((total_count - checked_count))
    
    echo ""
    print_info "Summary: $checked_count completed, $unchecked_count pending, $total_count total"
    
    return 0
}

# Export function
export -f list_prompts

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROMPT VALIDATION
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Validate prompt status in copilot-prompts.md
# Checks if a prompt exists and returns its status
# Arguments:
#   $1 - prompt_id: The ID of the prompt to check (e.g., P001)
#   $2 - journal_file: Path to copilot-prompts.md (optional, defaults to workspace copilot-prompts.md)
# Returns:
#   0 if prompt exists and is unchecked
#   1 if prompt exists and is checked
#   2 if prompt does not exist
#   3 if journal file not found
# Output:
#   Prints prompt status message
validate_prompt_status() {
    local prompt_id="$1"
    local journal_file="${2:-$WORKSPACE_DIR/.rdd.copilot-prompts.md}"
    
    # Validate prompt ID is provided
    if [ -z "$prompt_id" ]; then
        print_error "Prompt ID is required"
        echo "Usage: validate_prompt_status <prompt-id> [journal-file]"
        return 3
    fi
    
    # Check if journal file exists
    if [ ! -f "$journal_file" ]; then
        print_error "copilot-prompts.md not found at: $journal_file"
        return 3
    fi
    
    # Check if prompt exists and get its status
    if grep -q "^\s*-\s*\[\s*\]\s*\[$prompt_id\]" "$journal_file"; then
        print_info "Prompt $prompt_id exists and is unchecked (pending)"
        return 0
    elif grep -q "^\s*-\s*\[x\]\s*\[$prompt_id\]" "$journal_file"; then
        print_info "Prompt $prompt_id exists and is checked (completed)"
        return 1
    else
        print_warning "Prompt $prompt_id not found in copilot-prompts.md"
        return 2
    fi
}

# Export function
export -f validate_prompt_status
