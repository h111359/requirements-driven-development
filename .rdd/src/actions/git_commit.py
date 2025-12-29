#!/usr/bin/env python3
"""Create a git commit for the current active prompt.

Behavior:
  - Reads the active prompt from work-iteration-registry.json
  - Constructs commit message: iteration-id_prompt-id_prompt-title
  - Auto-stages all changes (git add -A)
  - Validates that changes exist before committing
  - Creates a git commit with the constructed message

This script is intentionally deterministic and non-interactive.

Usage:
  git_commit.py

Examples:
  python .rdd/src/actions/git_commit.py

Output:
  Prints status messages to stdout.
  Errors are printed to stderr.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def _repo_root() -> Path:
    """Get the repository root directory.
    
    Returns:
        Path: Absolute path to the repository root.
    """
    # This file lives at: <repo>/.rdd/src/actions/git_commit.py
    return Path(__file__).resolve().parents[3]


def _load_json(path: Path) -> Dict[str, Any]:
    """Load and parse a JSON file.
    
    Args:
        path: Path to the JSON file.
        
    Returns:
        Parsed JSON data as a dictionary.
        
    Raises:
        ValueError: If the JSON file doesn't contain an object.
    """
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Registry JSON must be an object: {path}")
    return data


def _find_active_prompt(prompts: list[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Find the prompt currently in 'planned' or 'in-progress' state.
    
    Args:
        prompts: List of prompt dictionaries from the registry.
        
    Returns:
        The active prompt dictionary, or None if no active prompt found.
    """
    for p in prompts:
        if not isinstance(p, dict):
            continue
        if p.get("state") in {"planned", "in-progress"}:
            return p
    return None


def _run_git_command(args: list[str], repo_root: Path, capture_output: bool = False) -> subprocess.CompletedProcess:
    """Run a git command in the repository root.
    
    Args:
        args: Git command arguments.
        repo_root: Path to the repository root.
        capture_output: Whether to capture stdout/stderr.
        
    Returns:
        CompletedProcess instance with the result.
    """
    return subprocess.run(
        ["git"] + args,
        cwd=repo_root,
        capture_output=capture_output,
        text=True
    )


def _has_changes_to_commit(repo_root: Path) -> bool:
    """Check if there are any changes to commit in the repository.
    
    Args:
        repo_root: Path to the repository root.
        
    Returns:
        True if there are changes (staged or unstaged), False otherwise.
    """
    # Check for unstaged changes
    result = _run_git_command(["status", "--porcelain"], repo_root, capture_output=True)
    
    if result.returncode != 0:
        return False
    
    # If there's any output from git status --porcelain, there are changes
    return bool(result.stdout.strip())


def main() -> int:
    """Main entry point for the git commit action.
    
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    repo_root = _repo_root()
    registry_path = repo_root / ".rdd-instance" / "workdir" / "work-iteration-registry.json"
    
    # Validate registry exists
    if not registry_path.exists():
        print(
            f"ERROR: Work iteration registry not found: {registry_path}",
            file=sys.stderr,
        )
        print(
            "REMEDIATION: Ensure a work iteration has been set up using 'python rdd.py workdir new-setup'",
            file=sys.stderr,
        )
        return 1
    
    # Load registry
    try:
        registry = _load_json(registry_path)
    except Exception as e:
        print(f"ERROR: Failed to load registry: {e}", file=sys.stderr)
        print(f"REMEDIATION: Check that {registry_path} is valid JSON", file=sys.stderr)
        return 1
    
    # Get iteration details
    iteration_id = registry.get("iteration-id")
    if not iteration_id:
        print("ERROR: No iteration-id found in registry", file=sys.stderr)
        print("REMEDIATION: Ensure the work iteration registry is properly initialized", file=sys.stderr)
        return 1
    
    # Find active prompt
    prompts = registry.get("prompts", [])
    active_prompt = _find_active_prompt(prompts)
    
    if not active_prompt:
        print("ERROR: No active prompt found (state must be 'planned' or 'in-progress')", file=sys.stderr)
        print("REMEDIATION: Set a prompt to 'planned' or 'in-progress' state using 'python rdd.py prompt set-state'", file=sys.stderr)
        return 1
    
    # Extract prompt details
    prompt_id = active_prompt.get("prompt-id")
    prompt_title = active_prompt.get("title") or active_prompt.get("prompt-title", "")
    
    if not prompt_id:
        print("ERROR: Active prompt missing prompt-id", file=sys.stderr)
        print("REMEDIATION: Verify the work iteration registry structure", file=sys.stderr)
        return 1
    
    # Construct commit message
    commit_message = f"{iteration_id}_{prompt_id}_{prompt_title}"
    
    print(f"Active prompt: {prompt_id} - {prompt_title}")
    print(f"Iteration: {iteration_id}")
    print(f"Commit message: {commit_message}")
    print()
    
    # Check if there are changes to commit
    if not _has_changes_to_commit(repo_root):
        print("No changes to commit. Working tree is clean.")
        return 0
    
    # Stage all changes
    print("Staging all changes...")
    result = _run_git_command(["add", "-A"], repo_root)
    
    if result.returncode != 0:
        print("ERROR: Failed to stage changes", file=sys.stderr)
        print("REMEDIATION: Check git status and ensure repository is in a valid state", file=sys.stderr)
        return 1
    
    # Create commit
    print("Creating commit...")
    result = _run_git_command(["commit", "-m", commit_message], repo_root)
    
    if result.returncode != 0:
        print("ERROR: Failed to create commit", file=sys.stderr)
        print("REMEDIATION: Check git status and ensure there are staged changes", file=sys.stderr)
        return 1
    
    print()
    print("✓ Commit created successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
