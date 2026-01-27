# Analysis: Conditional Visibility Enhancement

## Copilot Review

### Current State Assessment

The current Technical Design Schema Editor uses a simple textarea field for setting conditional visibility (`visibleWhen`), requiring users to manually write JavaScript-like expressions or JSON arrays. This approach has several issues:

1. **High error potential**: Manual text entry is prone to syntax errors, typos, and invalid references to question IDs
2. **Poor discoverability**: Users must remember exact question IDs and understand the expression syntax
3. **No validation**: The current implementation provides no immediate feedback on whether the expression is valid
4. **Steep learning curve**: New users must study examples to understand the format

### Impact on Existing Functionality

The enhancement will affect:
- **Technical Design Schema Editor** (`tech_design_schema_editor/`): Core UI/UX changes required
- **Schema validation logic**: New validation patterns needed for structured visibility rules
- **Existing schemas**: Must ensure backward compatibility with current `visibleWhen` format (both string expressions and array-based conditions)

### Risks and Challenges

1. **Complexity of UI controls**: Building intuitive inputs for nested conditional logic (AND/OR operators, multiple conditions) is non-trivial
2. **Backward compatibility**: Must handle existing schemas that use string-based JavaScript expressions like `answers["QuestionID"] === "Value"`
3. **Migration path**: Need clear strategy for converting existing expressions to new format
4. **Testing burden**: Complex conditional logic requires comprehensive test coverage
5. **Question ID references**: Need a picker/autocomplete to select valid question IDs
6. **Value validation**: Need to validate that condition values match the target question's options

### Completeness Assessment

The prompt is **incomplete** in these areas:
- No specification of which condition operators to support (equals, not equals, contains, etc.)
- No guidance on AND/OR combination of multiple conditions
- No mention of whether nested conditions are needed
- No indication of whether to preserve backward compatibility with string expressions
- No UI/UX mockup or detailed description of the "convenient input elements"

## Best Practices

### Research Sources

**1. Conditional Logic in Form Builders**

Source: [JotForm Conditional Logic](https://www.jotform.com/help/148-using-conditional-logic/)
- Best practice: Use visual rule builders with dropdown selections
- Pattern: IF [field] [operator] [value] THEN [action]
- Supports AND/OR grouping for multiple conditions
- Provides immediate visual feedback on active rules

**2. Survey Platforms (Typeform, SurveyMonkey)**

Source: [Typeform Logic Jumps](https://www.typeform.com/help/a/conditional-logic-360029573471/)
- Best practice: Show/hide logic should be simple and visual
- Pattern: Drag-and-drop condition builders
- Display preview of affected questions in real-time
- Limit nesting depth to prevent user confusion

**3. JSON Schema Conditional Validation**

Source: [JSON Schema if/then/else](https://json-schema.org/understanding-json-schema/reference/conditionals.html)
- Best practice: Structured condition objects rather than string expressions
- Pattern: Use structured format like `{"if": {...}, "then": {...}}`
- Supports schema-based validation of condition structure
- Easier to parse and validate programmatically

**4. UI Pattern Libraries**

Source: [Atlassian Design System - Rules Builder](https://atlassian.design/)
- Best practice: Rule builder UI with add/remove condition rows
- Pattern: Each row has [Field] [Operator] [Value] with + and - buttons
- Support AND/OR toggle at group level
- Clear visual hierarchy for condition groups

### Key Takeaways

1. **Visual builder over text input**: Industry standard is dropdown-based builders, not text fields
2. **Structured data format**: JSON-based condition objects beat string expressions
3. **Real-time validation**: Immediate feedback prevents invalid configurations
4. **Limited complexity**: Most tools limit nesting to 2-3 levels to maintain usability
5. **Autocomplete/pickers**: Essential for selecting field names and valid values

## Proposals

### Option 1: Simple Condition Builder (Recommended)

**Description**: Replace the textarea with a structured UI for building basic conditions

**Features**:
- Row-based condition builder: each row is [Question] [Operator] [Value]
- Supported operators: equals, not equals, contains (for multiselect)
- AND-only logic between conditions (OR requires multiple visibleWhen rules)
- Question ID picker with search/filter
- Value picker showing valid options from the referenced question
- Live preview showing when the question would be visible

**Pros**:
- Easier to implement than full expression parser
- Covers 95% of use cases based on current schema analysis
- Lower maintenance burden
- Better UX than text field
- Easy to validate

**Cons**:
- Less flexible than full expression language
- Cannot express complex OR logic in single rule

**Changes to Schema Format**:
```json
{
  "visibleWhen": [
    {
      "questionId": "Product_PrimaryProductCategory",
      "operator": "equals",
      "value": "Mobile application"
    },
    {
      "questionId": "Infra_UsesVNet",
      "operator": "contains",
      "value": "Single VNet"
    }
  ]
}
```

### Option 2: Full Expression Builder

**Description**: Support complex conditional logic with AND/OR groups and nesting

**Features**:
- Tree-based condition builder with groups
- Support AND/OR operators between conditions and groups
- Nesting up to 2 levels
- Visual tree representation of logic
- Expression preview in human-readable format

**Pros**:
- Handles all possible conditional scenarios
- Future-proof for complex requirements
- Professional-grade solution

**Cons**:
- Complex implementation
- Higher risk of user errors
- Requires sophisticated UI components
- More difficult to test and maintain
- May overwhelm users for simple cases

### Option 3: Hybrid Approach (Best of Both Worlds)

**Description**: Start with simple builder (Option 1), keep advanced mode for complex cases

**Features**:
- Default: Simple condition builder (Option 1)
- "Advanced" toggle: Shows textarea for complex expressions
- Auto-convert simple conditions to structured format
- Manual expressions stored as strings, validated on save

**Pros**:
- Serves both simple and complex use cases
- Gradual migration path
- Maintains backward compatibility
- Doesn't force migration of existing complex expressions

**Cons**:
- Dual maintenance burden
- Users might default to text mode instead of learning builder
- More complex codebase

### Requirement Modifications Suggested

1. **Add UR-0024-A**: The Technical Design Schema Editor shall provide a visual condition builder UI for setting question visibility rules, with dropdowns for question selection, operator selection, and value selection, replacing the current text-based input.

2. **Add UR-0024-B**: The condition builder shall validate question ID references in real-time and only allow valid values based on the referenced question's option set.

3. **Add UR-0024-C**: The schema shall support backward compatibility with existing string-based visibleWhen expressions while encouraging migration to structured format through the UI.

4. **Add TR-XXXX**: The visibleWhen condition format shall use structured JSON objects with fields: questionId, operator, value, supporting operators: equals, notEquals, contains, notContains.

## Prompt Modification

I would write this prompt as follows:

---

**Title**: Enhance Conditional Visibility with Visual Rule Builder

**Context**:
The Technical Design Schema Editor currently uses a plain textarea for configuring conditional visibility (`visibleWhen`), which requires users to manually write JSON expressions. This is error-prone and not user-friendly.

**Goal**:
Replace the `visibleWhen` textarea with a visual rule builder that makes it easy to create and manage visibility conditions without writing JSON manually.

**Requirements**:

1. **UI Component**: Create a condition builder interface with the following features:
   - Add/remove condition rows using + and - buttons
   - Each row contains three dropdowns:
     - Question selector (searchable, shows question labels with IDs)
     - Operator selector (equals, not equals, contains, not contains)
     - Value selector (populated from the selected question's options)
   - AND-only logic between conditions (all conditions must be true)
   - Display count of active conditions
   - Show/hide toggle to collapse the builder when not in use

2. **Question Selector**: 
   - Populate from all questions in the schema
   - Show format: "Category: Question Label (QuestionID)"
   - Include search/filter capability
   - Exclude the current question being edited

3. **Value Selector**:
   - For radio/dropdown: show all option labels
   - For multiselect: show all option labels (condition checks if array contains value)
   - For text/textarea/number: provide text input for free-form value
   - For checkbox: show "true" / "false" options

4. **Validation**:
   - Prevent circular references (Question A depends on Question B which depends on Question A)
   - Warn if referenced question doesn't exist
   - Warn if value doesn't match any options (for radio/dropdown/multiselect)
   - Highlight validation errors in red with clear messages

5. **Data Format**:
   - Store conditions as structured JSON array:
     ```json
     {
       "visibleWhen": [
         {"questionId": "Q1", "operator": "equals", "value": "Option1"},
         {"questionId": "Q2", "operator": "contains", "value": "Option2"}
       ]
     }
     ```

6. **Backward Compatibility**:
   - Support reading existing string expressions (legacy format)
   - Show legacy expressions in read-only textarea with warning message
   - Provide "Convert to Builder" button to attempt automatic conversion
   - If conversion fails, allow manual recreation in builder

7. **Auto-save**:
   - Maintain existing auto-save behavior
   - Save on blur events from dropdowns and inputs
   - Show saved indicator

8. **Analyze Mode Deliverable**:
   - Create an HTML demo file `conditional-visibility-demo.html` in the prompt workdir
   - Demo should show:
     - Example 1: Simple single condition (if Product Type = Mobile, show Mobile Platform question)
     - Example 2: Multiple AND conditions (if Cloud = Azure AND Region = US, show Compliance options)
     - Example 3: Multiselect contains check (if Features contains "AI/ML", show ML Platform question)
     - Include both the JSON format and a visual representation of each example
     - Provide code snippets for the UI components

**Out of Scope**:
- OR logic between conditions (future enhancement)
- Nested condition groups (future enhancement)
- Complex expressions with functions or calculations

**Success Criteria**:
- Users can create basic visibility rules without writing JSON
- Validation prevents common errors (invalid IDs, wrong values)
- Existing schemas with visibleWhen expressions continue to work
- Demo file clearly illustrates the different condition types

---

This revised prompt is more specific, includes clear requirements for UI components, data formats, validation, and backward compatibility. It also properly scopes the work and provides concrete success criteria.
