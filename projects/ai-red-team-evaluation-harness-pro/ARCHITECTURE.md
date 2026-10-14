# Architecture

Attack generation and scoring are separate concerns.

```text
Version-controlled cases
  -> target adapter
  -> owned/authorized AI app
  -> response
  -> deterministic detectors
  -> metrics/report
  -> baseline + release gate
```

Adapters:
- `secure_rag_http`
- `orchestrator_http`
