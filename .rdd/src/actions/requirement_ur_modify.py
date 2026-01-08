#!/usr/bin/env python3
"""Modify an existing User Requirement in requirements.md.

This script safely modifies requirement text while preserving ID and file format.

Usage:
  requirement_ur_modify.py id="UR-XXXX" text="<new requirement text>" [validation=basic|none]

Parameters:
  id - The requirement ID to modify (required, format: UR-XXXX)
  text - The new requirement text (required, 10-2048 characters)
  validation - Validation level: 'basic' (default) or 'none'

Output:
  Prints "SUCCESS: Modified UR-XXXX" to stdout on success
  Prints error message to stderr on failure
  Exit code: 0 for success, 1 for failure

Examples:
  python requirement_ur_modify.py id="UR-0042" text="The system shall export data in CSV and JSON formats"
  python requirement_ur_modify.py id="UR-0023" text="See spec v2" validation=none
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path
from typing import Dict, Optional


_REQUIREMENT_ID_FORMAT = re.compile(r"^UR-\d{4}$")
_VALIDATION_MODES = {"basic", "none"}


def _repo_root() -> Path:
    """Get repository root directory."""
    # This file lives at: <repo>/.rdd/src/actions/requirement_ur_modify.py
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
            f"Expected format: UR-XXXX (e.g., UR-0042)"
        )


def _validate_requirement_text(text: str, validation: str) -> None:
    """Validate requirement text according to validation mode.
    
    Args:
        text: Requirement text to validate
        validation: Validation mode ('basic' or 'none')
        
    Raises:
        ValueError: If validation fails
    """
    if validation == "none":
        return
    
    text_stripped = text.strip()
    
    if len(text_stripped) < 10:
        raise ValueError(
            f"Requirement text too short (minimum 10 characters). "
            f"Provided: {len(text_stripped)} characters. "
            f"Use validation=none to skip this check."
        )
    
    if len(text_stripped) > 2048:
        raise ValueError(
            f"Requirement text too long (maximum 2048 characters). "
            f"Provided: {len(text_stripped)} characters."
        )
    
    if "shall" not in text_stripped.lower():
        raise ValueError(
            "Requirement must contain 'shall' keyword. "
            "Example: 'The system shall validate user input.' "
            "Use validation=none to skip this check."
        )


def _modify_requirement(
    requirements_path: Path,
    requirement_id: str,
    new_text: str,
    validation: str
) -> None:
    """Modify an existing User Requirement.
    
    Args:
        requirements_path: Path to requirements.md file
        requirement_id: ID of requirement to modify
        new_text: New text for the requirement
        validation: Validation mode
        
    Raises:
        FileNotFoundError: If requirements.md doesn't exist
        ValueError: If validation fails or requirement not found
    """
    if not requirements_path.exists():
        raise FileNotFoundError(
            f"Requirements file not found: {requirements_path}. "
            f"Ensure .rdd-instance/specifications/requirements.md exists."
        )
    
    # Validate inputs
    _validate_requirement_id(requirement_id)
    _validate_requirement_text(new_text, validation)
    
    # Read current content
    content = requirements_path.read_text(encoding="utf-8")
    
    # Find the requirement line
    # Pattern matches: - [UR-XXXX] <anything>
    pattern = re.compile(
        r"^- \[" + re.escape(requirement_id) + r"\].*$",
        re.MULTILINE
    )
    
    match = pattern.search(content)
    if not match:
        raise ValueError(
            f"Requirement {requirement_id} not found in requirements.md. "
            f"Use requirement_ur_create.py to create new requirements."
        )
    
    # Check if modifying a deleted requirement
    if "[DELETED]" in match.group():
        print(
            f"WARNING: Modifying deleted requirement {requirement_id}",
            file=sys.stderr
        )
    
    # Replace the requirement line
    new_line = f"- [{requirement_id}] {new_text.strip()}"
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
            "Usage: requirement_ur_modify.py id=\"UR-XXXX\" text=\"New text...\"",
            file=sys.stderr
        )
        return 1
    requirement_id = requirement_id.strip()
    
    # Get required text parameter
    text = _get_param(params, "text")
    if not text or not text.strip():
        print(
            "ERROR: 'text' parameter required. "
            "Usage: requirement_ur_modify.py id=\"UR-XXXX\" text=\"New text...\"",
            file=sys.stderr
        )
        return 1
    
    # Get optional validation parameter
    validation = (_get_param(params, "validation") or "basic").strip()
    if validation not in _VALIDATION_MODES:
        print(
            f"ERROR: Invalid validation mode '{validation}'. "
            f"Expected one of: {', '.join(sorted(_VALIDATION_MODES))}",
            file=sys.stderr
        )
        return 1
    
    # Get requirements.md path
    repo_root = _repo_root()
    requirements_path = repo_root / ".rdd-instance" / "specifications" / "requirements.md"
    
    try:
        _modify_requirement(requirements_path, requirement_id, text, validation)
        print(f"SUCCESS: Modified {requirement_id}")
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
