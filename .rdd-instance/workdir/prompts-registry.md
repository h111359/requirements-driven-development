%%PROMPT P-001 "Initial version of the technical design"
[[[ROLE_SOLUTION_ARCHITECT]]]

Implement the **Technical Design** page end-to-end, including a **new schema format**, **automatic migration**, and **Python-only write operations**.

# Context and constraints

- Legacy content exists in `.rdd-instance/workdir/P-001_Initial version of the technical design/TechnicalDesignSchema.json` (currently not implemented). Use it as the authoritative source of categories/questions/options to carry forward.
- The Technical Design artifact is stored at:
  - `.rdd-instance/specifications/technical-design.json` - currently empty
- The new convention must be documented in:
  - `.rdd/conventions/technical-design.convention.md` - currently stating the file to be empty, which should be changed
- The Web UI must render from the new schema and provide a very convenient way to choose answers to part or all topics.
- The Technical Design is **optional**: RDD must not block other flows if it is missing or partial.
- However: whenever any technical design data exists, RDD must **always take it into consideration** in clarify/analyze/plan/implement.
- The spec file must store **only explicitly answered** items. As more are answered, add them dynamically; never pre-fill with all possibilities.
- **All modifications** to `.rdd-instance/specifications/technical-design.json` must be performed via **dedicated Python scripts** invoked from UI or prompts; never write directly from the UI or by manual editing.
- The new schema must support **conditional visibility** (like `visibleWhen` in the legacy schema).
- Remove/avoid “recommended options” concept entirely.

# High-level deliverables

1) **New Technical Design schema (replace legacy schema concept)**
   - Create a new machine-usable schema file (location `.rdd/config/technical-design-schema.json`).
   - The schema must support:
     - categories/sections and groups
     - question id, label, help/description
     - answer types: radio, multiselect, dropdown, free text, numeric, links, file references, tags/key-values (as needed), plus explicit `unknown` / `N/A` options where appropriate
     - conditional visibility via rules (e.g., `visibleWhen`)
   - Do NOT include schema versioning.

2) **New convention document**
   - Update `.rdd/conventions/technical-design.convention.md` describing:
     - purpose and invariants
     - schema structure and supported question types
     - conditional visibility rules
     - storage format of `.rdd-instance/specifications/technical-design.json` (only answered)
     - the required Python scripts for safe updates (create/update/delete answers)
     - how RDD execution must read and apply the tech design (optional but binding when present)
     - Follow the formatting as in the other convention files in `.rdd/conventions`

3) **Web UI: Technical Design page**
   - Implement a page that:
     - Renders the schema dynamically.
     - Navigation is a combination of:
       - a left sidebar listing categories (A)
       - within a category, groups are shown as collapsible accordions (B)
     - Provides:
       - search (search across labels/options/help text; highlight matches)
       - filter (at minimum: by category, by answered/unanswered, by question type)
       - no completion % indicator
     - UX expectations:
       - fast to fill partials
       - clear “Unknown / N/A” choices where relevant
       - expand/collapse all per category
       - jump-to next unanswered (optional but recommended)

4) **Python actions (mandatory)**
   - Implement Python scripts under `.rdd/src/actions/` for:
     - reading tech design (`technical_design_read.py` or equivalent)
     - setting/upserting an answer (`technical_design_answer_set.py`)
     - removing an answer (`technical_design_answer_remove.py`)
     - clearing a category or group answers (optional but useful)
     - validating the stored JSON against the new schema
     - migrating existing legacy format to the new storage format (see migration below)
   - Scripts must be callable similarly to existing requirement scripts (pattern used in `execution.md`).
   - The Web UI must call these scripts; it must not write the spec file directly.

5) **Automatic migration (A)**
   - Provide a migration script that:
     - detects if `.rdd-instance/specifications/technical-design.json` is in an older/legacy shape
     - converts to the new storage format
   - Ensure migration runs safely:
     - either on UI open of the Technical Design page
     - or as a dedicated “migrate now” action invoked by UI at startup when mismatch detected

6) **RDD execution integration**
   - Ensure the framework’s normal execution flow continues to:
     - read `.rdd-instance/specifications/technical-design.json` every run (it already does per `execution.md`)
     - treat it as optional
     - but always comply with it when present:
       - in clarify: questions asked should respect chosen stack/platform/security constraints
       - in analyze/plan/implement: recommended architectures and choices should be consistent with recorded decisions
   - Do not create hard dependencies (no blocking).

# Storage format for `.rdd-instance/specifications/technical-design.json`

Design a storage format optimized for “only answered items” and incremental updates. Requirements:
- Store:
  - `answers[]` or similar collection keyed by `questionId`
  - each entry includes:
    - questionId (stable)
    - type
    - value (scalar, list, object depending on type)
    - timestamps (optional but recommended)
    - optional note/rationale field per answer (recommended)
- No duplication; upsert semantics.
- Keep it straightforward to merge and review in Git.

# Legacy schema extraction instructions (must-do)

Read `TechnicalDesignSchema.json` and carry forward ALL of the following:
- Sections (33):
  - ProjectScale
  - ProductType
  - Criticality
  - ExpectedLifetime
  - EnterpriseConstraints
  - CloudStrategy
  - Compute
  - Frontend
  - Backend
  - Mobile
  - DataAnalytics
  - AI_ML
  - Security
  - Networking
  - CICD_DevOps
  - Observability
  - Compliance_Governance
  - DisasterRecovery
  - OperationalModel
  - DevelopmentProcess
  - ExpandedData
  - DataVisualization
  - DeepDisasterRecovery
  - IntegrationArchitecture
  - PerformanceScalability
  - NonFunctionalRequirements
  - EnvironmentStrategy
  - DeploymentStrategy
  - DataLifecycleRetention
  - SupportHoursSLAs
  - MonitoringMetrics
  - Logging
- For each section:
  - keep groups and their questions
  - keep question labels and types
  - keep options (radio/multiselect/dropdown) verbatim or lightly normalized (but do not lose meaning)
  - keep any conditional visibility logic (`visibleWhen` and similar)
  - keep any helpful subtitles/descriptions, but shorten where obviously verbose

# Implementation steps (required)

1) Inspect current repository structure:
   - locate existing Web UI patterns for “specifications” pages
   - locate how UI calls Python actions today (pattern for requirements is the reference)
   - locate `.rdd/config/manifest.json` conventions for actions (if applicable)

2) Design and implement the new schema:
   - choose “questionnaire-like”, “domain-model-like”, or hybrid—pick what best serves a dynamic UI + stable question IDs + conditional visibility.
   - implement the schema file under `.rdd/…`

3) Implement Python actions:
   - read / validate / upsert answer / remove answer / migrate
   - ensure atomic writes (write temp + replace) to avoid corruption
   - produce clear error messages for UI display

4) Implement Web UI Technical Design page:
   - dynamic rendering from schema
   - sidebar + accordion navigation
   - search + filter
   - per-question editing widgets by type
   - save via calling Python actions (upsert/remove)
   - on load: read current answers and render as filled-in state
   - on schema mismatch or legacy format: trigger migration via Python script

5) Update any RDD runtime integration needed so that:
   - in clarify/analyze/plan/implement, the agent can easily consume the technical design answers (e.g., expose a consolidated view, or ensure existing reads already work).
   - do not block if absent.

6) Documentation:
   - write `.rdd/conventions/technical-design.convention.md`
   - include examples of:
     - schema snippet
     - stored answers file
     - CLI invocations for scripts
   - Update `.rdd/docs/user-guide.md` under "### Technical Design" topic, replacing the WIP string there

7) Tests / validation:
   - add at least minimal unit/integration checks (where repo supports):
     - schema validation
     - migration correctness
     - upsert/remove correctness
   - add a “dry run” / validate-only mode for scripts if appropriate.

# Acceptance criteria (must pass)

- A user can open the Technical Design page and:
  - browse categories/groups
  - search and filter
  - answer any subset of questions
  - see answers persisted and reloaded
- `.rdd-instance/specifications/technical-design.json` contains ONLY answered questions.
- UI never writes the JSON directly; only via Python actions.
- Conditional visibility works and updates dynamically based on answers.
- Legacy/older format tech design files are migrated automatically without data loss.
- RDD flows remain optional but always comply with available technical design decisions.

# Implementation notes (required in implementation.md)

- Briefly explain:
  - why the chosen schema shape is best for UX + maintainability
  - how conditional visibility is represented and evaluated
  - how migration detection works
  - how scripts ensure safe writes and validation


### Modification 001

Error appeared: Error loading technical design: can't access property "value", textarea is null
%%ENDPROMPT

%%PROMPT P-002 "Fix test failures"
Tests failed. Test log is in `.rdd-instance/workdir/P-002_Fix test failures/logs_54657022391`
Troubleshoot, fix, test until all is fixed
%%ENDPROMPT

%%PROMPT P-003 "Remove filter by type in Tech Design page"
There is no need the questions in Tech Design page to be filtered by type. Remove this filter.
%%ENDPROMPT

%%PROMPT P-004 "Tech Dewsign text to reflect all categories"
In Technical Design page, when text search is fulfilled, it should filter the categories and the questions in the categories, not only the current category


### Modification 001

Add a button for clearing the text filter (if possible inside the text field)
%%ENDPROMPT

%%PROMPT P-005 "Remove indication answered vs all question in Tech Design category"
On Tech Design page each category has an indication how many questions are answered vs the total number of questions. Remove this indication as it is confusing
%%ENDPROMPT

%%PROMPT P-006 "Remove filter by status in Tech Design page"
In Tech Design page the filter by status is not behaving properly - sometimes the shown question are not accordingly the choice. Remove this filter entirely
%%ENDPROMPT

%%PROMPT P-007 "Flatten categories content of Tech Design"
In Tech Design page - remove groups accordion representation and flatten questions in the categories. Chane the format of `.rdd/config/technical-design-schema.json`
%%ENDPROMPT

%%PROMPT P-008 "Tech Design - unite to Product"
In Technical Design page unite the categories "Product scale", "Product type", "Criticality". Update all requirements, docstrigs, scripts, etc. where the old id and labels are present.


### Modification 001

When I edit the question "Product categories in scope (select all that apply)" - an error appears "Failed to save answer: Question ID not found in schema: Product_PrimaryProductCategory". Seems the changes introduced inconsistency. Troubleshoot, find the root cause, fix, test.

Also in the console appears "Uncaught SyntaxError: Unexpected end of input (at (index):1:70)" when I press the button for editing a modification. The modification can not be edited. Fix that also.


### Modification 002

Nothing to be done - this is just a test
%%ENDPROMPT

%%PROMPT P-009 "Remove Compliance and Governance"
Remove Technical Design category "Compliance & Governance" with all questions in it
%%ENDPROMPT

%%PROMPT P-010 "Unite Technical Design security"
In Technical Design - merge the questions from "Expanded Security" to "Security & IAM" and remove category "Expanded Security". Rename "Security & IAM" to simply "Security". Update the id and labels. Update the config, convention, requirements whenever needed.
%%ENDPROMPT

%%PROMPT P-011 "Technical Design - Merge Disaster Recovery"
In Technical Design - merge the questions in category "Deep Disaster Recovery" in "Disaster Recovery". Update configs, conventions, requirements.
%%ENDPROMPT

%%PROMPT P-012 "Technical Design - Merge Data"
In Technical Design page - merge in "Data & Analytics" the categories "Expanded Data", "Data Visualization", "Data Lifecycle & Retention"
%%ENDPROMPT
