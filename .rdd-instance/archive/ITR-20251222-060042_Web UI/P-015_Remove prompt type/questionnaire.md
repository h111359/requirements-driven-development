# Questionnaire for P-015: Remove prompt type

---

## ℹ️ Background

**Context:** Currently, the framework distinguishes between two types of prompts: "main" and "modification". The prompt type enforces different validation rules for the `parent-id` field:
- `main` prompts: parent-id must be null
- `modification` prompts: parent-id must reference an existing main prompt

The requirement is to remove this type distinction entirely.

**Current Implementation:**
- Type is prompted during prompt creation in CLI (`rdd.py` line 198)
- Type is stored in work-iteration-registry.json for each prompt
- Type is validated during prompt creation in `prompt_create.py` (lines 248-260)
- Type is used to enforce parent-id validation rules

---

## Questions

**Q1: What should happen to the parent-id validation after removing the type field?**

Please choose one:
- [x] **A)** Remove parent-id field entirely
  - **Pros:** Simplest solution, eliminates concept of prompt hierarchy
  - **Cons:** Loses ability to track prompt relationships and modifications
  
- [ ] **B)** Keep parent-id as optional for all prompts without type-based validation
  - **Pros:** Preserves prompt relationship tracking, simplifies validation logic
  - **Cons:** No enforcement of hierarchy rules, any prompt can reference any other prompt
  
- [ ] **C)** Keep parent-id with simplified validation (e.g., must reference existing prompt if provided)
  - **Pros:** Basic validation maintained, flexible hierarchy
  - **Cons:** Looser validation than current implementation
  
- [ ] **D)** Replace type-based validation with state-based validation (e.g., only completed prompts can be parents)
  - **Pros:** Maintains hierarchy rules, uses existing state field
  - **Cons:** More complex, state and parent-id become coupled
  
- [ ] **E)** Other approach (please describe):

**Recommendation:** Option B - Keep parent-id as optional without type-based validation. This preserves the ability to track prompt relationships while removing the artificial distinction between "main" and "modification" types.

---

**Q2: What should happen to existing prompts in work-iteration-registry.json that have a type field?**

Please choose one:
- [ ] **A)** Leave existing type fields as-is for backward compatibility
  - **Pros:** No migration needed, preserves historical data
  - **Cons:** Registry will have inconsistent format (some prompts with type, some without)
  
- [x] **B)** Remove type field from all existing prompts during next framework operation
  - **Pros:** Clean, consistent data format
  - **Cons:** Requires migration logic, loses historical type information
  
- [ ] **C)** Provide a one-time migration script to remove type from all prompts
  - **Pros:** Controlled migration, user-initiated
  - **Cons:** Extra step for users
  
- [ ] **D)** Archive current registry before migration and remove type from all prompts automatically
  - **Pros:** Safe migration with backup, automatic
  - **Cons:** Creates archive file
  
- [ ] **E)** Other approach (please describe):

**Recommendation:** Option B - Remove type field from all existing prompts automatically. The type information is not critical for historical analysis and keeping it would create inconsistency.

---

**Q3: Should the CLI prompt creation still ask for type parameter to maintain backward compatibility?**

Please choose one:
- [x] **A)** Remove type parameter completely from CLI
  - **Pros:** Clean implementation, enforces new model
  - **Cons:** Breaking change if users have scripts or workflows expecting it
  
- [ ] **B)** Keep type parameter in CLI but ignore it (for backward compatibility)
  - **Pros:** Non-breaking change for existing scripts
  - **Cons:** Confusing user experience (parameter is accepted but does nothing)
  
- [ ] **C)** Keep type parameter but show deprecation warning when used
  - **Pros:** Gradual transition, clear communication
  - **Cons:** More complex implementation
  
- [ ] **D)** Other approach (please describe):

**Recommendation:** Option A - Remove type parameter completely from CLI. This framework is in active development and not yet widely deployed, so a clean break is better than maintaining compatibility cruft.

---

**Q4: What should happen to the parent-id command-line parameter in prompt.create?**

Please choose one:
- [ ] **A)** Keep parent-id parameter as optional, no validation changes
  - **Pros:** Maintains current functionality
  - **Cons:** May allow invalid references
  
- [ ] **B)** Keep parent-id parameter with basic existence validation (must reference existing prompt-id)
  - **Pros:** Prevents broken references
  - **Cons:** Requires lookup logic
  
- [x] **C)** Remove parent-id parameter from prompt.create CLI
  - **Pros:** Simplifies interface
  - **Cons:** Loses ability to set parent relationship during creation
  
- [ ] **D)** Other approach (please describe):

**Recommendation:** Option B - Keep parent-id parameter with basic existence validation. This preserves the ability to track relationships while ensuring data integrity.

---

**Q5: Should there be any constraints on prompt-id references in parent-id field?**

Please choose one:
- [ ] **A)** No constraints - any prompt can reference any other prompt (even itself)
  - **Pros:** Maximum flexibility
  - **Cons:** Allows circular references and self-references
  
- [ ] **B)** Basic constraint - parent-id must reference existing prompt, cannot be self
  - **Pros:** Prevents obvious errors
  - **Cons:** Still allows circular references (A→B, B→A)
  
- [ ] **C)** Strict constraint - validate no circular references in parent chain
  - **Pros:** Maintains tree structure integrity
  - **Cons:** More complex validation logic
  
- [x] **D)** Other approach (please describe): parent-is should be removed

**Recommendation:** Option B - Basic constraint to prevent self-reference and require existing prompt. Circular references between different prompts are unlikely and don't cause functional issues.

---
