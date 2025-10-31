# Requirements Changes

> This file documents changes to be made to the main requirements.md file.
> Each statement is prefixed with [ADDED|MODIFIED|DELETED] to indicate the type of change.
>
> **For detailed formatting guidelines, see:** `.rdd/templates/requirements-format.md`

## Format Guidelines

- **[ADDED]**: New requirement not present in current requirements.md
  - **Format**: `[ADDED] [Title]: Description` (NO ID - will be auto-assigned during wrap-up)
  - **Example**: `[ADDED] User Authentication: System shall require OAuth2 login`
  
- **[MODIFIED]**: Change to an existing requirement from requirements.md
  - **Format**: `[MODIFIED] [EXISTING-ID] [Title]: New description`
  - **Example**: `[MODIFIED] [FR-05] Data Export: Change from CSV-only to CSV, JSON, and XML formats`
  - **Rule**: MUST include the existing requirement ID from requirements.md
  
- **[DELETED]**: Requirement to be removed from requirements.md
  - **Format**: `[DELETED] [EXISTING-ID] [Title]: Reason for deletion`
  - **Example**: `[DELETED] [FR-12] Legacy API Support: No longer needed after v2.0 migration`
  - **Rule**: MUST include the existing requirement ID from requirements.md

**Important**: IDs for [ADDED] requirements are auto-assigned during wrap-up based on the highest existing ID in requirements.md, preventing conflicts with parallel development.

---

## General Functionalities

- **[ADDED] Requirements Clarification Workflow**: The RDD framework shall provide a structured workflow for clarifying requirements through iterative questioning based on a clarity taxonomy
- **[ADDED] Workspace Management**: The framework shall maintain a workspace directory (.rdd-docs/workspace/) for active development work on features and fixes
- **[ADDED] Change Tracking**: The framework shall track the current active change/feature/fix being worked on
- **[ADDED] Requirements Merging**: The framework shall support merging clarified requirements from workspace into the main requirements.md file
- **[ADDED] Workspace Archiving**: The framework shall archive completed workspace content for historical reference

---

## Functional Requirements

### Workspace Structure & Organization

- **[ADDED] Flat Workspace Structure**: The system shall store all active workspace files directly in .rdd-docs/workspace/ without feature-specific subfolders
- **[ADDED] Current Change Detection**: The system shall use a .current-change JSON configuration file in workspace to track the active change with fields: changeName, changeId, branchName, changeType, startedAt, phase, status
- **[ADDED] Workspace Initialization**: The create-change.sh script shall initialize workspace with: change.md, clarity-taxonomy.md, open-questions.md, requirements-changes.md, clarification-log.jsonl, and .current-change
- **[ADDED] Clean Main Branch Workspace**: When on main branch, workspace shall be empty or contain only standard template content to clearly indicate no active development

### Clarification Process

- **[ADDED] Clarity Taxonomy Usage**: The clarification prompt shall use .rdd-docs/workspace/clarity-taxonomy.md as a checklist to identify unclear requirements
- **[ADDED] Structured Questioning**: The prompt shall ask questions with predefined answer options (A, B, C, D) while allowing custom "Other" responses
- **[ADDED] Question Formatting Standards**: All prompts shall follow guidelines from .rdd/templates/questions-formatting.md for user-friendly questioning
- **[ADDED] Open Questions Tracking**: The system shall maintain open-questions.md with status markers: [ ] open, [?] partial, [x] answered
- **[ADDED] Clarification Logging**: The system shall log all Q&A interactions in clarification-log.jsonl with timestamp, question, answer, answeredBy, and sessionId
- **[ADDED] Requirements Changes Documentation**: The system shall document requirement changes in requirements-changes.md with [ADDED|MODIFIED|DELETED] prefixes

### Script Automation

- **[ADDED] Clarification Script Actions**: The clarify-changes.sh script shall support actions: init, log-clarification, copy-taxonomy, backup, restore, get-current, clear, validate
- **[ADDED] Wrap-Up Script Actions**: The wrap-up.sh script shall support actions: merge-requirements, archive-workspace, full-wrap-up, validate-merge, preview-merge, get-change-id, sync-main
- **[ADDED] Script Parameter Execution**: Scripts shall accept parameters for predictable execution from prompts without user interaction
- **[ADDED] Auto-Approval Configuration**: The .vscode/settings.json shall configure auto-approval for .rdd/scripts/ execution

### Re-execution & Backup

- **[ADDED] Multiple Execution Support**: The clarification prompt shall support re-execution, building on previous work without data loss
- **[ADDED] Workspace Backup**: The system shall create timestamped backups in .rdd-docs/workspace/.backups/ before destructive operations
- **[ADDED] Backup Restoration**: The system shall support restoring workspace from latest backup
- **[ADDED] Re-execution Detection**: The prompt shall detect previous sessions by checking existing content in workspace files

### Requirements Merging & ID Management

- **[ADDED] Requirements Validation**: The system shall validate requirements-changes.md format before merging, checking for proper [ADDED|MODIFIED|DELETED] prefixes
- **[ADDED] Automatic ID Assignment for ADDED**: The system shall automatically assign IDs to [ADDED] requirements during wrap-up by finding the highest existing ID per section (GF/FR/NFR/TR) and incrementing from there
- **[ADDED] No IDs in Workspace for ADDED**: The workspace requirements-changes.md shall NOT include IDs for [ADDED] requirements - IDs are assigned only during wrap-up to prevent conflicts with parallel development
- **[ADDED] Required IDs for MODIFIED**: The workspace requirements-changes.md shall REQUIRE existing IDs from requirements.md for [MODIFIED] requirements in format: [MODIFIED] [EXISTING-ID] Title: Description
- **[ADDED] Required IDs for DELETED**: The workspace requirements-changes.md shall REQUIRE existing IDs from requirements.md for [DELETED] requirements in format: [DELETED] [EXISTING-ID] Title: Reason
- **[ADDED] ID Mapping Documentation**: The wrap-up process shall create .id-mapping.txt documenting the mapping from workspace placeholders to final assigned IDs
- **[ADDED] Merge Preview**: The system shall provide preview of changes (counts and content) before merging
- **[ADDED] Backup Before Merge**: The system shall create timestamped backup of requirements.md before merging changes

### Pre-Wrap-Up Synchronization

- **[ADDED] Auto-Commit Before Sync**: The wrap-up process shall automatically commit all uncommitted changes before syncing with main branch to prevent merge errors
- **[ADDED] Smart Commit Message**: The auto-commit message shall include the change type and name from .current-change file in format: "[change-type]: [change-name] - pre-wrap-up commit"
- **[ADDED] Main Branch Sync Before Wrap-Up**: The wrap-up process shall fetch and merge the latest state from main branch into the current feature branch before merging requirements
- **[ADDED] Conflict Detection on Sync**: The system shall detect merge conflicts during pre-wrap-up sync and halt the wrap-up process if conflicts exist
- **[ADDED] User Notification on Conflicts**: The system shall notify the user if merge conflicts are detected and instruct them to resolve conflicts manually before proceeding
- **[ADDED] Sync Validation**: The system shall validate that the merge from main completed successfully before proceeding with requirements merge

### Workspace Archiving

- **[ADDED] Archive Directory Structure**: The system shall create .rdd-docs/archive/<change-id>/ directories for each completed change
- **[ADDED] Complete Workspace Archive**: The system shall archive all workspace files: change.md, open-questions.md, requirements-changes.md, clarification-log.jsonl, clarity-taxonomy.md, .id-mapping.txt
- **[ADDED] Archive Metadata**: The system shall create .archive-info file with archivedAt timestamp, changeId, and archivedBy fields
- **[ADDED] Workspace Preservation**: The system shall preserve workspace content during archiving (copy, not move) until explicitly cleared

### Git Integration

- **[ADDED] Branch-Workspace Alignment**: The system shall align workspace content with the current git branch
- **[ADDED] Main Branch Fetch**: The wrap-up process shall fetch the latest changes from origin/main before synchronization
- **[ADDED] Latest Requirements Maintenance**: The .rdd-docs/requirements.md shall always reflect the latest committed state from main branch after wrap-up synchronization

---

## Non-Functional Requirements

### Usability

- **[ADDED] Developer Experience**: The framework shall provide smooth developer experience, minimizing technical overhead for requirement clarification
- **[ADDED] Visual Clarity**: Scripts shall use color-coded output (info: blue, success: green, warning: yellow, error: red) for clarity
- **[ADDED] Progress Indication**: Multi-step processes shall display progress indicators (e.g., "Step 2/3", "Clarification [1/N]")
- **[ADDED] Clear Error Messages**: Error messages shall include specific problem description and suggested remediation steps

### Maintainability

- **[ADDED] Immutable Change File**: The original change.md file shall never be modified by prompts or scripts
- **[ADDED] Separate Concerns**: Questions tracking (open-questions.md) and requirements changes (requirements-changes.md) shall be in separate files
- **[ADDED] Template-Based Files**: New files shall be generated from templates in .rdd/templates/ for consistency
- **[ADDED] Version Documentation**: All prompts shall include version number and last updated date

### Reliability

- **[ADDED] Data Preservation**: Re-execution of prompts shall preserve existing data unless explicitly reset by user
- **[ADDED] Backup Safety**: All destructive operations shall create backups before proceeding
- **[ADDED] Validation Before Action**: Scripts shall validate prerequisites before executing operations
- **[ADDED] Graceful Failure**: Scripts shall handle errors gracefully and provide recovery guidance

### Collaboration

- **[ADDED] Multi-Developer Support**: The framework shall support multiple developers working on different features simultaneously
- **[ADDED] Conflict Prevention**: The workspace structure shall minimize merge conflicts between developers
- **[ADDED] Audit Trail**: The clarification-log.jsonl shall provide complete audit trail of decision-making

---

## Technical Requirements

### File Formats

- **[ADDED] JSON Configuration**: The .current-change file shall use JSON format for machine and human readability
- **[ADDED] JSONL Logging**: The clarification-log.jsonl shall use JSON Lines format (one JSON object per line) for append-only logging
- **[ADDED] Markdown Documentation**: All documentation files (change.md, open-questions.md, requirements-changes.md) shall use Markdown format

### Script Implementation

- **[ADDED] Bash Scripts**: All automation scripts shall be implemented in Bash for cross-platform Linux/Mac compatibility
- **[ADDED] Exit on Error**: Scripts shall use `set -e` to exit immediately on command failure
- **[ADDED] JQ Dependency**: Scripts may use jq for JSON parsing with fallback to basic text processing if unavailable
- **[ADDED] Executable Permissions**: All script files shall have executable permissions (chmod +x)

### Directory Structure

- **[ADDED] Templates Location**: All file templates shall be stored in .rdd/templates/
- **[ADDED] Scripts Location**: All automation scripts shall be stored in .rdd/scripts/
- **[ADDED] Prompts Location**: All prompt files shall be stored in .github/prompts/
- **[ADDED] Workspace Location**: Active workspace shall be at .rdd-docs/workspace/
- **[ADDED] Archive Location**: Completed workspaces shall be archived in .rdd-docs/archive/<change-id>/

### VS Code Integration

- **[ADDED] Prompt Recommendations**: VS Code settings shall configure chat.promptFilesRecommendations for RDD prompts
- **[ADDED] Terminal Auto-Approve**: VS Code settings shall configure chat.tools.terminal.autoApprove for .rdd/scripts/
- **[ADDED] JSONL File Association**: VS Code settings shall associate *.jsonl files with jsonlines language
- **[ADDED] Editor Rulers**: VS Code settings shall configure editor rulers at 80 and 120 characters

### Prompt Design

- **[ADDED] Step-Based Structure**: Prompts shall use numbered steps (S01, S02, etc.) for clear execution flow
- **[ADDED] Script Integration**: Prompts shall call scripts for actions rather than implementing logic directly
- **[ADDED] Context Section**: Prompts shall include comprehensive context section describing workspace structure and available tools
- **[ADDED] Rules Section**: Prompts shall define clear rules for behavior and constraints
- **[ADDED] Error Handling Section**: Prompts shall include specific error handling guidance with examples

