Investigation of possible `visibleWhen` operators and implementation details

Summary
-------
I inspected the Tech Design Schema Editor frontend and server validation to determine which `visibleWhen` operators are supported and how legacy expressions are handled.

Commands run (reproducible)
---------------------------
- `cd /home/hromar/Desktop/vscode/requirements-driven-development && grep -nR "visibleWhen" tech_design_schema_editor || true`  # located frontend and server validations

Findings
--------
- Frontend (tech_design_schema_editor/static/app.js): the condition-builder UI uses a per-question operator list determined by `getOperatorsForQuestion(questionId)`.
- Server validation (tech_design_schema_editor/server.py) enforces an array of condition objects and accepts either the old `equals` field or the new `operator` + `value` pair. The server's `valid_operators` list is: `equals, notEquals, contains, notContains, startsWith, greaterThan, lessThan`.
- The frontend mapping (by question type) is:
  - `radio`, `dropdown`: `equals`, `notEquals`
  - `multiselect`: `contains`, `notContains` (multiselect values stored as arrays; builder uses OR semantics)
  - `checkbox`: `equals`
  - `text`: `equals`, `contains`, `startsWith`
  - `textarea`: `contains`
  - `number`: `equals`, `greaterThan`, `lessThan`
  - Fallback for unknown types: `equals`, `notEquals`

Legacy handling
---------------
- The frontend supports legacy string expressions (JavaScript expressions referencing `answers[...]`) and attempts to parse common patterns (`===`, `==`, `!==`, `.includes`/`.contains`) via `parseLegacyExpression()`, converting them to normalized `{questionId, operator, value}` objects when possible.
- The frontend normalizes old-format objects with `equals` into the new `{operator: 'equals', value: ...}` shape.

Data storage / value types
------------------------
- For option-based questions (radio, dropdown, multiselect) the builder stores option IDs (not labels) to ensure stability.
- For `multiselect`, `value` is stored as an array (OR semantics in the builder); server accepts arrays for `value` where appropriate.

What I considered from other artifacts
------------------------------------
- Technical Design: the instance `.rdd-instance/specifications/technical-design.json` currently contains an answered `Infra_DeploymentModel` (multiselect) which shows an example of an answered question; it is not directly changing operator semantics but is relevant when testing `visibleWhen` behavior for multiselect answers.
- Requirements: the requirements explicitly mandate support for conditional visibility and a visual condition builder (see UR/TR entries). This confirms the operator set must include equality, containment, string matching and numeric comparisons.
- Files-and-folders: the `tech_design_schema_editor` folder contains both the UI (`static/app.js`) and server (`server.py`) validations; both must stay consistent.

Precedence and decisions
-----------------------
- The `ACTIVE-PROMPT` instructions took precedence for this investigation and determined the work (inspect code and produce the report). No prompt-snippet overrides were present.
- No changes to requirements were made because the existing requirements already require conditional visibility support; therefore no requirement scripts were invoked.

Report
------
I created a concise `report.md` in the prompt workdir with the exact list of supported operators and short notes for QA and integration.

Next steps executed by me
------------------------
1. Created `implementation.md` and `report.md` in the prompt folder.
2. (To finalize execution) the framework scripts recommended by the execution flow should be run to mark the prompt executed and implementation completed; I will now run them and record outputs.

Commands to run for finalization (executing now):
--------------------------------------------------
python .rdd/src/actions/prompt_set_executed_on.py
python .rdd/src/actions/prompt_implementation_completed_on.py
python .rdd/src/actions/prompt_set_execution_mode.py mode=no-action

If any of these commands fail, the error will be logged to this file and partial work preserved.
