++ mkdir mode 0755
++ file mode 0644
```markdown
# Requirements Comparison: docs/ProductRequirementsSpecification.md

This document compares the Product Requirements Specification at
`docs/ProductRequirementsSpecification.md` (PRS) with the framework's
authoritative requirements at `.rdd-docs/requirements.md` (RDD Requirements).

## Summary (one-line)

Major divergences: PRS mandates a browser-based web UI and a single-file
`work-iteration-prompt.md` model, while `.rdd-docs/requirements.md` and
templates use a CLI/curses/numeric-menu model with `work-iteration-prompts.md`
(plural) and expect prompts in `.github/prompts/`. Several structural and
storage conventions differ and require a reconciliation decision.

## Files & artifacts observed in repo (quick map)

- `.github/prompts/rdd.execute.prompt.md` — present (supports an `rdd.execute` prompt)
- `.rdd/prompts/` — contains prompt files (e.g. `compare-requirements.prompt.md`)
- `.rdd-docs/requirements.md` — authoritative RDD requirements (source of truth for framework)
- `.rdd-docs/tech-spec.md` — technical specification referenced by requirements
- `templates/user-guide.md` — references `.rdd-docs/work-iteration-prompts.md`
- `templates/work-iteration-prompts.md` — seed template referenced in tech-spec and requirements
- tests/install/test_install.py, install/install.py, run-tests.py — test and installer artifacts

## Comparison result structure

Sections below follow the requested structure from the compare prompt:

- Missing Requirements in either document
- Inconsistent Requirements
- Additional Requirements in either document

---

## 1) Missing Requirements

1. Missing in `.rdd-docs/requirements.md` (present in PRS)

   - Web-based UI (local web portal) for prompt management and multiple UI pages
     (Prompt Management, Technical Specification, File/Folder Structure, Requirements,
     Version Control & Workspace, Administration). PRS requires a server + browser
     UI and automatic opening in default browser. The RDD requirements emphasize
     terminal-based interactive menus, curses, and Tkinter for installer GUI, but
     do not specify a browser-based web UI.

   - Structured Technical Design JSON and design configuration JSON (PRS requires
     tech design stored as structured JSON and a corresponding configuration JSON
     to drive UI forms). RDD requirements use `tech-spec.md` (Markdown) and do not
     require a design JSON format.

   - The PRS-specific single active prompt file name `work-iteration-prompt.md`
     (singular) under `.rdd-docs/`. RDD uses `work-iteration-prompts.md` (plural)
     in templates, tech-spec, and user-guide.

2. Missing in `docs/ProductRequirementsSpecification.md` (present in `.rdd-docs/requirements.md`)

   - Detailed workspace management behaviors: automatic backups (`.rdd-docs/workspace/.backups/`),
     explicit archive metadata format (`.archive-metadata` with fields: archivedAt, branch name, archivedBy, lastCommit, lastCommitMessage), copying vs moving behavior on archive.

   - Wrap-up and sync safety behaviors: auto-commit before sync, fetch from default branch before merging, conflict detection halting wrap-up, user notification on conflicts, pre-merge validation.

   - Many low-level TR / FR items (e.g., automatic ID assignment for added requirements, file template locations `.rdd/templates/`, prompts stored in `.github/prompts/` per TR-12, scripts in `.rdd/scripts/`, explicit CLI domains, test framework preferences, build/archive naming and checksum rules) that are spelled out in `.rdd-docs/requirements.md`.

   - Explicit `python` vs `python3` invocation guidance and cross-platform installer behavior (detailed in TR-30, FR-48, FR-53 and related items).

---

## 2) Inconsistent Requirements (conflicts or naming/location mismatches)

1. Prompt storage location

   - PRS: "A folder named `.rdd/prompts` must store predefined prompt files." (docs/ProductRequirementsSpecification.md)
   - RDD requirements (TR-12): "All prompt files shall be stored in `.github/prompts/`"

   Repo state: both `.rdd/prompts/` and `.github/prompts/rdd.execute.prompt.md` exist. This is an inconsistency that must be resolved by policy: which location is canonical for runtime execution vs authoring or packaging?

2. Work-iteration prompts file name & multiplicity

   - PRS: requires a single active file `work-iteration-prompt.md` (singular) containing exactly one prompt.
   - RDD requirements and templates: use `work-iteration-prompts.md` (plural) and the system supports lists of prompts, P IDs sequencing, and multiple prompts per iteration.

   Effect: tools, templates, and tests reference the plural name; PRS uses singular. This causes automated tooling to read/write different filenames and may break `execute` workflows.

3. UI model: Web UI vs Terminal/GUI

   - PRS: mandates browser-based UI (local web server + pages).
   - RDD requirements: rely on interactive terminal menus, numeric menu fallback, curses-based UI, and for installer a Tkinter GUI. No web UI is specified.

   Effect: implementation approach, architecture, and testing change significantly depending on chosen model.

4. Execute command / invocation model

   - PRS: single command `execute` and an rdd.execute prompt file model.
   - RDD requirements: domain-based CLI commands (`python .rdd/scripts/rdd.py <domain> <action>`), plus `rdd.execute` prompt exists in repo. The exact mechanism for invoking `execute` vs domain CLI is not fully aligned.

5. Technical design storage

   - PRS: expects Technical Design as structured JSON + design configuration JSON to drive UI.
   - RDD: technical documentation stored in `tech-spec.md` (Markdown), and many TR/FR items expect text files and templates.

---

## 3) Additional Requirements (present in one doc only)

1. Present only in PRS (not in `.rdd-docs/requirements.md`)

   - Full web portal with multiple pages (Prompt Management, Technical Spec editor, File/Folder visualizer, Requirements page with reverse-engineering, Version Control & Workspace management page, Administration page).

   - UI-driven JSON technical design editing with conditional logic and "Set Default Answers" functionality.

   - Explicit requirement that prompts be authored in a Web UI and persisted in Markdown and that the browser UI may be used instead of manual edits.

2. Present only in `.rdd-docs/requirements.md` (not in PRS)

   - Very detailed workflow and safety items: auto-commit before sync, pre-wrap-up merge/fetch from default, conflict detection and user notices, backup and restore semantics, archive metadata structure, P ID allocation rules, template locations, installer details, build artifact checksum and naming rules, test framework expectations (pytest, BATS, Pester), and many TR items.

   - Specific non-functional items like colored CLI output, progress indicators, data preservation during re-execution, and editor settings (VS Code rulers, JSONL association).

---

## 4) Mapping to repo artifacts / tests (quick trace)

- `docs/ProductRequirementsSpecification.md` — PRS being compared
- `.rdd-docs/requirements.md` — RDD requirements (source)
- `.github/prompts/rdd.execute.prompt.md` — PRS's `execute` concept is partially present here
- `.rdd/prompts/*` — authoring prompts found here (repo contains this folder)
- `templates/work-iteration-prompts.md` and `templates/user-guide.md` — point to `work-iteration-prompts.md` (plural)
- `.rdd-docs/tech-spec.md` — technical spec (Markdown) in repo (no JSON design files found)
- `install/install.py`, `run-tests.py`, `tests/install/test_install.py` — installer and tests exist, reflecting many RDD FR/TR items

Missing test/artifact mappings (gaps)

- No web UI code (no server or web assets found) and no tests for web UI pages.
- No technical-design JSON files or design configuration JSON; no tests validating JSON-driven UI.
- Conflicting prompt storage locations—no test that asserts canonical prompt folder.

## 5) Recommendations & Next Steps (practical)

1. Decide canonical prompt storage and work-iteration filename

   - Option A (minimal change): Accept current RDD requirements as canonical: keep `work-iteration-prompts.md` (plural) and canonical prompt folder `.github/prompts/`. Update PRS to reflect this and remove web-UI-only statements.

   - Option B (move to PRS): If web UI is desired, update the RDD requirements to include web UI requirements (new TR/FR entries) and add an explicit migration plan for `work-iteration-prompts.md` -> `work-iteration-prompt.md` (or provide a compatibility shim).

2. Reconcile `execute` invocation model

   - Define runtime contract: are prompts executed by a domain CLI (`python .rdd/scripts/rdd.py prompt execute`) or by issuing a single `execute` command that integrates with `.github/prompts/rdd.execute.prompt.md`?

   - Add a small compatibility layer if both models must be supported (e.g., `rdd.execute` plug-in that calls the domain CLI).

3. If web UI is approved, scope and start with an MVP

   - MVP: a small local web server that can read/write `work-iteration-prompts.md` (or the chosen canonical file) and display the generated implementation file(s). Create tests that mock filesystem and verify read/write behavior. Add design JSON schema later if needed.

4. Create targeted tests and docs for the chosen approach

   - Add unit/integration tests for: prompt file canonicalization, execute invocation, workspace archiving and `.archive-metadata` format, backup/restore, and ID allocation rules. If web UI adopted, add web UI integration tests and static asset checks.

5. Quick tactical changes (low risk)

   - Add a short note to `docs/ProductRequirementsSpecification.md` or `.rdd-docs/requirements.md` clarifying canonical prompt folder and work-iteration file name to avoid tooling breakage.

---

## 6) Clarifications requested (questions for product author)

1. Which is canonical: `.rdd/prompts/` or `.github/prompts/` for installed/packaged prompts? Are both needed (authoring vs installed runtime)?
2. Which work-iteration file name should be canonical: `work-iteration-prompt.md` (singular) or `work-iteration-prompts.md` (plural)? If singular, do we need a migration path for existing templates/tests?
3. Do you require a browser-based web UI as mandatory, optional, or out-of-scope for the initial release? If mandatory, shall we add Technical Design JSON now or later?
4. Which command invocation should be the developer-facing single command: `execute` (as in PRS) or domain CLI entrypoints under `rdd.py`? Is a wrapper acceptable?

---

## 7) Completion

This comparison file was produced by comparing `docs/ProductRequirementsSpecification.md`
against `.rdd-docs/requirements.md` and repo artifacts. Next step: please indicate
which of the reconciliation options above you'd like to pursue (minimal-change vs
web-UI-first). I can then implement the small low-risk changes (notes, compatibility
shim, and tests) in a follow-up.

```