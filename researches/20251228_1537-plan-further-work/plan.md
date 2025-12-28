## h111359: 

How to continue at that stage with the developent of RDD framework. Read all the related specifications and prompts and propose me a detailed plan aligned with the specifications and not realuzed requirements

## GitHub Copilot: 

**Where you are now (observed in repo)**
- ✅ Conventions exist: `work-iteration-registry`, `prompts-registry`, `requirements` formatting.
- ✅ Workdir ops exist: workdir_archive.py, workdir_new_setup.py (but it references a non-existent timestamp script path).
- ✅ Prompt creation exists: prompt_create.py (matches TR-20251225-0350) and seeds `prompts-registry.md`.
- ⚠️ Major pieces are missing/empty: rdd.py (empty), technical-design-form.json (empty), technical-design.json (empty), files-and-folders.md (stub), launchers rdd.sh + rdd.bat (stubs).
- ⚠️ “execute command” currently points to execution.md, but prompt snippets are internally inconsistent/outdated (e.g., execute-work-iteration.prompt.md references legacy `.rdd-instance/workdir/rdd-prompt-setup.json` and `userStories[]`, which does not match your current work-iteration-registry.json schema).

**Key requirement gaps (highest impact)**
- Web UI + server + REST + session token: UR-0904/0917–0922/0931/0935 + TR-0908–0910/0924/0931 (not implemented).
- CLI entrypoint and routing: UR-0914 + TR-0901 (not implemented; rdd.py empty).
- File listing command: UR-0916 + TR-0923 (not implemented).
- Technical design form (config-driven + conditional + defaults): UR-0918/0924/0925 + TR-0907 (config + renderer missing).
- Prompt execution model (“execute command” uses active prompt, loads/updates requirements, deterministic scripts): UR-0903/0905/0910/0912 + TR-0925/0928 (prompt snippets need a canonical v2 that matches your registry conventions).
- Test/CI alignment: UR-0915 + TR-0932–0946 (partially present but paths/filenames don’t match: workflow is tests.yml not `tests.yaml`; runner scripts live in scripts not src; requirements also conflict by asking for BATS/Pester while also saying “no shell frameworks”).

**Two spec conflicts to resolve first (otherwise you’ll build the wrong thing)**
- Archive naming: UR-0909 implies `.rdd-instance/archive/<iteration-id>_<iteration-name>/`, while TR-0927 says `.rdd-instance/archive/<iteration-name>/`. Pick one canonical and update the other requirement with `[DELETED]`/revision.
- Testing tools: UR-0915/TR-0932 say “no third-party shell testing frameworks”, but TR-0940/0943 mandate BATS/Pester. Decide (recommend: remove BATS/Pester requirement and keep Python-only), then update requirements accordingly.

---

## Detailed plan to continue (phased, aligned to unmet requirements)

### Phase 0 — Make the workflow canonical (unblocks everything)
- Produce a “single source of truth” execution spec:
  - Update execution.md to describe the *current* model: active prompt = `state in {planned,in-progress}` in work-iteration-registry.json.
  - Deprecate/replace execute-work-iteration.prompt.md (legacy schema) or rewrite it to the new schema.
- Add/adjust deterministic scripts needed by “execute command” so Copilot isn’t doing file logic:
  - `prompt_text_set.py` (edit text between `%%PROMPT …` / `%%ENDPROMPT`)
  - `prompt_set_state.py` (change prompt state; enforce “single active prompt” invariant)
  - `registry_validate.py` (TR-0925: detect mismatch between JSON registry and `prompts-registry.md`, stop with remediation guidance)
- Fix the hard bug in workdir_new_setup.py (timestamp script path) and add prerequisite checks + clearer remediation (UR-0927/0929/0930).

Acceptance: running “execute command” can reliably identify the active prompt and the exact prompt text, and can fail safely with actionable guidance if registries are inconsistent.

### Phase 1 — Implement the CLI backbone (TR-0901, UR-0914)
- Implement rdd.py as the main command router (domain-based):
  - Domains: `web`, `prompt`, `workdir`, `files`, `spec` (requirements/design/folders), `version`.
  - Interactive menus with curses + numeric fallback (UR-0932).
- Provide wrappers that always use `python` and remain cross-platform (TR-0902).

Acceptance: `python rdd.py --help` works; core actions callable via CLI; errors show cause + remediation (UR-0927).

### Phase 2 — Web server (TR-0908–0910) + REST endpoints (TR-0909)
- Add a Python stdlib server binding `127.0.0.1` on a free port, auto-open browser.
- Generate a session token at startup; require it for all non-read-only operations.
- Implement REST-like endpoints to read/write the framework-managed instance files:
  - requirements.md, `technical-design.json`, files-and-folders.md
  - work-iteration-registry.json, `prompts-registry.md`
  - action endpoints: `workdir/archive`, `workdir/new`, `prompt/create`, `prompt/state`, `files/list`

Acceptance: UI can load/save instance files and invoke commands; all operations are token-protected.

### Phase 3 — Web UI pages (UR-0904/0917–0922/0931/0935, TR-0901)
- Vanilla JS/HTML/CSS app with exactly these pages (per requirements):
  - Prompt Management (active prompt: load/edit/save; questionnaire interaction; plan review + approve/regenerate toggles)
  - Technical Specification (form-driven by technical-design-form.json)
  - File & Folder Structure (view + controlled edit of files-and-folders.md)
  - Requirements (view + controlled edit of requirements.md)
  - Workdir controls (archive iteration, clear workdir, create new iteration)
- Implement color-coded status toasts/banners (success/error/warn/info) and “suggested remediation” messages.

Acceptance: you can complete the main workflow from browser without manual file edits.

### Phase 4 — Technical design form engine (UR-0924/0925, TR-0907)
- Define the schema in technical-design-form.json (fields, defaults, conditional logic).
- Implement “Set Default Answers” (populate only unanswered fields).
- Persist values into technical-design.json.

Acceptance: design file is editable entirely via the form, conditions work, defaults fill correctly.

### Phase 5 — File listing + folder-structure update (UR-0916, TR-0923, prompt snippet update-folder-structure.prompt.md)
- Implement `files_list_generate.py` to write `.rdd-instance/workdir/files-list.json` with required fields + exclusions.
- Implement the folder-structure update command that uses `files-list.json` to update files-and-folders.md deterministically (no “Copilot logic” beyond calling scripts).

Acceptance: `files-list.json` is generated correctly and files-and-folders.md can be refreshed reliably.

### Phase 6 — Reverse-engineer requirements (UR-0908/0923)
- Add a command that analyzes repo + specs to propose requirement additions/changes without duplicating existing content.
- Output proposals into workdir artifacts for review (and only then apply updates).

Acceptance: “missing requirement suggestions” are generated, deduped, and reviewable.

### Phase 7 — Tests + CI alignment (UR-0915, TR-0932–0946)
- Move/duplicate test runner scripts into src (TR-0936) and update workflows to call them.
- Rename workflow to `.github/workflows/tests.yaml` and align steps/paths with TR-0938–0944.
- Decide whether to remove BATS/Pester requirements (recommended) and simplify CI accordingly.

Acceptance: CI runs on PRs to `dev`, produces `coverage.xml`, uploads even on failure, and local `python .rdd/src/run-tests.py` runs everything.

---

## Suggested next prompts to add (to drive work via “active prompt”)
Use prompt_create.py to create these as `type=modification parent-id=P-001`:

- `P-002` (state=`planned`): “Make execute command + registries canonical (rewrite prompt snippets; add registry validation + prompt state/text scripts)”
- `P-003` (state=`draft`): “Implement rdd.py CLI router + core domains + curses fallback”
- `P-004` (state=`draft`): “Add web server + token + REST endpoints; then minimal UI shell with required pages”

If you want, I can take Phase 0 and implement it directly (it’s the biggest unblocker and will immediately make “execute command” coherent with your current registry conventions).