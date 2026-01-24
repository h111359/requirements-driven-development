VisibleWhen operators - concise report

Scope: RDD artifacts only (conventions and .rdd config/schema)

Findings
--------

- Operators observed in RDD (authoritative sources):
  - `equals` — described in `.rdd/conventions/technical-design.convention.md` using `"equals"` rules; supports array values (array → OR semantics); used in legacy visibleWhen entries in `.rdd/config/technical-design-schema.json`.
  - `contains` — used explicitly in `.rdd/config/technical-design-schema.json` as `"operator": "contains"` for a multiselect-based condition.

- Semantics (from conventions + schema):
  - Multiple condition objects in `visibleWhen` are ANDed (all must hold).
  - Within a single condition, `equals` can be an array (interpreted as OR over the provided values).
  - For multiselect questions, `equals` or `contains` check membership (i.e., whether a given option is present in the answer array).

Notes and recommendation
------------------------
- The conventions document focuses on the `equals` form while the schema contains an explicit `contains` operator. This minor inconsistency is likely historical (legacy `equals` forms vs newer explicit operator syntax).
- Recommendation: standardize on a single canonical representation in `.rdd/config/technical-design-schema.json` and update `.rdd/conventions/technical-design.convention.md` to reflect supported operators (e.g., allow `operator` with values `equals|contains|notEquals` and clarify array semantics). This will reduce ambiguity for implementers and tools.

Examples (from repo)
--------------------
- Legacy equals array example (schema):

  "visibleWhen": [
    {
      "questionId": "Infra_UsesVNet",
      "equals": ["Single VNet", "Multiple VNets"]
    }
  ]

- Operator-based example (schema):

  "visibleWhen": [
    {
      "questionId": "Infra_DeploymentModel",
      "operator": "contains",
      "value": ["Public cloud"]
    }
  ]

End of report.
