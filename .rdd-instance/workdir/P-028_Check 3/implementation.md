Implementation log for prompt P-028 (Check 3)

Timestamp: 2026-01-24T

Summary
- Objective: Identify possible operators expected in `visibleWhen` conditions as recognized by RDD runtime and conventions.

Actions performed
1. Read work-iteration registry to identify active prompt (`P-028`) and execution mode (`implement`).
2. Opened active prompt file: prompt.md (found no snippet keys).
3. Searched repository for occurrences of "visibleWhen" and related condition-handling code.
4. Inspected relevant files:
   - tech_design_schema_editor/static/app.js (condition builder and parser)
   - tech_design_schema_editor/server.py (schema validation of visibleWhen)
   - .rdd/conventions/technical-design.convention.md (visibleWhen format and evaluation logic)
   - .rdd/src/web/static/app.js (RDD web app main script) — inspected for visibleWhen handling

Commands to reproduce (run in repo root):
- grep -R "visibleWhen" .
- grep -R "getOperatorsForQuestion" .
- sed -n '1480,1520p' tech_design_schema_editor/static/app.js
- sed -n '270,330p' tech_design_schema_editor/server.py

Findings
- The RDD conventions (`.rdd/conventions/technical-design.convention.md`) document `visibleWhen` as an array of condition objects, with the legacy `equals` shorthand supported.
- The editor (tech_design_schema_editor/static/app.js) implements a condition-builder and recognizes a set of operators via `getOperatorsForQuestion()`; it also parses legacy expressions via `parseLegacyExpression()`.
- The server-side schema validation (tech_design_schema_editor/server.py) explicitly allows the following operators in new-format `visibleWhen` conditions: `equals`, `notEquals`, `contains`, `notContains`, `startsWith`, `greaterThan`, `lessThan`.
- The RDD web UI script at `.rdd/src/web/static/app.js` does not contain detection or evaluation logic for `visibleWhen` (no matches found for `visibleWhen`); conditional visibility handling is implemented primarily in the editor and validated server-side.

Precedence and decisions
- Where the editor and server agree (operators list), treat those as canonical for content validation and UI editing.
- The conventions document demonstrates the intended semantics (equals and array-of-equals), but the operative set of recognized operators used by validation and editor is the superset found in server.py and editor JavaScript.

Notes / next steps
- If RDD runtime (non-editor UI) must evaluate `visibleWhen` at render time, implement evaluation logic in `.rdd/src/web/static/app.js` consistent with the operator set noted above.
- No requirements updates were necessary for this prompt.

Error handling
- If additional operators are discovered or required, record them here and update the convention and server validation accordingly.

(End of implementation log)
