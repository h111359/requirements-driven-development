# P06 Implementation

## Prompt Text

Do the following change as checking the functionality of all scripts and prompts to reflect it:
1. The file `.rdd/templates/copilot-prompts.md` should be renamed to `.rdd/templates/work-iteration-prompts.md` (run a terminal command for that). 
2. Change the expected location of `.rdd-docs/workplace/work-iteration-prompts.md` to `.rdd-docs/work-iteration-prompts.md`. 
3. Change the logic in the scripts in `.rdd/scripts` so the file to be seeded from `.rdd/templates/work-iteration-prompts.md`. During execution of "3. Complete current iteration" step when running `.rdd/scripts/rdd.py`, make functionality `.rdd-docs/work-iteration-prompts.md` to be copied in the folder `.rdd-docs/workspace` + overwritten from `.rdd/templates/work-iteration-prompts.md` so to be reset to its initial state.

## Context from Requirements

### Relevant Requirements:
- **[FR-05] Workspace Initialization**: A script shall initialize workspace with: work-iteration-prompts.md
- **[FR-82] Iteration Workspace Initialization**: The create iteration workflow shall initialize workspace with only copilot-prompts.md template, keeping workspace minimal

### Relevant Tech Spec Sections:

**Workspace Files**:
- **Stand-alone prompts**: `work-iteration-prompts.md` - Checklist of executable prompts

**Project Folder Structure**:
```
├── .rdd/                         # RDD framework internals
│   ├── templates/                # File templates for initialization
│   │   ├── copilot-prompts.md    # Stand-alone prompts template
```

## Analysis

The prompt asks for three changes:

1. **Rename template file**: `.rdd/templates/copilot-prompts.md` → `.rdd/templates/work-iteration-prompts.md`
2. **Change expected location**: From `.rdd-docs/workplace/work-iteration-prompts.md` (typo in original) to `.rdd-docs/work-iteration-prompts.md`
3. **Update logic in scripts**: 
   - Seed from the renamed template
   - During "Complete current iteration", copy `.rdd-docs/work-iteration-prompts.md` to `.rdd-docs/workspace/` and reset it from template

### Current Understanding

Looking at the requirements and tech spec, there's a naming inconsistency:
- Requirements mention "copilot-prompts.md" 
- But the actual file is referenced as "work-iteration-prompts.md" in workspace

The prompt aims to:
- Standardize on "work-iteration-prompts.md" naming
- Move the file from `.rdd-docs/workspace/work-iteration-prompts.md` to `.rdd-docs/work-iteration-prompts.md` (one level up)
- During iteration completion, backup current prompts to workspace and reset the main file

### Files to Check and Modify

1. `.rdd/templates/copilot-prompts.md` - needs to be renamed
2. `.rdd/scripts/rdd.py` - needs logic updates for:
   - create_iteration() - seed from new template location
   - complete_iteration() - copy to workspace and reset from template
3. `.github/prompts/rdd.execute.prompt.md` - may reference the old path
4. Other scripts or prompts that reference the old naming

## Implementation Plan

1. **Check if template file exists** and rename it
2. **Search for all references** to "copilot-prompts.md" and ".rdd-docs/workspace/work-iteration-prompts.md"
3. **Update rdd.py script**:
   - In `create_iteration()`: Seed `.rdd-docs/work-iteration-prompts.md` from `.rdd/templates/work-iteration-prompts.md`
   - In `complete_iteration()`: Copy `.rdd-docs/work-iteration-prompts.md` to `.rdd-docs/workspace/`, then reset from template
4. **Update all references** in prompts and documentation
5. **Test the changes** by reviewing the logic

## Implementation Steps

### Step 1: Rename the template file

Command executed:
```bash
mv .rdd/templates/copilot-prompts.md .rdd/templates/work-iteration-prompts.md
```

### Step 2: Update rdd.py script

Current implementation:
- Line 789: `copy_template("copilot-prompts.md", os.path.join(WORKSPACE_DIR, "work-iteration-prompts.md"))`
- Line 1169: `template_path = os.path.join(TEMPLATES_DIR, "copilot-prompts.md")`

Changes needed:
1. Update both references to use "work-iteration-prompts.md"
2. Change logic to seed `.rdd-docs/work-iteration-prompts.md` instead of `.rdd-docs/workspace/work-iteration-prompts.md`
3. Add logic in complete_iteration() to backup and reset prompts file

### Step 3: Update references in other files

Files with references found:
- `.github/prompts/rdd.execute.prompt.md` - references `.rdd-docs/workspace/work-iteration-prompts.md` (needs update to `.rdd-docs/work-iteration-prompts.md`)
- `.github/prompts/rdd.update.prompt.md` - references `.rdd-docs/workspace/work-iteration-prompts.md`
- `README.md` - references `.rdd-docs/workspace/work-iteration-prompts.md`
- `.rdd/scripts/scripts-catalogue.md` - documentation references
- `.rdd-docs/tech-spec.md` - technical documentation references
- `.rdd-docs/requirements.md` - requirements references

### Step 4: Test changes

## Summary of Changes Made

### Files Modified:

1. **Template file renamed**:
   - Renamed `.rdd/templates/copilot-prompts.md` → `.rdd/templates/work-iteration-prompts.md`

2. **.rdd/scripts/rdd.py**:
   - Line 789: Updated reference from `copilot-prompts.md` to `work-iteration-prompts.md`
   - Line 1170: Updated to seed `.rdd-docs/work-iteration-prompts.md` (not in workspace subfolder)
   - Added logic in `complete_iteration()` to backup and reset work-iteration-prompts.md

3. **.rdd/scripts/rdd_utils.py**:
   - Updated `mark_prompt_completed()` function to use `.rdd-docs/work-iteration-prompts.md`
   - Updated `list_prompts()` function to use `.rdd-docs/work-iteration-prompts.md`
   - Updated `validate_prompt_status()` function to use `.rdd-docs/work-iteration-prompts.md`
   - Updated comment references from "copilot-prompts.md" to "work-iteration-prompts.md"

4. **.github/prompts/rdd.execute.prompt.md**:
   - Updated all references from `.rdd-docs/workspace/work-iteration-prompts.md` to `.rdd-docs/work-iteration-prompts.md`
   - Updated in Context section, Instructions section, and Example Workflows

5. **.github/prompts/rdd.update.prompt.md**:
   - Updated reference from `.rdd-docs/workspace/work-iteration-prompts.md` to `.rdd-docs/work-iteration-prompts.md`

6. **README.md**:
   - Updated all references from `.rdd-docs/workspace/work-iteration-prompts.md` to `.rdd-docs/work-iteration-prompts.md`

7. **.rdd/scripts/scripts-catalogue.md**:
   - Updated documentation references

8. **tests/test-spec.md**:
   - Updated test documentation reference

9. **.rdd-docs/tech-spec.md**:
   - Updated template name reference
   - Updated folder structure documentation

10. **.rdd-docs/requirements.md**:
    - Updated FR-82 to reflect new location
    - Added FR-100 for backup and reset functionality

## New Behavior:

### During "Create new iteration":
- Template file `.rdd/templates/work-iteration-prompts.md` is copied to `.rdd-docs/work-iteration-prompts.md` (not in workspace subfolder)

### During "Complete current iteration":
1. Backs up `.rdd-docs/work-iteration-prompts.md` to `.rdd-docs/workspace/work-iteration-prompts.md`
2. Resets `.rdd-docs/work-iteration-prompts.md` from the template
3. Continues with archiving and other completion steps

This ensures:
- The prompts file is at the top level of .rdd-docs (not in workspace)
- Current prompts are preserved in the archive
- The main prompts file is reset for the next iteration

## Verification

1. ✅ Template file renamed successfully (confirmed via `git status`)
2. ✅ All script references updated
3. ✅ All prompt file references updated
4. ✅ All documentation references updated
5. ✅ Requirements updated with new FR-100
6. ✅ Tech spec folder structure updated
7. ✅ Prompt P06 marked as completed successfully

## Commands Executed

```bash
# Rename template file
mv .rdd/templates/copilot-prompts.md .rdd/templates/work-iteration-prompts.md

# Generate files list
python .rdd-docs/workspace/list-files.py

# Mark prompt as completed
python .rdd/scripts/rdd.py prompt mark-completed P06
```

## Result

All changes have been successfully implemented. The work-iteration-prompts.md file is now:
- Located at `.rdd-docs/work-iteration-prompts.md` (top level)
- Seeded from `.rdd/templates/work-iteration-prompts.md` during iteration creation
- Backed up to `.rdd-docs/workspace/` and reset during iteration completion
- Referenced correctly throughout all scripts, prompts, and documentation
