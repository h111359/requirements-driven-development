In Technical Design Schema Editor in `tech_design_schema_editor` I want to be able to move the categories, questions and question answer options up and down 

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