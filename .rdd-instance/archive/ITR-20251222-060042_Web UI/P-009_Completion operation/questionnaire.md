# Questionnaire for P-009: Completion Operation

**ℹ️ Context**

This questionnaire addresses ambiguities in the completion operation requirements. The prompt requires:
1. A new `prompt_complete.py` script to set prompts to "completed" state
2. Git operations integration based on a registry flag
3. An "executed" flag mechanism with a separate `prompt_set_executed_on.py` script
4. A Web UI button that executes the complete action

---

## Questions

**Q1: Where should the git operations enabled flag be stored in the registry?**

**ℹ️ Context:** The prompt states "In `.rdd-instance/workdir/work-iteration-registry.json` shall be added a key if git operations are enabled." This could be at different levels in the JSON structure.

Please choose one:
- [x] **A)** At the root level of the registry (alongside `iteration-id`, `iteration-name`, etc.)
  - **Pros:** Global setting, easy to access, applies to all prompts
  - **Cons:** Less flexibility if different prompts need different behavior
  
- [ ] **B)** Within each prompt object (alongside `prompt-id`, `state`, etc.)
  - **Pros:** Granular control per prompt, more flexible
  - **Cons:** More complex to maintain, redundant data
  
- [ ] **C)** In a separate configuration section within the registry
  - **Pros:** Organized configuration management, clear separation of concerns
  - **Cons:** Additional JSON structure complexity
  
- [ ] **D)** Other (please specify): 

**Recommendation:** Option A for simplicity and global application

---

**Q2: What should be the exact name and format of the git operations flag?**

Please choose one:
- [ ] **A)** `"git-operations-enabled": true/false`
  - **Pros:** Clear, follows existing naming convention with hyphens
  - **Cons:** None
  
- [x] **B)** `"git-enabled": true/false`
  - **Pros:** Shorter, concise
  - **Cons:** Less descriptive
  
- [ ] **C)** `"enable-git-commit": true/false`
  - **Pros:** Very specific about what git operation
  - **Cons:** Less extensible for future git operations
  
- [ ] **D)** Other (please specify): 

**Recommendation:** Option A for clarity and consistency with existing conventions

---

**Q3: What should be the structure and name of the "executed" flag for each prompt?**

Please choose one:
- [x] **A)** A simple boolean field: `"executed": true/false`
  - **Pros:** Simple, minimal
  - **Cons:** No metadata about when/how execution occurred
  
- [ ] **B)** An object with timestamp: `"executed": {"flag": true, "timestamp": "2025-12-30T10:30:00Z"}`
  - **Pros:** Includes execution time for audit trail
  - **Cons:** More complex structure
  
- [ ] **C)** An object with detailed metadata: `"executed": {"flag": true, "timestamp": "...", "by": "user/system"}`
  - **Pros:** Complete audit trail
  - **Cons:** Most complex, may be over-engineered
  
- [ ] **D)** Other (please specify): 

**Recommendation:** Option B for balance between simplicity and useful metadata

---

**Q4: Should the "Complete" button in the Web UI be visible for all prompts or only for in-progress prompts?**

Please choose one:
- [ ] **A)** Visible for all prompts, but enabled only when executed=true
  - **Pros:** User can always see the button and understand the workflow
  - **Cons:** UI clutter with disabled buttons
  
- [x] **B)** Visible only for prompts in "in-progress" state and enabled only when executed=true
  - **Pros:** Cleaner UI, shows only relevant actions
  - **Cons:** Button appears/disappears based on state
  
- [ ] **C)** Visible for prompts in "planned" or "in-progress" states
  - **Pros:** Shows button when prompt is active
  - **Cons:** May allow completion of planned but not executed prompts
  
- [ ] **D)** Other (please specify): 

**Recommendation:** Option B for cleaner UX and correct workflow enforcement

---

**Q5: What should happen if `prompt_complete.py` is called when git operations are enabled but no changes exist to commit?**

Please choose one:
- [ ] **A)** Fail with an error and don't change the prompt state
  - **Pros:** Strict validation, ensures commits are meaningful
  - **Cons:** May block legitimate completions
  
- [x] **B)** Warn but proceed with state change (skip git commit)
  - **Pros:** Flexible, allows completion even without changes
  - **Cons:** May result in inconsistent git history
  
- [ ] **C)** Create an empty commit with a message indicating no changes
  - **Pros:** Maintains git history consistency
  - **Cons:** Clutters git history with empty commits
  
- [ ] **D)** Other (please specify): 

**Recommendation:** Option B for flexibility while maintaining workflow

---

**Q6: Should `prompt_set_executed_on.py` validate that the prompt exists before setting the executed flag?**

Please choose one:
- [x] **A)** Yes - Fail if prompt-id doesn't exist in registry
  - **Pros:** Data integrity, prevents errors
  - **Cons:** None significant
  
- [ ] **B)** No - Just attempt to set the flag regardless
  - **Pros:** Simpler implementation
  - **Cons:** May cause silent failures or data corruption
  
- [ ] **C)** Other (please specify): 

**Recommendation:** Option A for data integrity

---

**Q7: In the Web UI, where should the "Complete" button be positioned in the prompt row?**

Please choose one:
- [x] **A)** In the Actions column, after the existing "Edit/View" and "Set State" buttons
  - **Pros:** Follows existing pattern, all actions together
  - **Cons:** May create long row if many buttons
  
- [ ] **B)** Replace the "Set State" button with "Complete" when conditions are met
  - **Pros:** Cleaner UI, context-aware
  - **Cons:** Lxss consistency, may confuse users
  
- [ ] **C)** In a separate "Completion" column
  - **Pros:** Clear separation of concerns
  - **Cons:** Adds another column to the table
  
- [ ] **D)** Other (please specify): 

**Recommendation:** Option A for consistency with existing UI patterns

---

**Q8: Should there be a way to mark a prompt as "executed" from the Web UI, or should this only be set programmatically?**

Please choose one:
- [ ] **A)** Add a button/toggle in Web UI to manually set executed flag
  - **Pros:** User control, flexibility for manual workflows
  - **Cons:** May bypass intended automation
  
- [x] **B)** Only allow programmatic setting via `prompt_set_executed_on.py`
  - **Pros:** Enforces workflow, prevents manual errors
  - **Cons:** Less flexible, requires command line access
  
- [ ] **C)** Automatically set executed=true when certain actions are performed in the UI
  - **Pros:** Automated, reduces manual steps
  - **Cons:** Need to define which actions trigger this
  
- [ ] **D)** Other (please specify): 

**Recommendation:** Option C with clear triggering conditions (e.g., saving implementation.md with content)
