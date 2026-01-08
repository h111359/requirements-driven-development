**Context**: Currently, the RDD framework allows AI agents and execution steps to directly edit `.rdd-instance/specifications/requirements.md`. This creates risks of format inconsistencies, ID conflicts, and accidental data corruption. The framework already uses deterministic Python scripts for other operations (prompts, modifications, questionnaires), but requirement management lacks this safety layer.

**Goal**: Enforce script-based requirement modifications by creating dedicated Python scripts and updating execution instructions to prohibit direct file editing.

**Requirements**:

1. **Create requirement management scripts** in `.rdd/src/actions/` following the existing framework patterns (see `prompt_create.py` as reference):

   - `requirement_ur_create.py` - Create new User Requirement
   - `requirement_ur_modify.py` - Modify existing User Requirement
   - `requirement_ur_delete.py` - Mark User Requirement as deleted (replace with [DELETED])
   - `requirement_tr_create.py` - Create new Technical Requirement
   - `requirement_tr_modify.py` - Modify existing Technical Requirement
   - `requirement_tr_delete.py` - Mark Technical Requirement as deleted (replace with [DELETED])

2. **Script behavior**:
   - **ID generation**: Automatically generate IDs  unless `id=` parameter is provided. 
   - **Validation**: Perform basic validation (non-empty, 10-2048 chars, contains "shall"). Use `validation=strict` for enhanced checks, `validation=none` to skip.
   - **Positioning**: Append new requirements to the end of the appropriate section (## User Requirements or ## Technical Requirements)
   - **Modification**: Replace entire requirement text when modifying
   - **Deletion**: Replace requirement text with [DELETED] marker, keeping the requirement ID line (following `.rdd/prompt-snippets/execution.md` rule and existing practice)
   - **Output**: Print "SUCCESS: <action> <requirement-id>" to stdout on success, error message to stderr on failure. Return exit code 0 for success, 1 for failure.
   - **File handling**: Use atomic writes (temp file + rename) to prevent corruption
   - **Format compliance**: Ensure all changes comply with `.rdd/conventions/requirements.convention.md`

3. **Update execution instructions**:
   - Modify `.rdd/prompt-snippets/execution.md` to add requirement script usage instructions and remove any references to direct requirements.md editing
   - Update `.rdd/prompt-snippets/execution-step.implementation.md` with examples of calling requirement scripts
   - Update any other execution snippets that mention requirements editing
   - Add prominent warning: **NEVER edit requirements.md directly - always use scripts**

4. **Parameters for each script**:
   - **Create**: `text="<requirement text>"` (required), `id="<override-id>"` (optional), `validation=strict|basic|none` (optional, default=basic)
   - **Modify**: `id="<requirement-id>"` (required), `text="<new complete text>"` (required), `validation=strict|basic|none` (optional, default=basic)
   - **Delete**: `id="<requirement-id>"` (required)

5. **Error handling**:
   - Validate ID format if user-provided
   - Check for ID conflicts/duplicates
   - Ensure target section exists in requirements.md
   - Provide clear error messages with suggested fixes
   - Fail fast before making any file modifications

**Success criteria**:
- All 6 scripts are functional and tested
- Execution snippets prohibit direct requirements.md editing
- Scripts successfully create, modify, and delete requirements while maintaining file format
- ID collision handling works correctly
- Validation catches common errors

**Related files**:
- Reference implementation: `.rdd/src/actions/prompt_create.py`
- Format convention: `.rdd/conventions/requirements.convention.md`
- Target file: `.rdd-instance/specifications/requirements.md`
- Execution orchestration: `.rdd/prompt-snippets/execution.md`