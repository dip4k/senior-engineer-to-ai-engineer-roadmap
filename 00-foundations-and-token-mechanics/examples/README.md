# Phase 00 Examples: Foundations & Token Mechanics

Production-grade reference implementations demonstrating exact token budgeting, test-time compute reasoning tokens, latency forecasting, and KV cache memory estimation.

## Files

| File | Language | Purpose | Key Patterns |
|---|---|---|---|
| [`token_profiler.py`](./token_profiler.py) | Python 3.11+ | Exact Token Profiler & Cost Auditor | Supports frontier models (`claude-3-7-sonnet`, `o3-mini`, `gpt-4.5`, `gemini-2.5-flash`, `deepseek-r1`), reasoning budget tokens, TTFT/decode latency modeling |
| [`adaptation_decision_matrix.py`](./adaptation_decision_matrix.py) | Python 3.11+ | Adaptation Decision Matrix & TCO Engine | Evaluates Prompt Caching, RAG, LoRA/QLoRA, and Test-Time Compute across volume, latency SLAs, multi-month TCO, and break-even math |
| [`TokenGovernorService.cs`](./TokenGovernorService.cs) | C# / .NET 9 | Token Budget & KV Cache Governor | ASP.NET Core minimal API, GQA VRAM formula, admission control, HTTP 429 |
