#!/usr/bin/env python3
"""Create a work iteration registry in the workdir.

Behavior:
  1) Calls `.rdd/src/actions/print_timestamp.py` to obtain a timestamp in
     format: YYYYMMDD-HHmiss
  2) Generates content for work-iteration-registry.json according to
     `.rdd/conventions/work-iteration-registry.convention.md`
  3) Writes the generated content into `.rdd-instance/workdir/` named:
       work-iteration-registry.json
  4) Sets JSON key `iteration-id` to `ITR-<timestamp>`
  5) Sets JSON key `iteration-name` to the value passed as command-line argument

This script is intentionally deterministic and non-interactive.

Usage:
  workdir_new_setup.py name="<iteration-name>"
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    # This file lives at: <repo>/.rdd/src/actions/copy_prompt_setup.py
    return Path(__file__).resolve().parents[3]


def _get_timestamp(repo_root: Path) -> str:
    ts_script = repo_root / ".rdd" / "src" / "actions" / "print_timestamp.py"
    try:
        result = subprocess.run(
            [sys.executable, str(ts_script)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or "").strip()
        raise RuntimeError(f"Failed to get timestamp from {ts_script}. {stderr}") from e

    timestamp = (result.stdout or "").strip()
    if not timestamp:
        raise RuntimeError(f"Timestamp script {ts_script} produced empty output")
    return timestamp


def main() -> int:
    # Parse named parameters from command line
    params = {}
    for arg in sys.argv[1:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            params[key] = value
    
    if "name" not in params:
        print("ERROR: 'name' parameter required", file=sys.stderr)
        print('Usage: workdir_new_setup.py name="<iteration-name>"', file=sys.stderr)
        return 1
    
    iteration_name = params["name"]
    
    repo_root = _repo_root()

    timestamp = _get_timestamp(repo_root)

    workdir = repo_root / ".rdd-instance" / "workdir"
    dest_path = workdir / "work-iteration-registry.json"

    workdir.mkdir(parents=True, exist_ok=True)

    # Safety guard: initialize only on an empty workdir to avoid clobbering
    # in-progress work.
    if any(workdir.iterdir()):
        print(f"Workdir is not empty - setup is stopped.")
        return 0

    # Generate JSON content according to .rdd/conventions/work-iteration-registry.convention.md
    data = {
        "iteration-id": f"ITR-{timestamp}",
        "iteration-name": iteration_name,
        "prompt-id-sequence-next-value": 1,
        "prompts": []
    }

    with dest_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        f.write("\n")

    # Keep stdout single-line and agent-friendly.
    print(str(dest_path))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
