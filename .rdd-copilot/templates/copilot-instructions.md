# RULES

## 1. Scope of Automated Changes
The assistant MAY create, modify, and clarify Change Request files (`*.cr.md`) and Task files (`*.task.md`), as well as update the CR and Task catalog files, WHEN such actions are explicitly triggered by invoking a prompt file under `.github/prompts/` (e.g., clarification, design, planning prompts). For all other code or documentation changes outside this CR/Task domain, a task file in `.rdd-docs/tasks/` is still required.

## 2. Prompt-Driven Exceptions
When a user invokes a prompt in `.github/prompts/` whose documented workflow includes editing CRs or tasks (e.g., `rdd-copilot.cr-clarify.prompt.md`, `rdd-copilot.cr-design.prompt.md`, future planning prompts), the assistant is AUTHORIZED to:
1. Create new CR files following naming pattern: `YYYYMMDD-HHmm-short-description.cr.md`.
2. Create new Task files following naming pattern: `YYYYMMDD-HHmm-short-description.task.md`.
3. Update catalog entries in `.rdd-docs/change-requests/cr-catalog.md` and `.rdd-docs/tasks/tasks-catalog.md` (status transitions, timestamps, links).
4. Append structured sections (Clarification Log, Clarifications, Parking Lot, Risks, etc.) inside the selected CR file.
5. Transition statuses per prompt rules (e.g., Draft -> Clarifying -> Clarified -> Ready for Design) without a separate task file.

## 3. Safeguards & Prohibited Actions
The assistant MUST NOT modify non-CR/non-Task source code, infrastructure definitions, or unrelated documentation unless a dedicated task file authorizes it. If the user requests such changes during a prompt-driven CR/Task workflow, the assistant will respond with a reminder to create an appropriate task file.

## 4. Additive Logging Principle
All modifications to CR files must be additive: never delete prior clarification entries or overwrite original problem/value statements. Use timestamped entries (`- [YYYY-MM-DD HH:MM]`) in chronological order.

## 5. Transparency
Before performing prompt-driven catalog or file edits, the assistant should briefly state the intended changes (plan summary) and then apply them; after  changes, summarize what was updated (statuses, files touched, sections added).

## 6. Quality & Formatting
Maintain clear, modular, and well-documented structure inside CR and Task files. Preserve naming patterns, consistent timestamp formatting (`YYYYMMDD-HHmm` for IDs; `YYYY-MM-DD HH:MM` for log lines), and required sections defined by prompt workflows.

## 7. Conflict Handling
If catalog status or file contents contradict the prompt workflow (e.g., a CR marked Clarified but missing acceptance criteria), assistant may flag inconsistency, propose corrective steps, and—if user confirms—apply corrective edits under the same prompt session.

## 8. Temporal Notes
If current iteration date differs from original CR filename date, append a `Temporal Notes` subsection citing the discrepancy (do NOT rename existing file unless explicitly tasked).

## 9. Catalog Integrity
Never remove historical rows. Status transitions must update the `Updated` date; final clarification adds `DateClarified` (if field exists) or notes in Decision/Log column per catalog format.

## 10. Task File Authorization (Non-Prompt Context)
Outside an active prompt session originating from `.github/prompts/`, any change (even CR/Task edits) still requires a corresponding task file for traceability.

---

# INSTRUCTIONS

1. Reference `.rdd-docs/folder-structure.md` for expected directory layout when creating new CR or Task files.
2. Consult `.rdd-docs/requirements.md` and `.rdd-docs/README.md` for overarching repository governance.
3. Follow each prompt file's embedded workflow strictly—do not introduce implementation details during clarification stages.
4. Use additive markdown sections (avoid rewriting existing headers unless fixing typos explicitly requested via task file).
5. For new CR creation: include initial sections (Who, What, Why, Acceptance Criteria, Additional Considerations) minimally before starting clarification.
6. For task files: capture Action, Related CR (if applicable), Constraints, Acceptance, and Timestamp ID.
7. After every status-changing edit, re-read the catalog to ensure consistency; correct if needed (add note if mismatch cannot be immediately resolved).
