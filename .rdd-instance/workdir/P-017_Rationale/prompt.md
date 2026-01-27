Technical design rationale field - implement the functionality so to be able to edit the rationale in the Web UI.

## Objective
Implement UI controls for editing the optional `rationale` field in the Technical Design page, allowing users to provide explanations for their architectural decisions.

## Context
- The backend already supports rationale: `technical_design_answer_set.py` accepts `rationale=` parameter (TR-0189)
- The `/api/technical-design/answer/set` endpoint accepts rationale in requests
- The frontend Technical Design page (`app.js`) currently has no UI controls for rationale
- Answer objects in `.rdd-instance/specifications/technical-design.json` include an optional `rationale` field

## Requirements
1. Display a textarea input for rationale on the Technical Design page
2. The textarea should appear inline below the answer selection controls
3. Only show rationale input when an answer exists for the question
4. Auto-save rationale to backend on blur (when user clicks away)
5. Display existing rationale text when loading answered questions
6. Clear rationale when the answer is cleared via "Clear Answer" button
7. Preserve existing rationale when updating an answer value

## Implementation Approach
**Location**: Modify the `renderQuestion()` function in `.rdd/src/web/static/app.js`

**Steps**:
1. Add rationale textarea element after answer controls when `currentAnswer` exists
2. Populate textarea with `currentAnswer.rationale` value (if any)
3. Add `onblur` handler to save rationale along with answer
4. Update `saveQuestionAnswer()` to include rationale in API request body
5. Ensure `clearQuestionAnswer()` also clears rationale

**UI Specifications**:
- Use Bootstrap `form-control` class for consistent styling
- Set `rows="3"` for comfortable editing
- Placeholder: "Explain the reasoning for this answer..."
- Label: "Rationale (optional)"
- Position: Between the current answer display and the Clear Answer button

## Acceptance Criteria
- ✅ User can type rationale text when editing any answered question
- ✅ Rationale auto-saves when user clicks away from textarea (blur event)
- ✅ Existing rationale loads and displays when viewing answered questions
- ✅ Rationale is cleared when user clicks "Clear Answer"
- ✅ Rationale is preserved when user changes the answer value
- ✅ Works correctly for all three question types (radio, multiselect, text)
- ✅ No console errors or API failures

## Testing Checklist
1. Answer a new question and add rationale → verify saves correctly
2. Reload page → verify rationale displays correctly
3. Update answer value → verify rationale is preserved
4. Clear answer → verify rationale is cleared
5. Test with radio, multiselect, and text question types
6. Test with and without existing rationale