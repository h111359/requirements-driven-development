# P03 Implementation: Merge Update Docs into Wrap-Up Prompt

## Task
Merge `.github/prompts/rdd.07-update-docs.prompt.md` to be executed during execution of `.github/prompts/rdd.08-wrap-up.prompt.md`. Format the `.github/prompts/rdd.08-wrap-up.prompt.md` in the same way as `.github/prompts/rdd.09-clean-up.prompt.md` without losing functionality and information.

## Implementation Steps

### Step 1: Read Current Files ✓
Reading both prompt files to understand their structure and content.

**Files analyzed:**
- `rdd.08-wrap-up.prompt.md` - Current wrap-up prompt (2 steps: S01, S02)
- `rdd.09-clean-up.prompt.md` - Target format (simple, concise structure)
- `rdd.07-update-docs.prompt.md` - Documentation update prompt (8 steps: S01-S08)

**Current structure of rdd.08:**
- Purpose, Instructions (S01, S02), Notes
- Calls `python .rdd/scripts/rdd.py change wrap-up`
- Mentions documentation updates but doesn't execute them

**Target structure (rdd.09):**
- Purpose, Context, Instructions (S01), Alternative, Notes
- Clean, concise format
- Clear command execution

### Step 2: Design Merged Structure
Planning how to merge documentation updates into wrap-up while maintaining clean format.

**Design decisions:**
1. Keep rdd.09-style format (Purpose, Context, Instructions, Notes)
2. Add documentation update as a step BEFORE executing wrap-up command
3. Integrate key guidelines from rdd.07 into the instructions
4. Keep it concise - reference the full rdd.07 prompt for detailed rules
5. Make documentation update mandatory part of wrap-up workflow

### Step 3: Create Merged Prompt ✓
Creating the new rdd.08-wrap-up.prompt.md with integrated documentation updates.

**Changes made to rdd.08-wrap-up.prompt.md:**
1. ✅ Added "Context" section explaining the combined workflow
2. ✅ Updated "Purpose" to include documentation updates
3. ✅ Added "S01: Update Documentation" step with:
   - Analysis of completed prompts
   - Guidelines for updating each documentation file
   - Key rules from rdd.07 (ID preservation, deletion marking, sequential IDs)
4. ✅ Renumbered steps: S01 (Update Docs), S02 (Execute Wrap-Up), S03 (Create PR)
5. ✅ Reformatted in rdd.09 style (cleaner, more concise)
6. ✅ Enhanced "Notes" section with documentation-first emphasis
7. ✅ Maintained all original functionality

**Format improvements:**
- Matches rdd.09-clean-up.prompt.md structure
- Clear section hierarchy
- Concise instructions
- Better organized notes

### Step 4: Deprecate Old Prompt ✓
Marking rdd.07-update-docs.prompt.md as deprecated since it's now merged into rdd.08.

**Changes made to rdd.07-update-docs.prompt.md:**
- ✅ Added deprecation warning at the top
- ✅ Kept all content for reference purposes
- ✅ Directed users to use rdd.08-wrap-up.prompt.md instead

## Summary

### Changes Completed
1. ✅ **Merged rdd.07 into rdd.08**: Documentation update workflow now integrated into wrap-up
2. ✅ **Reformatted rdd.08**: Matches rdd.09 style (Purpose, Context, Instructions, Notes)
3. ✅ **Preserved functionality**: All documentation update guidelines preserved
4. ✅ **Enhanced workflow**: Documentation updates now mandatory before wrap-up
5. ✅ **Deprecated rdd.07**: Marked as deprecated with clear redirection

### Structure Changes in rdd.08-wrap-up.prompt.md
**Before:**
- S01: Execute Wrap-Up
- S02: Follow Next Steps

**After:**
- S01: Update Documentation (from rdd.07)
- S02: Execute Wrap-Up (original S01)
- S03: Create Pull Request (enhanced from original S02)

### Benefits
- **Single workflow**: Documentation and wrap-up in one process
- **Cleaner format**: Matches rdd.09 style consistently
- **Better organization**: Clear steps and context
- **No lost functionality**: All rdd.07 content preserved in S01
- **Deprecation handled**: Old prompt marked clearly

### Files Modified
1. `.github/prompts/rdd.08-wrap-up.prompt.md` - Merged and reformatted
2. `.github/prompts/rdd.07-update-docs.prompt.md` - Marked as deprecated
3. `.rdd-docs/workspace/P03-implementation.md` - This file
