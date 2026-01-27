Report: Recognized `visibleWhen` operators (prompt P-028)

Objective: List operators that RDD recognizes or validates for `visibleWhen` conditions.

Summary of recognized operators (canonical set found in server validation and editor):

- equals
- notEquals
- contains
- notContains
- startsWith
- greaterThan
- lessThan

Sources and evidence:

- Server-side validation: tech_design_schema_editor/server.py — `valid_operators = ['equals', 'notEquals', 'contains', 'notContains', 'startsWith', 'greaterThan', 'lessThan']`
- Editor UI: tech_design_schema_editor/static/app.js — `getOperatorsForQuestion()` returns operator lists per question type and `parseLegacyExpression()` maps legacy JS expressions (==, ===, !=, !==, includes/contains) into normalized operator names such as `equals` and `contains`.
- Conventions: .rdd/conventions/technical-design.convention.md documents `visibleWhen` structure and evaluation semantics (primary example uses `equals`/array-of-equals), and requires `visibleWhen` rules to be honored by RDD flows.

Notes:
- The RDD web UI script at `.rdd/src/web/static/app.js` currently does not implement `visibleWhen` parsing/evaluation (no occurrences of `visibleWhen` found); conditional visibility support is present in the editor and enforced by server validation. If runtime evaluation is required in RDD UI, implement compatible evaluation logic using the operator set above.

Recommendation:
- Treat the operator set above as canonical for `visibleWhen` in RDD; update `.rdd/conventions/technical-design.convention.md` examples to list the full operator set to avoid ambiguity.
