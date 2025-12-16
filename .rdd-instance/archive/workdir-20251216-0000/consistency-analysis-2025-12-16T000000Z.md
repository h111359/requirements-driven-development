# Consistency Analysis (RDD)

## Timestamp

2025-12-16T000000Z

## Scope

Folders (recursive):
- `.rdd-instance/specifications/`
- `.rdd/conventions/`
- `.rdd/prompt-snippets/`
- `.rdd/prompt-templates/`
- `.rdd/templates/`
- `.rdd/docs/`

Individual files:
- `.rdd-instance/requirements.md`
- `.github/prompts/rdd.execute.prompt.md`
- `.rdd/manifest.json`

## Coverage & Gaps

### Coverage table

| Scope item | Discovered | Read/Reviewed | Notes |
|---|---:|---:|---|
| `.rdd-instance/specifications/` | 10 files | 1/10 read; structure inventoried | Only filenames were enumerated; individual spec contents were not read unless referenced by other in-scope docs. |
| `.rdd/conventions/` | 5 files | 5/5 read | Fully reviewed. |
| `.rdd/prompt-snippets/` | 7 files | 7/7 read | Fully reviewed. |
| `.rdd/prompt-templates/` | 5 files | 5/5 read | Fully reviewed. |
| `.rdd/templates/` | 6 files | 6/6 read | Fully reviewed. |
| `.rdd/docs/` | 2 files | 2/2 read | Fully reviewed (note: `user-guide.md` appears truncated/empty at head). |
| `.rdd-instance/requirements.md` | 1 file | 1/1 read (partial) | Reviewed lines 1–260 (file has 339 lines). |
| `.github/prompts/rdd.execute.prompt.md` | 1 file | 1/1 read | Fully reviewed (short). |
| `.rdd/manifest.json` | 1 file | 1/1 read | Fully reviewed. |

### Gaps / unreadable / not accessed

- **Partial read:** `.rdd-instance/requirements.md` (reviewed lines 1–260 of 339). Some findings below may be incomplete if relevant content exists after line 260.
- **Not read (by content):** `.rdd-instance/specifications/*.md` and `.rdd-instance/specifications/technical-design.json` contents were not opened during this run; only enumerated.

## Findings (Prioritized)

### F-001

- **Severity:** **Critical**
- **Title:** `.rdd/manifest.json` is invalid JSON due to mismatched braces in `upgradePolicy.rules`
- **Evidence:**
  - `.rdd/manifest.json` excerpt:
    - `"upgradePolicy": { ... "rules": [ ... { "path": ".rdd-instance/archive/**", "action": "preserve"}      }
    - The array is not closed properly and there is an extra `}`.
- **Why it matters:**
  - Any tooling that parses the manifest for validation/installation/upgrade decisions will fail outright.
  - Downstream prompts reference manifest concepts (required paths/files, workdir model, upgrade policy); if the manifest is unparsable, those rules can’t be reliably enforced.
- **Recommendation:**
  - Fix the JSON structure of `upgradePolicy.rules` so it is a valid JSON array and the object is properly closed.
  - Add a minimal JSON validation step to framework tests/build (e.g., parse manifests in CI).
- **Risk/Tradeoffs:**
  - Low risk: purely structural fix. Possible risk if consumers currently ignore `upgradePolicy` due to parse failure; fixing may “activate” behavior that was never applied.

### F-002

- **Severity:** **High**
- **Title:** Ownership policy conflict: `workdir` is declared overwrite-on-upgrade but prompts and workflows treat it as active user work state
- **Evidence:**
  - `.rdd/manifest.json`:
    - `instanceRuntimeState` → paths `.rdd-instance/workdir/**` → `policy": "overwriteOnUpgrade"`
    - `workdirModel.clearworkdirAfterArchive": true`
  - `.rdd/conventions/work-iteration-registry.convention.md`:
    - “The registry is the single source of truth for the current work-iteration’s progress...”
  - `.rdd/prompt-templates/compare-requirements.prompt.md`:
    - Instructs writing comparison output into `.rdd-instance/workdir/compare-requirements.md`.
- **Why it matters:**
  - If upgrades overwrite workdir, an in-progress iteration (registry, prompt, questionnaire, plan, implementation logs) can be destroyed.
  - This is especially risky because several prompts explicitly store artifacts in workdir, making it the default working location.
- **Recommendation:**
  - Clarify the intended lifecycle:
    - If workdir is ephemeral runtime state: ensure upgrades are blocked while work is active OR auto-archive before upgrade.
    - If workdir is user-authored work artifacts: change policy to preserve by default.
  - Document this clearly in `.rdd/docs/user-guide.md` and/or manifest comments.
- **Risk/Tradeoffs:**
  - Medium risk: changing upgrade semantics affects installations. Auto-archiving may be safer but needs careful implementation.

### F-003

- **Severity:** **High**
- **Title:** Execute prompt selects between `execute-task` and `execute-work-iteration`, but `execute-task.prompt.md` still describes legacy single-prompt workflow (not task queue)
- **Evidence:**
  - `.github/prompts/rdd.execute.prompt.md`:
    - If `mode` is `task`, follow `.rdd/prompt-templates/execute-task.prompt.md`.
  - `.rdd/prompt-templates/execute-task.prompt.md`:
    - Title is `# Execute Work Iteration Prompt` (misleading)
    - Uses global registry keys like `clarity.state`, `plan.state`, `implementation.state` directly under `[WI-REGISTRY]`.
  - `.rdd/conventions/work-iteration-registry.convention.md`:
    - Task queue lives under `tasks.Tasks-List` and selection is `active.active-task-id`.
- **Why it matters:**
  - In `task` mode, the framework expects executing a selected task, but the executor prompt doesn’t define mapping between `active-task-id` and task object fields, nor where the task prompt text comes from.
  - This can cause an agent to modify the wrong state keys or follow a non-existent workflow.
- **Recommendation:**
  - Rewrite `.rdd/prompt-templates/execute-task.prompt.md` to be task-mode specific:
    - Define `[TASK]` as the object in `tasks.Tasks-List` whose `task-id` equals `active.active-task-id`.
    - Define where prompt text comes from (e.g., task description vs a referenced file).
    - Define stage tracking for tasks (either reuse a per-task stage structure or specify minimal fields).
  - Fix the title to `# Execute Task Prompt`.
- **Risk/Tradeoffs:**
  - Medium: affects core execution behavior. But leaving it inconsistent is higher risk (agent errors).

### F-004

- **Severity:** **High**
- **Title:** Multiple documents define different “prompt text source” (`work-iteration-prompt.md` vs user story `prompt-file`)
- **Evidence:**
  - `.rdd/prompt-templates/execute-work-iteration.prompt.md`:
    - `[PROMPT-TEXT]` is “full content of the file referenced by `[USER-STORY].prompt-file`”.
  - `.rdd/prompt-snippets/execution-step.plan.md`:
    - `[PROMPT-TEXT]` is “the content of the file `.rdd-instance/workdir/work-iteration-prompt.md`”.
  - `.rdd/prompt-snippets/execution-step.implementation.md`:
    - Same: `.rdd-instance/workdir/work-iteration-prompt.md`.
  - `.rdd/prompt-snippets/execution-step.context.md`:
    - `[PROMPT-TEXT]` is “the content of the file in the attribute prompt-file ... under userStories ...”.
- **Why it matters:**
  - In `userStory` mode, executor template resolves prompt from `userStories[].prompt-file`, but plan/implementation snippets still point at the legacy work-iteration file.
  - Agents following snippets will read the wrong file and mis-execute instructions.
- **Recommendation:**
  - Make snippets parameterized and consistent:
    - Define `[PROMPT-TEXT]` as “content of the active prompt file” and define `[PROMPT-FILE]` earlier by mode.
    - Or maintain separate snippet sets for `userStory` vs `task`.
  - Update all snippet definitions to avoid hardcoding `.rdd-instance/workdir/work-iteration-prompt.md`.
- **Risk/Tradeoffs:**
  - Medium: touches multiple prompt assets; but it’s mostly text changes and improves safety.

### F-005

- **Severity:** **High**
- **Title:** `execute-work-iteration.prompt.md` includes conflicting “never change work-iteration-prompt.md” rule even though it may not be used in userStory mode
- **Evidence:**
  - `.rdd/prompt-templates/execute-work-iteration.prompt.md` Mandatory Rules:
    - “Never change the `.rdd-instance/workdir/work-iteration-prompt.md` file!... treat it as legacy and ignore it unless `[USER-STORY].prompt-file` points to it explicitly.”
- **Why it matters:**
  - In the common path described by the same file, the prompt text source is `[USER-STORY].prompt-file`. Declaring “never change work-iteration-prompt.md” is irrelevant and can confuse agents.
  - It also creates a potential contradiction with `.rdd/templates/work-iteration-prompt.md` (seed) and config `work-iteration-prompt` being enabled.
- **Recommendation:**
  - Clarify the rule’s applicability:
    - Either remove it from userStory mode execution, or gate it under “legacy mode only”.
  - Align `.rdd/templates/config.json` `specifications.work-iteration-prompt.enabled` with the intended modern workflow.
- **Risk/Tradeoffs:**
  - Low-medium: prompt wording change; main risk is breaking backward compatibility with older installs—mitigate by documenting legacy path.

### F-006

- **Severity:** **Medium**
- **Title:** State value inconsistency: snippets set `clarity.state` to `answered` / `done`, while conventions only explicitly mention `not-started` (others optional)
- **Evidence:**
  - `.rdd/conventions/work-iteration-registry.convention.md`:
    - `state` allowed values: `not-started` and “other values may be introduced ...”.
  - `.rdd/prompt-snippets/execution-step.plan.md`:
    - sets `clarity.state` to `answered`.
  - `.rdd/prompt-snippets/execution-step.questionnaire.md`:
    - sets `clarity.state` to `done`.
  - `.rdd/prompt-templates/execute-work-iteration.prompt.md`:
    - expects `clarity.state` values: `ready-to-start`, `generated`.
- **Why it matters:**
  - The executor decides which step to run based on exact string matches; inconsistent state labels can cause steps to be skipped forever or repeated.
- **Recommendation:**
  - Define a canonical finite set of states (per stage) in `.rdd/conventions/work-iteration-registry.convention.md`.
  - Update all templates/snippets to use the same state names (`not-started`, `ready-to-start`, `generated`, `done`, etc.).
- **Risk/Tradeoffs:**
  - Medium: changing state strings may break existing registries; consider migration guidance.

### F-007

- **Severity:** **Medium**
- **Title:** `Questions Formatting Guide` includes emoji symbols despite some environments expecting plain Markdown; also symbol list may be over-prescriptive
- **Evidence:**
  - `.rdd/conventions/questions-formatting.md`:
    - “Use symbols to convey meaning quickly” including `ℹ️`, `⚠️`, `📝`.
- **Why it matters:**
  - For cross-platform environments (some terminals/fonts) emoji can render poorly.
  - Some prompts/templates elsewhere do not use these symbols, creating format drift.
- **Recommendation:**
  - Mark emojis as optional enhancements and provide ASCII-only fallback equivalents.
- **Risk/Tradeoffs:**
  - Low.

### F-008

- **Severity:** **Medium**
- **Title:** Typo/terminology drift: `arcitecture-decision-record` key in `.rdd/templates/config.json`
- **Evidence:**
  - `.rdd/templates/config.json`:
    - `"arcitecture-decision-record": { "path": ".rdd-instance/specifications/architecture-decision-records.md" }`
- **Why it matters:**
  - Misspelled keys make it harder for tools and prompts to reference specifications consistently.
  - Context gathering snippet expects iterating `specifications` object to find enabled specs; a misspelling in keys may be tolerable but signals drift.
- **Recommendation:**
  - Rename key to `architecture-decision-records` (or similarly consistent), and if backward compatibility matters, support both keys in tooling.
- **Risk/Tradeoffs:**
  - Medium: renaming config keys can break scripts; requires migration.

### F-009

- **Severity:** **Low**
- **Title:** `.rdd/docs/user-guide.md` appears empty/truncated
- **Evidence:**
  - `.rdd/docs/user-guide.md` currently only shows header lines and then ends (as read).
- **Why it matters:**
  - User-facing guidance is missing; other docs (like `design-notes.md`) contain structure but not operational how-to.
- **Recommendation:**
  - Populate user guide with minimal steps: how to initialize, how to run execute command, how to manage workdir/registry.
- **Risk/Tradeoffs:**
  - Low.

### F-010

- **Severity:** **Nit**
- **Title:** Multiple spelling/grammar issues in templates/snippets reduce clarity (e.g., “impement”, “aks”, “furhter”, “promt”)
- **Evidence:**
  - `.rdd/prompt-snippets/execution-step.implementation.md`: “impement”
  - `.rdd/prompt-snippets/execution-step.questionnaire.md`: “aks the user”
  - `.rdd/prompt-templates/execute-work-iteration.prompt.md`: “furhter”
  - `.rdd/docs/design-notes.md`: “Depoloyement”, “worklow”, etc.
- **Why it matters:**
  - Small but pervasive typos can cause misinterpretation by agents/users and make the framework appear less trustworthy.
- **Recommendation:**
  - Run a spelling pass on prompt assets; keep it conservative to avoid changing semantics.
- **Risk/Tradeoffs:**
  - Low.

## Cross-Reference Check Summary

### Broken references (within scope)

- None conclusively verified as broken by existence checks, however see “Suspicious references” below.

### Suspicious references (verify)

- `.rdd/prompt-snippets/execution-step.plan.md` and `.rdd/prompt-snippets/execution-step.implementation.md` reference `.rdd-instance/workdir/work-iteration-prompt.md` as prompt text source, which conflicts with user story execution pathway.
- `.rdd/prompt-templates/execute-task.prompt.md` title and content suggests it’s not a task-mode executor.

## Redundancy & Source-of-Truth Map

### Work iteration execution semantics

- Canonical registry shape: `.rdd/conventions/work-iteration-registry.convention.md`
- Execute entrypoint routing by mode: `.github/prompts/rdd.execute.prompt.md`
- User story executor: `.rdd/prompt-templates/execute-work-iteration.prompt.md`
- Task executor (currently inconsistent): `.rdd/prompt-templates/execute-task.prompt.md`
- Stage logic details: `.rdd/prompt-snippets/execution-step.*.md` (but these currently mix legacy and new prompt sources)

### Requirements file format

- Format guide: `.rdd/conventions/requirements-format.md`
- Requirements instance: `.rdd-instance/requirements.md`

### Files/folders documentation

- Convention: `.rdd/conventions/files-and-folders.convention.md`
- Update procedure: `.rdd/prompt-templates/update-folder-structure.prompt.md`
- Project doc target: `.rdd-instance/specifications/files-and-folders.md` (not reviewed by content)

### Ownership/upgrade/workdir model

- Declared: `.rdd/manifest.json` (currently invalid JSON)
- Implied usage: prompt templates and snippet instructions (write many artifacts into workdir)

## Suggested Next Actions

- [ ] Fix invalid JSON in `.rdd/manifest.json` and add a JSON-parse validation test.
- [ ] Align prompt source-of-truth across templates/snippets (remove hardcoded legacy `.rdd-instance/workdir/work-iteration-prompt.md` where not applicable).
- [ ] Redesign `.rdd/prompt-templates/execute-task.prompt.md` to actually execute `active.active-task-id` from `tasks.Tasks-List`.
- [ ] Define a canonical set of stage state values and update all prompts/snippets accordingly.
- [ ] Decide and document the intended upgrade behavior for `.rdd-instance/workdir/**` to avoid data loss.
