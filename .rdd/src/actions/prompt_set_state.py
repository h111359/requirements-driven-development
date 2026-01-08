#!/usr/bin/env python3
"""Change the state of a prompt in the active work iteration.

Behavior:
  - Updates the `state` field of a prompt record in:
        `.rdd-instance/workdir/work-iteration-registry.json`
  - Enforces the "single active prompt" invariant:
      Only one prompt may be in state 'active' at a time.
  - If `prompt-id=` is omitted, defaults to the currently active prompt.

This script is intentionally deterministic and non-interactive.

Usage (named parameters):
  prompt_set_state.py state=<active|completed> [prompt-id=P-001]

Examples:
  # Set the active prompt to 'completed'
  prompt_set_state.py state=completed

  # Set a specific prompt to 'active'
  prompt_set_state.py state=active prompt-id=P-003

Output:
  Prints the updated prompt ID and state as a single line to stdout.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional


_PROMPT_STATES = {"active", "completed"}


def _repo_root() -> Path:
    # This file lives at: <repo>/.rdd/src/actions/prompt_set_state.py
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

    # Required: new state
    new_state = _get_param(params, "state")
    if not new_state or new_state.strip() not in _PROMPT_STATES:
        print(
            f"ERROR: 'state' parameter required; expected one of {sorted(_PROMPT_STATES)}",
            file=sys.stderr,
        )
        return 1
    new_state = new_state.strip()

    # Optional: prompt-id (if omitted, use active prompt)
    prompt_id_raw = _get_param(params, "prompt-id", "prompt_id")

    repo_root = _repo_root()
    workdir = repo_root / ".rdd-instance" / "workdir"
    registry_path = workdir / "work-iteration-registry.json"

    if not registry_path.is_file():
        raise FileNotFoundError(f"Work iteration registry not found: {registry_path}")

    registry = _load_json(registry_path)

    prompts = registry.get("prompts")
    if not isinstance(prompts, list):
        raise ValueError(f"Missing or invalid 'prompts' array in {registry_path}")

    # Determine which prompt to update
    target_prompt: Optional[Dict[str, Any]] = None

    if prompt_id_raw is not None:
        # Explicit prompt ID provided
        prompt_id = prompt_id_raw.strip()
        for p in prompts:
            if isinstance(p, dict) and p.get("prompt-id") == prompt_id:
                target_prompt = p
                break
        if target_prompt is None:
            raise ValueError(f"Prompt not found: {prompt_id}")
    else:
        # Default to active prompt
        target_prompt = _find_active_prompt(prompts)
        if target_prompt is None:
            raise ValueError(
                "No active prompt found (no prompt in 'active' state); "
                "please specify prompt-id= explicitly"
            )

    prompt_id = target_prompt["prompt-id"]
    old_state = target_prompt.get("state")

    # Check if state is already correct
    if old_state == new_state:
        print(f"{prompt_id} {new_state}")
        return 0

    # Enforce single-active invariant when setting to 'active'
    if new_state == "active":
        active_prompt = _find_active_prompt(prompts)
        if active_prompt is not None and active_prompt.get("prompt-id") != prompt_id:
            raise ValueError(
                f"Cannot set {prompt_id} to '{new_state}': "
                f"prompt {active_prompt.get('prompt-id')} is already in state '{active_prompt.get('state')}'. "
                "Only one prompt may be in 'active' state at a time."
            )

    # Update the state
    target_prompt["state"] = new_state

    # Write the updated registry
    _dump_json(registry_path, registry)

    print(f"{prompt_id} {new_state}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
