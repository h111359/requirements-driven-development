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
from datetime import datetime
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
    """Print error message with red X."""
    print(f"{Colors.RED}✗ {message}{Colors.NC}")


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
    Validate branch name format: {type}/{timestamp}-{name}.
    Where type is enh or fix.
    Returns True if valid, False if invalid.
    """
    if not branch_name:
        print_error("Branch name cannot be empty")
        return False
    
    # Check format: {type}/{timestamp}-{name}
    if not re.match(r'^(enh|fix)/[0-9]{8}-[0-9]{4}-.+$', branch_name):
        print_error(f"Invalid branch name format: '{branch_name}'")
        print_error("Expected format: {enh|fix}/{YYYYMMDD-HHmm}-{name}")
        print_error("Example: enh/20231101-1234-my-enhancement")
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
    Handles various inputs: "Add User Auth", "fix_login_bug", "update-README"
    Returns kebab-case string or None on failure.
    """
    if not input_str:
        return None
    
    # Normalization steps:
    # 1. Convert to lowercase
    # 2. Replace underscores and spaces with hyphens
    # 3. Remove any characters that aren't lowercase letters, numbers, or hyphens
    # 4. Replace multiple consecutive hyphens with single hyphen
    # 5. Remove leading and trailing hyphens
    
    normalized = input_str.lower()
    normalized = normalized.replace('_', '-').replace(' ', '-')
    normalized = re.sub(r'[^a-z0-9-]', '', normalized)
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
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


def get_timestamp_filename() -> str:
    """Get timestamp for filenames (no special characters, e.g., 20231101-1234)."""
    return datetime.now().strftime('%Y%m%d-%H%M')


# ============================================================================
# GIT REPOSITORY CHECKS
# ============================================================================

def check_git_repo() -> bool:
    """
    Check if we're in a git repository.
    Returns True if in git repo, exits with error if not.
    """
    result = subprocess.run(
        ['git', 'rev-parse', '--is-inside-work-tree'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode != 0:
        print_error("Not a git repository. Please run this from within a git repository.")
        sys.exit(1)
    
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


def get_default_branch() -> str:
    """
    Get the default branch name (main or master).
    Returns "main" or "master" depending on what exists.
    """
    # Check if main branch exists
    result = subprocess.run(
        ['git', 'show-ref', '--verify', '--quiet', 'refs/heads/main'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode == 0:
        return "main"
    
    # Check if master branch exists
    result = subprocess.run(
        ['git', 'show-ref', '--verify', '--quiet', 'refs/heads/master'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode == 0:
        return "master"
    
    return "main"  # Default to main


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
