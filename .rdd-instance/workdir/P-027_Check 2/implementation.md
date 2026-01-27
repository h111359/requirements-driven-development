Implementation log for prompt P-027: Check possible operators in visibleWhen

Summary
-------
This document records the investigative steps, commands considered/run, findings and actions taken while answering the active prompt: "Check what are the possible operators expected in the \"visibleWhen\" section of questions expected by web application in .rdd and the conventions."  The work produced a short report `report.md` in this folder.

Commands run or inspected (reproducible)
-------------------------------------
- Search for visibleWhen usages (repo-level):
  - grep -R "visibleWhen" .rdd .rdd-instance || true
- Inspect framework convention for Technical Design:
  - less .rdd/conventions/technical-design.convention.md
- Inspect framework schema (authoritative for runtime):
  - less .rdd/config/technical-design-schema.json
- Note: the editor implementation (tech_design_schema_editor) was inspected for reference, but is NOT authoritative for RDD unless conventions or config files state otherwise.

What I inspected (sources)
--------------------------
- `.rdd/conventions/technical-design.convention.md` — describes `visibleWhen` evaluation rules and examples (equals-based rules and array semantics).
- `.rdd/config/technical-design-schema.json` — actual framework schema file present in `.rdd/config/` which contains `visibleWhen` entries and in one place uses `operator: "contains"`.
- `.rdd-instance/specifications/technical-design.json` — instance answers file (sparse; not authoritative for operators but relevant to runtime behavior).
- Prompt snippet `execution.md` to follow execution flow (already followed).

Findings
--------
1. The conventions document defines `visibleWhen` primarily as rule objects that use `equals` semantics; arrays in `equals` represent OR within the condition, and multiple condition objects in `visibleWhen` are ANDed.

2. The authoritative framework schema `.rdd/config/technical-design-schema.json` contains `visibleWhen` rules in two shapes:
   - Legacy-style `equals` objects (e.g., `"equals": [ ... ]`) seen in several questions.
   - A newer-style rule using `operator: "contains"` (example: `Infra_PrimaryProvider` uses `operator: "contains"` against a multiselect `Infra_DeploymentModel`).

3. The presence of `operator: "contains"` in the schema indicates that the runtime/schema supports at least an explicit `contains` operator in addition to the `equals` legacy form.

4. The editor code (tech_design_schema_editor/static/app.js) exposes a wider operator map (equals, notEquals, contains, notContains, startsWith, greaterThan, lessThan, etc.), however the prompt explicitly asked to consider only RDD artifacts (conventions and `.rdd`), so editor-only operators are treated as non-authoritative unless mirrored in `.rdd` files.

Conclusion / Result
-------------------
- Operators explicitly present or described in the RDD framework (in `.rdd`):
  - `equals` (legacy form with `equals` property; supports array values → OR semantics for arrays; for multiselect equals means membership)
  - `contains` (explicit `operator: "contains"` used in the schema for multiselect checks)

- Notes on semantics observed from conventions and schema:
  - Multiple `visibleWhen` objects are evaluated with AND logic (all must be true).
  - Within a single rule, `equals` may accept an array representing OR semantics.
  - For multiselect questions, `equals`/`contains` semantics check membership in the answer array.

Actions taken
-------------
- Created this `implementation.md` log and `report.md` containing the concise operator list and examples.
- Did not modify any requirements (`.rdd-instance/specifications/requirements.md`) — no requirement changes were required.

Next steps (recommended)
------------------------
- Consider reconciling the small inconsistency between convention (equals-based) and schema (contains operator) to avoid confusion; recommendation recorded in `report.md`.

Files produced
--------------
- `report.md` — concise operator report for the active prompt (next file in same folder).

Error handling
--------------
No errors occurred while reading repository files. If file writes fail when saving these artifacts, the error should be recorded here and partial work preserved.

End of implementation log.
