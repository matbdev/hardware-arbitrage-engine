# Phase 2 Specification — Automation, Infrastructure, and Operations

## 1. Objective

Convert the reliable Phase 1 engine into an autonomous backend service using containerized infrastructure, Redis, Celery workers, Celery Beat scheduling, structured logs, metrics, and a deployment workflow.

This phase must preserve the data invariants established in Phase 1.

---

## 2. Completion outcome

At the end of Phase 2:

- one command starts the complete local platform;
- scheduled workflows run without blocking the API;
- tasks are retryable and idempotent;
- concurrent duplicate workflows are prevented;
- every workflow has visible status and metrics;
- logs contain correlation and pipeline identifiers;
- migrations run as a controlled deployment step;
- a deployed environment exposes liveness, readiness, metrics, and API documentation.

---

## 3. Technology decision

Use:

- **Redis** as Celery broker and short-lived result backend;
- **Celery** for task execution;
- **Celery Beat** for schedules.

Do not add APScheduler in parallel unless a separate embedded scheduling use case is documented.

---

## 4. Target services

```text
api            FastAPI application
worker         Celery worker
scheduler      Celery Beat
postgres       primary relational database
redis          broker and optional result backend
migration      one-shot Alembic upgrade service
adminer        optional local-only database interface
frontend       optional in Phase 2, required in Phase 4
```

---

## 5. Containerization

### P2-CONTAINER-01 — Create production-oriented Dockerfile

**Priority:** P1  
**Effort:** M

Requirements:

- multi-stage build;
- dependency installation with `uv`;
- locked dependencies;
- non-root runtime user;
- minimal runtime image;
- explicit application command;
- healthcheck support;
- no copied `.env`;
- build metadata labels;
- predictable Python path.

#### Acceptance criteria

- image builds from a clean checkout;
- container runs without root;
- vulnerability scan has no unresolved critical findings attributable to project configuration;
- image startup does not run development reload mode.

---

### P2-CONTAINER-02 — Build complete Compose stack

**Priority:** P1  
**Effort:** L

Required services:

- API;
- PostgreSQL;
- Redis;
- worker;
- scheduler;
- migration.

Required features:

- healthchecks;
- dependency health conditions;
- named volumes;
- internal network;
- restart policy;
- environment file support;
- local-only database/admin ports where appropriate;
- separate commands per service.

#### Acceptance criteria

```bash
docker compose up --build
```

results in:

- migrations applied;
- API ready;
- worker connected;
- Beat publishing scheduled jobs;
- PostgreSQL and Redis healthy.

---

### P2-CONTAINER-03 — Add deterministic seed profile

**Priority:** P1  
**Effort:** M

Add a profile or command to load safe demonstration data.

The seed must:

- contain no personal data;
- be deterministic;
- exercise Bronze, Silver, Gold, and API outputs;
- remain usable when marketplace scraping is unavailable.

---

## 6. Celery architecture

### P2-QUEUE-01 — Create Celery application configuration

**Priority:** P1  
**Effort:** M

Configure:

- broker URL;
- result backend policy;
- JSON serialization only;
- timezone;
- acknowledgment behavior;
- task time limits;
- prefetch strategy;
- retry defaults;
- queue names;
- worker concurrency through settings.

Recommended queues:

```text
discovery
extraction
transform
ai
maintenance
```

The `ai` queue may be created now but used in Phase 3.

---

### P2-QUEUE-02 — Convert pipeline stages into tasks

**Priority:** P1  
**Effort:** L

Tasks:

- `discover_listings`;
- `extract_pending_listings`;
- `run_silver_transform`;
- `calculate_product_dimensions`;
- `calculate_market_baselines`;
- `calculate_market_trends`;
- `calculate_price_drop_alerts`;
- `calculate_arbitrage_opportunities`;
- `finalize_pipeline_run`.

Each task must accept a `pipeline_run_id`.

#### Acceptance criteria

- tasks can be invoked independently for testing;
- task state is persisted in the database;
- task retry does not duplicate data.

---

### P2-QUEUE-03 — Implement workflow orchestration

**Priority:** P1  
**Effort:** L

Recommended workflow:

```text
discovery
  -> extraction batches
  -> silver
  -> product dimensions
  -> baselines
  -> trends
  -> alerts
  -> opportunities
  -> finalize
```

Use Celery chains, groups, or chords only where they improve the workflow.

Extraction may use parallel batches, but Gold execution must respect dependencies.

#### Acceptance criteria

- a failed stage prevents invalid dependent stages from running;
- retrying a failed stage resumes or safely recomputes according to documented policy;
- final run status is correct.

---

### P2-QUEUE-04 — Implement atomic task claiming

**Priority:** P0  
**Effort:** L

For extraction records:

- select pending records with row locking;
- use `SKIP LOCKED` where appropriate;
- mark records processing in the same transaction;
- attach worker/task identifier;
- release or retry stale claims.

#### Acceptance criteria

- two workers do not process the same listing simultaneously;
- worker termination leaves records recoverable.

---

### P2-QUEUE-05 — Implement retries and failure classification

**Priority:** P1  
**Effort:** M

Classify failures:

- transient network;
- rate limit;
- source unavailable;
- parser defect;
- data constraint;
- configuration error;
- permanent listing removal.

Policies:

- exponential backoff with jitter for transient errors;
- respect `Retry-After`;
- maximum attempts;
- no retry for known permanent conditions;
- safe error summaries in database;
- full stack trace in logs.

---

### P2-QUEUE-06 — Add distributed workflow lock

**Priority:** P0  
**Effort:** M

Prevent overlapping full-pipeline runs.

Options:

- PostgreSQL advisory lock;
- Redis lock with carefully defined expiry and ownership;
- database run-state uniqueness constraint.

Recommended: PostgreSQL advisory lock or database uniqueness for source-of-truth correctness.

#### Acceptance criteria

- scheduler cannot create two active full runs;
- manual override is explicit and audited.

---

## 7. Scheduling

### P2-SCHED-01 — Configure Celery Beat schedules

**Priority:** P1  
**Effort:** M

Initial schedules:

- discovery: every 30 minutes;
- extraction: every hour or after discovery;
- full Silver/Gold refresh: after extraction workflow completion;
- unavailable-listing recheck: daily;
- cleanup/maintenance: daily.

Schedules must be settings-driven.

#### Acceptance criteria

- changes do not require code edits;
- schedules are documented;
- development can disable automatic schedules.

---

### P2-SCHED-02 — Define marketplace-aware rate controls

**Priority:** P1  
**Effort:** M

Configure per source:

- request rate;
- concurrency;
- timeout;
- retry limits;
- user agent policy;
- cool-down after 403/429.

The scheduler must not imply permission to ignore marketplace terms or access restrictions.

---

## 8. Task and run API

### P2-API-01 — Add pipeline run endpoints

**Priority:** P1  
**Effort:** M

Endpoints:

- `POST /api/v1/pipeline-runs` — trigger authorized manual run;
- `GET /api/v1/pipeline-runs`;
- `GET /api/v1/pipeline-runs/{run_id}`;
- `GET /api/v1/pipeline-runs/{run_id}/tasks`;
- optional `POST /api/v1/pipeline-runs/{run_id}/retry`.

Administrative endpoints require authentication or development-only protection before public deployment.

---

### P2-API-02 — Improve readiness checks

**Priority:** P1  
**Effort:** M

Readiness should verify:

- database connection;
- migration revision;
- Redis connection;
- optional worker heartbeat freshness.

Liveness must remain lightweight and not depend on external services.

---

## 9. Observability

### P2-OBS-01 — Structured JSON logging

**Priority:** P1  
**Effort:** M

Every log event should support:

- timestamp;
- level;
- service;
- environment;
- correlation ID;
- pipeline run ID;
- Celery task ID;
- marketplace;
- listing/ad ID;
- event name;
- duration;
- safe error details.

Do not log:

- API keys;
- passwords;
- full sensitive configuration;
- raw personal data.

---

### P2-OBS-02 — Correlation propagation

**Priority:** P1  
**Effort:** M

Propagate identifiers through:

```text
API request -> pipeline run -> Celery workflow -> task -> database record
```

#### Acceptance criteria

A failure can be traced from API response or run record to the exact worker logs.

---

### P2-OBS-03 — Prometheus metrics

**Priority:** P1  
**Effort:** L

Required metric families:

**HTTP**

- request count;
- latency histogram;
- status codes;
- in-progress requests.

**Scraping**

- listings discovered;
- listings extracted;
- duplicate listings;
- 403/404/410/429 responses;
- retries;
- extraction duration.

**Pipeline**

- records read/written/skipped/failed;
- stage duration;
- successful and failed runs;
- active run age;
- baseline freshness.

**Celery**

- queued tasks;
- active tasks;
- success/failure/retry count;
- task latency and duration.

**Business**

- opportunities generated;
- median estimated margin;
- high-confidence baseline count;
- low-confidence opportunity count.

---

### P2-OBS-04 — Operational dashboard

**Priority:** P2  
**Effort:** M

Provide either:

- Grafana dashboard; or
- a small internal status page using the metrics API.

Required views:

- current pipeline status;
- last successful run;
- error rates;
- source health;
- opportunity count;
- baseline freshness.

---

### P2-OBS-05 — Define service objectives

**Priority:** P2  
**Effort:** S

Initial internal SLO examples:

- API readiness over the demo period;
- successful scheduled run percentage;
- maximum age of current baselines;
- maximum permanent extraction failure percentage.

These are engineering targets, not contractual guarantees.

---

## 10. Security and configuration

### P2-SEC-01 — Secret management policy

**Priority:** P1  
**Effort:** M

Requirements:

- `.env.example`;
- no credentials in Git;
- separate development and production values;
- rotation procedure;
- deployment secret store;
- log redaction.

---

### P2-SEC-02 — Administrative API protection

**Priority:** P1  
**Effort:** M

Before public deployment, protect:

- manual pipeline triggers;
- retries;
- worker/debug endpoints;
- operational details.

A simple API key or OAuth-based admin flow is sufficient depending on deployment scope. Public read-only opportunity endpoints may remain open with rate limiting.

---

### P2-SEC-03 — Rate limiting

**Priority:** P2  
**Effort:** M

Apply to:

- public API;
- chat endpoint in Phase 3;
- manual trigger endpoints;
- expensive analytical queries.

---

## 11. CI/CD and deployment

### P2-CI-01 — Container build pipeline

**Priority:** P1  
**Effort:** M

CI must:

- build image;
- run tests;
- run migrations against temporary PostgreSQL;
- optionally scan dependencies and image;
- publish tagged image for main releases.

---

### P2-CI-02 — Migration deployment step

**Priority:** P1  
**Effort:** M

Migrations must run before new application instances serve traffic.

Requirements:

- one-shot migration job;
- failure blocks deployment;
- revision visible in readiness;
- rollback plan documented.

---

### P2-DEPLOY-01 — Deploy public API environment

**Priority:** P1  
**Effort:** L

Required:

- HTTPS;
- environment-specific CORS;
- managed or persisted PostgreSQL;
- Redis;
- API;
- worker;
- scheduler;
- logs;
- health endpoints.

The selected provider is secondary to reproducibility and evidence.

---

### P2-DEPLOY-02 — Backup and recovery basics

**Priority:** P2  
**Effort:** M

Document:

- database backup;
- retention;
- restore test;
- what data can be reconstructed by rerunning pipelines;
- what data is irreplaceable.

---

## 12. Testing requirements

### Unit tests

- task configuration;
- retry classification;
- schedule parsing;
- metrics labels;
- lock behavior helpers.

### Integration tests

- Celery eager mode for workflow logic;
- real Redis for broker-sensitive tests where practical;
- PostgreSQL task claiming;
- duplicate-worker protection;
- migration service;
- readiness dependencies.

### Failure tests

- worker crash;
- Redis unavailable;
- PostgreSQL unavailable;
- 429 source response;
- malformed source data;
- stale processing claim;
- duplicate scheduled run.

### Load smoke tests

Measure:

- opportunity list endpoint;
- pipeline run status endpoint;
- a realistic extraction batch;
- worker throughput under configured concurrency.

---

## 13. Required deliverables

- multi-stage Dockerfile;
- complete Compose stack;
- Celery app;
- stage tasks;
- Beat schedule;
- workflow orchestration;
- distributed lock;
- task/run API;
- structured logs;
- metrics endpoint;
- deployment workflow;
- deployed environment;
- operations runbook;
- Phase 2 evidence report.

---

## 14. Definition of Done

Phase 2 is done when a reviewer can:

1. start the stack with one command;
2. observe healthy API, PostgreSQL, Redis, worker, and scheduler;
3. trigger or wait for a pipeline run;
4. inspect task progress;
5. observe a controlled retry;
6. confirm a duplicate run is blocked;
7. view metrics and correlated logs;
8. query updated opportunities;
9. access a deployed API environment.
