#!/usr/bin/env python3
"""Set the executed flag of a prompt to true.

Behavior:
  - Updates the `executed` field of a prompt record in:
        `.rdd-instance/workdir/work-iteration-registry.json`
  - If `prompt-id=` is omitted, defaults to the currently active prompt.
  - Validates that the prompt exists before setting the flag.

This script is intentionally deterministic and non-interactive.

Usage (named parameters):
  prompt_set_executed_on.py [prompt-id=P-001]

Examples:
  # Set the executed flag for the active prompt
  prompt_set_executed_on.py

  # Set the executed flag for a specific prompt
  prompt_set_executed_on.py prompt-id=P-003

Output:
  Prints the updated prompt ID and executed status as a single line to stdout.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def _repo_root() -> Path:
    # This file lives at: <repo>/.rdd/src/actions/prompt_set_executed_on.py
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

    # Check if executed flag is already set
    if target_prompt.get("executed") is True:
        print(f"{prompt_id} executed=true (already set)")
        return 0

    # Set the executed flag to true
    target_prompt["executed"] = True

    # Write the updated registry
    _dump_json(registry_path, registry)

    print(f"{prompt_id} executed=true")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
