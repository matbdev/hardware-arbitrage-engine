# Phase 4 Specification — Portfolio Productization and Demonstration

## 1. Objective

Transform the technically complete backend into a project that recruiters and engineering managers can understand, run, and evaluate quickly.

This phase exists because strong code alone is often invisible. The portfolio must show the problem, architecture, decisions, evidence, and working result.

---

## 2. Completion outcome

At the end of Phase 4:

- the system has a public or reproducible demonstration;
- a reviewer can understand the product in less than five minutes;
- a minimal frontend exposes the most valuable workflows;
- seeded data protects the demo from scraper instability;
- the README contains evidence rather than only technology names;
- a case study explains trade-offs and measurable outcomes;
- resume and interview material are ready.

---

## 3. Product experience

### P4-DEMO-01 — Define primary demo journey

**Priority:** P1  
**Effort:** S

The main journey should be:

1. open dashboard;
2. view current opportunities;
3. filter by budget, category, margin, and risk;
4. open an opportunity;
5. compare listing price with market baseline;
6. inspect AI risk evidence and estimated costs;
7. ask the assistant for recommendations;
8. view pipeline freshness and last update.

Do not expose every internal table as a primary interface.

---

### P4-DEMO-02 — Create demo mode

**Priority:** P1  
**Effort:** M

Demo mode must:

- use deterministic seeded data;
- clearly label synthetic or snapshot data;
- work without live scraping;
- allow the AI flow to use stored or controlled evaluation examples;
- reset safely.

This prevents a reviewer from seeing an empty or broken project because a marketplace changed.

---

### P4-DEMO-03 — Provide public environment or reproducible recording

**Priority:** P1  
**Effort:** L

Preferred evidence:

1. public frontend;
2. public read-only API docs;
3. short demonstration video;
4. screenshots and animated GIF;
5. local one-command setup.

If cost prevents an always-on deployment, a high-quality recording plus reproducible setup is acceptable, but the limitation must be explicit.

---

## 4. Frontend

### P4-FRONTEND-01 — Build minimal portfolio frontend

**Priority:** P1  
**Effort:** L

Recommended stack based on existing user skills:

- Next.js;
- TypeScript;
- server-side API client where appropriate;
- responsive UI;
- simple component library or Tailwind;
- charts only where they explain a decision.

Pages:

- overview dashboard;
- opportunities;
- opportunity details;
- market baselines/trends;
- AI assistant;
- system status/about.

---

### P4-FRONTEND-02 — Opportunity detail page

**Priority:** P1  
**Effort:** M

Display:

- source listing;
- purchase price;
- baseline range;
- gross spread;
- costs;
- estimated net profit;
- score breakdown;
- AI verdict;
- evidence;
- risk cost range;
- confidence;
- last seen;
- data freshness;
- calculation versions.

The page should explain the recommendation, not only display a score.

---

### P4-FRONTEND-03 — Market visualization

**Priority:** P2  
**Effort:** M

Useful charts:

- historical median price;
- active listing volume;
- price distribution;
- listing price versus baseline;
- opportunity count over time.

Avoid decorative dashboards with no decision value.

---

### P4-FRONTEND-04 — AI assistant interface

**Priority:** P2  
**Effort:** M

Requirements:

- streaming output;
- visible tool activity in a user-friendly form;
- referenced opportunity cards;
- error recovery;
- example prompts;
- budget and risk filters;
- disclaimer that estimates are not guarantees.

---

### P4-FRONTEND-05 — Accessibility and responsiveness

**Priority:** P1  
**Effort:** M

Requirements:

- keyboard navigation;
- semantic labels;
- sufficient contrast;
- responsive layout;
- loading and error states;
- accessible charts or textual alternatives.

---

## 5. Documentation

### P4-DOCS-01 — Rewrite README as a project landing page

**Priority:** P1  
**Effort:** M

Recommended structure:

1. one-sentence product statement;
2. demo links and screenshot;
3. problem and users;
4. system capabilities;
5. architecture diagram;
6. data flow;
7. important engineering decisions;
8. quick start;
9. testing;
10. API examples;
11. observability;
12. AI evaluation results;
13. security and limitations;
14. roadmap;
15. author and contact.

Avoid a wall of badges before the reader understands the product.

---

### P4-DOCS-02 — Add architecture diagrams

**Priority:** P1  
**Effort:** M

Required diagrams:

- system context;
- container/service architecture;
- data pipeline;
- Celery task sequence;
- AI appraisal flow;
- function-calling flow;
- deployment view.

Use Mermaid or version-controlled source where possible.

---

### P4-DOCS-03 — Publish ADR index

**Priority:** P1  
**Effort:** S

Provide a visible index linking decisions such as:

- why Medallion architecture;
- why Polars;
- why PostgreSQL;
- why Celery;
- why SSE;
- why structured outputs;
- why no arbitrary SQL;
- why deterministic repair costs;
- why a seeded demo mode.

---

### P4-DOCS-04 — Create operations runbook

**Priority:** P2  
**Effort:** M

Include:

- startup;
- migration;
- worker restart;
- scheduler troubleshooting;
- failed task retry;
- stale lock recovery;
- database restore;
- rotating secrets;
- provider outage behavior.

---

### P4-DOCS-05 — Create contributor guide

**Priority:** P2  
**Effort:** S

Include:

- local setup;
- branch model;
- commands;
- test categories;
- issue templates;
- commit conventions;
- Definition of Done.

---

## 6. Evidence and measurement

### P4-EVIDENCE-01 — Publish benchmark report

**Priority:** P1  
**Effort:** M

Measure:

- records processed per stage;
- pipeline duration on demo data;
- API p50/p95 latency;
- duplicate prevention result;
- worker retry demonstration;
- baseline sample quality;
- AI structured-output validity;
- AI critical-risk recall;
- average AI latency and cost.

Use honest dataset sizes and environment details.

---

### P4-EVIDENCE-02 — Show before/after engineering improvements

**Priority:** P1  
**Effort:** M

Examples:

- before: rerun could duplicate records;
- after: idempotent upsert with invariant test;
- before: SQLite tests masked PostgreSQL behavior;
- after: PostgreSQL CI integration;
- before: percentage contract inconsistent;
- after: data dictionary and contract test;
- before: LLM estimated costs directly;
- after: controlled repair-cost catalog.

This demonstrates reasoning and growth.

---

### P4-EVIDENCE-03 — Add CI, coverage, and deployment indicators

**Priority:** P1  
**Effort:** S

Badges should link to evidence:

- CI status;
- coverage;
- deployed API;
- documentation;
- latest release.

Do not add badges for unused tools.

---

## 7. Case study

### P4-CASE-01 — Create portfolio case study

**Priority:** P1  
**Effort:** L

Suggested structure:

#### Context

What problem exists in used-hardware marketplaces?

#### Constraints

- inconsistent listing text;
- changing marketplace pages;
- uncertain product condition;
- sparse comparable listings;
- external API/LLM cost;
- portfolio-scale infrastructure.

#### Architecture

Explain the major components and boundaries.

#### Engineering challenges

Focus on:

- idempotency;
- schema evolution;
- PostgreSQL compatibility;
- baseline quality;
- task orchestration;
- AI grounding;
- prompt injection.

#### Decisions and trade-offs

Explain rejected alternatives.

#### Results

Use measured evidence.

#### Limitations

Examples:

- estimates are not transaction guarantees;
- marketplace availability changes;
- limited geographic/product coverage;
- AI confidence depends on listing detail.

#### Next improvements

Only list realistic follow-up work.

---

## 8. Repository professionalism

### P4-REPO-01 — Add templates and automation

**Priority:** P2  
**Effort:** M

Add:

- issue templates;
- pull request template;
- bug report;
- feature request;
- architecture decision template;
- release notes template;
- Dependabot or equivalent dependency update configuration;
- code security scanning where appropriate.

---

### P4-REPO-02 — Create release strategy

**Priority:** P2  
**Effort:** M

Use semantic releases or a simple documented versioning model.

Initial suggested milestones:

- `v0.1.0` reliable local engine;
- `v0.2.0` autonomous worker stack;
- `v0.3.0` AI appraisal;
- `v1.0.0` public portfolio release.

---

### P4-REPO-03 — Add license and data notice

**Priority:** P1  
**Effort:** S

Include:

- software license;
- source-data limitations;
- trademark/non-affiliation notice;
- privacy and demo-data note;
- marketplace terms-awareness statement.

---

## 9. Career assets

### P4-CAREER-01 — Create concise project description

**Priority:** P1  
**Effort:** S

Prepare versions for:

- one-line resume;
- three-line resume;
- LinkedIn project section;
- GitHub repository description;
- interview explanation.

Claims must be backed by current evidence.

---

### P4-CAREER-02 — Prepare resume bullets

**Priority:** P1  
**Effort:** S

Bullet formula:

```text
Action + system + engineering challenge + measurable evidence + business result
```

Example style:

> Built an idempotent Bronze/Silver/Gold marketplace pipeline with PostgreSQL, Polars, and Celery, adding PostgreSQL integration tests and run-level observability to prevent duplicate processing and trace failures end to end.

Replace generic claims such as “used many modern technologies.”

---

### P4-CAREER-03 — Prepare interview narratives

**Priority:** P1  
**Effort:** M

Prepare 5–8 minute explanations for:

- architecture overview;
- hardest defect;
- PostgreSQL versus SQLite testing;
- idempotency design;
- Celery workflow;
- baseline methodology;
- AI evaluation;
- prompt-injection defense;
- deployment trade-offs.

---

## 10. Optional portfolio extensions

### P4-OPTIONAL-01 — Watchlist and alerts

**Priority:** P3

Allow users to define:

- category;
- maximum purchase price;
- minimum net margin;
- maximum risk;
- region.

Notify when a new matching opportunity appears.

This is a stronger product extension than adding unrelated infrastructure.

---

### P4-OPTIONAL-02 — Opportunity feedback

**Priority:** P3

Allow marking:

- useful;
- false positive;
- listing already sold;
- underestimated risk;
- inaccurate baseline.

Feedback can improve deterministic rules and future evaluation datasets.

---

### P4-OPTIONAL-03 — Marketplace adapter interface

**Priority:** P3

Create a source adapter contract and add a second marketplace only after the first source is stable.

This demonstrates extensibility through real use, not speculative abstraction.

---

## 11. Testing requirements

- frontend unit tests for key formatting and state;
- API contract tests generated from OpenAPI where useful;
- end-to-end demo journey;
- accessibility smoke test;
- deployment smoke test;
- seeded-demo reset test;
- screenshot or visual regression for critical pages;
- broken external source fallback test.

---

## 12. Required deliverables

- minimal frontend;
- seeded demo mode;
- public deployment or reproducible demo recording;
- landing-page README;
- architecture diagrams;
- case study;
- benchmark/evaluation report;
- operations runbook;
- contributor guide;
- license and data notice;
- resume bullets;
- interview narratives;
- Phase 4 release checklist.

---

## 13. Definition of Done

Phase 4 is done when an external reviewer can, without private guidance:

1. understand the project problem;
2. open a working demo or follow a reproducible setup;
3. identify the architecture;
4. inspect an opportunity and its explanation;
5. see operational and AI evidence;
6. understand limitations;
7. verify CI and tests;
8. recognize the specific engineering skills demonstrated.
