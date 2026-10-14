# Interview Q&A

1. **What is AI red teaming?** Adversarial testing designed to discover security, privacy, reliability, and business-control failures.
2. **Red team vs normal evaluation?** Evaluation measures intended performance; red teaming deliberately tries to violate requirements.
3. **Why separate attack generation from scoring?** Creative generation can be probabilistic; release gates should be repeatable.
4. **What is direct prompt injection?** Malicious user instruction conflicts with trusted policy.
5. **Indirect prompt injection?** Malicious instructions arrive through documents, web pages, email, tool output, or other context.
6. **Why doesn't RAG solve prompt injection?** Retrieved text is still untrusted input.
7. **What is RAG poisoning?** Manipulating retrievable content so malicious instructions or false facts enter model context.
8. **How do you test data leakage safely?** Use synthetic canary strings, never production secrets.
9. **What is ASR?** Attack Success Rate: successful adversarial failures divided by executed cases.
10. **Why isn't ASR enough?** Severity matters; one critical tenant leak can dominate several low-severity issues.
11. **How do you test hallucination?** Ask known-unanswerable questions and require abstention.
12. **How do you test citations?** Check expected facts, citation validity, and expected source documents.
13. **Why not only LLM judges?** They are probabilistic and attackable; hard invariants are better tested deterministically.
14. **When should you use an LLM judge?** For semantic criteria such as groundedness where exact checks are insufficient.
15. **How do you test multi-tenancy?** Use synthetic tenant-specific canaries; any cross-tenant retrieval is a critical failure.
16. **How do you test agent authorization?** Try to bypass approval; deterministic workflow state must block execution.
17. **What is a regression baseline?** Previously accepted security metrics for comparison.
18. **Why convert vulnerabilities into regression tests?** To prevent recurrence after model, prompt, or retrieval changes.
19. **Target failure vs evaluator failure?** Vulnerability versus broken test infrastructure.
20. **Why JUnit-style output?** CI systems can surface AI-security failures like normal engineering tests.
21. **What belongs in a PR suite?** Small deterministic critical controls.
22. **What belongs in a nightly suite?** Larger generated and mutated attacks.
23. **What is Promptfoo useful for?** Broad application-level adversarial generation and evaluation.
24. **What is garak useful for?** Complementary model-level vulnerability scanning.
25. **30-second pitch?** A version-controlled AI evaluation harness with deterministic detectors, ASR/severity metrics, regression baselines, RAG/workflow adapters, and synthetic fixtures.
