# RDD Framework Data Model

## Configuration Files

### Change Configuration File

#### Description:

The change configuration file tracks the current active change (enhancement or fix) being worked on in the workspace. This file uses a naming convention that embeds the change type and branch name directly in the filename.

#### File Naming Convention:

- **Pattern**: `.rdd.[type].[branch-name]`
- **Type**: Either `fix` or `enh`
- **Branch Name**: The full git branch name (e.g., `20251103-1257-prompt-08-bug-workspace-unclean`)
- **Examples**:
  - `.rdd.fix.20251103-1257-prompt-08-bug-workspace-unclean`
  - `.rdd.enh.20251102-1515-add-user-authentication`

#### Location:

- Path: `.rdd-docs/workspace/.rdd.[type].[branch-name]`
- Created during: Change/fix initialization
- Removed during: Workspace archiving and cleanup

#### Attributes:

- **changeName**: 
  - Description: Human-readable name of the change (kebab-case, max 5 words)
  - Mandatory: Yes
  - Data Type: String
  - Format: kebab-case (lowercase with hyphens)
  - Example: `prompt-08-bug-workspace-unclean`

- **changeId**: 
  - Description: Unique identifier combining timestamp and change name
  - Mandatory: Yes
  - Data Type: String
  - Format: `YYYYMMDD-HHmm-[change-name]`
  - Example: `20251103-1257-prompt-08-bug-workspace-unclean`

- **branchName**: 
  - Description: Full git branch name including type prefix
  - Mandatory: Yes
  - Data Type: String
  - Format: `[fix|enh]/[changeId]`
  - Example: `fix/20251103-1257-prompt-08-bug-workspace-unclean`

- **changeType**: 
  - Description: Type of change being made
  - Mandatory: Yes
  - Data Type: String
  - Format: Enum ["fix", "enh"]
  - Example: `fix`

- **startedAt**: 
  - Description: ISO 8601 timestamp when the change was initiated
  - Mandatory: Yes
  - Data Type: String (ISO 8601 DateTime)
  - Format: `YYYY-MM-DDTHH:MM:SSZ`
  - Example: `2025-11-03T12:57:00Z`

- **phase**: 
  - Description: Current phase of the change workflow
  - Mandatory: No
  - Data Type: String
  - Example: `clarification`, `implementation`, `testing`

- **status**: 
  - Description: Current status of the change
  - Mandatory: No
  - Data Type: String
  - Example: `in-progress`, `ready-for-review`

#### File Format:

JSON format for machine and human readability

#### Example File Content:

```json
{
  "changeName": "prompt-08-bug-workspace-unclean",
  "changeId": "20251103-1257-prompt-08-bug-workspace-unclean",
  "branchName": "fix/20251103-1257-prompt-08-bug-workspace-unclean",
  "changeType": "fix",
  "startedAt": "2025-11-03T12:57:00Z",
  "phase": "implementation",
  "status": "in-progress"
}
```

### Archive Metadata File

#### Description:

The archive metadata file documents when and by whom a workspace was archived, along with the last commit information at the time of archiving.

#### File Name:

- Fixed name: `.archive-metadata`

#### Location:

- Path: `.rdd-docs/archive/[sanitized-branch-name]/.archive-metadata`
- Created during: Workspace archiving

#### Attributes:

- **archivedAt**: 
  - Description: ISO 8601 timestamp when the workspace was archived
  - Mandatory: Yes
  - Data Type: String (ISO 8601 DateTime)
  - Format: `YYYY-MM-DDTHH:MM:SSZ`
  - Example: `2025-11-03T13:45:22Z`

- **branch**: 
  - Description: Original git branch name that was archived
  - Mandatory: Yes
  - Data Type: String
  - Example: `fix/20251103-1257-prompt-08-bug-workspace-unclean`

- **archivedBy**: 
  - Description: Git user who performed the archiving
  - Mandatory: Yes
  - Data Type: String
  - Format: `Name <email>`
  - Example: `John Doe <john.doe@example.com>`

- **lastCommit**: 
  - Description: SHA hash of the last commit before archiving
  - Mandatory: Yes
  - Data Type: String (Git SHA)
  - Example: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0`

- **lastCommitMessage**: 
  - Description: Commit message of the last commit before archiving
  - Mandatory: Yes
  - Data Type: String
  - Example: `fix: resolved workspace clearing issue`

#### File Format:

JSON format for machine and human readability

#### Example File Content:

```json
{
  "archivedAt": "2025-11-03T13:45:22Z",
  "branch": "fix/20251103-1257-prompt-08-bug-workspace-unclean",
  "archivedBy": "John Doe <john.doe@example.com>",
  "lastCommit": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
  "lastCommitMessage": "fix: resolved workspace clearing issue"
}
```

## Workspace Files

### Stand-Alone Prompts File

#### Description:

Tracks stand-alone prompts that need to be executed during fix/enhancement work. Used to manage a checklist of tasks.

#### File Name:

- Fixed name: `.rdd.copilot-prompts.md`

#### Location:

- Path: `.rdd-docs/workspace/.rdd.copilot-prompts.md`
- Created during: Workspace initialization (copied from template)

#### Format:

Markdown with checkbox list structure

### Execution Log File

#### Description:

JSON Lines format log of prompt executions with timestamps and details.

#### File Name:

- Fixed name: `log.jsonl`

#### Location:

- Path: `.rdd-docs/workspace/log.jsonl`

#### Format:

JSONL (JSON Lines) - one JSON object per line

#### Example Entry:

```json
{"timestamp":"2025-11-03T11:14:46Z","promptId":"P01","executionDetails":"Modified RDD scripts...","sessionId":"exec-20251103-1314"}
```

## Validation Rules

- **Config File Existence**: Only one `.rdd.[fix|enh].*` file should exist in workspace at a time
- **Branch Name Match**: The branch name in the config file must match the current git branch
- **Change Type Consistency**: The type in the filename must match the changeType field in the JSON content
- **Workspace Clearing**: All files must be removed from workspace directory during cleanup, not just specific files

## Physical Implementation

### Workspace Directory

- **Location**: `.rdd-docs/workspace/`
- **Purpose**: Active development workspace for current change/fix
- **Lifecycle**: Created during change initialization, cleared after archiving
- **Contents**: Dynamic based on workflow phase

### Archive Directory

- **Location**: `.rdd-docs/archive/[sanitized-branch-name]/`
- **Purpose**: Historical record of completed changes
- **Naming**: Branch name with slashes replaced by hyphens (e.g., `fix-20251103-1257-bug-name`)
- **Contents**: Complete snapshot of workspace at archiving time

### Config File Discovery

Scripts use the `find_change_config()` (Bash) or `Find-ChangeConfig` (PowerShell) helper function to locate the active config file:
- Searches for files matching `.rdd.fix.*` or `.rdd.enh.*` pattern
- Returns the first matching file found
- Used throughout the RDD framework for change tracking

## Platform-Specific Implementations

### Script Locations

- **Linux/macOS**: `src/linux/.rdd/scripts/*.sh` (Bash)
- **Windows**: `src/windows/.rdd/scripts/*.ps1` (PowerShell)
- **Legacy**: `.rdd/scripts/*.sh` (this repo scripts)

### Script Files

Both platforms include identical functionality across these scripts:

1. **rdd.{sh|ps1}** - Main entry point with domain routing
2. **core-utils.{sh|ps1}** - Common utility functions
3. **git-utils.{sh|ps1}** - Git operations
4. **branch-utils.{sh|ps1}** - Branch management
5. **workspace-utils.{sh|ps1}** - Workspace operations
6. **requirements-utils.{sh|ps1}** - Requirements handling
7. **change-utils.{sh|ps1}** - Change workflow
8. **clarify-utils.{sh|ps1}** - Clarification phase
9. **prompt-utils.{sh|ps1}** - Prompt management

