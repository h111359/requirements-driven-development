## Definitions

See the definitions in `.rdd/prompt-snippets/execution.md`



## Instructions - Follow these steps exactly:  

1. For each [ACTIVE-PROMPT] parts for which there are still multiple different interpretations and multiple variants of interpretation of the the required result - generate multiple-choice question with up to 5 most probable preferences in [QUESTIONNAIRE] following the conventions in [QUESTIONNAIRE-CONVENTION] and the JSON schema defined in `.rdd/conventions/questionnaire-json-schema.md`. 

   - The questionnaire must be created as a JSON file named `questionnaire.json` in the [ACTIVE-PROMPT-FOLDER]
   - Follow the JSON structure specified in `.rdd/conventions/questionnaire-json-schema.md`
   - Initialize all `user-selection` fields with `{"type": null, "value": null}`
   - Include context, question text, options with pros/cons, recommended option, and rationale for each question
   - Only add questions if the questionnaire is being created for the first time. If `questionnaire.json` already exists with questions, do not modify the existing questions but be careful not to repeat the same question several times.



 ## Execution Step Rules

- Do not generate quesions for which answers are already found in the context files. 

- Always follow the conventions defined in [QUESTIONNAIRE-CONVENTION].