# Questionnaire for P-008: Move analyze command in the Web UI

---

## Context

The current implementation requires users to manually type "analyze" in the chat to trigger analysis mode. This prompt proposes moving this to a boolean flag in the work-iteration-registry.json that can be toggled via:
1. Python scripts (prompt_analyze_on.py, prompt_analyze_off.py)
2. The Web UI (toggle switch)
3. Automatic turn-off after analyze execution completes

---

## Questions

**Q1: Should the analyze flag be automatically turned OFF after the analyze execution completes?**

**ℹ️ Context:** The prompt states "When the analyze execution is completed, the copilot should turn off the analyze option via the prompt_analyze_off.py script." This means after each analyze run, the flag would reset to false.

Please choose one:
- [x] **A)** Yes - Auto-disable after each analyze execution
  - **Pros:** Prevents accidental re-runs; clear single-use semantics; user must explicitly re-enable
  - **Cons:** Requires re-enabling for multiple analysis iterations; extra step if user wants consecutive runs
  
- [ ] **B)** No - Keep analyze ON until manually disabled
  - **Pros:** Easier for iterative analysis workflows; fewer toggles needed
  - **Cons:** May cause confusion if user forgets it's enabled; accidental re-execution possible
  
- [ ] **C)** Make it configurable - Add a "auto-reset" property
  - **Pros:** Maximum flexibility; supports both workflows
  - **Cons:** Adds complexity to the registry schema
  
- [ ] **D)** Other (please specify): 

**Recommendation:** Option A - aligns with the explicit instruction in the prompt and provides clearer execution semantics.

---

**Q2: What should happen if a user tries to enable analyze mode for a completed prompt?**

**ℹ️ Context:** The prompt states "should not be provided for completed prompts" in the Web UI context. This question clarifies the enforcement level.

Please choose one:
- [x] **A)** Hard block - Scripts and UI should prevent enabling analyze for completed prompts
  - **Pros:** Enforces clear workflow; prevents confusion
  - **Cons:** May limit flexibility for edge cases (e.g., re-analyzing a completed prompt)
  
- [ ] **B)** Soft warning - Allow but show a warning message
  - **Pros:** Flexibility for power users; handles edge cases
  - **Cons:** May confuse regular users; unclear semantics
  
- [ ] **C)** Allow silently - No restriction
  - **Pros:** Maximum flexibility
  - **Cons:** Violates stated requirement; may cause unexpected behavior
  
- [ ] **D)** Other (please specify): 

**Recommendation:** Option A - aligns with the stated requirement and provides clearer workflow boundaries.

---

**Q3: Should the analyze flag be stored per-prompt or globally for the active prompt?**

**ℹ️ Context:** The prompt says "every prompt to have a boolean key if the analyze modification should be turned on" suggesting per-prompt storage. However, only the active prompt (state=planned/in-progress) can be executed.

Please choose one:
- [x] **A)** Per-prompt storage - Each prompt has its own analyze flag
  - **Pros:** Maintains state if prompt becomes inactive then active again; clearer data model
  - **Cons:** Only active prompt can execute, so flags on other prompts are unused until activated
  
- [ ] **B)** Global active-prompt flag - Single "active-analyze" flag at root level
  - **Pros:** Simpler; always applies to whatever prompt is active; less redundant data
  - **Cons:** Loses analyze state if prompt changes; doesn't match "every prompt to have" wording
  
- [ ] **C)** Other (please specify): 

**Recommendation:** Option A - matches the explicit wording in the prompt and provides better state persistence.

---

**Q4: What should be the default value for the analyze flag when a new prompt is created?**

Please choose one:
- [x] **A)** False (disabled by default)
  - **Pros:** Conservative; user explicitly enables when needed; prevents accidental analysis runs
  - **Cons:** Requires extra step to enable
  
- [ ] **B)** True (enabled by default)
  - **Pros:** Automatic analysis for new prompts; fewer manual steps
  - **Cons:** May run analysis when not needed; less explicit control
  
- [ ] **C)** Inherit from a global default setting
  - **Pros:** Configurable behavior; supports different workflows
  - **Cons:** Adds complexity
  
- [ ] **D)** Other (please specify): 

**Recommendation:** Option A - provides explicit control and aligns with current "opt-in" analyze behavior.

---

**Q5: Should the execution.md prompt logic still support the legacy "analyze" modifier in chat for backward compatibility?**

**ℹ️ Context:** Currently users can type "analyze" in the chat. After this change, it would come from the registry. Should we keep both methods or remove the chat modifier entirely?

Please choose one:
- [x] **A)** Remove chat modifier entirely - Only use registry flag
  - **Pros:** Single source of truth; cleaner implementation; forces migration to new approach
  - **Cons:** Breaking change; existing documentation/habits need updating
  
- [ ] **B)** Support both - Registry flag OR chat modifier
  - **Pros:** Backward compatibility; gradual migration; flexibility
  - **Cons:** Two ways to do same thing; potential confusion about which takes precedence
  
- [ ] **C)** Deprecation path - Support both but warn about chat modifier
  - **Pros:** Smooth migration; clear direction forward
  - **Cons:** Temporary complexity during transition
  
- [ ] **D)** Other (please specify): 

**Recommendation:** Option A - provides cleaner long-term solution and aligns with the goal of moving control to the registry/UI.

---

**Q6: Where should the scripts (prompt_analyze_on.py, prompt_analyze_off.py) be located?**

**ℹ️ Context:** The prompt requires creating these scripts. Need to determine their location in the directory structure.

Please choose one:
- [ ] **A)** `.rdd/src/` - With other automation scripts
  - **Pros:** Follows TR-20251224-0936; consistent with existing script location
  - **Cons:** None identified
  
- [ ] **B)** `scripts/` - In the user-facing scripts folder
  - **Pros:** More visible; alongside run-tests.py
  - **Cons:** Less consistent with framework script organization
  
- [ ] **C)** `.rdd/src/cli/` - Create a CLI subdirectory
  - **Pros:** Better organization if more CLI commands are added
  - **Cons:** Adds new directory structure not currently present
  
- [x] **D)** Other (please specify): `.rdd/src/actions/`

**Recommendation:** Option A - aligns with TR-20251224-0936 requirement for automation scripts.

---

**Q7: Should the Web UI toggle be a simple on/off switch or a more complex control?**

Please choose one:
- [x] **A)** Simple toggle switch (checkbox or slider)
  - **Pros:** Minimal UI; clear binary state; easy to understand
  - **Cons:** Limited if future analyze options are added
  
- [ ] **B)** Button that shows current state ("Analyze: ON/OFF")
  - **Pros:** Clearer state visibility; can add tooltip/help text
  - **Cons:** Slightly more complex UI
  
- [ ] **C)** Dropdown with "Analyze: Enabled/Disabled"
  - **Pros:** Extensible for future options; consistent with other dropdowns
  - **Cons:** Overkill for binary choice
  
- [ ] **D)** Other (please specify): 

**Recommendation:** Option A - simplest and most intuitive for a binary flag.

---
