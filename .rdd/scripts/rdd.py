#!/usr/bin/env python3
"""
rdd.py
Main wrapper script for RDD framework (Python version)
Provides domain-based routing to all utility scripts
Drop-in compatible with rdd.sh
"""

import sys
import os
import subprocess
import shutil
import json
from pathlib import Path
from typing import List, Optional

# Add the script directory to the path to import rdd_utils
SCRIPT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(SCRIPT_DIR))

# Import all functions from rdd_utils
from rdd_utils import (
    # Output functions
    print_success, print_error, print_warning, print_info, print_step, print_banner,
    # Validation functions
    validate_name, validate_branch_name, validate_file_exists, validate_dir_exists,
    # Git functions
    check_git_repo, get_current_branch, get_default_branch, get_git_user,
    check_uncommitted_changes, get_repo_root,
    # String functions
    normalize_to_kebab_case,
    # Utility functions
    ensure_dir, get_timestamp, get_timestamp_filename, confirm_action,
    exit_with_error, debug_print,
    # Config functions
    find_change_config, get_config, set_config,
    # Help functions
    help_section, help_command, help_option,
    Colors
)

# Version information
RDD_VERSION = "1.0.0"

# Constants
WORKSPACE_DIR = ".rdd-docs/workspace"
ARCHIVE_BASE_DIR = ".rdd-docs/archive"
TEMPLATES_DIR = ".rdd/templates"


# ============================================================================
# GIT OPERATIONS
# ============================================================================

def fetch_main() -> bool:
    """Fetch latest changes from remote default branch. Returns True on success."""
    default_branch = get_default_branch()
    print_step(f"Fetching latest from origin/{default_branch}...")
    
    result = subprocess.run(
        ['git', 'fetch', 'origin', default_branch, '--quiet'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode == 0:
        debug_print(f"Successfully fetched origin/{default_branch}")
        return True
    else:
        print_warning(f"Failed to fetch from origin/{default_branch}")
        return False


def push_to_remote(branch_name: Optional[str] = None) -> bool:
    """Push current branch to remote with upstream tracking."""
    if not branch_name:
        branch_name = get_current_branch()
    
    if not branch_name:
        print_error("No branch name provided and could not determine current branch")
        return False
    
    print_info(f"Pushing branch '{branch_name}' to remote...")
    
    result = subprocess.run(
        ['git', 'push', '-u', 'origin', branch_name],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print_success("Branch pushed to remote with upstream tracking")
        return True
    else:
        print_error("Failed to push branch to remote")
        if result.stderr:
            print(result.stderr)
        return False


def auto_commit(message: str) -> int:
    """
    Auto-commit all changes with a message.
    Returns: 0 on success, 1 on failure, 2 if no changes to commit.
    """
    if not message:
        print_error("Commit message is required")
        return 1
    
    print_info("Staging changes...")
    subprocess.run(['git', 'add', '-A'])
    
    # Check if there are changes to commit
    result = subprocess.run(
        ['git', 'diff', '--cached', '--quiet'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode == 0:
        print_warning("No changes to commit")
        return 2
    
    print_info("Committing changes...")
    result = subprocess.run(
        ['git', 'commit', '-m', message],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print_success(f"Changes committed: {message}")
        return 0
    else:
        print_error("Failed to commit changes")
        if result.stderr:
            print(result.stderr)
        return 1


def compare_with_main() -> bool:
    """Compare current branch with main branch."""
    fetch_main()
    
    default_branch = get_default_branch()
    current_branch = get_current_branch()
    
    print()
    print("━" * 50)
    print(f"  COMPARISON: {current_branch} vs {default_branch}")
    print("━" * 50)
    print()
    
    # Show commit differences
    print_step("Commit differences:")
    result = subprocess.run(
        ['git', 'rev-list', '--count', f'origin/{default_branch}..HEAD'],
        capture_output=True,
        text=True
    )
    commit_count = result.stdout.strip() if result.returncode == 0 else "0"
    print(f"  This branch is {commit_count} commit(s) ahead of {default_branch}")
    print()
    
    if commit_count != "0":
        subprocess.run([
            'git', 'log', '--oneline', '--graph', '--max-count=10',
            f'origin/{default_branch}..HEAD'
        ])
        print()
    
    # Show file changes
    print_step("File changes:")
    get_modified_files()
    print()
    
    print("━" * 50)
    return True


def get_modified_files() -> bool:
    """Get list of modified files compared to main branch."""
    default_branch = get_default_branch()
    current_branch = get_current_branch()
    
    print_info(f"Comparing {current_branch} with {default_branch}...")
    print()
    
    result = subprocess.run(
        ['git', 'diff', '--name-only', f'origin/{default_branch}...HEAD'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0 or not result.stdout.strip():
        print_warning(f"No files modified compared to {default_branch}")
        return True
    
    print("Modified files:")
    for file in result.stdout.strip().split('\n'):
        if file:
            # Get file status
            status_result = subprocess.run(
                ['git', 'diff', '--name-status', f'origin/{default_branch}...HEAD'],
                capture_output=True,
                text=True
            )
            
            status = 'M'
            for line in status_result.stdout.split('\n'):
                if file in line:
                    status = line.split()[0]
                    break
            
            if status.startswith('A'):
                print(f"  {Colors.GREEN}+{Colors.NC} {file} (added)")
            elif status.startswith('M'):
                print(f"  {Colors.YELLOW}~{Colors.NC} {file} (modified)")
            elif status.startswith('D'):
                print(f"  {Colors.RED}-{Colors.NC} {file} (deleted)")
            elif status.startswith('R'):
                print(f"  {Colors.CYAN}→{Colors.NC} {file} (renamed)")
            else:
                print(f"  {Colors.BLUE}?{Colors.NC} {file}")
    
    print()
    file_count = len([f for f in result.stdout.strip().split('\n') if f])
    print_success(f"Found {file_count} modified file(s)")
    return True


# ============================================================================
# BRANCH OPERATIONS
# ============================================================================

def create_branch(branch_type: str, branch_name: str) -> bool:
    """Create a new branch with format validation."""
    if not branch_type or not branch_name:
        print_error("Branch type and name are required")
        print("Usage: create_branch <enh|fix> <branch_name>")
        return False
    
    # Validate branch type
    if branch_type not in ['enh', 'fix']:
        print_error(f"Invalid branch type: {branch_type}")
        print_info("Valid types: enh, fix")
        return False
    
    # Validate branch name format
    if not validate_name(branch_name):
        return False
    
    # Generate branch ID with timestamp
    date_time = get_timestamp_filename()
    branch_id = f"{date_time}-{branch_name}"
    full_branch_name = f"{branch_type}/{branch_id}"
    
    # Check if branch already exists
    result = subprocess.run(
        ['git', 'show-ref', '--verify', '--quiet', f'refs/heads/{full_branch_name}'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode == 0:
        print_error(f"Branch '{full_branch_name}' already exists")
        return False
    
    default_branch = get_default_branch()
    
    print_step(f"Creating new branch: {full_branch_name}")
    
    # Switch to default branch and pull latest
    print_info(f"Switching to '{default_branch}' and pulling latest changes...")
    result = subprocess.run(
        ['git', 'checkout', default_branch],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode != 0:
        print_error(f"Failed to checkout '{default_branch}'")
        return False
    
    result = subprocess.run(
        ['git', 'pull', 'origin', default_branch],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode != 0:
        print_warning("Failed to pull from origin (continuing anyway)")
    
    # Create and checkout new branch
    print_info(f"Creating branch '{full_branch_name}'...")
    result = subprocess.run(
        ['git', 'checkout', '-b', full_branch_name],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print_success(f"Created and checked out branch: {full_branch_name}")
        print()
        print_info("Branch details:")
        print(f"  Type: {branch_type}")
        print(f"  Name: {branch_name}")
        print(f"  ID: {branch_id}")
        print(f"  Full: {full_branch_name}")
        return True
    else:
        print_error("Failed to create branch")
        return False


def delete_branch(branch_name: str, force: bool = False) -> bool:
    """Delete a branch locally and remotely with safety checks."""
    if not branch_name:
        # Delete current branch
        branch_name = get_current_branch()
    
    if not branch_name:
        print_error("Branch name is required")
        return False
    
    check_git_repo()
    
    # Check for uncommitted changes
    print_info("Checking for uncommitted changes...")
    if not check_uncommitted_changes():
        print_error("Please commit or stash changes before deleting branch")
        return False
    print()
    
    # Check if branch exists locally
    result = subprocess.run(
        ['git', 'show-ref', '--verify', '--quiet', f'refs/heads/{branch_name}'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode != 0:
        print_error(f"Local branch '{branch_name}' does not exist")
        return False
    
    # Get default branch to switch to
    default_branch = get_default_branch()
    
    # Switch to default branch
    print_info(f"Switching to branch '{default_branch}'...")
    result = subprocess.run(
        ['git', 'checkout', default_branch],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode != 0:
        print_error(f"Failed to checkout '{default_branch}'")
        return False
    print()
    
    # Delete local branch
    print_info(f"Deleting local branch '{branch_name}'...")
    flag = '-D' if force else '-d'
    result = subprocess.run(
        ['git', 'branch', flag, branch_name],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print_success("Local branch deleted" if not force else "Local branch force-deleted")
    else:
        print_error("Failed to delete local branch")
        return False
    print()
    
    # Check if remote branch exists and delete
    result = subprocess.run(
        ['git', 'ls-remote', '--heads', 'origin', branch_name],
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        print_info(f"Deleting remote branch 'origin/{branch_name}'...")
        result = subprocess.run(
            ['git', 'push', 'origin', '--delete', branch_name],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success("Remote branch deleted")
        else:
            print_warning("Failed to delete remote branch (it may not exist)")
    
    return True


def list_branches(filter_str: Optional[str] = None) -> bool:
    """List branches with optional filter."""
    print_step("Listing branches...")
    print()
    
    args = ['git', 'branch', '-a']
    result = subprocess.run(args, capture_output=True, text=True)
    
    if result.returncode != 0:
        print_error("Failed to list branches")
        return False
    
    branches = result.stdout.strip().split('\n')
    
    for branch in branches:
        branch = branch.strip()
        if branch:
            if filter_str and filter_str not in branch:
                continue
            
            if branch.startswith('*'):
                print(f"{Colors.GREEN}* {branch[2:]}{Colors.NC}")
            else:
                print(f"  {branch}")
    
    return True


# ============================================================================
# WORKSPACE OPERATIONS
# ============================================================================

def init_workspace(workspace_type: str = "change") -> bool:
    """Initialize workspace with templates based on type (change or fix)."""
    if workspace_type not in ['change', 'fix']:
        print_error(f"Invalid workspace type: {workspace_type}")
        print_info("Valid types: change, fix")
        return False
    
    print_step(f"Initializing workspace for type: {workspace_type}...")
    
    # Ensure workspace directory exists
    ensure_dir(WORKSPACE_DIR)
    
    # Copy main template based on type
    if workspace_type == 'fix':
        copy_template("fix.md", os.path.join(WORKSPACE_DIR, "fix.md"))
    
    # Copy copilot-prompts.md template to workspace with new name
    copy_template("copilot-prompts.md", os.path.join(WORKSPACE_DIR, ".rdd.copilot-prompts.md"))
    
    print_success(f"Workspace initialized successfully for {workspace_type}")
    return True


def copy_template(template_name: str, destination: str) -> bool:
    """Copy template file to destination with validation."""
    if not template_name or not destination:
        print_error("Template name and destination are required")
        return False
    
    template_path = os.path.join(TEMPLATES_DIR, template_name)
    
    # Validate template exists
    if not os.path.isfile(template_path):
        print_error(f"Template not found: {template_path}")
        return False
    
    # Create destination directory if needed
    dest_dir = os.path.dirname(destination)
    ensure_dir(dest_dir)
    
    # Check if destination already exists
    if os.path.isfile(destination):
        print_warning(f"Destination file already exists: {destination}")
        if not confirm_action("Overwrite existing file?"):
            print_info("Copy cancelled by user")
            return False
    
    # Copy template
    shutil.copy2(template_path, destination)
    print_success(f"Copied template {template_name} to {destination}")
    return True


def archive_workspace(branch_name: str, keep_workspace: bool = False) -> bool:
    """Archive workspace to branch-specific folder."""
    if not branch_name:
        print_error("Branch name is required")
        return False
    
    # Check if workspace exists and has content
    if not os.path.isdir(WORKSPACE_DIR):
        print_error(f"Workspace directory does not exist: {WORKSPACE_DIR}")
        return False
    
    if not os.listdir(WORKSPACE_DIR):
        print_error(f"Workspace directory is empty: {WORKSPACE_DIR}")
        return False
    
    # Create archive directory named after the branch
    safe_branch_name = branch_name.replace('/', '-')
    archive_dir = os.path.join(ARCHIVE_BASE_DIR, safe_branch_name)
    
    # Check if archive already exists
    if os.path.isdir(archive_dir):
        print_warning(f"Archive directory already exists: {archive_dir}")
        if not confirm_action("Overwrite existing archive?"):
            print_info("Archive cancelled by user")
            return False
        shutil.rmtree(archive_dir)
    
    # Create archive directory
    os.makedirs(archive_dir, exist_ok=True)
    
    # Copy all files from workspace to archive
    for item in os.listdir(WORKSPACE_DIR):
        src = os.path.join(WORKSPACE_DIR, item)
        dst = os.path.join(archive_dir, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    
    # Create metadata file
    git_user = get_git_user()
    result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True)
    last_commit = result.stdout.strip() if result.returncode == 0 else ""
    
    result = subprocess.run(
        ['git', 'log', '-1', '--pretty=%B'],
        capture_output=True,
        text=True
    )
    last_message = result.stdout.strip().split('\n')[0] if result.returncode == 0 else ""
    
    metadata = {
        "archivedAt": get_timestamp(),
        "branch": branch_name,
        "archivedBy": git_user,
        "lastCommit": last_commit,
        "lastCommitMessage": last_message
    }
    
    with open(os.path.join(archive_dir, ".archive-metadata"), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print_success(f"Workspace archived to: {archive_dir}")
    
    # Clean up workspace unless keep_workspace is true
    if not keep_workspace:
        clear_workspace_forced()
        print_info("Workspace directory cleared")
    else:
        print_info("Workspace directory kept as requested")
    
    return True


def clear_workspace() -> bool:
    """Clear workspace with safety confirmation."""
    print_warning("This will clear all workspace files.")
    
    if os.path.isdir(WORKSPACE_DIR) and os.listdir(WORKSPACE_DIR):
        print_info("Current workspace contains:")
        for item in os.listdir(WORKSPACE_DIR):
            print(f"  - {item}")
        print()
    
    if not confirm_action("Are you sure you want to clear the workspace?"):
        print_info("Operation cancelled")
        return False
    
    clear_workspace_forced()
    return True


def clear_workspace_forced() -> None:
    """Clear workspace without confirmation (internal use)."""
    if not os.path.isdir(WORKSPACE_DIR):
        debug_print("Workspace directory does not exist")
        return
    
    # Remove all files and subdirectories in workspace
    for item in os.listdir(WORKSPACE_DIR):
        item_path = os.path.join(WORKSPACE_DIR, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
    
    debug_print(f"Removed all contents from {WORKSPACE_DIR}")
    print_success("Workspace cleared")


# ============================================================================
# CHANGE OPERATIONS
# ============================================================================

def create_change(normalized_name: str, change_type: str = "enh") -> bool:
    """Create a new change with branch and workspace setup."""
    # Create the branch
    if not create_branch(change_type, normalized_name):
        return False
    
    print()
    
    # Initialize the workspace
    workspace_type = "fix" if change_type == "fix" else "change"
    if not init_workspace(workspace_type):
        print_error("Failed to initialize workspace")
        return False
    
    print()
    print_success("Change created successfully!")
    print_info(f"Branch: {change_type}/{get_timestamp_filename()}-{normalized_name}")
    print_info(f"Workspace initialized in: {WORKSPACE_DIR}")
    
    return True


def wrap_up_change() -> bool:
    """Complete the current change workflow."""
    current_branch = get_current_branch()
    
    if not current_branch:
        print_error("Could not determine current branch")
        return False
    
    print_banner("Wrap Up Change")
    print()
    
    # Archive workspace
    print_step("Archiving workspace...")
    if not archive_workspace(current_branch, keep_workspace=False):
        print_error("Failed to archive workspace")
        return False
    
    print()
    
    # Commit changes
    print_step("Committing changes...")
    commit_msg = f"Wrap up: {current_branch}"
    result = auto_commit(commit_msg)
    
    if result == 2:
        print_info("No uncommitted changes to commit")
    elif result != 0:
        print_error("Failed to commit changes")
        return False
    
    print()
    
    # Push to remote
    print_step("Pushing to remote...")
    if not push_to_remote(current_branch):
        print_error("Failed to push to remote")
        return False
    
    print()
    print_banner("Wrap Up Complete")
    print_success("Change wrapped up successfully!")
    print()
    print_info("Next steps:")
    print("  1. Create a pull request on GitHub")
    print("  2. Request code review")
    print("  3. Merge after approval")
    
    return True


# ============================================================================
# HELP SYSTEM
# ============================================================================

def show_version() -> None:
    """Show version information."""
    print(f"RDD Framework v{RDD_VERSION} (Python)")


def show_main_help() -> None:
    """Show main help message."""
    print_banner("RDD Framework - Requirements-Driven Development")
    print()
    print("Usage: rdd.py <domain> <action> [options]")
    print()
    print("Domains:")
    print("  branch        Branch management operations")
    print("  workspace     Workspace initialization and management")
    print("  change        Change workflow management")
    print("  fix           Fix workflow management")
    print("  git           Git operations and comparisons")
    print()
    print("Options:")
    print("  --help, -h    Show this help message")
    print("  --version, -v Show version information")
    print()
    print("For domain-specific help, use: rdd.py <domain> --help")
    print()
    print("Examples:")
    print("  rdd.py change create")
    print("  rdd.py branch delete my-branch")
    print("  rdd.py git compare")


def show_branch_help() -> None:
    """Show branch management help."""
    print_banner("Branch Management")
    print()
    print("Usage: rdd.py branch <action> [options]")
    print()
    print("Actions:")
    print("  create <type> <name>    Create new branch (type: enh|fix)")
    print("  delete [name] [--force] Delete branch (current if name omitted)")
    print("  list [filter]           List branches (optional filter)")
    print()
    print("Examples:")
    print("  rdd.py branch create enh my-enhancement")
    print("  rdd.py branch delete my-old-branch")
    print("  rdd.py branch list")


def show_workspace_help() -> None:
    """Show workspace management help."""
    print_banner("Workspace Management")
    print()
    print("Usage: rdd.py workspace <action> [options]")
    print()
    print("Actions:")
    print("  init <type>        Initialize workspace (type: change|fix)")
    print("  archive [--keep]   Archive current workspace")
    print("  clear              Clear workspace with confirmation")
    print()
    print("Examples:")
    print("  rdd.py workspace init change")
    print("  rdd.py workspace archive --keep")
    print("  rdd.py workspace clear")


def show_change_help() -> None:
    """Show change workflow help."""
    print_banner("Change Workflow")
    print()
    print("Usage: rdd.py change <action> [options]")
    print()
    print("Actions:")
    print("  create [type]         Create new change (interactive)")
    print("                        Optional type: enh (default) | fix")
    print("  wrap-up               Complete change workflow")
    print()
    print("Examples:")
    print("  rdd.py change create")
    print("  rdd.py change create fix")
    print("  rdd.py change wrap-up")


def show_git_help() -> None:
    """Show git operations help."""
    print_banner("Git Operations")
    print()
    print("Usage: rdd.py git <action> [options]")
    print()
    print("Actions:")
    print("  compare           Compare current branch with main")
    print("  modified-files    List modified files")
    print("  push              Push current branch to remote")
    print()
    print("Examples:")
    print("  rdd.py git compare")
    print("  rdd.py git modified-files")
    print("  rdd.py git push")


# ============================================================================
# DOMAIN ROUTING
# ============================================================================

def route_branch(args: List[str]) -> int:
    """Route branch domain commands."""
    if not args or args[0] in ['--help', '-h']:
        show_branch_help()
        return 0
    
    action = args[0]
    
    if action == 'create':
        if len(args) < 3:
            print_error("Branch type and name required")
            print("Usage: rdd.py branch create <type> <name>")
            return 1
        return 0 if create_branch(args[1], args[2]) else 1
    
    elif action == 'delete':
        force = '--force' in args
        branch_name = args[1] if len(args) > 1 and args[1] != '--force' else None
        if branch_name:
            return 0 if delete_branch(branch_name, force) else 1
        else:
            return 0 if delete_branch(get_current_branch(), force) else 1
    
    elif action == 'list':
        filter_str = args[1] if len(args) > 1 else None
        return 0 if list_branches(filter_str) else 1
    
    else:
        print_error(f"Unknown branch action: {action}")
        print("Use 'rdd.py branch --help' for usage information")
        return 1


def route_workspace(args: List[str]) -> int:
    """Route workspace domain commands."""
    if not args or args[0] in ['--help', '-h']:
        show_workspace_help()
        return 0
    
    action = args[0]
    
    if action == 'init':
        if len(args) < 2:
            print_error("Workspace type required (change|fix)")
            print("Usage: rdd.py workspace init <type>")
            return 1
        return 0 if init_workspace(args[1]) else 1
    
    elif action == 'archive':
        keep = '--keep' in args
        branch_name = get_current_branch()
        return 0 if archive_workspace(branch_name, keep) else 1
    
    elif action == 'clear':
        return 0 if clear_workspace() else 1
    
    else:
        print_error(f"Unknown workspace action: {action}")
        print("Use 'rdd.py workspace --help' for usage information")
        return 1


def route_change(args: List[str]) -> int:
    """Route change domain commands."""
    if not args or args[0] in ['--help', '-h']:
        show_change_help()
        return 0
    
    action = args[0]
    
    if action == 'create':
        # Safety checks
        current_branch = get_current_branch()
        default_branch = get_default_branch()
        
        if current_branch != default_branch:
            print_error("Cannot create change: not on default branch")
            print_warning(f"Current branch: {current_branch}")
            print_warning(f"Expected branch: {default_branch}")
            print()
            print(f"Please switch to the {default_branch} branch before creating a new change:")
            print(f"  git checkout {default_branch}")
            return 1
        
        # Check if workspace folder is empty
        if os.path.isdir(WORKSPACE_DIR) and os.listdir(WORKSPACE_DIR):
            print_error("Cannot create change: workspace directory is not empty")
            print_warning(f"Workspace path: {WORKSPACE_DIR}")
            print()
            print("The workspace directory must be empty before creating a new change.")
            print()
            print("Options:")
            print("  1. Complete current change: rdd.py change wrap-up")
            print("  2. Archive current workspace: rdd.py workspace archive")
            print("  3. Clear workspace (WARNING: data loss): rdd.py workspace clear")
            return 1
        
        # Display banner
        print()
        print("─── RDD-COPILOT ───")
        print(" Prompt: Create Change")
        print(" Description:")
        print(" > Create a new Change folder with timestamped naming,")
        print(" > branch setup, and template initialization.")
        print()
        print(" User Action:")
        print(" > Provide a short description and name for the change.")
        print("───────────────")
        print()
        
        # Prompt for description
        print("Please provide a short description of the change:")
        print("(e.g., 'Add user authentication enhancement', 'Fix login page bug')")
        try:
            change_description = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            print_error("Operation cancelled")
            return 1
        
        if not change_description:
            print_error("Change description cannot be empty")
            return 1
        
        print_info(f"Description: {change_description}")
        print()
        
        # Prompt for name with normalization loop
        normalized_name = None
        while not normalized_name:
            print("Please provide a name for the change (will be normalized to kebab-case):")
            print("(e.g., 'add user auth', 'Fix Login Bug', 'update-readme')")
            try:
                change_name = input("> ").strip()
            except (KeyboardInterrupt, EOFError):
                print()
                print_error("Operation cancelled")
                return 1
            
            if not change_name:
                print_error("Change name cannot be empty")
                continue
            
            # Normalize the name
            normalized_name = normalize_to_kebab_case(change_name)
            
            if not normalized_name:
                print_error(f"Unable to normalize name: {change_name}")
                print("Please try a different name (use only letters, numbers, spaces, hyphens)")
                continue
            
            # Validate normalized name
            if not validate_name(normalized_name):
                print_warning(f"Normalized name '{normalized_name}' doesn't meet requirements")
                print("Requirements: kebab-case, max 5 words, lowercase, hyphens only")
                print()
                normalized_name = None
                continue
            
            # Show normalized name and confirm
            print_success(f"Normalized name: {normalized_name}")
            try:
                confirm = input("Use this name? (y/n): ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print()
                print_error("Operation cancelled")
                return 1
            
            if confirm not in ['y', 'yes']:
                print("Let's try again...")
                print()
                normalized_name = None
        
        # Get change type or use default
        change_type = args[1] if len(args) > 1 else "enh"
        
        # Create the change
        return 0 if create_change(normalized_name, change_type) else 1
    
    elif action == 'wrap-up':
        return 0 if wrap_up_change() else 1
    
    else:
        print_error(f"Unknown change action: {action}")
        print("Use 'rdd.py change --help' for usage information")
        return 1


def route_fix(args: List[str]) -> int:
    """Route fix domain commands (similar to change but for fixes)."""
    if not args or args[0] in ['--help', '-h']:
        print_banner("Fix Workflow")
        print()
        print("Usage: rdd.py fix <action> [options]")
        print()
        print("Actions:")
        print("  init <name>    Initialize fix workflow")
        print("  wrap-up        Complete fix workflow")
        print()
        print("Examples:")
        print("  rdd.py fix init my-bugfix")
        print("  rdd.py fix wrap-up")
        return 0
    
    action = args[0]
    
    if action == 'init':
        if len(args) < 2:
            print_error("Fix name required")
            print("Usage: rdd.py fix init <name>")
            return 1
        
        # Similar safety checks as change create
        current_branch = get_current_branch()
        default_branch = get_default_branch()
        
        if current_branch != default_branch:
            print_error("Cannot create fix: not on default branch")
            return 1
        
        if os.path.isdir(WORKSPACE_DIR) and os.listdir(WORKSPACE_DIR):
            print_error("Cannot create fix: workspace directory is not empty")
            return 1
        
        return 0 if create_change(args[1], "fix") else 1
    
    elif action == 'wrap-up':
        return 0 if wrap_up_change() else 1
    
    else:
        print_error(f"Unknown fix action: {action}")
        return 1


def route_git(args: List[str]) -> int:
    """Route git domain commands."""
    if not args or args[0] in ['--help', '-h']:
        show_git_help()
        return 0
    
    action = args[0]
    
    if action == 'compare':
        return 0 if compare_with_main() else 1
    
    elif action == 'modified-files':
        return 0 if get_modified_files() else 1
    
    elif action == 'push':
        return 0 if push_to_remote() else 1
    
    else:
        print_error(f"Unknown git action: {action}")
        print("Use 'rdd.py git --help' for usage information")
        return 1


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main() -> int:
    """Main entry point for the script."""
    args = sys.argv[1:]
    
    # Handle no arguments - show help
    if not args:
        show_main_help()
        return 0
    
    # Handle global options
    if args[0] in ['--version', '-v']:
        show_version()
        return 0
    
    if args[0] in ['--help', '-h']:
        show_main_help()
        return 0
    
    # Route to domain handler
    domain = args[0]
    domain_args = args[1:]
    
    if domain == 'branch':
        return route_branch(domain_args)
    elif domain == 'workspace':
        return route_workspace(domain_args)
    elif domain == 'change':
        return route_change(domain_args)
    elif domain == 'fix':
        return route_fix(domain_args)
    elif domain == 'git':
        return route_git(domain_args)
    else:
        print_error(f"Unknown domain: {domain}")
        print()
        print("Available domains: branch, workspace, change, fix, git")
        print()
        print("Use 'rdd.py --help' for more information")
        return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        print_warning("Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if os.environ.get('DEBUG') == '1':
            import traceback
            traceback.print_exc()
        sys.exit(1)
