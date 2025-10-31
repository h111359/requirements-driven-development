# Questions Formatting Guide

> Guidelines for generating user-friendly questions and requests for input in chat sessions.
> All RDD prompts should follow these formatting standards.

---

## Core Principles

1. **Clarity First**: Questions should be unambiguous and easy to understand
2. **Context Included**: Always provide enough context so the user knows why you're asking
3. **Options When Possible**: Offer predefined choices (A, B, C, D) for faster responses
4. **Allow Custom Input**: Always include "Other (please specify)" option
5. **Visual Structure**: Use formatting to make questions scannable
6. **Progressive Disclosure**: Ask one question at a time, or group related questions logically

---

## Question Format Templates

### Single Question (Basic)

```markdown
**Q: [Question text]?**

Please provide your answer:
```

### Single Question (With Options)

```markdown
**Q: [Question text]?**

Please choose one:
- **A)** [Option A description]
- **B)** [Option B description]
- **C)** [Option C description]
- **D)** Other (please specify)

Your choice: 
```

### Multiple Related Questions (Grouped)

```markdown
## [Topic/Category Name]

**Q1: [First question]?**
- **A)** [Option]
- **B)** [Option]
- **C)** Other (please specify)

**Q2: [Second question]?**
- **A)** [Option]
- **B)** [Option]

**Q3: [Third question]?**
[Open-ended question]

---
```

### Yes/No Confirmation

```markdown
**Confirm: [Action/Statement]?**

- ✓ **Yes** - [What happens if yes]
- ✗ **No** - [What happens if no]

Your choice:
```

### Clarification Request

```markdown
**ℹ️ Clarification Needed**

I need to understand [aspect] better before proceeding.

**Context:** [Brief explanation of why this matters]

**Question:** [Specific question]?

**Examples:**
- [Example 1]
- [Example 2]

Your answer:
```

---

## Formatting Standards

### Visual Hierarchy

Use markdown elements to create clear visual hierarchy:

```markdown
## Main Topic
**Q: Primary question?**
- **A)** Option A
- **B)** Option B

> **Note:** Additional context or important information

**Follow-up:** Secondary question if needed
```

### Symbols for Clarity

Use symbols to convey meaning quickly:

- **Q:** or **Question:** - For questions
- **ℹ️** - For information/context
- **⚠️** - For warnings or important notes
- **✓** - For confirmations/yes
- **✗** - For negations/no
- **→** - For indicating results or next steps
- **📝** - For notes or examples

### Option Formatting

**Preferred format for options:**

```markdown
- **A)** Short label - Detailed description
- **B)** Short label - Detailed description
- **C)** Short label - Detailed description
- **D)** Other (please specify)
```

**Alternative for complex options:**

```markdown
### Option A: [Name]
**Description:** [What this option means]
**Pros:** [Advantages]
**Cons:** [Disadvantages]

### Option B: [Name]
**Description:** [What this option means]
**Pros:** [Advantages]
**Cons:** [Disadvantages]
```

---

## Context Provision

Always provide context before asking questions:

```markdown
**Context**
[Explanation of what we're doing and why]

**Current Situation**
[What we know so far]

**Decision Needed**
**Q: [Question based on above context]?**
- **A)** [Option]
- **B)** [Option]
```

---

## Progressive Disclosure

### For Sequential Questions

```markdown
**Step 1 of 3: [Step name]**

Q: [First question]?
- A) [Option]
- B) [Option]

Once answered, I'll ask about [next topic].
```

### For Dependent Questions

```markdown
**Q1: [Primary question]?**
- A) [Option]
- B) [Option]

> **Note:** Your answer will determine the next questions.
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

**Context:** The workspace currently has files scattered across subdirectories. We need to decide on the structure for better maintainability.

**Q: How should we organize the workspace files?**

- **A)** Flat structure - All files directly in workspace/ folder
  - **Pros:** Simple, easy to access
  - **Cons:** Can become cluttered with many files
  
- **B)** Feature-based folders - Separate folder per feature
  - **Pros:** Organized, scalable
  - **Cons:** More complex navigation
  
- **C)** Hybrid approach - Main files flat, archives in subfolders
  - **Pros:** Balance of simplicity and organization
  - **Cons:** Requires consistent discipline
  
- **D)** Other approach (please describe)

**Recommendation:** Option A for projects with <10 active features simultaneously

Your choice:
```

---

## Handling Multiple Answers

When users provide multiple answers at once:

```markdown
**Thank you for your answers!**

Let me confirm my understanding:
- **Q1:** [Their answer to Q1]
- **Q2:** [Their answer to Q2]
- **Q3:** [Their answer to Q3]

Is this correct? (Yes/No)
```

---

## Handling Unclear Answers

```markdown
**⚠️ Clarification Needed**

I received: "[their answer]"

Could you please clarify by choosing one of these options:

- **A)** [Interpretation 1]
- **B)** [Interpretation 2]
- **C)** Neither - Let me rephrase: [space for their answer]

Or simply answer: [simpler version of the question]
```

---

## Summary Format

After collecting multiple answers:

```markdown
## 📋 Summary of Clarifications

**[Topic 1]**
- Question: [Q1]
- Answer: [A1]

**[Topic 2]**
- Question: [Q2]
- Answer: [A2]

**[Topic 3]**
- Question: [Q3]
- Answer: [A3]

✓ Ready to proceed? (Yes/No)
```

---

## Interactive Elements

### Progress Indicator

```markdown
**Clarification Progress: [3/7 questions answered]**

███████░░░░░░░░ 42%

Current: [Current topic]
Next: [Next topic]
```

### Checklist Format

```markdown
## Clarification Checklist

- [x] Problem statement
- [x] Acceptance criteria
- [ ] User roles
- [ ] Non-functional requirements
- [ ] Dependencies

**Next: Let's clarify the user roles...**
```

---

## Best Practices

1. **One Question Per Interaction** - Unless questions are tightly related
2. **Provide Context Always** - Users shouldn't need to guess why you're asking
3. **Offer Recommendations** - When you have expertise, suggest a preferred option
4. **Allow Escape Hatch** - Always allow "Other" or custom input
5. **Confirm Understanding** - Repeat back critical answers to ensure accuracy
6. **Show Progress** - Let users know where they are in a multi-question sequence
7. **Be Concise** - Use clear, direct language without unnecessary jargon
8. **Format for Skimming** - Use bold, bullets, and spacing for easy scanning

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

## Adaptation for Different Audiences

### For Technical Users
- Can use more technical terminology
- Provide deeper technical pros/cons
- Reference specific patterns/standards

### For Non-Technical Users
- Simplify language
- Use analogies and examples
- Focus on outcomes over implementation

### For Mixed Audiences
- Start simple, provide "technical details" in collapsible sections
- Use analogies alongside technical terms
- Offer both business and technical perspectives

---

## Version

- **Version:** 1.0
- **Last Updated:** 2025-10-31
- **Status:** Active
