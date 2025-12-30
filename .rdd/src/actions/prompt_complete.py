#!/usr/bin/env python3
"""Complete a prompt by setting its state to 'completed' and optionally executing git commit.

Behavior:
  - Updates the `state` field of a prompt to 'completed' in:
        `.rdd-instance/workdir/work-iteration-registry.json`
  - If the root-level `git-enabled` flag is true, executes `.rdd/src/actions/git_commit.py`
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
    """Find the prompt currently in 'planned' or 'in-progress' state."""
    for p in prompts:
        if not isinstance(p, dict):
            continue
        if p.get("state") in {"planned", "in-progress"}:
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
                "No active prompt found (no prompt in 'planned' or 'in-progress' state); "
                "please specify prompt-id= explicitly\n"
                "Remediation: Either specify a prompt-id or set a prompt to 'planned' or 'in-progress' state."
            )

    prompt_id = target_prompt["prompt-id"]
    old_state = target_prompt.get("state")

    # Check if already completed
    if old_state == "completed":
        print(f"{prompt_id} already completed")
        return 0

    # Check git-enabled flag
    git_enabled = registry.get("git-enabled", False)
    git_result = None

    if git_enabled:
        # Execute git commit
        git_commit_script = repo_root / ".rdd" / "src" / "actions" / "git_commit.py"
        if not git_commit_script.is_file():
            print(
                f"WARNING: git-enabled is true but git_commit.py not found at {git_commit_script}",
                file=sys.stderr,
            )
        else:
            try:
                result = subprocess.run(
                    ["python", str(git_commit_script)],
                    cwd=str(repo_root),
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    git_result = "success"
                    print(f"Git commit executed successfully: {result.stdout.strip()}")
                else:
                    # Check if failure is due to no changes
                    if "no changes to commit" in result.stderr.lower() or "working tree clean" in result.stderr.lower():
                        git_result = "no-changes"
                        print(
                            f"WARNING: Git commit skipped - no changes to commit",
                            file=sys.stderr,
                        )
                    else:
                        # Other git error - log but continue
                        git_result = "error"
                        print(
                            f"WARNING: Git commit failed: {result.stderr.strip()}",
                            file=sys.stderr,
                        )
            except Exception as e:
                git_result = "error"
                print(
                    f"WARNING: Error executing git commit: {e}",
                    file=sys.stderr,
                )

    # Update the state to completed
    target_prompt["state"] = "completed"

    # Write the updated registry
    _dump_json(registry_path, registry)

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
