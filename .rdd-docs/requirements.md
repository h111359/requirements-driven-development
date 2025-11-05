# Overview

<OVERVIEW-PLACEHOLDER>

## Terminology

In the RDD framework, **"change"** is an umbrella term that encompasses two types of work:
- **Enhancement** (abbreviated as "enh"): New functionality, features, or improvements to existing functionality
- **Fix**: Bug fixes, corrections, or patches to resolve issues

When we refer to a "change", we mean either an enhancement or a fix. This terminology is used consistently across the framework in branch names, workflows, and documentation.

# General Functionalities

- **[GF-03] Requirements Clarification Workflow**: The RDD framework shall provide a structured workflow for clarifying requirements through iterative questioning based on a clarity taxonomy
- **[GF-04] Workspace Management**: The framework shall maintain a workspace directory (.rdd-docs/workspace/) for active development work on enhancements and fixes
- **[GF-05] Change Tracking**: The framework shall track the current active change (enhancement or fix) being worked on
- **[GF-06] Requirements Merging**: The framework shall support merging clarified requirements from workspace into the main requirements.md file
- **[GF-07] Workspace Archiving**: The framework shall archive completed workspace content for historical reference
- **[GF-08] Fix Branch Workflow**: The framework shall provide a guided workflow for creating and documenting fix branches, including naming, description, and initialization.
- **[GF-09] Fix Branch Wrap-Up**: The framework shall provide a workflow for wrapping up fix branches, archiving documentation, and preparing for merge review.
- **[GF-10] Requirements Change Detection**: The framework shall provide a workflow for detecting and documenting requirements changes by comparing code with the main branch.
- **[GF-11] Post-Merge Branch Cleanup**: The framework shall provide a workflow for cleaning up local and remote branches after PR merge, ensuring workspace synchronization with main.
# Functional Requirements

- **[FR-03] Flat Workspace Structure**: The system shall store all active workspace files directly in .rdd-docs/workspace/ without enhancement-specific subfolders
- **[FR-04] Current Change Detection**: The system shall use a configuration file named .rdd.[fix|enh].<branch-name> in workspace to mark visually the current working branch
- **[FR-05] Workspace Initialization**: A script shall initialize workspace with: .rdd.copilot-prompts.md
- **[FR-06] Clean Main Branch Workspace**: When on main branch, workspace shall be empty or contain only standard template content to clearly indicate no active development
- **[FR-07] Clarity Checklist Usage**: The clarification prompt shall use .rdd-docs/workspace/clarity-checklist.md as a checklist to identify unclear requirements
- **[FR-08] Structured Questioning**: The prompt shall ask questions with predefined answer options (A, B, C, D) while allowing custom "Other" responses
- **[FR-09] Question Formatting Standards**: All prompts shall follow guidelines from .rdd/templates/questions-formatting.md for user-friendly questioning
- **[FR-10] Open Questions Tracking**: The system shall maintain open-questions.md with status markers: [ ] open, [?] partial, [x] answered
- **[FR-11] [DELETED]
- **[FR-12] [DELETED]
- **[FR-13] [DELETED]
- **[FR-14] [DELETED]
- **[FR-15] Script Parameter Execution**: Scripts shall accept parameters for predictable execution from prompts without user interaction
- **[FR-16] Auto-Approval Configuration**: The .vscode/settings.json shall configure auto-approval for .rdd/scripts/ execution
- **[FR-17] Multiple Execution Support**: The clarification prompt shall support re-execution, building on previous work without data loss
- **[FR-18] Workspace Backup**: The system shall create timestamped backups in .rdd-docs/workspace/.backups/ before destructive operations
- **[FR-19] Backup Restoration**: The system shall support restoring workspace from latest backup
- **[FR-20] Re-execution Detection**: The prompt shall detect previous sessions by checking existing content in workspace files
- **[FR-21] Requirements Validation**: The system shall validate requirements-changes.md format before merging, checking for proper [ADDED|MODIFIED|DELETED] prefixes
- **[FR-22] Automatic ID Assignment for ADDED**: The system shall automatically assign IDs to [ADDED] requirements during wrap-up by finding the highest existing ID per section (GF/FR/NFR/TR) and incrementing from there
- **[FR-23] No IDs in Workspace for ADDED**: The workspace requirements-changes.md shall NOT include IDs for [ADDED] requirements - IDs are assigned only during wrap-up to prevent conflicts with parallel development
- **[FR-24] Required IDs for MODIFIED**: The workspace requirements-changes.md shall REQUIRE existing IDs from requirements.md for [MODIFIED] requirements in format: [MODIFIED] [EXISTING-ID] Title: Description
- **[FR-25] Required IDs for DELETED**: The workspace requirements-changes.md shall REQUIRE existing IDs from requirements.md for [DELETED] requirements in format: [DELETED] [EXISTING-ID] Title: Reason
- **[FR-26] ID Mapping Documentation**: The wrap-up process shall create .id-mapping.txt documenting the mapping from workspace placeholders to final assigned IDs
- **[FR-27] Merge Preview**: The system shall provide preview of changes (counts and content) before merging
- **[FR-28] Backup Before Merge**: The system shall create timestamped backup of requirements.md before merging changes
- **[FR-29] Auto-Commit Before Sync**: The wrap-up process shall automatically commit all uncommitted changes before syncing with main branch to prevent merge errors
- **[FR-30] Smart Commit Message**: The auto-commit message shall include the change type and name from .current-change file in format: "[change-type]: [change-name] - pre-wrap-up commit"
- **[FR-31] Main Branch Sync Before Wrap-Up**: The wrap-up process shall fetch and merge the latest state from main branch into the current enhancement branch before merging requirements
- **[FR-32] Conflict Detection on Sync**: The system shall detect merge conflicts during pre-wrap-up sync and halt the wrap-up process if conflicts exist
- **[FR-33] User Notification on Conflicts**: The system shall notify the user if merge conflicts are detected and instruct them to resolve conflicts manually before proceeding
- **[FR-34] Sync Validation**: The system shall validate that the merge from main completed successfully before proceeding with requirements merge
- **[FR-35] Archive Directory Structure**: The system shall create .rdd-docs/archive/<change-id>/ directories for each completed change
- **[FR-36] Complete Workspace Archive**: The system shall archive all workspace files from .rdd-docs/workspace/ preserving the complete state at time of archiving
- **[FR-37] Archive Metadata**: The system shall create .archive-metadata file with archivedAt timestamp, branch name, archivedBy, lastCommit, and lastCommitMessage fields
- **[FR-38] Workspace Preservation**: The system shall preserve workspace content during archiving (copy, not move) until explicitly cleared
- **[FR-39] Branch-Workspace Alignment**: The system shall align workspace content with the current git branch
- **[FR-40] Main Branch Fetch**: The wrap-up process shall fetch the latest changes from origin/main before synchronization
- **[FR-41] Latest Requirements Maintenance**: The .rdd-docs/requirements.md shall always reflect the latest committed state from main branch after wrap-up synchronization
- **[FR-42] Complete Workspace Clearing**: The system shall remove all files and subdirectories from .rdd-docs/workspace/ when clearing workspace after archiving, ensuring no files remain from previous work
- **[FR-43] Config File Naming Convention**: The system shall name workspace config files using the pattern .rdd.[type].[branch-name] where type is either 'fix' or 'enh' and branch-name matches the git branch name
- **[FR-44] [DELETED]
- **[FR-45] No change.md in Workspace**: The workspace initialization shall NOT create a change.md file, as this template has been removed from the framework
- **[FR-46] Post-Merge Cleanup Workflow**: The framework shall provide a guided cleanup prompt (rdd.09-clean-up.prompt.md) for removing local and remote branches after PR merge, automating the cleanup command execution
- **[FR-47] Python-Based Script Implementation**: All RDD operations shall be implemented in Python (rdd.py) with domain-based command routing, replacing legacy bash scripts which are archived

# Non-Functional Requirements

- **[NFR-03] Developer Experience**: The framework shall provide smooth developer experience, minimizing technical overhead for requirement clarification
- **[NFR-04] Visual Clarity**: Scripts shall use color-coded output (info: blue, success: green, warning: yellow, error: red) for clarity
- **[NFR-05] Progress Indication**: Multi-step processes shall display progress indicators (e.g., "Step 2/3", "Clarification [1/N]")
- **[NFR-06] Clear Error Messages**: Error messages shall include specific problem description and suggested remediation steps
- **[NFR-07] DELETED
- **[NFR-08] Separate Concerns**: Questions tracking (open-questions.md) and requirements changes (requirements-changes.md) shall be in separate files
- **[NFR-09] Template-Based Files**: New files shall be generated from templates in .rdd/templates/ for consistency
- **[NFR-10] Version Documentation**: All prompts shall include version number and last updated date
- **[NFR-11] Data Preservation**: Re-execution of prompts shall preserve existing data unless explicitly reset by user
- **[NFR-12] Backup Safety**: All destructive operations shall create backups before proceeding
- **[NFR-13] Validation Before Action**: Scripts shall validate prerequisites before executing operations
- **[NFR-14] Graceful Failure**: Scripts shall handle errors gracefully and provide recovery guidance
- **[NFR-15] Multi-Developer Support**: The framework shall support multiple developers working on different features simultaneously
- **[NFR-16] Conflict Prevention**: The workspace structure shall minimize merge conflicts between developers
- **[NFR-17] DELETED
- **[NFR-18] Fix Documentation Template**: The framework shall provide a template for documenting fixes, including What, Why, and Acceptance Criteria sections, to ensure consistency and traceability.
# Technical Requirements

- **[TR-03] JSON Configuration**: The .current-change file shall use JSON format for machine and human readability
- **[TR-04] DELETED
- **[TR-05] DELETED
- **[TR-06] Python Scripts**: All automation scripts shall be implemented in Python for cross-platform compatibility (legacy bash scripts archived)
- **[TR-07] Exit on Error**: Scripts shall use proper error handling to exit immediately on command failure
- **[TR-08] JQ Dependency**: Legacy bash scripts used jq for JSON parsing; Python implementation uses native json module
- **[TR-09] Executable Permissions**: All script files shall have executable permissions (chmod +x)
- **[TR-10] Templates Location**: All file templates shall be stored in .rdd/templates/
- **[TR-11] Scripts Location**: All automation scripts shall be stored in .rdd/scripts/
- **[TR-12] Prompts Location**: All prompt files shall be stored in .github/prompts/
- **[TR-13] Workspace Location**: Active workspace shall be at .rdd-docs/workspace/
- **[TR-14] Archive Location**: Completed workspaces shall be archived in .rdd-docs/archive/<change-id>/
- **[TR-15] Prompt Recommendations**: VS Code settings shall configure chat.promptFilesRecommendations for RDD prompts
- **[TR-16] Terminal Auto-Approve**: VS Code settings shall configure chat.tools.terminal.autoApprove for .rdd/scripts/
- **[TR-17] JSONL File Association**: VS Code settings shall associate *.jsonl files with jsonlines language
- **[TR-18] Editor Rulers**: VS Code settings shall configure editor rulers at 80 and 120 characters
- **[TR-19] Step-Based Structure**: Prompts shall use numbered steps (S01, S02, etc.) for clear execution flow
- **[TR-20] Script Integration**: Prompts shall call scripts for actions rather than implementing logic directly
- **[TR-21] Context Section**: Prompts shall include comprehensive context section describing workspace structure and available tools
- **[TR-22] Rules Section**: Prompts shall define clear rules for behavior and constraints
- **[TR-23] Error Handling Section**: Prompts shall include specific error handling guidance with examples
- **[TR-24] Fix Branch Management Script**: The framework shall provide a Bash script to automate fix branch creation, documentation, validation, wrap-up, and cleanup.
- **[TR-25] Requirements Analysis Script**: The framework shall provide a Bash script to automate requirements analysis, file comparison, and impact detection.
- **[TR-26] Merged Branch Deletion Tool**: The framework shall provide an interactive Bash script for cleaning up merged git branches, supporting both local and remote deletion.
- **[TR-27] PowerShell Script Support**: The framework shall provide PowerShell (.ps1) equivalents of all Bash scripts for Windows compatibility, maintaining identical functionality and structure.
- **[TR-28] Cross-Platform Script Organization**: Linux/Bash scripts shall be stored in `src/linux/.rdd/scripts/` and Windows/PowerShell scripts in `src/windows/.rdd/scripts/`, with parallel folder structures for templates and prompts.
