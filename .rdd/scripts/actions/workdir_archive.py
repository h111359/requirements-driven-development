#!/usr/bin/env python3
"""Archive the current workdir into `.rdd-instance/archive/workdir-<prompt-id>/`.

Source of truth for `<prompt-id>`:
  `.rdd-instance/workdir/rdd-workdir-setup.json` key: `prompt-id`

Behavior:
  - Reads the `prompt-id` from the setup JSON.
  - Copies the entire contents of `.rdd-instance/workdir/` into a new folder:
      `.rdd-instance/archive/workdir-<prompt-id>/`
  - Refuses to run if the destination archive folder already exists.

This script is intentionally deterministic and non-interactive.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


def _repo_root() -> Path:
    # This file lives at: <repo>/.rdd/scripts/actions/workdir-archive.py
    return Path(__file__).resolve().parents[3]


def _read_prompt_id(setup_path: Path) -> str:
    with setup_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Setup JSON must be an object: {setup_path}")

    prompt_id = data.get("prompt-id")
    if not isinstance(prompt_id, str) or not prompt_id.strip():
        raise ValueError(f"Missing or empty 'prompt-id' in {setup_path}")

    # Keep it simple (and safe for folder names).
    prompt_id = prompt_id.strip()
    if "/" in prompt_id or "\\" in prompt_id:
        raise ValueError(f"Invalid prompt-id (must not contain path separators): {prompt_id!r}")
    return prompt_id


def main() -> int:
    repo_root = _repo_root()

    workdir = repo_root / ".rdd-instance" / "workdir"
    setup_path = workdir / "rdd-workdir-setup.json"
    archive_root = repo_root / ".rdd-instance" / "archive"

    if not workdir.is_dir():
        raise FileNotFoundError(f"Workdir not found: {workdir}")
    if not setup_path.is_file():
        raise FileNotFoundError(f"Workdir setup file not found: {setup_path}")

    prompt_id = _read_prompt_id(setup_path)
    dest_dir = archive_root / f"workdir-{prompt_id}"

    if dest_dir.exists():
        print(f"Archive destination already exists ({dest_dir}); nothing to do.")
        return 0

    archive_root.mkdir(parents=True, exist_ok=True)

    # Copy the entire directory tree.
    shutil.copytree(workdir, dest_dir)

    # Clear workdir after successful archive.
    # Keep the workdir folder itself, but remove all children.
    for child in workdir.iterdir():
        try:
            if child.is_dir() and not child.is_symlink():
                shutil.rmtree(child)
            else:
                child.unlink()
        except Exception as e:
            # Best-effort cleanup: report but continue.
            print(f"WARNING: Could not delete {child}: {e}", file=sys.stderr)

    # Keep stdout single-line and agent-friendly.
    print(str(dest_dir))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
