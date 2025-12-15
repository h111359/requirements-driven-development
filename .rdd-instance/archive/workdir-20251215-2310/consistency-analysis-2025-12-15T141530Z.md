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
| `.rdd-instance/specifications/` | 10 | `technical-design.json`, `data.md`, `infrastructure.md` are present but empty |
| `.rdd/conventions/` | 5 | Read all |
| `.rdd/prompt-snippets/` | 7 | Read all |
| `.rdd/prompt-templates/` | 9 | Read all |
| `.rdd/templates/` | 6 | Read all |
| `.rdd/docs/` | 2 | Read first ~260 lines of `user-guide.md`; read `design-notes.md` |
| `.rdd-instance/requirements.md` | 1 | Read first ~260 lines (file continues beyond) |
| `.github/prompts/rdd.execute.prompt.md` | 1 | Read all |
| `.rdd/manifest.json` | 1 | Read all |

### Gaps / unreadable items

None were unreadable. The following are **present but empty**, which reduces the ability to validate alignment:
- `.rdd-instance/specifications/technical-design.json`
- `.rdd-instance/specifications/data.md`
- `.rdd-instance/specifications/infrastructure.md`

## Findings (Prioritized)

### F-001

- **Severity:** **Critical**
- **Title:** Work-iteration registry and execution mode are inconsistent across sources ("prompt" vs "userStory"; registry schema mismatch)
- **Evidence**
  - `.rdd/templates/work-iteration-registry.json`:
    ```json
    {
        "PROMPT-ID": "",
        "PROMPT-NAME": "",
        "mode": "prompt",
        "context": { "state": "not-started", "file": "" },
        "clarity": { "state": "not-started", "file": "" },
        "plan": { "state": "not-started", "file": "" },
        "implementation": { "state": "not-started", "approved": false, "file": "" }
    }
    ```
  - `.rdd/conventions/work-iteration-registry-convention.md`:
    ```markdown
    - Allowed values:
      - `userStory`, `task`
    ```
    (also requires `userStories`, `active`, and `tasks` objects)
  - `.github/prompts/rdd.execute.prompt.md`:
    ```markdown
    - If the "mode" is "prompt", follow the instructions in `.rdd/prompt-templates/execute-work-iteration.prompt.md`.
    - Else If the "mode" is "task", follow the instructions in `.rdd/prompt-templates/execute-task.prompt.md`.
    ```
  - `.rdd/prompt-templates/execute-work-iteration.prompt.md`:
    ```markdown
    - If [WI-MODE] is `userStory`, the prompt to execute is [PROMPT-TEXT] from `[USER-STORY].prompt-file`.
    ```
- **Why it matters**
  - This is the core control plane for execution. A Copilot agent (or any tooling) following the prompt can end up reading/writing the wrong registry fields, skipping stages, or halting due to “unrecognized mode”.
  - It’s a source-of-truth conflict: template seed provides one schema while the convention defines another.
- **Recommendation**
  - **Apply Option A (selected):** adopt `.rdd/conventions/work-iteration-registry-convention.md` as the canonical schema.
  - Concrete edits to apply (do not apply in this report):
    - Update `.rdd/templates/work-iteration-registry.json` to match the convention schema (top-level keys: `mode` in `{userStory, task}`, plus `active`, `userStories[]`, `tasks`).
    - Update `.github/prompts/rdd.execute.prompt.md` decision logic to use `mode=userStory` (not `prompt`).
      - I.e., dispatch to `.rdd/prompt-templates/execute-work-iteration.prompt.md` when `mode == "userStory"`.
    - Update any docs/specs that still mention `mode=prompt` to the new vocabulary (`userStory`/`task`).
  - Deprecation note (recommended): explicitly mark the legacy `mode=prompt` schema as deprecated (in docs) and provide a short migration note for existing registries.
- **Risk/Tradeoffs**
  - Aligning to the new schema requires migration logic in scripts and user data migration for existing installations.

### F-002

- **Severity:** **Critical**
- **Title:** "workspace" vs "workdir" drift (folder name, file paths) causes broken references and weak safety rules
- **Evidence**
  - `.rdd/manifest.json` defines workspace root:
    ```json
    "workspaceRoot": ".rdd-instance/workdir"
    ```
  - `.rdd/docs/design-notes.md` contains:
    ```markdown
    ├── workspace/                 # Current iteration work files
    ```
  - `.rdd/prompt-templates/execute-work-iteration.prompt.md`:
    ```markdown
    - Never change the `.rdd-instance\workspace\work-iteration-prompt.md` file!
    ```
  - `.rdd/prompt-snippets/execution-step.context.md`:
    ```markdown
    - [PROMPT-TEXT] is the content of the file `.rdd-instance/workdir/work-iteration-prompt.md`
    ```
  - `.rdd/templates/config.json` uses `.rdd-instance\\workspace\\...`:
    ```json
    "path": ".rdd-instance\\workspace\\work-iteration-prompt.md"
    ```
- **Why it matters**
  - Agents and scripts may read/write inside a non-existent directory (`.rdd-instance/workspace`) even though the manifest’s workspace model is `workdir`.
  - Safety rules like “Never change X” become ineffective when “X” is the wrong path.
- **Recommendation**
  - Pick one canonical folder name (strongly suggested: `workdir` because it’s baked into `manifest.json` requiredPaths/requiredFiles + workspaceModel).
  - Update:
    - `.rdd/docs/design-notes.md` and any other docs that describe `workspace/` to `workdir/`.
    - `.rdd/templates/config.json` to use POSIX paths and `workdir`.
    - `.rdd/prompt-templates/execute-work-iteration.prompt.md` to consistently refer to `.rdd-instance/workdir/...`.
- **Risk/Tradeoffs**
  - Some older installations might still use `workspace/`. Consider documenting a migration step or supporting both temporarily.

### F-003

- **Severity:** **High**
- **Title:** Several prompt templates are placeholders or reference non-existent files (workflow chain cannot execute as written)
- **Evidence**
  - `.rdd/prompt-templates/execution-plan.prompt.md`:
    ```markdown
    [To be implemented in future release]
    ```
  - `.rdd/prompt-templates/questionnaire-generation.prompt.md`:
    ```markdown
    Follow guidelines from `.rdd/templates/questions-formatting.md`
    ```
    but `.rdd/templates/questions-formatting.md` does **not** exist; the actual file is `.rdd/conventions/questions-formatting.md`.
  - `.rdd/prompt-templates/folder-structure-sync.prompt.md` is also a placeholder.
- **Why it matters**
  - If these templates are surfaced in a UI/library (as implied in requirements/specs), they can cause user confusion and agent failures.
- **Recommendation**
  - Either implement a minimal viable version of each placeholder template, or clearly label them “not for execution” and keep them out of pick-lists.
  - Fix the broken cross-reference in `questionnaire-generation.prompt.md` to point to `.rdd/conventions/questions-formatting.md`.
- **Risk/Tradeoffs**
  - Implementing these prompts may imply broader changes in scripts/UI; smallest change is to correct references and labeling first.

### F-004

- **Severity:** **High**
- **Title:** `.rdd/templates/config.json` encodes legacy schema + Windows path separators + missing convention file names
- **Evidence**
  - `.rdd/templates/config.json`:
    ```json
    "specifications": {
      "work-iteration-prompt": {
        "path": ".rdd-instance\\workspace\\work-iteration-prompt.md",
        "conventions-file": ".rdd\\conventions\\work-iteration-prompt-format.md"
      },
      "work-iteration-registry": {
        "path": ".rdd-instance\\workspace\\work-iteration-registry.md",
        "conventions-file": ".rdd\\conventions\\work-iteration-registry-format.md"
      }
    }
    ```
  - Missing in the current repo state:
    - `.rdd/conventions/work-iteration-prompt-format.md` (not found)
    - `.rdd/conventions/work-iteration-registry-format.md` (not found)
  - The actual convention file appears to be `.rdd/conventions/work-iteration-registry-convention.md`.
- **Why it matters**
  - The manifest uses this template for seeding `.rdd-instance/config.json`. If it contains invalid references, the workflow can’t reliably discover which specs to load.
  - Mixed separators (`\` vs `/`) create cross-platform ambiguity.
- **Recommendation**
  - Normalize template paths to POSIX-style (`/`) or explicitly document a path-joining rule.
  - Bring config schema in line with the manifest + conventions:
    - `workdir` not `workspace`
    - reference real convention filenames
- **Risk/Tradeoffs**
  - Changing config schema requires migration support in installer/tooling; but leaving it broken guarantees failures.

### F-005

- **Severity:** **High**
- **Title:** Agent safety/ownership constraints are inconsistent and could result in editing the wrong file
- **Evidence**
  - `.rdd/manifest.json` ownership:
    ```json
    { "paths": [".rdd/**"], "policy": "overwriteOnUpgrade" }
    ...
    { "paths": [".rdd-instance/requirements.md", ".rdd-instance/specifications/**"], "policy": "preserveOnUpgrade" }
    ```
  - `.rdd/prompt-templates/execute-work-iteration.prompt.md`:
    ```markdown
    - Never change the `.rdd-instance\workspace\work-iteration-prompt.md` file!
    ```
    but manifest expects `.rdd-instance/workdir/work-iteration-prompt.md`.
- **Why it matters**
  - The framework aims for strict separation of framework-managed vs instance-managed artifacts. If safety rules point to the wrong file/path, an agent may modify the wrong artifact (or fail to protect the right one).
- **Recommendation**
  - Align “must not edit” rules with `manifest.json` as canonical.
  - Explicitly enumerate which `workdir` artifacts are outputs vs inputs.
- **Risk/Tradeoffs**
  - Tightening rules might break legacy flows but reduces accidental corruption.

### F-006

- **Severity:** **Medium**
- **Title:** Specs reference artifacts not present in this repo snapshot (`.rdd/about.json`, `.rdd/prompts/`)
- **Evidence**
  - `.rdd-instance/specifications/deployment.md`:
    ```markdown
    Extracts version from `.rdd/about.json` as single source of truth
    ```
    but `.rdd/about.json` was not found in this workspace.
  - `.rdd-instance/specifications/front-end.md`:
    ```markdown
    - Lists all `.md` files in `.rdd/prompts/`
    ```
    but current `.rdd/` tree contains `prompt-templates/` and `prompt-snippets/`, not `.rdd/prompts/`.
- **Why it matters**
  - These specs guide implementation; stale paths cause incorrect automation and wasted effort.
- **Recommendation**
  - Decide canonical location(s) (manifest + actual tree), then update specifications.
  - If `.rdd/about.json` is intended, add it as a requiredFile in manifest OR update docs/specs to the actual version file.
- **Risk/Tradeoffs**
  - Could reflect a version mismatch between docs/specs and the codebase; handle as “version drift” and standardize.

### F-007

- **Severity:** **Medium**
- **Title:** User guide conflicts with requirements and manifest on platforms and the installer story
- **Evidence**
  - `.rdd/docs/user-guide.md`:
    ```markdown
    ... consistent across Windows, Linux, and macOS platforms.
    ```
    but `.rdd/manifest.json`:
    ```json
    "supportedPlatforms": ["windows", "linux"]
    ```
  - `.rdd/docs/user-guide.md` instructs running `install.sh`, while `.rdd-instance/requirements.md` includes:
    ```markdown
    - [FR-045] ... omitting shell-based or PowerShell-based installers.
    ```
- **Why it matters**
  - Users will follow the guide; mismatched statements undermine trust and may violate stated requirements.
- **Recommendation**
  - Make a single canonical installation approach:
    - Recommend `python install.py` first.
    - Treat `install.sh`/`install.bat` as optional wrappers (or remove them if truly disallowed).
  - Align platform statements (either add `macos` to manifest or remove it from the guide).
- **Risk/Tradeoffs**
  - Updating docs is low risk. Updating manifest impacts validation tooling.

### F-008

- **Severity:** **Medium**
- **Title:** Requirements ID convention doesn’t define suffix IDs but requirements file uses them
- **Evidence**
  - `.rdd/conventions/requirements-format.md`:
    ```markdown
    - **ID**: Sequential number (001, 002, 003, etc.)
    ```
  - `.rdd-instance/requirements.md`:
    ```markdown
    - [FR-002a] ...
    - [FR-069a] ...
    - [TR-005a] ...
    ```
- **Why it matters**
  - Agent instructions and tools may reject or “correct” valid-but-undocumented IDs, causing unnecessary churn.
- **Recommendation**
  - Extend the convention to explicitly allow suffix IDs (e.g., `FR-002a`, `FR-002b`) as a compatibility mechanism.
- **Risk/Tradeoffs**
  - Slightly more complex sorting/validation logic.

### F-009

- **Severity:** **Low**
- **Title:** Typos and wording drift reduce clarity in prompts and requirements
- **Evidence**
  - `.rdd/prompt-snippets/execution-step.context.md`:
    ```markdown
    - Readn the files descriptions ...
    - Write the summary in consise ... without ommition ...
    ```
  - `.rdd/prompt-templates/execute-task.prompt.md`:
    ```markdown
    before eachq step
    ```
  - `.rdd-instance/requirements.md`:
    ```markdown
    The the product is a system that seves...
    ... exexuted ... understant ... vanila ...
    ```
- **Why it matters**
  - Typos in operational prompts can lead to misinterpretation and decrease trust.
- **Recommendation**
  - Quick editorial pass on high-traffic prompts/snippets.
- **Risk/Tradeoffs**
  - Low; editorial only.

## Cross-Reference Check Summary

### Broken references (confirmed missing)

- `.rdd/prompt-templates/questionnaire-generation.prompt.md` → `.rdd/templates/questions-formatting.md` (missing; likely `.rdd/conventions/questions-formatting.md`).
- `.rdd/templates/config.json` → `.rdd/conventions/work-iteration-prompt-format.md` (missing).
- `.rdd/templates/config.json` → `.rdd/conventions/work-iteration-registry-format.md` (missing; likely `.rdd/conventions/work-iteration-registry-convention.md`).
- `.rdd-instance/specifications/deployment.md` / `.rdd-instance/specifications/components.md` → `.rdd/about.json` (missing in this repo state).

### Suspicious references (verify)

- Specs reference `.rdd/prompts/` as a prompt library root; repo appears to use `.rdd/prompt-templates/`.
- Widespread use of `.rdd-instance/workspace/` vs `.rdd-instance/workdir/`.
- User guide says macOS supported but manifest lists only windows/linux.

## Redundancy & Source-of-Truth Map

### Canonical sources (as implied by current repo)

- **Ownership & upgrade policy:** `.rdd/manifest.json`
- **Workspace model (workdir):** `.rdd/manifest.json` (`workspaceModel`, `requiredPaths`, `requiredFiles`)
- **Execution entrypoint:** `.github/prompts/rdd.execute.prompt.md`
- **Execution workflow:** `.rdd/prompt-templates/execute-work-iteration.prompt.md` + `.rdd/prompt-snippets/execution-step.*.md`
- **Requirements format:** `.rdd/conventions/requirements-format.md`
- **Question formatting:** `.rdd/conventions/questions-formatting.md`

### Conflicts between sources

- **Workspace folder name**:
  - Manifest: `workdir`
  - Design notes + templates: `workspace`
- **Registry schema**:
  - Template seed: legacy single-prompt schema (`mode: prompt`) — **to be updated** to userStory/task schema (Option A)
  - Convention: userStory/task schema — **canonical (Option A)**
  - Execute entry prompt: prompt/task schema — **to be updated** to userStory/task schema (Option A)
- **Prompt library path**:
  - Specs: `.rdd/prompts/`
  - Repo content: `.rdd/prompt-templates/` and `.rdd/prompt-snippets/`

## Suggested Next Actions

- [ ] Apply Option A for F-001: make `.rdd/conventions/work-iteration-registry-convention.md` canonical and migrate the template + execute entry prompt to match.
- [ ] Decide canonical workspace folder name (`workdir` seems canonical per manifest) and update docs/templates/prompts accordingly.
- [ ] Fix confirmed broken references (question formatting path, missing convention file names, `.rdd/about.json` story).
- [ ] Add migration notes (or code migration) for older installs using legacy schema/paths.
- [ ] Editorial clean-up: fix typos in prompt snippets and high-visibility docs.
