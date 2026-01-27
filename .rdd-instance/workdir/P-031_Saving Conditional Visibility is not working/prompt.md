When initially fulfilling "Conditional Visibility" for a question in "Technical Design Schema Editor", the set condition is not recorded in the JSON file and the editor for multiselect is not appearing.


In browser console the following errors appear:

app.js:1329 Uncaught TypeError: Cannot set properties of null (setting 'innerHTML')
    at handleConditionQuestionChange (app.js:1329:30)
    at HTMLSelectElement.<anonymous> (app.js:1266:54)
handleConditionQuestionChange	@	app.js:1329
(anonymous)	@	app.js:1266

Check the code in `tech_design_schema_editor/static/app.js`, troubleshoot and refactor the functionality.

Improved prompt:

**Problem Statement**:
The conditional visibility feature in the Technical Design Schema Editor fails when users attempt to initially set visibility conditions for a question. The browser console shows:

```
Uncaught TypeError: Cannot set properties of null (setting 'innerHTML')
    at handleConditionQuestionChange (app.js:1329:30)
```

**Reproduction Steps**:
1. Open the Technical Design Schema Editor
2. Select any question in the editor
3. Scroll to "Conditional Visibility" section
4. Click "Add Condition" to create a new condition row
5. Select a category from the first dropdown
6. Select a question from the second dropdown
7. **Error occurs**: Console shows null reference error
8. **Observable issues**:
   - Operator dropdown is not populated
   - Value field (multiselect for multiselect questions) does not appear
   - Condition is not saved to the JSON file

**Root Cause Analysis** (optional, but helpful):
Initial investigation suggests the querySelector at line 1325 may be matching the wrong element due to non-specific selector `[data-index="${index}"]` which could match option items or other elements.

**Expected Behavior**:
- Operator dropdown should populate based on selected question type
- Value field should appear and show appropriate input type (multiselect, single select, or text)
- Condition should be saved to question's visibleWhen property in JSON
- No console errors should occur

**Required Changes**:
1. Fix the querySelector specificity to target only condition rows
2. Implement the moderate refactoring approach as defined in questionnaire answer Q1-B
3. Add defensive null checks as per Q3-A
4. Avoid unnecessary re-renders as per Q4-A
5. Add inline validation messages as per Q2-B
6. Ensure existing conditions (if any) continue to load and edit correctly

**Files to Modify**:
- `tech_design_schema_editor/static/app.js` - Primary fix location

**Testing Checklist**:
- [ ] Can add new condition rows without errors
- [ ] Category selection populates question dropdown correctly
- [ ] Question selection populates operator dropdown correctly
- [ ] Operator selection shows appropriate value field (multiselect/select/text)
- [ ] Value changes are saved to window.currentConditions
- [ ] Conditions are persisted to JSON on save
- [ ] Existing conditions load and display correctly
- [ ] Multiple conditions can be added and edited
- [ ] Removing conditions works correctly
- [ ] Focus is preserved when editing individual fields

**Implementation Guidance**:
Follow the questionnaire decisions made in questionnaire.json for this prompt, particularly regarding refactoring scope (moderate), error handling (inline messages), defensive programming (yes), and DOM lifecycle management (avoid unnecessary re-renders).
