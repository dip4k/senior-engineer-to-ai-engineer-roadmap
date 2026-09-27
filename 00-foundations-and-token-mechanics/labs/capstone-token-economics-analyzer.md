# Capstone Engineering Challenge: High-Throughput Token Budgeting Proxy

**Objective:** Construct an enterprise API proxy in Python (FastAPI), TypeScript (Fastify/Node), or C# (ASP.NET Core) that intercepts LLM calls before provider dispatch to eliminate runaway inference costs, prevent GPU out-of-memory crashes, and enforce tenant SLAs.

### Core Architectural Components & Implementation Steps:

1. **Exact Multi-Model Token Profiler:**
   - Detect the target model family (`gpt-4.5`, `claude-3-7-sonnet`, `gemini-2.5-flash`, `llama-3.3-70b`).
   - Use the appropriate native tokenizer bindings (`tiktoken` / `tokenizers` / C# `Microsoft.ML.Tokenizers`).
   - Profile incoming `system`, `user`, and `tool_calls` payloads with per-message framing overhead (+3 to +4 tokens per message).

2. **In-Flight GPU KV-Cache & VRAM Allocation Estimator:**
   - Compute required KV-cache footprint using the formula: $2 \times 2 \times \text{Layers} \times H_{KV} \times d_k \times \text{Batch} \times \text{TotalSequenceLen}$.
   - Maintain an in-memory concurrent allocation counter across running inferences.
   - If an incoming request pushes total GPU KV-cache allocation past threshold (e.g., 85% of available VRAM), enqueue or reject before invoking downstream providers.

3. **Sliding-Window Token-Per-Minute (TPM) Governor:**
   - Implement a distributed Redis-backed or atomic local sliding-window rate limiter tracking tenant consumption over a 60-second rolling window.
   - Return standard rate limiting headers: `X-RateLimit-Limit-Tokens`, `X-RateLimit-Remaining-Tokens`, `Retry-After`.

4. **Telemetry & Failure Recovery (RFC 7807):**
   - Emit OpenTelemetry spans with attributes: `llm.provider`, `llm.model`, `llm.tokens.prompt`, `llm.cost.estimated_usd`.
   - On budget or rate limit breach, return HTTP 429 / 400 with an RFC 7807 compliant problem details JSON object.

### Verification & Test Scenarios:
- **Baseline Test:** Send 10 concurrent valid 500-token prompts and assert `HTTP 200` with correct token counts and estimated costs.
- **TPM Ceiling Test:** Fire a burst of requests exceeding the 100,000 TPM limit; assert immediate `HTTP 429` with valid `Retry-After` header.
- **KV-Cache Overflow Protection:** Simulate a 128k context request against a constrained budget; assert early rejection before dispatching to the upstream LLM API.

---
[Return to Module 00](../README.md#12-capstone-engineering-challenge)
