# Questionnaire JSON Schema Convention

## Overview

This document defines the JSON schema for questionnaire files in the RDD framework. Questionnaires are generated during the analyze execution step to help clarify design decisions and collect user preferences for prompt implementation.

## File Location

- **File name:** `questionnaire.json`
- **Location:** Inside the prompt's working folder at `.rdd-instance/workdir/<PROMPT-ID>_<PROMPT-TITLE>/questionnaire.json`

## JSON Structure

```json
{
  "context": "string - descriptive context about the prompt and purpose of the questionnaire",
  "questions": [
    {
      "id": "string - question identifier (Q1, Q2, Q3, etc.)",
      "question-text": "string - the question text",
      "options": [
        {
          "id": "string - option identifier (A, B, C, D, etc.)",
          "label": "string - descriptive label for the option",
          "pros": "string - advantages and benefits of choosing this option",
          "cons": "string - disadvantages and drawbacks of choosing this option"
        }
      ],
      "recommended-option": "string - ID of the recommended option (e.g., 'A', 'B')",
      "recommendation-rationale": "string - explanation for why this option is recommended",
      "user-selection": {
        "type": "string|null - 'predefined', 'custom', or null if unanswered",
        "value": "string|null - option ID (e.g., 'A') for predefined, custom text for custom, or null if unanswered"
      }
    }
  ]
}
```

## Field Descriptions

### Root Level

- **context** (required): Provides background information about the prompt and explains why these questions are being asked. Helps the user understand the context before answering.

- **questions** (required): Array of question objects. Each question represents a design decision or preference that needs user input.

### Question Object

- **id** (required): Unique identifier for the question within the questionnaire. Format: `Q1`, `Q2`, `Q3`, etc. Used for programmatic access and reference.

- **question-text** (required): The actual question being asked. Should be clear, concise, and focused on a single decision point.

- **options** (required): Array of possible answer options. Each option represents a different approach or choice for the question.

- **recommended-option** (required): The ID of the option that is recommended based on analysis. Helps guide the user toward a reasonable default choice.

- **recommendation-rationale** (required): Explanation of why the recommended option is suggested. Should provide clear reasoning to help the user make an informed decision.

- **user-selection** (required): Object containing the user's answer to the question. Initially null when the questionnaire is generated.

### Option Object

- **id** (required): Unique identifier for the option within the question. Format: `A`, `B`, `C`, `D`, etc.

- **label** (required): Description of what this option represents. Should be clear and comprehensive enough that the user understands the choice.

- **pros** (required): Advantages, benefits, and positive aspects of choosing this option. Helps the user understand when this option is appropriate.

- **cons** (required): Disadvantages, drawbacks, and limitations of choosing this option. Helps the user understand potential trade-offs.

### User Selection Object

- **type** (required): Indicates the kind of answer provided:
  - `null`: Question has not been answered yet
  - `"predefined"`: User selected one of the predefined options
  - `"custom"`: User provided a custom text answer

- **value** (required): The actual answer value:
  - `null`: Question has not been answered yet
  - Option ID (e.g., `"A"`, `"B"`): User selected this predefined option
  - Custom text string: User provided a custom answer

## Example

```json
{
  "context": "The current logging system uses print statements scattered throughout the codebase. This questionnaire helps decide how to implement a proper logging framework for better debugging and monitoring.",
  "questions": [
    {
      "id": "Q1",
      "question-text": "Which logging library should be used for the project?",
      "options": [
        {
          "id": "A",
          "label": "Python standard library logging module",
          "pros": "Built-in, no external dependencies, widely known, comprehensive features",
          "cons": "More verbose configuration, steeper learning curve for basic usage"
        },
        {
          "id": "B",
          "label": "loguru library",
          "pros": "Simple API, automatic formatting, better error handling, easier to configure",
          "cons": "External dependency, less familiar to some developers"
        },
        {
          "id": "C",
          "label": "structlog library",
          "pros": "Structured logging, excellent for JSON output, great for log aggregation systems",
          "cons": "External dependency, overkill for simple projects, more complex setup"
        }
      ],
      "recommended-option": "A",
      "recommendation-rationale": "The standard library logging module is recommended because it requires no external dependencies, is well-documented, and provides all necessary features for this project's scope. It's the most maintainable choice for a framework that aims to minimize dependencies.",
      "user-selection": {
        "type": "predefined",
        "value": "A"
      }
    },
    {
      "id": "Q2",
      "question-text": "What should be the default logging level for the application?",
      "options": [
        {
          "id": "A",
          "label": "DEBUG",
          "pros": "Maximum visibility, helpful during development, catches everything",
          "cons": "Very verbose output, performance impact, cluttered logs in production"
        },
        {
          "id": "B",
          "label": "INFO",
          "pros": "Balanced verbosity, shows important events, good for production monitoring",
          "cons": "May miss some debug details, not ideal for troubleshooting complex issues"
        },
        {
          "id": "C",
          "label": "WARNING",
          "pros": "Minimal noise, focuses on problems, clean production logs",
          "cons": "Misses informational events, harder to trace normal operation flow"
        }
      ],
      "recommended-option": "B",
      "recommendation-rationale": "INFO level provides the best balance between visibility and noise. It captures important application events without overwhelming the logs, making it suitable for both development and production environments.",
      "user-selection": {
        "type": null,
        "value": null
      }
    }
  ]
}
```

## Validation Rules

1. **Required Fields:** All fields marked as required must be present in the JSON.

2. **ID Format:** 
   - Question IDs must follow the pattern `Q<number>` (e.g., Q1, Q2)
   - Option IDs must be single uppercase letters (A, B, C, D, etc.)

3. **Recommended Option:** The `recommended-option` value must match one of the option IDs in the `options` array.

4. **User Selection Type:** Must be one of: `null`, `"predefined"`, or `"custom"`.

5. **User Selection Value:**
   - If type is `null`, value must be `null`
   - If type is `"predefined"`, value must match one of the option IDs
   - If type is `"custom"`, value must be a non-empty string

6. **Consistency:** Each question must have at least 2 options.

## Usage Guidelines

### For AI Agents Generating Questionnaires

1. **Context Writing:**
   - Start with a brief summary of what the prompt is about
   - Explain why these questions need to be asked
   - Keep it concise but informative (2-4 sentences)

2. **Question Writing:**
   - Focus each question on a single decision point
   - Make questions specific and actionable
   - Avoid compound questions that mix multiple concerns
   - Use clear, simple language

3. **Option Writing:**
   - Provide 2-5 options per question (typically 3-4)
   - Make options mutually exclusive
   - Write clear, descriptive labels
   - Be balanced in presenting pros and cons
   - Don't bias the options through wording

4. **Pros and Cons:**
   - List concrete, specific benefits and drawbacks
   - Avoid generic or vague statements
   - Consider technical, maintainability, and user experience aspects
   - Be honest about limitations

5. **Recommendations:**
   - Base recommendations on analysis of the specific context
   - Provide clear rationale that references specific pros/cons
   - Don't just pick arbitrarily—explain the reasoning
   - It's okay to recommend different options for different questions

6. **Initialization:**
   - Always initialize `user-selection` with `{"type": null, "value": null}`
   - Never pre-fill user answers during generation

### For Web UI Implementation

1. **Rendering:**
   - Display context at the top of the form
   - Render each question in a collapsible accordion or card
   - Show options as radio buttons with visible pros/cons
   - Highlight the recommended option with a badge or visual indicator
   - Provide a text input for custom answers

2. **User Interaction:**
   - When user selects a radio button, set `type: "predefined"` and `value: <option-id>`
   - When user enters custom text, set `type: "custom"` and `value: <custom-text>`
   - Implement auto-save on selection change
   - Use debouncing (2 seconds) for custom text input to avoid excessive saves

3. **Validation:**
   - Show visual indicators for answered vs. unanswered questions
   - Display completion percentage
   - Allow proceeding with unanswered questions (non-blocking)

## Migration and Compatibility

- **Legacy Markdown Files:** Existing `questionnaire.md` files from previous prompts will remain in markdown format. The Web UI should detect file extension and render markdown files as read-only text.

- **New Questionnaires:** All new questionnaires generated by the analyze step should use this JSON format.

- **No Automatic Migration:** Do not automatically convert existing markdown questionnaires to JSON. Historical data remains in its original format.

## Related Files

- `.rdd/prompt-snippets/execution-step.analyze.md` - Instructions for generating questionnaires
- `.rdd/conventions/questions-formatting.md` - Guidelines for question content and style
- `.rdd/src/web/static/app.js` - Web UI implementation for questionnaire rendering
- `.rdd/src/actions/prompt_create.py` - Script that initializes questionnaire.json for new prompts
