# P01 Implementation: Remove Fix Branch Prefix

## Prompt Description
When executed `.github/prompts/rdd.01-initiate.prompt.md`, the script called is asking to be clarified if it will be fix or enhancement branch and in case of fix - predefines a prefix "fix/". Remove this predefined prefix. Let the user decides by themselves the whole string. Only kebab case should be left. Asking for Fix should remain as it defines the content of the workspace that needs to be populated.

## Analysis

### Current Behavior
The prompt P01 describes an issue where the script `rdd.py change create` is:
1. Asking users to select between fix/enhancement (which is correct)
2. Pre-defining a "fix/" prefix for fix branches (which needs to be removed)
3. The user wants full control over the branch name string
4. Only kebab-case validation should remain
5. The fix/enhancement distinction should remain as it affects workspace initialization

### Files to Investigate
1. `.rdd/scripts/rdd.py` - Main entry point for change creation
2. `.rdd/scripts/rdd_utils.py` - Utility functions for branch creation

### Implementation Plan
1. Read the current implementation of change creation
2. Identify where the "fix/" prefix is being added
3. Remove the prefix logic while keeping kebab-case validation
4. Keep the fix/enhancement distinction for workspace initialization
5. Test the changes
6. Document the changes in this file

## Step 1: Reading Current Implementation

I've read the implementation files. The key findings:

### Current Behavior in rdd.py:

In the `create_branch()` function (lines ~706-779):
```python
# Generate branch ID with timestamp
date_time = get_timestamp_filename()
branch_id = f"{date_time}-{branch_name}"
full_branch_name = f"{branch_type}/{branch_id}"  # <-- Creates branch with type prefix
```

The script creates branches in this format:
- For fix: `fix/20251107-0541-my-fix`
- For enhancement: `enh/20251107-0541-my-enhancement`

### Issue Identified

The user wants to:
1. ✅ Keep the fix/enhancement distinction (it determines workspace content)
2. ❌ **Remove the automatic "fix/" or "enh/" prefix** from the branch name
3. ✅ Keep only kebab-case validation
4. ✅ Let users decide the full branch name string themselves

### Root Cause

The prefix is added in the `create_branch()` function on line ~717:
```python
full_branch_name = f"{branch_type}/{branch_id}"
```

This automatically prepends "fix/" or "enh/" to all branch names.

## Step 2: Implementation Strategy

The solution requires:
1. Remove the automatic prefix from branch name construction
2. Let users provide the full branch name (including any prefix they want)
3. Keep the fix/enhancement type selection (for workspace initialization only)
4. Update the branch creation logic to use the user-provided name directly
5. Keep kebab-case validation
6. Update timestamp injection to be optional or remove it if user wants control

### Approach
The cleanest approach is to:
1. Still ask user for change type (fix/enhancement) - this determines workspace content
2. Ask user for branch name - accept full branch name as-is (with kebab-case validation)
3. Remove automatic prefix and timestamp injection
4. Let user control the entire branch naming

## Step 3: Making the Changes

Now I'll modify the code to remove the automatic prefix.

### Change 1: Modified `create_branch()` function in rdd.py

**Location**: Lines ~706-779

**Changes made**:
1. Removed automatic timestamp injection: `date_time = get_timestamp_filename()`
2. Removed branch ID construction: `branch_id = f"{date_time}-{branch_name}"`
3. Removed automatic prefix: `full_branch_name = f"{branch_type}/{branch_id}"`
4. Changed to use branch_name as-is: `full_branch_name = branch_name`
5. Updated display output to show branch type separately

**Before**:
```python
# Generate branch ID with timestamp
date_time = get_timestamp_filename()
branch_id = f"{date_time}-{branch_name}"
full_branch_name = f"{branch_type}/{branch_id}"
```

**After**:
```python
# Use the branch_name as-is (no automatic prefix or timestamp)
full_branch_name = branch_name
```

This change means:
- Users provide the complete branch name (e.g., "fix/my-bugfix", "my-feature", "20251107-my-fix")
- No automatic "fix/" or "enh/" prefix is added
- No automatic timestamp is injected
- Only kebab-case validation is enforced
- The branch type (fix/enh) is still tracked for workspace initialization purposes

### Change 2: Modified `validate_branch_name()` in rdd_utils.py

**Location**: Lines ~151-167

**Changes made**:
1. Removed strict format requirement for `{type}/{timestamp}-{name}`
2. Changed to allow any kebab-case format with slashes
3. Updated error messages to reflect new validation rules

**Before**:
```python
# Check format: {type}/{timestamp}-{name}
if not re.match(r'^(enh|fix)/[0-9]{8}-[0-9]{4}-.+$', branch_name):
```

**After**:
```python
# Check kebab-case format (lowercase, hyphens, numbers, slashes allowed)
if not re.match(r'^[a-z0-9]+([/-][a-z0-9]+)*$', branch_name):
```

### Change 3: Updated wrap-up validation messages in rdd.py

**Location**: Lines ~1143-1150

**Changes made**:
Updated example branch names in error messages to reflect that users now control the full branch name.

**Before**:
```
Valid branch format examples:
  • enh/20241101-1234-my-enhancement
  • fix/20241101-1234-my-bugfix
```

**After**:
```
Valid branch examples:
  • my-enhancement
  • fix/my-bugfix
  • 20241101-1234-my-feature
```

### Change 4: Updated string normalization in rdd_utils.py

**Location**: Lines ~198-220

**Changes made**:
Updated `normalize_to_kebab_case()` function to preserve slashes in branch names.

**Before**:
```python
normalized = re.sub(r'[^a-z0-9-]', '', normalized)
```

**After**:
```python
normalized = re.sub(r'[^a-z0-9/-]', '', normalized)
```

This allows users to input branch names like "fix/my-bugfix" or "Fix/My Bugfix" and have them normalized to "fix/my-bugfix".

### Change 5: Updated help messages and prompts

**Changes made**:
1. Updated `show_branch_help()` to show examples with user-controlled branch names
2. Updated change creation banner to mention "user-controlled branch name"
3. Updated input prompt examples to show full branch names with slashes
4. Updated success message to show branch type separately from branch name

## Step 4: Testing the Changes

Let me verify that the changes don't break any existing functionality by checking for errors:

### Syntax Check

No syntax errors found in the modified files.

### Summary of All Changes

1. **rdd.py - `create_branch()` function**: Removed automatic prefix and timestamp injection, now uses branch_name as-is
2. **rdd_utils.py - `validate_branch_name()` function**: Relaxed validation to allow any kebab-case format with slashes
3. **rdd_utils.py - `normalize_to_kebab_case()` function**: Updated to preserve slashes in branch names
4. **rdd.py - `wrap_up_change()` function**: Updated example branch names in error messages
5. **rdd.py - `show_branch_help()` function**: Updated help examples
6. **rdd.py - `route_change()` function**: Updated banner and prompts for branch name input
7. **rdd.py - `create_change()` function**: Updated success message display

## Step 5: Implementation Complete

The implementation is now complete. The changes achieve the following goals:

✅ **User Control**: Users now have complete control over the branch name string
✅ **No Automatic Prefix**: The "fix/" or "enh/" prefix is no longer automatically added
✅ **Kebab-Case Only**: Only kebab-case validation remains (plus slashes are allowed)
✅ **Fix/Enhancement Distinction Preserved**: The fix/enhancement selection is still asked for workspace initialization
✅ **Flexible Naming**: Users can choose to include prefixes like "fix/" if they want, or use any other naming convention

### Examples of Valid Branch Names Now:

- `my-feature` (simple name)
- `fix/my-bugfix` (user chooses to add fix/ prefix)
- `20251107-my-enhancement` (user includes timestamp)
- `feature/add-user-auth` (custom prefix)
- `bugfix-login-issue` (no prefix, descriptive name)

The change type (fix/enhancement) is still selected interactively, but it only affects workspace initialization, not the branch name.

## Completion

✅ Prompt P01 has been successfully executed and marked as completed.

### Files Modified:
1. `.rdd/scripts/rdd.py` - 4 modifications
2. `.rdd/scripts/rdd_utils.py` - 2 modifications

### Verification:
- No syntax errors in modified files
- All changes follow the requirements
- Kebab-case validation preserved
- Fix/enhancement distinction maintained for workspace initialization
- User has full control over branch naming
