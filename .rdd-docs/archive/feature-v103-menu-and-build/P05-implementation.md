# P05 Implementation: Fix Misleading "main" Naming in Git Operations

## Prompt
In the menu and as names of the procedures in `.rdd/scripts/rdd.py` and `.rdd/scripts/rdd_utils.py` for git operations is used main as representation of the default branch. For example: merge_main_into_current, fetch_main, compare_with_main and so on. These commands actually are working with the default branch from config file. Analyze and fix this misleading naming. Be careful not to change the places were the name "main" is properly used. Update '.rdd/scripts/scripts-catalogue.md' as well in accordance.

## Analysis Started
Date: 2025-11-08

## Step 1: Reading Context Files

Successfully read:
- `.rdd-docs/requirements.md` - Requirements file
- `.rdd/scripts/rdd.py` - Main script with menu and procedures
- `.rdd/scripts/rdd_utils.py` - Utility functions
- `.rdd/scripts/scripts-catalogue.md` - Scripts catalogue documentation

## Step 2: Analysis

### Current Situation
The code uses "main" in several places where it should use "default branch" terminology:

**In rdd.py:**
1. Function names:
   - `fetch_main()` - should reference default branch
   - `pull_main()` - in rdd_utils, should reference default branch
   - `merge_main_into_current()` - should reference default branch
   - `compare_with_main()` - should reference default branch
   
2. Menu text and documentation:
   - Menu option: "Compare with Main"
   - Menu option: "Update from Main"
   - Help text references

**In rdd_utils.py:**
1. Function names:
   - `pull_main()` - should reference default branch
   - `merge_main_into_current()` - should reference default branch
   - `update_from_main()` - should reference default branch

2. String messages within functions that say "main" but actually work with default branch

**In scripts-catalogue.md:**
1. Menu option names: "Compare with Main", "Update from Main"

### Implementation Strategy

I need to:
1. Rename functions to use "default" instead of "main" terminology
2. Update all menu text and help text
3. Update the scripts-catalogue.md documentation
4. Be careful NOT to change places where "main" is properly used (e.g., when checking if a branch is literally named "main")

### Affected Functions and Their New Names

**rdd.py:**
- `fetch_main()` → `fetch_default_branch()`
- `compare_with_main()` → `compare_with_default_branch()`

**rdd_utils.py:**
- `pull_main()` → `pull_default_branch()`
- `merge_main_into_current()` → `merge_default_branch_into_current()`
- `update_from_main()` → `update_from_default_branch()`

**Menu changes:**
- "Compare with Main" → "Compare with Default Branch"
- "Update from Main" → "Update from Default Branch"
- "Cleanup After Merge" description mentions main

**Help text changes:**
- Update all help documentation to use "default branch" terminology

## Step 3: Implementation

### Changes in rdd_utils.py

1. **Renamed function `pull_main()` to `pull_default_branch()`**
   - Updated function name and docstring
   - All internal logic remains the same (already uses `get_default_branch()`)

2. **Renamed function `merge_main_into_current()` to `merge_default_branch_into_current()`**
   - Updated function name and docstring
   - Fixed comment inside function: "don't merge if we're on main" → "don't merge if we're on default branch"

3. **Renamed function `update_from_main()` to `update_from_default_branch()`**
   - Updated function name and docstring
   - Updated docstring references from "main" to "default branch"
   - Updated internal comments from "main" to "default branch"
   - Updated calls to renamed functions: `pull_main()` → `pull_default_branch()`
   - Updated calls to renamed functions: `merge_main_into_current()` → `merge_default_branch_into_current()`

### Changes in rdd.py

1. **Updated imports from rdd_utils**
   - Changed: `pull_main` → `pull_default_branch`
   - Changed: `merge_main_into_current` → `merge_default_branch_into_current`
   - Changed: `update_from_main` → `update_from_default_branch`

2. **Renamed function `fetch_main()` to `fetch_default_branch()`**
   - Updated function name and docstring

3. **Renamed function `compare_with_main()` to `compare_with_default_branch()`**
   - Updated function name and docstring
   - Updated call to `fetch_main()` → `fetch_default_branch()`

4. **Updated function calls in route_git()**
   - Line ~1428: `compare_with_main()` → `compare_with_default_branch()`
   - Line ~1437: `update_from_main()` → `update_from_default_branch()`
   - CLI action name: `'update-from-main'` → `'update-from-default-branch'`

5. **Updated function calls in git_operations_submenu()**
   - Line ~1740: `compare_with_main()` → `compare_with_default_branch()`
   - Line ~1746: `update_from_main()` → `update_from_default_branch()`

6. **Updated menu labels in git_operations_submenu()**
   - "Compare with Main" → "Compare with Default Branch"
   - "Update from Main" → "Update from Default Branch"

7. **Updated help text in show_git_help()**
   - Action description: "Compare current branch with main" → "Compare current branch with default branch"
   - Action description: "Update current branch from main" → "Update current branch from default branch"
   - Action name: `update-from-main` → `update-from-default-branch`
   - Example command: `rdd.py git update-from-main` → `rdd.py git update-from-default-branch`

8. **Updated help text in show_branch_help()**
   - "Post-merge cleanup: fetch main, pull, delete branch" → "Post-merge cleanup: fetch default branch, pull, delete branch"

### Changes in scripts-catalogue.md

1. **Updated Git Operations menu entries**
   - "Compare with Main" → "Compare with Default Branch"
   - Description: "Compares current branch with main/default branch" → "Compares current branch with the configured default branch"
   - "Modified Files" description: "Lists files modified compared to main/default branch" → "Lists files modified compared to the configured default branch"
   - "Update from Main" → "Update from Default Branch"
   - Command: `rdd.py git update-from-main` → `rdd.py git update-from-default-branch`
   - Description: "Updates current branch with latest changes from main/default branch" → "Updates current branch with latest changes from the configured default branch"

## Step 4: Verification

Running error check on modified files...

**Result:** ✅ No errors found in:
- `/home/hromar/Desktop/vscode/requirements-driven-development/.rdd/scripts/rdd.py`
- `/home/hromar/Desktop/vscode/requirements-driven-development/.rdd/scripts/rdd_utils.py`

## Step 5: Summary

Successfully renamed all misleading "main" references in git operations to use "default branch" terminology:

### Functions Renamed:
- `fetch_main()` → `fetch_default_branch()`
- `pull_main()` → `pull_default_branch()`
- `merge_main_into_current()` → `merge_default_branch_into_current()`
- `compare_with_main()` → `compare_with_default_branch()`
- `update_from_main()` → `update_from_default_branch()`

### CLI Command Changed:
- `rdd.py git update-from-main` → `rdd.py git update-from-default-branch`

### Menu Options Updated:
- "Compare with Main" → "Compare with Default Branch"
- "Update from Main" → "Update from Default Branch"

### Files Modified:
1. `.rdd/scripts/rdd_utils.py` - 3 function renames + internal comments
2. `.rdd/scripts/rdd.py` - 2 function renames + imports + menu labels + help text
3. `.rdd/scripts/scripts-catalogue.md` - Documentation updated

### Places NOT Changed (Correctly):
- References to the literal branch name "main" in protected branch checks
- Archived legacy code in `.rdd-docs/archive/` directory

All changes maintain backward compatibility with the actual functionality - the code already used `get_default_branch()` internally, we just fixed the misleading naming.

## Completion

✅ Prompt P05 has been successfully executed and marked as completed.

All misleading "main" references in git operation names have been corrected to use "default branch" terminology, making the code clearer and more accurate about what it actually does (working with the configured default branch, not necessarily "main").
