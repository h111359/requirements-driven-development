#!/usr/bin/env python3
"""Check if all questionnaire questions are answered and set questionnaire-answered flag.

This script validates that all questions in a prompt's questionnaire.json file have been
answered (user-selection.type is not null). If all questions are answered, it automatically
sets the questionnaire-answered flag to true in the work iteration registry.

Usage:
  questionnaire_check_complete.py [prompt-id=P-XXX]

If prompt-id is omitted, uses the active prompt.

Output:
  Prints SUCCESS or INFO message to stdout
  Prints ERROR messages to stderr
  Returns 0 on success, 1 on error
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def _repo_root() -> Path:
    # This file lives at: <repo>/.rdd/src/actions/questionnaire_check_complete.py
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
        raise ValueError(f"JSON must be an object: {path}")
    return data


def _dump_json(path: Path, data: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        f.write("\n")


def _find_active_prompt_id(registry: Dict[str, Any]) -> Optional[str]:
    prompts = registry.get("prompts", [])
    for p in prompts:
        if isinstance(p, dict) and p.get("state") == "active":
            return p.get("prompt-id")
    return None


def _find_prompt_by_id(registry: Dict[str, Any], prompt_id: str) -> Optional[Dict[str, Any]]:
    prompts = registry.get("prompts", [])
    for p in prompts:
        if isinstance(p, dict) and p.get("prompt-id") == prompt_id:
            return p
    return None


def _sanitize_title_for_path_component(title: str) -> str:
    sanitized = title.replace("/", "_").replace("\\", "_")
    sanitized = sanitized.strip()
    return sanitized


def _check_questionnaire_complete(questionnaire_path: Path) -> tuple[bool, int, int]:
    """Check if all questions in questionnaire are answered.
    
    Returns:
        (all_answered, total_questions, answered_questions)
    """
    if not questionnaire_path.exists():
        return False, 0, 0
    
    questionnaire = _load_json(questionnaire_path)
    questions = questionnaire.get("questions", [])
    
    if not questions:
        # No questions means nothing to answer
        return True, 0, 0
    
    total = len(questions)
    answered = 0
    
    for question in questions:
        if not isinstance(question, dict):
            continue
        
        user_selection = question.get("user-selection", {})
        if isinstance(user_selection, dict):
            selection_type = user_selection.get("type")
            # Question is answered if type is not null
            if selection_type is not None:
                answered += 1
    
    return answered == total, total, answered


def main() -> int:
    params = _parse_params(sys.argv[1:])
    
    repo_root = _repo_root()
    workdir = repo_root / ".rdd-instance" / "workdir"
    registry_path = workdir / "work-iteration-registry.json"
    
    if not registry_path.is_file():
        print(f"ERROR: Work iteration registry not found: {registry_path}", file=sys.stderr)
        return 1
    
    registry = _load_json(registry_path)
    
    # Determine which prompt to check
    explicit_id = _get_param(params, "prompt-id")
    if explicit_id:
        prompt_id = explicit_id.strip()
        prompt = _find_prompt_by_id(registry, prompt_id)
        if not prompt:
            print(f"ERROR: Prompt {prompt_id} not found in registry", file=sys.stderr)
            return 1
    else:
        prompt_id = _find_active_prompt_id(registry)
        if not prompt_id:
            print("ERROR: No active prompt found", file=sys.stderr)
            return 1
        prompt = _find_prompt_by_id(registry, prompt_id)
        if not prompt:
            print(f"ERROR: Active prompt {prompt_id} not found", file=sys.stderr)
            return 1
    
    # Get prompt folder
    prompt_title = prompt.get("prompt-title", "")
    prompt_folder = workdir / f"{prompt_id}_{_sanitize_title_for_path_component(prompt_title)}"
    questionnaire_path = prompt_folder / "questionnaire.json"
    
    # Check if questionnaire exists
    if not questionnaire_path.exists():
        print(f"INFO: No questionnaire file found for {prompt_id}, questionnaire-answered flag remains false")
        return 0
    
    # Check completion status
    all_answered, total, answered = _check_questionnaire_complete(questionnaire_path)
    
    if all_answered:
        # Set questionnaire-answered flag to true if not already set
        if not prompt.get("questionnaire-answered", False):
            prompt["questionnaire-answered"] = True
            _dump_json(registry_path, registry)
            print(f"SUCCESS: All {total} questions answered, questionnaire-answered flag set to True for prompt '{prompt_id}'")
        else:
            print(f"INFO: All {total} questions already answered, questionnaire-answered already True for prompt '{prompt_id}'")
    else:
        # Ensure flag is false
        if prompt.get("questionnaire-answered", False):
            prompt["questionnaire-answered"] = False
            _dump_json(registry_path, registry)
            print(f"INFO: Only {answered}/{total} questions answered, questionnaire-answered flag set to False for prompt '{prompt_id}'")
        else:
            print(f"INFO: Only {answered}/{total} questions answered, questionnaire-answered already False for prompt '{prompt_id}'")
    
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
