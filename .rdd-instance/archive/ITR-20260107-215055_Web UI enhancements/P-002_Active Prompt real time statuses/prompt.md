Refactor the code so the status icons on "Active Prompt" page (representing the flags "state", "questionnaire-generated", "questionnaire-answered", "plan-generated", "implementation-completed",            "execution-mode", "executed") as well as the coloring of the buttons Prompt, Questionnaire, Analysis, Plan, Implementation, Modifications to reflect in real time (up to 2 seconds delay) the real state in `.rdd-instance/workdir/work-iteration-registry.json` and the presence of the files in `.rdd-instance/workdir/`. Buttons for deletion shall be disabled if the file is not present.

**Description:**

**Context:**
The Active Prompt page currently is supposed to update the status icons every 2 seconds via the `refreshActivePromptStatuses()` function, which fetches the work iteration registry and updates flag indicators (questionnaire-generated, questionnaire-answered, plan-generated, implementation-completed, executed). However, it is not working in reliable way. Also, the file view buttons (Questionnaire, Analysis, Plan, Implementation, Modifications) only update their enabled/disabled states on initial page load.

**Objective:**
Stabilize and extend the existing 2-second polling mechanism to also update file button states, ensuring they reflect the current workflow state in near real-time (up to 2 seconds delay).

**Testing:**
   - Verify button states update within 2 seconds of registry changes
   - Test with various workflow states (new prompt, questionnaire generated, plan generated, etc.)
   - Ensure no performance degradation from the additional button state logic
   - Verify disabled buttons remain non-clickable
