## Execution Step Name

Plan the prompt

## Execution Step Definitions

- [WI-REGISTRY] is the file `.rdd-instance/workdir/work-iteration-registry.json`

- [PROMPT-ID] is the value of the attribute "PROMPT-ID" in the file [WI-REGISTRY]

- [CONTEXT-ANALYSIS-FILE] is the file set in "context.file" attribute of [WI-REGISTRY].

- [PROMPT-TEXT] is the content of the file `.rdd-instance/workdir/work-iteration-prompt.md`

- [QUESTIONNAIRE] is file set in "clarity.file" attribute of [WI-REGISTRY]

- [PLAN] is the file `.rdd-instance/workdir/[PROMPT-ID]-plan.md`

## Execution Step Instructions

- If **ALL** the questions in [QUESTIONNAIRE] are answered - set "clarity.state" attribute in [WI-REGISTRY] to "answered", otherwise - stop the execution and aks the user to answer the questions.

- based on [PROMPT-TEXT], [WI-REGISTRY], [CONTEXT-ANALYSIS-FILE], [QUESTIONNAIRE], create in [PLAN] a detailed plan how you will achieve the result asked in the prompt. 

- For each of the requirements in `.rdd-instance/requirements.md`, check if it is already observed by the plan you have created in the previous step. If some requirement is not followed and there is no overwriting statement of this requirements in [PROMPT-TEXT], [WI-REGISTRY], [CONTEXT-ANALYSIS-FILE] or [QUESTIONNAIRE], change the plan accordingly to ensure all requirements will be fulfilled during the execution of the prompt. 

- Add in the plan the exact updates that should be made in `.rdd-instance/requirements.md` as adding new requirements rows in it or modifying requirement rows. Follow the conventions defined in `.rdd/conventions/requirements-format.md` for that. Do not apply changes directly in `.rdd-instance/requirements.md` yet (it will be done in the execution step) - only describe them in the plan. 

- Add in the plan the exact updates that should be made in the specification statements and the specification files defined in `.rdd-instance/config.json` as adding new technical specification rows in it or modifying technical specification rows. Do not apply changes directly in the files yet (it will be done in the execution step) - only describe them in the plan. 

- Update the value of the attribute "plan.state" in [WI-REGISTRY] to "done".

- Set "implementation.state" attribute in [WI-REGISTRY] to "ready-to-start".

## Execution Step Rules

- Break down the plan into clear steps written in separate paragraphs

- Describe for each step clearly what exactly will be done in that step. 

- Assign sequentia number to each step

- Cover all the requirements of [PROMPT-TEXT], [WI-REGISTRY], [CONTEXT-ANALYSIS-FILE], [QUESTIONNAIRE]. 







 

