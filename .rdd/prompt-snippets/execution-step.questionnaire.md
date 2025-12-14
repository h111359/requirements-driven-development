## Execution Step Name

Ensure questionnaire is answered

## Execution Step Definitions

- [WI-REGISTRY] is the file `.rdd-instance/workdir/work-iteration-registry.json`

- [QUESTIONNAIRE] is file set in "clarity.file" attribute of [WI-REGISTRY]

## Execution Step Instructions

- If **ALL** the questions in [QUESTIONNAIRE] are answered:
    * set "clarity.state" attribute in [WI-REGISTRY] to "done"
    * set "plan.state" attribute in [WI-REGISTRY] is "ready-to-start"

- Otherwise, if not all questions are answered - stop the execution and aks the user to answer the questions.

 

