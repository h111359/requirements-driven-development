# Work Iteration Prompts

## Prompt Definitions

 - [x] [P01] Add to `.rdd/scripts/rdd.py` and `.rdd/scripts/rdd_utils.py` functionality which lists all the files, folders and recursively do the same for their subfolders and stores the result in `.rdd-docs/workspace/files-list.json`. If this file exists - recreate it. For each file write its name, relative path and the time of last change. Exclude folders and subfolders which start with "." or folders like "venv". 
  
 - [x] [P02] Web UI

### What is needed:

What is the possibility to be created a web interface over `.rdd/scripts/rdd.py`. It should be running both under windows and linux and if possible - not to use additional libraries and not be dependent on additional installations. I don't want additional scripts to be created. Everything should be integrated in rdd.py and when rdd.py is started - to open the UI in browser. Use as style the styles in the file `.rdd-docs/workspace/system-questionnaire.html`

### Why it is needed:

More convenience in RDD processing and more ability for additional help and explanations of the options to the user

### Additional Considerations

Plan: Embed Web UI in `.rdd/scripts/rdd.py`
TL;DR: Add a small HTTP server and minimal SPA directly inside rdd.py (no extra files) using only Python stdlib (http.server, threading, webbrowser, subprocess, json). The server binds to loopback, opens the browser, exposes JSON/SSE endpoints and invokes existing RDD functions in-process (with a subprocess fallback). Minimal safe changes to rdd.py are required so import/use is non-destructive.

Goal: Add an embedded web UI inside .rdd/scripts/rdd.py only (no extra files, no new deps beyond Python stdlib). Running python .rdd/scripts/rdd.py on Windows and Linux should start a localhost HTTP server, open the browser to the UI, and expose endpoints to run RDD actions.

Server: use ThreadingHTTPServer (or similar) bound to 127.0.0.1, port=0 for auto-pick. Generate a random token; require it via header or ?token=. HTTP only on loopback.

Start a loopback-only server with defaults host=127.0.0.1 and port=0 (OS picks a free port). If binding fails, retry on a new ephemeral port; if the IPv4 loopback isn’t available, switch to the IPv6 loopback address 0:0:0:0:0:0 (line 0, column 1). Also honor optional env/flags (RDD_HOST, RDD_PORT, --host, --port) when set.

UI assets: inline HTML/JS/CSS strings served by the handler (no external files). If SSE is supported via stdlib, serve logs as text/event-stream; otherwise allow long-polling fallback—pick one and implement it fully.

Actions: support all actions in rdd.py available. Provide a start_rdd_task(action, options, log_cb) running in background threads in-process; if in-process fails, fallback to a subprocess using sys.executable rdd.py <domain> <action>. No interactive prompts; if required input is missing, return structured errors.

Cancellation: implement cancel_rdd_task(run_id); on Unix use process groups and os.killpg; on Windows use CREATE_NEW_PROCESS_GROUP and TerminateProcess/CTRL_BREAK as appropriate.
Main entry: default to web UI when no args; provide --cli or RDD_NO_WEB_UI=1 to force the old CLI menu.

Behavior guarantees: no top-level side effects on import; avoid sys.exit inside internal call paths; return structured JSON responses {run_id, state, error?}.
Concurrency/state: in-memory run registry; reasonable cap on concurrent tasks (e.g., 2-4) is fine; no persistence needed.

Validation: describe a quick manual check (run script, see URL printed, browser opens, start action, see live logs, cancel works).


 - [x] [P03] Analyze and update requirements and tech-spec based on PRS

Context:
- Product Requirements: docs/ProductRequirementsSpecification.md
- Baseline requirements: .rdd-docs/requirements.md
- Baseline technical spec: .rdd-docs/tech-spec.md
- Comparison notes (draft): .rdd-docs/workspace/compare-requirements.md

Task:
1. Re-read docs/ProductRequirementsSpecification.md and .rdd-docs/requirements.md.
2. Treat .rdd-docs/requirements.md as the primary requirements document; PRS overrides only where it introduces new behavior or clearly replaces existing behavior.
3. Using .rdd-docs/workspace/compare-requirements.md as input (not as truth), produce:
   - A list of concrete requirement changes to apply to .rdd-docs/requirements.md:
     - New requirements to add (with proper IDs and sections GF/FR/NFR/TR).
     - Existing requirements to modify (show [OLD] and [NEW] text).
     - Existing requirements to mark as [DELETED] or [DEPRECATED].
   - A list of matching updates needed in .rdd-docs/tech-spec.md (sections, paragraphs, bullets).

4. Output three clearly separated sections in your answer:
   - "Planned changes for .rdd-docs/requirements.md"
   - "Planned changes for .rdd-docs/tech-spec.md"
   - Implementation steps to be executed so to implement the changes

5. Then, at the end of your reply, generate a *single* implementation prompt P04(detailed prompt text) that will:
   - Apply all decided changes to .rdd-docs/requirements.md and .rdd-docs/tech-spec.md.
   - Keep formatting and IDs consistent with .rdd/templates/requirements-format.md.
   - Implement the changes in the code

Constraints:
- Do NOT directly edit any file in this step; only propose exact P04 text in markdown.
- Respect existing numbering and [DELETED]/[DEPRECATED] conventions in .rdd-docs/requirements.md.
- Reference sections in .rdd-docs/tech-spec.md by headings so edits are easy to apply manually.

Deliverables:
- Validated and complete list of requirement and tech-spec updates.
- A ready-to-use P04 implementation prompt text that I can copy into .rdd-docs/work-iteration-prompts.md.
 
 - [x] [P04]   <START-OF-P04>
 
 Apply PRS-based requirement and tech-spec updates, create prompt folder structure, stub execute command

**Context**:
- Analysis completed in `.rdd-docs/workspace/P03-implementation.md`
- Planned changes documented in P03 analysis (three sections: requirements changes, tech-spec changes, implementation steps)
- PRS alignment decisions: partial redesign, full Web portal docs, single-prompt model, new execute requirements, detailed Web UI specs
- User design preferences: Q1=b, Q2=a, Q3=b, Q4=a, Q5=a

**Objectives**:
1. Update `.rdd-docs/requirements.md` with all planned changes (new requirements, modifications, deprecations)
2. Update `.rdd-docs/tech-spec.md` with all planned changes (new sections, section updates)
3. Create `.rdd/prompts/` directory structure with placeholder prompt files
4. Create/update template files for single-prompt model
5. Stub out execute command in `rdd.py` and `rdd_utils.py`
6. Update build/installer to handle new prompt folder and gitMode config

**Detailed Tasks**:

### Task 1: Update `.rdd-docs/requirements.md`

**Add new requirements** at end of each section (preserve existing numbering, continue from highest ID):

*General Functionalities* (after GF-12):
- [GF-13] Web-Based UI for Prompt and Workspace Management: The framework shall provide a web-based user interface hosted on a local web server and opened automatically in the user's default browser, allowing creation, editing, and management of prompts, questionnaires, implementation plans, technical specifications, file structure, requirements, and workspace/version control operations.
- [GF-14] Prompt Authoring Persistence: Prompts shall be authored through the Web UI and persisted as Markdown files in the repository; ad-hoc prompt text typed only into Copilot chat shall not be used as canonical prompt definitions, ensuring traceability and history preservation.

*Functional Requirements* (after FR-129):
- [FR-130] Canonical Prompt Storage and Precedence: The framework shall define two prompt storage locations with clear purpose: `.rdd/prompts/` for framework-provided reusable prompt templates, and `.github/prompts/` for repository-specific Copilot prompt files. The `execute` command and Web UI shall use `.rdd/prompts/` as the primary location for user-created and framework templates, with `.github/prompts/` reserved for GitHub Copilot integration prompts. Configuration shall allow override of this precedence.
- [FR-131] Single Active Work-Iteration Prompt File: The framework shall maintain a single active work-iteration prompt file named `work-iteration-prompt.md` located at `.rdd-docs/work-iteration-prompt.md`. At any time it shall contain exactly one active prompt definition to be executed by the `execute` command. Multi-prompt checklist files may exist as supporting artifacts but are not used directly by `execute`.
- [FR-132] Execute Command Ordered Workflow: The `execute` command shall implement the following ordered steps: (1) read the current prompt from `.rdd-docs/work-iteration-prompt.md`, (2) create an implementation file in `.rdd-docs/workspace/` with a filename based on prompt ID and copy the full prompt text into it, (3) load `.rdd-docs/requirements.md` and `.rdd-docs/tech-spec.md`, (4) optionally read additional repository files for context, (5) if context remains incomplete or ambiguous, generate a questionnaire requiring developer input and write it to the implementation file, (6) produce a detailed implementation plan and write it to the implementation file, (7) execute the implementation plan, (8) update `.rdd-docs/requirements.md` and `.rdd-docs/tech-spec.md` to reflect all changes made, and (9) mark the prompt as completed in the source file.
- [FR-133] Web UI Prompt Management Page: The Web UI shall provide a Prompt Management page allowing users to load the current content of `work-iteration-prompt.md`, edit it in-place with a text editor component, save changes back to the file, display any generated questionnaire with input fields for responses, and display the generated implementation plan.
- [FR-134] Web UI Technical Specification Page: The Web UI shall provide a Technical Specification page with two sub-features: (a) a Technical Design editor that loads a structured JSON design document, presents a form generated from a design configuration JSON defining structure/options/defaults, supports predefined answer options with single/multiple selection and free-text input, implements conditional/hierarchical question logic, and provides a "Set Default Answers" function to populate unanswered fields; and (b) a File & Folder Structure visualizer allowing controlled updates to the project folder structure.
- [FR-135] Web UI Requirements Page: The Web UI shall provide a Requirements page supporting two operations: (a) generate a prompt for adding a new requirement, pre-populating the prompt template with requirement metadata, and (b) reverse-engineer requirements from the existing project state by analyzing code, documentation, and configuration files to propose requirement additions.
- [FR-136] Web UI Version Control & Workspace Management Page: The Web UI shall provide a Version Control & Workspace Management page supporting operations for creating branches, updating from the default branch, committing changes, switching to the default branch, merging branches, archiving the workspace, and loading an archived workspace. All git operations shall respect the configured operational mode (noGit, localGit, remoteGit).
- [FR-137] Web UI Administration Page: The Web UI shall provide an Administration page for configuring framework settings including default branch, operational mode (noGit, localGit, remoteGit), local-only mode toggle, version information, and other administrative options.
- [FR-138] Web UI Predefined Prompts Library: The Web UI shall provide access to predefined prompt files stored in `.rdd/prompts/`, allowing users to browse available prompts (requirement revision, folder structure sync, questionnaire generation, etc.) and load any prompt file entirely into `work-iteration-prompt.md` for execution.
- [FR-139] Questionnaire Response Interface: When the `execute` command generates a questionnaire due to incomplete or ambiguous context, the Web UI shall display the questionnaire on the Prompt Management page with input fields for each question, save responses back to the implementation file, and allow re-execution of the `execute` command to continue with the provided answers.
- [FR-140] Implementation Plan Review Interface: After the `execute` command generates an implementation plan, the Web UI shall display the plan on the Prompt Management page, allow users to review and optionally edit the plan, and provide a mechanism to approve and proceed with execution or request plan regeneration.

*Non-Functional Requirements* (after NFR-20):
- [NFR-21] Web UI User Experience: The Web UI shall provide a modern, responsive interface optimized for desktop browsers, with clear navigation between pages, real-time feedback on operations, color-coded status indicators (success: green, error: red, warning: yellow, info: blue), and graceful error handling with user-friendly messages.

*Technical Requirements* (after TR-54):
- [TR-130] Prompts Folder in .rdd for Framework Prompts: The `.rdd/prompts/` directory shall store framework-provided reusable prompt templates; the installer and build processes shall populate this directory with framework prompts during installation. Repository-specific Copilot prompts shall remain in `.github/prompts/` and the `execute` command shall prefer `.rdd/prompts/` for user-created and framework templates unless configuration specifies otherwise.
- [TR-131] Operational Modes Explicit Enumeration: The framework shall support three operational modes configurable in `config.json` via a `gitMode` field: (a) `noGit` - no git operations performed, all version control features disabled; (b) `localGit` - git operations performed locally only, no remote fetch/push/pull; (c) `remoteGit` - full git operations including remote synchronization. Installation process shall prompt users to select mode, and all git-dependent workflows shall check and respect the configured mode.
- [TR-132] Web Server Implementation: The Web UI shall be implemented using Python's built-in `http.server` module or equivalent stdlib components, binding to `127.0.0.1` (localhost) with an auto-selected ephemeral port, and automatically opening the user's default browser to the UI URL. The server shall serve inline HTML/CSS/JavaScript assets (no external files required), expose RESTful JSON endpoints for file operations and command execution, and implement basic security via a randomly generated session token required for all operations.

**Modify existing requirements** (replace full text, preserve ID):

*TR-12*: Replace entire bullet text with:
"Prompts Location: The framework shall use two prompt locations: framework templates and user-created prompts in `.rdd/prompts/`, and repository-specific Copilot prompt files in `.github/prompts/`. The `execute` command and Web UI shall prefer `.rdd/prompts/` for templates and execution, with `.github/prompts/` reserved for GitHub Copilot integration prompts. Configuration may override this precedence."

*FR-05*: Replace entire bullet text with:
"Workspace Initialization: A script shall initialize workspace with a single active prompt file: `work-iteration-prompt.md` (located at `.rdd-docs/work-iteration-prompt.md`). Multi-prompt checklist files may be created as supporting artifacts but are not required for execution."

*FR-82*: Replace entire bullet text with:
"Iteration Workspace Initialization: The create iteration workflow shall initialize the single active prompt file `work-iteration-prompt.md` at `.rdd-docs/work-iteration-prompt.md` from template, keeping workspace minimal. Multi-prompt checklists may be created as supporting artifacts but are not part of the primary execution model."

*FR-100*: Replace entire bullet text with:
"Work Iteration Prompt Backup and Reset: During iteration completion, the system shall copy `.rdd-docs/work-iteration-prompt.md` to `.rdd-docs/workspace/` as a backup and then reset the main file from the template to prepare for the next iteration. Any supporting multi-prompt checklist files shall also be backed up to workspace."

**Deprecate requirements** (replace full text with [DEPRECATED] marker):

*TR-24*: Replace entire bullet text with:
"[DEPRECATED]: Legacy Bash script requirement replaced by Python-based implementation in `rdd.py`. See FR-47 and FR-69 for Python-first policy."

*TR-25*: Replace entire bullet text with:
"[DEPRECATED]: Legacy Bash script requirement replaced by Python-based implementation in `rdd.py`. See FR-47 and FR-69 for Python-first policy."

*TR-26*: Replace entire bullet text with:
"[DEPRECATED]: Legacy Bash script requirement replaced by Python-based implementation in `rdd.py`. See FR-47 and FR-69 for Python-first policy."

*TR-27*: Replace entire bullet text with:
"[DEPRECATED]: PowerShell scripts no longer required due to Python cross-platform implementation. See FR-47 and FR-69 for Python-first policy."

*TR-28*: Replace entire bullet text with:
"[DEPRECATED]: Platform-specific script directories (`src/linux/.rdd/scripts/`, `src/windows/.rdd/scripts/`) no longer used. Python implementation in `.rdd/scripts/` provides cross-platform support. See FR-47 and FR-69 for Python-first policy."

**Validation**: After all edits, verify:
- All ID sequences continuous and in order per section (GF, FR, NFR, TR)
- No duplicate IDs
- All [DELETED] and [DEPRECATED] markers preserved
- Formatting consistent with existing style

### Task 2: Update `.rdd-docs/tech-spec.md`

**Add new "Web UI Architecture" section** under "Component Architecture" (insert after "### Utility Scripts" subsection, before "### Cross-Platform Implementation"):

```markdown
### Web UI Architecture

The framework provides a browser-based interface for prompt management, technical specification editing, requirements management, and workspace operations.

#### Web Server Implementation
- **Technology**: Python's built-in `http.server.ThreadingHTTPServer` or equivalent stdlib component
- **Binding**: Localhost (`127.0.0.1`) with ephemeral port (OS-assigned)
- **Security**: Random session token generated on startup, required in `Authorization` header or query parameter
- **Lifecycle**: Server starts automatically when RDD framework invoked without CLI arguments; opens default browser to `http://127.0.0.1:<port>/?token=<token>`
- **Shutdown**: User closes browser tab; server terminates on idle timeout or explicit shutdown command

#### UI Technology Stack
- **Inline Assets**: All HTML, CSS, and JavaScript served as inline strings from Python handler (no external files)
- **Styling**: Minimalist CSS based on existing RDD styles (see [system-questionnaire.html](http://_vscodecontentref_/40) for reference)
- **No External Dependencies**: No npm, webpack, or third-party JS libraries required
- **Client-Side Logic**: Vanilla JavaScript for form handling, AJAX requests, and page navigation

#### Page Structure and Routing
The Web UI consists of six main pages, each served by a dedicated route:

1. **`/` or `/prompts`** - Prompt Management Page
   - Displays current content of `.rdd-docs/work-iteration-prompt.md`
   - Provides text editor for in-place editing
   - Shows generated questionnaire (if any) with input fields
   - Displays implementation plan (if any)
   - Buttons: Save, Execute Command, Load Predefined Prompt

2. **`/techspec`** - Technical Specification Page
   - Sub-tab: Technical Design JSON editor (form-based)
   - Sub-tab: File & Folder Structure visualizer
   - Loads design config JSON to generate form dynamically
   - Supports conditional/hierarchical questions
   - Button: Set Default Answers, Save Design

3. **`/requirements`** - Requirements Page
   - Button: Generate Add Requirement Prompt
   - Button: Reverse-Engineer Requirements
   - Displays generated prompts for review before copying to `work-iteration-prompt.md`

4. **`/vcs`** - Version Control & Workspace Management Page
   - Buttons: Create Branch, Update from Default, Commit Changes, Switch to Default, Merge Branch
   - Buttons: Archive Workspace, Load Archived Workspace
   - Displays git status, branch info, and operation results

5. **`/admin`** - Administration Page
   - Configuration editor: defaultBranch, gitMode, localOnly, version
   - Displays current config values
   - Allows saving updated config back to `config.json`

6. **`/library`** - Predefined Prompts Library
   - Lists all `.md` files in [prompts](http://_vscodecontentref_/41)
   - Shows preview of each prompt
   - Button: Load into `work-iteration-prompt.md`

#### Data Persistence and File Operations
- **File Read/Write**: Web server handler uses Python's `open()`, `json.load()`, `json.dump()` for file operations
- **Git Operations**: Executes git commands via `subprocess` module, respecting `gitMode` from config
- **Validation**: Server-side validation of all user inputs before file writes
- **Error Handling**: Returns JSON responses with `{success: bool, message: str, data: obj}` format

#### Execute Command Integration
- **Endpoint**: `POST /api/execute`
- **Behavior**: 
  - Reads `.rdd-docs/work-iteration-prompt.md`
  - Invokes execute command handler (from `rdd_utils.py` or dedicated module)
  - Streams execution logs back to client via JSON polling or SSE
  - Updates implementation file in real-time
  - Returns completion status and links to generated files
- **Concurrency**: Only one execute command may run at a time; subsequent requests return "busy" status

Add new "Execute Command Flow" subsection under "Command Routing Pattern" section (insert after the existing command examples):

### Execute Command Flow

The `execute` command is the primary entry point for prompt execution, integrating requirement analysis, planning, implementation, and documentation updates in a single automated workflow.

**Command**: `python .rdd/scripts/rdd.py execute` or invoked via Web UI button

**Ordered Steps**:

1. **Read Current Prompt**: Load full content of `.rdd-docs/work-iteration-prompt.md`
   - Validate file exists and is non-empty
   - Parse prompt metadata (if present): ID, tags, dependencies

2. **Create Implementation File**: Generate `<prompt-id>-implementation.md` in `.rdd-docs/workspace/`
   - Filename format: `P<nn>-implementation.md` or `<custom-id>-implementation.md`
   - Copy full prompt text as first section
   - Initialize sections: Context Summary, Questionnaire, Plan, Execution Log, Results

3. **Load Requirements and Tech Spec**: Read `.rdd-docs/requirements.md` and `.rdd-docs/tech-spec.md`
   - Parse existing requirement IDs and sections
   - Build context map of current system state

4. **Contextual File Reading** (optional): Based on prompt content, identify and read additional repository files
   - Parse imports, references, and file paths mentioned in prompt
   - Load relevant source files, configs, documentation
   - Append summaries to implementation file Context section

5. **Ambiguity Detection and Questionnaire Generation**: Analyze prompt against requirements and tech-spec
   - Check clarity checklist (`.rdd/templates/clarity-checklist.md`)
   - Identify missing information not already documented
   - If ambiguities found:
     - Generate questionnaire following `.rdd/templates/questions-formatting.md`
     - Write questions to implementation file Questionnaire section
     - Pause execution and prompt user for answers via Web UI or CLI
     - On re-execution, load answers and continue

6. **Implementation Plan Generation**: Produce detailed, step-by-step plan
   - Break down prompt into concrete tasks
   - Identify files to create/modify/delete
   - Specify commands to run, tests to write, documentation updates
   - Write plan to implementation file Plan section
   - Include expected outcomes and validation criteria

7. **Plan Execution**: Execute each planned step
   - Create/modify files using appropriate edit tools
   - Run commands via subprocess
   - Log each action to implementation file Execution Log section
   - Capture outputs, errors, and results
   - On error: pause, log error, prompt user for resolution

8. **Requirements and Tech-Spec Update**: After successful execution, update documentation
   - Add new requirements with proper IDs (continue from highest ID in each section)
   - Modify existing requirements where behavior changed (preserve IDs)
   - Mark obsolete requirements as `[DELETED]` or `[DEPRECATED]`
   - Update tech-spec sections to reflect architecture/implementation changes
   - Validate ID sequences remain continuous

9. **Mark Prompt as Completed**: Update prompt file to indicate completion
   - If using multi-prompt checklist: change `- [ ]` to `- [x]`
   - If using single prompt file: add completion timestamp and archive marker
   - Optionally move completed prompt to archive or history

**Error Handling**: At each step, if an error occurs:
- Log error to implementation file
- Return structured error response to caller
- Preserve partial work (don't delete implementation file or undo changes)
- Provide recovery guidance (re-run with fixes, manual intervention, rollback options)

**Output Artifacts**:
- Implementation file: `.rdd-docs/workspace/<prompt-id>-implementation.md`
- Updated requirements: `.rdd-docs/requirements.md`
- Updated tech-spec: `.rdd-docs/tech-spec.md`
- Modified source files, configs, tests (as per plan)
- Execution logs (in implementation file)

Find "Key Principles" subsection and add new principle 6:

6. **Prompt Storage Locations**
   - `.rdd/prompts/`: Framework-provided and user-created reusable prompt templates
   - `.github/prompts/`: Repository-specific GitHub Copilot integration prompts
   - `.rdd-docs/work-iteration-prompt.md`: Single active prompt file for execute command
   - Multi-prompt checklists may exist as supporting artifacts but are not primary execution mechanism

   Add new subsection "Operational Modes" after "Configuration Priority":

   #### Operational Modes

The framework supports three git operational modes, configured via the `gitMode` field in `config.json`:

1. **`noGit`** - No Git Operations
   - No git commands executed
   - Version control features disabled in Web UI and CLI
   - Suitable for non-git projects or pure experimentation
   - Workspace management (archive, backup) still functional using filesystem operations

2. **`localGit`** - Local Git Only
   - Git commands executed for local operations: commit, branch, merge, status
   - No remote operations: fetch, push, pull skipped
   - Equivalent to previous `localOnly: true` configuration
   - Suitable for local-only repositories or offline development

3. **`remoteGit`** - Full Git with Remote (default)
   - All git operations enabled: local and remote
   - Fetch, push, pull executed during sync and wrap-up workflows
   - Suitable for standard GitHub-backed repositories

**Mode Selection**:
- User prompted during installation to select mode
- Mode stored in `config.json` and respected by all workflows
- Can be changed later via Web UI Administration page or `python .rdd/scripts/rdd.py config set gitMode <mode>`

**Backward Compatibility**:
- Existing `localOnly: true` configs automatically migrated to `gitMode: "localGit"`
- Existing `localOnly: false` configs automatically migrated to `gitMode: "remoteGit"`

 <END-OF-P04>
