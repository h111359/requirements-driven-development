## Execution Step Name

Ensure clarity

## Execution Step Definitions

- [WI-REGISTRY] is the file `.rdd-instance/workdir/work-iteration-registry.json`

- [PROMPT-ID] is the value of the attribute "PROMPT-ID" in the file [WI-REGISTRY]

- [CONTEXT-ANALYSIS-FILE] is the file set in "context.file" attribute of [WI-REGISTRY].

- [PROMPT-TEXT] is the content of the file `.rdd-instance/workdir/work-iteration-prompt.md`

- [PROMPT-STATEMENT] is any part of the [PROMPT-TEXT] or [CONTEXT-ANALYSIS-FILE] text defining some aspect of the results needed to be achieved. 

- [QUESTIONNAIRE] is a file containing questions to the user. The file location is in folder `.rdd-instance/workdir/`. The file name convention is `[PROMPT-ID]-questionnaire.md`, where [PROMPT-ID] should be replaced with the respective [PROMPT-ID] value.

- [QUESTIONNAIRE-CONVENTION] is the file `.rdd/conventions/questions-formatting.md`

## Execution Step Instructions

1. For each [PROMPT-STATEMENT] parts for which there are multiple different interpretations and multiple options the required result to be understood - generate multiple-choice question with up to 5 most probable preferences in [QUESTIONNAIRE] following the conventions in [QUESTIONNAIRE-CONVENTION].

2. Set "clarity.state" attribute in [WI-REGISTRY] to "generated". Set "clarity.file" state to the relative path to [QUESTIONNAIRE]

 ## Execution Step Rules

- Do not generate quesions for which answers are already found in the context files. 

- Always follow the conventions defined in [QUESTIONNAIRE-CONVENTION].