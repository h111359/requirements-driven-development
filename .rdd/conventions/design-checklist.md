## Design Checklist (use to identify coverage gaps):

### Architecture

- [ ] Architecture & System Boundaries are defined. The system components, layering, runtime topology should be defined

- [ ] Assumptions & Constraints Catalogue (external dependencies, boundaries) is defined
  
- [ ] Key Design Decisions list (alternatives, rationale, trade-offs, implications) is defined

- [ ] Technical Debt Tracking list (deferred items, payoff criteria) is defined

### Data

- [ ] Domain Model & Data Model are defined in '.rdd-instance/data-model.md' - (entities, aggregates, relationships, metadata)

- [ ] Data Flows & Integration Contracts (sync/async, protocols, schemas) are defined

- [ ] Consistency & Transactions policies (isolation levels, eventual vs strong, idempotency) are defined

- [ ] Concurrency & Locking rules (optimistic/pessimistic, contention strategy) are defined

- [ ] Storage Strategy (databases, indexing, partitioning, archival, cold storage) are defined

- [ ] Data Quality & Validation strategy (constraints, sanitization, integrity rules) are defined

- [ ] Internationalization & Localization strategy (formats, language support) is defined

- [ ] Backup & Restore / Disaster Recovery Strategy (RPO, RTO, test cadence) is defined
  
- [ ] Data Migration & Evolution strategy (versioning, backward compatibility, cutover) is defined

- [ ] Data Archival and Data Lifecycle strategy (legal hold, retrieval workflows) is defined

- [ ] Master Data & Reference Data Management strategy (governance, stewardship) is defined

- [ ] Data Pipeline & ETL Orchestration strategy (scheduling, lineage, recovery) is defined


### Security, Privacy

- [ ] Security & Identity aspects (authN, authZ, secrets, encryption, key rotation) are defined

- [ ] Privacy & Compliance principles (PII, GDPR, retention, data minimization) are defined

### Performance, Scalability, Reliability

- [ ] Performance & Capacity assumptions (latency, throughput, sizing assumptions) are defined

- [ ] Scalability & Elasticity strategy (horizontal/vertical strategies, auto-scaling triggers) are defined

- [ ] Reliability & Availability strategies (HA patterns, redundancy, failover) are defined

- [ ] Resilience & Fault Tolerance (circuit breakers, retries, backoff, bulkheads) is defined


- [ ] State Management & Caching Strategy strategy (layers, invalidation, TTL) are defined

### Observability

- [ ] Observability strategy (logging, metrics, tracing, dashboards, alerting) is defined
  
- [ ] Monitoring KPIs / SLIs / SLOs strategy (definitions, thresholds, error budgets) is defined
  
- [ ] Operational Runbooks & Incident Response strategy (escalation, triage steps) is defined
  
### Development and Deployment
  
- [ ] Lifecycle Events strategy (startup, upgrades, decommission, end-of-life) is defined

- [ ] Release Strategy (branching, tagging, canary, blue/green, rollback, CI/CD, code generation, scripts) is defined
  
- [ ] Deployment & Runtime strategy (environments, IaC, containers, orchestration) is defined
  
- [ ] Environment Parity & Configuration Management strategy (dev/stage/prod consistency) is defined
  
- [ ] Dependency Management & External Services strategy (versioning, SLAs, fallbacks) is defined

- [ ] Test Strategy (unit, integration, contract, e2e, performance, chaos) is defined

- [ ] Code Standards & Static Analysis strategy (linting, formatting, coverage) is defined

### Governance

- [ ] Governance & Compliance Controls strategy (audit logging, change tracking) is defined

- [ ] Cost Optimization & Resource Efficiency strategy (utilization, scaling thresholds) is defined


  






- [ ] AI/ML Model Lifecycle & MLOps (training, drift detection, rollback)

- [ ] Knowledge Management & Documentation (KB curation, feedback loop)

- [ ] User Training & Adoption (enablement plan, competency tracking)

- [ ] Onboarding & Offboarding Automation (accounts, access revocation)

- [ ] Secret & Credential Scanning (repository monitoring, rotation triggers)

