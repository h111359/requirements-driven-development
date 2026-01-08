# Implementation Plan: Requirements Scripts

## Overview

This plan implements script-based requirement management to replace direct editing of `requirements.md`. Based on questionnaire answers:
- Q1: Only accept `basic` and `none` validation (no `strict`)
- Q2: Always auto-generate IDs (no user-provided `id=` parameter)
- Q3: No duplicate text checking (simplified validation)
- Q4: Both consolidated section + inline warnings in execution instructions
- Q5: Simple temp file approach for atomic writes

## Step 1: Create requirement_ur_create.py script

Create `.rdd/src/actions/requirement_ur_create.py` to create new User Requirements.

**Implementation details:**
- Follow the pattern from `prompt_create.py` (parameter parsing, JSON handling, error messages)
- Parse parameters: `text="..."` (required), `validation=basic|none` (optional, default=basic)
- Read `requirements.md` and parse existing UR IDs using regex `\[UR-(\d{4})\]`
- Find highest existing UR ID number and increment by 1 to generate new ID
- Format new ID as `UR-XXXX` with 4-digit zero-padding
- If `validation=basic`, validate:
  - Text length 10-2048 characters
  - Text contains "shall" keyword (case-insensitive)
  - Text is not empty after stripping whitespace
- Parse file to locate `## User Requirements` section
- Create in-memory updated content with new requirement appended at end of section
- Format: `- [UR-XXXX] <text>`
- Write to temporary file in same directory
- Validate temp file was written correctly
- Use atomic rename to replace original requirements.md
- Print `SUCCESS: Created UR-XXXX` to stdout
- On error, print to stderr with problem + suggested fix, exit code 1

**Error handling examples:**
- Missing text parameter: "ERROR: 'text' parameter required. Usage: requirement_ur_create.py text='The system shall...'"
- Text too short: "ERROR: Requirement text too short (minimum 10 characters). Provided: X characters."
- Missing 'shall': "ERROR: Requirement must contain 'shall' keyword. Use validation=none to skip validation."
- Section not found: "ERROR: '## User Requirements' section not found in requirements.md. File may be corrupted."

## Step 2: Create requirement_tr_create.py script

Create `.rdd/src/actions/requirement_tr_create.py` to create new Technical Requirements.

**Implementation details:**
- Identical to Step 1 but for Technical Requirements
- Parse existing TR IDs using regex `\[TR-(\d{4})\]`
- Find highest TR ID and increment
- Locate `## Technical Requirements` section
- Append new requirement to end of TR section
- All other behavior identical to UR create script
- Print `SUCCESS: Created TR-XXXX` to stdout

## Step 3: Create requirement_ur_modify.py script

Create `.rdd/src/actions/requirement_ur_modify.py` to modify existing User Requirements.

**Implementation details:**
- Parse parameters: `id="UR-XXXX"` (required), `text="..."` (required), `validation=basic|none` (optional, default=basic)
- Validate ID format matches `UR-\d{4}`
- Read requirements.md and search for the requirement with matching ID
- Use regex to find line: `^- \[UR-XXXX\].*$` (multiline mode)
- If not found, error: "ERROR: Requirement UR-XXXX not found in requirements.md"
- If found and current text is `[DELETED]`, warn but allow: "WARNING: Modifying deleted requirement UR-XXXX"
- If `validation=basic`, validate new text (same checks as create)
- Replace entire requirement line with: `- [UR-XXXX] <new text>`
- Preserve all other content unchanged
- Write to temp file, validate, atomic rename
- Print `SUCCESS: Modified UR-XXXX` to stdout

## Step 4: Create requirement_tr_modify.py script

Create `.rdd/src/actions/requirement_tr_modify.py` to modify existing Technical Requirements.

**Implementation details:**
- Identical to Step 3 but for Technical Requirements
- Validate ID format matches `TR-\d{4}`
- Search for TR requirements
- Print `SUCCESS: Modified TR-XXXX` to stdout

## Step 5: Create requirement_ur_delete.py script

Create `.rdd/src/actions/requirement_ur_delete.py` to delete User Requirements.

**Implementation details:**
- Parse parameters: `id="UR-XXXX"` (required)
- No validation parameter needed (deletion doesn't validate text)
- Validate ID format matches `UR-\d{4}`
- Read requirements.md and find requirement with matching ID
- If not found, error: "ERROR: Requirement UR-XXXX not found in requirements.md"
- Replace requirement text with `[DELETED]` marker
- Format: `- [UR-XXXX] [DELETED]`
- Preserve the ID, only replace the text portion
- Write to temp file, validate, atomic rename
- Print `SUCCESS: Deleted UR-XXXX` to stdout

## Step 6: Create requirement_tr_delete.py script

Create `.rdd/src/actions/requirement_tr_delete.py` to delete Technical Requirements.

**Implementation details:**
- Identical to Step 5 but for Technical Requirements
- Validate ID format matches `TR-\d{4}`
- Print `SUCCESS: Deleted TR-XXXX` to stdout

## Step 7: Update execution.md with requirements management rules

Modify `.rdd/prompt-snippets/execution.md` to add requirements management rules.

**Changes:**
1. Add new section after "Definitions" and before "Instructions" titled `## Requirements Management Rules`:
   ```markdown
   ## Requirements Management Rules
   
   **CRITICAL - Requirements File Safety:**
   
   NEVER edit `.rdd-instance/specifications/requirements.md` directly. Always use the requirement management scripts to ensure format consistency and prevent data corruption.
   
   **Available Scripts:**
   
   Create new requirement:
   ```
   python .rdd/src/actions/requirement_ur_create.py text="The system shall..."
   python .rdd/src/actions/requirement_tr_create.py text="The framework shall..."
   ```
   
   Modify existing requirement:
   ```
   python .rdd/src/actions/requirement_ur_modify.py id="UR-XXXX" text="Updated text..."
   python .rdd/src/actions/requirement_tr_modify.py id="TR-XXXX" text="Updated text..."
   ```
   
   Delete requirement (marks as [DELETED]):
   ```
   python .rdd/src/actions/requirement_ur_delete.py id="UR-XXXX"
   python .rdd/src/actions/requirement_tr_delete.py id="TR-XXXX"
   ```
   
   **Validation:**
   - Default: Basic validation (10-2048 chars, contains "shall")
   - Skip validation: Add `validation=none` parameter
   
   **Examples:**
   ```
   # Create with validation
   python .rdd/src/actions/requirement_ur_create.py text="The system shall export data in CSV format"
   
   # Create without validation (for special cases)
   python .rdd/src/actions/requirement_tr_create.py text="See external document XYZ" validation=none
   ```
   ```

2. Update step 10 in "Instructions" section to add inline reminder:
   Change from:
   ```
   10. Update [REQUIREMENTS] if needed. In all cases - write in the chat and in [IMPLEMENTATION] your rationale what is changed and if no changes - why.
   ```
   
   To:
   ```
   10. Update [REQUIREMENTS] if needed using requirement scripts (NEVER edit requirements.md directly - see Requirements Management Rules above). In all cases - write in the chat and in [IMPLEMENTATION] your rationale what is changed and if no changes - why.
   ```

## Step 8: Update execution-step.implementation.md with script examples

Modify `.rdd/prompt-snippets/execution-step.implementation.md` to add examples of using requirement scripts.

**Changes:**
Add new section after the main instructions titled `## Examples: Managing Requirements During Implementation`:

```markdown
## Examples: Managing Requirements During Implementation

**IMPORTANT**: Never edit requirements.md directly. Always use requirement scripts.

**Creating new requirements:**

```bash
# Add new user requirement
python .rdd/src/actions/requirement_ur_create.py text="The system shall provide export to PDF format"

# Add new technical requirement
python .rdd/src/actions/requirement_tr_create.py text="The export module shall use the reportlab library"
```

**Modifying existing requirements:**

```bash
# Update user requirement
python .rdd/src/actions/requirement_ur_modify.py id="UR-0042" text="The system shall export data in CSV and JSON formats"

# Update technical requirement  
python .rdd/src/actions/requirement_tr_modify.py id="TR-0015" text="The framework shall use Python 3.11 or higher"
```

**Deleting requirements:**

```bash
# Mark user requirement as deleted
python .rdd/src/actions/requirement_ur_delete.py id="UR-0088"

# Mark technical requirement as deleted
python .rdd/src/actions/requirement_tr_delete.py id="TR-0052"
```

**Skipping validation (special cases only):**

```bash
# Create requirement without validation
python .rdd/src/actions/requirement_ur_create.py text="See section 5.2 of external specification" validation=none
```

**Documenting requirement changes in implementation.md:**

After running requirement scripts, document in your implementation file:
- Which requirements were added/modified/deleted
- Why the changes were made
- How they relate to the prompt objectives
```

## Step 9: Check other execution snippets for requirements editing references

Search and update any other execution snippet files that mention requirements editing:

**Files to check:**
- `.rdd/prompt-snippets/execution-step.clarify.md`
- `.rdd/prompt-snippets/execution-step.analyze.md`
- `.rdd/prompt-snippets/execution-step.plan.md`
- `.rdd/prompt-snippets/execution-step.modification.md`

**Changes needed:**
- If any file mentions editing requirements.md directly, add a note: "(use requirement scripts - see execution.md)"
- Add inline warnings where appropriate
- Ensure no conflicting instructions exist

## Step 10: Add requirement for script-based requirement management

Add new technical requirement to document this new capability.

**Action:**
Run the newly created script:
```bash
python .rdd/src/actions/requirement_tr_create.py text="The framework shall provide deterministic Python scripts for requirement management (requirement_ur_create.py, requirement_ur_modify.py, requirement_ur_delete.py, requirement_tr_create.py, requirement_tr_modify.py, requirement_tr_delete.py) that enforce format consistency, prevent ID conflicts, and provide atomic file operations with validation."
```

This will add a new TR requirement documenting the requirement management scripts capability.

## Step 11: Test all scripts with various scenarios

Test each script to ensure it works correctly:

**Test requirement_ur_create.py:**
- Valid creation with basic validation
- Creation with validation=none
- Error: missing text parameter
- Error: text too short (< 10 chars)
- Error: text too long (> 2048 chars)
- Error: missing "shall" keyword

**Test requirement_tr_create.py:**
- Same tests as UR create

**Test requirement_ur_modify.py:**
- Valid modification
- Error: ID not found
- Error: invalid ID format
- Modify deleted requirement (should warn but allow)

**Test requirement_tr_modify.py:**
- Same tests as UR modify

**Test requirement_ur_delete.py:**
- Valid deletion
- Error: ID not found
- Delete already deleted requirement (should succeed, idempotent)

**Test requirement_tr_delete.py:**
- Same tests as TR delete

**Integration tests:**
- Create → Modify → Delete sequence
- Verify requirements.md format is preserved
- Verify atomic writes (no corruption on interruption if possible)
- Verify ID sequence increments correctly
- Verify section boundaries are respected

## Step 12: Document changes in implementation.md

Create implementation.md documenting:
- All scripts created with their functionality
- All execution instruction files updated
- Testing performed and results
- Any issues encountered and resolutions
- New requirement added to requirements.md

## Requirements Specification Updates

### New Requirements to Add

**TR-XXXX** (will be auto-generated in Step 10): The framework shall provide deterministic Python scripts for requirement management (requirement_ur_create.py, requirement_ur_modify.py, requirement_ur_delete.py, requirement_tr_create.py, requirement_tr_modify.py, requirement_tr_delete.py) that enforce format consistency, prevent ID conflicts, and provide atomic file operations with validation.

### Existing Requirements Verification

Review existing requirements to ensure plan complies:

- **UR-0010**: "Prompts shall call scripts for file and folder modifications or other deterministic actions rather than the copilot implementing the logic" - ✓ Satisfied by creating requirement scripts
- **UR-0027**: "Error messages shall include specific problem description and suggested remediation steps" - ✓ Satisfied by detailed error messages in all scripts
- **UR-0028**: "All destructive operations shall create backups before proceeding" - Not applicable (requirement modifications are tracked in git, atomic writes prevent corruption)
- **UR-0029**: "Scripts shall validate prerequisites before executing operations" - ✓ Satisfied by validation checks before file modification
- **UR-0030**: "Scripts shall handle errors gracefully and provide recovery guidance" - ✓ Satisfied by error handling with suggested fixes

All relevant existing requirements will be satisfied by this implementation.

## Technical Specifications Updates

No changes needed to technical-design.json for this implementation. The requirement management scripts are operational scripts, not configuration-driven features requiring technical design entries.

## Files and Folders Updates

New files to be added to files-and-folders.md documentation:

**In `.rdd/src/actions/` directory:**
- `requirement_ur_create.py` - Script to create new User Requirements with automatic ID generation and validation
- `requirement_ur_modify.py` - Script to modify existing User Requirements
- `requirement_ur_delete.py` - Script to mark User Requirements as deleted
- `requirement_tr_create.py` - Script to create new Technical Requirements with automatic ID generation and validation
- `requirement_tr_modify.py` - Script to modify existing Technical Requirements
- `requirement_tr_delete.py` - Script to mark Technical Requirements as deleted

These will be documented in the files-and-folders specification during implementation step.
