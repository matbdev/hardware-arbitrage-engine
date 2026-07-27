# Cross-Cutting Engineering Standards Specification

## 1. Purpose

This document defines standards that apply across every implementation phase. These are not a separate “cleanup phase.” Each feature must comply when it is introduced.

---

## 2. Definition of Done

A work item is complete only when applicable requirements are satisfied.

### Code

- implementation is focused and readable;
- public functions and domain decisions are documented;
- no dead code or commented-out production flow remains;
- naming matches the data dictionary;
- configuration is not hardcoded.

### Tests

- relevant unit tests exist;
- integration behavior is tested when database, Redis, provider, or network boundaries matter;
- regression test exists for a fixed defect;
- failure path is covered;
- tests are deterministic.

### Data

- natural key is defined;
- rerun behavior is defined;
- nullable behavior is defined;
- unit and range are documented;
- migration exists;
- backfill requirement is addressed.

### API

- schema and example are valid;
- status codes are correct;
- error does not expose internal detail;
- authorization and rate-limit need are evaluated;
- observability context exists.

### Operations

- logs are structured;
- key metrics are emitted;
- timeout and retry policy are defined;
- health impact is understood;
- runbook update exists when needed.

### Documentation

- README or module docs are updated;
- ADR exists for significant decisions;
- current versus planned status is accurate;
- evidence is linked.

---

## 3. Data contracts

Each important field must define:

- semantic meaning;
- type;
- unit;
- allowed range;
- null meaning;
- source;
- calculation;
- version;
- example.

Example:

```text
Field: profit_margin_pct
Type: Decimal
Unit: percentage points
Range: 0 to 100 for promoted opportunities
Null: calculation unavailable
Formula: estimated_net_profit / purchase_price * 100
Version: opportunity-score-v2
```

---

## 4. Money and numeric precision

Use decimal-safe types for monetary calculations.

Rules:

- database: `NUMERIC` with documented precision and scale;
- Python: `Decimal` in domain calculations;
- API: serialize consistently;
- tests: avoid binary floating-point equality for money;
- currency must be explicit;
- rounding policy must be centralized.

---

## 5. Time handling

Rules:

- persist timestamps in UTC;
- expose ISO 8601;
- store source-local time only when necessary;
- distinguish event time from processing time;
- track `first_seen`, `last_seen`, and `processed_at`;
- scheduled task timezone must be explicit.

---

## 6. Database standards

### Required

- migrations for every schema change;
- foreign keys where relationships are real;
- unique constraints for invariants;
- indexes justified by queries;
- named constraints;
- transaction boundaries;
- connection pooling settings by environment;
- read-only role for agent queries.

### Prohibited

- production table creation through `Base.metadata.create_all`;
- silent migration drift;
- production dependence on SQLite-specific behavior;
- destructive migration without backup/backfill plan.

---

## 7. Idempotency standards

Every background or pipeline operation must answer:

1. What is its idempotency key?
2. What happens if it runs twice?
3. What happens if it fails after partial writes?
4. What transaction protects the state?
5. How are stale claims recovered?
6. How is the result versioned?

---

## 8. Logging standards

Use event names rather than prose-only messages.

Example:

```json
{
  "event": "listing_extraction_failed",
  "pipeline_run_id": "...",
  "task_id": "...",
  "marketplace": "olx",
  "ad_id": "...",
  "attempt": 3,
  "error_class": "rate_limited"
}
```

Log levels:

- `DEBUG`: diagnostic development details;
- `INFO`: successful lifecycle events;
- `WARNING`: recoverable abnormal condition;
- `ERROR`: failed operation requiring attention;
- `CRITICAL`: systemic failure.

---

## 9. Error taxonomy

Define stable application error codes.

Categories:

- configuration;
- authentication/authorization;
- validation;
- source network;
- source rate limit;
- source unavailable;
- parsing;
- data quality;
- database;
- task timeout;
- LLM provider;
- LLM validation;
- budget exhausted;
- internal unexpected.

Error codes should be useful in logs, metrics, API responses, and tests.

---

## 10. Security baseline

### Secrets

- never commit;
- never log;
- rotate if exposed;
- use environment/provider secret store;
- document required variables.

### HTTP

- TLS verification enabled;
- external timeouts;
- redirect policy;
- allow-listed outbound hosts where feasible;
- safe user-agent and rate policy.

### API

- least privilege;
- rate limits;
- restricted administrative endpoints;
- safe error responses;
- input size limits;
- request correlation.

### AI

- untrusted content delimiters;
- read-only tools;
- no arbitrary SQL;
- structured output validation;
- evidence grounding;
- prompt/model version tracking;
- personal-data minimization.

---

## 11. Testing pyramid

### Unit

Pure transformations, calculations, parsing, schemas, scoring, and policies.

### Integration

PostgreSQL, Redis, Celery, migrations, API dependencies, provider contracts.

### End to end

Seed data through pipeline to API/frontend.

### Evaluation

AI quality, safety, latency, and cost.

### Manual exploratory

Marketplace page changes and visual experience.

---

## 12. CI quality gates

Recommended jobs:

1. lint and format;
2. unit tests;
3. PostgreSQL integration tests;
4. migration upgrade/downgrade;
5. API contract tests;
6. container build;
7. dependency/security scan;
8. optional frontend tests;
9. optional AI recorded-contract tests.

Pull requests must not merge with failing required jobs.

---

## 13. Architectural decision records

Create an ADR when a decision:

- affects multiple modules;
- changes data semantics;
- introduces infrastructure;
- changes a public contract;
- creates long-term operational cost;
- rejects a plausible alternative.

ADR template:

```text
Title
Status
Context
Decision
Alternatives
Consequences
Validation
Follow-up
```

---

## 14. GitHub issue specification

Each issue should contain:

- problem;
- scope;
- non-goals;
- design notes;
- data/API changes;
- acceptance criteria;
- test plan;
- observability;
- security considerations;
- dependencies;
- evidence required.

---

## 15. Pull request standard

Each PR must include:

- concise summary;
- linked issue;
- screenshots or API examples if applicable;
- migration notes;
- test evidence;
- operational impact;
- rollback or recovery note;
- remaining limitations.

Large PRs should be split by responsibility.

---

## 16. Documentation truthfulness

Use these labels:

- planned;
- experimental;
- implemented;
- validated;
- demonstrated;
- deprecated.

A technology dependency alone does not make a capability implemented.

---

## 17. Performance standards

Measure before optimizing.

For important paths, define:

- dataset size;
- environment;
- p50/p95 latency;
- throughput;
- memory;
- database query count;
- external-call count.

Avoid unsupported claims such as “high performance” or “enterprise grade.”

---

## 18. Data privacy and source ethics

- do not publish seller contact details;
- minimize stored personal information;
- use synthetic or redacted portfolio fixtures;
- document marketplace-source limitations;
- respect access controls and rate limits;
- provide data-retention rules;
- do not imply marketplace affiliation.

---

## 19. Dependency management

- lock dependencies;
- separate runtime and development groups;
- remove unused packages;
- review major upgrades;
- automate update pull requests carefully;
- scan known vulnerabilities;
- document Python-version compatibility.

---

## 20. Release checklist

Before a release:

- migrations tested;
- rollback/recovery documented;
- CI green;
- seed/demo verified;
- API contract reviewed;
- metrics and logs verified;
- secrets checked;
- README reflects current capabilities;
- changelog prepared;
- public demo smoke-tested;
- known limitations documented.
