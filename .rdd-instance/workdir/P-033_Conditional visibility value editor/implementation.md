# Implementation Log: P-033 Conditional Visibility Value Editor

**Prompt:** The value editor in "Conditional Visibility" in "Technical Design Schema Editor" should reflect the type of the corresponding question and represent text value as text field, radio as radio, multiselect as multiselect and so on.

**Implementation Date:** 2026-01-25

## Context

### Relevant Technical Design
- **Infrastructure - Deployment Model:** Public cloud

### Relevant Requirements
- **UR-0024:** The technical-design configuration JSON shall support conditional and hierarchical logic, enabling form fields to appear or change behavior based on previously selected answers.
- **UR-0025:** The Web UI shall provide a Technical Specification page for editing of technical-design.

### Relevant Files and Folders
- **tech_design_schema_editor/**: Standalone web-based editor for technical design schema
  - **static/app.js**: Client-side JavaScript application
  - **static/style.css**: Styles for the editor
  - **index.html**: Main HTML page

### Questionnaire Decisions
Based on the answered questionnaire, the following decisions were made:

**Q1: UI Control Type Matching**
- **Decision:** Option A - Match exact control type
- **Rationale:** Use radio buttons for radio questions, checkboxes for multiselect questions, and appropriate controls for each question type for better intuitiveness and consistency.

**Q2: Non-Option Question Types**
- **Decision:** Option B - Add type-specific input controls
- **Rationale:** Provide type-specific controls (number input for number fields, checkbox for checkbox fields, etc.) for better user experience and validation.

**Q3: Display Format for Options**
- **Decision:** Option A - Display labels only
- **Rationale:** More user-friendly and readable, matching what users see when answering questions.

## Implementation Steps

### 1. Modified `updateConditionValueField` Function
**File:** [tech_design_schema_editor/static/app.js](tech_design_schema_editor/static/app.js)

Updated the function to create appropriate UI controls based on the referenced question type:

- **For multiselect questions:** Generate checkboxes instead of multi-select dropdown
- **For radio questions:** Generate radio buttons instead of single-select dropdown  
- **For dropdown questions:** Keep dropdown control (most appropriate for this type)
- **For number questions:** Use `<input type="number">` with proper validation
- **For checkbox questions:** Use single checkbox with true/false value
- **For text/textarea questions:** Use text input fields

### 2. Modified `createConditionRow` Function
**File:** [tech_design_schema_editor/static/app.js](tech_design_schema_editor/static/app.js)

Updated the function to apply the same control type matching logic when creating new condition rows. This ensures consistency between initial row creation and dynamic updates.

### 3. Added New Event Handlers
**File:** [tech_design_schema_editor/static/app.js](tech_design_schema_editor/static/app.js)

Implemented four new event handler functions:

- **`handleConditionValueChangeCheckbox(event, index)`**: Handles checkbox changes for multiselect questions, collecting all checked values into an array
- **`handleConditionValueChangeRadio(event, index)`**: Handles radio button selection for radio questions, storing the single selected value
- **`handleConditionValueChangeCheckboxSingle(event, index)`**: Handles single checkbox toggle for checkbox-type questions, storing 'true' or 'false'
- Updated existing handlers remain for dropdown and text input compatibility

### 4. Updated Event Listener Attachment
**File:** [tech_design_schema_editor/static/app.js](tech_design_schema_editor/static/app.js)

Modified the event listener attachment code in `createConditionRow` to:
- Detect which type of control was created (checkboxes, radios, single checkbox, dropdown, or input)
- Attach the appropriate event handler based on the control type
- Ensure all controls properly trigger the save operation

### 5. Added CSS Styles
**File:** [tech_design_schema_editor/static/style.css](tech_design_schema_editor/static/style.css)

Added styling for the new checkbox and radio button controls:

- **`.condition-value-checkboxes, .condition-value-radios`**: Container styles with max-height, scrolling, border, and padding
- **`.form-check`**: Layout for individual checkbox/radio items
- **`.form-check-input`**: Styling for checkbox and radio inputs
- **`.form-check-label`**: Styling for labels with proper cursor and sizing

## Technical Details

### Control Type Mapping

| Question Type | Value Editor Control | Storage Format |
|--------------|---------------------|----------------|
| radio | Radio buttons | Single option ID (string) |
| multiselect | Checkboxes | Array of option IDs |
| dropdown | Dropdown select | Single option ID (string) |
| number | Number input | Number value (string) |
| checkbox | Single checkbox | 'true' or 'false' (string) |
| text | Text input | Text value (string) |
| textarea | Text input | Text value (string) |

### Implementation Approach

1. **Type Detection:** The implementation detects the question type by looking up the question in the schema using `getQuestionById()`
2. **Dynamic Rendering:** Value fields are rendered dynamically based on the detected type
3. **Event Handling:** Different event handlers capture values appropriately for each control type
4. **Data Consistency:** All controls store values in the same condition object format for backend compatibility

### Key Functions Modified

1. **`updateConditionValueField(index, questionId)`** (~160 lines)
   - Dynamically updates the value field when question selection changes
   - Creates appropriate control based on question type
   - Attaches correct event handlers

2. **`createConditionRow(condition, index)`** (~120 lines) 
   - Creates initial condition row with proper controls
   - Handles pre-selected values for existing conditions
   - Attaches all necessary event listeners

3. **Event Handlers** (~80 lines total)
   - `handleConditionValueChangeCheckbox`: Array collection from checkboxes
   - `handleConditionValueChangeRadio`: Single value from radio group
   - `handleConditionValueChangeCheckboxSingle`: Boolean from checkbox
   - Existing handlers retained for backward compatibility

## Testing Notes

The implementation maintains backward compatibility with existing condition data:
- Existing conditions with dropdown values continue to work
- Array values for multiselect are properly handled whether from old multi-select dropdowns or new checkboxes
- Single values for radio/dropdown questions work with both old and new controls

## Alignment with Requirements

This implementation directly addresses:
- **UR-0024:** Enhanced conditional visibility with type-appropriate controls
- **UR-0025:** Improved Technical Design page editing experience

The implementation follows the questionnaire decisions:
- **Q1 (Control Type Matching):** ✅ Implemented radio buttons for radio questions, checkboxes for multiselect
- **Q2 (Type-Specific Controls):** ✅ Implemented number input, checkbox controls for non-option types
- **Q3 (Display Labels):** ✅ All option-based controls display labels while storing IDs internally

## Commands Executed

No requirement management scripts were executed as this is a UI enhancement that doesn't require changes to the requirements specification. The existing requirements adequately cover the conditional visibility functionality.

## Files Modified

1. `/home/hromar/Desktop/vscode/requirements-driven-development/tech_design_schema_editor/static/app.js` - JavaScript logic for value editors
2. `/home/hromar/Desktop/vscode/requirements-driven-development/tech_design_schema_editor/static/style.css` - Styling for new controls

## Conclusion

The implementation successfully enhances the conditional visibility value editor to reflect the type of the corresponding question. Users now see intuitive, type-appropriate controls when setting up conditional visibility rules, improving the overall user experience of the Technical Design Schema Editor.
