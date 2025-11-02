#!/bin/bash

# pr-utils.sh
# Utility script for pull request management in the RDD framework
# Handles PR creation, updates, reviews, and workflow automation

# Prevent multiple sourcing
[[ -n "${PR_UTILS_SOURCED:-}" ]] && return
readonly PR_UTILS_SOURCED=1

# Source dependencies
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/core-utils.sh"
source "$SCRIPT_DIR/git-utils.sh"

# Get repository root
REPO_ROOT=$(get_repo_root)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GITHUB CLI AVAILABILITY CHECK
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Check if GitHub CLI is available
# Returns:
#   0 if gh is available and authenticated
#   1 if gh is not available
check_gh_cli() {
    if ! command -v gh >/dev/null 2>&1; then
        return 1
    fi
    
    # Check if authenticated (optional - may fail in some environments)
    if ! gh auth status >/dev/null 2>&1; then
        return 1
    fi
    
    return 0
}

# Export function
export -f check_gh_cli

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PULL REQUEST CREATION
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Create a pull request using GitHub CLI
# Arguments:
#   $1 - branch_name: The branch to create PR for
#   $2 - title: PR title
#   $3 - body: PR body/description
#   $4 - draft: Optional flag to create as draft (true/false, default: false)
# Returns:
#   0 on success
#   1 on error (gh not available, PR already exists, creation failed)
# Output:
#   Success message with PR URL or error message with manual command
create_pr() {
    local branch_name="$1"
    local title="$2"
    local body="$3"
    local draft="${4:-false}"
    
    # Validate required parameters
    if [ -z "$branch_name" ]; then
        print_error "Branch name is required"
        echo "Usage: create_pr <branch-name> <title> <body> [draft]"
        return 1
    fi
    
    if [ -z "$title" ]; then
        print_error "PR title is required"
        echo "Usage: create_pr <branch-name> <title> <body> [draft]"
        return 1
    fi
    
    if [ -z "$body" ]; then
        print_error "PR body is required"
        echo "Usage: create_pr <branch-name> <title> <body> [draft]"
        return 1
    fi
    
    # Check if GitHub CLI is available
    if ! check_gh_cli; then
        print_warning "GitHub CLI (gh) not found or not authenticated - create the pull request manually"
        local base_branch=$(get_default_branch)
        echo "Suggested command: gh pr create --base $base_branch --head $branch_name --title \"$title\" --body \"$body\""
        return 1
    fi
    
    # Check if PR already exists for this branch
    if gh pr view "$branch_name" >/dev/null 2>&1; then
        print_warning "Pull request already exists for $branch_name - skipping creation"
        gh pr view "$branch_name" --web 2>/dev/null || true
        return 0
    fi
    
    # Create temporary file for PR body
    local pr_body_file=$(mktemp)
    echo "$body" > "$pr_body_file"
    
    # Get base branch (main or master)
    local base_branch=$(get_default_branch)
    
    # Build gh pr create command
    local gh_command="gh pr create --base $base_branch --head $branch_name --title \"$title\" --body-file \"$pr_body_file\""
    
    # Add draft flag if requested
    if [ "$draft" = "true" ]; then
        gh_command="$gh_command --draft"
    fi
    
    # Execute PR creation
    if eval "$gh_command"; then
        print_success "Pull request created for $branch_name"
        rm -f "$pr_body_file"
        return 0
    else
        rm -f "$pr_body_file"
        print_error "Failed to create pull request via GitHub CLI"
        echo "Try manually: gh pr create --base $base_branch --head $branch_name --title \"$title\" --body \"$body\""
        return 1
    fi
}

# Export function
export -f create_pr

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PULL REQUEST UPDATES
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Update an existing pull request
# Arguments:
#   $1 - pr_number: The PR number to update
#   $2 - updates: JSON-formatted string with updates (e.g., '{"title":"New Title","body":"New body"}')
# Returns:
#   0 on success
#   1 on error (gh not available, invalid PR number, update failed)
# Example:
#   update_pr 123 '{"title":"Updated title"}'
update_pr() {
    local pr_number="$1"
    local updates="$2"
    
    # Validate required parameters
    if [ -z "$pr_number" ]; then
        print_error "PR number is required"
        echo "Usage: update_pr <pr-number> <updates-json>"
        return 1
    fi
    
    if [ -z "$updates" ]; then
        print_error "Updates JSON is required"
        echo "Usage: update_pr <pr-number> <updates-json>"
        echo "Example: update_pr 123 '{\"title\":\"New Title\",\"body\":\"New body\"}'"
        return 1
    fi
    
    # Check if GitHub CLI is available
    if ! check_gh_cli; then
        print_warning "GitHub CLI (gh) not found or not authenticated"
        echo "Cannot update PR without GitHub CLI"
        return 1
    fi
    
    # Parse updates and build gh pr edit command
    local gh_command="gh pr edit $pr_number"
    
    # Extract title if present
    if echo "$updates" | grep -q '"title"'; then
        local title=$(echo "$updates" | grep -o '"title":"[^"]*"' | cut -d'"' -f4)
        if [ -n "$title" ]; then
            gh_command="$gh_command --title \"$title\""
        fi
    fi
    
    # Extract body if present
    if echo "$updates" | grep -q '"body"'; then
        local body=$(echo "$updates" | grep -o '"body":"[^"]*"' | cut -d'"' -f4)
        if [ -n "$body" ]; then
            gh_command="$gh_command --body \"$body\""
        fi
    fi
    
    # Execute PR update
    if eval "$gh_command"; then
        print_success "Pull request #$pr_number updated successfully"
        return 0
    else
        print_error "Failed to update pull request #$pr_number"
        return 1
    fi
}

# Export function
export -f update_pr

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PULL REQUEST REVIEWS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Request reviews for a pull request
# Arguments:
#   $1 - pr_number: The PR number to request reviews for
#   $2 - reviewers: Comma-separated list of GitHub usernames
# Returns:
#   0 on success
#   1 on error (gh not available, invalid parameters, request failed)
# Example:
#   request_review 123 "user1,user2,user3"
request_review() {
    local pr_number="$1"
    local reviewers="$2"
    
    # Validate required parameters
    if [ -z "$pr_number" ]; then
        print_error "PR number is required"
        echo "Usage: request_review <pr-number> <reviewers>"
        return 1
    fi
    
    if [ -z "$reviewers" ]; then
        print_error "Reviewers list is required"
        echo "Usage: request_review <pr-number> <reviewers>"
        echo "Example: request_review 123 \"user1,user2\""
        return 1
    fi
    
    # Check if GitHub CLI is available
    if ! check_gh_cli; then
        print_warning "GitHub CLI (gh) not found or not authenticated"
        echo "Cannot request reviews without GitHub CLI"
        return 1
    fi
    
    # Convert comma-separated list to space-separated for gh command
    local reviewer_list=$(echo "$reviewers" | tr ',' ' ')
    
    # Request reviews using gh pr edit
    if gh pr edit "$pr_number" --add-reviewer "$reviewer_list"; then
        print_success "Review requested from: $reviewers"
        return 0
    else
        print_error "Failed to request reviews for PR #$pr_number"
        return 1
    fi
}

# Export function
export -f request_review

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PULL REQUEST WORKFLOW AUTOMATION
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Automated PR workflow for change/fix wrap-up
# Creates a standardized PR with consistent format
# Arguments:
#   $1 - branch_name: The branch to create PR for (must be feat/* or fix/*)
#   $2 - archive_path: Path to archived workspace (relative to repo root)
# Returns:
#   0 on success
#   1 on error
# PR Format:
#   Title: "feat/fix: {name} wrap-up"
#   Body: Summary with branch name and archive location
pr_workflow() {
    local branch_name="$1"
    local archive_path="$2"
    
    # Validate required parameters
    if [ -z "$branch_name" ]; then
        print_error "Branch name is required"
        echo "Usage: pr_workflow <branch-name> <archive-path>"
        return 1
    fi
    
    if [ -z "$archive_path" ]; then
        print_error "Archive path is required"
        echo "Usage: pr_workflow <branch-name> <archive-path>"
        return 1
    fi
    
    # Validate branch name format (feat/* or fix/*)
    if [[ ! "$branch_name" =~ ^(feat|fix)/ ]]; then
        print_error "Invalid branch name: $branch_name"
        print_error "Branch must start with 'feat/' or 'fix/'"
        return 1
    fi
    
    # Extract branch type and name
    local branch_type="${branch_name%%/*}"
    local change_name="${branch_name#*/}"
    
    # Build PR title
    local pr_title="${branch_type}: ${change_name} wrap-up"
    
    # Build PR body
    local pr_body="## Summary
- Wrap-up for ${branch_type} branch \`$branch_name\`
- Workspace archived at \`$archive_path\`

## Testing
- Manual validation (${branch_type}-specific)

## Archive Location
\`\`\`
$archive_path
\`\`\`
"
    
    # Create the pull request
    print_info "Creating pull request for $branch_name..."
    if create_pr "$branch_name" "$pr_title" "$pr_body"; then
        print_success "PR workflow completed successfully"
        return 0
    else
        print_warning "PR workflow completed with warnings - check messages above"
        return 1
    fi
}

# Export function
export -f pr_workflow
