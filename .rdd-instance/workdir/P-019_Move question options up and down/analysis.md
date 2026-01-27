# Analysis: Move question options up and down

## Copilot Review

### Current Situation

The prompt requests adding reordering functionality to the Technical Design Schema Editor in `tech_design_schema_editor/`. The editor is a standalone web-based tool for managing `.rdd/config/technical-design-schema.json`.

**Current Editor Capabilities:**
- Full CRUD operations on categories and questions
- Tree navigation with expand/collapse
- Search and filter
- Form-based editing
- Validation and backup
- Vanilla JavaScript (no external libraries)
- ~785 lines of JavaScript code

**Missing Functionality:**
The editor currently lacks any reordering mechanism. Users cannot change the order of:
- Categories within the schema
- Questions within a category
- Options within a question

**Questionnaire Responses:**
All questions answered with option A:
1. **UI Pattern**: Up/Down arrow buttons (not drag-and-drop)
2. **Control Placement**: Inline with each item (always visible)
3. **Keyboard Shortcuts**: Yes - Alt+Up/Down
4. **Edge Cases**: Disable buttons when move is invalid
5. **Save Behavior**: Manual save (mark as modified)

### Assessment

**Completeness of Prompt:**
The prompt is clear about what needs to be done but lacks implementation details. The questionnaire fills this gap by clarifying UX decisions.

**Scope:**
- Add reordering for 3 entity types: categories, questions, options
- Implement UI controls (arrow buttons)
- Implement keyboard shortcuts (Alt+Up/Down)
- Update editor state management
- Integrate with existing save workflow

**Implementation Complexity:**
- **Low-Medium Complexity**: The core logic (array swapping) is straightforward
- **Integration Points**: Must integrate with existing tree rendering, form editing, and save workflow
- **No External Dependencies**: Implementation uses vanilla JavaScript matching existing codebase

### Potential Risks and Challenges

**1. State Management:**
- Need to track which item is currently selected for keyboard shortcuts
- Must preserve selection after reordering
- Tree view must re-render after each move

**2. UI Complexity:**
- Adding buttons to tree items may crowd the interface
- Need to dynamically enable/disable buttons based on position
- Must handle nested structures (categories contain questions contain options)

**3. Data Integrity:**
- Reordering must preserve all item properties
- Must mark schema as modified
- Need to validate after reorder (ensure no data corruption)

**4. User Experience:**
- Focus management after move (keep moved item focused)
- Visual feedback during move
- Keyboard shortcuts must not conflict with browser shortcuts

**5. Testing:**
- Multiple edge cases: first item, last item, single item lists
- Keyboard shortcuts across different browsers
- Undo/redo behavior (currently not supported)

### Impact on Existing Functionality

**Minimal Risk:**
- Feature is additive (no removal of existing functionality)
- Core editing and validation remain unchanged
- Only affects rendering and event handling

**Modified Components:**
- Tree rendering function (add arrow buttons)
- Event listeners (keyboard shortcuts)
- Save workflow (already handles modifications)
- Option rendering in question form

## Best Practices

### URLs Checked:

**1. Array Reordering Implementation:**
- https://stackoverflow.com/questions/76096628/reorder-javascript-array-by-up-down-buttons
- https://gomakethings.com/how-to-reorder-an-item-in-an-array-with-vanilla-js/
- https://www.delftstack.com/howto/javascript/javascript-reorder-array/

**2. UX and Accessibility:**
- https://www.darins.page/articles/designing-a-reorderable-list-component
- https://ux.stackexchange.com/questions/153585/reordering-list-items-using-up-down-buttons

**3. Keyboard Shortcuts:**
- https://keypress.io/resources/keyboard-shortcuts-javascript
- https://javascriptbit.com/handle-keyboard-shortcuts-javascript/
- https://joshuatz.com/posts/2020/get-alt-keyboard-shortcuts-working-quickly-with-javascript/

### Key Findings:

**Array Reordering:**
```javascript
function moveElement(array, fromIndex, toIndex) {
    if (toIndex < 0 || toIndex >= array.length) return array;
    [array[fromIndex], array[toIndex]] = [array[toIndex], array[fromIndex]];
    return array;
}
```
- Use array destructuring for clean swapping
- Boundary checks prevent invalid moves
- Mutate in place, then re-render

**Button State Management:**
- Disable "Up" button on first item
- Disable "Down" button on last item
- Use `button.disabled = true/false` for visual feedback
- Re-evaluate button states after each move

**Keyboard Shortcuts:**
```javascript
document.addEventListener('keydown', (e) => {
    if (e.altKey && e.code === 'ArrowUp') {
        e.preventDefault();
        moveSelectedItemUp();
    }
});
```
- Use `keydown` event (not keypress/keyup)
- Check `event.altKey` for modifier
- Use `event.code` for physical key (not deprecated keyCode)
- Call `preventDefault()` to avoid browser conflicts
- Alt+Arrow is safer than Ctrl+Arrow (less browser conflicts)

**UX Best Practices:**
- Always-visible controls are more discoverable
- Provide clear visual feedback (disabled state)
- Keep focus on moved item after reordering
- Use unicode arrow symbols: ↑ (U+2191), ↓ (U+2193)
- Add aria-label for accessibility

**Focus Management:**
- After moving, set focus back to the moved item
- Helps keyboard users track their position
- Important for screen readers

## Proposals

### Recommended Implementation Approach

**Phase 1: Core Reordering Logic**
1. Add helper functions for array manipulation:
   - `moveItemUp(array, index)`
   - `moveItemDown(array, index)`
2. Integrate with schema state management
3. Mark schema as modified on each move

**Phase 2: UI Controls for Categories**
1. Add up/down arrow buttons to category tree items
2. Wire buttons to reorder category array
3. Implement button enable/disable logic
4. Re-render tree after move

**Phase 3: UI Controls for Questions**
1. Add arrow buttons to question tree items (nested under categories)
2. Wire to reorder questions within current category
3. Handle button states
4. Update tree rendering

**Phase 4: UI Controls for Options**
1. Add arrow buttons to option list in question editor form
2. Wire to reorder options array
3. Update form rendering
4. Consider inline editing vs. separate controls

**Phase 5: Keyboard Shortcuts**
1. Track currently selected item (category, question, or option)
2. Add global keydown listener for Alt+Up/Down
3. Determine item type and call appropriate move function
4. Provide visual feedback (highlight moved item)

**Phase 6: Testing & Polish**
1. Test all edge cases (first, last, single item)
2. Test keyboard shortcuts across browsers
3. Verify focus management
4. Ensure accessibility (aria-labels, keyboard navigation)
5. Update README with new feature documentation

### Alternative: Simplified Version

If full implementation is too complex initially, consider:
- **Phase 1 Only**: Implement just option reordering (most frequently needed)
- **Defer Keyboard Shortcuts**: Add in future iteration
- **Inline Only**: Skip tree view reordering, only form-based option reordering

**Pros**: Faster delivery, lower risk, addresses most common use case
**Cons**: Incomplete solution, may require rework later

### Recommended: Full Implementation

Given the questionnaire responses and the straightforward nature of the implementation, proceed with full implementation. The technical complexity is manageable and aligns with user expectations for a schema editor.

## Prompt Modification

### Improved Prompt Version

```
Add reordering functionality to the Technical Design Schema Editor (`tech_design_schema_editor/`) to allow users to change the order of categories, questions, and question options.

**Context:**
- Editor location: `tech_design_schema_editor/`
- Schema file: `.rdd/config/technical-design-schema.json`
- Current implementation: Vanilla JavaScript (~785 lines), no external libraries
- Existing capabilities: Full CRUD, tree navigation, search, validation

**Requirements:**

1. **Reordering Mechanisms:**
   - Categories: Reorder within schema.categories array
   - Questions: Reorder within category.questions array
   - Options: Reorder within question.options array

2. **UI Controls - Arrow Buttons:**
   - Add inline up (↑) and down (↓) arrow buttons
   - Always visible next to each item
   - Disable up button on first item
   - Disable down button on last item
   - Use unicode symbols: ↑ (U+2191), ↓ (U+2193)
   - Add aria-label for accessibility

3. **Keyboard Shortcuts:**
   - Alt+Up: Move selected item up
   - Alt+Down: Move selected item down
   - Add global keydown listener
   - Use event.preventDefault() to avoid browser conflicts
   - Track currently selected item (category/question/option)

4. **Behavior:**
   - Swap adjacent items in array
   - Mark schema as modified (trigger existing modified flag)
   - Re-render affected UI sections
   - Maintain focus on moved item after reordering
   - Require manual save (consistent with editor workflow)

5. **Implementation Details:**
   - Use array destructuring for swapping: `[arr[i], arr[j]] = [arr[j], arr[i]]`
   - Add boundary checks before moving
   - Update button disabled states after each move
   - Preserve all item properties during move
   - No external libraries (vanilla JavaScript only)

6. **Integration Points:**
   - Modify tree rendering to include arrow buttons
   - Modify option rendering in question form editor
   - Add event handlers for button clicks
   - Add global keyboard event listener
   - Use existing `setModified()` function to mark changes

7. **Testing Requirements:**
   - Test edge cases: first item, last item, single item
   - Verify keyboard shortcuts work across browsers
   - Ensure focus management works correctly
   - Validate data integrity after multiple moves
   - Test with empty arrays

8. **Documentation:**
   - Update README.md with new reordering feature
   - Document keyboard shortcuts
   - Add usage examples for reordering

**Deliverables:**
- Modified `tech_design_schema_editor/static/app.js`
- Modified `tech_design_schema_editor/index.html` (if needed for styling)
- Modified `tech_design_schema_editor/static/style.css` (if needed)
- Updated `tech_design_schema_editor/README.md`

**Success Criteria:**
- Users can reorder categories using buttons and keyboard
- Users can reorder questions using buttons and keyboard
- Users can reorder options using buttons and keyboard
- Buttons are properly enabled/disabled at boundaries
- Schema is marked as modified after reordering
- Changes persist when saved
- Keyboard shortcuts don't conflict with browser shortcuts
- Feature is documented in README
```

### Rationale for Changes:

1. **Specific Implementation Details**: Provides exact array manipulation approach, UI symbols, keyboard event handling
2. **Clear Requirements**: Breaks down into discrete, testable requirements
3. **Integration Guidance**: Identifies exact points where code modifications are needed
4. **Testing Criteria**: Defines specific edge cases and validation steps
5. **Deliverables**: Lists exact files to be modified
6. **Success Criteria**: Provides measurable completion criteria
7. **Maintains Scope**: Stays focused on reordering feature without scope creep
8. **Accessibility**: Explicitly mentions aria-label and keyboard navigation
9. **Browser Compatibility**: Addresses potential conflicts and testing needs
