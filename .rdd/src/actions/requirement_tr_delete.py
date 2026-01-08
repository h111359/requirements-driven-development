#!/usr/bin/env python3
"""Delete (mark as [DELETED]) a Technical Requirement in requirements.md.

This script marks a requirement as deleted by replacing its text with [DELETED]
marker while preserving the requirement ID for traceability.

Usage:
  requirement_tr_delete.py id="TR-XXXX"

Parameters:
  id - The requirement ID to delete (required, format: TR-XXXX)

Output:
  Prints "SUCCESS: Deleted TR-XXXX" to stdout on success
  Prints error message to stderr on failure
  Exit code: 0 for success, 1 for failure

Examples:
  python requirement_tr_delete.py id="TR-0052"
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path
from typing import Dict, Optional


_REQUIREMENT_ID_FORMAT = re.compile(r"^TR-\d{4}$")


def _repo_root() -> Path:
    """Get repository root directory."""
    # This file lives at: <repo>/.rdd/src/actions/requirement_tr_delete.py
    return Path(__file__).resolve().parents[3]


def _parse_params(argv: list[str]) -> Dict[str, str]:
    """Parse command-line parameters in key=value format."""
    params: Dict[str, str] = {}
    for arg in argv:
        if "=" not in arg:
            continue
        key, value = arg.split("=", 1)
        params[key.strip()] = value
    return params


def _get_param(params: Dict[str, str], *names: str) -> Optional[str]:
    """Get parameter value by name(s)."""
    for name in names:
        if name in params:
            return params[name]
    return None


def _validate_requirement_id(requirement_id: str) -> None:
    """Validate requirement ID format.
    
    Args:
        requirement_id: Requirement ID to validate
        
    Raises:
        ValueError: If ID format is invalid
    """
    if not _REQUIREMENT_ID_FORMAT.match(requirement_id):
        raise ValueError(
            f"Invalid requirement ID format: '{requirement_id}'. "
            f"Expected format: TR-XXXX (e.g., TR-0042)"
        )


def _delete_requirement(
    requirements_path: Path,
    requirement_id: str
) -> None:
    """Delete (mark as [DELETED]) a Technical Requirement.
    
    Args:
        requirements_path: Path to requirements.md file
        requirement_id: ID of requirement to delete
        
    Raises:
        FileNotFoundError: If requirements.md doesn't exist
        ValueError: If requirement not found
    """
    if not requirements_path.exists():
        raise FileNotFoundError(
            f"Requirements file not found: {requirements_path}. "
            f"Ensure .rdd-instance/specifications/requirements.md exists."
        )
    
    # Validate ID
    _validate_requirement_id(requirement_id)
    
    # Read current content
    content = requirements_path.read_text(encoding="utf-8")
    
    # Find the requirement line
    # Pattern matches: - [TR-XXXX] <anything>
    pattern = re.compile(
        r"^- \[" + re.escape(requirement_id) + r"\].*$",
        re.MULTILINE
    )
    
    match = pattern.search(content)
    if not match:
        raise ValueError(
            f"Requirement {requirement_id} not found in requirements.md. "
            f"Cannot delete non-existent requirement."
        )
    
    # Replace the requirement line with [DELETED] marker
    new_line = f"- [{requirement_id}] [DELETED]"
    new_content = content[:match.start()] + new_line + content[match.end():]
    
    # Write atomically using temp file + rename
    temp_fd, temp_path = tempfile.mkstemp(
        dir=requirements_path.parent,
        prefix=".requirements_",
        suffix=".md.tmp",
        text=True
    )
    
    try:
        with open(temp_fd, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        # Atomic rename
        Path(temp_path).replace(requirements_path)
    except Exception:
        # Clean up temp file on error
        try:
            Path(temp_path).unlink()
        except Exception:
            pass
        raise


def main() -> int:
    """Main entry point."""
    params = _parse_params(sys.argv[1:])
    
    # Get required id parameter
    requirement_id = _get_param(params, "id")
    if not requirement_id or not requirement_id.strip():
        print(
            "ERROR: 'id' parameter required. "
            "Usage: requirement_tr_delete.py id=\"TR-XXXX\"",
            file=sys.stderr
        )
        return 1
    requirement_id = requirement_id.strip()
    
    # Get requirements.md path
    repo_root = _repo_root()
    requirements_path = repo_root / ".rdd-instance" / "specifications" / "requirements.md"
    
    try:
        _delete_requirement(requirements_path, requirement_id)
        print(f"SUCCESS: Deleted {requirement_id}")
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
