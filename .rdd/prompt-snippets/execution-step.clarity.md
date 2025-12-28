## Execution Step Name

Ensure clarity

## Definitions

- [QUESTIONNAIRE] is a file containing questions to the user. The file location is in folder `.rdd-instance/workdir/<prompt-id>_<prompt-title>`. The file name convention is `questionnaire.md`.

- [QUESTIONNAIRE-CONVENTION] is the file `.rdd/conventions/questions-formatting.md`

- [WI-REGISTRY] is the file `.rdd-instance/workdir/work-iteration-registry.json`
  
- [PROMPT-REGISTRY] is the file `.rdd-instance/workdir/prompts-registry.md`

* [active-prompt] - The prompt in `.rdd-instance/workdir/work-iteration-registry.json` which is with state `planned` or `in-progress`. The framework allows only one prompt to be in some of those states and this prompt is considered to be the `active prompt`



## Instructions - Follow these steps exactly:  

1. **Read the registry**: Open and read the [WI-REGISTRY] file.
   
2. Identify the ID of the [active-prompt].

3. Identify the [active-prompt] in [PROMPT-REGISTRY] and execute its instructions.

4. For each [active-prompt] parts for which there are multiple different interpretations and multiple options the required result to be understood - generate multiple-choice question with up to 5 most probable preferences in [QUESTIONNAIRE] following the conventions in [QUESTIONNAIRE-CONVENTION].

 ## Execution Step Rules

- Do not generate quesions for which answers are already found in the context files. 

- Always follow the conventions defined in [QUESTIONNAIRE-CONVENTION].