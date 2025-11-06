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
    check_git_repo, get_current_branch, get_default_branch, get_branch_type, 
    is_enh_or_fix_branch, get_git_user,
    check_uncommitted_changes, get_repo_root,
    stash_changes, restore_stashed_changes, pull_main, merge_main_into_current,
    update_from_main,
    # String functions
    normalize_to_kebab_case,
    # Utility functions
    ensure_dir, get_timestamp, get_timestamp_filename, confirm_action,
    exit_with_error, debug_print,
    # Config functions
    find_change_config, get_config, set_config,
    get_rdd_config_path, get_rdd_config, set_rdd_config,
    # Prompt functions
    mark_prompt_completed, log_prompt_execution, list_prompts, validate_prompt_status,
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

# Feature flags / hidden options
# Enhancement selection exists but is hidden from the interactive menu by default.
SHOW_ENH_IN_MENU_DEFAULT = False


# ============================================================================
# INTERACTIVE UI HELPERS
# ============================================================================

def _curses_menu(stdscr, title: str, items: list) -> int:
    """
    Basic arrow-key menu using curses. Returns selected index.
    Controls: Up/Down to move, Enter/Space to select, 'q' or ESC to cancel (returns -1).
    """
    curses = None
    try:
        import curses  # type: ignore
    except Exception:
        # Should never get here because this function is only called after import succeeded
        return -1

    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    current = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Title
        title_lines = [title, "", "Use ↑/↓ to move, Enter/Space to select."]
        for i, line in enumerate(title_lines):
            stdscr.addstr(i, 0, line[: max(0, w - 1)])

        # Items
        base_row = len(title_lines) + 1
        for idx, label in enumerate(items):
            prefix = "> " if idx == current else "  "
            line = f"{prefix}{label}"
            if idx == current:
                try:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(base_row + idx, 0, line[: max(0, w - 1)])
                    stdscr.attroff(curses.A_REVERSE)
                except Exception:
                    stdscr.addstr(base_row + idx, 0, line[: max(0, w - 1)])
            else:
                stdscr.addstr(base_row + idx, 0, line[: max(0, w - 1)])

        stdscr.refresh()

        key = stdscr.getch()
        if key in (ord('q'), 27):  # q or ESC
            return -1
        if key in (curses.KEY_UP, ord('k')):
            current = (current - 1) % len(items)
        elif key in (curses.KEY_DOWN, ord('j')):
            current = (current + 1) % len(items)
        elif key in (curses.KEY_ENTER, 10, 13, ord(' ')):
            return current


def select_change_type_interactive(reveal_enh: bool = SHOW_ENH_IN_MENU_DEFAULT) -> Optional[str]:
    """
    Show an interactive menu to select change type.
    By default, only 'Fix' is shown. 'Enhancement' can be revealed via flag/env.
    Returns: 'fix' or 'enh' or None if cancelled.
    """
    # Build visible options
    visible_options = [("Fix", "fix")]
    if reveal_enh:
        visible_options.append(("Enhancement", "enh"))

    labels = [label for (label, _code) in visible_options]

    # Try curses-based UI first
    try:
        import curses  # noqa: F401

        def _run(stdscr):
            return _curses_menu(stdscr, "Select change type", labels)

        selected_idx = __import__('curses').wrapper(_run)
        if selected_idx is None or selected_idx < 0:
            return None
        return visible_options[selected_idx][1]
    except Exception:
        # Fallback to simple numeric input
        print_info("Interactive menu unavailable; falling back to numeric selection.")
        for i, (label, _code) in enumerate(visible_options, start=1):
            print(f"  {i}. {label}")
        try:
            raw = input("Choose an option [1..{0}] (Enter for 1): ".format(len(visible_options))).strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return None
        if not raw:
            return visible_options[0][1]
        try:
            idx = int(raw)
            if 1 <= idx <= len(visible_options):
                return visible_options[idx - 1][1]
        except ValueError:
            pass
        print_warning("Invalid selection. Defaulting to 'fix'.")
        return 'fix'


def select_default_branch_interactive() -> Optional[str]:
    """
    Show an interactive menu to select the default branch.
    Options: main, dev, or custom entry
    Returns: selected branch name or None if cancelled.
    """
    # Build menu options
    menu_options = [
        ("main", "main"),
        ("dev", "dev"),
        ("Enter custom branch name", "custom")
    ]
    
    labels = [label for (label, _code) in menu_options]
    
    # Try curses-based UI first
    try:
        import curses  # noqa: F401
        
        def _run(stdscr):
            return _curses_menu(stdscr, "Select default branch for RDD framework", labels)
        
        selected_idx = __import__('curses').wrapper(_run)
        if selected_idx is None or selected_idx < 0:
            return None
        
        code = menu_options[selected_idx][1]
        
        # If custom, prompt for input
        if code == "custom":
            try:
                branch_name = input("Enter branch name: ").strip()
                if not branch_name:
                    print_warning("No branch name entered. Defaulting to 'main'.")
                    return "main"
                # Validate branch name format
                if not validate_branch_name(branch_name):
                    print_error(f"Invalid branch name: {branch_name}")
                    return None
                return branch_name
            except (KeyboardInterrupt, EOFError):
                print()
                return None
        
        return code
        
    except Exception:
        # Fallback to simple numeric input
        print_info("Interactive menu unavailable; falling back to numeric selection.")
        for i, (label, _code) in enumerate(menu_options, start=1):
            print(f"  {i}. {label}")
        try:
            raw = input("Choose an option [1..3] (Enter for 1): ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return None
        
        if not raw:
            return "main"
        
        try:
            idx = int(raw)
            if 1 <= idx <= len(menu_options):
                code = menu_options[idx - 1][1]
                
                # If custom, prompt for input
                if code == "custom":
                    try:
                        branch_name = input("Enter branch name: ").strip()
                        if not branch_name:
                            print_warning("No branch name entered. Defaulting to 'main'.")
                            return "main"
                        if not validate_branch_name(branch_name):
                            print_error(f"Invalid branch name: {branch_name}")
                            return None
                        return branch_name
                    except (KeyboardInterrupt, EOFError):
                        print()
                        return None
                
                return code
        except ValueError:
            pass
        
        print_warning("Invalid selection. Defaulting to 'main'.")
        return 'main'


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


def cleanup_after_merge(branch_name: str = None) -> bool:
    """
    Clean up after a branch has been merged.
    Switches to default branch, fetches and pulls latest, deletes the specified merged branch.
    
    Args:
        branch_name: Branch to delete (optional, will prompt if not provided)
    
    Returns:
        True on success, False on failure
    """
    check_git_repo()
    
    print_banner("POST-MERGE CLEANUP")
    print()
    
    # Get default branch and current branch
    default_branch = get_default_branch()
    current_branch = get_current_branch()
    
    # If no branch name provided, prompt for it or use current branch
    if not branch_name:
        # If we're not on the default branch, offer to delete current branch
        if current_branch != default_branch:
            print_info(f"Current branch: {current_branch}")
            if confirm_action("Delete current branch after cleanup?"):
                branch_name = current_branch
            else:
                try:
                    branch_name = input("Enter branch name to delete (or press Enter to skip): ").strip()
                except (KeyboardInterrupt, EOFError):
                    print()
                    print_info("Operation cancelled")
                    return False
                
                if not branch_name:
                    print_info("No branch specified for deletion")
        else:
            try:
                branch_name = input("Enter branch name to delete (or press Enter to skip): ").strip()
            except (KeyboardInterrupt, EOFError):
                print()
                print_info("Operation cancelled")
                return False
            
            if not branch_name:
                print_info("No branch specified for deletion")
    
    # Switch to default branch
    print_step(f"1. Switching to '{default_branch}' branch")
    if current_branch != default_branch:
        result = subprocess.run(
            ['git', 'checkout', default_branch],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        if result.returncode != 0:
            print_error(f"Failed to checkout '{default_branch}'")
            return False
        print_success(f"Switched to '{default_branch}'")
    else:
        print_info(f"Already on '{default_branch}'")
    print()
    
    # Fetch latest changes
    print_step("2. Fetching latest changes from remote")
    result = subprocess.run(
        ['git', 'fetch', 'origin'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode != 0:
        print_warning("Failed to fetch from remote")
    else:
        print_success("Fetched latest changes")
    print()
    
    # Pull latest changes for default branch
    print_step(f"3. Pulling latest changes for '{default_branch}'")
    result = subprocess.run(
        ['git', 'pull', 'origin', default_branch],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode != 0:
        print_warning("Failed to pull latest changes")
    else:
        print_success("Pulled latest changes")
    print()
    
    # Delete the branch if specified
    if branch_name:
        print_step(f"4. Deleting branch '{branch_name}'")
        
        # Check if branch exists locally
        result = subprocess.run(
            ['git', 'show-ref', '--verify', '--quiet', f'refs/heads/{branch_name}'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        if result.returncode == 0:
            # Try to delete local branch
            result = subprocess.run(
                ['git', 'branch', '-d', branch_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print_success("Local branch deleted")
            else:
                print_warning("Branch not fully merged, use --force if needed")
                if confirm_action("Force delete local branch?"):
                    result = subprocess.run(
                        ['git', 'branch', '-D', branch_name],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        print_success("Local branch force-deleted")
                    else:
                        print_error("Failed to delete local branch")
        else:
            print_info("Local branch does not exist (already deleted)")
        
        # Check and delete remote branch
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
                print_error("Failed to delete remote branch")
        else:
            print_info("Remote branch does not exist (already deleted)")
        
        print()
    
    # Display completion summary
    print_banner("CLEANUP COMPLETE")
    print_success("Post-merge cleanup completed successfully!")
    print()
    print_info("Summary:")
    print(f"  • Switched to '{default_branch}' branch")
    print("  • Fetched and pulled latest changes")
    if branch_name:
        print(f"  • Deleted branch '{branch_name}' (local and remote)")
    print()
    
    return True


# ============================================================================
# WORKSPACE OPERATIONS
# ============================================================================

def init_rdd_docs() -> bool:
    """Initialize .rdd-docs directory with core template files if it doesn't exist."""
    rdd_docs_dir = ".rdd-docs"
    
    # List of core templates that should always exist in .rdd-docs
    core_templates = [
        "backlog.md",
        "requirements.md",
        "tech-spec.md",
        "folder-structure.md",
        "data-model.md",
        "config.json"
    ]
    
    # Check if .rdd-docs directory exists
    if not os.path.isdir(rdd_docs_dir):
        print_step("Initializing .rdd-docs directory with core templates...")
        ensure_dir(rdd_docs_dir)
    else:
        # Check if all core templates exist
        missing_templates = []
        for template_name in core_templates:
            dest_path = os.path.join(rdd_docs_dir, template_name)
            if not os.path.isfile(dest_path):
                missing_templates.append(template_name)
        
        # If no templates are missing, skip initialization
        if not missing_templates:
            debug_print(".rdd-docs already initialized with all core templates")
            return True
        
        print_step(f"Initializing missing templates in .rdd-docs ({len(missing_templates)} templates)...")
    
    # Copy core template files to .rdd-docs
    success_count = 0
    config_needs_population = False
    
    for template_name in core_templates:
        dest_path = os.path.join(rdd_docs_dir, template_name)
        
        # Skip if file already exists (don't overwrite existing work)
        if os.path.isfile(dest_path):
            debug_print(f"Skipping {template_name} (already exists)")
            success_count += 1
            continue
        
        # Copy template from .rdd/templates/
        template_path = os.path.join(TEMPLATES_DIR, template_name)
        
        if not os.path.isfile(template_path):
            print_warning(f"Template not found: {template_path}")
            continue
        
        try:
            shutil.copy2(template_path, dest_path)
            debug_print(f"Copied {template_name} to .rdd-docs/")
            success_count += 1
            
            # Mark that config.json needs to be populated
            if template_name == "config.json":
                config_needs_population = True
                
        except Exception as e:
            print_error(f"Failed to copy {template_name}: {e}")
            return False
    
    # Populate config.json if it was just created
    if config_needs_population:
        print_step("Configuring default branch...")
        
        # Prompt user to select default branch
        selected_branch = select_default_branch_interactive()
        
        if not selected_branch:
            print_warning("No branch selected. Using 'main' as default.")
            selected_branch = "main"
        
        # Update config.json with selected branch and timestamps
        from datetime import datetime, timezone
        config_path = os.path.join(rdd_docs_dir, "config.json")
        
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            
            config_data["defaultBranch"] = selected_branch
            config_data["created"] = datetime.now(timezone.utc).isoformat()
            config_data["lastModified"] = datetime.now(timezone.utc).isoformat()
            
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            print_success(f"Default branch configured: {selected_branch}")
            
        except Exception as e:
            print_error(f"Failed to populate config.json: {e}")
            return False
    
    if success_count == len(core_templates):
        print_success(f".rdd-docs initialized with {len(core_templates)} core templates")
        return True
    else:
        print_error(f"Failed to initialize all templates ({success_count}/{len(core_templates)} succeeded)")
        return False


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
    
    # Initialize .rdd-docs directory with core templates if needed
    if not init_rdd_docs():
        print_error("Failed to initialize .rdd-docs directory")
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
    
    # Validate that we're on an enh or fix branch
    if not is_enh_or_fix_branch(current_branch):
        print_error(f"Cannot wrap up: not on an enhancement or fix branch")
        print_warning(f"Current branch: {current_branch}")
        print()
        print_info("Wrap-up can only be performed on branches starting with 'enh/' or 'fix/'")
        print()
        print("Valid branch format examples:")
        print("  • enh/20241101-1234-my-enhancement")
        print("  • fix/20241101-1234-my-bugfix")
        return False
    
    print_banner("Wrap Up Change")
    print()
    
    # Archive workspace
    print_step("Archiving workspace...")
    if not archive_workspace(current_branch, keep_workspace=False):
        print_error("Failed to archive workspace")
        return False
    
    print()
    
    # Commit changes (including any uncommitted changes)
    print_step("Committing changes...")
    commit_msg = f"wrap up {current_branch}"
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
    print("  prompt        Stand-alone prompt management")
    print("  config        Configuration management")
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
    print("  rdd.py prompt mark-completed P01")
    print("  rdd.py config show")


def show_branch_help() -> None:
    """Show branch management help."""
    print_banner("Branch Management")
    print()
    print("Usage: rdd.py branch <action> [options]")
    print()
    print("Actions:")
    print("  create <type> <name>    Create new branch (type: enh|fix)")
    print("  delete [name] [--force] Delete branch (current if name omitted)")
    print("  cleanup [name]          Post-merge cleanup: fetch main, pull, delete branch")
    print("  list [filter]           List branches (optional filter)")
    print()
    print("Examples:")
    print("  rdd.py branch create enh my-enhancement")
    print("  rdd.py branch delete my-old-branch")
    print("  rdd.py branch cleanup enh/20241101-1234-my-enhancement")
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
    print("  update-from-main  Update current branch from main")
    print()
    print("Examples:")
    print("  rdd.py git compare")
    print("  rdd.py git modified-files")
    print("  rdd.py git push")
    print("  rdd.py git update-from-main")


def show_prompt_help() -> None:
    """Show prompt management help."""
    print_banner("Prompt Management")
    print()
    print("Usage: rdd.py prompt <action> [options]")
    print()
    print("Actions:")
    print("  mark-completed <id>          Mark prompt as completed")
    print("  log-execution <id> <details> Log prompt execution")
    print("  list [--status=unchecked]    List prompts")
    print()
    print("Examples:")
    print("  rdd.py prompt mark-completed P01")
    print("  rdd.py prompt log-execution P01 \"Created enhancement\"")
    print("  rdd.py prompt list --status=unchecked")


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
    
    elif action == 'cleanup':
        branch_name = args[1] if len(args) > 1 else None
        return 0 if cleanup_after_merge(branch_name) else 1
    
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
        
        # Determine change type
        # Hidden reveal flag for enhancement option in the interactive menu
        reveal_enh = False
        # Allow env override to reveal enhancement in menu
        if os.environ.get("RDD_REVEAL_ENH", "0") in ("1", "true", "True"):
            reveal_enh = True
        # Allow hidden CLI flag (will be ignored by help) and strip it from args
        if "--reveal-enh" in args:
            reveal_enh = True
            args = [a for a in args if a != "--reveal-enh"]

        # If user passed type explicitly, honor it (keeps non-interactive, script-param capability)
        if len(args) > 1 and args[1] in ("enh", "fix"):
            change_type = args[1]
        else:
            # Interactive selection (menu shows only Fix by default)
            print()
            print_step("Select change type")
            selected = select_change_type_interactive(reveal_enh=reveal_enh)
            if not selected:
                print_info("Operation cancelled")
                return 1
            change_type = selected
        
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
    
    elif action == 'update-from-main':
        return 0 if update_from_main() else 1
    
    else:
        print_error(f"Unknown git action: {action}")
        print("Use 'rdd.py git --help' for usage information")
        return 1


def route_prompt(args: List[str]) -> int:
    """Route prompt domain commands."""
    if not args or args[0] in ['--help', '-h']:
        show_prompt_help()
        return 0
    
    action = args[0]
    
    if action == 'mark-completed':
        if len(args) < 2:
            print_error("Prompt ID required")
            print("Usage: rdd.py prompt mark-completed <id>")
            return 1
        journal_file = os.path.join(WORKSPACE_DIR, ".rdd.copilot-prompts.md")
        return 0 if mark_prompt_completed(args[1], journal_file) else 1
    
    elif action == 'log-execution':
        if len(args) < 3:
            print_error("Prompt ID and details required")
            print("Usage: rdd.py prompt log-execution <id> <details>")
            return 1
        session_id = f"exec-{get_timestamp_filename()}"
        return 0 if log_prompt_execution(args[1], args[2], session_id) else 1
    
    elif action == 'list':
        status = "all"
        if len(args) > 1:
            if args[1] == "--status=unchecked":
                status = "unchecked"
            elif args[1] == "--status=checked":
                status = "checked"
        journal_file = os.path.join(WORKSPACE_DIR, ".rdd.copilot-prompts.md")
        return 0 if list_prompts(status, journal_file) else 1
    
    else:
        print_error(f"Unknown prompt action: {action}")
        print("Use 'rdd.py prompt --help' for usage information")
        return 1


def route_config(args: List[str]) -> int:
    """Route config domain commands."""
    if not args or args[0] in ['--help', '-h']:
        show_config_help()
        return 0
    
    action = args[0]
    
    if action == 'show':
        config_path = get_rdd_config_path()
        if not os.path.isfile(config_path):
            print_warning("No RDD config file found at .rdd-docs/config.json")
            print_info("Run 'rdd.py change create' to initialize the configuration")
            return 1
        try:
            with open(config_path, 'r') as f:
                content = f.read()
            print(content)
            return 0
        except Exception as e:
            print_error(f"Failed to read config: {e}")
            return 1
    
    elif action == 'get':
        if len(args) < 2:
            print_error("Config key required")
            print_info("Usage: rdd.py config get <key>")
            return 1
        key = args[1]
        value = get_rdd_config(key)
        if value is not None:
            print(f"{key}: {value}")
            return 0
        else:
            print_warning(f"Config key '{key}' not found")
            return 1
    
    elif action == 'set':
        if len(args) < 3:
            print_error("Config key and value required")
            print_info("Usage: rdd.py config set <key> <value>")
            return 1
        key = args[1]
        value = args[2]
        
        if set_rdd_config(key, value):
            print_success(f"Configuration updated: {key} = {value}")
            return 0
        else:
            return 1
    
    else:
        print_error(f"Unknown config action: {action}")
        print()
        show_config_help()
        return 1


def show_config_help() -> None:
    """Show config management help."""
    print_banner("Configuration Management")
    print()
    print("Usage: rdd.py config <action> [options]")
    print()
    print("Actions:")
    print("  show              Display entire configuration file")
    print("  get <key>         Get specific configuration value")
    print("  set <key> <val>   Set configuration value")
    print()
    print("Configuration file location: .rdd-docs/config.json")
    print()
    print("Available keys:")
    print("  defaultBranch     The default branch for creating changes")
    print()
    print("Examples:")
    print("  rdd.py config show")
    print("  rdd.py config get defaultBranch")
    print("  rdd.py config set defaultBranch dev")
    print()


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
    elif domain == 'prompt':
        return route_prompt(domain_args)
    elif domain == 'config':
        return route_config(domain_args)
    else:
        print_error(f"Unknown domain: {domain}")
        print()
        print("Available domains: branch, workspace, change, fix, git, prompt, config")
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
