[[[Analyse]]]

Check if the following files are still in use or they are obsolete:

.rdd/src/actions/prompt_analyze_off.py
.rdd/src/actions/prompt_analyze_on.py
.rdd/src/actions/prompt_plan_off.py
.rdd/src/actions/prompt_plan_on.py

Also check if these requirements should stay or are obsolete:

- [TR-20251230-2004] Each prompt in work-iteration-registry.json shall have an `analyze-enabled` boolean field with default value `false`.
- [TR-20251230-2006] The execution prompt logic shall read analyze mode from the `analyze-enabled` field in work-iteration-registry.json rather than from chat modifiers.

Check all the prompts executed up to now. In case of conflict, prompts with bigger number are with precedence.