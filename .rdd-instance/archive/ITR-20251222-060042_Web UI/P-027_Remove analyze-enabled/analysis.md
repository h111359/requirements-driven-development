# Analysis - P-027: Remove analyze-enabled

## Copilot Review

The request to check if certain files and requirements are obsolete is **valid and necessary**. Here's my honest assessment:

**The Good:**
- The framework has evolved from boolean flags (`analyze-enabled`, `plan-enabled`) to a unified `execution-mode` attribute, which is a cleaner design
- P-016 properly introduced this change with a comprehensive plan
- The new approach eliminates mutual exclusivity issues and provides clearer state management

**The Bad:**
- The cleanup wasn't completed when P-016 was implemented - obsolete scripts, CLI commands, and requirements were left behind
- The `analyze-enabled` field still exists in some prompts in work-iteration-registry.json, creating confusion about what's actually used
- This technical debt should have been addressed immediately after P-016

**The Reality:**
- The four scripts (.rdd/src/actions/prompt_analyze_on.py, prompt_analyze_off.py, prompt_plan_on.py, prompt_plan_off.py) are completely obsolete and serve no purpose
- The CLI actions (analyze-on, analyze-off, plan-on, plan-off) are dead code
- The requirements mentioning these components are outdated and confusing

**Recommendation:** Remove all obsolete components immediately to prevent confusion and reduce maintenance burden.

## Best Practices

**Registry Schema Evolution:**
- When evolving data schemas, perform complete migration - don't leave old fields lingering
- Remove deprecated fields in the same commit/prompt that introduces replacements
- Update all references atomically (scripts, CLI, documentation, requirements)

**CLI Command Deprecation:**
- Either remove deprecated commands immediately or add deprecation warnings before removal
- Don't expose users to commands that manipulate attributes no longer used by the system

**Code Cleanup:**
- Dead code should be removed, not left "just in case"
- If uncertain about removal, use feature flags or version tags in git history
- Prefer clean state over accumulating technical debt

**Documentation Hygiene:**
- Requirements should reflect current system state
- Mark obsolete requirements explicitly (e.g., [DELETED] tag) with timestamp and reason
- Keep requirements.md as single source of truth

## Samples from GitHub

Common patterns for handling schema evolution in configuration-driven systems:

1. **Django Migrations Pattern:**
   - Create migration that adds new field
   - Create migration that populates new field from old field  
   - Create migration that removes old field
   - All in sequence, with clear version tracking

2. **Database Migration Tools:**
   - Forward migration adds new schema
   - Backward migration removes old schema
   - Never leave orphaned columns/attributes

3. **API Versioning:**
   - When changing API contracts, explicitly deprecate old endpoints
   - Provide migration period with warnings
   - Remove after migration window closes

**This framework's approach:** Since this is a file-based system without version migration capabilities, the approach should be simpler - immediate removal when replacement is proven stable.

## Proposals

### Option A: Complete Removal (Recommended)

**Actions:**
1. Delete the four obsolete Python scripts
2. Remove the four CLI actions from .rdd/src/rdd.py
3. Remove `analyze-enabled` field from all prompts in work-iteration-registry.json
4. Mark obsolete requirements as [DELETED] in requirements.md with timestamp

**Pros:**
- Clean state, no confusion
- Reduces code maintenance surface
- Aligns code with actual behavior
- Simple and complete

**Cons:**
- If anyone still has scripts calling these CLI commands, they'll break
- No migration path for external tools

### Option B: Deprecation with Warnings

**Actions:**
1. Keep scripts but add warning messages: "This command is deprecated, use prompt_set_execution_mode.py instead"
2. Keep CLI actions but emit deprecation warnings
3. Remove `analyze-enabled` field from registry
4. Mark requirements as [DEPRECATED]

**Pros:**
- Gentler migration path
- Discoverable migration for users

**Cons:**
- More complex
- Maintains dead code
- Likely overkill for internal framework

### Option C: Convert to Aliases

**Actions:**
1. Modify obsolete scripts to call prompt_set_execution_mode.py with appropriate mode
2. Keep CLI actions but route to new script

**Pros:**
- Maintains backward compatibility
- No user-facing changes

**Cons:**
- Maintains unnecessary abstraction layer
- Confusing to have two ways to do the same thing
- Still need to clean up eventually

### Recommendation: Option A

Since this is an internal framework tool (not a public API), and the change happened in P-016 which was relatively recent, complete removal is appropriate. The framework is version-controlled in git, so the history is preserved if needed.

## Prompt Modification

If I were writing this prompt, I would structure it as follows:

---

**Title:** Clean up obsolete analyze/plan mode artifacts

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

---

**Why this is better:**
- More specific and actionable
- Provides complete task list with file paths
- Includes verification steps
- Sets clear expectations for outcome
- Easier to track completion
