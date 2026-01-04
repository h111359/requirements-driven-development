#!/usr/bin/env python3
"""Create a new Technical Requirement in requirements.md.

This script enforces safe, deterministic requirement creation with automatic
ID generation and format validation.

Usage:
  requirement_tr_create.py text="<requirement text>" [validation=basic|none]

Parameters:
  text - The requirement text (required, 10-2048 characters)
  validation - Validation level: 'basic' (default) or 'none'

Output:
  Prints "SUCCESS: Created TR-XXXX" to stdout on success
  Prints error message to stderr on failure
  Exit code: 0 for success, 1 for failure

Examples:
  python requirement_tr_create.py text="The framework shall use Python 3.11 or higher"
  python requirement_tr_create.py text="See external spec" validation=none
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path
from typing import Dict, Optional


_REQUIREMENT_ID_RE = re.compile(r"\[TR-(\d{4})\]")
_VALIDATION_MODES = {"basic", "none"}


def _repo_root() -> Path:
    """Get repository root directory."""
    # This file lives at: <repo>/.rdd/src/actions/requirement_tr_create.py
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
            "Example: 'The framework shall use Python 3.11 or higher.' "
            "Use validation=none to skip this check."
        )


def _find_highest_tr_id(content: str) -> int:
    """Find the highest existing TR ID number in requirements.md.
    
    Args:
        content: Content of requirements.md file
        
    Returns:
        Highest ID number found, or 0 if none found
    """
    highest = 0
    for match in _REQUIREMENT_ID_RE.finditer(content):
        id_num = int(match.group(1))
        if id_num > highest:
            highest = id_num
    return highest


def _find_section_end(content: str, section_header: str) -> Optional[int]:
    """Find the end position of a section in requirements.md.
    
    Args:
        content: Content of requirements.md file
        section_header: Section header to find (e.g., "## Technical Requirements")
        
    Returns:
        Position where new requirement should be inserted, or None if section not found
    """
    # Find the section header
    section_pattern = re.compile(r"^" + re.escape(section_header) + r"\s*$", re.MULTILINE)
    match = section_pattern.search(content)
    
    if not match:
        return None
    
    section_start = match.end()
    
    # Find the next section header (starts with ##)
    next_section = re.compile(r"^##\s+", re.MULTILINE)
    next_match = next_section.search(content, section_start)
    
    if next_match:
        # Insert before the next section
        # Find the last non-empty line before the next section
        section_content = content[section_start:next_match.start()]
        lines = section_content.rstrip().split('\n')
        # Calculate position at end of last requirement
        return section_start + len(section_content.rstrip())
    else:
        # This is the last section, append at end
        return len(content.rstrip())


def _create_requirement(
    requirements_path: Path,
    requirement_text: str,
    validation: str
) -> str:
    """Create a new Technical Requirement.
    
    Args:
        requirements_path: Path to requirements.md file
        requirement_text: Text of the requirement
        validation: Validation mode
        
    Returns:
        Created requirement ID (e.g., "TR-0042")
        
    Raises:
        FileNotFoundError: If requirements.md doesn't exist
        ValueError: If validation fails or section not found
    """
    if not requirements_path.exists():
        raise FileNotFoundError(
            f"Requirements file not found: {requirements_path}. "
            f"Ensure .rdd-instance/specifications/requirements.md exists."
        )
    
    # Validate requirement text
    _validate_requirement_text(requirement_text, validation)
    
    # Read current content
    content = requirements_path.read_text(encoding="utf-8")
    
    # Find highest existing TR ID
    highest_id = _find_highest_tr_id(content)
    new_id_num = highest_id + 1
    new_id = f"TR-{new_id_num:04d}"
    
    # Find where to insert the new requirement
    section_end = _find_section_end(content, "## Technical Requirements")
    if section_end is None:
        raise ValueError(
            "'## Technical Requirements' section not found in requirements.md. "
            "File may be corrupted or improperly formatted."
        )
    
    # Create new requirement line
    new_requirement = f"\n\n- [{new_id}] {requirement_text.strip()}"
    
    # Insert at section end
    new_content = content[:section_end] + new_requirement + "\n" + content[section_end:]
    
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
    
    return new_id


def main() -> int:
    """Main entry point."""
    params = _parse_params(sys.argv[1:])
    
    # Get required text parameter
    text = _get_param(params, "text")
    if not text or not text.strip():
        print(
            "ERROR: 'text' parameter required. "
            "Usage: requirement_tr_create.py text=\"The framework shall...\"",
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
        requirement_id = _create_requirement(requirements_path, text, validation)
        print(f"SUCCESS: Created {requirement_id}")
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
