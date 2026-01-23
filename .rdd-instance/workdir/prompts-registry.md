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

%%PROMPT P-013 "Unite observability"
In Technical Design page - merge in "Observability" the categories "Monitoring Metrics", "Logging"
%%ENDPROMPT

%%PROMPT P-014 "Technical Design - Merge Deployment"
In Technical Design page - merge the categories "CI/CD & DevOps" in "Deployment Strategy" and rename to simply "Deployment"
%%ENDPROMPT

%%PROMPT P-015 "Tech Design Editor"
I need an editor of the `.rdd/config/technical-design-schema.json` with web interface.
It should be created with html, css and vanila JavaScript in a new folder "tech_design_schema_editor" in the repo root
The editor should be able to read and write `.rdd/config/technical-design-schema.json`
If needed, create a local web server to overcome the limitations of browser to manipulate files in the file system
The editor should be able to create new questions, edit the existing questions and delete questions from the current `.rdd/config/technical-design-schema.json`
The editor should be entirely independent from the scripts in .rdd and .rdd-instance folders
Copy the css for Technical Design page so to have same look and feel

**Objective**: Create a standalone web-based editor for managing the Technical Design schema file (`.rdd/config/technical-design-schema.json`) with full CRUD capabilities and validation.

**Context**:
- The Technical Design schema defines the questions, categories, and options shown in the RDD Framework's Technical Design page
- The schema structure is defined in P-001 implementation with categories, groups, questions, and conditional visibility rules
- This editor must be independent of the RDD framework runtime - it should work as a standalone tool that can be run separately
- The schema file is critical infrastructure - invalid schemas will break the Technical Design page

**Requirements**:

1. **Location & Independence**:
   - Create in folder: `tech_design_schema_editor/` at repository root
   - Must not depend on `.rdd/` or `.rdd-instance/` runtime scripts or files
   - Should work when run standalone, even if moved to a different location
   - Can be run by developers when they need to modify the schema via run_editor.bat and run_editor.sh files in `tech_design_schema_editor/`

2. **Technology Stack**:
   - Server: Python HTTP server (similar to `.rdd/src/web/server.py` pattern)
   - Frontend: HTML, CSS, vanilla JavaScript only
   - CSS: Extract relevant styles from Technical Design page (`.rdd/src/web/static/style.css`) for consistent look and feel
   - No external JavaScript libraries except for optional syntax highlighting

3. **Functionality**:
   - **Load Schema**: Read `.rdd/config/technical-design-schema.json` on startup
   - **Navigate**: Browse categories and questions with tree/sidebar navigation
   - **Create**: Add new categories, groups, and questions
   - **Edit**: Modify existing questions, options, help text, conditional rules
   - **Delete**: Remove categories, groups, or questions
   - **Validate**: Real-time validation of schema structure before save
   - **Save**: Write validated schema back to file with atomic write operation

4. **UI Layout**:
   - Two-panel layout:
     - Left sidebar: Tree navigation showing categories → groups → questions
     - Right panel: Form editor for selected item
   - Top toolbar: Save, Validate, Reload, Backup buttons
   - Status bar: Validation messages and save status

5. **Validation Requirements**:
   - Required fields present (id, label, type for questions)
   - Question IDs are unique across entire schema
   - Valid question types (radio, multiselect, dropdown, text, number, etc.)
   - Valid option structures for choice-based questions
   - Conditional visibility rules (`visibleWhen`) are syntactically valid
   - No circular dependencies in visibility rules

6. **Question Types to Support**:
   Based on the existing schema structure (from P-001):
   - `radio` - single selection from options
   - `multiselect` - multiple selections from options  
   - `dropdown` - single selection dropdown
   - `text` - free text input
   - `number` - numeric input
   - `textarea` - multi-line text
   - Support for `visibleWhen` conditional rules on any question

7. **Error Handling**:
   - Show validation errors inline with specific field references
   - Prevent saving invalid schemas
   - Create automatic backup before each save
   - Provide clear error messages for file system failures
   - Handle malformed JSON gracefully with recovery options

8. **Server API Endpoints**:
   - `GET /api/schema` - Load schema from file
   - `POST /api/schema` - Save schema to file (with validation)
   - `POST /api/validate` - Validate schema without saving
   - `POST /api/backup` - Create timestamped backup of current schema
   - `GET /` - Serve the editor HTML page

9. **Implementation Approach**:
   - Start with the Hybrid Approach (see Proposal 3 in analysis)
   - Two-panel layout with form-based editing
   - Text editor for `visibleWhen` rules with syntax highlighting
   - Bootstrap 5 for UI components (consistent with existing Web UI)
   - Atomic file writes (write to temp, then rename)

10. **Testing & Documentation**:
    - Include README.md in `tech_design_schema_editor/` with:
      - How to start the server
      - How to access the editor
      - Schema structure documentation
      - Validation rules
    - Manual testing checklist for CRUD operations
    - Example of adding a new category and question

**Acceptance Criteria**:
1. Server starts successfully and opens editor in browser
2. Can load existing schema without errors
3. Can create new category with questions
4. Can edit existing questions and options
5. Can delete questions and categories
6. Validation catches common errors (duplicate IDs, missing required fields)
7. Invalid schemas cannot be saved
8. Saved schemas can be loaded by Technical Design page without errors
9. UI is responsive and matches Technical Design page style
10. All operations provide clear user feedback (success/error messages)

**Out of Scope** (can be added later if needed):
- Drag-and-drop reordering
- Undo/redo functionality
- Visual rule builder for conditional logic (use text editor instead)
- Multi-language support
- Real-time collaboration

**Implementation Notes Required**:
- Document the schema validation rules implemented
- Explain the atomic write approach for file safety
- Document any limitations or known issues
- Provide examples of adding different question types
%%ENDPROMPT

%%PROMPT P-016 "Fix validation error of tech design schema editor"
When validate the current schema in "Technical Design Schema Editor", it says categories[2].question[2].visibleWhen must be a string (3 times)
This validation seems to be wrong
Find the issue and fix it


### Modification 001

Currently the value of equals is expected to be array only. It could be a string as well. Modify


### Modification 002

In validation errors instead of indexes of categories and questions should be written the name of the category and the name of the question
%%ENDPROMPT

%%PROMPT P-017 "Rationale"
Technical design rationale field - implement the functionality so to be able to edit the rationale in the Web UI.

## Objective
Implement UI controls for editing the optional `rationale` field in the Technical Design page, allowing users to provide explanations for their architectural decisions.

## Context
- The backend already supports rationale: `technical_design_answer_set.py` accepts `rationale=` parameter (TR-0189)
- The `/api/technical-design/answer/set` endpoint accepts rationale in requests
- The frontend Technical Design page (`app.js`) currently has no UI controls for rationale
- Answer objects in `.rdd-instance/specifications/technical-design.json` include an optional `rationale` field

## Requirements
1. Display a textarea input for rationale on the Technical Design page
2. The textarea should appear inline below the answer selection controls
3. Only show rationale input when an answer exists for the question
4. Auto-save rationale to backend on blur (when user clicks away)
5. Display existing rationale text when loading answered questions
6. Clear rationale when the answer is cleared via "Clear Answer" button
7. Preserve existing rationale when updating an answer value

## Implementation Approach
**Location**: Modify the `renderQuestion()` function in `.rdd/src/web/static/app.js`

**Steps**:
1. Add rationale textarea element after answer controls when `currentAnswer` exists
2. Populate textarea with `currentAnswer.rationale` value (if any)
3. Add `onblur` handler to save rationale along with answer
4. Update `saveQuestionAnswer()` to include rationale in API request body
5. Ensure `clearQuestionAnswer()` also clears rationale

**UI Specifications**:
- Use Bootstrap `form-control` class for consistent styling
- Set `rows="3"` for comfortable editing
- Placeholder: "Explain the reasoning for this answer..."
- Label: "Rationale (optional)"
- Position: Between the current answer display and the Clear Answer button

## Acceptance Criteria
- ✅ User can type rationale text when editing any answered question
- ✅ Rationale auto-saves when user clicks away from textarea (blur event)
- ✅ Existing rationale loads and displays when viewing answered questions
- ✅ Rationale is cleared when user clicks "Clear Answer"
- ✅ Rationale is preserved when user changes the answer value
- ✅ Works correctly for all three question types (radio, multiselect, text)
- ✅ No console errors or API failures

## Testing Checklist
1. Answer a new question and add rationale → verify saves correctly
2. Reload page → verify rationale displays correctly
3. Update answer value → verify rationale is preserved
4. Clear answer → verify rationale is cleared
5. Test with radio, multiselect, and text question types
6. Test with and without existing rationale
%%ENDPROMPT

%%PROMPT P-018 "Troubleshoot search in Technical Design"
The search filed in Technical Design page is not working. 

**Root Cause:**
The search functionality in the Technical Design page is failing because the code in `applySearchFilter()` function (line 3514 in app.js) attempts to iterate over `category.groups`, but the schema was flattened in prompt P-007 ("Flatten categories content of Tech Design") which removed the groups structure entirely. Categories now directly contain a `questions` array instead of having a nested `groups` structure.

The console sais:
app.js:3517 Uncaught TypeError: Cannot read properties of undefined (reading 'forEach')
    at app.js:3517:25
    at Array.forEach (<anonymous>)
    at applySearchFilter (app.js:3514:33)
    at applyTechnicalDesignFilters (app.js:3478:5)
    at HTMLInputElement.<anonymous> (app.js:3455:9)

Troubleshoot, find the root cause. Implement the best fix. Test.

Beyond fixing search, audit entire app.js for any other references to removed schema structures.

Improved prompt:

**Context**:
- In prompt P-007, the Technical Design schema was flattened to remove the groups accordion structure
- Categories now directly contain `questions` arrays instead of nested `groups` structures
- The schema change was implemented in `.rdd/config/technical-design-schema.json`
- Normal category browsing was updated to work with the flattened structure
- However, the search functionality was not updated and is now broken

**Current Behavior**:
When typing in the search field on the Technical Design page, the following error appears in the browser console:
```
app.js:3517 Uncaught TypeError: Cannot read properties of undefined (reading 'forEach')
    at app.js:3517:25
    at Array.forEach (<anonymous>)
    at applySearchFilter (app.js:3514:33)
    at applyTechnicalDesignFilters (app.js:3478:5)
    at HTMLInputElement.<anonymous> (app.js:3455:9)
```

**Root Cause**:
The `applySearchFilter()` function at line 3514 in `.rdd/src/web/static/app.js` still attempts to iterate over `category.groups`, which no longer exists in the flattened schema.

**Expected Behavior**:
Search should filter questions across all categories based on matching text in:
- Question labels
- Question help text  
- Option labels

**Tasks**:
1. **Audit**: Search for all references to `category.groups` in `.rdd/src/web/static/app.js`
2. **Fix**: Update `applySearchFilter()` to iterate over `category.questions` directly
3. **Verify**: Check related functions `renderSearchResults()` and `renderFilteredCategoryList()` for schema assumptions
4. **Test**: Verify search works for:
   - Single-word searches
   - Multi-word searches
   - Searches matching labels, help text, and options
   - Search with no results
   - Clearing search filter

**Files to Modify**:
- `.rdd/src/web/static/app.js` (lines around 3514)

**Acceptance Criteria**:
- Search field accepts input without console errors
- Search correctly filters questions across all categories
- Matching questions are displayed with their category context
- "No results" message appears when search has no matches
- Clearing search returns to normal category view
- All test scenarios pass
%%ENDPROMPT

%%PROMPT P-019 "Move question options up and down"
In Technical Design Schema Editor in `tech_design_schema_editor` I want to be able to move the categories, questions and question answer options up and down 

### Improved Prompt Version

```
Add reordering functionality to the Technical Design Schema Editor (`tech_design_schema_editor/`) to allow users to change the order of categories, questions, and question options.

**Context:**
- Editor location: `tech_design_schema_editor/`
- Schema file: `.rdd/config/technical-design-schema.json`
- Current implementation: Vanilla JavaScript (~785 lines), no external libraries
- Existing capabilities: Full CRUD, tree navigation, search, validation

**Requirements:**

1. **Reordering Mechanisms:**
   - Categories: Reorder within schema.categories array
   - Questions: Reorder within category.questions array
   - Options: Reorder within question.options array

2. **UI Controls - Arrow Buttons:**
   - Add inline up (↑) and down (↓) arrow buttons
   - Always visible next to each item
   - Disable up button on first item
   - Disable down button on last item
   - Use unicode symbols: ↑ (U+2191), ↓ (U+2193)
   - Add aria-label for accessibility

3. **Keyboard Shortcuts:**
   - Alt+Up: Move selected item up
   - Alt+Down: Move selected item down
   - Add global keydown listener
   - Use event.preventDefault() to avoid browser conflicts
   - Track currently selected item (category/question/option)

4. **Behavior:**
   - Swap adjacent items in array
   - Mark schema as modified (trigger existing modified flag)
   - Re-render affected UI sections
   - Maintain focus on moved item after reordering
   - Require manual save (consistent with editor workflow)

5. **Implementation Details:**
   - Use array destructuring for swapping: `[arr[i], arr[j]] = [arr[j], arr[i]]`
   - Add boundary checks before moving
   - Update button disabled states after each move
   - Preserve all item properties during move
   - No external libraries (vanilla JavaScript only)

6. **Integration Points:**
   - Modify tree rendering to include arrow buttons
   - Modify option rendering in question form editor
   - Add event handlers for button clicks
   - Add global keyboard event listener
   - Use existing `setModified()` function to mark changes

7. **Testing Requirements:**
   - Test edge cases: first item, last item, single item
   - Verify keyboard shortcuts work across browsers
   - Ensure focus management works correctly
   - Validate data integrity after multiple moves
   - Test with empty arrays

8. **Documentation:**
   - Update README.md with new reordering feature
   - Document keyboard shortcuts
   - Add usage examples for reordering

**Deliverables:**
- Modified `tech_design_schema_editor/static/app.js`
- Modified `tech_design_schema_editor/index.html` (if needed for styling)
- Modified `tech_design_schema_editor/static/style.css` (if needed)
- Updated `tech_design_schema_editor/README.md`

**Success Criteria:**
- Users can reorder categories using buttons and keyboard
- Users can reorder questions using buttons and keyboard
- Users can reorder options using buttons and keyboard
- Buttons are properly enabled/disabled at boundaries
- Schema is marked as modified after reordering
- Changes persist when saved
- Keyboard shortcuts don't conflict with browser shortcuts
- Feature is documented in README
%%ENDPROMPT

%%PROMPT P-020 "Tech design schema editor - auto save"
I want the Technical Design Schema Editor in `tech_design_schema_editor` to save automatically the changes made by the user in the Web UI. There should be no need of save buttons.
%%ENDPROMPT

%%PROMPT P-021 "Remove Save Question button"
In Technical Design Schema Editor remove "Save Question" button as the question modifications should be automatically saved


### Modification 001

The auto-save functionality is not working when I edit the fields of a category. Similar issue exists for questions as well - when I edit a question, no autosave. Troubleshoot and fix
%%ENDPROMPT

%%PROMPT P-022 "Stop Technical Design backup on every change"
`Currently Technical Design editor makes a backup file on every change of `.rdd/config/technical-design-schema.json`. Remove this functionality and keep only the button for manual backup
%%ENDPROMPT
