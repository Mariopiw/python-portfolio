# Security Notes

Use only against systems you own or are explicitly authorized to test.

Fixtures use synthetic canaries only. Never place real passwords, API keys, customer data, medical data, or confidential records in attack fixtures.

Covered:
- prompt injection
- RAG poisoning
- synthetic leakage
- hallucination
- citation failure
- cross-tenant disclosure
- agent/workflow authorization bypass
- regression

Limitations:
- regex refusal detection
- no semantic entailment judge
- no multi-turn attacks
- no multimodal attacks
- no MCP/tool-argument security tests yet
