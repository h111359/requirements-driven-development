## Definitions

See the definitions in `.rdd/prompt-snippets/execution.md`



## Instructions - Follow these steps exactly:  

1. For each [ACTIVE-PROMPT] parts for which there are still multiple different interpretations and multiple variants of interpretation of the the required result - generate multiple-choice question with up to 5 most probable preferences in [QUESTIONNAIRE] following the conventions in [QUESTIONNAIRE-CONVENTION]. Only add questions in [QUESTIONNAIRE], do not modify the existing content. If there are already existing questions there - do not change them but be careful not to repeat the same question several times.

2. After completing the analyze execution, automatically disable analyze mode by running the command: `python .rdd/src/actions/prompt_analyze_off.py`



 ## Execution Step Rules

- Do not generate quesions for which answers are already found in the context files. 

- Always follow the conventions defined in [QUESTIONNAIRE-CONVENTION].