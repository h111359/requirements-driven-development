# P07 Implementation

## Prompt Text

Create a file user-story.md in `.rdd/templates` with a standard user story definition structure for answering the questions "What is needed?", "Why is needed and for whom?", "What are the acceptance criteria?", "What other considerations should be taken into account?". Change the functionalities so this file to be copied in `.rdd-docs` when "1. Create new iteration" step is executed. The file should be seeded from .rdd/templates/user-story.md and when completing the iteration - to be copied in the workspace + rewritten from the template. During execution of "3. Complete current iteration" step when running `.rdd/scripts/rdd.py`, make functionality `.rdd-docs/user-story.md` to be copied in the folder `.rdd-docs/workspace` + overwritten from `.rdd/templates/user-story.md` so to be reset to its initial state.

## Context Analysis

### From requirements.md:
- No specific requirements about user stories currently exist
- The framework follows a pattern of template-based file management
- Templates are stored in `.rdd/templates/`
- Similar patterns exist for `work-iteration-prompts.md` (FR-100)

### From tech-spec.md:
- Templates are stored in `.rdd/templates/` directory
- The `create_iteration()` function in rdd.py initializes workspace
- The `complete_iteration()` function archives workspace and resets files
- Similar pattern: work-iteration-prompts.md is backed up to workspace and reset from template during completion

### From rdd.py:
- `create_iteration()` function: Creates new branch, initializes workspace with templates
- Currently copies `work-iteration-prompts.md` from `.rdd/templates/` to `.rdd-docs/`
- `complete_iteration()` function: Archives workspace, backs up work-iteration-prompts.md to workspace, resets from template
- Pattern to follow: Same logic for user-story.md

## Clarity Check

The instructions are clear:
1. Create a template file `.rdd/templates/user-story.md` with standard user story structure
2. During "Create new iteration" - copy template to `.rdd-docs/user-story.md`
3. During "Complete current iteration" - backup to workspace and reset from template

## Implementation Plan

1. **Create user-story.md template** ✓
   - Create `.rdd/templates/user-story.md` with standard user story structure
   - Structure should answer: What, Why/For whom, Acceptance Criteria, Other Considerations

2. **Modify create_iteration() in rdd.py** ✓
   - Add logic to copy user-story.md template to `.rdd-docs/user-story.md`
   - Follow same pattern as work-iteration-prompts.md

3. **Modify complete_iteration() in rdd.py** ✓
   - Add logic to backup `.rdd-docs/user-story.md` to workspace
   - Add logic to reset `.rdd-docs/user-story.md` from template
   - Follow same pattern as work-iteration-prompts.md

4. **Update requirements.md**
   - Add new requirement about user story file management

5. **Update tech-spec.md**
   - Add user-story.md to Project Folder Structure section
   - Document the workflow in relevant sections

## Implementation Details

### Step 1: Created user-story.md template ✓

**File:** `.rdd/templates/user-story.md`

Created a template with the following structure:
- **What is needed?** - Description of feature/functionality
- **Why is it needed and for whom?** - Problem, value, and beneficiaries
- **What are the acceptance criteria?** - Checklist of completion criteria
- **What other considerations should be taken into account?** - Technical constraints, dependencies, risks
- **Instructions** - Usage guidance

### Step 2: Modified create_iteration() ✓

**File:** `.rdd/scripts/rdd.py`
**Location:** Lines ~1056-1068 (in create_iteration function, Step 2)

Added code to copy user-story.md template:
```python
# Copy user-story.md template to .rdd-docs/
user_story_template = os.path.join(TEMPLATES_DIR, "user-story.md")
user_story_dest = ".rdd-docs/user-story.md"

if not os.path.isfile(user_story_template):
    print_warning(f"User story template not found: {user_story_template}")
else:
    shutil.copy2(user_story_template, user_story_dest)
```

### Step 3: Modified complete_iteration() ✓

**File:** `.rdd/scripts/rdd.py`
**Location:** Lines ~935-970 (in complete_iteration function, Step 0)

Added code to backup and reset user-story.md:
```python
# Backup and reset user-story.md
user_story_file = ".rdd-docs/user-story.md"
user_story_backup = os.path.join(WORKSPACE_DIR, "user-story.md")
template_user_story = os.path.join(TEMPLATES_DIR, "user-story.md")

# Copy current user story file to workspace (backup)
if os.path.isfile(user_story_file):
    shutil.copy2(user_story_file, user_story_backup)
    print_success(f"Backed up user story file to workspace")
else:
    print_warning(f"User story file not found: {user_story_file}")

# Reset user story file from template
if os.path.isfile(template_user_story):
    shutil.copy2(template_user_story, user_story_file)
    print_success(f"Reset user story file from template")
else:
    print_warning(f"Template not found: {template_user_story}")
```

### Step 4: Updated requirements.md ✓

**File:** `.rdd-docs/requirements.md`

Added new requirement:
- **[FR-101] User Story File Management**: The framework shall provide a user-story.md template that is copied to .rdd-docs/ during iteration creation and backed up to workspace then reset from template during iteration completion

### Step 5: Updated tech-spec.md ✓

**File:** `.rdd-docs/tech-spec.md`

Updated Project Folder Structure section:
- Added `user-story.md` to `.rdd/templates/` directory listing
- Added `user-story.md` to `.rdd-docs/` directory listing with explanation of backup during completion
- Updated workspace comment to mention user-story.md is backed up during completion

## Summary

Successfully implemented all requirements from P07:

1. ✅ Created `.rdd/templates/user-story.md` template with standard structure
2. ✅ Modified `create_iteration()` to copy user-story.md to `.rdd-docs/` during iteration creation
3. ✅ Modified `complete_iteration()` to backup user-story.md to workspace and reset from template
4. ✅ Added FR-101 to requirements.md
5. ✅ Updated tech-spec.md Project Folder Structure section

The implementation follows the same pattern as work-iteration-prompts.md, ensuring consistency with the existing framework design.

## Files Analysis

Ran the script `.rdd-docs/workspace/list-files.py` which generated `.rdd-docs/workspace/files-list.md` containing:
- Total of 5346 items (files and folders) scanned
- Excluded all folders starting with "."
- Each file includes name, relative path, and last modification timestamp

The files-list.md will be used by files-analysis.md (if needed) to track changes and update tech-spec.md Project Folder Structure section.

Note: Since this is a prompt execution and we already manually updated the tech-spec.md with the new user-story.md file locations, the automated folder structure update is already complete. The files-list.md and files-analysis.md are available for future reference if deeper analysis is needed.

## Bug Fix

**Issue Found**: The `mark-completed` and `list` actions in `route_prompt()` were still using the old path `WORKSPACE_DIR/work-iteration-prompts.md` instead of the new path `.rdd-docs/work-iteration-prompts.md` (as changed in P06).

**Fix Applied**: Updated both references in `.rdd/scripts/rdd.py`:
- Line ~1796: Changed `journal_file = os.path.join(WORKSPACE_DIR, "work-iteration-prompts.md")` to `journal_file = ".rdd-docs/work-iteration-prompts.md"`
- Line ~1806: Changed `journal_file = os.path.join(WORKSPACE_DIR, "work-iteration-prompts.md")` to `journal_file = ".rdd-docs/work-iteration-prompts.md"`

**Verification**: Successfully marked P07 as completed after the fix.

Command executed:
```bash
python .rdd/scripts/rdd.py prompt mark-completed P07
```

Result: ✓ Marked prompt P07 as completed

## Final Status

✅ **All tasks completed successfully**

- Created user-story.md template with standard structure
- Integrated into create_iteration() workflow
- Integrated into complete_iteration() workflow  
- Updated requirements.md with FR-101
- Updated tech-spec.md Project Folder Structure
- Fixed bug in prompt marking functionality
- Successfully marked P07 as completed

The user story template is now fully integrated into the RDD framework and follows the same lifecycle pattern as work-iteration-prompts.md.
