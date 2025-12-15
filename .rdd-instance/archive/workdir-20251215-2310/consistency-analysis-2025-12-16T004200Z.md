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

### Coverage table

| Scope item | Files discovered | Notes |
|---|---:|---|
| `.rdd-instance/specifications/` | 10 | All files readable; `technical-design.json` is present but empty. |
| `.rdd/conventions/` | 5 | All files readable. |
| `.rdd/prompt-snippets/` | 7 | All files readable. |
| `.rdd/prompt-templates/` | 5 | All files readable. |
| `.rdd/templates/` | 6 | All files readable. |
| `.rdd/docs/` | 2 | `user-guide.md` appears truncated/empty beyond the title. |
| `.rdd-instance/requirements.md` | 1 | Readable. |
| `.github/prompts/rdd.execute.prompt.md` | 1 | Readable. |
| `.rdd/manifest.json` | 1 | Readable. |

### Inventory (by folder)

#### `.rdd-instance/specifications/`

- `.rdd-instance/specifications/architecture-decision-records.md`
- `.rdd-instance/specifications/components.md`
- `.rdd-instance/specifications/data.md`
- `.rdd-instance/specifications/deployment.md`
- `.rdd-instance/specifications/files-and-folders.md`
- `.rdd-instance/specifications/front-end.md`
- `.rdd-instance/specifications/infrastructure.md`
- `.rdd-instance/specifications/quality-assurance.md`
- `.rdd-instance/specifications/security.md`
- `.rdd-instance/specifications/technical-design.json` (empty file)

#### `.rdd/conventions/`

- `.rdd/conventions/design-checklist.md`
- `.rdd/conventions/questions-formatting.md`
- `.rdd/conventions/requirements-format.md`
- `.rdd/conventions/work-iteration-registry.convention.md`
- `.rdd/conventions/files-and-folders.convention.md`

#### `.rdd/prompt-snippets/`

- `.rdd/prompt-snippets/execution-step.clarity.md`
- `.rdd/prompt-snippets/execution-step.context.md`
- `.rdd/prompt-snippets/execution-step.implementation.md`
- `.rdd/prompt-snippets/execution-step.plan.md`
- `.rdd/prompt-snippets/execution-step.questionnaire.md`
- `.rdd/prompt-snippets/role.solution-architect.md`
- `.rdd/prompt-snippets/role.sotware-developer.md`

#### `.rdd/prompt-templates/`

- `.rdd/prompt-templates/check-consistency.prompt.md`
- `.rdd/prompt-templates/compare-requirements.prompt.md`
- `.rdd/prompt-templates/execute-task.prompt.md`
- `.rdd/prompt-templates/execute-work-iteration.prompt.md`
- `.rdd/prompt-templates/update-folder-structure.prompt.md`

#### `.rdd/templates/`

- `.rdd/templates/config.json`
- `.rdd/templates/requirements.md`
- `.rdd/templates/settings.json`
- `.rdd/templates/technical-design-form.json`
- `.rdd/templates/work-iteration-prompt.md`
- `.rdd/templates/work-iteration-registry.json`

#### `.rdd/docs/`

- `.rdd/docs/design-notes.md`
- `.rdd/docs/user-guide.md`

### Gaps and unreadable items

- `.rdd/docs/user-guide.md` contains only a heading and does not include the rest of the guide (may be incomplete, truncated, or placeholder). This limits consistency checking against the user documentation.
- Several paths referenced by `.rdd-instance/config.json` appear to be missing from the repository (see Findings and Cross-Reference Summary).

## Findings (Prioritized)

### F-001

- **Severity:** **Critical**
- **Title:** Manifest ownership vs upgrade policy contradict for `.rdd-instance/specifications/**`
- **Evidence:**
  - `.rdd/manifest.json`:
    - Ownership declares overwrite:
      - `"label": "instanceDocs"`, `"paths": [".rdd-instance/specifications/**"]`, `"policy": "overwriteOnUpgrade"`
    - Upgrade policy declares preserve:
      - `{ "path": ".rdd-instance/specifications/**", "action": "preserve" }`
- **Why it matters:**
  - This is a direct conflict in the framework’s “source of truth” for upgrades. Tooling or agents may overwrite instance-managed specifications unexpectedly (data loss), or preserve them when overwrite is expected (stale specs after upgrade).
- **Recommendation:**
  - Choose a single canonical rule and make both sections match.
  - Suggested smallest change:
    - If specs are instance-authored: change ownership rule `instanceDocs` policy to `preserveOnUpgrade` (or equivalent wording) to match `upgradePolicy`.
    - If specs are framework-provided and should refresh: change `upgradePolicy` rule for `.rdd-instance/specifications/**` from `preserve` to an overwrite/seed rule, and document why.
- **Risk/Tradeoffs:**
  - Preserving specs reduces upgrade consistency but avoids losing repo-specific documentation.
  - Overwriting specs improves “fresh install” parity but risks clobbering repo-specific content.

### F-002

- **Severity:** **Critical**
- **Title:** Inconsistent/missing convention paths referenced by `.rdd-instance/config.json` (execution workflows may break)
- **Evidence:**
  - `.rdd-instance/config.json` uses missing conventions:
    - `"conventions-file": ".rdd/conventions/work-iteration-prompt-format.md"`
    - `"conventions-file": ".rdd/conventions/work-iteration-registry-format.md"`
    - `"conventions-file": ".rdd/conventions/concepts-format.md"`
  - Repository conventions folder (observed):
    - `.rdd/conventions/work-iteration-registry.convention.md` exists.
    - No `work-iteration-*-format.md` files exist under `.rdd/conventions/`.
    - No `concepts-format.md` exists under `.rdd/conventions/`.
- **Why it matters:**
  - `.rdd/prompt-snippets/execution-step.context.md` explicitly says to consult `.rdd-instance/config.json` `specifications` and read their conventions to guide behavior.
  - Broken convention paths push agents into undefined formatting and can yield inconsistent artifacts or failures.
- **Recommendation:**
  - Align all convention pointers to existing files.
  - Smallest changes:
    - Replace `work-iteration-registry-format.md` references with `work-iteration-registry.convention.md`.
    - Either add missing convention files under `.rdd/conventions/` (if intended), or change config to stop referencing non-existent conventions.
    - Remove or disable `concepts` spec until `.rdd-instance/concepts.md` and its convention exist.
- **Risk/Tradeoffs:**
  - Adding new convention files changes the framework surface area; minimal but must be versioned.
  - Editing config changes behavior for existing installs.

### F-003

- **Severity:** **High**
- **Title:** `.rdd/templates/config.json` seeds different conventions than `.rdd-instance/config.json` (format vs convention drift)
- **Evidence:**
  - `.rdd/templates/config.json`:
    - `work-iteration-registry.conventions-file` is `.rdd/conventions/work-iteration-registry.convention.md`
    - `work-iteration-prompt.conventions-file` is `""`
  - `.rdd-instance/config.json`:
    - `work-iteration-registry.conventions-file` is `.rdd/conventions/work-iteration-registry-format.md` (missing)
    - `work-iteration-prompt.conventions-file` is `.rdd/conventions/work-iteration-prompt-format.md` (missing)
- **Why it matters:**
  - Seeding and the “live” instance config disagree. New installs may behave differently than existing repos, and internal docs/prompts will not reliably match.
- **Recommendation:**
  - Make `.rdd/templates/config.json` and `.rdd-instance/config.json` converge.
  - Smallest changes: pick one naming scheme and update both.
- **Risk/Tradeoffs:**
  - Any change affects an upgrade seeding/merge policy; ensure merge strategy preserves repo customization.

### F-004

- **Severity:** **High**
- **Title:** Prompt instructions mix Windows path separators with POSIX and conflict with platform consistency goals
- **Evidence:**
  - `.rdd/prompt-templates/execute-work-iteration.prompt.md`:
    - `Never change the `.rdd-instance\workdir\work-iteration-prompt.md` file!`
  - `.rdd/prompt-templates/execute-task.prompt.md`:
    - `Find ... from `.rdd-instance\workdir\work-iteration-registry.json``
  - Most other docs use POSIX-style paths like `.rdd-instance/workdir/...` and the framework lists supported platforms `["windows", "linux"]` in `.rdd/manifest.json`.
- **Why it matters:**
  - Mixed separators can confuse agents and make cross-reference validation ambiguous.
  - It also conflicts with requirements emphasizing multi-platform behavior and clarity.
- **Recommendation:**
  - Normalize to POSIX-style paths in documentation/prompts (since they are interpreted by humans/agents), while optionally noting Windows filesystem uses `\`.
  - Smallest change: replace literal strings containing `\.rdd-instance\workdir\...` with `.rdd-instance/workdir/...` in prompt templates.
- **Risk/Tradeoffs:**
  - Low risk; mostly documentation correctness.

### F-005

- **Severity:** **High**
- **Title:** Task-mode prompt (`execute-task.prompt.md`) references wrong convention filename (`work-iteration-registry-format.md`)
- **Evidence:**
  - `.rdd/prompt-templates/execute-task.prompt.md`:
    - `see `.rdd/conventions/work-iteration-registry-format.md` for details`
  - Actual file present:
    - `.rdd/conventions/work-iteration-registry.convention.md`
- **Why it matters:**
  - This is a broken cross-reference inside the core execution template.
  - Agents following it will fail to locate the referenced conventions.
- **Recommendation:**
  - Update the reference to the existing file name.
- **Risk/Tradeoffs:**
  - Low risk; fixes a broken pointer.

### F-006

- **Severity:** **High**
- **Title:** Execution snippets assume top-level `PROMPT-ID`/`PROMPT-NAME` in registry, but registry convention defines per-user-story structure
- **Evidence:**
  - `.rdd/prompt-snippets/execution-step.context.md`:
    - `[PROMPT-ID] is the value of the attribute "PROMPT-ID" in the file `.rdd-instance/workdir/work-iteration-registry.json``
  - `.rdd/prompt-templates/execute-task.prompt.md`:
    - `Find ... "PROMPT-ID" and "PROMPT-NAME" from `.rdd-instance\workdir\work-iteration-registry.json``
  - `.rdd/conventions/work-iteration-registry.convention.md` defines:
    - Top-level keys like `mode`, `active`, `userStories`, `tasks`
    - No `PROMPT-ID`/`PROMPT-NAME` keys at top level
- **Why it matters:**
  - This is a schema mismatch: the “execution engine” prompt steps depend on registry fields that the convention does not define.
  - Likely outcome: agents update wrong fields, create wrongly named artifacts (`[PROMPT-ID]-plan.md` etc.), or stop due to missing IDs.
- **Recommendation:**
  - Decide the canonical registry schema:
    - Option A (preferable): adjust snippets/templates to derive an identifier from:
      - userStory mode: `active.active-user-story-id` (e.g., `US001`) and/or `userStories[].user-story-id`
      - task mode: `active.active-task-id` or `tasks.Next-Task-For-Execution`
    - Option B: extend the registry convention to include top-level `PROMPT-ID` and keep it synchronized.
  - Smallest change is Option A: update snippets to stop requiring `PROMPT-ID` from the registry and instead define `[PROMPT-ID] := [ACTIVE-USER-STORY-ID]` in userStory mode.
- **Risk/Tradeoffs:**
  - Medium risk: affects file naming conventions and workflow history if existing iterations already used PROMPT-ID.
  - But leaving it inconsistent is higher risk.

### F-007

- **Severity:** **High**
- **Title:** Execution snippets hardcode `.rdd-instance/workdir/work-iteration-prompt.md` as `[PROMPT-TEXT]`, conflicting with user-story prompt-file model
- **Evidence:**
  - `.rdd/prompt-snippets/execution-step.context.md`:
    - `[PROMPT-TEXT] is the content of the file `.rdd-instance/workdir/work-iteration-prompt.md``
  - `.rdd/prompt-templates/execute-work-iteration.prompt.md`:
    - Defines `[PROMPT-TEXT]` as the content of `[USER-STORY].prompt-file`
    - Also states: legacy `work-iteration-prompt.md` should be ignored unless explicitly pointed to.
- **Why it matters:**
  - Snippets and template disagree on the canonical prompt location.
  - Agents following snippets may analyze/execute the legacy file even when the registry points to `user-story-US001.prompt.md`.
- **Recommendation:**
  - Update snippets to accept input prompt path as a parameter from the calling template.
  - Smallest change:
    - In each snippet, redefine `[PROMPT-TEXT]` as “the content of the prompt to execute” and specify it is passed in by the parent template.
- **Risk/Tradeoffs:**
  - Medium: requires consistent update across multiple snippet files.

### F-008

- **Severity:** **Medium**
- **Title:** `.rdd-instance/specifications/files-and-folders.md` appears stale and conflicts with current repo structure and RDD manifest
- **Evidence:**
  - `.rdd-instance/specifications/files-and-folders.md` lists many files not present in the repo structure shown and/or not represented in `.rdd/manifest.json` required paths/files, e.g.:
    - `.rdd/about.json`
    - `.rdd/scripts/rdd.py`, `.rdd/scripts/rdd_utils.py`
    - `.github/copilot-instructions.md`
    - shell install scripts in `scripts/` (`install.sh`, `install.ps1`) which conflict with requirements claiming python-only.
  - `.rdd/manifest.json` required paths list does not mention `.rdd/about.json` and required files list does not list `.rdd/scripts/rdd.py`.
- **Why it matters:**
  - The file is used by context gathering (`execution-step.context.md`) to decide which files to read and summarize.
  - Stale entries cause wasted effort and missed real files.
- **Recommendation:**
  - Refresh `files-and-folders.md` to align with actual repository structure and with the manifest’s declared requiredPaths/requiredFiles.
  - Smallest change: explicitly label the existing structure as an example and add an “Actual structure (generated)” section with current paths.
- **Risk/Tradeoffs:**
  - Low-medium: documentation change but may affect tools that parse it.

### F-009

- **Severity:** **Medium**
- **Title:** Requirements claim “python-only installer” but framework README and structure reference shell/batch installers
- **Evidence:**
  - `.rdd-instance/requirements.md`:
    - `[FR-045] The framework shall depend on Python-based installation, omitting shell-based or PowerShell-based installers.`
  - `.rdd/README.md`:
    - `For Linux - run install.sh`
    - `For Windows - run install.bat`
  - `.rdd-instance/specifications/files-and-folders.md`:
    - Lists `scripts/install.sh`, `scripts/install.ps1`, `scripts/install.bat`
- **Why it matters:**
  - Conflicting “canonical install method” confuses users and agents.
  - It impacts security posture and platform support expectations.
- **Recommendation:**
  - Decide canonical installer UX:
    - If python-only: update `.rdd/README.md` to instruct `python scripts/install.py` (or `.rdd/scripts/install.py`) and treat shell/batch as thin wrappers.
    - If wrappers allowed: update `[FR-045]` to clarify “installation logic must be implemented in Python; wrappers may exist.”
- **Risk/Tradeoffs:**
  - Medium: changes user-facing install instructions.

### F-010

- **Severity:** **Medium**
- **Title:** `.rdd/docs/user-guide.md` is incomplete, while other docs present detailed folder structure guidance
- **Evidence:**
  - `.rdd/docs/user-guide.md` head only contains:
    - `# RDD Framework User Guide` and no additional sections.
  - `.rdd/docs/design-notes.md` contains extensive folder structure details.
- **Why it matters:**
  - Users expect user-guide to be the canonical learning resource; incomplete file shifts the source-of-truth to design notes.
- **Recommendation:**
  - Either populate `user-guide.md` fully (copy or reference canonical sections) or remove it and point users to `.rdd/docs/design-notes.md`.
- **Risk/Tradeoffs:**
  - Low: docs-only.

### F-011

- **Severity:** **Low**
- **Title:** Terminology drift: “workdir” vs “workdir folder” vs “work iteration”, and inconsistent capitalization
- **Evidence:**
  - `.rdd-instance/requirements.md` uses both `workdir directory` and `workdir folder`.
  - `.rdd/conventions/work-iteration-registry.convention.md` uses “work-iteration” and “Work Iteration Registry”.
  - Spelling/capitalization issues:
    - `.rdd/prompt-snippets/role.sotware-developer.md` filename appears to have a typo (`sotware`).
- **Why it matters:**
  - Minor friction, but terminology is core to a prompt-driven workflow.
- **Recommendation:**
  - Add a short glossary section (likely in `.rdd/docs/user-guide.md` once restored) and normalize usage in prompts.
  - Fix the snippet file name typo if referenced elsewhere (verify references first).
- **Risk/Tradeoffs:**
  - Low; renaming files has higher risk if referenced.

### F-012

- **Severity:** **Low**
- **Title:** `design-checklist.md` references a non-scoped/non-existent data model path
- **Evidence:**
  - `.rdd/conventions/design-checklist.md`:
    - `Domain Model & Data Model are defined in '.rdd-instance/data-model.md'`
  - `.rdd-instance/specifications/` suggests data belongs in `.rdd-instance/specifications/data.md`.
- **Why it matters:**
  - Checklist might steer authors to create undocumented files outside the specifications folder.
- **Recommendation:**
  - Update the checklist to point to `.rdd-instance/specifications/data.md` as the canonical location.
- **Risk/Tradeoffs:**
  - Low.

## Cross-Reference Check Summary

### Broken references

- `.rdd-instance/config.json`:
  - `.rdd/conventions/work-iteration-prompt-format.md` (missing)
  - `.rdd/conventions/work-iteration-registry-format.md` (missing)
  - `.rdd/conventions/concepts-format.md` (missing)
  - `.rdd-instance/concepts.md` (missing)

- `.rdd/prompt-templates/execute-task.prompt.md`:
  - `.rdd/conventions/work-iteration-registry-format.md` (missing)

### Suspicious references (may be correct but should be verified)

- `.rdd-instance/specifications/files-and-folders.md` references many files that appear to describe a different/older structure (e.g. `.rdd/scripts/rdd.py`, `.rdd/about.json`). This looks like a legacy template rather than hydrated instance docs.

## Redundancy & Source-of-Truth Map

### Key concepts and where they are defined

- **Upgrade/ownership rules**
  - Canonical: `.rdd/manifest.json` (`ownership`, `upgradePolicy`, `workdirModel`)
  - Conflict: ownership vs upgradePolicy for `.rdd-instance/specifications/**`

- **Folder structure description**
  - Conventions (formatting): `.rdd/conventions/files-and-folders.convention.md`
  - “Documentation”: `.rdd/docs/design-notes.md` (contains the structure)
  - Instance spec: `.rdd-instance/specifications/files-and-folders.md` (currently stale)

- **Work iteration registry schema**
  - Conventions: `.rdd/conventions/work-iteration-registry.convention.md`
  - Execution behavior entrypoint: `.github/prompts/rdd.execute.prompt.md` + `.rdd/prompt-templates/*`
  - Conflict: snippets/templates expect `PROMPT-ID`/`PROMPT-NAME`, but convention doesn’t define them

- **Requirements formatting**
  - Conventions: `.rdd/conventions/requirements-format.md`
  - Instance: `.rdd-instance/requirements.md`

### Conflicts between sources

- `.rdd/manifest.json`: `ownership` vs `upgradePolicy` for `.rdd-instance/specifications/**`.
- Execution workflow schema: `execute-work-iteration.prompt.md` + registry convention vs snippet expectations.
- Installation method: `.rdd-instance/requirements.md` python-only vs `.rdd/README.md` shell/bat instructions.

## Suggested Next Actions

- [ ] Resolve manifest conflict: decide preserve vs overwrite for `.rdd-instance/specifications/**` and make `ownership` and `upgradePolicy` consistent.
- [ ] Fix broken convention pointers in `.rdd-instance/config.json` and `.rdd/prompt-templates/execute-task.prompt.md`.
- [ ] Align execution snippets with the registry convention (remove `PROMPT-ID` dependency or add it to the registry schema).
- [ ] Normalize path separators (prefer `/`) across prompts.
- [ ] Refresh `.rdd-instance/specifications/files-and-folders.md` to match actual structure and the manifest.
- [ ] Restore or remove `.rdd/docs/user-guide.md` so there’s a clear documentation entry point.
