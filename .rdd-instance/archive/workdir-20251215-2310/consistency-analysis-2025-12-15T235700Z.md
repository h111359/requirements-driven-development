# Consistency Analysis (RDD)

## Timestamp

2025-12-15T141530Z

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

### Coverage inventory

| Scope item | Files discovered | Notes |
|---|---:|---|
| `.rdd-instance/specifications/` | 10 | `deployment.md`, `components.md` contain only headings; `infrastructure.md` is empty |
| `.rdd/conventions/` | 5 | Read all |
| `.rdd/prompt-snippets/` | 7 | Read all |
| `.rdd/prompt-templates/` | 5 | Read all |
| `.rdd/templates/` | 6 | Read all |
| `.rdd/docs/` | 2 | `user-guide.md` appears truncated/empty after header within first 260 lines; `design-notes.md` read |
| `.rdd-instance/requirements.md` | 1 | Read through line ~260; file continues beyond |
| `.github/prompts/rdd.execute.prompt.md` | 1 | Read all |
| `.rdd/manifest.json` | 1 | Read all |

### Gaps / unreadable content

- No files were unreadable (permissions).
- **Potential gap:** `.rdd/docs/user-guide.md` returned only a header and blank space in the captured range.
  - Evidence: `.rdd/docs/user-guide.md` starts with `# RDD Framework User Guide` and then no additional content observed in lines 1–260.
  - This could mean the file is intentionally short, or content exists beyond line 260.

### Out-of-scope but observed (not analyzed)

Some references in in-scope files point to locations outside the declared scope (e.g., `.rdd/scripts/rdd.py`, `.rdd-instance/config.json`, `.rdd/templates/questions-formatting.md`). These are treated as external dependencies; I cite the references but do not analyze those out-of-scope files.

## Findings (Prioritized)

### F-001

- **Severity:** **Critical**
- **Title:** Execute entry prompt dispatches on legacy `mode="prompt"`, but the canonical registry uses `mode="userStory"` / `"task"`
- **Evidence:**
  - `.github/prompts/rdd.execute.prompt.md`:
    - `- If the "mode" is "prompt", follow the instructions in `.rdd/prompt-templates/execute-work-iteration.prompt.md`.'`
    - `- Else If the "mode" is "task", follow the instructions in `.rdd/prompt-templates/execute-task.prompt.md`.
  - `.rdd/conventions/work-iteration-registry.convention.md`:
    - `Allowed values: userStory, task`
  - `.rdd-instance/workdir/work-iteration-registry.json`:
    - `"mode": "userStory"`
- **Why it matters:**
  - This breaks the *main execution entrypoint* path: users following the execute prompt will hit “unrecognized mode” even when the registry is valid per the convention and the current seeded registry.
  - Because `.github/prompts/rdd.execute.prompt.md` is labeled as the single entry prompt in `.rdd/manifest.json`, this is a workflow-stopper.
- **Recommendation:**
  - Update `.github/prompts/rdd.execute.prompt.md` dispatch logic to:
    - If mode is `userStory` → execute `.rdd/prompt-templates/execute-work-iteration.prompt.md`
    - If mode is `task` → execute `.rdd/prompt-templates/execute-task.prompt.md`
  - Consider a backward-compatibility note: accept `prompt` as an alias for `userStory` *only if you still support legacy registries*.
- **Risk/Tradeoffs:**
  - Low risk if the framework has already migrated to userStory/task.
  - If users still have old registries with `mode=prompt`, you either need dual support or a migration step.

### F-002

- **Severity:** **Critical**
- **Title:** `.rdd/templates/work-iteration-registry.json` is incompatible with the registry convention and the current live registry
- **Evidence:**
  - `.rdd/templates/work-iteration-registry.json`:
    - Contains `"PROMPT-ID"`, `"PROMPT-NAME"`, and `"mode": "prompt"` with top-level `context/clarity/plan/implementation`.
  - `.rdd/conventions/work-iteration-registry.convention.md`:
    - Defines top-level keys: `mode` in `{userStory, task}`, plus `active`, `userStories[]`, `tasks`, and stage sections per-user-story.
  - `.rdd-instance/workdir/work-iteration-registry.json`:
    - Matches the convention shape (has `active`, `userStories`, `tasks`).
- **Why it matters:**
  - The template is used as a seeding / reference artifact; if incorporated into installation or docs, it will produce a registry shape that the execute workflow cannot interpret.
  - This also creates two competing “sources of truth” (template vs convention) for the registry schema.
- **Recommendation:**
  - Align `.rdd/templates/work-iteration-registry.json` to the canon example in `.rdd/conventions/work-iteration-registry.convention.md`.
  - Alternatively, if you intentionally support two schemas, explicitly version them and document the migration.
- **Risk/Tradeoffs:**
  - Medium risk if scripts/UI still expect the legacy `PROMPT-ID` fields.
  - If legacy scripts exist, you’ll need a compatibility layer or a one-time migration.

### F-003

- **Severity:** **High**
- **Title:** `.rdd/templates/config.json` and `.rdd-instance/config.json` reference non-existent or mismatched paths (`work-iteration-registry.md` vs `.json`) and missing convention files
- **Evidence:**
  - `.rdd/templates/config.json`:
    - `"path": ".rdd-instance\\workdir\\work-iteration-registry.md"` (but the registry file is `.json`)
    - `"conventions-file": ".rdd\\conventions\\concepts-format.md"` (file not present in `.rdd/conventions/`)
  - `.rdd-instance/config.json`:
    - Also points to `work-iteration-registry.md` and `work-iteration-registry-format.md`.
  - `.rdd/manifest.json` requiredFiles:
    - Requires `.rdd-instance/workdir/work-iteration-registry.json`
  - Workspace observation:
    - The actual registry file present is `.rdd-instance/workdir/work-iteration-registry.json`.
- **Why it matters:**
  - Agents and the Web UI (per `.rdd/prompt-snippets/execution-step.context.md`) are instructed to use `.rdd-instance/config.json` to discover enabled specs; if those spec paths are wrong, context gathering and workflow automation will miss key files.
  - This increases the chance the agent reads/writes the wrong artifact (`.md` vs `.json`).
- **Recommendation:**
  - Normalize spec paths to use POSIX `/` and correct extensions, at least for:
    - `work-iteration-registry` → `.rdd-instance/workdir/work-iteration-registry.json`
  - Ensure `conventions-file` values point to actual in-repo convention files (or remove the field when unused).
  - If `concepts` is a planned feature, add the missing `.rdd/conventions/concepts-format.md` and `.rdd-instance/concepts.md` (or disable concepts until implemented).
- **Risk/Tradeoffs:**
  - Medium: could impact any existing scripts/UI that expect `.md` registry paths.
  - But since manifest and workdir already use `.json`, this likely fixes an actual bug.

### F-004

- **Severity:** **High**
- **Title:** Path separator inconsistency (Windows `\\` used in JSON configs) conflicts with cross-platform Linux expectations and repo-wide POSIX examples
- **Evidence:**
  - `.rdd-instance/config.json` and `.rdd/templates/config.json` use `".rdd-instance\\workdir\\..."`.
  - Multiple docs, prompts, and manifest use POSIX-style paths, e.g. `.rdd-instance/workdir/work-iteration-registry.json` in `.rdd/manifest.json`.
- **Why it matters:**
  - On Linux/macOS, backslash-heavy paths can be treated as literal characters in many contexts and will not resolve as file system paths.
  - Agents may follow those paths literally, leading to “file not found” behavior.
- **Recommendation:**
  - Standardize stored file paths in JSON to POSIX `/` (recommended for cross-platform tooling) and convert in platform-specific layers if needed.
  - If Windows is a strict target, document that all internal paths are POSIX and must be normalized by scripts.
- **Risk/Tradeoffs:**
  - Low to medium: if any Windows-only code treats backslashes as required, you’ll need path normalization.

### F-005

- **Severity:** **High**
- **Title:** Specs and ADRs reference a prompt library directory `.rdd/prompts/` that doesn’t exist in the framework layout (prompt templates/snippets are in different folders)
- **Evidence:**
  - `.rdd-instance/specifications/front-end.md`:
    - `Lists all .md files in .rdd/prompts/`
  - `.rdd-instance/specifications/architecture-decision-records.md`:
    - `[ADR-009] Prompt templates ... are stored in .rdd/prompts/.`
  - Workspace structure:
    - In-scope framework prompt storage is `.rdd/prompt-templates/` and `.rdd/prompt-snippets/`.
- **Why it matters:**
  - Misleading specs can cause the Web UI implementation to look in the wrong directory and fail to find templates.
  - This creates confusing “competing truths” about the canonical prompt library location.
- **Recommendation:**
  - Decide a single canonical prompt library root:
    - either keep current `.rdd/prompt-templates/` and update specs/ADRs accordingly,
    - or reintroduce `.rdd/prompts/` (and update manifest + requiredPaths).
- **Risk/Tradeoffs:**
  - Medium: changing directory conventions can affect existing users and automation.

### F-006

- **Severity:** **Medium**
- **Title:** Requirements say “All RDD framework operations shall be implemented in Python”, but specs mention legacy Bash/PowerShell script locations
- **Evidence:**
  - `.rdd-instance/requirements.md`:
    - `- [FR-026] All RDD framework operations shall be implemented in Python.`
    - `- [FR-045] The framework shall depend only on Python-based installation, omitting shell-based or PowerShell-based installers.`
  - `.rdd-instance/specifications/front-end.md`:
    - `Legacy Implementation: Bash and PowerShell scripts (archived)`
    - Mentions locations: `src/linux/.rdd/scripts/` and `src/windows/.rdd/scripts/`
- **Why it matters:**
  - This is potentially fine (history), but it reads like current required structure, and those referenced folders are not part of the scoped structure.
  - Confuses contributors about what should exist and be maintained.
- **Recommendation:**
  - Mark legacy locations clearly as historical/out-of-scope, or remove exact path claims unless they are still shipped.
- **Risk/Tradeoffs:**
  - Low: purely documentation clarity.

### F-007

- **Severity:** **Medium**
- **Title:** `.rdd/conventions/files-and-folders.convention.md` example uses `documentation/` but framework uses `.rdd/docs/`
- **Evidence:**
  - `.rdd/conventions/files-and-folders.convention.md` example tree:
    - `│   ├── documentation/             # User guides`
  - `.rdd/manifest.json` requiredPaths:
    - `.rdd/docs/`
  - `.rdd/docs/design-notes.md`:
    - Lists `.rdd/docs/`.
- **Why it matters:**
  - This convention is meant to standardize file structure docs; having the example disagree with the canonical manifest risks propagating outdated folder names.
- **Recommendation:**
  - Update the convention example to use `docs/` consistently.
- **Risk/Tradeoffs:**
  - Low.

### F-008

- **Severity:** **Medium**
- **Title:** `questions-formatting` guidance appears duplicated across `conventions` and `templates`, risking drift
- **Evidence:**
  - `.rdd/conventions/questions-formatting.md` defines question formatting.
  - **External dependency observed (not in scope list, but present in repo):** `.rdd/templates/questions-formatting.md` appears to contain a similar guide.
- **Why it matters:**
  - Two copies of the same spec tend to diverge, causing agents to follow different formatting standards depending on which file they find.
  - In-scope execution steps explicitly specify `.rdd/conventions/questions-formatting.md` as the authoritative convention.
- **Recommendation:**
  - Keep the authoritative guidance in `.rdd/conventions/questions-formatting.md`.
  - If a template is needed, ensure it is a thin pointer (or auto-generated) and not a separate maintained copy.
- **Risk/Tradeoffs:**
  - Low to medium depending on how other tooling references the template file.

### F-009

- **Severity:** **Low**
- **Title:** `.rdd/templates/requirements.md` seed template is an empty skeleton that doesn’t match the richer structure used in `.rdd-instance/requirements.md`
- **Evidence:**
  - `.rdd/templates/requirements.md` contains only section headers.
  - `.rdd-instance/requirements.md` includes extensive sections: Product Overview, Definitions, Design principles, etc.
- **Why it matters:**
  - New installs will seed a minimal `requirements.md` that does not match the established conventions/habits in this repo instance.
- **Recommendation:**
  - Either expand the template to include the “front-matter” structure used by the instance, or update the convention to explicitly allow a minimal skeleton.
- **Risk/Tradeoffs:**
  - Low.

### F-010

- **Severity:** **Low**
- **Title:** Several specification files are empty/placeholder, making enabled specs low-value or misleading
- **Evidence:**
  - `.rdd-instance/specifications/deployment.md` only contains `## Deployment`.
  - `.rdd-instance/specifications/components.md` only contains `## Component Architecture`.
  - `.rdd-instance/specifications/infrastructure.md` exists but is empty.
  - `.rdd-instance/config.json` marks `components`, `front-end`, `infrastructure`, `security`, etc. as enabled.
- **Why it matters:**
  - Execution context gathering (`execution-step.context.md`) may waste effort “summarizing” empty specs, and enforcement expectations become unclear.
- **Recommendation:**
  - Either (a) disable empty specs by default until filled, or (b) provide minimal baseline content templates.
- **Risk/Tradeoffs:**
  - Low to medium.

### F-011

- **Severity:** **Nit**
- **Title:** Minor typos and wording issues reduce polish and may confuse agents
- **Evidence:**
  - `.rdd-instance/requirements.md`: `seves`, `primarely`, `furhter`, `e`execute command``.
  - `.rdd/prompt-snippets/execution-step.plan.md`: `aks the user`, `sequentia number`.
- **Why it matters:**
  - Typos in critical rules can cause misinterpretation; also reduces professional feel.
- **Recommendation:**
  - Fix typos in prompts/conventions and keep “must/shall” phrasing consistent.
- **Risk/Tradeoffs:**
  - Very low.

## Cross-Reference Check Summary

### Broken references

- `.rdd-instance/config.json` and `.rdd/templates/config.json` reference missing convention files:
  - `.rdd\conventions\concepts-format.md`
  - `.rdd\conventions\work-iteration-prompt-format.md`
  - `.rdd\conventions\work-iteration-registry-format.md`
- `.rdd-instance/config.json` and `.rdd/templates/config.json` refer to `work-iteration-registry.md` whereas the required/live file is `work-iteration-registry.json` per `.rdd/manifest.json`.

### Suspicious references (verify intent)

- `.rdd-instance/specifications/files-and-folders.md` claims `.rdd/about.json` exists and describes it, but `.rdd/manifest.json` does not list it as required.
- `.rdd-instance/specifications/files-and-folders.md` describes top-level `.rdd-instance/work-iteration-prompts.md` and `.rdd-instance/user-story.md` which are not part of the manifest’s requiredFiles.
- `.rdd/docs/user-guide.md` appears incomplete/truncated in the captured range.

## Redundancy & Source-of-Truth Map

### Canonical sources (implied by current framework)

- **Ownership / upgrade policy / required paths**: `.rdd/manifest.json`
- **Entry prompt for Copilot**: `.github/prompts/rdd.execute.prompt.md`
- **Work iteration registry schema**: `.rdd/conventions/work-iteration-registry.convention.md`
- **Requirements formatting**: `.rdd/conventions/requirements-format.md`
- **Question formatting**: `.rdd/conventions/questions-formatting.md`

### Conflicts / competing sources

- **Registry schema conflict**:
  - Template: `.rdd/templates/work-iteration-registry.json` (legacy)
  - Convention: `.rdd/conventions/work-iteration-registry.convention.md` (current)
  - Live seeded file: `.rdd-instance/workdir/work-iteration-registry.json` (current)

- **Prompt library location conflict**:
  - Specs/ADRs: `.rdd/prompts/`
  - Repo content: `.rdd/prompt-templates/` and `.rdd/prompt-snippets/`

- **Iteration work model conflict (legacy vs current):**
  - `.rdd-instance/specifications/files-and-folders.md` documents a `.rdd-docs`-style model (work-iteration-prompts.md checklist; workspace log.jsonl) but the manifest/workdir model is `.rdd-instance/workdir` with `work-iteration-prompt.md` and `work-iteration-registry.json`.

## Suggested Next Actions

- [ ] Fix the execute entry prompt to recognize `mode=userStory`.
- [ ] Decide and document the canonical work-iteration registry schema; update `.rdd/templates/work-iteration-registry.json` accordingly.
- [ ] Normalize `.rdd-instance/config.json` spec paths to correct filenames and POSIX separators.
- [ ] Resolve `.rdd/prompts/` vs `.rdd/prompt-templates/` naming in specs/ADRs.
- [ ] Either populate or disable empty enabled specifications (`deployment`, `components`, `infrastructure`).
