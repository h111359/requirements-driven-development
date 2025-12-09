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

**Context:** The workspace currently has files scattered across subdirectories. We need to decide on the structure for better maintainability.

**Q: How should we organize the workspace files?**

- [ ] **A)** Flat structure - All files directly in workspace/ folder
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

