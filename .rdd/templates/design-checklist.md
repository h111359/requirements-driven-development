## Design Checklist (use to identify coverage gaps):

### Architecture

- [ ] Architecture & System Boundaries are defined. The system components, layering, runtime topology should be defined

- [ ] Assumptions & Constraints Catalogue (external dependencies, boundaries) is defined in `.rdd-docs/tech-spec.md`
  
- [ ] Key Design Decisions list (alternatives, rationale, trade-offs, implications) is defined in `.rdd-docs/tech-spec.md`  

- [ ] Technical Debt Tracking list (deferred items, payoff criteria) is defined in `.rdd-docs/tech-spec.md`

### Data

- [ ] Domain Model & Data Model are defined in '.rdd-docs/data-model.md' - (entities, aggregates, relationships, metadata)

- [ ] Data Flows & Integration Contracts (sync/async, protocols, schemas) are defined in `.rdd-docs/tech-spec.md`

- [ ] Consistency & Transactions policies (isolation levels, eventual vs strong, idempotency) are defined in `.rdd-docs/tech-spec.md`

- [ ] Concurrency & Locking rules (optimistic/pessimistic, contention strategy) are defined in `.rdd-docs/tech-spec.md`

- [ ] Storage Strategy (databases, indexing, partitioning, archival, cold storage) are defined in `.rdd-docs/tech-spec.md`

- [ ] Data Quality & Validation strategy (constraints, sanitization, integrity rules) are defined in `.rdd-docs/tech-spec.md`

- [ ] Internationalization & Localization strategy (formats, language support) is defined in `.rdd-docs/tech-spec.md`

- [ ] Backup & Restore / Disaster Recovery Strategy (RPO, RTO, test cadence) is defined in `.rdd-docs/tech-spec.md`
  
- [ ] Data Migration & Evolution strategy (versioning, backward compatibility, cutover) is defined in `.rdd-docs/tech-spec.md`

- [ ] Data Archival and Data Lifecycle strategy (legal hold, retrieval workflows) is defined in `.rdd-docs/tech-spec.md`

- [ ] Master Data & Reference Data Management strategy (governance, stewardship) is defined in `.rdd-docs/tech-spec.md`

- [ ] Data Pipeline & ETL Orchestration strategy (scheduling, lineage, recovery) is defined in `.rdd-docs/tech-spec.md`


### Security, Privacy

- [ ] Security & Identity aspects (authN, authZ, secrets, encryption, key rotation) are defined in `.rdd-docs/tech-spec.md`

- [ ] Privacy & Compliance principles (PII, GDPR, retention, data minimization) are defined in `.rdd-docs/tech-spec.md`

### Performance, Scalability, Reliability

- [ ] Performance & Capacity assumptions (latency, throughput, sizing assumptions) are defined in `.rdd-docs/tech-spec.md`

- [ ] Scalability & Elasticity strategy (horizontal/vertical strategies, auto-scaling triggers) are defined in `.rdd-docs/tech-spec.md`

- [ ] Reliability & Availability strategies (HA patterns, redundancy, failover) are defined in `.rdd-docs/tech-spec.md`

- [ ] Resilience & Fault Tolerance (circuit breakers, retries, backoff, bulkheads) is defined in `.rdd-docs/tech-spec.md`


- [ ] State Management & Caching Strategy strategy (layers, invalidation, TTL) are defined in `.rdd-docs/tech-spec.md`

### Observability

- [ ] Observability strategy (logging, metrics, tracing, dashboards, alerting) is defined in `.rdd-docs/tech-spec.md`
  
- [ ] Monitoring KPIs / SLIs / SLOs strategy (definitions, thresholds, error budgets) is defined in `.rdd-docs/tech-spec.md`
  
- [ ] Operational Runbooks & Incident Response strategy (escalation, triage steps) is defined in `.rdd-docs/tech-spec.md`
  
### Development and Deployment
  
- [ ] Lifecycle Events strategy (startup, upgrades, decommission, end-of-life) is defined in `.rdd-docs/tech-spec.md`

- [ ] Release Strategy (branching, tagging, canary, blue/green, rollback, CI/CD, code generation, scripts) is defined in `.rdd-docs/tech-spec.md`
  
- [ ] Deployment & Runtime strategy (environments, IaC, containers, orchestration) is defined in `.rdd-docs/tech-spec.md`
  
- [ ] Environment Parity & Configuration Management strategy (dev/stage/prod consistency) is defined in `.rdd-docs/tech-spec.md`
  
- [ ] Dependency Management & External Services strategy (versioning, SLAs, fallbacks) is defined in `.rdd-docs/tech-spec.md`

- [ ] Test Strategy (unit, integration, contract, e2e, performance, chaos) is defined in `.rdd-docs/tech-spec.md`

- [ ] Code Standards & Static Analysis strategy (linting, formatting, coverage) is defined in `.rdd-docs/tech-spec.md`

### Governance

- [ ] Governance & Compliance Controls strategy (audit logging, change tracking) is defined in `.rdd-docs/tech-spec.md`

- [ ] Cost Optimization & Resource Efficiency strategy (utilization, scaling thresholds) is defined in `.rdd-docs/tech-spec.md`


  






- [ ] AI/ML Model Lifecycle & MLOps (training, drift detection, rollback)

- [ ] Knowledge Management & Documentation (KB curation, feedback loop)

- [ ] User Training & Adoption (enablement plan, competency tracking)

- [ ] Onboarding & Offboarding Automation (accounts, access revocation)

- [ ] Secret & Credential Scanning (repository monitoring, rotation triggers)

