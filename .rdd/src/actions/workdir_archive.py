#!/usr/bin/env python3
"""Archive the current workdir into `.rdd-instance/archive/<iteration-id>_<iteration-name>/`.

Source of truth:
    `.rdd-instance/workdir/work-iteration-registry.json`
        keys: `iteration-id`, `iteration-name`

Behavior:
    - Reads `iteration-id` and `iteration-name` from the registry JSON.
    - Copies the entire contents of `.rdd-instance/workdir/` into a new folder:
            `.rdd-instance/archive/<iteration-id>_<iteration-name>/`
  - Refuses to run if the destination archive folder already exists.

This script is intentionally deterministic and non-interactive.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


def _repo_root() -> Path:
    # This file lives at: <repo>/.rdd/src/actions/workdir-archive.py
    return Path(__file__).resolve().parents[3]


def _read_iteration_archive_name(registry_path: Path) -> str:
    with registry_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Registry JSON must be an object: {registry_path}")

    iteration_id = data.get("iteration-id")
    iteration_name = data.get("iteration-name")

    if not isinstance(iteration_id, str) or not iteration_id.strip():
        raise ValueError(f"Missing or empty 'iteration-id' in {registry_path}")
    if not isinstance(iteration_name, str) or not iteration_name.strip():
        raise ValueError(f"Missing or empty 'iteration-name' in {registry_path}")

    # Exact requested shape: <iteration-id> + "_" + <iteration-name>
    archive_name = f"{iteration_id.strip()}_{iteration_name.strip()}"

    # Safety: disallow path separators; keep name as a single folder.
    if "/" in archive_name or "\\" in archive_name:
        raise ValueError(
            "Invalid iteration registry values (must not contain path separators): "
            f"{archive_name!r}"
        )

    return archive_name


def main() -> int:
    repo_root = _repo_root()

    workdir = repo_root / ".rdd-instance" / "workdir"
    registry_path = workdir / "work-iteration-registry.json"
    archive_root = repo_root / ".rdd-instance" / "archive"

    if not workdir.is_dir():
        raise FileNotFoundError(f"Workdir not found: {workdir}")
    if not registry_path.is_file():
        raise FileNotFoundError(f"Work iteration registry not found: {registry_path}")

    archive_name = _read_iteration_archive_name(registry_path)
    dest_dir = archive_root / archive_name

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
