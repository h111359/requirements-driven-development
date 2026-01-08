Change `.rdd/src/actions/prompt_create.py` not to create empty plan.md, prompt.md and questionnaire.json files when creating a new prompt

Create scripts in `.rdd/src/actions/` trough which are created the questionnaire.json file and in it are added the needed questions and all other elements + chosen answers are set. The prompts should not directly change the questionnaire.json file but only via these scripts.

questionnaire-generated flag should be set to true only after creation of the questionnaire (currently it is set immediately after prompt creation). Fix so these flags to be set only after clarify is executed.

questionnaire-answered flag should be set to true only after all questions are answered

Implementation tab in Active Prompt is visible immediately after creation of the prompt. It shall remain hidden until "implementation-completed" attribute of the Active Prompt in `.rdd-instance/workdir/work-iteration-registry.json` is changed to truth. 