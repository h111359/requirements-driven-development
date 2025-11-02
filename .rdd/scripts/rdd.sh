#!/bin/bash

# rdd.sh
# Main wrapper script for RDD framework
# Provides domain-based routing to all utility scripts

# Version information
RDD_VERSION="1.0.0"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source all utility scripts
source "$SCRIPT_DIR/core-utils.sh"
source "$SCRIPT_DIR/git-utils.sh"
source "$SCRIPT_DIR/workspace-utils.sh"
source "$SCRIPT_DIR/branch-utils.sh"
source "$SCRIPT_DIR/requirements-utils.sh"
source "$SCRIPT_DIR/clarify-utils.sh"
source "$SCRIPT_DIR/prompt-utils.sh"
source "$SCRIPT_DIR/pr-utils.sh"
source "$SCRIPT_DIR/change-utils.sh"

# ============================================================================
# HELP SYSTEM
# ============================================================================

show_version() {
    echo "RDD Framework v${RDD_VERSION}"
}

show_main_help() {
    print_banner "RDD Framework - Requirements-Driven Development"
    echo ""
    echo "Usage: rdd.sh <domain> <action> [options]"
    echo ""
    echo "Domains:"
    echo "  branch        Branch management operations"
    echo "  workspace     Workspace initialization and management"
    echo "  requirements  Requirements validation and merging"
    echo "  change        Change workflow management"
    echo "  fix           Fix workflow management"
    echo "  clarify       Clarification phase operations"
    echo "  prompt        Stand-alone prompt management"
    echo "  pr            Pull request operations"
    echo "  git           Git operations and comparisons"
    echo ""
    echo "Options:"
    echo "  --help, -h    Show this help message"
    echo "  --version, -v Show version information"
    echo ""
    echo "For domain-specific help, use: rdd.sh <domain> --help"
    echo ""
    echo "Examples:"
    echo "  rdd.sh change create my-feature feat"
    echo "  rdd.sh branch delete my-branch"
    echo "  rdd.sh requirements merge --dry-run"
}

show_branch_help() {
    print_banner "Branch Management"
    echo ""
    echo "Usage: rdd.sh branch <action> [options]"
    echo ""
    echo "Actions:"
    echo "  create <type> <name>    Create new branch (type: feat|fix)"
    echo "  delete [name] [--force] Delete branch (current if name omitted)"
    echo "  delete-merged           Delete all merged branches"
    echo "  status <name>           Check merge status of branch"
    echo "  list [filter]           List branches (optional filter)"
    echo ""
    echo "Examples:"
    echo "  rdd.sh branch create feat my-feature"
    echo "  rdd.sh branch delete my-old-branch"
    echo "  rdd.sh branch delete-merged"
    echo "  rdd.sh branch status feat/20241101-1234-my-feature"
}

show_workspace_help() {
    print_banner "Workspace Management"
    echo ""
    echo "Usage: rdd.sh workspace <action> [options]"
    echo ""
    echo "Actions:"
    echo "  init <type>        Initialize workspace (type: change|fix)"
    echo "  archive [--keep]   Archive current workspace"
    echo "  backup             Create backup of workspace"
    echo "  restore            Restore from latest backup"
    echo "  clear              Clear workspace with confirmation"
    echo ""
    echo "Examples:"
    echo "  rdd.sh workspace init change"
    echo "  rdd.sh workspace archive --keep"
    echo "  rdd.sh workspace backup"
}

show_requirements_help() {
    print_banner "Requirements Management"
    echo ""
    echo "Usage: rdd.sh requirements <action> [options]"
    echo ""
    echo "Actions:"
    echo "  validate              Validate requirements-changes.md format"
    echo "  merge [--dry-run]     Merge requirements changes"
    echo "  preview               Preview requirements merge"
    echo "  analyze               Analyze requirements impact"
    echo ""
    echo "Examples:"
    echo "  rdd.sh requirements validate"
    echo "  rdd.sh requirements merge --dry-run"
    echo "  rdd.sh requirements preview"
}

show_change_help() {
    print_banner "Change Workflow"
    echo ""
    echo "Usage: rdd.sh change <action> [options]"
    echo ""
    echo "Actions:"
    echo "  create [type]         Create new change (interactive)"
    echo "                        Optional type: feat (default) | fix"
    echo "  wrap-up               Complete change workflow"
    echo ""
    echo "Interactive Workflow:"
    echo "  The 'create' command will:"
    echo "  1. Display banner and instructions"
    echo "  2. Prompt for change description"
    echo "  3. Prompt for change name (any format)"
    echo "  4. Normalize name to kebab-case automatically"
    echo "  5. Validate and confirm name with user"
    echo "  6. Create branch and initialize workspace"
    echo ""
    echo "Examples:"
    echo "  rdd.sh change create          # Interactive, creates feat"
    echo "  rdd.sh change create fix      # Interactive, creates fix"
    echo "  rdd.sh change wrap-up         # Complete workflow"
}

show_fix_help() {
    print_banner "Fix Workflow"
    echo ""
    echo "Usage: rdd.sh fix <action> [options]"
    echo ""
    echo "Actions:"
    echo "  init <name>    Initialize fix workflow"
    echo "  wrap-up        Complete fix workflow"
    echo ""
    echo "Examples:"
    echo "  rdd.sh fix init my-bugfix"
    echo "  rdd.sh fix wrap-up"
}

show_clarify_help() {
    print_banner "Clarification Operations"
    echo ""
    echo "Usage: rdd.sh clarify <action> [options]"
    echo ""
    echo "Actions:"
    echo "  init                     Initialize clarification phase"
    echo "  log <Q> <A> [answeredBy] Log clarification Q&A"
    echo "  show [session]           Show clarifications"
    echo "  count                    Count clarifications"
    echo ""
    echo "Examples:"
    echo "  rdd.sh clarify init"
    echo "  rdd.sh clarify log \"What is X?\" \"X is Y\" \"John\""
}

show_prompt_help() {
    print_banner "Prompt Management"
    echo ""
    echo "Usage: rdd.sh prompt <action> [options]"
    echo ""
    echo "Actions:"
    echo "  mark-completed <id>       Mark prompt as completed"
    echo "  log-execution <id> <details> Log prompt execution"
    echo "  list [--status=unchecked] List prompts"
    echo ""
    echo "Examples:"
    echo "  rdd.sh prompt mark-completed P01"
    echo "  rdd.sh prompt log-execution P01 \"Created feature\""
    echo "  rdd.sh prompt list --status=unchecked"
}

show_pr_help() {
    print_banner "Pull Request Operations"
    echo ""
    echo "Usage: rdd.sh pr <action> [options]"
    echo ""
    echo "Actions:"
    echo "  create [--draft]           Create PR for current branch"
    echo "  request-review <reviewers> Request PR review"
    echo "  workflow                   Run automated PR workflow"
    echo ""
    echo "Examples:"
    echo "  rdd.sh pr create --draft"
    echo "  rdd.sh pr request-review @user1,@user2"
}

show_git_help() {
    print_banner "Git Operations"
    echo ""
    echo "Usage: rdd.sh git <action> [options]"
    echo ""
    echo "Actions:"
    echo "  compare           Compare current branch with main"
    echo "  modified-files    List modified files"
    echo "  file-diff <file>  Show diff for specific file"
    echo "  push              Push current branch to remote"
    echo ""
    echo "Examples:"
    echo "  rdd.sh git compare"
    echo "  rdd.sh git modified-files"
    echo "  rdd.sh git file-diff README.md"
}

# ============================================================================
# DOMAIN ROUTING
# ============================================================================

route_branch() {
    local action="$1"
    shift
    
    case "$action" in
        create)
            if [ $# -lt 2 ]; then
                print_error "Branch type and name required"
                echo "Usage: rdd.sh branch create <type> <name>"
                return 1
            fi
            create_branch "$1" "$2"
            ;;
        delete)
            if [ "$1" = "--force" ]; then
                delete_branch "" "true" "false"
            elif [ -n "$1" ] && [ "$2" = "--force" ]; then
                delete_branch "$1" "true" "false"
            elif [ -n "$1" ]; then
                delete_branch "$1" "false" "false"
            else
                delete_branch "" "false" "false"
            fi
            ;;
        delete-merged)
            delete_merged_branches
            ;;
        status)
            if [ -z "$1" ]; then
                print_error "Branch name required"
                echo "Usage: rdd.sh branch status <name>"
                return 1
            fi
            check_merge_status "$1"
            ;;
        list)
            list_branches "$1"
            ;;
        --help|-h)
            show_branch_help
            ;;
        *)
            print_error "Unknown branch action: $action"
            echo "Use 'rdd.sh branch --help' for usage information"
            return 1
            ;;
    esac
}

route_workspace() {
    local action="$1"
    shift
    
    case "$action" in
        init)
            # Check for --help flag before executing
            if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
                echo "Usage: rdd.sh workspace init <type>"
                echo ""
                echo "Initialize workspace with templates."
                echo ""
                echo "Arguments:"
                echo "  type    Workspace type: 'change' or 'fix'"
                echo ""
                echo "Examples:"
                echo "  rdd.sh workspace init change"
                echo "  rdd.sh workspace init fix"
                return 0
            fi
            if [ -z "$1" ]; then
                print_error "Workspace type required (change|fix)"
                echo "Usage: rdd.sh workspace init <type>"
                return 1
            fi
            init_workspace "$1"
            ;;
        archive)
            # Check for --help flag before executing
            if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
                echo "Usage: rdd.sh workspace archive [--keep]"
                echo ""
                echo "Archive current workspace to .rdd-docs/archive/"
                echo ""
                echo "Options:"
                echo "  --keep    Keep workspace after archiving (don't clear)"
                echo ""
                echo "Examples:"
                echo "  rdd.sh workspace archive"
                echo "  rdd.sh workspace archive --keep"
                return 0
            fi
            local keep="false"
            if [ "$1" = "--keep" ]; then
                keep="true"
            fi
            local branch_name=$(get_current_branch)
            archive_workspace "$branch_name" "$keep"
            ;;
        backup)
            # Check for --help flag before executing
            if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
                echo "Usage: rdd.sh workspace backup"
                echo ""
                echo "Create a backup of the current workspace."
                return 0
            fi
            backup_workspace
            ;;
        restore)
            # Check for --help flag before executing
            if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
                echo "Usage: rdd.sh workspace restore"
                echo ""
                echo "Restore workspace from the latest backup."
                return 0
            fi
            restore_workspace
            ;;
        clear)
            # Check for --help flag before executing
            if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
                echo "Usage: rdd.sh workspace clear"
                echo ""
                echo "Clear the workspace directory with confirmation."
                echo ""
                echo "WARNING: This will delete all workspace files!"
                return 0
            fi
            clear_workspace
            ;;
        --help|-h)
            show_workspace_help
            ;;
        *)
            print_error "Unknown workspace action: $action"
            echo "Use 'rdd.sh workspace --help' for usage information"
            return 1
            ;;
    esac
}

route_requirements() {
    local action="$1"
    shift
    
    case "$action" in
        validate)
            local req_file=".rdd-docs/workspace/requirements-changes.md"
            validate_requirements "$req_file"
            ;;
        merge)
            local dry_run="false"
            local backup="true"
            if [ "$1" = "--dry-run" ]; then
                dry_run="true"
            fi
            if [ "$1" = "--no-backup" ]; then
                backup="false"
            fi
            merge_requirements "$dry_run" "$backup"
            ;;
        preview)
            preview_merge
            ;;
        analyze)
            analyze_requirements_impact
            ;;
        --help|-h)
            show_requirements_help
            ;;
        *)
            print_error "Unknown requirements action: $action"
            echo "Use 'rdd.sh requirements --help' for usage information"
            return 1
            ;;
    esac
}

route_change() {
    local action="$1"
    shift
    
    case "$action" in
        create)
            # Safety checks before creating a change
            # 1. Check if we're on the main/master branch
            local current_branch=$(get_current_branch)
            local default_branch=$(get_default_branch)
            
            if [ "$current_branch" != "$default_branch" ]; then
                print_error "Cannot create change: not on default branch"
                print_warning "Current branch: $current_branch"
                print_warning "Expected branch: $default_branch"
                echo ""
                echo "Please switch to the $default_branch branch before creating a new change:"
                echo "  git checkout $default_branch"
                echo ""
                return 1
            fi
            
            # 2. Check if workspace folder is empty
            local workspace_dir=".rdd-docs/workspace"
            if [ -d "$workspace_dir" ] && [ -n "$(ls -A "$workspace_dir" 2>/dev/null)" ]; then
                print_error "Cannot create change: workspace directory is not empty"
                print_warning "Workspace path: $workspace_dir"
                echo ""
                echo "The workspace directory must be empty before creating a new change."
                echo "This prevents corruption of work in progress from another branch."
                echo ""
                echo "Options:"
                echo "  1. Complete current change: rdd.sh change wrap-up"
                echo "  2. Archive current workspace: rdd.sh workspace archive"
                echo "  3. Clear workspace (WARNING: data loss): rdd.sh workspace clear"
                echo ""
                return 1
            fi
            
            # Display banner
            echo ""
            echo "─── RDD-COPILOT ───"
            echo " Prompt: Create Change"
            echo " Description:"
            echo " > Create a new Change folder with timestamped naming,"
            echo " > branch setup, and template initialization."
            echo ""
            echo " User Action:"
            echo " > Provide a short description and name for the change."
            echo "───────────────"
            echo ""
            
            # 1. Prompt for description
            echo "Please provide a short description of the change:"
            echo "(e.g., 'Add user authentication feature', 'Fix login page bug')"
            read -p "> " change_description
            
            # Validate description was provided
            if [ -z "$change_description" ]; then
                print_error "Change description cannot be empty"
                return 1
            fi
            
            print_info "Description: $change_description"
            echo ""
            
            # 2. Prompt for name with normalization loop
            local change_name=""
            local normalized_name=""
            
            while true; do
                echo "Please provide a name for the change (will be normalized to kebab-case):"
                echo "(e.g., 'add user auth', 'Fix Login Bug', 'update-readme')"
                read -p "> " change_name
                
                # Check if name was provided
                if [ -z "$change_name" ]; then
                    print_error "Change name cannot be empty"
                    continue
                fi
                
                # Normalize the name to kebab-case
                normalized_name=$(normalize_to_kebab_case "$change_name")
                
                # Check if normalization was successful
                if [ $? -ne 0 ]; then
                    print_error "Unable to normalize name: $change_name"
                    echo "Please try a different name (use only letters, numbers, spaces, hyphens)"
                    continue
                fi
                
                # Validate normalized name
                if ! validate_name "$normalized_name"; then
                    print_warning "Normalized name '$normalized_name' doesn't meet requirements"
                    echo "Requirements: kebab-case, max 5 words, lowercase, hyphens only"
                    echo ""
                    continue
                fi
                
                # Show normalized name and confirm
                print_success "Normalized name: $normalized_name"
                read -p "Use this name? (y/n): " confirm
                
                if [[ "$confirm" =~ ^[Yy] ]]; then
                    break
                fi
                
                echo "Let's try again..."
                echo ""
            done
            
            # Store description in temp file (for reference/logging)
            local desc_file="/tmp/rdd-change-description-$$.txt"
            echo "$change_description" > "$desc_file"
            
            print_info "Description saved to: $desc_file"
            echo ""
            
            # Get change type or use default
            local change_type="${1:-feat}"
            
            # Create the change with normalized name
            create_change "$normalized_name" "$change_type"
            ;;
        wrap-up)
            # Check for --help flag before executing
            if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
                echo "Usage: rdd.sh change wrap-up"
                echo ""
                echo "Complete the current change workflow by:"
                echo "  1. Archiving workspace to .rdd-docs/archive/"
                echo "  2. Committing changes with automated message"
                echo "  3. Pushing branch to remote"
                echo ""
                echo "Note: This command does NOT create a pull request."
                echo "      You should manually create the PR on GitHub."
                return 0
            fi
            wrap_up_change
            ;;
        --help|-h)
            show_change_help
            ;;
        *)
            print_error "Unknown change action: $action"
            echo "Use 'rdd.sh change --help' for usage information"
            return 1
            ;;
    esac
}

route_fix() {
    local action="$1"
    shift
    
    case "$action" in
        init)
            if [ -z "$1" ]; then
                print_error "Fix name required"
                echo "Usage: rdd.sh fix init <name>"
                return 1
            fi
            
            # Safety checks before creating a fix (same as change create)
            # 1. Check if we're on the main/master branch
            local current_branch=$(get_current_branch)
            local default_branch=$(get_default_branch)
            
            if [ "$current_branch" != "$default_branch" ]; then
                print_error "Cannot create fix: not on default branch"
                print_warning "Current branch: $current_branch"
                print_warning "Expected branch: $default_branch"
                echo ""
                echo "Please switch to the $default_branch branch before creating a new fix:"
                echo "  git checkout $default_branch"
                echo ""
                return 1
            fi
            
            # 2. Check if workspace folder is empty
            local workspace_dir=".rdd-docs/workspace"
            if [ -d "$workspace_dir" ] && [ -n "$(ls -A "$workspace_dir" 2>/dev/null)" ]; then
                print_error "Cannot create fix: workspace directory is not empty"
                print_warning "Workspace path: $workspace_dir"
                echo ""
                echo "The workspace directory must be empty before creating a new fix."
                echo "This prevents corruption of work in progress from another branch."
                echo ""
                echo "Options:"
                echo "  1. Complete current change: rdd.sh change wrap-up"
                echo "  2. Archive current workspace: rdd.sh workspace archive"
                echo "  3. Clear workspace (WARNING: data loss): rdd.sh workspace clear"
                echo ""
                return 1
            fi
            
            create_change "$1" "fix"
            ;;
        wrap-up)
            # Check for --help flag before executing
            if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
                echo "Usage: rdd.sh fix wrap-up"
                echo ""
                echo "Complete the current fix workflow by:"
                echo "  1. Archiving workspace to .rdd-docs/archive/"
                echo "  2. Committing changes with automated message"
                echo "  3. Pushing branch to remote"
                echo ""
                echo "Note: This command does NOT create a pull request."
                echo "      You should manually create the PR on GitHub."
                return 0
            fi
            wrap_up_change
            ;;
        --help|-h)
            show_fix_help
            ;;
        *)
            print_error "Unknown fix action: $action"
            echo "Use 'rdd.sh fix --help' for usage information"
            return 1
            ;;
    esac
}

route_clarify() {
    local action="$1"
    shift
    
    case "$action" in
        init)
            init_clarification
            ;;
        log)
            if [ $# -lt 2 ]; then
                print_error "Question and answer required"
                echo "Usage: rdd.sh clarify log <question> <answer> [answeredBy]"
                return 1
            fi
            local question="$1"
            local answer="$2"
            local answered_by="${3:-$(get_git_user)}"
            local session_id="$(date +%s)"
            log_clarification "$question" "$answer" "$answered_by" "$session_id"
            ;;
        show)
            show_clarifications "$1"
            ;;
        count)
            count_clarifications
            ;;
        --help|-h)
            show_clarify_help
            ;;
        *)
            print_error "Unknown clarify action: $action"
            echo "Use 'rdd.sh clarify --help' for usage information"
            return 1
            ;;
    esac
}

route_prompt() {
    local action="$1"
    shift
    
    case "$action" in
        mark-completed)
            if [ -z "$1" ]; then
                print_error "Prompt ID required"
                echo "Usage: rdd.sh prompt mark-completed <id>"
                return 1
            fi
            local journal_file=".rdd-docs/workspace/journal.md"
            mark_prompt_completed "$1" "$journal_file"
            ;;
        log-execution)
            if [ $# -lt 2 ]; then
                print_error "Prompt ID and details required"
                echo "Usage: rdd.sh prompt log-execution <id> <details>"
                return 1
            fi
            local session_id="$(date +%s)"
            log_prompt_execution "$1" "$2" "$session_id"
            ;;
        list)
            local status="all"
            if [ "$1" = "--status=unchecked" ]; then
                status="unchecked"
            elif [ "$1" = "--status=checked" ]; then
                status="checked"
            fi
            local journal_file=".rdd-docs/workspace/journal.md"
            list_prompts "$status" "$journal_file"
            ;;
        --help|-h)
            show_prompt_help
            ;;
        *)
            print_error "Unknown prompt action: $action"
            echo "Use 'rdd.sh prompt --help' for usage information"
            return 1
            ;;
    esac
}

route_pr() {
    local action="$1"
    shift
    
    case "$action" in
        create)
            local draft="false"
            if [ "$1" = "--draft" ]; then
                draft="true"
            fi
            local branch_name=$(get_current_branch)
            local title="${branch_name} wrap-up"
            local body="Automated PR for branch ${branch_name}"
            create_pr "$branch_name" "$title" "$body" "$draft"
            ;;
        request-review)
            if [ -z "$1" ]; then
                print_error "Reviewers required"
                echo "Usage: rdd.sh pr request-review <reviewers>"
                return 1
            fi
            # This would need the PR number - simplified for now
            print_warning "PR review request requires PR number"
            print_info "Use GitHub CLI directly: gh pr review <pr-number> --request-reviewers $1"
            ;;
        workflow)
            local branch_name=$(get_current_branch)
            local archive_path=".rdd-docs/archive/${branch_name}"
            pr_workflow "$branch_name" "$archive_path"
            ;;
        --help|-h)
            show_pr_help
            ;;
        *)
            print_error "Unknown pr action: $action"
            echo "Use 'rdd.sh pr --help' for usage information"
            return 1
            ;;
    esac
}

route_git() {
    local action="$1"
    shift
    
    case "$action" in
        compare)
            compare_with_main
            ;;
        modified-files)
            get_modified_files
            ;;
        file-diff)
            if [ -z "$1" ]; then
                print_error "File path required"
                echo "Usage: rdd.sh git file-diff <file>"
                return 1
            fi
            get_file_diff "$1"
            ;;
        push)
            local branch_name=$(get_current_branch)
            push_to_remote "$branch_name"
            ;;
        --help|-h)
            show_git_help
            ;;
        *)
            print_error "Unknown git action: $action"
            echo "Use 'rdd.sh git --help' for usage information"
            return 1
            ;;
    esac
}

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

main() {
    # Handle no arguments
    if [ $# -eq 0 ]; then
        show_main_help
        return 0
    fi
    
    # Handle global options
    case "$1" in
        --version|-v)
            show_version
            return 0
            ;;
        --help|-h)
            show_main_help
            return 0
            ;;
    esac
    
    # Route to domain handler
    local domain="$1"
    shift
    
    case "$domain" in
        branch)
            route_branch "$@"
            ;;
        workspace)
            route_workspace "$@"
            ;;
        requirements)
            route_requirements "$@"
            ;;
        change)
            route_change "$@"
            ;;
        fix)
            route_fix "$@"
            ;;
        clarify)
            route_clarify "$@"
            ;;
        prompt)
            route_prompt "$@"
            ;;
        pr)
            route_pr "$@"
            ;;
        git)
            route_git "$@"
            ;;
        *)
            print_error "Unknown domain: $domain"
            echo ""
            echo "Available domains: branch, workspace, requirements, change, fix, clarify, prompt, pr, git"
            echo ""
            echo "Did you mean one of these?"
            case "$domain" in
                *branch*|*br*)
                    echo "  rdd.sh branch --help"
                    ;;
                *work*|*ws*)
                    echo "  rdd.sh workspace --help"
                    ;;
                *req*)
                    echo "  rdd.sh requirements --help"
                    ;;
                *change*|*ch*)
                    echo "  rdd.sh change --help"
                    ;;
                *fix*)
                    echo "  rdd.sh fix --help"
                    ;;
                *clarif*|*clar*)
                    echo "  rdd.sh clarify --help"
                    ;;
                *prompt*|*pr*)
                    echo "  rdd.sh prompt --help"
                    ;;
                *pull*|*pr*)
                    echo "  rdd.sh pr --help"
                    ;;
                *git*)
                    echo "  rdd.sh git --help"
                    ;;
                *)
                    echo "  rdd.sh --help"
                    ;;
            esac
            return 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
