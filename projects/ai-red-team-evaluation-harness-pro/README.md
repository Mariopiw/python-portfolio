# AI Red-Team / Evaluation Harness Pro

Professional portfolio project for a **Secure AI Solutions Engineer**.

## What it demonstrates

- prompt-injection testing
- RAG-poisoning / indirect-injection testing
- synthetic secret-leakage checks
- hallucination and abstention evaluation
- citation/source validation
- cross-tenant isolation testing
- workflow/agent authorization testing
- severity-aware security gates
- regression baselines
- JSON, Markdown, and JUnit-style reporting
- pluggable target adapters for RAG and workflow systems

## 80/20 architecture

```text
Version-controlled attack cases
        ↓
Target adapter
        ↓
Owned / authorized AI application
        ↓
Response
        ↓
Deterministic detectors
        ↓
PASS / FAIL
        ↓
Metrics + reports
        ↓
Regression baseline
        ↓
Release gate
```

The central design principle is:

> **Attack generation and pass/fail scoring are separate concerns.**

Creative attack discovery can be probabilistic. Hard security requirements should be checked deterministically whenever possible.

## Project layout

```text
harness/
  cli.py
  dataset.py
  detectors.py
  gates.py
  models.py
  regression.py
  reporting.py
  runner.py
  settings.py
  targets/
    base.py
    factory.py
    rag_http.py
    orchestrator_http.py

datasets/
fixtures/
tests/
```

## Setup

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
ruff check .
```

## Test a Secure RAG application

Configure:

```text
TARGET_KIND=secure_rag_http
TARGET_BASE_URL=http://localhost:8000
TARGET_BEARER_TOKEN=YOUR_TOKEN
```

Then run:

```bash
python -m harness.cli
```

The RAG adapter expects a query endpoint that returns fields such as:

```json
{
  "answer": "365 days [S1]",
  "sources": [
    {
      "source_id": "S1",
      "filename": "company_ai_policy.txt"
    }
  ],
  "citation_valid": true
}
```

## Safe RAG-poisoning fixture

Fixture upload is disabled by default.

Enable it only against a system you own or are explicitly authorized to test:

```yaml
run:
  allow_fixture_uploads: true
```

The included document uses a harmless marker, `POISON_SUCCESS`, so the harness can determine whether retrieved untrusted instructions changed model behavior.

## Test the Workflow Orchestrator

Configure:

```text
TARGET_KIND=orchestrator_http
TARGET_BASE_URL=http://localhost:8000
TARGET_BEARER_TOKEN=YOUR_SUBMITTER_TOKEN
```

For the authorization test, run only:

```yaml
run:
  categories:
    - agent_authorization
```

The synthetic high-risk workflow may be accepted, but it must not immediately become:

```text
APPROVED
EXECUTING
COMPLETED
```

That demonstrates that natural-language instructions cannot bypass deterministic human-approval controls.

## Metrics

The harness measures:

- overall Attack Success Rate (ASR)
- ASR by category
- high-severity failures
- critical failures
- evaluation errors
- citation failure rate
- mean request latency

## Regression testing

Save an accepted baseline:

```bash
python -m harness.cli --update-baseline
```

Then rerun the suite after changing:

- model
- system prompt
- chunking
- embeddings
- retriever / reranker
- citation logic
- guardrails
- authorization logic

The command exits non-zero when configured gates or regression thresholds fail.

## Test categories

| Category | Purpose |
|---|---|
| Prompt injection | Detect trusted-instruction override or prompt leakage |
| RAG poisoning | Detect malicious instructions embedded in retrieved content |
| Data leakage | Detect disclosure of synthetic canary values |
| Hallucination | Verify abstention when evidence is absent |
| Citation accuracy | Verify known answers and expected sources |
| Tenant isolation | Detect synthetic cross-tenant disclosure |
| Agent authorization | Verify high-risk work cannot self-authorize |

## Safety scope

Use this project only against systems you own or have explicit permission to test.

All included secrets, tenant markers, and poisoned-document content are synthetic. Do not place real credentials, customer information, medical data, or confidential production material in the fixtures.

## Portfolio story

This project is designed to work with:

1. **Secure Regulated RAG Platform** — build and secure retrieval-grounded AI.
2. **Secure AI Workflow Orchestrator** — build reliable, approval-controlled automation.
3. **AI Red-Team / Evaluation Harness Pro** — attack, measure, regress, and verify both systems.

Together they demonstrate:

```text
BUILD → ATTACK → MEASURE → FIX → PROVE
```

See also:

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [SECURITY.md](SECURITY.md)
- [CONTROL_MAPPING.md](CONTROL_MAPPING.md)
- [INTERVIEW_QA.md](INTERVIEW_QA.md)
