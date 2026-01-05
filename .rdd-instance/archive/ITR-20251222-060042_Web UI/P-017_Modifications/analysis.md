# Design Proposal for Post-Implementation Modifications Feature

## Overview

This document presents a design for supporting small corrections after implementation completion without requiring a new prompt. This feature is intended for cases where users spot minor adjustments needed after the main implementation is done.

## Selected Design (Based on Questionnaire Responses)

Based on the questionnaire answers, the following design approach is recommended:

### 1. Data Model & Storage

**Registry Changes (work-iteration-registry.json):**
- Add `current-modification-id` field to each prompt entry (null when not in modification mode)
- Add `modifications-count` field to track total number of modifications created
- Keep existing fields: `implementation-completed`, `execution-mode`

**File Structure:**
- Create individual markdown files: `modification-001.md`, `modification-002.md`, etc. in the prompt folder
- Create `modifications-log.json` in the prompt folder as an index/history file (metadata only)
- Create `modification-<ID>-implementation.md` for tracking implementation details of each modification

Example registry entry:
```json
{
    "prompt-id": "P-017",
    "prompt-title": "Modifications",
    "state": "active",
    "implementation-completed": true,
    "execution-mode": "modification",
    "current-modification-id": "001",
    "modifications-count": 3,
    ...
}
```

### 2. Execution Modes

**New Execution Mode:** `"modification"`
- Only available when `implementation-completed` is `true`
- Replaces `"no-action"` when a modification is active
- Returns to `"no-action"` after modification completion
- Reuses implementation execution logic but operates on modification files

**Mode Transition Flow:**
```
implementation-completed=true + execution-mode="no-action"
    ↓ [user creates modification]
current-modification-id="001" + execution-mode="modification"
    ↓ [implementation of modification]
modification completed
    ↓ [reset]
current-modification-id=null + execution-mode="no-action"
```

### 3. File Naming and Structure

**In each prompt folder (e.g., P-017_Modifications/):**

```
P-017_Modifications/
├── prompt.md                           # Original prompt
├── plan.md                             # Original plan (if exists)
├── implementation.md                    # Original implementation log
├── modifications-log.json               # Index of all modifications (metadata only)
├── modification-001.md                  # First modification description
├── modification-001-implementation.md   # First modification implementation log
├── modification-002.md                  # Second modification description
├── modification-002-implementation.md   # Second modification implementation log
└── ...
```

**modifications-log.json format:**
```json
{
    "prompt-id": "P-017",
    "modifications": [
        {
            "modification-id": "001",
            "created": "2026-01-01T10:30:00",
            "status": "completed",
            "completed": "2026-01-01T10:35:00"
        },
        {
            "modification-id": "002",
            "created": "2026-01-01T14:20:00",
            "status": "in-progress",
            "completed": null
        }
    ]
}
```

Note: The modification description text is stored in the individual `modification-<ID>.md` files, not in the JSON metadata file.

### 4. Workflow Simplification

**No Questionnaire/Planning for Modifications:**
- Modifications are meant for "small corrections"
- Skip `questionnaire.md` and `plan.md` generation
- Go directly to implementation with `modification-<ID>-implementation.md`
- Simpler, faster workflow

**If complex changes are needed:**
- User should create a new prompt instead of a modification

### 5. CLI and Web UI Integration

**CLI Actions:**

New action scripts to create:
- `.rdd/src/actions/modification_create.py` - Creates a new modification
  - Parameters: `description="Fix something"`
  - Creates `modification-<ID>.md` file with the description text
  - Updates registry: sets `current-modification-id`, increments `modifications-count`
  - Adds entry to `modifications-log.json` with metadata (id, created timestamp, status)

- `.rdd/src/actions/modification_list.py` - Lists all modifications for active prompt
  - Reads `modifications-log.json`
  - Displays modification history with metadata

- `.rdd/src/actions/modification_set_execution_mode.py` - Sets execution mode to "modification"
  - Can only be called when `implementation-completed=true`
  - Sets `execution-mode="modification"`

- `.rdd/src/actions/modification_complete.py` - Marks modification as complete
  - Updates `modifications-log.json` with completion timestamp and status
  - Resets `current-modification-id` to null
  - Sets `execution-mode="no-action"`

**Web UI Changes:**

Extend `.rdd/web-ui/index.html`:
- Add "Add Modification" button in prompt editor page
  - Only visible when `implementation-completed` is `true`
  - Shows a modal/form to enter modification description
  - Calls `modification_create.py` script

- Add "Modifications History" section
  - Shows list of all modifications from `modifications-log.json`
  - Each modification shows status, timestamps
  - Click on modification to view full description from `modification-<ID>.md`

- Extend execution mode selector
  - Add "Modification" option
  - Only enabled when `current-modification-id` is not null

### 6. Execution Snippet Changes

**Update `.rdd/prompt-snippets/execution.md`:**

Add new definition:
```markdown
- [CURRENT-MODIFICATION-ID] is the value of `current-modification-id` field in [WI-REGISTRY] for the active prompt

- [MODIFICATION-FILE] is the file `modification-<[CURRENT-MODIFICATION-ID]>.md` in [ACTIVE-PROMPT-FOLDER]

- [MODIFICATION-IMPLEMENTATION] is the file `modification-<[CURRENT-MODIFICATION-ID]>-implementation.md` in [ACTIVE-PROMPT-FOLDER]

- [MODIFICATIONS-LOG] is the file `modifications-log.json` in [ACTIVE-PROMPT-FOLDER]
```

Extend execution mode check in step 5:
```markdown
* If `execution-mode` is `"modification"`:
  * Write in the chat "Modification mode"
  * Follow the instructions in `.rdd/prompt-snippets/execution-step.modification.md`
  * After modification execution is completed:
    - Execute `.rdd/src/actions/modification_complete.py`
  * Stop (do not continue with the next instructions here)
```

**Create new file `.rdd/prompt-snippets/execution-step.modification.md`:**
```markdown
## Execution Step Instructions for Modification Mode

1. Read [CURRENT-MODIFICATION-ID] from [WI-REGISTRY]

2. Read the modification description from [MODIFICATION-FILE]

3. Execute the modification instructions. Log all implementation details to [MODIFICATION-IMPLEMENTATION]

4. Update `.rdd-instance/specifications/requirements.md` if needed to reflect changes

5. Update [MODIFICATIONS-LOG] to mark the modification as completed with timestamp

## Rules

- Modifications are meant for small corrections
- If the change is complex, recommend creating a new prompt instead
- Follow the same requirements update conventions as regular implementation
- Be concise but thorough in logging to [MODIFICATION-IMPLEMENTATION]
```

### 7. Requirements Changes

**Update `.rdd-instance/specifications/requirements.md`:**

Add new requirements (examples):
```markdown
| REQ-MOD-001 | System shall support creation of modifications for prompts with implementation-completed=true |
| REQ-MOD-002 | Each modification shall be stored in a separate markdown file modification-<ID>.md |
| REQ-MOD-003 | System shall maintain a modifications-log.json index file with metadata in each prompt folder |
| REQ-MOD-004 | Modifications shall skip questionnaire and planning steps |
| REQ-MOD-005 | Only one modification can be active (in execution mode) at a time |
| REQ-MOD-006 | Web UI shall display "Add Modification" button only when implementation-completed=true |
| REQ-MOD-007 | CLI shall provide commands for modification creation, listing, and completion |
| REQ-MOD-008 | Execution mode "modification" shall only be available when current-modification-id is not null |
```

### 8. Implementation Steps Summary

**Phase 1: Core Infrastructure**
1. Update work-iteration-registry.json schema with new fields
2. Create modification_create.py script
3. Create modification_list.py script
4. Create modification_complete.py script
5. Create modification_set_execution_mode.py script

**Phase 2: Execution Framework**
6. Update execution.md with modification definitions
7. Create execution-step.modification.md
8. Update prompt_set_execution_mode.py to support "modification" mode

**Phase 3: UI Integration**
9. Update Web UI index.html with "Add Modification" button
10. Add modifications history display
11. Extend execution mode selector

**Phase 4: Documentation & Testing**
12. Update requirements.md with modification-related requirements
13. Test complete workflow: create → execute → complete
14. Update README.md if needed with modification usage instructions

## Benefits of This Design

1. **Lightweight:** Modifications don't require full questionnaire/planning workflow
2. **Traceable:** All modifications are logged in modifications-log.json with metadata
3. **Isolated:** Each modification has its own files, easy to review
4. **Integrated:** Reuses existing execution mode infrastructure
5. **Clear State:** One modification active at a time, simple state management
6. **User-Friendly:** Simple CLI commands and Web UI integration
7. **Scalable:** Can handle many modifications without cluttering the registry

## Alternative Designs Not Selected

### Option 1: Array-Based Tracking (Q1 Option A)
- Store all modifications in a `modifications` array in the registry
- **Rejected because:** Would make registry file larger and more complex

### Option 2: All in implementation.md (Q3 Option B)
- Append all modifications to the main implementation.md file
- **Rejected because:** File would become too large, harder to isolate changes

### Option 3: Full Workflow for Modifications (Q4 Option A)
- Each modification gets questionnaire and plan files
- **Rejected because:** Too heavy for "small corrections", defeats the purpose

### Option 4: Separate Corrections Dashboard (Q5 Option D)
- Add corrections section to prompt list page
- **Rejected because:** Adds complexity, modifications should be part of prompt flow

### Option 5: Boolean Flag Instead of Mode (Q2 Option B)
- Use `modification-mode` boolean instead of execution-mode value
- **Rejected because:** Less consistent with existing execution-mode pattern

## Risk Mitigation

**Risk 1: Modification Scope Creep**
- *Mitigation:* Document clearly that modifications are for "small corrections"
- *Mitigation:* In execution-step.modification.md, add logic to detect complex changes and recommend creating a new prompt

**Risk 2: Lost Modification State**
- *Mitigation:* modifications-log.json serves as permanent metadata history
- *Mitigation:* All modification files (both .md and implementation files) are preserved even after completion

**Risk 3: File System Clutter**
- *Mitigation:* Files are well-named with consistent pattern
- *Mitigation:* All in the same prompt folder, easy to manage

**Risk 4: Confusion Between Modes**
- *Mitigation:* Clear documentation in execution snippets
- *Mitigation:* Web UI clearly shows current mode and available transitions

## Next Steps

1. Get user approval on this design
2. Begin implementation in phases as outlined above
3. Test each phase before moving to the next
4. Update all relevant documentation

---

**Document Status:** Draft for Review  
**Created:** 2026-01-01  
**Author:** GitHub Copilot (based on questionnaire responses)
