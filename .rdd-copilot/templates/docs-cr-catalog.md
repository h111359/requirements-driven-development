---
title: "Change Requests Catalog"
version: 1.0.0
lastUpdated: 2025-10-11
description: "Catalog of all change requests (CRs) submitted for the project with lifecycle tracking."
---

# Change Requests (CR) Catalog

This file lists all Change Requests proposed, accepted, implemented, or rejected. Each CR provides traceability from an initial need to its resolution.

## Lifecycle States
- proposed: Submitted and awaiting review
- accepted: Approved for implementation (may have scheduled window)
- in-progress: Actively being implemented
- implemented: Work merged & deployed (include deployment tag/reference)
- rejected: Reviewed and declined (must include rationale)
- superseded: Replaced by a newer CR (link successor ID)

## Submission Guidelines
Include the following fields in each CR entry:
- ID: Unique incremental integer (CR-1, CR-2, ...)
- Title: Short descriptive summary
- Description: Detailed explanation of the change and motivation
- Impact: Systems, docs, or processes affected
- Risk: Low / Medium / High with short justification
- Dependencies: Other CRs, tasks, or external events
- Owner: Person/team responsible
- Status: Lifecycle state
- Created: YYYY-MM-DD
- Updated: YYYY-MM-DD (last status change)
- Links: Related tasks, issues, PRs
- Decision: (For implemented/rejected/superseded) Summary of decision outcome

## CR Table
| ID | Title | Status | Impact | Risk | Owner | Created | Updated | Links | Decision |
|----|-------|--------|--------|------|-------|---------|---------|-------|----------|
| CR-0 | Example change request | proposed | docs tooling | low | team | 2025-10-11 | 2025-10-11 | - | - |

## Process
1. Propose CR by adding a new row with status `proposed`.
2. Review board evaluates impact, risk, and dependencies; update to `accepted` or `rejected`.
3. When work begins, status -> `in-progress` and link tasks.
4. On completion & deployment, status -> `implemented` with deployment tag.
5. If a CR is superseded, mark `superseded` and link successor CR ID in Decision column.
6. Never delete historical rows; maintain audit trail.

## Decision Log Example
```
CR-3 implemented under release tag v1.2.0. Supersedes CR-1 for logging approach.
```

## Review Cadence
- Weekly review of all `proposed` and `in-progress` CRs.
- Escalate any `accepted` CR stuck >2 weeks without progress.

## Metrics (optional)
Track: number of open CRs, average time from proposed -> implemented, rejection rate.

## Notes
- Use incremental IDs even if earlier CRs are rejected.
- Prefer concise titles (<= 60 chars).
- Link to tasks in `.rdd-docs/tasks/` and PR numbers.
