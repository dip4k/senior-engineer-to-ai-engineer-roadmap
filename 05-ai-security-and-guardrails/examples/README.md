# Phase 05 Examples: AI Security & Guardrails

Production-grade security and guardrail implementations demonstrating dual-LLM quarantine architectures, PII redaction, honeytoken/canary detection, and ASP.NET Core Semantic Kernel middleware.

## Files

| File | Language | Purpose | Key Patterns |
|---|---|---|---|
| [`guardrail_pipeline.py`](./guardrail_pipeline.py) | Python 3.12+ | Multi-Stage Guardrail Pipeline | PII redaction (compiled regex + cryptographic surrogate vault), canary token verification, Llama Guard safety classification |
| [`GuardrailMiddleware.cs`](./GuardrailMiddleware.cs) | C# / .NET 9 | ASP.NET Core Guardrail Middleware | Pipeline filter, prompt sanitization, secret leakage prevention, OWASP Top 10 mitigation |
