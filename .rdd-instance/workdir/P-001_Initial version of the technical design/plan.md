# Implementation Plan for Technical Design System

## Overview

This plan outlines the step-by-step implementation of a complete Technical Design system for the RDD framework, including a new schema format, Web UI page, Python action scripts, migration capability, and comprehensive documentation.

Based on questionnaire answers:
- Schema structure: Hierarchical nested model (sections > groups > questions)
- Conditional visibility: Simple rule objects with questionId and expected value(s)
- Web UI stack: Match existing Web UI technology stack
- UI-Python communication: Match existing Web UI to Python communication pattern
- Migration trigger: On Web UI startup
- Answers storage: Object/map keyed by questionId
- Completion indicator: No completion percentage indicator

## Step 1: Repository and Web UI Pattern Discovery

**Goal**: Understand the existing codebase structure to ensure consistency.

**Actions**:
- Locate and examine the existing Web UI directory structure
- Identify the technology stack used (check for package.json, framework imports, etc.)
- Review how existing "specifications" pages (Requirements, Files & Folders) are implemented
- Examine how the Web UI currently calls Python action scripts (especially requirement management scripts)
- Document the communication pattern (REST API, subprocess calls, or other)
- Identify reusable components, utilities, and styling patterns
- Review the `.rdd/config/manifest.json` to understand action registration if applicable

**Deliverables**:
- Clear understanding of Web UI architecture documented in implementation.md
- List of reusable patterns and components
- Communication protocol identified

## Step 2: Read and Analyze Legacy Schema

**Goal**: Extract all categories, groups, questions, and logic from the legacy schema.

**Actions**:
- Read `.rdd-instance/workdir/P-001_Initial version of the technical design/TechnicalDesignSchema.json`
- Extract all 33 sections with their complete structure
- Document all question types, options, conditional visibility rules (visibleWhen)
- Map the existing structure to the new hierarchical nested model
- Identify any patterns or conventions used in the legacy schema
- Create a mapping document showing old → new schema transformation

**Deliverables**:
- Complete inventory of legacy schema content in implementation.md
- Mapping strategy for migration

## Step 3: Design New Schema Format

**Goal**: Create the new schema format at `.rdd/config/technical-design-schema.json`.

**Actions**:
- Design hierarchical JSON structure: categories[] → groups[] → questions[]
- Define question types: radio, multiselect, dropdown, free-text, numeric, links, file-references, tags, plus explicit unknown/N/A
- Implement conditional visibility using simple rule objects: `{"questionId": "Q-xyz", "equals": "value"}` with support for AND/OR combinators
- Include metadata: category id/label/description, group id/label/description, question id/label/help/type/options
- Ensure stable question IDs across all sections for reliable reference
- Add support for pros/cons per option (carry over from legacy if present)
- Include example N/A and Unknown options where appropriate
- Do NOT add schema versioning per prompt requirements
- Migrate all 33 sections from legacy schema:
  - ProjectScale, ProductType, Criticality, ExpectedLifetime, EnterpriseConstraints
  - CloudStrategy, Compute, Frontend, Backend, Mobile
  - DataAnalytics, AI_ML, Security_IAM, Networking, CICD_DevOps
  - Observability, Compliance_Governance, DisasterRecovery, OperationalModel, DevelopmentProcess
  - ExpandedSecurity, ExpandedData, DataVisualization, DeepDisasterRecovery, IntegrationArchitecture
  - PerformanceScalability, NonFunctionalRequirements, EnvironmentStrategy, DeploymentStrategy
  - DataLifecycleRetention, SupportHoursSLAs, MonitoringMetrics, Logging
- Preserve all questions, options, conditional logic, and help text from legacy schema

**Deliverables**:
- `.rdd/config/technical-design-schema.json` created with full schema definition

## Step 4: Design Storage Format for Answers

**Goal**: Define the structure of `.rdd-instance/specifications/technical-design.json`.

**Actions**:
- Design object/map structure keyed by questionId for O(1) lookup
- Define answer object fields:
  - questionId (string)
  - type (string: matches question type from schema)
  - value (varies: string for radio/dropdown/free-text, array for multiselect, number for numeric, etc.)
  - answeredAt (ISO 8601 timestamp)
  - rationale (optional string for user notes)
- Ensure upsert semantics: new answer overwrites previous for same questionId
- Keep format Git-friendly with readable diffs
- Example structure:
  ```json
  {
    "Q-ProjectScale-001": {
      "questionId": "Q-ProjectScale-001",
      "type": "radio",
      "value": "enterprise",
      "answeredAt": "2026-01-17T12:30:00Z",
      "rationale": "Expected user base > 100k"
    },
    "Q-Frontend-002": {
      "questionId": "Q-Frontend-002",
      "type": "multiselect",
      "value": ["react", "typescript"],
      "answeredAt": "2026-01-17T12:35:00Z"
    }
  }
  ```

**Deliverables**:
- Storage format specification documented in implementation.md
- Will be implemented in convention doc (Step 6)

## Step 5: Implement Python Action Scripts

**Goal**: Create Python scripts for safe manipulation of technical-design.json.

**Actions**:
- Create `.rdd/src/actions/technical_design_read.py`:
  - Read and return current technical design answers
  - Handle missing/empty file gracefully
  - Return structured data (JSON output to stdout)
- Create `.rdd/src/actions/technical_design_answer_set.py`:
  - Accept parameters: questionId, type, value, rationale (optional)
  - Validate questionId exists in schema
  - Validate value matches question type
  - Load current answers
  - Upsert the answer (add or update)
  - Write atomically (temp file + rename)
  - Add timestamp
  - Return success/error message
- Create `.rdd/src/actions/technical_design_answer_remove.py`:
  - Accept parameter: questionId
  - Load current answers
  - Remove the specified answer if exists
  - Write atomically
  - Return success/error message
- Create `.rdd/src/actions/technical_design_validate.py`:
  - Validate technical-design.json against schema
  - Check all questionIds reference valid schema questions
  - Check all answer values match question types
  - Check all required fields present
  - Return validation results
- Create `.rdd/src/actions/technical_design_migrate.py`:
  - Detect if technical-design.json is in legacy format
  - If legacy or other old format: transform to new storage format
  - Preserve all existing answers during migration
  - Backup old file before migration
  - Write new format atomically
  - Log migration details
  - Return migration status
- Optional but useful: Create `.rdd/src/actions/technical_design_clear_category.py` and `technical_design_clear_group.py`
- Follow patterns from existing requirement scripts (requirement_ur_create.py, etc.)
- Use atomic writes (write to temp + os.replace) to prevent corruption
- Provide clear error messages with recovery guidance per UR-0027
- Validate prerequisites before executing per UR-0029
- Handle errors gracefully per UR-0030

**Deliverables**:
- All Python action scripts created under `.rdd/src/actions/`
- Scripts callable from command line with clear parameter syntax

## Step 6: Create Convention Documentation

**Goal**: Document the Technical Design system comprehensively.

**Actions**:
- Update `.rdd/conventions/technical-design.convention.md` (currently says empty):
  - Purpose: structured technical architecture decisions, optional but binding when present
  - Invariants: only answered questions stored, Python scripts enforce safety
  - Schema structure explanation: hierarchical categories → groups → questions
  - Supported question types with examples
  - Conditional visibility rules and evaluation logic
  - Storage format specification (answers keyed by questionId)
  - Python scripts reference and usage examples:
    ```bash
    python .rdd/src/actions/technical_design_answer_set.py questionId="Q-Frontend-001" type="radio" value="react"
    python .rdd/src/actions/technical_design_answer_remove.py questionId="Q-Frontend-001"
    python .rdd/src/actions/technical_design_validate.py
    python .rdd/src/actions/technical_design_migrate.py
    ```
  - RDD execution integration: how clarify/analyze/plan/implement modes consume technical design
  - Optional nature: Technical Design absence does not block other workflows
  - Follow formatting conventions from other `.rdd/conventions/*.md` files
  - Include examples of schema snippets and stored answers
- Document migration strategy and detection logic
- Explain atomic write pattern for safety

**Deliverables**:
- `.rdd/conventions/technical-design.convention.md` fully updated

## Step 7: Implement Web UI Technical Design Page - Backend Integration

**Goal**: Integrate Python scripts with Web UI backend.

**Actions**:
- Examine existing Web UI backend code (likely Python-based server)
- Create backend endpoints or handlers that:
  - Call `technical_design_read.py` to load schema and current answers
  - Call `technical_design_answer_set.py` when user saves an answer
  - Call `technical_design_answer_remove.py` when user clears an answer
  - Call `technical_design_validate.py` for validation feedback
  - Call `technical_design_migrate.py` on startup to ensure format compatibility
- Match the existing pattern used for requirements management (per questionnaire Q4 answer)
- Ensure error handling and user-friendly error messages per UR-0027, UR-0035
- Return JSON responses with success/error status and color-coded message types (UR-0031)

**Deliverables**:
- Backend endpoints/handlers for Technical Design operations
- Migration check integrated into Web UI startup

## Step 8: Implement Web UI Technical Design Page - Frontend

**Goal**: Create the Technical Design page UI matching existing Web UI patterns.

**Actions**:
- Use the existing Web UI technology stack identified in Step 1
- Create Technical Design page with:
  - **Left sidebar navigation (A)**:
    - List all categories from schema
    - Highlight active category
    - Click to navigate to category
  - **Main content area (B)**:
    - Within selected category, render groups as collapsible accordions
    - Each accordion shows group label/description
    - Within each group, render questions with appropriate input widgets:
      - Radio buttons for single-choice questions
      - Checkboxes for multiselect questions
      - Dropdown for dropdown type
      - Text input for free-text
      - Number input for numeric
      - Special inputs for links, file references, tags as needed
    - Include "Unknown" and "N/A" options where appropriate
    - Display help/description text per question
    - Show pros/cons for options if present in schema
  - **Search functionality**:
    - Search box at top
    - Search across question labels, options, help text
    - Highlight matches
    - Show search results across all categories
  - **Filter functionality**:
    - Filter by category (dropdown)
    - Filter by answered/unanswered status
    - Filter by question type
    - Apply filters dynamically
  - **UX features**:
    - Expand/collapse all accordions per category button
    - Fast partial completion (save answers immediately on change per UR-0062)
    - Clear visual indicators for answered vs unanswered questions
    - Jump-to next unanswered button (optional but recommended per prompt)
  - **No completion percentage** per prompt requirement (UR-0025 conflicts removed)
  - **Conditional visibility**:
    - Evaluate visibleWhen rules dynamically based on current answers
    - Hide/show questions as dependencies change
    - Re-evaluate on every answer change
- Reuse existing Web UI components, styling, and layout patterns
- Follow responsive design for desktop usage per UR-0035
- Implement color-coded feedback per UR-0031 (green=success, red=error, yellow=warning, blue=info)
- Real-time feedback on save operations
- Graceful error handling with informative messages
- Load current answers on page load and populate form

**Deliverables**:
- Technical Design page fully functional in Web UI
- Navigation, search, filter, expand/collapse all working
- Conditional visibility implemented and tested
- Integration with backend endpoints complete

## Step 9: Implement Automatic Migration on Startup

**Goal**: Ensure legacy technical-design.json files are migrated automatically.

**Actions**:
- In Web UI startup sequence (per questionnaire Q5: "On Web UI startup"):
  - Call `technical_design_migrate.py` during initialization
  - Migration script checks if `.rdd-instance/specifications/technical-design.json` exists and format
  - If legacy format detected: perform migration and log result
  - If new format: skip migration
  - If file doesn't exist: create empty object `{}`
  - If migration fails: log error but don't block Web UI startup (Technical Design is optional)
- Display migration status in console/logs
- Optionally show migration notification in UI if migration occurred

**Deliverables**:
- Migration integrated into Web UI startup
- Migration runs automatically and safely
- Errors logged but don't block startup

## Step 10: Integrate Technical Design into RDD Execution Flow

**Goal**: Ensure clarify/analyze/plan/implement modes consume Technical Design when present.

**Actions**:
- Review `.rdd/prompt-snippets/execution.md` step 4 which already reads [TECHNICAL-DESIGN]
- Ensure execution flow reads `.rdd-instance/specifications/technical-design.json` at start (already specified)
- Treat Technical Design as optional but binding:
  - If present: agent must respect recorded decisions
  - If absent: no blocking, proceed normally
- In clarify mode (`.rdd/prompt-snippets/execution-step.clarify.md`):
  - Questions should avoid asking what's already decided in Technical Design
  - Respect technology stack, platform, security constraints from Technical Design
- In analyze mode (`.rdd/prompt-snippets/execution-step.analyze.md`):
  - Analysis should align with technical decisions
  - Recommended architectures consistent with Technical Design
- In plan mode (`.rdd/prompt-snippets/execution-step.plan.md`):
  - Plan steps must comply with Technical Design choices
- In implement mode (`.rdd/prompt-snippets/execution-step.implementation.md`):
  - Implementation must follow Technical Design specifications
  - Technology choices, architecture patterns must match recorded decisions
- Update execution step snippets if needed to explicitly reference Technical Design compliance
- Document integration in implementation.md

**Deliverables**:
- RDD execution flow properly integrates Technical Design
- Optional nature preserved (no hard dependencies)
- Binding compliance when Technical Design exists

## Step 11: Update User Guide Documentation

**Goal**: Provide user-facing documentation for the Technical Design feature.

**Actions**:
- Locate `.rdd/docs/user-guide.md`
- Find the "### Technical Design" section (prompt states it has "WIP string")
- Replace WIP content with comprehensive documentation:
  - Overview: what Technical Design is and why it's useful
  - How to access the Technical Design page in Web UI
  - How to navigate categories and groups
  - How to answer questions (different input types)
  - How to search and filter
  - How to use expand/collapse all
  - How conditional visibility works
  - How to clear/remove answers
  - How to use Python scripts directly (CLI reference)
  - Migration: automatic on startup, what happens with legacy files
  - Integration with RDD execution: how decisions affect clarify/analyze/plan/implement
  - Optional nature: can leave questions unanswered or skip entirely
- Include screenshots or examples if appropriate
- Follow formatting conventions from rest of user guide

**Deliverables**:
- `.rdd/docs/user-guide.md` updated with complete Technical Design section

## Step 12: Add Tests and Validation

**Goal**: Ensure the Technical Design system is robust and correct.

**Actions**:
- Add unit tests for Python action scripts:
  - Test `technical_design_read.py` with missing file, empty file, valid file
  - Test `technical_design_answer_set.py` with valid/invalid questionIds, various value types
  - Test `technical_design_answer_remove.py` with existing/non-existing answers
  - Test `technical_design_validate.py` with valid/invalid technical-design.json
  - Test `technical_design_migrate.py` with legacy format, new format, edge cases
  - Test atomic write behavior (no corruption on errors)
- Add integration tests:
  - Test Web UI page loads correctly
  - Test answer save/remove via UI
  - Test search functionality
  - Test filter functionality
  - Test conditional visibility updates
  - Test migration on startup
- Add test for schema validation:
  - Schema file is valid JSON
  - All questionIds are unique
  - visibleWhen references point to valid questionIds
- Add "dry run" mode to migration script per prompt suggestion
- Follow test patterns from `tests/` directory structure
- Tests should run on both Windows and Linux per UR-0006

**Deliverables**:
- Unit tests created under `tests/` directory
- Integration tests for Web UI and end-to-end flows
- All tests passing

## Step 13: Requirements Updates

**Goal**: Ensure all requirements are met and update requirements file if needed.

**Actions**:
- Review all requirements in `.rdd-instance/specifications/requirements.md`
- Verify compliance with:
  - UR-0004: Web UI for Technical Design ✓
  - UR-0007: Visualization and modification via Web UI ✓
  - UR-0010: Scripts for modifications (Python actions) ✓
  - UR-0018: Technical Specification page with config-driven form ✓
  - UR-0022: Display and controlled edits ✓
  - UR-0024: Conditional and hierarchical logic ✓
  - UR-0025: Technical Specification page editing ✓ (note: "Set Default Answers" function NOT in current prompt, document in implementation.md)
  - UR-0027: Specific error messages with remediation ✓
  - UR-0028: Backups before destructive operations (migration backup) ✓
  - UR-0029: Validate prerequisites ✓
  - UR-0030: Graceful error handling ✓
  - UR-0031: Color-coded feedback ✓
  - UR-0035: Desktop-optimized Web UI ✓
- Consider if any new requirements should be added:
  - Potentially: "The framework shall provide a Technical Design schema defining architectural questions in categories and groups with conditional visibility support"
  - Potentially: "The framework shall store only explicitly answered Technical Design questions in .rdd-instance/specifications/technical-design.json"
  - Potentially: "The framework shall automatically migrate legacy Technical Design formats to current format on Web UI startup"
- If new requirements needed, describe in plan and use requirement scripts in implementation:
  ```bash
  python .rdd/src/actions/requirement_tr_create.py text="The framework shall..."
  ```
- Note: UR-0025 mentions "Set Default Answers" function which is NOT in the current prompt acceptance criteria. Document this discrepancy in implementation.md. Will NOT implement "Set Default Answers" as it contradicts prompt's "only answered items" principle.

**Deliverables**:
- Requirements review documented in implementation.md
- New requirements described if needed (to be created during implementation step)

## Step 14: Final Validation and Documentation

**Goal**: Ensure complete implementation and proper documentation.

**Actions**:
- Verify all acceptance criteria from prompt:
  - ✓ User can open Technical Design page
  - ✓ Browse categories/groups
  - ✓ Search and filter
  - ✓ Answer any subset of questions
  - ✓ Answers persisted and reloaded
  - ✓ technical-design.json contains ONLY answered questions
  - ✓ UI never writes JSON directly, only via Python actions
  - ✓ Conditional visibility works dynamically
  - ✓ Legacy formats migrated automatically without data loss
  - ✓ RDD flows remain optional but comply with Technical Design when present
- Complete implementation.md with:
  - Rationale for hierarchical schema (best for UX + maintainability)
  - How conditional visibility is represented (simple rule objects) and evaluated (on answer change)
  - How migration detection works (check file structure, compare to expected format)
  - How scripts ensure safe writes (atomic temp + rename) and validation (schema checks)
- Run all tests
- Verify on both Windows and Linux if possible
- Test migration with actual legacy TechnicalDesignSchema.json from prompt folder
- Test Web UI end-to-end with real user workflow

**Deliverables**:
- All acceptance criteria met
- implementation.md complete with required rationale
- System validated and tested
- Ready for execution

## Requirements Conformance

This plan ensures compliance with all relevant requirements:

- **UR-0004**: Web UI provided for Technical Design management
- **UR-0007**: Visualization and controlled modification via Web UI
- **UR-0010**: Python scripts for modifications, not copilot logic
- **UR-0018**: Technical Specification page with config-driven form
- **UR-0022**: Display and controlled edits of specifications
- **UR-0024**: Conditional and hierarchical logic support
- **UR-0025**: Technical Specification page for editing (Note: "Set Default Answers" NOT implemented per prompt)
- **UR-0027**: Error messages with remediation steps
- **UR-0028**: Backups before destructive operations
- **UR-0029**: Prerequisites validation
- **UR-0030**: Graceful error handling
- **UR-0031**: Color-coded feedback
- **UR-0035**: Desktop-optimized Web UI

## Specifications Updates

During implementation (NOT in plan mode), the following updates will be made:

**To `.rdd-instance/specifications/requirements.md`**:
- Potentially add new technical requirements for Technical Design schema, storage format, and migration
- Scripts to use: `requirement_tr_create.py`
- All changes via requirement scripts only

**To `.rdd-instance/specifications/technical-design.json`**:
- Will be populated with answered questions as users interact with Web UI
- Format: object keyed by questionId with answer objects
- All changes via Python action scripts only

**To `.rdd-instance/specifications/files-and-folders.md`**:
- Add documentation for new files:
  - `.rdd/config/technical-design-schema.json`
  - `.rdd/conventions/technical-design.convention.md`
  - `.rdd/src/actions/technical_design_*.py` scripts
  - Web UI Technical Design page files
- Update during implementation phase

## Summary

This plan delivers a complete Technical Design system with:
- New hierarchical schema with 33 sections migrated from legacy
- Simple conditional visibility with rule objects
- Web UI page matching existing patterns with sidebar + accordion navigation
- Search, filter, expand/collapse functionality
- Python action scripts for safe manipulation
- Automatic migration on startup
- Comprehensive documentation
- Integration with RDD execution flow
- Optional but binding architecture
- Tests and validation

The implementation will be done in the next execution mode: "implement".
