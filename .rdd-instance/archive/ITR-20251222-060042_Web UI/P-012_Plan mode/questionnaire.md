# Questionnaire for P-012: Plan Mode

**ℹ️ Context**

We are implementing a "Plan mode" feature similar to the existing "Analyze mode". This mode will allow users to generate a plan without immediately proceeding to implementation, giving them a chance to review the plan first.

**Current Situation**

The analyze mode is implemented with:
- A toggle switch in the Web UI prompts table
- An `analyze-enabled` boolean field in the work iteration registry
- Action scripts `prompt_analyze_on.py` and `prompt_analyze_off.py`
- Automatic disabling after analyze execution completes

---

## Questions

**Q1: Where should the plan mode toggle be placed in the Web UI?**

Please choose one:
- [ ] **A)** Add as a new column "Plan Mode" next to the "Analyze Mode" column in the prompts table
  - **Pros**: Clear separation, easy to see both modes at a glance, consistent with current layout
  - **Cons**: Makes the table wider, may require horizontal scrolling on smaller screens
- [x] **B)** Combine both modes in a single column with two separate toggle switches
  - **Pros**: More compact, saves horizontal space
  - **Cons**: May be visually crowded, harder to scan
- [ ] **C)** Use a radio button group or dropdown to select mode (None/Analyze/Plan)
  - **Pros**: Enforces mutual exclusivity in the UI, cleaner interface
  - **Cons**: Requires two clicks to switch modes (disable one, enable other)
- [ ] **D)** Other (please specify): 

---

**Q2: How should mutual exclusivity between analyze mode and plan mode be enforced?**

Please choose one:
- [x] **A)** Automatically disable one mode when the other is enabled (in both UI and backend)
  - **Pros**: Simple user experience, impossible to have both enabled
  - **Cons**: User might not notice the automatic change
- [ ] **B)** Show an error/warning message and prevent enabling if the other mode is already on
  - **Pros**: User is explicitly informed, more transparent
  - **Cons**: Requires extra step to switch modes
- [ ] **C)** Disable the toggle for one mode in the UI when the other is active
  - **Pros**: Clear visual feedback, prevents user error
  - **Cons**: User must manually disable the active mode before enabling the other
- [ ] **D)** Other (please specify): 

---

**Q3: What should be the field name in the work iteration registry for plan mode?**

Please choose one:
- [x] **A)** `plan-enabled` (consistent with `analyze-enabled`)
- [ ] **B)** `plan-mode`
- [ ] **C)** `plan-mode-enabled`
- [ ] **D)** Other (please specify): 

---

**Q4: Should plan mode be automatically disabled after the plan is generated?**

Please choose one:
- [x] **A)** Yes - automatically disable plan mode after execution (consistent with analyze mode)
  - **Pros**: User doesn't need to manually turn it off, consistent behavior
  - **Cons**: If user wants to regenerate plan, must re-enable
- [ ] **B)** No - keep plan mode enabled until manually turned off
  - **Pros**: User can run execution multiple times to refine the plan
  - **Cons**: User must remember to turn it off before proceeding to implementation
- [ ] **C)** Provide a checkbox option in the Web UI to control this behavior
  - **Pros**: Maximum flexibility
  - **Cons**: More complex UI and logic
- [ ] **D)** Other (please specify): 

---

**Q5: What should happen if a user tries to enable plan mode while analyze mode is active (or vice versa)?**

**ℹ️ Note**: This question relates to Q2 but focuses on the backend validation logic.

Please choose one:
- [x] **A)** Backend automatically disables the other mode and enables the requested one
  - **Pros**: Seamless experience, no errors
  - **Cons**: Silent state changes might confuse users
- [ ] **B)** Backend returns an error and does not change any state
  - **Pros**: Explicit, user must make conscious decision
  - **Cons**: Extra step required
- [ ] **C)** Backend returns a warning but proceeds with the change
  - **Pros**: Informs user but doesn't block operation
  - **Cons**: Warning might be ignored
- [ ] **D)** Other (please specify): 

---

**Q6: Should there be action scripts for plan mode similar to analyze mode?**

Please choose one:
- [x] **A)** Yes - create `prompt_plan_on.py` and `prompt_plan_off.py` (consistent with analyze mode)
- [ ] **B)** No - use a single script with a parameter to enable/disable
- [ ] **C)** Other (please specify): 

---

**Q7: After plan mode execution completes and plan.md is generated, how should the execution flow proceed?**

Please choose one:
- [x] **A)** Stop execution completely; user must manually trigger execution again (with plan mode off) to proceed to implementation
  - **Pros**: Clear separation of phases, user can review plan before proceeding
  - **Cons**: Requires manual intervention
- [ ] **B)** Prompt user for confirmation before proceeding to implementation
  - **Pros**: Convenient workflow, user has a chance to abort
  - **Cons**: Requires interactive input, may not work well in automated scenarios
- [ ] **C)** Wait for plan mode to be manually disabled, then auto-continue if execution is triggered again
  - **Pros**: Flexible, user controls the flow
  - **Cons**: May be unclear when system is waiting
- [ ] **D)** Other (please specify): 
