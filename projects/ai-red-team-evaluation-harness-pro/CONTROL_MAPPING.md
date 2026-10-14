# Control Mapping

| Risk | Tests | Main control |
|---|---|---|
| Prompt injection | `pi-*` | trust boundaries, least privilege, validation |
| Sensitive disclosure | `leak-*` | authorization, minimization, canary testing |
| RAG poisoning | `poison-*` | provenance, untrusted-data handling |
| Hallucination | `hall-*` | abstention, grounding |
| Citation integrity | `cite-*` | deterministic citation verification |
| Cross-tenant leakage | `tenant-*` | app authorization + database RLS |
| Excessive agency | `agent-auth-*` | approval/state-machine controls |
