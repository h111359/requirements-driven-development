#!/bin/bash

# fix-management.sh
# Script to manage fix branches in the RDD framework
# Usage: ./fix-management.sh <action> [parameters]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
WORKSPACE_DIR="$REPO_ROOT/.rdd-docs/workspace"
TEMPLATE_DIR="$REPO_ROOT/.rdd/templates"
CHANGE_TEMPLATE="$TEMPLATE_DIR/copilot-prompts.md"
ARCHIVE_DIR="$REPO_ROOT/.rdd-docs/archive"

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

# Function to check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        print_error "Not a git repository. Please run this from within a git repository."
        exit 1
    fi
}

# Function to validate fix name (kebab-case)
validate_fix_name() {
    local name="$1"
    
    if [[ ! "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
        print_error "Invalid fix name: '$name'"
        print_error "Must be kebab-case (lowercase, hyphens only, no spaces)"
        return 1
    fi
    
    # Count words (split by hyphen)
    local word_count=$(echo "$name" | tr '-' '\n' | wc -l)
    if [ "$word_count" -gt 5 ]; then
        print_error "Fix name too long: $word_count words (maximum 5)"
        return 1
    fi
    
    return 0
}

# Function to initialize fix branch and workspace
init_fix() {
    local fix_name="$1"
    
    if [ -z "$fix_name" ]; then
        print_error "Fix name is required"
        echo "Usage: $0 init <fix-name>"
        exit 1
    fi
    
    # Validate name
    if ! validate_fix_name "$fix_name"; then
        exit 1
    fi
    
    local branch_name="fix/$fix_name"
    
    # Check if branch already exists
    if git show-ref --verify --quiet "refs/heads/$branch_name"; then
        print_error "Branch '$branch_name' already exists"
        exit 1
    fi
    
    # Create workspace directory if it doesn't exist
    mkdir -p "$WORKSPACE_DIR"
    print_success "Workspace directory ready: $WORKSPACE_DIR"
    
    # Copy copilot-prompts.md template
    if [ ! -f "$CHANGE_TEMPLATE" ]; then
        print_error "Template not found: $CHANGE_TEMPLATE"
        exit 1
    fi
    
    cp "$CHANGE_TEMPLATE" "$WORKSPACE_DIR/.rdd.copilot-prompts.md"
    print_success "Template copied to workspace"
    
    # Create and checkout new branch
    git checkout -b "$branch_name"
    print_success "Created and checked out branch: $branch_name"
    
    echo ""
    print_success "Fix branch initialized successfully!"
}

# Function to archive the workspace for a fix branch
archive_fix_workspace() {
    local branch_name="$1"

    if [ ! -d "$WORKSPACE_DIR" ]; then
        print_error "Workspace directory not found at $WORKSPACE_DIR"
        return 1
    fi

    if [ -z "$(ls -A "$WORKSPACE_DIR")" ]; then
        print_error "Workspace directory is empty - document the fix before wrapping up"
        return 1
    fi

    local fix_name="${branch_name#fix/}"
    if [ -z "$fix_name" ]; then
        fix_name="unnamed-fix"
    fi

    local timestamp=$(date -u +%Y%m%d-%H%M%SZ)
    local archive_root="$ARCHIVE_DIR/fixes"
    mkdir -p "$archive_root"

    local archive_dir_name="${timestamp}-${fix_name}"
    local archive_path="$archive_root/$archive_dir_name"
    mkdir -p "$archive_path"

    # Copy workspace contents
    cp -R "$WORKSPACE_DIR"/. "$archive_path"/
    
    # Remove any config files from archive (they're branch-specific)
    rm -f "$archive_path"/.rdd.fix.* "$archive_path"/.rdd.enh.*

    cat > "$archive_path/.archive-info" << EOF
{
  "archivedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "branch": "$branch_name",
  "fixName": "$fix_name",
  "type": "fix"
}
EOF

    local relative_path="$archive_path"
    if [[ "$archive_path" == "$REPO_ROOT"* ]]; then
        relative_path="${archive_path#$REPO_ROOT/}"
    fi

    echo "$relative_path"
}

# Function to create a wrap-up commit for the fix
create_wrap_up_commit() {
    local branch_name="$1"
    local fix_name="${branch_name#fix/}"
    local commit_message="fix: ${fix_name} wrap-up"

    git add -A
    if git diff --cached --quiet; then
        print_warning "No changes staged for commit - skipping commit creation"
        return 2
    fi

    if git commit -m "$commit_message"; then
        print_success "Created commit: $commit_message"
        return 0
    else
        print_error "Failed to create wrap-up commit"
        return 1
    fi
}

# Function to create a pull request for the fix branch
create_fix_pull_request() {
    local branch_name="$1"
    local archive_path="$2"
    local fix_name="${branch_name#fix/}"

    if ! command -v gh >/dev/null 2>&1; then
        print_warning "GitHub CLI (gh) not found - create the pull request manually"
        echo "Suggested command: gh pr create --base main --head $branch_name --title \"fix: ${fix_name} wrap-up\" --body \"Wrap-up for $branch_name. Archive: $archive_path\""
        return 1
    fi

    if gh pr view "$branch_name" >/dev/null 2>&1; then
        print_warning "Pull request already exists for $branch_name - skipping creation"
        return 0
    fi

    local pr_title="fix: ${fix_name} wrap-up"
    local pr_body_file=$(mktemp)

    cat > "$pr_body_file" << EOF
## Summary
- Wrap-up for fix branch \`$branch_name\`
- Workspace archived at \`$archive_path\`

## Testing
- Manual validation (fix-specific)
EOF

    if gh pr create --base main --head "$branch_name" --title "$pr_title" --body-file "$pr_body_file"; then
        print_success "Pull request created for $branch_name"
        rm -f "$pr_body_file"
        return 0
    else
        rm -f "$pr_body_file"
        print_error "Failed to create pull request via GitHub CLI"
        echo "Try manually: gh pr create --base main --head $branch_name --title \"$pr_title\" --body \"Wrap-up for $branch_name. Archive: $archive_path\""
        return 1
    fi
}

# Function to run the fix wrap-up flow
wrap_up_fix() {
    local current_branch=$(git branch --show-current)

    if [[ ! "$current_branch" =~ ^fix/ ]]; then
        print_error "Wrap-up can only be executed from a fix branch"
        exit 1
    fi

    print_info "Archiving workspace contents..."
    local archive_relative
    if ! archive_relative=$(archive_fix_workspace "$current_branch"); then
        print_error "Failed to archive workspace"
        exit 1
    fi
    print_success "Workspace archived to $archive_relative"

    print_info "Creating wrap-up commit..."
    local commit_status
    create_wrap_up_commit "$current_branch"
    commit_status=$?
    if [ $commit_status -eq 1 ]; then
        exit 1
    elif [ $commit_status -eq 2 ]; then
        print_warning "No changes detected - continuing without new commit"
    fi

    print_info "Pushing branch to remote..."
    push

    print_info "Creating pull request..."
    create_fix_pull_request "$current_branch" "$archive_relative"

    print_success "Fix wrap-up completed"
}

# Function to push branch to remote
push() {
    local current_branch=$(git branch --show-current)
    
    if [[ ! "$current_branch" =~ ^fix/.+ ]]; then
        print_error "Not on a fix branch (current: $current_branch)"
        exit 1
    fi
    
    print_info "Pushing branch to remote..."
    git push -u origin "$current_branch"
    print_success "Branch pushed to remote with upstream tracking"
}

# Function to cleanup (delete branch and workspace)
cleanup() {
    local current_branch=$(git branch --show-current)
    
    if [[ ! "$current_branch" =~ ^fix/.+ ]]; then
        print_error "Not on a fix branch (current: $current_branch)"
        exit 1
    fi
    
    print_warning "Cleaning up fix branch..."
    
    # Switch to main or master branch
    if git show-ref --verify --quiet refs/heads/main; then
        git checkout main
    elif git show-ref --verify --quiet refs/heads/master; then
        git checkout master
    else
        print_error "Cannot find main or master branch to switch to"
        exit 1
    fi
    
    # Delete the fix branch
    git branch -D "$current_branch"
    print_success "Deleted branch: $current_branch"
    
    # Remove workspace files if they exist
    if [ -d "$WORKSPACE_DIR" ]; then
        rm -rf "$WORKSPACE_DIR"
        print_success "Removed workspace directory"
    fi
}

# Function to mark a stand-alone prompt as completed
mark_prompt_completed() {
    local prompt_id="$1"
    local fix_journal="$WORKSPACE_DIR/.rdd.copilot-prompts.md"
    
    if [ -z "$prompt_id" ]; then
        print_error "Prompt ID is required"
        echo "Usage: $0 mark-prompt-completed <prompt-id>"
        exit 1
    fi
    
    if [ ! -f "$fix_journal" ]; then
        print_error ".rdd.copilot-prompts.md not found at: $fix_journal"
        exit 1
    fi
    
    # Check if the prompt exists and is not already completed
    if ! grep -q "^\s*-\s*\[\s*\]\s*\[$prompt_id\]" "$fix_journal"; then
        if grep -q "^\s*-\s*\[x\]\s*\[$prompt_id\]" "$fix_journal"; then
            print_warning "Prompt $prompt_id is already marked as completed"
            return 0
        else
            print_error "Prompt $prompt_id not found in .rdd.copilot-prompts.md"
            exit 1
        fi
    fi
    
    # Mark the prompt as completed using sed
    # This will change "- [ ] [PROMPT_ID]" to "- [x] [PROMPT_ID]"
    # Handle various spacing variations
    if sed -i "s/^\(\s*-\s*\)\[\s*\]\(\s*\[\s*$prompt_id\s*\]\)/\1[x]\2/" "$fix_journal"; then
        print_success "Marked prompt $prompt_id as completed"
    else
        print_error "Failed to mark prompt $prompt_id as completed"
        exit 1
    fi
}

# Function to log prompt execution details to log.jsonl
# This function creates a structured log entry containing:
# - timestamp: ISO 8601 format timestamp when the log entry was created
# - promptId: The ID of the executed prompt (e.g., P001, P002)
# - executionDetails: The full content of the execution including agent responses
# - sessionId: Optional session identifier for grouping related executions
log_prompt_execution() {
    local prompt_id="$1"
    local execution_details="$2"
    local session_id="${3:-exec-$(date +%Y%m%d-%H%M)}"
    local log_file="$WORKSPACE_DIR/log.jsonl"
    
    # Validate required parameters
    if [ -z "$prompt_id" ]; then
        print_error "Prompt ID is required for logging"
        echo "Usage: $0 log-prompt-execution <prompt-id> <execution-details> [session-id]"
        exit 1
    fi
    
    if [ -z "$execution_details" ]; then
        print_error "Execution details are required for logging"
        echo "Usage: $0 log-prompt-execution <prompt-id> <execution-details> [session-id]"
        exit 1
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
}

# Function to display usage
usage() {
    echo "Usage: $0 <action> [parameters]"
    echo ""
    echo "Actions:"
    echo "  init <fix-name>              - Initialize fix branch and workspace"
    echo "  wrap-up                      - Archive workspace, commit, push, and create PR"
    echo "  push                         - Push branch to remote"
    echo "  cleanup                      - Delete branch and workspace"
    echo "  mark-prompt-completed <id>   - Mark a stand-alone prompt as completed in .rdd.copilot-prompts.md"
    echo "  log-prompt-execution <id> \"<details>\" [session-id] - Log prompt execution details to log.jsonl"
    echo ""
    echo "Examples:"
    echo "  $0 init fix-login-button"
    echo "  $0 mark-prompt-completed P001"
    echo "  $0 log-prompt-execution P001 \"Execution details here\" \"session-123\""
    echo "  $0 push"
}

# Main script logic
main() {
    check_git_repo
    
    local action="$1"
    shift || true
    
    case "$action" in
        init)
            init_fix "$@"
            ;;
        push)
            push
            ;;
        wrap-up)
            wrap_up_fix
            ;;
        cleanup)
            cleanup
            ;;
        mark-prompt-completed)
            mark_prompt_completed "$@"
            ;;
        log-prompt-execution)
            log_prompt_execution "$@"
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
