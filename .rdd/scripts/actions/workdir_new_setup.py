#!/usr/bin/env python3
"""Create a timestamped copy of the RDD prompt setup template in the workdir.

Behavior:
  1) Calls `.rdd/scripts/actions/print_timestamp.py` to obtain a timestamp in
     format: YYYYMMDD-hhmiss
  2) Reads `.rdd/templates/rdd-workdir-setup.json`
  3) Writes a copy into `.rdd-instance/workdir/` named:
       rdd-workdir-setup.json
  4) Sets JSON key `prompt-id` to `<timestamp>`
  5) Creates an empty prompt file in `.rdd-instance/workdir/` named:
      rdd-prompt-<timestamp>.md

This script is intentionally deterministic and non-interactive.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    # This file lives at: <repo>/.rdd/scripts/actions/copy_prompt_setup.py
    return Path(__file__).resolve().parents[3]


def _get_timestamp(repo_root: Path) -> str:
    ts_script = repo_root / ".rdd" / "scripts" / "actions" / "print_timestamp.py"
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
    repo_root = _repo_root()

    timestamp = _get_timestamp(repo_root)

    template_path = repo_root / ".rdd" / "templates" / "rdd-workdir-setup.json"
    workdir = repo_root / ".rdd-instance" / "workdir"
    dest_path = workdir / f"rdd-workdir-setup.json"
    prompt_path = workdir / f"rdd-prompt-{timestamp}.md"

    if not template_path.is_file():
        raise FileNotFoundError(f"Template not found: {template_path}")
    workdir.mkdir(parents=True, exist_ok=True)

    # Safety guard: initialize only on an empty workdir to avoid clobbering
    # in-progress work.
    if any(workdir.iterdir()):
        print(f"Workdir is not empty - setup is stopped.")
        return 0

    with template_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Template JSON must be an object: {template_path}")

    data["prompt-id"] = timestamp

    with dest_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        f.write("\n")

    # Create (or truncate) the prompt file.
    prompt_path.write_text("", encoding="utf-8")

    # Keep stdout single-line and agent-friendly.
    print(str(dest_path))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
