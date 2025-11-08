#!/usr/bin/env python3
"""
rdd_utils.py
Shared utility functions for RDD framework Python scripts
Provides common utilities used across all RDD Python scripts
"""

import os
import sys
import re
import subprocess
import shutil
import json
from datetime import datetime, timezone
from typing import Optional, List, Tuple
from pathlib import Path


# ============================================================================
# CONSTANTS
# ============================================================================

# ANSI color codes for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color


# Global debug flag
DEBUG = os.environ.get('DEBUG', '0') == '1'


# ============================================================================
# COLORED OUTPUT FUNCTIONS
# ============================================================================

def print_success(message: str) -> None:
    """Print success message with green checkmark."""
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")


def print_error(message: str) -> None:
    """Print error message with red X to stderr."""
    print(f"{Colors.RED}✗ {message}{Colors.NC}", file=sys.stderr)


def print_warning(message: str) -> None:
    """Print warning message with yellow warning symbol."""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.NC}")


def print_info(message: str) -> None:
    """Print info message with blue info symbol."""
    print(f"{Colors.BLUE}ℹ {message}{Colors.NC}")


def print_step(message: str) -> None:
    """Print step message with cyan arrow."""
    print(f"{Colors.CYAN}▶{Colors.NC} {message}")


def print_banner(title: str, subtitle: str = "") -> None:
    """Print a formatted banner with custom title and optional subtitle."""
    total_width = 60
    
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("╔" + "═" * (total_width - 2) + "╗")
    
    # Calculate padding for centered title
    title_len = len(title)
    padding = (total_width - 2 - title_len) // 2
    padding_str = " " * padding
    # Adjust for odd/even differences
    right_padding = " " * (total_width - 2 - title_len - padding)
    
    print(f"║{padding_str}{title}{right_padding}║")
    
    if subtitle:
        subtitle_len = len(subtitle)
        sub_padding = (total_width - 2 - subtitle_len) // 2
        sub_padding_str = " " * sub_padding
        sub_right_padding = " " * (total_width - 2 - subtitle_len - sub_padding)
        print(f"║{sub_padding_str}{subtitle}{sub_right_padding}║")
    
    print("╚" + "═" * (total_width - 2) + "╝")
    print(f"{Colors.NC}")


# ============================================================================
# DEBUG FUNCTIONS
# ============================================================================

def is_debug_mode() -> bool:
    """Check if running in debug mode."""
    return DEBUG


def debug_print(message: str) -> None:
    """Debug print (only prints if DEBUG=1)."""
    if is_debug_mode():
        print(f"{Colors.CYAN}[DEBUG]{Colors.NC} {message}", file=sys.stderr)


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_name(name: str) -> bool:
    """
    Validate name is in kebab-case format with max 5 words.
    Returns True if valid, False if invalid.
    """
    if not name:
        print_error("Name cannot be empty")
        return False
    
    # Check kebab-case format (lowercase, hyphens only, no spaces)
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        print_error(f"Invalid name: '{name}'")
        print_error("Must be kebab-case (lowercase, hyphens only, no spaces)")
        print_error("Examples: my-enhancement, bug-fix, user-authentication")
        return False
    
    # Count words (split by hyphen)
    word_count = len(name.split('-'))
    if word_count > 5:
        print_error(f"Name too long: {word_count} words (maximum 5)")
        print_error("Use a shorter, more concise name")
        return False
    
    return True


def validate_branch_name(branch_name: str) -> bool:
    """
    Validate branch name format: kebab-case only.
    Returns True if valid, False if invalid.
    """
    if not branch_name:
        print_error("Branch name cannot be empty")
        return False
    
    # Check kebab-case format (lowercase, hyphens, numbers, slashes allowed)
    if not re.match(r'^[a-z0-9]+([/-][a-z0-9]+)*$', branch_name):
        print_error(f"Invalid branch name format: '{branch_name}'")
        print_error("Must be kebab-case (lowercase, hyphens, numbers, and slashes only)")
        print_error("Example: fix/my-bugfix, my-enhancement, 20251107-my-fix")
        return False
    
    return True


def validate_file_exists(file_path: str, file_description: str = "File") -> bool:
    """
    Check if a file exists.
    Returns True if exists, False if not.
    """
    if not file_path:
        print_error("File path cannot be empty")
        return False
    
    if not os.path.isfile(file_path):
        print_error(f"{file_description} not found: {file_path}")
        return False
    
    return True


def validate_dir_exists(dir_path: str, dir_description: str = "Directory") -> bool:
    """
    Check if a directory exists.
    Returns True if exists, False if not.
    """
    if not dir_path:
        print_error("Directory path cannot be empty")
        return False
    
    if not os.path.isdir(dir_path):
        print_error(f"{dir_description} not found: {dir_path}")
        return False
    
    return True


# ============================================================================
# STRING NORMALIZATION
# ============================================================================

def normalize_to_kebab_case(input_str: str) -> Optional[str]:
    """
    Normalize text to kebab-case format.
    Handles various inputs: "Add User Auth", "fix_login_bug", "fix/update-README"
    Preserves slashes for branch prefixes like "fix/" or "enh/"
    Returns kebab-case string or None on failure.
    """
    if not input_str:
        return None
    
    # Normalization steps:
    # 1. Convert to lowercase
    # 2. Replace underscores and spaces with hyphens (but keep slashes)
    # 3. Remove any characters that aren't lowercase letters, numbers, hyphens, or slashes
    # 4. Replace multiple consecutive hyphens with single hyphen
    # 5. Remove leading and trailing hyphens (but not slashes)
    
    normalized = input_str.lower()
    normalized = normalized.replace('_', '-').replace(' ', '-')
    normalized = re.sub(r'[^a-z0-9/-]', '', normalized)
    normalized = re.sub(r'-+', '-', normalized)
    normalized = normalized.strip('-')
    
    # Check if result is empty (all characters were invalid)
    if not normalized:
        return None
    
    return normalized


# ============================================================================
# DIRECTORY OPERATIONS
# ============================================================================

def ensure_dir(dir_path: str) -> None:
    """Create directory if it doesn't exist."""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        debug_print(f"Created directory: {dir_path}")


# ============================================================================
# TIMESTAMP FUNCTIONS
# ============================================================================

def get_timestamp() -> str:
    """Get timestamp in ISO 8601 format (e.g., 2023-11-01T12:34:56Z)."""
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def get_timestamp_filename() -> str:
    """Get timestamp for filenames (no special characters, e.g., 20231101-1234)."""
    return datetime.now().strftime('%Y%m%d-%H%M')


# ============================================================================
# GIT REPOSITORY CHECKS
# ============================================================================

def check_git_repo(repo_path: str = None, exit_on_error: bool = True) -> bool:
    """
    Check if we're in a git repository.
    
    Args:
        repo_path: Optional path to check. If None, checks current directory.
        exit_on_error: If True, exits with error when not a git repo. If False, returns False.
    
    Returns:
        True if in git repo, False if not (when exit_on_error=False), exits otherwise.
    """
    cmd = ['git', 'rev-parse', '--is-inside-work-tree']
    kwargs = {
        'stdout': subprocess.DEVNULL,
        'stderr': subprocess.DEVNULL
    }
    
    if repo_path:
        kwargs['cwd'] = repo_path
    
    result = subprocess.run(cmd, **kwargs)
    
    if result.returncode != 0:
        if exit_on_error:
            print_error("Not a git repository. Please run this from within a git repository.")
            sys.exit(1)
        return False
    
    debug_print("Git repository verified")
    return True


def get_repo_root() -> str:
    """Get repository root directory."""
    result = subprocess.run(
        ['git', 'rev-parse', '--show-toplevel'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return result.stdout.strip()
    return os.getcwd()


# ============================================================================
# GIT BRANCH OPERATIONS
# ============================================================================

def get_current_branch() -> str:
    """Get current branch name."""
    result = subprocess.run(
        ['git', 'branch', '--show-current'],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def interactive_branch_cleanup(base_branch: str = None) -> None:
    """
    Show an interactive menu listing all branches merged into the base branch.
    Lets the user choose branches to delete locally (and optionally remotely).
    """
    if not base_branch:
        base_branch = get_default_branch()

    print_banner("Merged Branches Cleanup", f"Base: {base_branch}")
    
    # Check for uncommitted changes before attempting checkout
    if not check_uncommitted_changes():
        print_error("Cannot proceed with branch cleanup.")
        print_info("Please commit or stash your changes first.")
        return
    
    # Fetch from remote only if not in local-only mode
    if not is_local_only_mode():
        subprocess.run(["git", "fetch", "origin", "--quiet"])
    else:
        print_info("Local-only mode: Skipping remote fetch")
    
    # Attempt to checkout base branch
    result = subprocess.run(
        ["git", "checkout", base_branch],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print_error(f"Failed to checkout {base_branch}")
        if result.stderr:
            print(result.stderr)
        return

    # Get merged branches
    result = subprocess.run(
        ["git", "branch", "--merged", base_branch],
        capture_output=True, text=True
    )
    
    # Protected branches that should never be deleted
    protected_branches = {base_branch, "dev", "main", "master"}
    
    merged_branches = []
    for b in result.stdout.splitlines():
        # Remove leading/trailing whitespace and the asterisk marker
        branch_name = b.strip().lstrip("* ").strip()
        # Only include if non-empty and not protected
        if branch_name and branch_name not in protected_branches:
            merged_branches.append(branch_name)

    if not merged_branches:
        print_info("No merged branches to clean up.")
        return

    print_info("The following branches are fully merged:")
    for i, branch in enumerate(merged_branches, start=1):
        print(f"  {i}. {branch}")

    print("")
    selected = input(f"{Colors.YELLOW}Enter numbers to delete (comma-sep or 'all' to delete all, ENTER to cancel): {Colors.NC}").strip()

    if not selected:
        print_info("Cleanup cancelled.")
        return

    if selected.lower() == "all":
        to_delete = merged_branches
    else:
        try:
            indexes = [int(x.strip()) for x in selected.split(",") if x.strip().isdigit()]
            to_delete = [merged_branches[i - 1] for i in indexes if 0 < i <= len(merged_branches)]
        except Exception:
            print_error("Invalid input.")
            return

    if not to_delete:
        print_info("No valid branches selected.")
        return

    print("")
    print_warning(f"About to delete {len(to_delete)} merged branch(es):")
    for b in to_delete:
        print(f"  - {b}")

    if not confirm_action("Proceed with deletion?"):
        print_info("Cleanup aborted.")
        return

    for b in to_delete:
        subprocess.run(["git", "branch", "-d", b])
    print_success("Selected merged branches deleted locally.")

    # Only ask about remote deletion if not in local-only mode
    if not is_local_only_mode():
        if confirm_action("Also delete them from origin (remote)?"):
            for b in to_delete:
                subprocess.run(["git", "push", "origin", "--delete", b])
            print_success("Deleted selected branches from remote as well.")
    else:
        print_info("Local-only mode: Skipping remote branch deletion")


def get_default_branch() -> str:
    """
    Get the default branch name with intelligent detection.
    Priority:
    1. User config file (.rdd-docs/config.json)
    2. Local branch detection (main, then master)
    3. Fallback to "main"
    """
    # 1. Check config file first (user configuration)
    config_branch = get_rdd_config("defaultBranch")
    if config_branch:
        # Verify branch actually exists
        result = subprocess.run(
            ['git', 'show-ref', '--verify', '--quiet', f'refs/heads/{config_branch}'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            return config_branch
        else:
            debug_print(f"Configured default branch '{config_branch}' not found, using auto-detection")
    
    # 2. Check if main branch exists
    result = subprocess.run(
        ['git', 'show-ref', '--verify', '--quiet', 'refs/heads/main'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode == 0:
        return "main"
    
    # 3. Check if master branch exists
    result = subprocess.run(
        ['git', 'show-ref', '--verify', '--quiet', 'refs/heads/master'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode == 0:
        return "master"
    
    # 4. Final fallback
    return "main"  # Default to main


def get_branch_type(branch_name: str = None) -> str:
    """
    Get the type of the branch (enh or fix).
    If branch_name is not provided, uses current branch.
    Returns 'enh', 'fix', or empty string if not a valid type.
    """
    if not branch_name:
        branch_name = get_current_branch()
    
    if not branch_name:
        return ""
    
    if branch_name.startswith('enh/'):
        return 'enh'
    elif branch_name.startswith('fix/'):
        return 'fix'
    
    return ""


def is_enh_or_fix_branch(branch_name: str = None) -> bool:
    """
    DEPRECATED: Use is_valid_work_branch() instead.
    Check if the branch is an enhancement or fix branch.
    If branch_name is not provided, uses current branch.
    Returns True if branch starts with 'enh/' or 'fix/', False otherwise.
    """
    branch_type = get_branch_type(branch_name)
    return branch_type in ['enh', 'fix']


def is_valid_work_branch(branch_name: str = None) -> bool:
    """
    Check if the branch is valid for work (not a protected branch).
    If branch_name is not provided, uses current branch.
    
    A valid work branch is any branch EXCEPT:
    - The default branch (detected via get_default_branch())
    - "main"
    - "master"
    
    Returns True if valid work branch, False otherwise.
    """
    if not branch_name:
        branch_name = get_current_branch()
    
    if not branch_name:
        return False
    
    # Get the default branch
    default_branch = get_default_branch()
    
    # Check if current branch is one of the protected branches
    protected_branches = {default_branch, 'main', 'master'}
    
    return branch_name not in protected_branches


def get_git_user() -> str:
    """Get git user information. Returns 'Name <email>'."""
    name_result = subprocess.run(
        ['git', 'config', 'user.name'],
        capture_output=True,
        text=True
    )
    email_result = subprocess.run(
        ['git', 'config', 'user.email'],
        capture_output=True,
        text=True
    )
    
    name = name_result.stdout.strip()
    email = email_result.stdout.strip()
    
    return f"{name} <{email}>"


def check_uncommitted_changes() -> bool:
    """
    Check for uncommitted changes (modified, staged, or untracked files).
    Returns True if no changes, False if changes exist.
    """
    # Check for modified or staged files
    result = subprocess.run(
        ['git', 'diff-index', '--quiet', 'HEAD', '--'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    has_changes = result.returncode != 0
    
    # Check for untracked files
    result = subprocess.run(
        ['git', 'ls-files', '--others', '--exclude-standard'],
        capture_output=True,
        text=True
    )
    if result.stdout.strip():
        has_changes = True
    
    if has_changes:
        print_error("There are uncommitted changes in the repository.")
        print_error("Please commit or stash your changes before proceeding.")
        print("")
        print_info("Uncommitted changes:")
        subprocess.run(['git', 'status', '--short'])
        return False
    
    debug_print("No uncommitted changes found")
    return True


def stash_changes() -> bool:
    """
    Stash uncommitted changes with timestamp.
    Returns True on success, False on failure.
    """
    from datetime import datetime
    
    print_step("Stashing uncommitted changes...")
    
    # Check if there are any changes to stash
    result = subprocess.run(
        ['git', 'diff-index', '--quiet', 'HEAD', '--'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    has_modified = result.returncode != 0
    
    # Check for untracked files
    result = subprocess.run(
        ['git', 'ls-files', '--others', '--exclude-standard'],
        capture_output=True,
        text=True
    )
    has_untracked = bool(result.stdout.strip())
    
    if not has_modified and not has_untracked:
        print_info("No uncommitted changes to stash")
        return True
    
    # Create stash with timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    stash_message = f"RDD auto-stash {timestamp}"
    
    result = subprocess.run(
        ['git', 'stash', 'push', '-u', '-m', stash_message],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print_success("Changes stashed successfully")
        debug_print(f"Stash message: {stash_message}")
        return True
    else:
        print_error("Failed to stash changes")
        if result.stderr:
            print(result.stderr)
        return False


def restore_stashed_changes() -> int:
    """
    Restore stashed changes (most recent RDD auto-stash).
    Returns: 0 on success, 1 on failure, 2 if no stash found.
    """
    print_step("Restoring stashed changes...")
    
    # Get stash list
    result = subprocess.run(
        ['git', 'stash', 'list'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print_warning("Failed to list stashes")
        return 1
    
    # Find the first RDD auto-stash
    stash_lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
    stash_index = None
    
    for i, line in enumerate(stash_lines):
        if 'RDD auto-stash' in line:
            # Extract stash reference (e.g., "stash@{0}")
            stash_ref = line.split(':')[0].strip()
            stash_index = stash_ref
            break
    
    if not stash_index:
        print_warning("No RDD auto-stash found")
        return 2
    
    # Pop the specific RDD auto-stash
    result = subprocess.run(
        ['git', 'stash', 'pop', stash_index],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print_success("Stashed changes restored successfully")
        return 0
    else:
        print_error("Failed to restore stashed changes")
        print_warning("Changes are still in stash. Use 'git stash list' to see stashes and 'git stash pop' manually.")
        if result.stderr:
            print(result.stderr)
        return 1


def pull_main() -> bool:
    """
    Pull latest changes from default branch.
    In local-only mode, skips remote operations.
    Returns True on success, False on failure.
    """
    default_branch = get_default_branch()
    
    # Check if we're in local-only mode
    if is_local_only_mode():
        print_info(f"Local-only mode: Skipping remote fetch from origin/{default_branch}")
        print_success(f"Using local {default_branch} branch (no remote sync)")
        return True
    
    print_step(f"Pulling latest changes from origin/{default_branch}...")
    
    # First fetch from origin
    result = subprocess.run(
        ['git', 'fetch', 'origin', default_branch, '--quiet'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode != 0:
        print_error(f"Failed to fetch from origin/{default_branch}")
        return False
    
    # Check if local default branch exists
    result = subprocess.run(
        ['git', 'show-ref', '--verify', '--quiet', f'refs/heads/{default_branch}'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode != 0:
        # Local branch doesn't exist, create it from origin
        result = subprocess.run(
            ['git', 'branch', default_branch, f'origin/{default_branch}'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        if result.returncode == 0:
            print_success(f"Created local {default_branch} branch from origin")
            return True
        else:
            print_error(f"Failed to create local {default_branch} branch")
            return False
    
    # Try to update local main branch reference (fast-forward only)
    current_branch = get_current_branch()
    if current_branch != default_branch:
        # We're not on main, try to fast-forward the local main branch
        result = subprocess.run(
            ['git', 'fetch', 'origin', f'{default_branch}:{default_branch}'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        if result.returncode == 0:
            print_success(f"Updated local {default_branch} branch")
            return True
        else:
            # Fast-forward failed, probably because of local commits or conflicts
            # Just ensure we have the latest from origin
            print_success(f"Fetched latest from origin/{default_branch}")
            debug_print(f"Could not fast-forward local {default_branch} (may have local commits)")
            return True
    else:
        # We're on main, do a regular pull
        result = subprocess.run(
            ['git', 'pull', 'origin', default_branch],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success(f"Successfully pulled latest {default_branch}")
            return True
        else:
            print_error(f"Failed to pull from origin/{default_branch}")
            if result.stderr:
                print(result.stderr)
            return False


def merge_main_into_current() -> bool:
    """
    Merge default branch into current branch.
    Returns True on success, False on failure (including conflicts).
    """
    default_branch = get_default_branch()
    current_branch = get_current_branch()
    
    # Safety check: don't merge if we're on main
    if current_branch == default_branch:
        print_error(f"Cannot merge {default_branch} into itself")
        return False
    
    print_step(f"Merging {default_branch} into {current_branch}...")
    
    # Attempt merge
    result = subprocess.run(
        ['git', 'merge', default_branch, '--no-edit'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print_success(f"Successfully merged {default_branch} into {current_branch}")
        return True
    else:
        # Check if it's a conflict using reliable programmatic output
        result = subprocess.run(
            ['git', 'ls-files', '-u'],
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            print_error("Merge conflicts detected!")
            print("")
            print_warning("Conflicts found in:")
            
            # Get unique file paths from unmerged files
            conflict_files = set()
            for line in result.stdout.strip().split('\n'):
                if line:
                    # Format: <mode> <hash> <stage> <file>
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        conflict_files.add(parts[1])
            
            for file in sorted(conflict_files):
                print(f"  - {file}")
            
            print("")
            print_info("Please resolve conflicts manually:")
            print("  1. Edit conflicted files")
            print("  2. Stage resolved files: git add <file>")
            print("  3. Complete merge: git commit")
            print("")
            return False
        else:
            print_error("Merge failed for unknown reason")
            if result.stderr:
                print(result.stderr)
            return False


def update_from_main() -> bool:
    """
    Update current branch from main (full workflow).
    Stashes changes, pulls main, merges, and restores stash.
    Returns True on success, False on failure.
    """
    default_branch = get_default_branch()
    current_branch = get_current_branch()
    
    print_banner(f"Update Branch from {default_branch}")
    print("")
    print_info(f"Current branch: {current_branch}")
    print_info(f"Target: {default_branch}")
    print("")
    
    # Safety check: don't run on main
    if current_branch == default_branch:
        print_error(f"Cannot update {default_branch} from itself")
        print_info(f"This command is meant to update feature branches with latest {default_branch}")
        return False
    
    # Step 1: Stash changes
    if not stash_changes():
        print_error("Failed to stash changes. Aborting.")
        return False
    
    # Step 2: Pull latest main
    if not pull_main():
        print_error(f"Failed to pull latest {default_branch}. Aborting.")
        # Try to restore stash
        restore_result = restore_stashed_changes()
        if restore_result != 0:
            print_error("Also failed to restore stashed changes")
            print_warning("Your changes are safely in the stash. Run 'git stash list' to see them.")
        return False
    
    # Step 3: Merge main into current branch
    if not merge_main_into_current():
        print_error("Merge failed. Please resolve conflicts manually.")
        print_warning("Your changes are still stashed. After resolving conflicts:")
        print("  1. Complete the merge: git commit")
        print("  2. Restore your changes: git stash pop")
        return False
    
    # Step 4: Restore stashed changes
    restore_result = restore_stashed_changes()
    
    if restore_result == 0:
        print("")
        print_banner("Update Complete")
        print_success(f"Branch updated from {default_branch}")
        print_success("Local changes restored (uncommitted)")
        return True
    elif restore_result == 2:
        print("")
        print_banner("Update Complete")
        print_success(f"Branch updated from {default_branch}")
        print_info("No stashed changes to restore")
        return True
    else:
        print("")
        print_warning("Update complete but failed to restore stash")
        print_info("Your changes are still in stash. Restore manually with:")
        print("  git stash pop")
        return False


# ============================================================================
# USER INTERACTION
# ============================================================================

def confirm_action(prompt: str) -> bool:
    """
    Confirm action with user.
    Returns True if yes, False if no.
    """
    try:
        response = input(f"{Colors.YELLOW}{prompt} [y/N]: {Colors.NC}").strip().lower()
        return response in ['y', 'yes']
    except (KeyboardInterrupt, EOFError):
        print()
        return False


# ============================================================================
# ERROR HANDLING
# ============================================================================

def exit_with_error(message: str, code: int = 1) -> None:
    """Exit with error message."""
    print_error(message)
    sys.exit(code)


def check_status(status: int, error_msg: str = "Command failed") -> None:
    """Check exit status and exit with error if non-zero."""
    if status != 0:
        exit_with_error(error_msg, status)


# ============================================================================
# CONFIGURATION FILE HELPERS
# ============================================================================

def find_change_config(workspace_dir: str = ".rdd-docs/workspace") -> Optional[str]:
    """
    Find the change config file in workspace.
    Returns path to config file or None if not found.
    """
    if not os.path.isdir(workspace_dir):
        return None
    
    # Look for .rdd.fix.* or .rdd.enh.* files
    for file in os.listdir(workspace_dir):
        if file.startswith('.rdd.fix.') or file.startswith('.rdd.enh.'):
            config_path = os.path.join(workspace_dir, file)
            if os.path.isfile(config_path):
                return config_path
    
    return None


def get_config(key: str, config_file: Optional[str] = None) -> Optional[str]:
    """
    Get configuration value from config file.
    Returns configuration value or None if not found.
    """
    # If no config file specified, try to find it
    if not config_file:
        config_file = find_change_config(".rdd-docs/workspace")
        if not config_file:
            return None
    
    if not os.path.isfile(config_file):
        return None
    
    try:
        with open(config_file, 'r') as f:
            if config_file.endswith('.json'):
                data = json.load(f)
                return data.get(key)
            else:
                # Fallback: simple grep for key-value pairs
                content = f.read()
                match = re.search(rf'"{key}"\s*:\s*"([^"]*)"', content)
                if match:
                    return match.group(1)
    except Exception:
        pass
    
    return None


def set_config(key: str, value: str, config_file: Optional[str] = None) -> bool:
    """
    Set configuration value in config file.
    Returns True if successful, False if failed.
    """
    if not key or not value:
        print_error("Key and value are required for set_config")
        return False
    
    # If no config file specified, try to find it
    if not config_file:
        config_file = find_change_config(".rdd-docs/workspace")
        if not config_file:
            print_error("No change config file found")
            return False
    
    # Create config file if it doesn't exist
    if not os.path.isfile(config_file):
        with open(config_file, 'w') as f:
            json.dump({}, f)
    
    try:
        if config_file.endswith('.json'):
            # Read existing data or create empty dict
            if os.path.isfile(config_file) and os.path.getsize(config_file) > 0:
                with open(config_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {}
            
            data[key] = value
            
            with open(config_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        else:
            print_warning(f"Non-JSON config file. Manual editing required for: {key}={value}")
            return False
    except Exception as e:
        print_error(f"Failed to set config: {e}")
        return False


def get_rdd_config_path() -> str:
    """
    Get the path to the RDD configuration file.
    Returns: Path to .rdd-docs/config.json
    """
    return os.path.join(get_repo_root(), ".rdd-docs", "config.json")


def get_rdd_config(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get value from global RDD config file (.rdd-docs/config.json).
    Returns value or default if not found.
    """
    config_path = get_rdd_config_path()
    
    if not os.path.isfile(config_path):
        return default
    
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
            return data.get(key, default)
    except Exception:
        return default


def set_rdd_config(key: str, value: str) -> bool:
    """
    Set value in global RDD config file (.rdd-docs/config.json).
    Creates file if it doesn't exist.
    Returns True if successful, False otherwise.
    """
    config_path = get_rdd_config_path()
    
    # Create .rdd-docs directory if needed
    rdd_docs_dir = os.path.dirname(config_path)
    if not os.path.isdir(rdd_docs_dir):
        try:
            os.makedirs(rdd_docs_dir, exist_ok=True)
        except Exception as e:
            print_error(f"Failed to create .rdd-docs directory: {e}")
            return False
    
    # Load existing config or create new
    if os.path.isfile(config_path):
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
        except Exception:
            data = {}
    else:
        from datetime import datetime, timezone
        data = {
            "version": "1.0.0",
            "created": datetime.now(timezone.utc).isoformat()
        }
    
    # Update value and timestamp
    from datetime import datetime, timezone
    data[key] = value
    data["lastModified"] = datetime.now(timezone.utc).isoformat()
    
    # Write back
    try:
        with open(config_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print_error(f"Failed to write config: {e}")
        return False


def is_local_only_mode() -> bool:
    """
    Check if the repository is configured for local-only mode (no GitHub remote).
    Returns True if localOnly is set to true in config.json, False otherwise.
    """
    local_only = get_rdd_config("localOnly", "false")
    # Handle both string and boolean values
    if isinstance(local_only, bool):
        return local_only
    return str(local_only).lower() in ['true', '1', 'yes']


# ============================================================================
# HELP MESSAGE GENERATION
# ============================================================================

def help_section(title: str, description: str = "") -> None:
    """Generate a formatted help section."""
    print(f"{Colors.CYAN}{Colors.BOLD}{title}{Colors.NC}")
    if description:
        print(f"  {description}")
    print()


def help_command(command: str, description: str, example: str = "") -> None:
    """Generate a help command entry."""
    print(f"  {Colors.GREEN}{command}{Colors.NC}")
    print(f"      {description}")
    if example:
        print(f"      {Colors.BLUE}Example: {example}{Colors.NC}")
    print()


def help_option(option: str, description: str) -> None:
    """Generate a help option entry."""
    print(f"  {Colors.YELLOW}{option}{Colors.NC}")
    print(f"      {description}")
    print()


# ============================================================================
# PROMPT MANAGEMENT FUNCTIONS
# ============================================================================

def mark_prompt_completed(prompt_id: str, journal_file: str = None) -> bool:
    """
    Mark a stand-alone prompt as completed in .rdd.copilot-prompts.md.
    Changes checkbox from "- [ ]" to "- [x]".
    
    Args:
        prompt_id: The ID of the prompt (e.g., P01, P02, P001)
        journal_file: Path to .rdd.copilot-prompts.md (optional, defaults to workspace file)
    
    Returns:
        True on success, False on error
    """
    import re
    
    if not journal_file:
        journal_file = os.path.join(".rdd-docs/workspace", ".rdd.copilot-prompts.md")
    
    # Validate prompt ID is provided
    if not prompt_id:
        print_error("Prompt ID is required")
        return False
    
    # Check if journal file exists
    if not os.path.isfile(journal_file):
        print_error(f".rdd.copilot-prompts.md not found at: {journal_file}")
        return False
    
    # Read the file
    try:
        with open(journal_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print_error(f"Failed to read file: {e}")
        return False
    
    # Check if the prompt exists and is not already completed
    unchecked_pattern = rf'^\s*-\s*\[\s*\]\s*\[{re.escape(prompt_id)}\]'
    checked_pattern = rf'^\s*-\s*\[x\]\s*\[{re.escape(prompt_id)}\]'
    
    if not re.search(unchecked_pattern, content, re.MULTILINE):
        if re.search(checked_pattern, content, re.MULTILINE):
            print_warning(f"Prompt {prompt_id} is already marked as completed")
            return True
        else:
            print_error(f"Prompt {prompt_id} not found in .rdd.copilot-prompts.md")
            return False
    
    # Mark the prompt as completed
    # This will change "- [ ] [PROMPT_ID]" to "- [x] [PROMPT_ID]"
    new_content = re.sub(
        rf'(^\s*-\s*)\[\s*\](\s*\[{re.escape(prompt_id)}\])',
        r'\1[x]\2',
        content,
        flags=re.MULTILINE
    )
    
    # Write back to file
    try:
        with open(journal_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print_success(f"Marked prompt {prompt_id} as completed")
        return True
    except Exception as e:
        print_error(f"Failed to mark prompt {prompt_id} as completed: {e}")
        return False


def log_prompt_execution(prompt_id: str, execution_details: str, session_id: str = None) -> bool:
    """
    Log prompt execution details to log.jsonl.
    Creates a structured JSONL entry with timestamp, promptId, executionDetails, sessionId.
    
    Args:
        prompt_id: The ID of the executed prompt (e.g., P01, P02)
        execution_details: Full content describing what was executed
        session_id: Optional session identifier (defaults to exec-YYYYMMDD-HHmm)
    
    Returns:
        True on success, False on error
    
    Format:
        {"timestamp":"2025-11-05T10:30:00Z","promptId":"P01","executionDetails":"...","sessionId":"exec-20251105-1030"}
    """
    from datetime import datetime
    
    workspace_dir = ".rdd-docs/workspace"
    log_file = os.path.join(workspace_dir, "log.jsonl")
    
    # Validate required parameters
    if not prompt_id:
        print_error("Prompt ID is required for logging")
        return False
    
    if not execution_details:
        print_error("Execution details are required for logging")
        return False
    
    # Default session ID if not provided
    if not session_id:
        session_id = f"exec-{datetime.now().strftime('%Y%m%d-%H%M')}"
    
    # Ensure workspace directory exists
    os.makedirs(workspace_dir, exist_ok=True)
    
    # Create log file if it doesn't exist
    if not os.path.isfile(log_file):
        open(log_file, 'a').close()
        debug_print(f"Created log file: {log_file}")
    
    # Create JSON line entry
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    log_entry = {
        "timestamp": timestamp,
        "promptId": prompt_id,
        "executionDetails": execution_details,
        "sessionId": session_id
    }
    
    # Write to log file
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
        print_success(f"Logged execution details for prompt {prompt_id} to {log_file}")
        return True
    except Exception as e:
        print_error(f"Failed to log execution: {e}")
        return False


def list_prompts(status: str = "all", journal_file: str = None) -> bool:
    """
    List prompts from .rdd.copilot-prompts.md filtered by status.
    
    Args:
        status: Filter by status ('unchecked', 'checked', 'all')
        journal_file: Path to .rdd.copilot-prompts.md (optional, defaults to workspace file)
    
    Returns:
        True on success, False on error
    """
    import re
    
    if not journal_file:
        journal_file = os.path.join(".rdd-docs/workspace", ".rdd.copilot-prompts.md")
    
    # Validate status parameter
    if status not in ['unchecked', 'checked', 'all']:
        print_error(f"Invalid status filter: '{status}'")
        print("Valid options: unchecked, checked, all")
        return False
    
    # Check if journal file exists
    if not os.path.isfile(journal_file):
        print_error(f".rdd.copilot-prompts.md not found at: {journal_file}")
        return False
    
    # Print header
    print_banner(f"PROMPTS LIST ({status})")
    
    # Read file and filter
    try:
        with open(journal_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print_error(f"Failed to read file: {e}")
        return False
    
    # Patterns for matching prompts
    unchecked_pattern = re.compile(r'^\s*-\s*\[\s*\]\s*\[([P][0-9]+)\]\s*(.*)$')
    checked_pattern = re.compile(r'^\s*-\s*\[x\]\s*\[([P][0-9]+)\]\s*(.*)$')
    
    total_count = 0
    checked_count = 0
    unchecked_count = 0
    
    for line in lines:
        # Try unchecked pattern
        match = unchecked_pattern.match(line)
        if match:
            total_count += 1
            unchecked_count += 1
            if status in ['unchecked', 'all']:
                prompt_id = match.group(1)
                prompt_title = match.group(2).strip()[:80]
                print(f"  ☐ [{prompt_id}] {prompt_title}")
            continue
        
        # Try checked pattern
        match = checked_pattern.match(line)
        if match:
            total_count += 1
            checked_count += 1
            if status in ['checked', 'all']:
                prompt_id = match.group(1)
                prompt_title = match.group(2).strip()[:80]
                print(f"  ☑ [{prompt_id}] {prompt_title}")
    
    # Print summary
    print()
    print_info(f"Summary: {checked_count} completed, {unchecked_count} pending, {total_count} total")
    
    return True


def validate_prompt_status(prompt_id: str, journal_file: str = None) -> int:
    """
    Validate prompt status in copilot-prompts.md.
    Checks if a prompt exists and returns its status.
    
    Args:
        prompt_id: The ID of the prompt to check (e.g., P01, P02)
        journal_file: Path to copilot-prompts.md (optional, defaults to workspace file)
    
    Returns:
        0 if prompt exists and is unchecked
        1 if prompt exists and is checked
        2 if prompt does not exist
        3 if journal file not found
    """
    import re
    
    if not journal_file:
        journal_file = os.path.join(".rdd-docs/workspace", ".rdd.copilot-prompts.md")
    
    # Validate prompt ID is provided
    if not prompt_id:
        print_error("Prompt ID is required")
        return 3
    
    # Check if journal file exists
    if not os.path.isfile(journal_file):
        print_error(f".rdd.copilot-prompts.md not found at: {journal_file}")
        return 3
    
    # Read file
    try:
        with open(journal_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print_error(f"Failed to read file: {e}")
        return 3
    
    # Check if prompt exists and get its status
    unchecked_pattern = rf'^\s*-\s*\[\s*\]\s*\[{re.escape(prompt_id)}\]'
    checked_pattern = rf'^\s*-\s*\[x\]\s*\[{re.escape(prompt_id)}\]'
    
    if re.search(unchecked_pattern, content, re.MULTILINE):
        print_info(f"Prompt {prompt_id} exists and is unchecked (pending)")
        return 0
    elif re.search(checked_pattern, content, re.MULTILINE):
        print_info(f"Prompt {prompt_id} exists and is checked (completed)")
        return 1
    else:
        print_warning(f"Prompt {prompt_id} not found in copilot-prompts.md")
        return 2


if __name__ == '__main__':
    # Test the module when run directly
    print_banner("RDD Utils Test", "Testing utility functions")
    print()
    print_success("Success message test")
    print_error("Error message test")
    print_warning("Warning message test")
    print_info("Info message test")
    print_step("Step message test")
    print()
    
    test_name = "my-test-name"
    if validate_name(test_name):
        print_success(f"'{test_name}' is valid")
    
    print()
    normalized = normalize_to_kebab_case("Add User Auth")
    if normalized:
        print_success(f"Normalized: 'Add User Auth' -> '{normalized}'")
