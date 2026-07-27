# Phase 1 Specification — Stabilization and Corrections

## 1. Objective

Make the current Hardware Arbitrage Engine correct, repeatable, PostgreSQL-compatible, and trustworthy before adding distributed workers or AI features.

This phase addresses defects and architectural gaps already present in the repository. It is not a refactor for style alone; it establishes the invariants required by every later phase.

---

## 2. Completion outcome

At the end of Phase 1:

- one documented command executes the full pipeline against PostgreSQL;
- repeated execution is safe;
- all core business metrics use one consistent unit;
- Gold tables contain current and explainable results;
- API contracts match stored data;
- integration tests exercise PostgreSQL-specific behavior;
- known security and configuration weaknesses are removed;
- the README accurately represents implementation status.

---

## 3. Scope

### Included

- business metric semantics;
- Silver transformation correctness;
- PostgreSQL dialect compatibility;
- idempotency and deduplication;
- data model constraints and migrations;
- pipeline run tracking;
- error handling and configuration;
- API contract corrections;
- test-suite improvements;
- documentation alignment.

### Excluded

- Redis;
- Celery;
- scheduled execution;
- Prometheus deployment;
- LLM appraisal;
- chatbot;
- public frontend.

---

## 4. Domain contracts

### P1-DOMAIN-01 — Standardize percentage representation

**Priority:** P0  
**Effort:** S

#### Problem

`profit_margin_pct` is currently produced as a 0–100 value in the Gold pipeline, while API filters, examples, schemas, and tests treat it as a 0–1 ratio.

#### Decision

Use:

- `profit_margin_pct`: numeric percentage in the inclusive range 0–100;
- `profit_margin_ratio`: do not add unless a downstream use case requires it.

Examples:

```text
25% -> 25.0
7.5% -> 7.5
```

#### Required changes

- update API filter defaults and validation;
- change `min_margin` to `min_margin_pct`;
- update service-layer parameter names;
- update Pydantic descriptions and examples;
- update unit and API tests;
- update OpenAPI query examples;
- document the field in a data dictionary;
- add a database `CHECK` constraint if practical.

#### Acceptance criteria

- `GET /opportunities?min_margin_pct=20` excludes 19.99 and includes 20.00;
- no public interface documents `0.20` as 20%;
- pipeline, ORM, API, tests, and README use the same convention.

---

### P1-DOMAIN-02 — Standardize opportunity score

**Priority:** P0  
**Effort:** S

#### Decision

Use a score from 0 to 100.

#### Required changes

- correct schema description and examples;
- define the meaning of each score component;
- extract scoring logic into a named pure function or dedicated module;
- persist `score_version`;
- add tests for lower and upper bounds;
- ensure clipping is applied once.

#### Proposed initial formula

```text
opportunity_score =
    price_advantage_component
  + condition_component
  + urgency_component
  - known_risk_component
```

The exact weights may remain heuristic in Phase 1, but they must be named and documented.

#### Acceptance criteria

- every score is in the range 0–100;
- a reviewer can identify why a listing received its score;
- score-version changes can be traced.

---

### P1-DOMAIN-03 — Replace gross spread with explicit financial fields

**Priority:** P1  
**Effort:** M

#### Required fields

- `purchase_price`;
- `reference_resale_price`;
- `gross_spread`;
- `estimated_fees`;
- `estimated_shipping_cost`;
- `estimated_refurbish_cost`;
- `risk_reserve`;
- `estimated_net_profit`;
- `estimated_net_margin_pct`.

In Phase 1, optional cost fields may default to zero or configured conservative values, but the schema must distinguish gross spread from net profit.

#### Acceptance criteria

- `potential_profit` is either renamed or clearly documented as gross spread;
- no API field calls median minus purchase price “net profit”;
- net-profit calculation is tested independently.

---

## 5. Silver pipeline correctness

### P1-SILVER-01 — Guarantee baseline identifier generation

**Priority:** P0  
**Effort:** M

#### Problem

The Silver model requires `baseline_id`, while the final Silver DataFrame path must guarantee that it is created and selected before insertion.

#### Required design

Create one deterministic function:

```python
build_baseline_id(
    category,
    brand,
    cpu_brand,
    cpu_model,
    ram_gb,
    storage_gb,
)
```

Rules:

- normalize casing and whitespace;
- replace missing values with explicit tokens;
- avoid locale-dependent formatting;
- generate a stable hash or canonical slug;
- document versioning if the identifier algorithm changes.

#### Required tests

- equal specifications produce the same identifier;
- meaningful specification changes produce different identifiers;
- missing fields do not crash generation;
- reordered input labels do not change the identifier.

#### Acceptance criteria

- every Silver record eligible for a baseline has a non-null `baseline_id`;
- the Gold dimension pipeline does not create duplicate configurations.

---

### P1-SILVER-02 — Correct memory and storage normalization

**Priority:** P0  
**Effort:** M

#### Required behavior

Normalize:

- MB to GB;
- GB to GB;
- TB to GB;
- decimal values such as `1.5 TB`;
- common localized formats;
- SSD/HDD/NVMe text without allowing the medium label to affect capacity parsing.

Examples:

```text
512 MB -> 0.5 GB
16 GB -> 16 GB
1 TB -> 1024 GB
1.5 TB -> 1536 GB
```

#### Required implementation

Move parsing into pure functions and test them with parametrized cases.

#### Acceptance criteria

- no `1 TB` listing is stored as `1 GB`;
- invalid or ambiguous values produce `None` plus a data-quality reason;
- parsing tests contain real examples captured from marketplace data.

---

### P1-SILVER-03 — Define missing-value and quality policy

**Priority:** P1  
**Effort:** M

Introduce:

- `data_quality_status`;
- `data_quality_issues`;
- `spec_extraction_confidence`;
- explicit distinction between `unknown`, `not applicable`, and numeric zero.

A missing RAM value must not be stored as `0 GB` unless zero is a valid business value.

#### Acceptance criteria

- Gold baselines exclude records below the agreed quality threshold;
- API responses can expose why a listing was excluded or considered low-confidence.

---

### P1-SILVER-04 — Remove dynamic-schema fragility from one-hot features

**Priority:** P1  
**Effort:** M

Dynamic one-hot columns derived from arbitrary listing characteristics can change between runs and break inserts.

Choose one:

1. store normalized features in JSON/JSONB;
2. maintain an allow-listed fixed set of feature columns;
3. use a child table for listing features.

Recommended for this project: fixed high-value columns plus JSONB for uncommon features.

#### Acceptance criteria

- new marketplace characteristic text cannot cause a database-column mismatch;
- schema migrations are not required for every new characteristic.

---

## 6. PostgreSQL compatibility and schema design

### P1-DB-01 — Replace SQLite-specific upsert code

**Priority:** P0  
**Effort:** S

Use PostgreSQL dialect inserts in PostgreSQL execution paths:

```python
from sqlalchemy.dialects.postgresql import insert
```

Alternatively, create an explicit repository abstraction if SQLite must remain a supported runtime.

#### Acceptance criteria

- product-dimension upsert executes against PostgreSQL;
- integration test validates `ON CONFLICT`;
- no production pipeline imports `sqlalchemy.dialects.sqlite`.

---

### P1-DB-02 — Align ORM types and migrations

**Priority:** P0  
**Effort:** M

Audit:

- `ram_gb` and `storage_gb`;
- date versus timestamp;
- nullable fields;
- JSON versus JSONB;
- monetary values;
- foreign keys;
- unique constraints;
- indexes.

Use `Numeric`/`Decimal` for monetary values where precision matters.

Recommended constraints:

- unique marketplace listing key;
- foreign key from Gold opportunity to product dimension;
- checks for non-negative prices;
- checks for percentage and score ranges.

#### Acceptance criteria

- ORM metadata and latest Alembic migration produce the same schema;
- autogenerate produces no unexplained drift;
- migration upgrade and downgrade are tested in a temporary database.

---

### P1-DB-03 — Stop ignoring required migration configuration

**Priority:** P1  
**Effort:** S

Do not rely on an untracked `alembic.ini` without a documented template.

Choose:

- commit a safe `alembic.ini` with environment-driven URL; or
- commit `alembic.ini.example` and document the copy step.

No secrets should be stored in the file.

#### Acceptance criteria

- a fresh clone can run migrations using documented commands;
- CI does not depend on a developer-local configuration file.

---

## 7. Idempotency and execution state

### P1-IDEMP-01 — Define listing lifecycle fields

**Priority:** P0  
**Effort:** M

Add or confirm:

- `first_seen_at`;
- `last_seen_at`;
- `last_checked_at`;
- `available`;
- `source_status`;
- `extraction_status`;
- `extraction_attempts`;
- `last_error`;
- `processed_at`.

Suggested statuses:

```text
pending
processing
processed
retryable_failed
permanently_failed
unavailable
```

#### Acceptance criteria

- extraction selects pending or retryable records, not the first arbitrary 100;
- sold or removed listings retain history;
- failures are inspectable.

---

### P1-IDEMP-02 — Make every pipeline stage rerunnable

**Priority:** P0  
**Effort:** L

For each stage, document:

- natural key;
- read set;
- write set;
- upsert policy;
- stale-record policy;
- transaction boundary;
- safe retry behavior.

#### Stage requirements

**Discovery**

- upsert by marketplace and external listing identifier or canonical URL;
- update `last_seen_at`;
- do not duplicate a known listing.

**Extraction**

- claim records atomically;
- persist attempts and errors;
- update existing extraction snapshots or append versioned snapshots according to the selected history model.

**Silver**

- merge by listing and observation date;
- update transformed values when parser version changes.

**Gold**

- replace or upsert current baselines;
- preserve historical trend snapshots;
- recompute opportunities deterministically.

#### Acceptance criteria

Running the same pipeline twice with unchanged source data:

- does not increase duplicate counts;
- does not fail on primary or unique keys;
- produces equivalent current-state Gold results.

---

### P1-IDEMP-03 — Add pipeline-run tables

**Priority:** P0  
**Effort:** M

Create:

```text
pipeline_run
pipeline_task_run
```

Minimum fields:

- run identifier;
- pipeline name;
- stage;
- status;
- started and finished timestamps;
- records read;
- records written;
- records skipped;
- records failed;
- error summary;
- code version or commit SHA;
- trigger type;
- configuration snapshot or hash.

#### Acceptance criteria

- every manual full-pipeline execution creates a run;
- failed stages are visible without reading console output;
- later Celery tasks can reuse the same model.

---

## 8. Gold-layer data quality

### P1-GOLD-01 — Define baseline time window and minimum sample

**Priority:** P1  
**Effort:** M

The current “latest listing date” approach may calculate a median from a very small or unrepresentative sample.

Define:

- rolling window, for example recent active observations;
- minimum sample count;
- regional segmentation;
- condition segmentation;
- outlier policy;
- stale baseline policy.

Persist:

- sample count;
- window start and end;
- percentile values;
- standard deviation or robust dispersion;
- baseline confidence;
- calculation version.

#### Acceptance criteria

- a baseline with insufficient sample size is marked low-confidence or unavailable;
- opportunities are not promoted solely from one anomalous listing.

---

### P1-GOLD-02 — Add robust outlier handling

**Priority:** P1  
**Effort:** M

Select and document one approach:

- IQR;
- median absolute deviation;
- percentile clipping;
- domain thresholds.

Store both raw and filtered sample counts.

#### Acceptance criteria

- tests demonstrate that extreme listings do not dominate the baseline;
- the selected approach is explained in an ADR.

---

### P1-GOLD-03 — Version transformations and scores

**Priority:** P1  
**Effort:** S

Add:

- `pipeline_version`;
- `baseline_version`;
- `score_version`;
- optional `parser_version`.

#### Acceptance criteria

- a stored opportunity can be traced to the calculation rules that generated it.

---

## 9. API and configuration corrections

### P1-API-01 — Standardize error responses

**Priority:** P0  
**Effort:** M

Create a global error model:

```json
{
  "code": "OPPORTUNITY_QUERY_FAILED",
  "message": "Unable to retrieve opportunities.",
  "correlation_id": "...",
  "details": null
}
```

Rules:

- validation errors remain 422;
- client mistakes use 400 or 404;
- unexpected database failures use 500 or 503;
- internal exception strings are not exposed;
- full exception context is logged.

#### Acceptance criteria

- a simulated database outage returns a safe 503 response;
- logs contain the correlation identifier and exception.

---

### P1-API-02 — Restrict CORS

**Priority:** P0  
**Effort:** S

Load allowed origins from configuration.

Do not use wildcard origins with credentials.

#### Acceptance criteria

- local development origin is configurable;
- unapproved origins are rejected in integration tests.

---

### P1-API-03 — Re-enable TLS verification

**Priority:** P0  
**Effort:** S

Remove `verify=False` as the default.

If a corporate certificate is required, expose a CA bundle setting.

#### Acceptance criteria

- production configuration verifies TLS;
- insecure mode requires an explicit development-only flag;
- the flag is documented as unsafe.

---

### P1-API-04 — Centralize typed settings

**Priority:** P1  
**Effort:** M

Use a typed settings object for:

- environment;
- database URL;
- allowed origins;
- HTTP timeouts;
- concurrency;
- scraping limits;
- logging level;
- external-service credentials;
- feature flags.

Recommended: `pydantic-settings`.

#### Acceptance criteria

- application startup fails clearly when required production settings are absent;
- secrets do not have insecure production defaults.

---

### P1-API-05 — Correct response schemas and naming

**Priority:** P0  
**Effort:** M

Audit all:

- examples;
- units;
- optional fields;
- score ranges;
- money descriptions;
- naming inconsistencies;
- typo `avaliable`.

#### Acceptance criteria

- OpenAPI examples pass Pydantic validation;
- contract tests compare endpoint responses with schemas.

---

## 10. Testing and CI

### P1-TEST-01 — Add PostgreSQL service tests

**Priority:** P0  
**Effort:** L

Run integration tests against PostgreSQL in CI using either:

- a GitHub Actions service container; or
- Testcontainers.

Test:

- schema migrations;
- PostgreSQL upserts;
- schema-qualified tables;
- JSONB behavior;
- constraints;
- transaction rollbacks;
- full service queries.

Keep SQLite only for fast isolated tests where dialect behavior is irrelevant.

#### Acceptance criteria

- CI has a distinct PostgreSQL integration job;
- a SQLite-only passing suite cannot mask PostgreSQL incompatibility.

---

### P1-TEST-02 — Add end-to-end pipeline fixture

**Priority:** P0  
**Effort:** L

Create deterministic fixture data representing:

- valid listing;
- duplicate listing;
- unavailable listing;
- 1 TB storage;
- missing specifications;
- repair keywords;
- urgent-sale keywords;
- extreme outlier;
- two observations of the same listing.

Execute Bronze fixture load → Silver → Gold.

#### Acceptance criteria

- expected opportunities and baselines are asserted;
- rerun produces no duplicates;
- results are deterministic.

---

### P1-TEST-03 — Add coverage and quality gates

**Priority:** P1  
**Effort:** M

Add:

- coverage report;
- minimum threshold focused on production modules;
- formatting check;
- stronger Ruff rule set;
- optional static type checking;
- migration drift check.

Do not optimize for an arbitrary 100% coverage target. Cover critical behavior.

---

### P1-TEST-04 — Add regression tests for discovered defects

**Priority:** P0  
**Effort:** S

Every fixed defect in this phase must receive a regression test.

Required initial cases:

- percentage scale;
- score scale;
- `baseline_id`;
- TB conversion;
- PostgreSQL upsert;
- CORS;
- TLS configuration;
- error-response safety;
- `available` spelling;
- repeated pipeline execution.

---

## 11. Documentation corrections

### P1-DOCS-01 — Separate current and planned capabilities

**Priority:** P0  
**Effort:** S

README sections:

- What works now;
- Architecture;
- How to run;
- How to test;
- API examples;
- Current limitations;
- Roadmap.

Badges must not imply a completed capability that only exists as a plan or dependency.

---

### P1-DOCS-02 — Add data dictionary

**Priority:** P1  
**Effort:** M

Document for key Gold fields:

- name;
- type;
- unit;
- nullable behavior;
- calculation;
- source;
- version;
- example.

---

### P1-DOCS-03 — Add architecture decision records

**Priority:** P1  
**Effort:** M

Minimum ADRs:

1. percentage and score units;
2. baseline identifier design;
3. PostgreSQL as production database;
4. idempotency strategy;
5. baseline outlier method;
6. money precision;
7. feature-storage model.

---

## 12. Required deliverables

- updated ORM models;
- Alembic migrations;
- corrected pipelines;
- corrected API contracts;
- typed settings;
- PostgreSQL integration-test job;
- end-to-end fixture test;
- pipeline-run tables;
- data dictionary;
- ADRs;
- updated README;
- Phase 1 completion report with evidence.

---

## 13. Definition of Done

Phase 1 is done only when all P0 items are complete and:

```text
1. Fresh clone
2. Start PostgreSQL
3. Apply migrations
4. Load deterministic fixture
5. Run full pipeline
6. Run full pipeline again
7. Query API
8. Execute tests
```

All steps complete successfully, and the second pipeline execution does not create duplicates or inconsistent current-state results.
