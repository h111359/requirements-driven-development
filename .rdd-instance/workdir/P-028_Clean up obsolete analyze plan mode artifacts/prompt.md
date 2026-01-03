**Context:**
P-016 introduced `execution-mode` attribute to replace the boolean `analyze-enabled` and `plan-enabled` flags. This was a successful refactoring that simplified the execution flow. However, the old infrastructure was not fully removed.

**Objective:**
Complete the cleanup initiated by P-016 by removing all obsolete artifacts related to the old boolean flag approach.

**Tasks:**

1. **Remove obsolete Python scripts:**
   - Delete `.rdd/src/actions/prompt_analyze_on.py`
   - Delete `.rdd/src/actions/prompt_analyze_off.py`
   - Delete `.rdd/src/actions/prompt_plan_on.py`
   - Delete `.rdd/src/actions/prompt_plan_off.py`

2. **Remove obsolete CLI commands from `.rdd/src/rdd.py`:**
   - Remove `prompt.analyze-on` action
   - Remove `prompt.analyze-off` action
   - Remove `prompt.plan-on` action
   - Remove `prompt.plan-off` action

3. **Clean work-iteration-registry.json:**
   - Remove `analyze-enabled` field from all prompts (currently exists in P-021, P-022, P-024, P-025, P-026)

4. **Update requirements.md:**
   - Mark the following as [DELETED - 20260103] with note "Superseded by execution-mode in P-016":
     - [TR-20251230-2004]
     - [TR-20251230-2005]
     - [TR-20251230-2006]
     - [TR-20251230-2009]
     - [TR-20251230-2010]
     - [TR-20251231-0205]

5. **Update convention documents:**
   - Check `.rdd/conventions/work-iteration-registry.convention.md` for references to `analyze-enabled` or `plan-enabled`
   - Remove any such references if found

**Expected Outcome:**
Clean codebase with no references to the deprecated boolean flag approach, fully aligned with the execution-mode design introduced in P-016.