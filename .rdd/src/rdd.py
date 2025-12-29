#!/usr/bin/env python3
"""RDD Framework CLI - Main Command Router.

This module provides the main entry point for the RDD (Requirements-Driven Development)
framework command-line interface. It implements a domain-based command routing architecture
with support for interactive menus and direct command execution.

Domains:
  - prompt: Operations related to prompt management (create, set-state, list)
  - workdir: Operations related to working directory management (new-setup, archive)
  - git: Operations related to version control (commit)

Usage:
  python rdd.py                    # Interactive menu mode
  python rdd.py <domain>           # Domain-specific menu
  python rdd.py <domain> <action>  # Direct action execution

Examples:
  python rdd.py                         # Show main menu
  python rdd.py prompt                  # Show prompt domain menu
  python rdd.py prompt create           # Create a new prompt
  python rdd.py workdir new-setup       # Setup new work iteration
  python rdd.py git commit              # Commit changes for active prompt
"""

from __future__ import annotations

import sys
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any


def _repo_root() -> Path:
    """Get the repository root directory.
    
    Returns:
        Path: Absolute path to the repository root.
    """
    # This file lives at: <repo>/.rdd/src/rdd.py
    return Path(__file__).resolve().parents[2]


def _actions_dir() -> Path:
    """Get the actions directory path.
    
    Returns:
        Path: Absolute path to the .rdd/src/actions directory.
    """
    return _repo_root() / ".rdd" / "src" / "actions"


def _get_python_cmd() -> str:
    """Get the python command to use for cross-platform compatibility.
    
    Returns:
        str: The python command ('python').
    """
    return "python"


def _try_curses_menu(title: str, options: List[Dict[str, str]]) -> Optional[str]:
    """Try to display an interactive curses menu.
    
    Args:
        title: Menu title to display.
        options: List of menu options, each with 'key' and 'desc' fields.
        
    Returns:
        Selected option key if successful, None if curses is unavailable.
    """
    try:
        import curses
        
        def menu(stdscr):
            """Curses menu display function."""
            curses.curs_set(0)  # Hide cursor
            current = 0
            
            while True:
                stdscr.clear()
                h, w = stdscr.getmaxyx()
                
                # Display title
                stdscr.addstr(0, 0, title, curses.A_BOLD)
                stdscr.addstr(1, 0, "=" * min(len(title), w - 1))
                
                # Display options
                for idx, opt in enumerate(options):
                    y = idx + 3
                    if y >= h - 1:
                        break
                    
                    line = f"{idx + 1}. {opt['desc']}"
                    if idx == current:
                        stdscr.addstr(y, 0, line, curses.A_REVERSE)
                    else:
                        stdscr.addstr(y, 0, line)
                
                # Display instructions
                if len(options) + 4 < h:
                    stdscr.addstr(h - 2, 0, "Arrow keys to navigate, Enter to select, Q to quit", curses.A_DIM)
                
                stdscr.refresh()
                
                # Handle input
                key = stdscr.getch()
                
                if key == curses.KEY_UP and current > 0:
                    current -= 1
                elif key == curses.KEY_DOWN and current < len(options) - 1:
                    current += 1
                elif key in (curses.KEY_ENTER, 10, 13):  # Enter key
                    return options[current]['key']
                elif key in (ord('q'), ord('Q')):
                    return None
        
        result = curses.wrapper(menu)
        return result
        
    except (ImportError, Exception):
        # Curses not available or error occurred
        return None


def _numeric_menu(title: str, options: List[Dict[str, str]]) -> Optional[str]:
    """Display a numeric fallback menu.
    
    Args:
        title: Menu title to display.
        options: List of menu options, each with 'key' and 'desc' fields.
        
    Returns:
        Selected option key, or None if user quits.
    """
    print()
    print(title)
    print("=" * len(title))
    print()
    
    for idx, opt in enumerate(options, 1):
        print(f"{idx}. {opt['desc']}")
    
    print()
    print("Enter option number (or 'q' to quit):")
    
    while True:
        try:
            choice = input("> ").strip().lower()
            
            if choice == 'q':
                return None
            
            idx = int(choice)
            if 1 <= idx <= len(options):
                return options[idx - 1]['key']
            else:
                print(f"Invalid option. Please enter 1-{len(options)} or 'q':")
        
        except ValueError:
            print(f"Invalid input. Please enter 1-{len(options)} or 'q':")
        except (EOFError, KeyboardInterrupt):
            print()
            return None


def _show_menu(title: str, options: List[Dict[str, str]]) -> Optional[str]:
    """Display an interactive menu with curses or numeric fallback.
    
    Args:
        title: Menu title to display.
        options: List of menu options, each with 'key' and 'desc' fields.
        
    Returns:
        Selected option key, or None if user quits.
    """
    # Try curses first
    result = _try_curses_menu(title, options)
    
    # Fall back to numeric menu if curses unavailable
    if result is None and sys.stdout.isatty():
        result = _numeric_menu(title, options)
    
    return result


def _prompt_for_parameters(action_key: str) -> List[str]:
    """Prompt user for parameters required by an action.
    
    Args:
        action_key: The action identifier in format 'domain.action'.
        
    Returns:
        List of parameter strings in format 'key=value'.
    """
    # Define parameter specifications for each action
    param_specs = {
        "prompt.create": [
            {"name": "title", "prompt": "Enter prompt title", "required": True},
            {"name": "type", "prompt": "Enter prompt type (main/modification)", "required": True, "default": "main"},
        ],
        "prompt.set-state": [
            {"name": "state", "prompt": "Enter new state (draft/planned/in-progress/completed)", "required": True},
            {"name": "prompt-id", "prompt": "Enter prompt ID (or leave empty for active prompt)", "required": False},
        ],
        "workdir.new-setup": [
            {"name": "name", "prompt": "Enter iteration name", "required": True},
        ],
    }
    
    specs = param_specs.get(action_key, [])
    if not specs:
        return []
    
    print()
    print("Action Parameters")
    print("=" * 17)
    print()
    
    params = []
    
    for spec in specs:
        param_name = spec["name"]
        param_prompt = spec["prompt"]
        required = spec.get("required", False)
        default = spec.get("default")
        
        prompt_text = f"{param_prompt}"
        if default:
            prompt_text += f" [default: {default}]"
        if not required:
            prompt_text += " (optional)"
        prompt_text += ": "
        
        while True:
            try:
                value = input(prompt_text).strip()
                
                # Use default if provided and user input is empty
                if not value and default:
                    value = default
                
                # Validate required fields
                if required and not value:
                    print(f"Error: {param_name} is required. Please provide a value.")
                    continue
                
                # Add to params if value provided
                if value:
                    params.append(f"{param_name}={value}")
                
                break
                
            except (EOFError, KeyboardInterrupt):
                print()
                print("Parameter input cancelled.")
                return []
    
    print()
    return params


def _execute_action(domain: str, action: str, args: List[str]) -> int:
    """Execute a domain action script.
    
    Args:
        domain: Domain name (e.g., 'prompt', 'workdir').
        action: Action name (e.g., 'create', 'set-state').
        args: Additional arguments to pass to the action script.
        
    Returns:
        Exit code from the action script.
    """
    # Map domain/action to script name
    script_name = f"{domain}_{action.replace('-', '_')}.py"
    script_path = _actions_dir() / script_name
    
    if not script_path.exists():
        print(f"Error: Action script not found: {script_path}", file=sys.stderr)
        print(f"Remediation: Ensure the action '{action}' exists for domain '{domain}'", file=sys.stderr)
        return 1
    
    # Build command
    cmd = [_get_python_cmd(), str(script_path)] + args
    
    try:
        result = subprocess.run(cmd, cwd=_repo_root())
        return result.returncode
    
    except FileNotFoundError:
        print(f"Error: Python interpreter not found", file=sys.stderr)
        print(f"Remediation: Ensure 'python' command is available in PATH", file=sys.stderr)
        return 1
    
    except Exception as e:
        print(f"Error: Failed to execute action: {e}", file=sys.stderr)
        print(f"Remediation: Check script permissions and Python installation", file=sys.stderr)
        return 1


def _prompt_domain_menu() -> int:
    """Show prompt domain menu and execute selected action.
    
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    options = [
        {"key": "create", "desc": "Create a new prompt"},
        {"key": "set-state", "desc": "Change prompt state"},
        {"key": "list", "desc": "List all prompts"},
    ]
    
    choice = _show_menu("RDD - Prompt Domain", options)
    
    if choice is None:
        return 0
    
    # Prompt for parameters if needed
    action_key = f"prompt.{choice}"
    params = _prompt_for_parameters(action_key)
    
    # Check if parameter gathering was cancelled
    if action_key in ["prompt.create", "prompt.set-state"] and not params:
        print("Action cancelled.")
        return 0
    
    return _execute_action("prompt", choice, params)


def _workdir_domain_menu() -> int:
    """Show workdir domain menu and execute selected action.
    
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    options = [
        {"key": "new-setup", "desc": "Setup new work iteration"},
        {"key": "archive", "desc": "Archive current work iteration"},
    ]
    
    choice = _show_menu("RDD - Workdir Domain", options)
    
    if choice is None:
        return 0
    
    # Prompt for parameters if needed
    action_key = f"workdir.{choice}"
    params = _prompt_for_parameters(action_key)
    
    # Check if parameter gathering was cancelled
    if action_key == "workdir.new-setup" and not params:
        print("Action cancelled.")
        return 0
    
    return _execute_action("workdir", choice, params)


def _git_domain_menu() -> int:
    """Show git domain menu and execute selected action.
    
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    options = [
        {"key": "commit", "desc": "Commit changes for active prompt"},
    ]
    
    choice = _show_menu("RDD - Git Domain", options)
    
    if choice is None:
        return 0
    
    return _execute_action("git", choice, [])


def _main_menu() -> int:
    """Show main domain menu and route to selected domain.
    
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    options = [
        {"key": "prompt", "desc": "Prompt management (create, set-state, list)"},
        {"key": "workdir", "desc": "Working directory management (new-setup, archive)"},
        {"key": "git", "desc": "Version control operations (commit)"},
    ]
    
    choice = _show_menu("RDD Framework - Main Menu", options)
    
    if choice is None:
        return 0
    
    if choice == "prompt":
        return _prompt_domain_menu()
    elif choice == "workdir":
        return _workdir_domain_menu()
    elif choice == "git":
        return _git_domain_menu()
    
    return 0


def _show_help() -> None:
    """Display help information."""
    print(__doc__)


def main(argv: List[str]) -> int:
    """Main entry point for the RDD CLI.
    
    Args:
        argv: Command-line arguments (excluding program name).
        
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    # Handle help flags
    if any(arg in ("-h", "--help", "help") for arg in argv):
        _show_help()
        return 0
    
    # No arguments: show main menu
    if len(argv) == 0:
        return _main_menu()
    
    # Single argument: domain menu
    if len(argv) == 1:
        domain = argv[0]
        
        if domain == "prompt":
            return _prompt_domain_menu()
        elif domain == "workdir":
            return _workdir_domain_menu()
        elif domain == "git":
            return _git_domain_menu()
        else:
            print(f"Error: Unknown domain '{domain}'", file=sys.stderr)
            print(f"Remediation: Valid domains are 'prompt', 'workdir', and 'git'. Use --help for more info.", file=sys.stderr)
            return 1
    
    # Two or more arguments: direct action execution
    domain = argv[0]
    action = argv[1]
    args = argv[2:]
    
    if domain not in ("prompt", "workdir", "git"):
        print(f"Error: Unknown domain '{domain}'", file=sys.stderr)
        print(f"Remediation: Valid domains are 'prompt', 'workdir', and 'git'. Use --help for more info.", file=sys.stderr)
        return 1
    
    return _execute_action(domain, action, args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
