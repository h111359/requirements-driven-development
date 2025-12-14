## Execution Step Name

Implement the prompt

## Execution Step Definitions

- [WI-REGISTRY] is the file `.rdd-instance/workdir/work-iteration-registry.json`

- [PROMPT-ID] is the value of the attribute "PROMPT-ID" in the file [WI-REGISTRY]

- [CONTEXT-ANALYSIS-FILE] is the file set in "context.file" attribute of [WI-REGISTRY].

- [PROMPT-TEXT] is the content of the file `.rdd-instance/workdir/work-iteration-prompt.md`

- [QUESTIONNAIRE] is file set in "clarity.file" attribute of [WI-REGISTRY]

- [PLAN] is the file `.rdd-instance/workdir/[PROMPT-ID]-plan.md`

## Execution Step Instructions

- based on [PROMPT-TEXT], [WI-REGISTRY], [CONTEXT-ANALYSIS-FILE], [QUESTIONNAIRE] and [PLAN] - follow the plan in [PLAN] and impement the plan. 

- Along with implementation add continuously information for the implementation details in file `.rdd-instance/workdir/[PROMPT-ID]-implementation.md` on each step. Especially take care of adding the commands you run in a terminal! Do not log the content of the changed files. 

- If you are asked to make an analysis, create a research, advice, recommend, find best-practice, review or similar - enter your findings in the file `.rdd-instance/workdir/[PROMPT-ID]-implementation.md`. In those cases you are encouraged to make a deep research in Internet (make your best effort to do that) for finding the best possible answer. 

- Set "implementation.state" attribute in [WI-REGISTRY] to "done".

## Execution Step Rules

- Do not skip any of the steps in the plan 

- Do not stop the implementation until the entire plan is completed. 

- Cover all the requirements of [PROMPT-TEXT], [WI-REGISTRY], [CONTEXT-ANALYSIS-FILE], [QUESTIONNAIRE] and [PLAN]. 







 

