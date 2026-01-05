# Implementation Plan for P-022: Questionnaire to JSON

## Overview

This plan implements the conversion of the questionnaire system from Markdown to JSON format, enabling programmatic parsing and interactive form-based UI in the Active Prompt page. The JSON structure will support all existing questionnaire attributes (questions, options with pros/cons, recommendations, and custom answers) while providing immediate persistence of user selections.

---

## Step 1: Define JSON Schema and Create Sample Structure

Create a JSON schema definition that reflects the chosen structure from the questionnaire answers:

**Schema Structure:**
```json
{
  "context": "string - descriptive context about the prompt",
  "questions": [
    {
      "id": "string - question identifier (Q1, Q2, etc.)",
      "question-text": "string - the question text",
      "options": [
        {
          "id": "string - option identifier (A, B, C, etc.)",
          "label": "string - option description",
          "pros": "string - advantages of this option",
          "cons": "string - disadvantages of this option"
        }
      ],
      "recommended-option": "string - ID of recommended option",
      "recommendation-rationale": "string - explanation for recommendation",
      "user-selection": {
        "type": "string - predefined|custom|null",
        "value": "string - option ID or custom text or null"
      }
    }
  ]
}
```

Document this schema in a convention file for future reference.

**Files to create:**
- `.rdd/conventions/questionnaire-json-schema.md` - documenting the JSON structure

---

## Step 2: Update Questionnaire Generation Logic

Modify the analyze execution step to generate `questionnaire.json` instead of `questionnaire.md` for new prompts.

**Changes to apply:**
- Update `.rdd/prompt-snippets/execution-step.analyze.md` to specify that questionnaires should be generated in JSON format
- The analyze step should generate well-formed JSON with the schema defined in Step 1
- Each question should include all required fields: id, question-text, options array, recommended-option, recommendation-rationale
- Initial user-selection should be set to `{"type": null, "value": null}` for unanswered questions

**Note:** No changes to existing markdown questionnaires (backward compatibility not required per prompt specification).

---

## Step 3: Create API Endpoint for Questionnaire File Operations

Leverage the existing `/api/file/save` endpoint for questionnaire JSON updates, but add helper functionality if needed.

**Implementation approach:**
- Reuse existing `/api/file/save` endpoint (as per Q10 answer B)
- The frontend will read the entire JSON, modify the specific question's user-selection, and save back
- No new API endpoints required

**Validation to add:**
- Ensure JSON structure is valid before saving
- Validate that user-selection updates only modify the intended question

---

## Step 4: Implement Web UI Questionnaire Form Renderer

Create a new questionnaire form component in the Active Prompt page that renders JSON questionnaires interactively.

**UI Components to implement in `.rdd/src/web/static/app.js`:**

1. **Questionnaire Form Renderer:**
   - Check if questionnaire file is `.json` or `.md`
   - For JSON: render interactive form
   - For MD: display as read-only text (existing behavior for old prompts)

2. **Accordion-style Question Display (Q5 answer B):**
   - Each question in a collapsible Bootstrap accordion panel
   - Question text as accordion header
   - Options rendered as radio buttons inside accordion body
   - Display pros/cons for each option
   - Show recommendation badge/alert with rationale

3. **Custom Answer Field (Q9 answer B):**
   - Always visible text input below radio options
   - Labeled "Custom answer (if none of the above options fit)"
   - When text is entered, automatically set user-selection type to "custom"

4. **Save Mechanism (Q7 answer A - immediate save on selection):**
   - Add onChange event listener to radio buttons and custom text field
   - Trigger API save immediately when user makes a selection
   - Show visual feedback (e.g., spinner, then checkmark) to indicate save status
   - Implement debouncing for custom text input (2-second delay) to avoid excessive saves while typing

5. **Validation (Q8 answer B - partial validation):**
   - Display warning badge for unanswered questions
   - Show overall completion percentage
   - Allow proceeding without answering all questions
   - No blocking validation

**Files to modify:**
- `.rdd/src/web/static/app.js` - add questionnaire form rendering functions
- `.rdd/src/web/static/style.css` - add styling for questionnaire form elements

---

## Step 5: Update Active Prompt Page UI Integration

Integrate the questionnaire form into the Active Prompt page, replacing the current text-based questionnaire display.

**Changes to Active Prompt Page:**
- Replace questionnaire.md textarea with dynamic renderer
- If `questionnaire.json` exists: render interactive form (Step 4)
- If `questionnaire.md` exists: show read-only markdown text (legacy support)
- If no questionnaire file exists: show "No questionnaire generated" message

**Tab/Section Updates:**
- Keep the "Questionnaire" tab in the prompt editor
- Load and detect file type (.json vs .md) dynamically
- Render appropriate UI based on file type

**Files to modify:**
- `.rdd/src/web/static/app.js` - update prompt editor questionnaire tab rendering
- `.rdd/src/web/templates/active-prompt.html` - ensure questionnaire section can host both form and text views

---

## Step 6: Update Prompt Creation to Initialize questionnaire.json

Ensure that when prompts are created, they initialize with `questionnaire.json` instead of `questionnaire.md`.

**Changes needed:**
- Modify `.rdd/src/actions/prompt_create.py` to create empty `questionnaire.json` file with initial structure:
  ```json
  {
    "context": "",
    "questions": []
  }
  ```
- Remove creation of `questionnaire.md` for new prompts

**Files to modify:**
- `.rdd/src/actions/prompt_create.py`

---

## Step 7: Test and Validate Implementation

**Testing checklist:**
1. Create a new prompt and verify `questionnaire.json` is created
2. Run analyze mode and verify questions are generated in JSON format
3. Open Active Prompt page and verify questionnaire form renders correctly
4. Select radio button options and verify immediate save to JSON file
5. Enter custom text and verify it saves after debounce delay
6. Verify old prompts with `questionnaire.md` still display as text
7. Verify completion percentage and warning badges update correctly
8. Test multiple questions with different answer types
9. Verify recommendation display and styling
10. Test browser refresh to ensure answers persist

---

## Step 8: Update Requirements File

Add new requirements to `.rdd-instance/specifications/requirements.md` following the conventions in `.rdd/conventions/requirements.convention.md`.

**User Requirements to add:**

- [UR-20260102-1300] The framework shall store questionnaire data in JSON format with structured fields for questions, options, pros/cons, recommendations, and user answers to enable programmatic parsing and interactive UI rendering.

- [UR-20260102-1301] The Web UI Active Prompt page shall display questionnaires as interactive forms with radio buttons for option selection, custom answer text inputs, and visual indicators for recommendations.

- [UR-20260102-1302] User answers to questionnaire questions shall be persisted immediately to the JSON file when selections are made, without requiring a manual save action.

- [UR-20260102-1303] The questionnaire form shall display pros and cons for each answer option, show recommended answers with rationale, and allow custom text answers when predefined options are insufficient.

- [UR-20260102-1304] The framework shall support both legacy markdown questionnaires (read-only display) and new JSON questionnaires (interactive forms) without requiring migration of historical data.

**Technical Requirements to add:**

- [TR-20260102-1300] Questionnaire JSON files shall follow the schema defined in `.rdd/conventions/questionnaire-json-schema.md` with root-level `context` and `questions` array fields.

- [TR-20260102-1301] Each question object in the JSON shall include: `id`, `question-text`, `options` array, `recommended-option`, `recommendation-rationale`, and `user-selection` object with `type` and `value` fields.

- [TR-20260102-1302] Question options shall be stored as an array of objects with `id`, `label`, `pros`, and `cons` fields for each option.

- [TR-20260102-1303] User selections shall be stored as an object with `type` field ("predefined", "custom", or null) and `value` field containing the selected option ID or custom text.

- [TR-20260102-1304] The Web UI shall render questionnaire forms using Bootstrap accordion components with individual panels for each question, displaying options as radio buttons with associated pros/cons text.

- [TR-20260102-1305] The questionnaire form shall implement immediate persistence using the existing `/api/file/save` endpoint, updating the entire JSON file when user selections change.

- [TR-20260102-1306] Custom answer text inputs shall use debounced auto-save with a 2-second delay to reduce file write operations during typing.

- [TR-20260102-1307] The analyze execution step in `.rdd/prompt-snippets/execution-step.analyze.md` shall generate questionnaire data in JSON format stored as `questionnaire.json` in the prompt's working folder.

- [TR-20260102-1308] The prompt creation script `.rdd/src/actions/prompt_create.py` shall initialize new prompts with an empty `questionnaire.json` file containing the base structure with empty context and questions array.

- [TR-20260102-1309] The Web UI Active Prompt page shall detect questionnaire file type (.json vs .md) and render interactive forms for JSON files while displaying markdown files as read-only text for legacy support.

**Location:** Add these requirements to the appropriate sections in `.rdd-instance/specifications/requirements.md`.

---

## Step 9: Update Documentation

Update the questionnaire formatting conventions to include JSON generation guidelines.

**Files to update:**
- `.rdd/conventions/questions-formatting.md` - Add section on JSON questionnaire generation
  - Document the JSON structure
  - Provide examples of well-formed JSON questionnaires
  - Explain field meanings and requirements
  - Include guidelines for writing effective pros/cons

---

## Step 10: Implementation Verification

After implementing all steps:

1. Verify all new files are created
2. Verify all modified files work correctly
3. Test end-to-end flow: create prompt → analyze → generate JSON questionnaire → answer in UI → verify persistence
4. Ensure no regressions in existing functionality
5. Verify legacy markdown questionnaires still work as read-only
6. Update implementation.md with actual implementation details

---

## Summary

This plan converts the questionnaire system from Markdown to JSON format while maintaining:
- All existing questionnaire attributes (questions, options, pros/cons, recommendations)
- User answer capability with both predefined selections and custom text
- Immediate persistence of user selections
- Backward compatibility for legacy markdown questionnaires (read-only)
- Clean separation between question definition and user answers
- Interactive form-based UI with accordion-style presentation

The implementation leverages existing infrastructure (API endpoints, UI components) and follows the framework's conventions for requirements documentation and file organization.
