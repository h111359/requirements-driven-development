#!/usr/bin/env python3
"""Complete a prompt by setting its state to 'completed' and optionally executing git commit.

Behavior:
  - Updates the `state` field of a prompt to 'completed' in:
        `.rdd-instance/workdir/work-iteration-registry.json`
  - If the `git-enabled` flag in `.rdd-instance/config/instance-config.json` is true,
    creates a git commit with all changes
  - Commit message format: iteration-id_prompt-id_prompt-title
  - If git commit fails due to no changes, logs a warning but proceeds with state change
  - If `prompt-id=` is omitted, defaults to the currently active prompt.

This script is intentionally deterministic and non-interactive.

Usage (named parameters):
  prompt_complete.py [prompt-id=P-001]

Examples:
  # Complete the active prompt
  prompt_complete.py

  # Complete a specific prompt
  prompt_complete.py prompt-id=P-003

Output:
  Prints the completion status to stdout, including git operation results if applicable.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def _repo_root() -> Path:
    # This file lives at: <repo>/.rdd/src/actions/prompt_complete.py
    return Path(__file__).resolve().parents[3]


def _parse_params(argv: list[str]) -> Dict[str, str]:
    params: Dict[str, str] = {}
    for arg in argv:
        if "=" not in arg:
            continue
        key, value = arg.split("=", 1)
        params[key.strip()] = value
    return params


def _get_param(params: Dict[str, str], *names: str) -> Optional[str]:
    for name in names:
        if name in params:
            return params[name]
    return None


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Registry JSON must be an object: {path}")
    return data


def _dump_json(path: Path, data: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        f.write("\n")


def _find_active_prompt(prompts: list[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Find the prompt currently in 'active' state."""
    for p in prompts:
        if not isinstance(p, dict):
            continue
        if p.get("state") == "active":
            return p
    return None


def main() -> int:
    params = _parse_params(sys.argv[1:])

    # Optional: prompt-id (if omitted, use active prompt)
    prompt_id_raw = _get_param(params, "prompt-id", "prompt_id")

    repo_root = _repo_root()
    workdir = repo_root / ".rdd-instance" / "workdir"
    registry_path = workdir / "work-iteration-registry.json"

    if not registry_path.is_file():
        raise FileNotFoundError(
            f"Work iteration registry not found: {registry_path}\n"
            f"Remediation: Ensure you have initialized a work iteration using the workdir create-iteration command."
        )

    registry = _load_json(registry_path)

    prompts = registry.get("prompts")
    if not isinstance(prompts, list):
        raise ValueError(f"Missing or invalid 'prompts' array in {registry_path}")

    # Determine which prompt to complete
    target_prompt: Optional[Dict[str, Any]] = None

    if prompt_id_raw is not None:
        # Explicit prompt ID provided
        prompt_id = prompt_id_raw.strip()
        for p in prompts:
            if isinstance(p, dict) and p.get("prompt-id") == prompt_id:
                target_prompt = p
                break
        if target_prompt is None:
            raise ValueError(
                f"Prompt not found: {prompt_id}\n"
                f"Remediation: Verify the prompt ID exists in the registry using 'prompt list' command."
            )
    else:
        # Default to active prompt
        target_prompt = _find_active_prompt(prompts)
        if target_prompt is None:
            raise ValueError(
                "No active prompt found (no prompt in 'active' state); "
                "please specify prompt-id= explicitly\n"
                "Remediation: Either specify a prompt-id or set a prompt to 'active' state."
            )

    prompt_id = target_prompt["prompt-id"]
    old_state = target_prompt.get("state")

    # Check if already completed
    if old_state == "completed":
        print(f"{prompt_id} already completed")
        return 0

    # Update the state to completed
    target_prompt["state"] = "completed"

    # Write the updated registry
    _dump_json(registry_path, registry)
    
    # Add prompt to prompts-registry.md
    try:
        add_to_registry_script = repo_root / ".rdd" / "src" / "actions" / "prompt_add_to_registry.py"
        subprocess.run(
            ["python", str(add_to_registry_script), f"prompt-id={prompt_id}"],
            cwd=str(repo_root),
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Added {prompt_id} to prompts-registry.md")
    except subprocess.CalledProcessError as e:
        print(
            f"WARNING: Failed to add prompt to prompts-registry.md: {e.stderr if e.stderr else str(e)}",
            file=sys.stderr,
        )
    except Exception as e:
        print(
            f"WARNING: Error adding prompt to prompts-registry.md: {e}",
            file=sys.stderr,
        )

    # Check git-enabled flag from instance config
    config_path = repo_root / ".rdd-instance" / "config" / "instance-config.json"
    git_enabled = False
    
    try:
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                git_enabled = config.get("git-enabled", False)
        else:
            print(
                "WARNING: Instance configuration file not found. Git operations disabled.",
                file=sys.stderr,
            )
            print(
                f"Expected file: {config_path}",
                file=sys.stderr,
            )
            print(
                "Remediation: Re-run the seed script to create the configuration file.",
                file=sys.stderr,
            )
    except Exception as e:
        print(
            f"WARNING: Failed to read instance configuration: {e}",
            file=sys.stderr,
        )
        print("Git operations disabled.", file=sys.stderr)
    
    git_result = None

    if git_enabled:
        # Execute git commit inline (can't use git_commit.py since we already changed state)
        try:
            # Get iteration details
            iteration_id = registry.get("iteration-id", "UNKNOWN")
            prompt_title = target_prompt.get("prompt-title") or target_prompt.get("title", "UNKNOWN")
            
            # Construct commit message
            commit_message = f"{iteration_id}_{prompt_id}_{prompt_title}"
            
            # Stage all changes
            subprocess.run(
                ["git", "add", "-A"],
                cwd=str(repo_root),
                check=True,
                capture_output=True,
                text=True
            )
            
            # Check if there are changes to commit
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                check=True
            )
            
            if not status_result.stdout.strip():
                git_result = "no-changes"
                print(
                    f"WARNING: Git commit skipped - no changes to commit",
                    file=sys.stderr,
                )
            else:
                # Create commit
                commit_result = subprocess.run(
                    ["git", "commit", "-m", commit_message],
                    cwd=str(repo_root),
                    capture_output=True,
                    text=True,
                    check=True
                )
                git_result = "success"
                print(f"Git commit executed successfully: {commit_message}")
                
        except subprocess.CalledProcessError as e:
            git_result = "error"
            print(
                f"WARNING: Git commit failed: {e.stderr if e.stderr else str(e)}",
                file=sys.stderr,
            )
        except Exception as e:
            git_result = "error"
            print(
                f"WARNING: Error executing git commit: {e}",
                file=sys.stderr,
            )

    if git_result:
        print(f"{prompt_id} completed (git: {git_result})")
    else:
        print(f"{prompt_id} completed")
    
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
