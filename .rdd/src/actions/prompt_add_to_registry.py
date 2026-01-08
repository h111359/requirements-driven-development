#!/usr/bin/env python3
"""Add or update a prompt's text in the prompts-registry.md file.

Behavior:
  - Reads the prompt.md file from the prompt's workdir folder
  - Reads any modification-XXX.md files if they exist
  - Formats the content according to `.rdd/conventions/prompts-registry.convention.md`
  - Updates the prompts-registry.md file, replacing the content for that prompt-id
  - If `prompt-id=` is omitted, defaults to the currently active prompt

This script is intentionally deterministic and non-interactive.

Usage (named parameters):
  prompt_add_to_registry.py [prompt-id=P-001]

Examples:
  # Add the active prompt to registry
  prompt_add_to_registry.py

  # Add a specific prompt to registry
  prompt_add_to_registry.py prompt-id=P-003

Output:
  Prints the operation status to stdout.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def _repo_root() -> Path:
    # This file lives at: <repo>/.rdd/src/actions/prompt_add_to_registry.py
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


def _find_active_prompt(prompts: list[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Find the prompt currently in 'active' state."""
    for p in prompts:
        if not isinstance(p, dict):
            continue
        if p.get("state") == "active":
            return p
    return None


def _find_prompt_by_id(prompts: list[Dict[str, Any]], prompt_id: str) -> Optional[Dict[str, Any]]:
    """Find a prompt by its ID."""
    for p in prompts:
        if isinstance(p, dict) and p.get("prompt-id") == prompt_id:
            return p
    return None


def _get_prompt_folder(workdir: Path, prompt_id: str, prompt_title: str) -> Path:
    """Find the prompt folder. Handle both exact match and pattern match."""
    # Try exact match first
    folder_name = f"{prompt_id}_{prompt_title}"
    folder_path = workdir / folder_name
    if folder_path.is_dir():
        return folder_path
    
    # Try pattern match (in case title has changed)
    pattern = f"{prompt_id}_*"
    matches = list(workdir.glob(pattern))
    if matches:
        return matches[0]
    
    raise FileNotFoundError(f"Prompt folder not found for {prompt_id}")


def _read_modifications(prompt_folder: Path) -> List[tuple[str, str]]:
    """Read all modification files. Returns list of (id, content) tuples."""
    modifications = []
    
    # Look for modification-XXX.md files
    mod_files = sorted(prompt_folder.glob("modification-*.md"))
    
    for mod_file in mod_files:
        # Extract modification ID from filename (e.g., "modification-001.md" -> "001")
        match = re.match(r"modification-(\d+)\.md$", mod_file.name)
        if match:
            mod_id = match.group(1)
            content = mod_file.read_text(encoding="utf-8").strip()
            modifications.append((mod_id, content))
    
    return modifications


def _build_prompt_content(prompt_md_content: str, modifications: List[tuple[str, str]]) -> str:
    """Build the complete prompt content including modifications."""
    parts = [prompt_md_content.strip()]
    
    # Add modifications if any
    for mod_id, mod_content in modifications:
        parts.append(f"\n\n### Modification {mod_id}\n\n{mod_content.strip()}")
    
    return "\n".join(parts)


def _update_prompts_registry(
    registry_path: Path,
    prompt_id: str,
    prompt_title: str,
    new_content: str
) -> None:
    """Update or add a prompt in prompts-registry.md."""
    
    # Read existing registry
    if registry_path.is_file():
        registry_content = registry_path.read_text(encoding="utf-8")
    else:
        registry_content = ""
    
    # Pattern to match the prompt record
    start_sentinel = f'%%PROMPT {prompt_id} "{prompt_title}"'
    end_sentinel = "%%ENDPROMPT"
    
    # Try to find and replace existing record
    pattern = re.compile(
        rf'^%%PROMPT {re.escape(prompt_id)} ".*?"\n(.*?)\n%%ENDPROMPT',
        re.MULTILINE | re.DOTALL
    )
    
    new_record = f'{start_sentinel}\n{new_content}\n{end_sentinel}'
    
    if pattern.search(registry_content):
        # Replace existing record
        updated_content = pattern.sub(new_record, registry_content)
    else:
        # Append new record
        if registry_content and not registry_content.endswith('\n'):
            registry_content += '\n'
        if registry_content:
            registry_content += '\n'
        updated_content = registry_content + new_record + '\n'
    
    # Write back to file
    registry_path.write_text(updated_content, encoding="utf-8")


def main() -> int:
    params = _parse_params(sys.argv[1:])

    # Optional: prompt-id (if omitted, use active prompt)
    prompt_id_raw = _get_param(params, "prompt-id", "prompt_id")

    repo_root = _repo_root()
    workdir = repo_root / ".rdd-instance" / "workdir"
    registry_path = workdir / "work-iteration-registry.json"
    prompts_registry_path = workdir / "prompts-registry.md"

    if not registry_path.is_file():
        raise FileNotFoundError(
            f"Work iteration registry not found: {registry_path}\n"
            f"Remediation: Ensure you have initialized a work iteration."
        )

    registry = _load_json(registry_path)

    prompts = registry.get("prompts")
    if not isinstance(prompts, list):
        raise ValueError(f"Missing or invalid 'prompts' array in {registry_path}")

    # Determine which prompt to process
    target_prompt: Optional[Dict[str, Any]] = None

    if prompt_id_raw is not None:
        # Explicit prompt ID provided
        prompt_id = prompt_id_raw.strip()
        target_prompt = _find_prompt_by_id(prompts, prompt_id)
        if target_prompt is None:
            raise ValueError(
                f"Prompt not found: {prompt_id}\n"
                f"Remediation: Verify the prompt ID exists in the registry."
            )
    else:
        # Default to active prompt
        target_prompt = _find_active_prompt(prompts)
        if target_prompt is None:
            raise ValueError(
                "No active prompt found; please specify prompt-id= explicitly\n"
                "Remediation: Either specify a prompt-id or set a prompt to 'active' state."
            )

    prompt_id = target_prompt["prompt-id"]
    prompt_title = target_prompt.get("prompt-title") or target_prompt.get("title", "UNKNOWN")

    # Find the prompt folder
    try:
        prompt_folder = _get_prompt_folder(workdir, prompt_id, prompt_title)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"{e}\n"
            f"Remediation: Ensure the prompt folder exists in .rdd-instance/workdir/"
        )

    # Read prompt.md
    prompt_md_path = prompt_folder / "prompt.md"
    if not prompt_md_path.is_file():
        raise FileNotFoundError(
            f"prompt.md not found in {prompt_folder}\n"
            f"Remediation: Ensure prompt.md exists in the prompt folder."
        )

    prompt_md_content = prompt_md_path.read_text(encoding="utf-8")

    # Read modifications
    modifications = _read_modifications(prompt_folder)

    # Build complete content
    complete_content = _build_prompt_content(prompt_md_content, modifications)

    # Update prompts-registry.md
    _update_prompts_registry(prompts_registry_path, prompt_id, prompt_title, complete_content)

    if modifications:
        print(f"SUCCESS: {prompt_id} added to prompts-registry.md (with {len(modifications)} modification(s))")
    else:
        print(f"SUCCESS: {prompt_id} added to prompts-registry.md")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
