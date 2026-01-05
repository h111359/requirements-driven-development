# Questionnaire for P-021: Add prompt texts in prompts-registry

**ℹ️ Context**

The requirement is to copy prompt.md and all modifications texts to prompts-registry.md when a prompt is completed. Currently, prompts-registry.md contains mostly "TBD" placeholders. We need to clarify the implementation details.

---

## Questions

**Q1: When exactly should the prompt text be copied to prompts-registry.md?**

Please choose one:
- [x] **A)** When the "Complete Prompt" button is pressed in the Web UI (before setting state to completed)
- [ ] **B)** When the prompt state is set to "completed" (could be via any mechanism - Web UI, CLI, or action script)
- [ ] **C)** As a separate manual action after completion (e.g., a new button "Archive to Registry")
- [ ] **D)** Other (please specify): 

---

**Q2: How should modifications be included in the prompts-registry.md?**

Please choose one:
- [x] **A)** Append modifications inline within the same prompt record, separated by markers (e.g., `### Modification 001`, `### Modification 002`, etc.)
- [ ] **B)** Create separate prompt records for each modification (e.g., `%%PROMPT P-018-M001 "..."`)
- [ ] **C)** Only include the base prompt.md text, ignore modifications
- [ ] **D)** Include modifications as a section at the end of the prompt text with clear delimiters
- [ ] **E)** Other (please specify): 

**ℹ️ Note:** Modifications are stored in files like `modification-001.md`, `modification-002.md`, etc. within the prompt folder.

---

**Q3: Should we retroactively populate prompts-registry.md for all completed prompts?**

Please choose one:
- [x] **A)** Yes - Create a script or action to copy all existing completed prompts to prompts-registry.md now
- [ ] **B)** No - Only apply this for newly completed prompts from now on (leave existing "TBD" entries as is)
- [ ] **C)** Manual - Provide a tool/command that can be run selectively for specific prompts
- [ ] **D)** Other (please specify): 

---

**Q4: What should happen if a prompt text is updated after it has been copied to prompts-registry.md?**

Please choose one:
- [x] **A)** Automatically update the prompts-registry.md when the prompt.md file changes
- [ ] **B)** Never update - prompts-registry.md is immutable once written (historical record)
- [ ] **C)** Provide a manual "Re-sync to Registry" action for when users explicitly want to update
- [ ] **D)** Warn the user but don't auto-update; require explicit confirmation
- [ ] **E)** Other (please specify): 

---

**Q5: Should the implementation create a dedicated action script for this operation?**

Please choose one:
- [x] **A)** Yes - Create `.rdd/src/actions/prompt_add_to_registry.py` as a standalone, reusable action
- [ ] **B)** No - Integrate this into existing completion scripts (e.g., `prompt_complete.py`)
- [ ] **C)** Both - Create a standalone action AND call it from the completion workflow
- [ ] **D)** Other (please specify): 

---

**Q6: If a prompt has no modifications, what should be written to prompts-registry.md?**

Please choose one:
- [x] **A)** Just the prompt.md content between the sentinel lines
- [ ] **B)** The prompt.md content with an empty "## Modifications" section noting "None"
- [ ] **C)** Same as (A), no special handling needed
- [ ] **D)** Other (please specify): 

---
