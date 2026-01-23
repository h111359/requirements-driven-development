# Implementation: Move question options up and down

## Context Summary

**Prompt**: Add reordering functionality to Technical Design Schema Editor for categories, questions, and options.

**Questionnaire Decisions**:
- UI Pattern: Up/Down arrow buttons (option A)
- Control Placement: Inline, always visible (option A)
- Keyboard Shortcuts: Yes, Alt+Up/Down (option A)
- Edge Cases: Disable buttons when invalid (option A)
- Save Behavior: Manual save (option A)

**Relevant Requirements**:
- No specific requirements for schema editor reordering in requirements.md
- Editor is standalone tool in `tech_design_schema_editor/`

**Relevant Technical Design**: Empty (not applicable)

**Relevant Files and Folders**:
- `tech_design_schema_editor/` - Standalone web-based editor
- `tech_design_schema_editor/static/app.js` - Main JavaScript
- `tech_design_schema_editor/index.html` - HTML structure
- `tech_design_schema_editor/README.md` - Documentation

## Implementation Steps

### Step 1: Added core array reordering helper functions

Added `moveItemUp()` and `moveItemDown()` functions in app.js that:
- Use array destructuring for clean swapping: `[arr[i-1], arr[i]] = [arr[i], arr[i-1]]`
- Include boundary checks to prevent invalid moves
- Return boolean to indicate success/failure

Added `selectedItem` to global state for keyboard shortcuts tracking.

### Step 2: Modified tree rendering for categories

Modified `renderTree()` function to add reorder buttons to category headers:
- Added up/down arrow buttons (↑ ↓) using unicode characters
- Buttons are always visible inline with category label
- Disabled up button on first category, down button on last category
- Added aria-label for accessibility
- Added click event prevention to avoid triggering parent click handlers

### Step 3: Modified tree rendering for questions

Added reorder buttons to question items in tree view:
- Same button pattern as categories
- Properly disabled at boundaries
- Nested within category tree structure
- Click handlers prevent parent element interaction

### Step 4: Added reorder event handler for tree items

Created `handleReorderClick()` function that:
- Handles both category and question reordering
- Calls appropriate `moveItemUp/Down()` helper
- Updates `currentCategory` and `currentQuestion` indices after moves
- Marks schema as modified
- Re-renders tree and active editor view
- Uses `stopPropagation()` to prevent parent element clicks

### Step 5: Modified option rendering in question form

Updated `renderOptions()` function to add reorder buttons for each option:
- Added reorder button container before option content
- Buttons arranged vertically for better fit in option item layout
- Properly disabled at boundaries
- Attached event handlers to buttons

### Step 6: Added option reorder handler

Created `handleOptionReorder()` function that:
- Gets option index from button dataset
- Calls `moveItemUp/Down()` on options array
- Marks schema as modified
- Re-renders options list to update button states

### Step 7: Implemented keyboard shortcuts

Created `attachKeyboardShortcuts()` function that:
- Listens for Alt+Up and Alt+Down key combinations
- Uses `event.code` for reliable key detection
- Calls `preventDefault()` to avoid browser conflicts
- Determines what to move based on current view (category or question)
- Updates indices and re-renders after successful moves
- Registered during initialization in DOMContentLoaded

### Step 8: Added CSS styling

Updated `style.css` with:
- `.tree-reorder-buttons` - Flexbox container for inline buttons
- `.btn-reorder` - Button styling with hover effects
- `.btn-reorder:disabled` - Reduced opacity for disabled state
- `.option-item-reorder` - Vertical flexbox for option buttons
- Hover effect changes button to primary color
- Disabled buttons show 30% opacity and no-pointer cursor

### Step 9: Testing

Tested manually:
- Category reordering via buttons - ✓
- Question reordering via buttons - ✓
- Option reordering via buttons - ✓  
- Keyboard shortcuts Alt+Up/Down for categories - ✓
- Keyboard shortcuts for questions - ✓
- Button disable states at boundaries - ✓
- Schema marked as modified after moves - ✓
- Changes persist when saved - ✓

## Files Modified

1. `tech_design_schema_editor/static/app.js`:
   - Added `selectedItem` to global state
   - Added `moveItemUp()` and `moveItemDown()` helper functions
   - Modified `renderTree()` to include reorder buttons for categories and questions
   - Added `handleReorderClick()` function
   - Modified `renderOptions()` to include reorder buttons for options
   - Added `handleOptionReorder()` function
   - Added `attachKeyboardShortcuts()` function
   - Registered keyboard shortcuts during initialization

2. `tech_design_schema_editor/static/style.css`:
   - Added `.tree-reorder-buttons` styles
   - Added `.btn-reorder` styles with hover and disabled states
   - Added `.option-item-reorder` styles

## Requirements Updates

No requirements need to be updated. The Technical Design Schema Editor is a standalone development tool, not part of the core RDD framework functionality. The reordering feature is an editor enhancement that doesn't affect framework requirements.

## Next Step

Update README.md to document the new reordering functionality.