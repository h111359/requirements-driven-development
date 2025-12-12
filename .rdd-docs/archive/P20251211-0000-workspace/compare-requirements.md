## RDD Requirements Comparison Report

Source documents compared:
- `docs/ProductRequirementsSpecification.md` (Product Requirements Specification, PRS)
- `.rdd-docs/requirements.md` (Baseline RDD requirements)

Generated: 2025-12-06

### 1) Executive summary

The PRS (ProductRequirementsSpecification.md) and the baseline `.rdd-docs/requirements.md` overlap substantially on core goals: prompt persistence, traceability, automated requirements maintenance, an `execute` command, and multi-platform support. However, there are a number of important mismatches and missing items that must be addressed before the two documents can be considered aligned.

Major findings (high-level):
- Missing: explicit Web-based UI requirement (hosted locally and opened in default browser) and the requirement that prompts be authored in the Web UI and persisted as Markdown instead of ad-hoc chat prompts.
- Inconsistent: canonical prompts folder and prompt filename conventions differ between documents (`.rdd/prompts` vs `.github/prompts`, `work-iteration-prompt.md` vs `work-iteration-prompts.md`).
- Missing: an explicit, ordered `execute` command specification exists in the PRS but is not fully present as a single requirement in `requirements.md`.
- Conflicting legacy/script recommendations: PRS requires Python-first implementation and archival of legacy scripts, but `requirements.md` still defines multiple Bash/PowerShell script requirements that contradict the Python-first policy.

### 2) Methodology

I read the PRS and the baseline requirements and compared them by topic areas: high-level concepts, prompt & workspace naming/location, the `execute` command, UI requirements, installer/installation, Git/operational modes, and scripting/implementation language. For each discrepancy I either:
- proposed a new requirement (same bullet/ID style used in `requirements.md`), or
- proposed an edit to an existing requirement (showing the original requirement id and suggested change), or
- flagged a requirement as invalid/obsolete and recommended its removal or revision.

### 3) Discrepancies and missing items (detailed)

3.1 Canonical prompts location and naming
- PRS: requires `.rdd/prompts` as the folder for predefined prompt files (section 5), and uses `work-iteration-prompt.md` (singular) located under `.rdd-docs` as the single active prompt file (section 2).
- Baseline: `requirements.md` contains `TR-12` "Prompts Location: All prompt files shall be stored in .github/prompts/" and many features reference `work-iteration-prompts.md` (plural) at `.rdd-docs/work-iteration-prompts.md` (see FR-82, FR-100).
- Impact: tools and UI will disagree which folder to read/write. This affects the `execute` command, installer behavior, and prompt persistence.

Suggested resolution: Clarify and standardize prompt locations and file names (see edits below). Two viable options:
1. Adopt PRS naming (use `.rdd/prompts/` and `work-iteration-prompt.md`) and update `requirements.md` accordingly.
2. Or explicitly state both locations and purposes: `.rdd/prompts/` for framework-provided reusable prompts, and `.github/prompts/` for GitHub-specific Copilot prompt files. If both are used, the `execute` command must define precedence.

3.2 Web-based UI requirement
- PRS: requires a browser-based UI (local web server, opened automatically in default browser) supporting prompt creation/editing and all user interactions except the final execution of the `execute` command (section 4 and 7).
- Baseline: `requirements.md` contains many interactive CLI and installer GUI items (curses, Tkinter, numeric menus) but lacks an explicit requirement for a web-based UI for full prompt/workflow management.
- Impact: missing web UI requirement will result in different implementations (CLI/Tkinter vs Web) and UX fragmentation.

3.3 Execute command detailed flow
- PRS: provides a step-by-step execute command flow (read current prompt, create implementation file copying prompt text, read reqs/tech design, optionally read other repo files, generate questionnaire if needed, produce implementation plan, execute plan, update requirements/tech spec, mark prompt as completed).
- Baseline: `requirements.md` contains pieces (FR-62 implementation files, FR-118 cross-reference, state machine S01-S09 style items) but not a single, authoritative requirement listing the full ordered execute flow.
- Impact: implementers may miss important steps (e.g., copying prompt to implementation file, questionnaire generation, marking prompt completed) unless the flow is captured as a single requirement.

3.4 Scripting and legacy artifacts
- PRS: mandates Python-first implementation (core functionality in Python) and multi-platform support, and implies legacy scripts are archived.
- Baseline: contains several TR items requesting Bash and PowerShell scripts and locations (TR-24 through TR-28, TR-45/TR-46) which conflict with the Python-first mandate (FR-47, FR-69).
- Impact: conflicting guidance about primary implementation language will create maintenance burden.

3.5 Operation without Git installed
- PRS: explicitly defines three operational modes (No Git, Local Git only, Local Git + Remote GitHub) and requires storing the selected mode in configuration.
- Baseline: covers local-only mode with config (FR-71, FR-72, FR-73) but does not explicitly enumerate the three named modes as in PRS.

3.6 Prompt persistence policy (authoring location)
- PRS: requires prompts must be authored in Web UI and saved in Markdown files rather than being typed directly into Copilot chat (traceability requirement).
- Baseline: lacks a clearly stated requirement that forbids ad-hoc prompt usage in chat and mandates authoring via UI and file persistence.

### 4) Missing requirements to add (ready-to-insert entries)

Add these entries to `.rdd-docs/requirements.md` to match the PRS. Use IDs from the next available ranges (examples use suggested IDs — adjust numbering to repository conventions):

- **[GF-13] Web-based UI for prompt and workspace management**: The framework shall provide a web-based user interface hosted on a local web server and opened automatically in the user's default browser, allowing creation, editing, and management of prompts, questionnaires, implementation plans, and workspace files. The Web UI shall support all user interactions except the final execution step invoked by the `execute` command.

- **[GF-14] Prompt Authoring Persistence**: Prompts shall be authored through the Web UI and persisted as Markdown files in the repository; ad-hoc prompt text typed only into Copilot chat shall not be used as canonical prompt definitions to ensure traceability and history preservation.

- **[FR-130] Canonical prompt storage and precedence**: The framework shall define two prompt storage locations with clear purpose: `.rdd/prompts/` for framework-provided reusable prompts, and `.github/prompts/` for repository-specific Copilot prompt files. The `execute` command shall define which location has precedence when loading prompts.

- **[FR-131] Single active work-iteration prompt file**: The framework shall maintain a single active work-iteration prompt file named `work-iteration-prompt.md` located at `.rdd-docs/work-iteration-prompt.md`. At any time it shall contain exactly one active prompt definition used by the `execute` command.

- **[FR-132] Execute command ordered workflow**: The `execute` command shall implement the following ordered steps: (1) read `.rdd-docs/work-iteration-prompt.md`, (2) create an implementation file in `.rdd-docs/workspace/` containing a copy of the prompt, (3) load `.rdd-docs/requirements.md` and `tech-spec.md`, (4) optionally read repository files for context, (5) if ambiguity remains, generate a questionnaire for developer input, (6) produce a detailed implementation plan and write it to the implementation file, (7) execute the implementation plan (or run prepared scripts), (8) update requirements and technical specification files to reflect changes, and (9) mark the prompt as completed.

- **[TR-130] Prompts folder in .rdd for framework prompts**: The `.rdd/prompts/` directory shall store framework-provided reusable prompt templates; installer and build processes shall populate this directory with framework prompts during installation. Repository-specific Copilot prompts shall remain allowed in `.github/prompts/` but the framework shall prefer `.rdd/prompts/` for templates and UI-sourced prompts unless an explicit override is set in configuration.

- **[TR-131] Operational modes explicit enumeration**: The framework shall support three operation modes (configurable in `config.json`): `noGit`, `localGit`, and `remoteGit`. Behavior for each mode (what git operations are performed or skipped) shall be defined and honored by installation, sync, and wrap-up workflows.

### 5) Inconsistent requirements — suggested edits (exact changes)

Below are targeted edits to existing requirements to resolve conflicts. Where practical I propose replacement text. Please validate ID numbers and adjust only the text shown.

1) TR-12 (Prompts Location) — replace current text with:

- **[TR-12] Prompts Location**: The framework shall use two prompt locations: framework templates in `.rdd/prompts/` and repository-specific copilot prompt files in `.github/prompts/`. The `execute` command and Web UI shall clearly document precedence and allow override via configuration.

Rationale: resolves the `.rdd/prompts` vs `.github/prompts` conflict and documents precedence.

2) FR-82 / FR-100 / references to `work-iteration-prompts.md` — replace occurrences with `work-iteration-prompt.md` and ensure they reference `.rdd-docs/work-iteration-prompt.md`.

Example replacement for FR-82 and FR-100 descriptions: update file name to `work-iteration-prompt.md` and ensure wording "single active prompt" is present.

3) Remove or revise Bash/PowerShell script requirements that contradict Python-first policy. Suggested action: mark TR-24, TR-25, TR-26, TR-27 and TR-28 as deprecated and replace with Python-based tooling requirements or archival statements.

Proposed replacement (for TR-24..TR-28):

- **[TR-24] Deprecated legacy scripts**: Legacy Bash and PowerShell scripts are considered archived and any functionality required by the framework shall be implemented in Python. Where a legacy script provides a unique, non-trivial function that cannot be ported immediately, it must be documented, tested, and scheduled for porting to Python.

Rationale: this consolidates the policy and avoids contradictory requirements.

4) FR-47 (Python-Based Script Implementation) — ensure it explicitly states that Bash/PowerShell scripts are archived and not required, and that installer/build scripts are Python-based.

### 6) Requirements recommended for removal or revision (invalid/obsolete)

- **TR-24, TR-25, TR-26, TR-27, TR-28**: Recommend marking these as deprecated or removing them in favor of Python implementations or well-scoped archival requirements (see suggested replacement above). They conflict with FR-47 and FR-69 which mandate Python-only or Python-first approaches.

- **FR-05 (Workspace Initialization: A script shall initialize workspace with: work-iteration-prompts.md)**: Recommend revision to mention the canonical filename `work-iteration-prompt.md` (singular) and to reference the UI-based creation flow when applicable.

Rationale: Remove ambiguity and duplicate references to plural vs singular filenames.

### 7) Clarifications and follow-ups required (questions for authors)

1. Which prompt folder should be canonical: `.rdd/prompts/`, `.github/prompts/`, or both with defined roles? I recommend the two-location approach with explicit precedence (see `TR-130`).
2. Confirm canonical name for the single active prompt file: `work-iteration-prompt.md` (singular) or `work-iteration-prompts.md` (plural)? PRS uses singular. I recommend adopting singular to match the "exactly one prompt" statement.
3. Confirm the preferred UI strategy: web-based UI (PRS) or CLI/Tkinter/curses (requirements.md). My recommendation: make the web UI the primary user experience for prompt/workspace management while retaining CLI for automation and recovery workflows.
4. For backward compatibility, should legacy Bash and PowerShell scripts be fully removed or retained in an `archived/` area until ported to Python? I recommend archiving with a migration schedule and deprecation warnings in the installer.

### 8) Proposed next steps (practical roadmap)

1. Accept and merge the suggested new requirements (GF-13, GF-14, FR-130..FR-132, TR-130..TR-131).
2. Update the existing `TR-12`, `FR-05`, `FR-82`, `FR-100`, and any other references to the canonical prompt filename/location to the chosen canonical values.
3. Mark TR-24..TR-28 as deprecated in `requirements.md` and add TR-24 replacement wording stating the archival and migration policy.
4. Add an `Execute command` section in `requirements.md` containing the FR-132 entry so implementation and testing can be written against the single authoritative flow.
5. Implement a short PR to apply these textual changes and include a single unit/integration test that verifies the `execute` command reads `.rdd-docs/work-iteration-prompt.md` and creates an implementation file in `.rdd-docs/workspace/` (simple smoke test).

### 9) Assumptions made during comparison

- I assumed PRS author intent is authoritative for the new design direction (Web UI + Python-first) and that `requirements.md` is the living requirements document to be updated.
- I used the PRS naming as the basis for suggested canonical names (e.g., `work-iteration-prompt.md`, `.rdd/prompts/`) but left the option to adopt the two-locations approach in `TR-130` in case project maintainers want both folders.

### 10) Wrap-up

This report provides the key discrepancies, ready-to-insert requirement statements, and exact edits to resolve conflicts. If you want, I can:
- apply the textual edits to `.rdd-docs/requirements.md` (in a focused patch),
- create a short smoke test that validates the `execute` command preconditions (file presence and implementation file creation), or
- open a draft PR with the proposed changes.

End of report.
