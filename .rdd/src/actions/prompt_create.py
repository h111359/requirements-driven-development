#!/usr/bin/env python3
"""Create/register a prompt in the active work iteration.

Behavior:
  - Appends a prompt-metadata record to:
        `.rdd-instance/workdir/work-iteration-registry.json`
  - Ensures a matching prompt record exists in:
        `.rdd-instance/workdir/prompts-registry.md`
    (creates the file if missing)
  - Allocates a new prompt ID using `prompt-id-sequence-next-value` unless `id=` is provided.
  - Does NOT add real prompt text; the record content is created as a stub `TBD`.

This script is intentionally deterministic and non-interactive.

Usage (named parameters):
  prompt_create.py title="<title>" type=<main|modification> [state=<draft|planned|in-progress|completed>] \
      [id=P-001] [parent-id=P-001|parent_id=P-001|parent-id=null] \
      [analysis-approval=true|false] [analysis-state=<not-started|waiting-approval|approved|completed>] \
      [questionnaire-approval=true|false] [questionnaire-state=<not-started|waiting-approval|approved|completed>] \
      [plan-approval=true|false] [plan-state=<not-started|waiting-approval|approved|completed>]

Output:
  Prints the created prompt ID as a single line to stdout.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional


_PROMPT_ID_RE = re.compile(r"^P-[0-9]{3,}$")

_PROMPT_TYPES = {"main", "modification"}
_PROMPT_STATES = {"draft", "planned", "in-progress", "completed"}
_ARTIFACT_STATES = {"not-started", "waiting-approval", "approved", "completed"}


def _repo_root() -> Path:
    # This file lives at: <repo>/.rdd/src/actions/prompt_create.py
    return Path(__file__).resolve().parents[3]


def _parse_bool(raw: str) -> bool:
    v = raw.strip().lower()
    if v in {"true", "1", "yes", "y"}:
        return True
    if v in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"Invalid boolean value: {raw!r}")


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


def _validate_prompt_id(prompt_id: str) -> None:
    if not _PROMPT_ID_RE.match(prompt_id):
        raise ValueError(
            "Invalid prompt id format; expected P- followed by at least 3 digits, e.g. P-001"
        )


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


def _ensure_prompts_registry_record(
    prompts_registry_path: Path,
    prompt_id: str,
    title: str,
    *,
    stub_text: str = "TBD",
) -> None:
    prompts_registry_path.parent.mkdir(parents=True, exist_ok=True)

    existing = ""
    if prompts_registry_path.exists():
        existing = prompts_registry_path.read_text(encoding="utf-8")

    # Strict ID uniqueness guard (record starts at column 1).
    if re.search(rf"^%%PROMPT\s+{re.escape(prompt_id)}\s+\"", existing, flags=re.M):
        raise ValueError(
            f"Prompt text record already exists for {prompt_id} in {prompts_registry_path}"
        )

    record = (
        f"%%PROMPT {prompt_id} \"{title}\"\n"
        f"{stub_text}\n"
        f"%%ENDPROMPT\n"
    )

    prefix = existing
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    if prefix and not prefix.endswith("\n\n"):
        prefix += "\n"

    prompts_registry_path.write_text(prefix + record, encoding="utf-8")


def _sanitize_title_for_path_component(title: str) -> str:
    # Keep the folder name human-readable, but prevent path traversal / separators.
    # Spaces are allowed on all supported OSes; we only replace characters that
    # would break path semantics.
    sanitized = title.replace("/", "_").replace("\\", "_")
    sanitized = sanitized.strip()
    return sanitized


def _ensure_prompt_workdir_artifacts(workdir: Path, prompt_id: str, title: str) -> Path:
    prompt_dir = workdir / f"{prompt_id}_{_sanitize_title_for_path_component(title)}"
    prompt_dir.mkdir(parents=True, exist_ok=True)

    for name in ("prompt.md", "plan.md", "implementation.md"):
        p = prompt_dir / name
        if not p.exists():
            p.write_text("", encoding="utf-8")

    return prompt_dir


def _artifact_block(
    params: Dict[str, str],
    name: str,
    *,
    default_approval: bool = False,
    default_state: str = "not-started",
) -> Dict[str, Any]:
    approval_raw = _get_param(params, f"{name}-approval", f"{name}_approval")
    state_raw = _get_param(params, f"{name}-state", f"{name}_state")

    approval = default_approval if approval_raw is None else _parse_bool(approval_raw)
    state = default_state if state_raw is None else state_raw.strip()

    if state not in _ARTIFACT_STATES:
        raise ValueError(
            f"Invalid {name} state {state!r}; expected one of {sorted(_ARTIFACT_STATES)}"
        )
    if not approval and state in {"waiting-approval", "approved"}:
        raise ValueError(
            f"Invalid {name} state {state!r} when {name} approval is false"
        )

    return {"approval": approval, "state": state}


def main() -> int:
    params = _parse_params(sys.argv[1:])

    title = _get_param(params, "title")
    if not title or not title.strip():
        print("ERROR: 'title' parameter required", file=sys.stderr)
        return 1
    title = title.strip()
    if len(title) > 128:
        raise ValueError("Title must be <= 128 characters")

    prompt_type = _get_param(params, "type")
    if not prompt_type or prompt_type.strip() not in _PROMPT_TYPES:
        raise ValueError(f"'type' required; expected one of {sorted(_PROMPT_TYPES)}")
    prompt_type = prompt_type.strip()

    state = (_get_param(params, "state") or "draft").strip()
    if state not in _PROMPT_STATES:
        raise ValueError(f"Invalid prompt state {state!r}; expected one of {sorted(_PROMPT_STATES)}")

    parent_id_raw = _get_param(params, "parent-id", "parent_id")
    parent_id: Optional[str]
    if parent_id_raw is None or parent_id_raw.strip().lower() == "null" or parent_id_raw.strip() == "":
        parent_id = None
    else:
        parent_id = parent_id_raw.strip()

    repo_root = _repo_root()
    workdir = repo_root / ".rdd-instance" / "workdir"
    registry_path = workdir / "work-iteration-registry.json"
    prompts_registry_path = workdir / "prompts-registry.md"

    if not registry_path.is_file():
        raise FileNotFoundError(f"Work iteration registry not found: {registry_path}")

    registry = _load_json(registry_path)

    prompts = registry.get("prompts")
    if not isinstance(prompts, list):
        raise ValueError(f"Missing or invalid 'prompts' array in {registry_path}")

    existing_ids = {
        p.get("prompt-id") for p in prompts if isinstance(p, dict) and isinstance(p.get("prompt-id"), str)
    }

    explicit_id = _get_param(params, "prompt-id")
    if explicit_id is not None:
        prompt_id = explicit_id.strip()
        _validate_prompt_id(prompt_id)
    else:
        next_value = registry.get("prompt-id-sequence-next-value")
        if not isinstance(next_value, int) or next_value < 1:
            raise ValueError(
                f"Missing or invalid 'prompt-id-sequence-next-value' in {registry_path}"
            )
        prompt_id = f"P-{next_value:03d}"
        registry["prompt-id-sequence-next-value"] = next_value + 1

    if prompt_id in existing_ids:
        raise ValueError(f"Prompt id already exists in work iteration registry: {prompt_id}")

    # Enforce the single-active invariant when creating planned/in-progress prompts.
    if state in {"planned", "in-progress"}:
        for p in prompts:
            if not isinstance(p, dict):
                continue
            s = p.get("state")
            if s in {"planned", "in-progress"}:
                raise ValueError(
                    "Only one prompt may be in state 'planned' or 'in-progress' at a time; "
                    f"already active: {p.get('id')!r}"
                )

    # Validate parent relationship.
    if prompt_type == "main":
        if parent_id is not None:
            raise ValueError("'parent-id' must be null for type=main")
    else:
        if parent_id is None:
            raise ValueError("'parent-id' is required for type=modification")
        if parent_id not in existing_ids:
            raise ValueError(f"'parent-id' must reference an existing main prompt id: {parent_id}")
        parent_obj = next(
            (p for p in prompts if isinstance(p, dict) and p.get("prompt-id") == parent_id), None
        )
        if not isinstance(parent_obj, dict) or parent_obj.get("type") != "main":
            raise ValueError(f"'parent-id' must reference a prompt with type=main: {parent_id}")

    analysis = _artifact_block(params, "analysis")
    questionnaire = _artifact_block(params, "questionnaire")
    plan = _artifact_block(params, "plan")

    prompt_metadata: Dict[str, Any] = {
        "prompt-id": prompt_id,
        "title": title,
        "type": prompt_type,
        "state": state,
        "parent-id": parent_id,
        "analysis": analysis,
        "questionnaire": questionnaire,
        "plan": plan,
    }

    prompts.append(prompt_metadata)

    # Write JSON first (allocates IDs deterministically), then append prompts registry.
    _dump_json(registry_path, registry)
    _ensure_prompts_registry_record(prompts_registry_path, prompt_id, title)
    _ensure_prompt_workdir_artifacts(workdir, prompt_id, title)

    print(prompt_id)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
