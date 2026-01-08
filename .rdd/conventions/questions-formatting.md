# Questions Formatting Guide

> Guidelines for generating user-friendly questions.
> All RDD prompts and questions in RDD generated questionnaires should follow these formatting standards.

---

## Core Principles

1. **Clarity First**: Questions should be unambiguous and easy to understand
2. **Context Included**: Always provide enough context so the user knows why you're asking
3. **Options When Possible**: Offer predefined choices (A, B, C, D) for faster responses
4. **Allow Custom Input**: Always include "Other (please specify)" option
5. **Visual Structure**: Use formatting to make questions scannable

---

## Question Format Templates

### Free Text Questions

```markdown
**Q: [Question text]?**

Please provide your answer:
```

### Questions With Predefined Options

```markdown
**Q: [Question text]?**

Please choose one:
- [ ] **A)** [Option A description, if meaningful - add pros and cons]
- [ ] **B)** [Option B description, if meaningful - add pros and cons]
- [ ] **C)** [Option C description, if meaningful - add pros and cons]
<add more options here if needed>
- [ ] **<the next upper letter after all predefined options are listed>)** Other (please specify): 
```

### Yes/No Confirmation

```markdown
**Confirm: [Action/Statement]?**

- [ ] **Yes** - [What happens if yes]
- [ ] **No** - [What happens if no]
```


## Formatting Standards

### Symbols for Clarity

Use symbols to convey meaning quickly:

- **Q:** or **Question:** - For questions
- **ℹ️** - For information/context
- **⚠️** - For warnings or important notes
- **✓** - For confirmations/yes
- **✗** - For negations/no
- **→** - For indicating results or next steps
- **📝** - For notes or examples


## Context Provision

Always provide context before asking questions:

```markdown
**Context**
[Explanation of what we're doing and why]

**Current Situation**
[What we know so far]
```
---


## Examples of Good vs. Bad Questions

### ❌ Bad Example

```
What do you want to do with the files?
```

**Problems:**
- No context
- Too vague
- No options
- Unclear scope

### ✅ Good Example

```markdown
**ℹ️ File Organization Decision**

**Context:** The workdir currently has files scattered across subdirectories. We need to decide on the structure for better maintainability.

**Q: How should we organize the workdir files?**

- [ ] **A)** Flat structure - All files directly in workdir/ folder
  - **Pros:** Simple, easy to access
  - **Cons:** Can become cluttered with many files
  
- [ ] **B)** Feature-based folders - Separate folder per feature
  - **Pros:** Organized, scalable
  - **Cons:** More complex navigation
  
- [ ] **C)** Hybrid approach - Main files flat, archives in subfolders
  - **Pros:** Balance of simplicity and organization
  - **Cons:** Requires consistent discipline
  
- [ ] **D)** Other approach (please describe)

**Recommendation:** Option A for projects with <10 active features simultaneously
```

---

## Best Practices

✅ **Provide Context Always** - Users shouldn't need to guess why you're asking
✅ **Offer Recommendations** - When you have expertise, suggest a preferred option
✅ **Allow Escape Hatch** - Always allow "Other" or custom input
✅ **Be Concise** - Use clear, direct language without unnecessary jargon
✅ **Format for Skimming** - Use bold, bullets, and spacing for easy scanning

---

## Anti-Patterns to Avoid

❌ **Multiple unrelated questions in one block** without clear separation
❌ **Asking questions without context** about why it matters
❌ **Providing options that are not mutually exclusive**
❌ **Using technical jargon** without explanation
❌ **Long paragraphs** without formatting breaks
❌ **No recommended option** when one clearly makes sense
❌ **Forgetting to allow custom input** (always include "Other")

---

## JSON Questionnaire Format (New)

Starting with the questionnaire JSON implementation, all new questionnaires are generated as `questionnaire.json` files following the schema defined in `.rdd/conventions/questionnaire-json-schema.md`.

### JSON Structure Overview

```json
{
  "context": "Background information about why these questions are being asked",
  "questions": [
    {
      "id": "Q1",
      "question-text": "The question being asked",
      "options": [
        {
          "id": "A",
          "label": "Option description",
          "pros": "Advantages of this option",
          "cons": "Disadvantages of this option"
        }
      ],
      "recommended-option": "A",
      "recommendation-rationale": "Why this option is recommended",
      "user-selection": {
        "type": null,
        "value": null
      }
    }
  ]
}
```

### Guidelines for JSON Questionnaires

When generating questionnaires in JSON format:

1. **Context Writing:**
   - Start with a 2-4 sentence summary explaining the prompt and purpose
   - Provide enough background so questions make sense
   - Keep it concise but informative

2. **Question IDs:**
   - Use sequential format: Q1, Q2, Q3, etc.
   - IDs must be unique within the questionnaire

3. **Option IDs:**
   - Use uppercase letters: A, B, C, D, etc.
   - IDs must be unique within each question
   - Typically provide 2-5 options per question

4. **Pros and Cons:**
   - Be specific and concrete
   - List actual benefits and drawbacks
   - Avoid vague or generic statements
   - Consider technical, maintainability, and UX aspects

5. **Recommendations:**
   - Base recommendations on analysis of the context
   - Provide clear rationale referencing specific pros/cons
   - Explain why this option fits the use case
   - Don't pick arbitrarily

6. **User Selection:**
   - Always initialize with `{"type": null, "value": null}`
   - Never pre-fill answers during generation
   - The Web UI will update this when user answers

7. **Custom Answers:**
   - The Web UI provides a text field for custom answers automatically
   - Users can provide free-text answers if predefined options don't fit
   - No need to add "Other" as an option in the JSON

### Example JSON Question

```json
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
    "type": null,
    "value": null
  }
}
```

### Legacy Markdown Questionnaires

Existing questionnaires in markdown format (questionnaire.md) will continue to be supported:
- They will be displayed as read-only text in the Web UI
- No migration is required
- New questionnaires will use JSON format
- The same content guidelines apply for both formats

See `.rdd/conventions/questionnaire-json-schema.md` for complete JSON schema documentation.
