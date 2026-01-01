# Questionnaire - P-014: States Simplification

---

## Context

The current prompt requests to remove the `draft`, `planned`, and `in-progress` states and replace them with a single `active` state. This affects multiple components including scripts, Web UI, conventions, requirements, and execution logic. Several important implementation details need clarification to ensure correct and consistent changes across the system.

---

## Questions

### **Q1: What should be the default state when a new prompt is created?**

**Context:** Currently, new prompts are created in `draft` state by default. With the new model, there's only `active` and `completed`.

Please choose one:
- [x] **A)** New prompts should be created in `active` state
  - **Pros:** Simple, consistent with the requirement "New prompt shall be allowed to be created if all other prompts are in 'Completed' state"
  - **Cons:** Immediately activates the prompt which may not be intended
  
- [ ] **B)** New prompts should be created in `completed` state and then manually changed to `active`
  - **Pros:** Allows creation without immediate activation
  - **Cons:** Counter-intuitive to create a prompt as already completed
  
- [ ] **C)** Other approach (please specify):

**Recommendation:** Option A - creates prompt as `active` automatically

---

### **Q2: Should the `executed` flag remain in the system?**

**Context:** Currently, prompts have an `executed` field that tracks whether the prompt has been run. The completion operation checks if `state == "in-progress"` AND `executed == true` before allowing completion.

Please choose one:
- [x] **A)** Keep the `executed` flag unchanged
  - **Pros:** Maintains tracking of execution history; allows distinction between "active but not yet executed" and "active and executed"
  - **Cons:** Adds complexity to the simplified state model
  
- [ ] **B)** Remove the `executed` flag completely
  - **Pros:** Simplifies the model even further
  - **Cons:** Loses execution tracking information; no way to know if an active prompt was ever executed
  
- [ ] **C)** Rename `executed` to something else (please specify what):

**Recommendation:** Option A - keep execution tracking for historical purposes

---

### **Q3: How should the completion button behavior change in the Web UI?**

**Context:** Currently, the completion button is enabled only for prompts with `state == "in-progress"` AND `executed == true`. With the new simplified states, we need to decide the completion criteria.

Please choose one:
- [ ] **A)** Complete button enabled for any `active` prompt (regardless of `executed` flag)
  - **Pros:** Simple, consistent with simplified state model
  - **Cons:** Users might accidentally complete prompts they haven't executed yet
  
- [x] **B)** Complete button enabled only for `active` prompts with `executed == true`
  - **Pros:** Prevents accidental completion of non-executed prompts
  - **Cons:** Requires keeping the `executed` flag (see Q2)
  
- [ ] **C)** Add a confirmation dialog when completing non-executed prompts
  - **Pros:** Provides safety while allowing flexibility
  - **Cons:** Adds UI complexity
  
- [ ] **D)** Other approach (please specify):

**Recommendation:** Option B if `executed` flag is kept (Q2-A), otherwise Option A

---

### **Q4: Should analyze-enabled and plan-enabled flags have state restrictions?**

**Context:** Currently, the convention states that `analyze-enabled` and `plan-enabled` can only be set to `true` for prompts with state `draft`, `planned`, or `in-progress`. With only `active` and `completed` states, we need to decide the new rules.

Please choose one:
- [x] **A)** These flags can only be set to `true` for `active` prompts (not for `completed`)
  - **Pros:** Logical - you can't analyze/plan a completed prompt
  - **Cons:** Restricts flexibility
  
- [ ] **B)** These flags can be set to `true` for any state
  - **Pros:** Maximum flexibility; allows re-analyzing completed prompts if needed
  - **Cons:** May lead to inconsistent states
  
- [ ] **C)** Remove these flags and use a different mechanism
  - **Pros:** Simplifies the model further
  - **Cons:** Loses current functionality
  
- [ ] **D)** Other approach (please specify):

**Recommendation:** Option A - restrict to `active` prompts only

---

### **Q5: How should historical/completed prompts be displayed in the Web UI?**

**Context:** The Web UI currently shows different badge colors for different states (Draft=secondary/gray, Planned=info/blue, In Progress=primary/blue, Completed=success/green). With only two states, the visual distinction will be simpler.

Please choose one:
- [ ] **A)** Active=primary/blue, Completed=success/green
  - **Pros:** Clear distinction, uses standard Bootstrap colors
  - **Cons:** None
  
- [x] **B)** Active=warning/yellow, Completed=success/green
  - **Pros:** Yellow draws attention to active work
  - **Cons:** Yellow often indicates warnings/problems
  
- [ ] **C)** Active=info/blue, Completed=secondary/gray
  - **Pros:** Grays out completed items
  - **Cons:** Less celebratory for completed work
  
- [ ] **D)** Other color scheme (please specify):

**Recommendation:** Option A - standard blue for active, green for completed

---

### **Q6: Should prompt creation validate the "only one active prompt" rule?**

**Context:** The prompt creation script needs to validate that no other prompt is in `active` state when creating a new `active` prompt, similar to how it currently validates for `planned` or `in-progress`.

Please choose one:
- [x] **A)** Yes - strictly enforce only one active prompt at a time
  - **Pros:** Maintains clear focus; prevents confusion about which prompt to execute
  - **Cons:** Requires completing or deactivating the current active prompt before starting a new one
  
- [ ] **B)** No - allow multiple active prompts
  - **Pros:** More flexibility for parallel work
  - **Cons:** Loses the "single active prompt" concept that drives the execution model
  
- [ ] **C)** Warn but allow multiple active prompts
  - **Pros:** Balance between flexibility and guidance
  - **Cons:** Introduces ambiguity in the execution model
  
- [ ] **D)** Other approach (please specify):

**Recommendation:** Option A - maintain the single active prompt rule

---

### **Q7: Should the prompt set_state command allow all state transitions?**

**Context:** Currently, `prompt_set_state.py` allows setting any state. With the simplified model, we might want to enforce specific transitions.

Please choose one:
- [x] **A)** Allow any transition (active ↔ completed)
  - **Pros:** Maximum flexibility; allows reopening completed prompts
  - **Cons:** May lead to messy workflow
  
- [ ] **B)** Only allow active → completed (one-way transition)
  - **Pros:** Clean workflow; completed prompts stay completed
  - **Cons:** Cannot reopen a prompt if needed
  
- [ ] **C)** Allow completed → active only with confirmation/warning
  - **Pros:** Allows reopening with safeguards
  - **Cons:** Adds complexity
  
- [ ] **D)** Other approach (please specify):

**Recommendation:** Option A - allow bidirectional transitions for maximum flexibility

---

### **Q8: How should error messages be updated?**

**Context:** Many scripts have error messages referring to `"state='planned' or 'in-progress'"`. These need to be updated to reflect the new state model.

Please choose one:
- [x] **A)** Update all error messages to refer to `"state='active'"`
  - **Pros:** Accurate and consistent with new model
  - **Cons:** None
  
- [ ] **B)** Keep generic messages without mentioning specific states
  - **Pros:** More maintainable if states change again
  - **Cons:** Less helpful to users
  
- [ ] **C)** Other approach (please specify):

**Recommendation:** Option A - be explicit and accurate

---

## Additional Notes

**ℹ️ Impact Analysis:**

This change will affect:
- **Python scripts:** ~10 files in `.rdd/src/actions/` and `.rdd/src/rdd.py`
- **Web UI:** HTML templates and JavaScript app logic
- **Conventions:** `work-iteration-registry.convention.md` and related docs
- **Requirements:** Definition of "active prompt" in requirements.md
- **Execution logic:** Prompt snippets referring to states

**⚠️ Important Considerations:**

1. All changes must be synchronized across Python, JavaScript, and documentation
2. Existing JSON data in work-iteration-registry.json needs to handle migration
3. Tests may need to be updated to reflect new states
4. Git commit messages and release notes should document this breaking change
