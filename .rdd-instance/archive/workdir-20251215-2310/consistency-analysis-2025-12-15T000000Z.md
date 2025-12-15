# Consistency Analysis (RDD)

## Timestamp

2025-12-15T000000Z

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
| `.rdd/docs/` | 2 | Read first ~260 lines of `user-guide.md`; read `design-notes.md` (file is short) |
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
- **Evidence:**
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
    - Allowed `mode` values:
      ```markdown
      - Allowed values:
        - `userStory`, `task`
      ```
    - Requires `userStories`, `active`, and `tasks` objects.
  - `.github/prompts/rdd.execute.prompt.md`:
    ```markdown
    - If the "mode" is "prompt", follow the instructions in `.rdd/prompt-templates/execute-work-iteration.prompt.md`.
    - Else If the "mode" is "task", follow the instructions in `.rdd/prompt-templates/execute-task.prompt.md`.
    ```
  - `.rdd/prompt-templates/execute-work-iteration.prompt.md`:
    ```markdown
    - If [WI-MODE] is `userStory`, the prompt to execute is [PROMPT-TEXT] from `[USER-STORY].prompt-file`.
    ```
- **Why it matters:**
  - This is the core control plane for execution. A Copilot agent (or any tooling) following the prompt can end up reading/writing the wrong registry fields, skipping stages, or halting due to “unrecognized mode”.
  - It’s also a strong source-of-truth conflict: template seed provides one schema while the convention defines another.
- **Recommendation:**
  - Choose one canonical registry schema and align all references:
    - Option A (recommended): adopt `.rdd/conventions/work-iteration-registry-convention.md` as canonical.
      - Update `.rdd/templates/work-iteration-registry.json` to match that schema.
      - Update `.github/prompts/rdd.execute.prompt.md` to reference `mode=userStory` rather than `prompt`.
      - Update any docs/specs that still mention `mode=prompt`.
    - Option B: keep legacy `mode=prompt` schema and downgrade the convention + execute-work-iteration prompt accordingly (riskier, loses userStories/tasks separation).
- **Risk/Tradeoffs:**
  - Aligning to the new schema may require migration logic in scripts and user data migration for existing installations.

### F-002

- **Severity:** **Critical**
- **Title:** "workdir" vs "workdir" drift (folder name, file paths) causes broken references and unsafe instructions
- **Evidence:**
  - `.rdd/manifest.json` defines workdir root:
    ```json
    "workdirRoot": ".rdd-instance/workdir"
    ```
  - `.rdd/docs/design-notes.md` contains:
    ```markdown
    ├── workdir/                 # Current iteration work files
    ```
    and also references `.rdd-instance/workdir/` in multiple spots.
  - `.rdd/prompt-templates/execute-work-iteration.prompt.md`:
    ```markdown
    - Never change the `.rdd-instance\workdir\work-iteration-prompt.md` file!
    ```
  - `.rdd/prompt-snippets/execution-step.context.md`:
    ```markdown
    - [PROMPT-TEXT] is the content of the file `.rdd-instance/workdir/work-iteration-prompt.md`
    ```
  - `.rdd/templates/config.json` uses `.rdd-instance\\workdir\\...`:
    ```json
    "path": ".rdd-instance\\workdir\\work-iteration-prompt.md"
    ```
- **Why it matters:**
  - Agents and scripts may read/write inside a non-existent directory (`.rdd-instance/workdir`) even though the manifest’s workdir model is `workdir`.
  - Safety rules like “Never change X” become ineffective when “X” is the wrong path.
- **Recommendation:**
  - Pick one canonical folder name (strongly suggested: `workdir` because it is baked into the manifest, ownership rules, requiredPaths, and requiredFiles).
  - Update:
    - `.rdd/docs/design-notes.md` and any other doc that describes `workdir/` to `workdir/`.
    - `.rdd/templates/config.json` to use POSIX paths and `workdir`.
    - `.rdd/prompt-templates/execute-work-iteration.prompt.md` to consistently refer to `.rdd-instance/workdir/...`.
- **Risk/Tradeoffs:**
  - Some older installations might still use `workdir/`; consider documenting a migration step or supporting both temporarily.

### F-003

- **Severity:** **High**
- **Title:** Several prompt templates are placeholders or reference non-existent files (broken workflow chain)
- **Evidence:**
  - `.rdd/prompt-templates/execution-plan.prompt.md`:
    ```markdown
    [To be implemented in future release]
    ```
  - `.rdd/prompt-templates/questionnaire-generation.prompt.md`:
    ```markdown
    [To be implemented in future release]
    ```
    and references:
    ```markdown
    Follow guidelines from `.rdd/templates/questions-formatting.md`
    ```
    However, `.rdd/templates/questions-formatting.md` does **not** exist; the actual file is `.rdd/conventions/questions-formatting.md`.
  - `.rdd/prompt-templates/folder-structure-sync.prompt.md` is also marked placeholder.
- **Why it matters:**
  - If these templates are surfaced in the UI/library (as implied by several requirements), they can cause user confusion and agent failures.
  - The broken cross-reference (`.rdd/templates/questions-formatting.md`) is a concrete correctness bug.
- **Recommendation:**
  - Either:
    - Implement minimal viable versions of these prompt templates, or
    - Clearly mark them as “not for use” and ensure they aren’t presented as executable options.
  - Fix the cross-reference in `questionnaire-generation.prompt.md` from `.rdd/templates/questions-formatting.md` to `.rdd/conventions/questions-formatting.md`.
- **Risk/Tradeoffs:**
  - Implementing these prompts might imply broader changes in scripts/UI; smallest change is to correct references and labeling first.

### F-004

- **Severity:** **High**
- **Title:** `.rdd/templates/config.json` appears to encode legacy/mismatched conventions and Windows-only path separators
- **Evidence:**
  - `.rdd/templates/config.json` uses backslashes and older schema keys:
    ```json
    "work-iteration-prompt": {
      "path": ".rdd-instance\\workdir\\work-iteration-prompt.md",
      "conventions-file": ".rdd\\conventions\\work-iteration-prompt-format.md"
    }
    ```
  - Missing referenced convention files:
    - `.rdd/conventions/work-iteration-prompt-format.md` not found (not in scoped conventions list).
    - `.rdd/conventions/work-iteration-registry-format.md` not found; actual file is `.rdd/conventions/work-iteration-registry-convention.md`.
  - `.rdd/prompt-snippets/execution-step.context.md` also uses backslashes:
    ```markdown
    The `specifications` object in `.rdd-instance\config.json` ...
    ```
- **Why it matters:**
  - This template is used for seeding `.rdd-instance/config.json` (per manifest). If it contains invalid references, the runtime workflow can’t reliably discover which specs to load.
  - Mixed path separators create cross-platform ambiguity and complicate parsing.
- **Recommendation:**
  - Normalize template paths to POSIX-style (`/`) or explicitly define a path-joining rule.
  - Bring config schema in line with manifest + conventions:
    - Use `workdir` instead of `workdir`.
    - Reference actual convention file names.
- **Risk/Tradeoffs:**
  - Changing config schema requires migration support in installer/tooling; but leaving it broken guarantees failures.

### F-005

- **Severity:** **High**
- **Title:** Safety/ownership constraints are inconsistent and could mislead an agent into editing the wrong files
- **Evidence:**
  - `.rdd/manifest.json` ownership:
    ```json
    { "paths": [".rdd/**"], "policy": "overwriteOnUpgrade" }
    ```
    and `.rdd-instance/**` are preserve.
  - `.rdd/prompt-snippets/execution-step.plan.md` instructs planned updates to `.rdd-instance/requirements.md` (fine) but also says “it will be done in the execution step” (meaning an agent will edit it).
  - `.rdd/prompt-templates/execute-work-iteration.prompt.md` includes:
    ```markdown
    - Never change the `.rdd-instance\workdir\work-iteration-prompt.md` file!
    ```
    which is likely the *active prompt* file in some legacy layouts, but manifest says active prompt is `.rdd-instance/workdir/work-iteration-prompt.md`.
- **Why it matters:**
  - The framework tries to strictly separate framework-managed vs instance-managed state. If safety rules point to the wrong file/path, an agent may modify the wrong artifact (or fail to protect the right one).
- **Recommendation:**
  - Align “never edit”/“must edit” rules with the **manifest** as canonical:
    - Explicitly state which files in `workdir` are writable outputs.
    - Explicitly protect only the current “active prompt” file (correct path).
- **Risk/Tradeoffs:**
  - Tightening these rules might break older flows, but reduces accidental corruption.

### F-006

- **Severity:** **Medium**
- **Title:** Docs and specs mention non-existent artifacts (e.g., `.rdd/about.json`, `.rdd/prompts/`) within this repo state
- **Evidence:**
  - `.rdd-instance/specifications/deployment.md`:
    ```markdown
    Extracts version from `.rdd/about.json` as single source of truth
    ```
    but `.rdd/about.json` was not found in the repository snapshot.
  - `.rdd-instance/specifications/front-end.md`:
    ```markdown
    - Lists all `.md` files in `.rdd/prompts/`
    ```
    but the framework structure in `.rdd` (as listed) contains `prompt-templates/` and `prompt-snippets/`, not `.rdd/prompts/`.
  - `.rdd-instance/specifications/files-and-folders.md` claims `.rdd/templates/questions-formatting.md`, etc. (its own listed structure doesn’t match actual `.rdd/templates/`).
- **Why it matters:**
  - These specs are supposed to guide implementation; stale paths will waste time and cause incorrect automation.
- **Recommendation:**
  - Decide which is canonical: manifest + actual tree, then update specifications to match.
  - If `.rdd/about.json` is intended, ensure it is created/seeded and listed in manifest requiredFiles.
- **Risk/Tradeoffs:**
  - Could be a partial checkout; if the file exists outside scope in other branches/releases, treat as version drift and document it.

### F-007

- **Severity:** **Medium**
- **Title:** User guide conflicts with requirements and manifest regarding installer approach and platform support
- **Evidence:**
  - `.rdd/docs/user-guide.md` says:
    ```markdown
    The RDD framework installation process is straightforward and consistent across Windows, Linux, and macOS platforms.
    ```
    whereas `.rdd/manifest.json` lists:
    ```json
    "supportedPlatforms": ["windows", "linux"]
    ```
  - `.rdd/docs/user-guide.md` instructs:
    ```bash
    chmod +x install.sh
    ./install.sh
    ```
    but `.rdd-instance/requirements.md` includes:
    ```markdown
    - [FR-045] The framework shall depend only on Python-based installation, omitting shell-based or PowerShell-based installers.
    ```
- **Why it matters:**
  - The guide directs users to a shell installer that the requirements say should not exist/be required.
  - Platform statement drift can mislead users and test expectations.
- **Recommendation:**
  - Make a single canonical installation story:
    - If the Python installer is canonical, user guide should recommend `python install.py` first and treat `install.sh`/`install.bat` as optional conveniences.
    - Align supportedPlatforms list (either add `macos` to manifest or remove it from guide).
- **Risk/Tradeoffs:**
  - Adjusting manifest may affect validation tooling; adjust docs is lower risk.

### F-008

- **Severity:** **Medium**
- **Title:** Requirements-format convention differs from actual requirements practices in `.rdd-instance/requirements.md`
- **Evidence:**
  - `.rdd/conventions/requirements-format.md` specifies sequential IDs like `001, 002, 003`.
  - `.rdd-instance/requirements.md` uses:
    ```markdown
    - [FR-002] [DELETED]
    - [FR-002a] ...
    - [FR-069a] ...
    - [TR-005a] ...
    ```
- **Why it matters:**
  - Suffixes (`002a`) may be valid for “don’t renumber” policies, but the convention doesn’t define them, so automated tooling or prompting rules may conflict.
- **Recommendation:**
  - Extend the convention to explicitly allow suffix IDs (e.g., `FR-002a`, `FR-002b`) as a compatibility mechanism.
  - Or define an official “reserved/obsoleted” mechanism beyond `[DELETED]`.
- **Risk/Tradeoffs:**
  - Loosening ID rules can complicate sorting; but it reflects reality and prevents fights between agent instructions and the existing file.

### F-009

- **Severity:** **Low**
- **Title:** Typos and wording drift reduce clarity in prompts and requirements
- **Evidence:**
  - `.rdd/prompt-snippets/execution-step.context.md`:
    ```markdown
    - Readn the files descriptions ...
    - Write the summary in consise and clear style without ommition of information
    ```
  - `.rdd/prompt-templates/execute-task.prompt.md` has multiple typos and legacy references (e.g., `before eachq step`).
  - `.rdd-instance/requirements.md` includes:
    ```markdown
    The the product is a system that seves...
    ... exexuted ... understant ... primarely ... vanila ...
    ```
- **Why it matters:**
  - Typos in operational prompts can lead to misinterpretation or reduced trust. They also signal stale/duplicated content.
- **Recommendation:**
  - Quick pass to correct typos in prompt snippets and high-visibility docs; keep changes minimal.
- **Risk/Tradeoffs:**
  - Low; mostly editorial.

## Cross-Reference Check Summary

### Broken references (confirmed missing)

- `.rdd/prompt-templates/questionnaire-generation.prompt.md` → references `.rdd/templates/questions-formatting.md` (missing). Canonical appears to be `.rdd/conventions/questions-formatting.md`.
- `.rdd/templates/config.json` → references `.rdd/conventions/work-iteration-prompt-format.md` (missing).
- `.rdd/templates/config.json` → references `.rdd/conventions/work-iteration-registry-format.md` (missing); canonical appears to be `.rdd/conventions/work-iteration-registry-convention.md`.
- `.rdd-instance/specifications/deployment.md` and `.rdd-instance/specifications/components.md` reference `.rdd/about.json` (missing in this repo state).

### Suspicious references (may be correct in another version, but inconsistent here)

- `.rdd-instance/specifications/front-end.md` references `.rdd/prompts/` as prompt library root (repo uses `.rdd/prompt-templates/` + `.rdd/prompt-snippets/`).
- `.rdd/docs/user-guide.md` states macOS support while manifest lists only windows/linux.
- Widespread use of `.rdd-instance/workdir/` vs `.rdd-instance/workdir/`.

## Redundancy & Source-of-Truth Map

### Canonical sources (as currently implied)

- **Ownership & upgrade policy:** `.rdd/manifest.json`
- **Workdir model:** `.rdd/manifest.json` (workdirModel) and `.rdd/conventions/work-iteration-registry-convention.md`
- **Execution entrypoint:** `.github/prompts/rdd.execute.prompt.md`
- **Execution workflow:** `.rdd/prompt-templates/execute-work-iteration.prompt.md` + `.rdd/prompt-snippets/execution-step.*.md`
- **Requirements format:** `.rdd/conventions/requirements-format.md`
- **Question formatting:** `.rdd/conventions/questions-formatting.md`

### Competing / conflicting sources

- **workdir folder naming & layout**:
  - `.rdd/manifest.json` → `workdir`
  - `.rdd/docs/design-notes.md` + `.rdd/templates/config.json` + `execute-task.prompt.md` legacy text → `workdir`
- **Registry schema**:
  - `.rdd/templates/work-iteration-registry.json` legacy single-prompt schema (`mode: prompt`)
  - `.rdd/conventions/work-iteration-registry-convention.md` multi-user-story schema (`mode: userStory|task`)
  - `.github/prompts/rdd.execute.prompt.md` expects `mode: prompt|task`
- **Prompt library root**:
  - Specs mention `.rdd/prompts/`
  - Repo appears to use `.rdd/prompt-templates/` as library

## Suggested Next Actions

- [ ] Decide and document the canonical work-iteration registry schema (legacy vs userStory/task). Then update template + entry prompt + docs to match.
- [ ] Decide and document the canonical workdir folder name (`workdir` vs `workdir`). Update templates and safety rules accordingly.
- [ ] Fix confirmed broken references (questions-formatting path; missing convention filenames; `.rdd/about.json` story).
- [ ] Add a migration note (or code migration) for older installations that use legacy paths/schema.
- [ ] Editorial pass for typos in high-traffic prompts/snippets.
