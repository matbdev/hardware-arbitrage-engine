# Master Implementation Roadmap

## 1. Purpose

This document defines the execution order for evolving the **Hardware Arbitrage Engine** from its current state into a reliable, autonomous, AI-assisted portfolio product.

The roadmap is based on four implementation phases plus one cross-cutting engineering specification:

1. **Stabilization and correctness**
2. **Automation, infrastructure, and operations**
3. **AI appraisal and conversational agent**
4. **Portfolio productization and demonstration**
5. **Cross-cutting engineering standards**

The order is deliberate. Task queues, AI agents, and dashboards must not be built on top of inconsistent business semantics or non-idempotent pipelines.

---

## 2. Product definition

The target product is:

> A data and backend platform that discovers used-hardware listings, normalizes their specifications, calculates market baselines, identifies arbitrage opportunities, evaluates textual risks with AI, and exposes the results through APIs and a demonstrable user interface.

The data pipeline remains the product core. AI enriches the product; it does not replace the deterministic pricing and data-engineering layers.

---

## 3. Architectural target

```text
Marketplace sources
        |
        v
Bronze discovery and extraction
        |
        v
Silver normalization and data quality
        |
        v
Gold baselines, trends, alerts, opportunities
        |
        +----------------------+
        |                      |
        v                      v
AI appraisal worker       FastAPI read API
        |                      |
        v                      v
Gold AI results           Portfolio frontend / chatbot
        |
        v
Metrics, logs, tracing, evaluation results
```

Target operational services:

```text
api
worker
scheduler
postgres
redis
migration
optional-admin-ui
frontend
```

---

## 4. Phase dependency graph

```text
Phase 1: correctness and idempotency
    |
    v
Phase 2: autonomous execution and deployment
    |
    v
Phase 3: AI appraisal and agent
    |
    v
Phase 4: public product and portfolio case study
```

Some Phase 4 documentation work may begin earlier, but the public case study must reflect validated implementation rather than planned capabilities.

---

## 5. Phase gates

### Gate 1 — Reliable engine

Phase 1 is complete only when:

- percentage and score semantics are consistent across pipeline, database, API, OpenAPI, and tests;
- the full Bronze → Silver → Gold path runs successfully against PostgreSQL;
- rerunning the pipeline does not duplicate or corrupt data;
- the system has explicit processing states and pipeline-run records;
- critical PostgreSQL integration tests pass in CI;
- current security and configuration issues are corrected;
- the README accurately separates implemented and planned capabilities.

### Gate 2 — Autonomous service

Phase 2 is complete only when:

- one command starts the complete local stack;
- scheduled execution is handled by Celery Beat;
- pipeline work executes in Celery workers;
- workflows are retryable, observable, and protected against concurrent duplicate runs;
- logs and metrics identify failures by run, task, marketplace, and listing;
- database migrations are applied automatically as a deployment step;
- a deployment environment exposes working health endpoints.

### Gate 3 — Evaluated AI

Phase 3 is complete only when:

- AI output is schema-validated;
- repair costs come from deterministic domain data rather than unsupported model guesses;
- prompts and model versions are persisted;
- a labeled evaluation dataset exists;
- measurable quality, latency, structured-output, and cost results are documented;
- database tools are read-only and allow-listed;
- prompt-injection and untrusted-listing risks are addressed;
- streaming chat works without exposing arbitrary SQL execution.

### Gate 4 — Recruiter-ready product

Phase 4 is complete only when:

- a public demo or recorded reproducible demo exists;
- the project can be understood in less than five minutes;
- screenshots, diagrams, sample outputs, and a short case study are available;
- the README includes setup, architecture, design decisions, limitations, and measurable results;
- seeded demo data allows the product to be evaluated even when scraping sources are unavailable;
- the resume and project description use evidence-based claims.

---

## 6. Priority model

Use the following priority labels:

- **P0 — Blocking correctness:** production claims or later phases are unsafe without it.
- **P1 — Core portfolio value:** strongly improves engineering credibility.
- **P2 — Product completeness:** useful after the critical path is reliable.
- **P3 — Optional extension:** defer unless it supports a specific job target.

### Recommended priority sequence

| Order | Workstream | Priority |
|---:|---|---|
| 1 | Business-unit and score consistency | P0 |
| 2 | Silver pipeline completeness and baseline identifiers | P0 |
| 3 | PostgreSQL compatibility and integration testing | P0 |
| 4 | Idempotency, upserts, and run tracking | P0 |
| 5 | API error/configuration/security corrections | P0 |
| 6 | Baseline quality and net-profit model | P1 |
| 7 | Dockerized API and migration workflow | P1 |
| 8 | Redis, Celery workers, Celery Beat | P1 |
| 9 | Structured logging and metrics | P1 |
| 10 | Public deployment | P1 |
| 11 | Structured AI appraisal | P1 |
| 12 | AI evaluation harness | P1 |
| 13 | Function-calling chatbot | P2 |
| 14 | Portfolio frontend and case study | P1 |
| 15 | Advanced agent workflows | P3 |

---

## 7. Recommended milestone structure

### Milestone M1 — Semantic consistency

Contains:

- `P1-DOMAIN-*`
- `P1-SILVER-*`
- `P1-API-*`

Expected evidence:

- unit tests;
- API examples;
- migration updates;
- documented field definitions.

### Milestone M2 — Reliable PostgreSQL pipeline

Contains:

- `P1-DB-*`
- `P1-IDEMP-*`
- `P1-TEST-*`

Expected evidence:

- CI job using PostgreSQL;
- successful repeated pipeline execution;
- before/after row counts;
- recorded pipeline runs.

### Milestone M3 — Autonomous execution

Contains:

- `P2-CONTAINER-*`
- `P2-QUEUE-*`
- `P2-SCHED-*`

Expected evidence:

- complete Compose stack;
- queued workflow;
- retry demonstration;
- task status endpoint.

### Milestone M4 — Operational readiness

Contains:

- `P2-OBS-*`
- `P2-DEPLOY-*`
- `P2-SEC-*`

Expected evidence:

- structured logs;
- Prometheus metrics;
- live readiness checks;
- deployed API.

### Milestone M5 — AI appraisal

Contains:

- `P3-DATA-*`
- `P3-APPRAISAL-*`
- `P3-EVAL-*`

Expected evidence:

- validated JSON outputs;
- labeled dataset;
- evaluation report;
- cost and latency measurements.

### Milestone M6 — Conversational AI

Contains:

- `P3-TOOLS-*`
- `P3-CHAT-*`
- `P3-SAFETY-*`

Expected evidence:

- tool-call traces;
- streaming response demo;
- read-only permission validation;
- prompt-injection tests.

### Milestone M7 — Portfolio release

Contains:

- `P4-DEMO-*`
- `P4-FRONTEND-*`
- `P4-DOCS-*`
- `P4-CAREER-*`

Expected evidence:

- public URL or video;
- case study;
- architecture diagrams;
- resume bullets and project summary.

---

## 8. Issue sizing

Use relative effort rather than calendar promises:

- **XS:** isolated correction with direct test coverage;
- **S:** one module or one migration;
- **M:** multiple modules with integration tests;
- **L:** cross-service feature;
- **XL:** split into smaller issues before implementation.

No implementation issue should remain XL.

---

## 9. Pull request strategy

Recommended branch flow:

```text
feature/* -> develop -> main
fix/*     -> develop -> main
docs/*    -> develop -> main
```

Each phase should be delivered through multiple focused pull requests. Avoid one pull request that adds Redis, Celery, metrics, Docker, and deployment simultaneously.

A pull request should answer:

1. What problem is being solved?
2. Why is this approach appropriate?
3. What changed?
4. How was it tested?
5. What operational or data risks remain?
6. What evidence demonstrates completion?

---

## 10. Portfolio claim policy

Use three explicit capability states:

- **Implemented:** code exists.
- **Validated:** tests or operational evidence exist.
- **Demonstrated:** a reviewer can observe it in a public or reproducible demo.

Only “demonstrated” capabilities should be highlighted prominently in the project overview.

Example:

```text
Implemented: Celery task definitions.
Validated: retry and idempotency integration tests.
Demonstrated: worker and scheduler visible in the public demo.
```

---

## 11. Explicitly deferred scope

The following items should remain out of scope until a concrete need appears:

- Kubernetes;
- Kafka;
- microservice decomposition;
- GraphQL;
- multiple LLM orchestration frameworks;
- arbitrary SQL generation;
- WebSockets when SSE is sufficient;
- multiple databases for the same responsibility;
- complex authentication before administrative features exist.

These technologies may reduce portfolio clarity if they do not solve a visible requirement.

---

## 12. Final success definition

The final project should allow a reviewer to verify this statement:

> The system starts reproducibly, ingests or seeds data, processes it without duplication, produces explainable arbitrage opportunities, exposes tested APIs, runs autonomously, reports its operational state, uses evaluated AI for textual risk analysis, and presents the result through a clear public demonstration.
