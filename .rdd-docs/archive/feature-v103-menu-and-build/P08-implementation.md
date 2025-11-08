# P08 Implementation: Reorder Menu Options

## Prompt
Order the options in the menu in that way:
- "Create new iteration",
- "Update from default",
- "Complete current iteration",
- "Delete merged branches",
- "Exit"

## Analysis

### Current Menu Order (from rdd.py)
Looking at the `main_menu_loop()` function at line 1855, the current order is:
1. Complete current iteration
2. Create new iteration
3. Delete merged branches
4. Update from default
5. Exit

### Required Order (from P08)
1. Create new iteration
2. Update from default
3. Complete current iteration
4. Delete merged branches
5. Exit

### Changes Needed
The menu options need to be reordered in the `main_menu_loop()` function in `.rdd/scripts/rdd.py` to match the required order. This requires:
- Reordering the `items` list (lines ~1878-1884)
- Updating the conditional checks for `selected` index (lines ~1886-1900)

## Execution Log

### Step 1: Read Current Implementation ✓
Read `.rdd/scripts/rdd.py` at line 1855 to understand the current menu structure.

**Current menu items array:**
```python
items = [
    "Complete current iteration",  # index 0
    "Create new iteration",         # index 1
    "Delete merged branches",       # index 2
    "Update from default",          # index 3
    "Exit"                          # index 4
]
```

**Current action mapping:**
- Index 0 → complete_iteration()
- Index 1 → create_iteration()
- Index 2 → cleanup_after_merge()
- Index 3 → update_from_default_branch()
- Index 4 → Exit

### Step 2: Reorder Menu Items ✓

**File:** `.rdd/scripts/rdd.py`
**Function:** `main_menu_loop()`
**Lines changed:** ~1878-1900

**Changes made:**

1. **Reordered items list** (lines ~1878-1884):
   ```python
   # OLD ORDER:
   items = [
       "Complete current iteration",  # 0
       "Create new iteration",         # 1
       "Delete merged branches",       # 2
       "Update from default",          # 3
       "Exit"                          # 4
   ]
   
   # NEW ORDER:
   items = [
       "Create new iteration",         # 0
       "Update from default",          # 1
       "Complete current iteration",   # 2
       "Delete merged branches",       # 3
       "Exit"                          # 4
   ]
   ```

2. **Updated action mapping** (lines ~1890-1900):
   ```python
   # OLD MAPPING:
   if selected == 0:    # Complete current iteration
   elif selected == 1:  # Create new iteration
   elif selected == 2:  # Delete merged branches
   elif selected == 3:  # Update from default
   
   # NEW MAPPING:
   if selected == 0:    # Create new iteration
   elif selected == 1:  # Update from default
   elif selected == 2:  # Complete current iteration
   elif selected == 3:  # Delete merged branches
   ```

**Result:** Menu now displays options in the order specified by P08 prompt.

### Step 3: Verification ✓

**Command:** Checked the updated code in rdd.py

**Verified:**
- ✅ Menu items list reordered correctly (lines 1879-1885)
- ✅ Action mapping updated to match new indices (lines 1891-1903)
- ✅ Exit option still at index 4
- ✅ All function calls preserved correctly

**New menu flow:**
1. User sees "Create new iteration" first
2. Then "Update from default"
3. Then "Complete current iteration"
4. Then "Delete merged branches"
5. Finally "Exit"

### Step 4: Update Help Text ✓

**File:** `.rdd/scripts/rdd.py`
**Function:** `show_main_help()`
**Lines changed:** ~1330-1340

**Changes made:**
Updated the help text to match the new menu order:

```python
# OLD ORDER:
print("  1. Complete current iteration")
print("  2. Create new iteration")
print("  3. Delete merged branches")
print("  4. Update from default")

# NEW ORDER:
print("  1. Create new iteration")
print("  2. Update from default")
print("  3. Complete current iteration")
print("  4. Delete merged branches")
```

**Command run:** `python .rdd/scripts/rdd.py --help`

**Result:** Help text now shows correct menu order.

## Summary

Successfully reordered the menu options in `.rdd/scripts/rdd.py` to match the P08 requirements:

**Files modified:**
- `.rdd/scripts/rdd.py` (2 locations: menu loop and help text)

**Changes:**
1. ✅ Reordered `items` array in `main_menu_loop()` (lines ~1879-1885)
2. ✅ Updated action mapping conditionals (lines ~1891-1903)
3. ✅ Updated help text in `show_main_help()` (lines ~1330-1340)

**New menu order:**
1. Create new iteration
2. Update from default
3. Complete current iteration
4. Delete merged branches
5. Exit

**Result:** Menu now displays in the logical workflow order specified by P08, both in the interactive menu and help documentation.

## Completion

✅ **Prompt P08 marked as completed**

**Command:** `python .rdd/scripts/rdd.py prompt mark-completed P08`

**Final Status:** All changes implemented successfully. The menu now displays options in the order:
1. Create new iteration
2. Update from default  
3. Complete current iteration
4. Delete merged branches
5. Exit

This order follows a logical workflow where users first create work, update it, complete it, then clean up.

