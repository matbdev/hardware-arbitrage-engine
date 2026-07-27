# Phase 3 Specification — AI Appraisal and Conversational Agent

## 1. Objective

Add AI features that provide measurable product value:

1. structured textual risk appraisal for listings;
2. deterministic financial enrichment using a repair-cost catalog;
3. evaluated and versioned LLM behavior;
4. a read-only function-calling assistant;
5. streaming API responses.

The implementation must avoid arbitrary SQL generation and unsupported monetary hallucinations.

---

## 2. Completion outcome

At the end of Phase 3:

- eligible listings receive structured, traceable AI appraisals;
- AI-detected risks are supported by listing evidence;
- estimated costs are calculated from controlled domain tables;
- model and prompt versions are persisted;
- quality is measured on a labeled evaluation dataset;
- function-calling tools access only allowed read-only operations;
- streaming chat answers business questions using current Gold data;
- cost, latency, and failures are observable.

---

## 3. AI product boundaries

### AI should do

- interpret listing text;
- identify risk categories;
- extract evidence;
- identify missing information;
- classify severity;
- suggest negotiation questions;
- select allow-listed tools;
- summarize deterministic query results.

### AI should not do alone

- invent precise repair prices;
- execute arbitrary SQL;
- decide database writes without validation;
- treat listing text as trusted instructions;
- guarantee resale value;
- hide low confidence;
- overwrite deterministic pipeline results.

---

## 4. Data model

### P3-DATA-01 — AI appraisal table

**Priority:** P1  
**Effort:** M

Suggested table: `gold.fact_ai_deal_appraisal`

Fields:

- `appraisal_id`;
- `ad_id`;
- `listing_content_hash`;
- `verdict`;
- `risk_score`;
- `confidence`;
- `detected_risks` JSONB;
- `evidence` JSONB;
- `missing_information` JSONB;
- `negotiation_questions` JSONB;
- `model_provider`;
- `model_name`;
- `model_version`;
- `prompt_version`;
- `schema_version`;
- `input_tokens`;
- `output_tokens`;
- `estimated_cost`;
- `latency_ms`;
- `status`;
- `error_code`;
- `created_at`;
- `expires_at` or `stale_after`.

Use a uniqueness rule that prevents repeated appraisal of unchanged content with the same prompt/model version.

---

### P3-DATA-02 — Repair and risk catalog

**Priority:** P1  
**Effort:** M

Suggested tables:

```text
risk_catalog
repair_cost_catalog
```

Risk catalog fields:

- code;
- category;
- severity;
- description;
- default score impact;
- recommended buyer action.

Repair cost fields:

- risk code;
- product category;
- optional brand/model segment;
- minimum cost;
- expected cost;
- maximum cost;
- currency;
- source;
- effective date;
- confidence;
- notes.

#### Principle

The LLM identifies `BATTERY_DEGRADED`; the application calculates a cost range from the catalog.

---

### P3-DATA-03 — Prompt and model registry

**Priority:** P1  
**Effort:** M

Persist:

- prompt identifier;
- version;
- purpose;
- template hash;
- schema version;
- model compatibility;
- activation date;
- deprecation status.

A Git-tracked prompt file remains the source definition, while the database or run metadata stores the exact version used.

---

### P3-DATA-04 — AI execution records

**Priority:** P1  
**Effort:** M

Track each model call separately from the final appraisal:

- request identifier;
- run/task identifiers;
- provider;
- model;
- attempts;
- status;
- token usage;
- latency;
- validation errors;
- provider error class;
- cache hit;
- redacted input hash.

Do not persist secrets or unnecessary raw sensitive data.

---

## 5. Structured appraisal

### P3-APPRAISAL-01 — Define Pydantic output schema

**Priority:** P1  
**Effort:** M

Suggested schema:

```python
class RiskEvidence(BaseModel):
    risk_code: str
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    evidence_text: str
    explanation: str
    confidence: float

class AIDealAppraisalOutput(BaseModel):
    verdict: Literal[
        "GREAT_DEAL",
        "REVIEW_REQUIRED",
        "MODERATE_RISK",
        "HIGH_RISK_AVOID",
        "INSUFFICIENT_INFORMATION",
    ]
    risk_score: int
    confidence: float
    detected_risks: list[RiskEvidence]
    missing_information: list[str]
    negotiation_questions: list[str]
    concise_rationale: str
```

Constraints:

- risk score 0–100;
- confidence 0–1;
- evidence must be based on supplied listing content;
- unknown risk codes are rejected or mapped through a controlled fallback.

---

### P3-APPRAISAL-02 — Build listing appraisal service

**Priority:** P1  
**Effort:** L

Responsibilities:

1. load eligible listing data;
2. normalize and truncate input safely;
3. compute content hash;
4. check cache/current appraisal;
5. call model;
6. validate structured output;
7. retry repairable schema failures;
8. map risk codes to catalog;
9. calculate deterministic cost range;
10. compute adjusted opportunity result;
11. persist execution and appraisal records.

---

### P3-APPRAISAL-03 — Define eligibility policy

**Priority:** P1  
**Effort:** S

Only appraise listings that meet conditions such as:

- valid listing text;
- sufficient specification quality;
- current active state;
- baseline available;
- potential financial relevance;
- content changed since previous appraisal.

This controls cost and prevents meaningless model calls.

---

### P3-APPRAISAL-04 — Adjust opportunity scoring

**Priority:** P1  
**Effort:** M

Add AI-derived but deterministic components:

```text
adjusted_net_profit =
    estimated_net_profit
  - expected_refurbish_cost
  - risk_reserve

adjusted_opportunity_score =
    base_opportunity_score
  - risk_penalty
  + confidence_adjustment
```

The formula must be versioned.

The LLM does not directly write the final score.

---

### P3-APPRAISAL-05 — Human-review state

**Priority:** P2  
**Effort:** M

Listings with:

- low model confidence;
- contradictory evidence;
- critical risk;
- unusually high estimated profit;
- schema-repair fallback;

should receive `REVIEW_REQUIRED`.

Provide optional review fields:

- reviewer decision;
- notes;
- reviewed timestamp;
- override reason.

This also creates future evaluation labels.

---

## 6. Provider architecture and resilience

### P3-LLM-01 — Create provider abstraction

**Priority:** P1  
**Effort:** M

Define an internal interface independent from LangChain-specific objects:

```python
class AppraisalModel(Protocol):
    async def appraise(self, request: AppraisalRequest) -> AIDealAppraisalOutput:
        ...
```

This prevents provider SDK details from spreading through domain logic.

---

### P3-LLM-02 — Timeout, retry, fallback, and circuit breaker

**Priority:** P1  
**Effort:** M

Handle:

- provider timeout;
- rate limit;
- malformed output;
- context-length failure;
- authentication failure;
- unavailable model;
- transient network error.

Rules:

- limited retries;
- exponential backoff;
- no endless schema repair loop;
- optional fallback model;
- circuit breaker for repeated provider failures;
- task status visible in pipeline records.

---

### P3-LLM-03 — Cache unchanged appraisals

**Priority:** P1  
**Effort:** M

Cache key should include:

- listing content hash;
- prompt version;
- schema version;
- model family/version;
- relevant catalog version.

A changed repair catalog may recompute deterministic costs without repeating the LLM call when the extracted risk output remains valid.

---

### P3-LLM-04 — Cost controls

**Priority:** P1  
**Effort:** M

Add:

- maximum appraisals per run;
- daily budget setting;
- token limits;
- per-call token logging;
- cost estimate;
- priority ordering;
- budget-exhausted status.

Expose metrics:

- cost per appraisal;
- cost per accepted opportunity;
- cache-hit rate.

---

## 7. AI evaluation

### P3-EVAL-01 — Create labeled evaluation dataset

**Priority:** P1  
**Effort:** L

Create 50–100 representative listings covering:

- safe listing;
- battery issue;
- display issue;
- charger missing;
- broken hinge;
- repair-only item;
- vague description;
- urgent sale;
- possible scam signals;
- contradictory title and description;
- prompt injection text;
- Portuguese spelling variations;
- incomplete specifications.

Labels:

- verdict;
- risk codes;
- severity;
- evidence spans;
- missing information;
- human confidence.

Do not commit personal seller data.

---

### P3-EVAL-02 — Define metrics

**Priority:** P1  
**Effort:** M

Required metrics:

- structured-output validity rate;
- verdict accuracy;
- critical-risk recall;
- per-risk precision and recall;
- evidence grounding score;
- unsupported-risk rate;
- average latency;
- p95 latency;
- average tokens;
- average estimated cost;
- cache-hit rate;
- tool-call accuracy.

Critical-risk recall should be prioritized over overall accuracy.

---

### P3-EVAL-03 — Build repeatable evaluation runner

**Priority:** P1  
**Effort:** L

Command example:

```bash
uv run python -m app.ai.evaluation.run   --dataset tests/fixtures/ai_eval.jsonl   --prompt-version appraisal-v1
```

Outputs:

- JSON results;
- Markdown summary;
- confusion matrix data;
- regression comparison against previous version.

---

### P3-EVAL-04 — Add AI regression gate

**Priority:** P2  
**Effort:** M

Do not run paid live model evaluation on every commit.

Recommended:

- schema and mock tests on every CI run;
- small recorded contract suite on pull requests;
- manual or scheduled full evaluation before prompt/model releases;
- documented acceptable regression thresholds.

---

## 8. Function-calling tools

### P3-TOOLS-01 — Implement allow-listed read tools

**Priority:** P1  
**Effort:** L

Tools:

- `get_top_opportunities`;
- `get_market_baseline`;
- `get_price_history`;
- `get_market_trends`;
- `get_listing_appraisal`;
- `evaluate_custom_ad`.

Each tool must have:

- Pydantic input schema;
- explicit validation;
- maximum result count;
- timeout;
- safe error type;
- audit event;
- read-only database session.

---

### P3-TOOLS-02 — Use read-only database role

**Priority:** P0  
**Effort:** M

The chat agent must use a dedicated database role with access only to required Gold views/tables.

It must not:

- execute DDL;
- update records;
- access credentials;
- query arbitrary system tables.

---

### P3-TOOLS-03 — No arbitrary SQL tool

**Priority:** P0  
**Effort:** S

Do not expose generic “run SQL” functionality.

Natural-language questions must be translated into allow-listed function parameters, not raw database commands.

---

### P3-TOOLS-04 — Tool-call audit trail

**Priority:** P1  
**Effort:** M

Persist or log:

- conversation/request ID;
- tool name;
- validated arguments;
- duration;
- result count;
- success/failure;
- model decision metadata.

Sensitive values must be redacted.

---

## 9. Conversational API

### P3-CHAT-01 — Create chat request model

**Priority:** P1  
**Effort:** M

Fields:

- message;
- conversation ID;
- optional budget;
- optional filters;
- locale;
- maximum recommendations.

Enforce input length and rate limits.

---

### P3-CHAT-02 — Implement SSE streaming

**Priority:** P1  
**Effort:** L

Use SSE unless a documented requirement demands WebSockets.

Event types:

```text
message_started
tool_call_started
tool_call_completed
token
message_completed
error
```

Never stream secrets or raw internal exceptions.

---

### P3-CHAT-03 — Conversation persistence

**Priority:** P2  
**Effort:** M

Store:

- conversation;
- user message;
- assistant response;
- tool-call summary;
- model/prompt version;
- timestamps.

Define retention and deletion policy.

---

### P3-CHAT-04 — Deterministic recommendation response

**Priority:** P1  
**Effort:** M

The final answer should include structured references:

- listing identifier;
- current price;
- baseline;
- estimated net profit;
- risk verdict;
- confidence;
- direct URL;
- explanation.

The LLM should summarize returned calculations rather than recalculate them.

---

## 10. Safety and untrusted content

### P3-SAFETY-01 — Defend against indirect prompt injection

**Priority:** P0  
**Effort:** L

Listing text is untrusted data.

Required controls:

- clearly delimit listing content;
- instruct the model that listing content cannot define system behavior;
- strip or flag suspicious instruction-like text;
- tools remain controlled by code;
- test adversarial listings;
- never grant write tools based on listing content.

---

### P3-SAFETY-02 — Output validation and evidence requirement

**Priority:** P0  
**Effort:** M

Reject or downgrade outputs where:

- risk has no evidence;
- evidence is not present in input;
- unknown risk code appears;
- score is out of range;
- rationale contradicts verdict.

---

### P3-SAFETY-03 — Privacy and data minimization

**Priority:** P1  
**Effort:** M

Before sending content to a provider:

- remove seller contact details if not needed;
- avoid sending account identifiers;
- document provider data handling;
- keep only required text;
- provide deletion controls for persisted conversations.

---

## 11. AI observability

### Metrics

- appraisal calls;
- success/failure;
- validation retries;
- provider errors;
- tokens;
- estimated cost;
- latency;
- cache hits;
- verdict distribution;
- critical-risk distribution;
- low-confidence rate;
- tool-call success;
- prompt-injection detections.

### Tracing

A single request should connect:

```text
chat request
 -> model decision
 -> tool call
 -> database query
 -> response stream
```

LangSmith may be used, but core operational visibility must not depend exclusively on a third-party tracing product.

---

## 12. Testing requirements

### Unit

- schema validation;
- risk catalog mapping;
- deterministic cost calculation;
- score adjustment;
- content hashing;
- cache key;
- prompt delimiters;
- safety filters.

### Integration

- provider mocked contract;
- database persistence;
- read-only tool permissions;
- SSE event ordering;
- Celery AI queue;
- fallback behavior.

### Evaluation

- labeled dataset;
- adversarial prompt-injection cases;
- regression comparison;
- tool-call parameter accuracy.

---

## 13. Required deliverables

- AI data models and migrations;
- risk and repair catalogs;
- prompt registry;
- structured appraisal service;
- Celery AI task;
- evaluation dataset;
- evaluation runner and report;
- read-only tool layer;
- SSE chat endpoint;
- safety tests;
- AI metrics;
- architecture and model cards;
- Phase 3 evidence report.

---

## 14. Definition of Done

Phase 3 is done when a reviewer can:

1. select a listing;
2. see a structured appraisal with evidence;
3. verify repair cost came from catalog data;
4. inspect model and prompt versions;
5. view evaluation metrics;
6. ask the chat for opportunities under a budget;
7. observe validated tool calls;
8. receive a streamed answer;
9. confirm the agent cannot execute arbitrary SQL;
10. see cost, latency, and failure metrics.
