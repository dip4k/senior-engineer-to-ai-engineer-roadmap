# Capstone Lab: Production Multi-Provider Resilient AI Gateway

> **Tier**: 🟡 Engineering Depth (Capstone Lab)  
> **Parent Module**: [Phase 07: High-Throughput Serving & LLMOps](../README.md)  
> **Estimated Lab Time**: 60–90 minutes  
> **Core Deliverable**: An enterprise-grade resilient AI Gateway microservice with dual-tier caching, token-bucket rate limiting, circuit breaking, SSE streaming, and client disconnect cancellation.

---

### 🎯 Challenge Objective
Architect and implement an enterprise-grade **Resilient Multi-Provider AI Gateway Microservice** in either **Python (FastAPI)** or **C# (.NET 9)** capable of sustaining simulated provider outages and rate-limit surges without dropping active client connections.

```mermaid
flowchart TD
    Scope["CAPSTONE ARCHITECTURAL SCOPE"]
    
    C1["1. Dual-Tier Cache<br/>Exact SHA-256 + Semantic Vector"]
    C2["2. Distributed Rate Limiter<br/>Two-Phase Token-Bucket (TPM / RPM)"]
    C3["3. Tiered Model Fallback<br/>Primary -> Secondary -> Degraded"]
    C4["4. SSE Token Streaming<br/>Server-Sent Events Protocol"]
    C5["5. Cancellation Propagation<br/>Client Disconnect Aborts Upstream"]
    C6["6. OpenTelemetry Tracing<br/>GenAI SemConv Spans & Metrics"]
    
    Scope --> C1
    Scope --> C2
    Scope --> C3
    Scope --> C4
    Scope --> C5
    Scope --> C6

    style Scope fill:none,stroke:#3b82f6,stroke-width:2px
    style C1 fill:none,stroke:#10b981,stroke-width:2px
    style C2 fill:none,stroke:#f59e0b,stroke-width:2px
    style C3 fill:none,stroke:#ef4444,stroke-width:2px
    style C4 fill:none,stroke:#8b5cf6,stroke-width:2px
    style C5 fill:none,stroke:#ec4899,stroke-width:2px
    style C6 fill:none,stroke:#64748b,stroke-width:2px
```

#### Diagram Walkthrough
The capstone architecture integrates six production systems capabilities into a single gateway pipeline:
1. **Dual-Tier Cache**: Checks sub-5ms exact SHA-256 hashes first, falling back to semantic vector cosine similarity.
2. **Distributed Rate Limiter**: Enforces two-phase token reservation and post-stream settlement against Redis.
3. **Tiered Fallback**: Automated circuit breaker that trips to secondary providers on HTTP 429 or 5xx outages.
4. **SSE Streaming**: Unbuffered Server-Sent Events flow directly to clients with `X-Accel-Buffering: no`.
5. **Cancellation Propagation**: Immediate termination of upstream generation when clients disconnect.
6. **OpenTelemetry Tracing**: Emits standardized `gen_ai.*` span attributes and latency metrics.

---

### Term Ledger
| Term | Status | Definition / Clarification |
| :--- | :--- | :--- |
| **Token-Bucket Rate Limiting** | Assumed | Rate limiting algorithm that regulates consumption by replenishing token credits at fixed rates. |
| **Two-Phase Token Reservation** | Assumed | Reserving estimated token quota upfront and settling actual usage post-stream. |
| **Exact Hash Cache** | Assumed | Sub-5ms SHA-256 string hash lookup for deterministic query caching. |
| **Semantic Vector Cache** | Assumed | Cosine similarity matching against vector embeddings for near-duplicate queries. |
| **Circuit Breaker** | Assumed | Automated failover pattern stopping outbound calls to degraded providers to prevent cascading failure. |
| **Server-Sent Events (SSE)** | Assumed | Unidirectional HTTP streaming protocol delivering real-time text chunks (`data: {...}\n\n`). |
| **Cancellation Propagation** | Assumed | Terminating upstream LLM generation immediately when a client disconnects to prevent zombie token burn. |

---

### 📐 Architectural & Functional Requirements

1. **Dual-Tier Cache Engine**:
   - **Tier 1**: Exact string hash matching (`SHA-256`) against Redis with TTL = 24 hours.
   - **Tier 2**: Semantic vector similarity search against Redis Vector or pgvector using dense embeddings (`text-embedding-3-small`). If cosine similarity >= 0.85–0.92, serve cached content immediately.
2. **Dynamic Tiered Resilience Router**:
   - **Primary Model**: Claude 3.7 Sonnet or Azure OpenAI GPT-4o / o3.
   - **Secondary Model**: Google Cloud Vertex AI Gemini 2.0 Flash.
   - **Tertiary Model (Degraded)**: Claude 3.5 Haiku or Local vLLM SLM.
   - Configure a circuit breaker: If the primary provider fails 3–5 times consecutively or returns HTTP 429, trip the circuit into `OPEN` state for 15–30 seconds and route traffic directly to the secondary provider.
3. **Token Budget & Rate Limiting**:
   - Enforce a tenant quota: 100,000 tokens per tenant per day.
   - Maintain a sliding window rate limiter: Max 30 requests per minute per user.
   - Implement two-phase reservation: atomic reservation before generation and post-stream settlement.
4. **Streaming Protocol**:
   - Expose endpoint `POST /v1/gateway/chat/stream`.
   - Stream tokens formatted as standard SSE (`data: {...}\n\n`).
   - Propagate cancellation tokens: If the client terminates the HTTP connection, immediately abort inference on the active provider.
5. **Observability**:
   - Emit an OpenTelemetry span for every request containing attributes:
     `gen_ai.system`, `gen_ai.request.model`, `gen_ai.response.model`, `gen_ai.usage.prompt_tokens`, `gen_ai.usage.completion_tokens`, and `gateway.cache_hit_type` (none, exact, semantic).

---

### 🧪 Verification & Acceptance Test Suite

Your capstone implementation must pass the following simulated production chaos tests:

- [ ] **Test Case 1: The Exact Cache Hit**:
  - Dispatch prompt: *"Explain CAP theorem in two sentences."* (Observe full generation, record TTFT).
  - Dispatch identical prompt again.
  - **Assertion**: Response returned with `"cached": true`, latency < 15ms, and zero upstream LLM API calls generated.
- [ ] **Test Case 2: The Semantic Cache Hit**:
  - Dispatch prompt: *"Explain the CAP theorem in two concise sentences."*
  - **Assertion**: Cosine similarity matches cached entry; response returned from cache with `"cache_type": "semantic"`, latency < 50ms.
- [ ] **Test Case 3: Primary Provider 429 Outage Simulation**:
  - Inject a mock or proxy rule forcing the Primary Model to return `HTTP 429 Too Many Requests`.
  - Dispatch 5 requests.
  - **Assertion**: The Gateway automatically catches the 429, logs the incident, falls back to the Secondary Provider (Gemini 2.0 Flash), and the end user receives an unbroken SSE token stream without seeing an error.
- [ ] **Test Case 4: Client Disconnect Cancellation**:
  - Initiate a generation requiring 2,000 tokens.
  - Terminate the client socket after receiving 50 tokens.
  - **Assertion**: Microservice logs show `Client disconnected. Cancellation token triggered.` Upstream inference terminates immediately, preventing unread token generation.
- [ ] **Test Case 5: Tenant Quota Enforcement**:
  - Exhaust a test tenant's token budget.
  - Dispatch an additional request.
  - **Assertion**: Gateway immediately returns `HTTP 429 Quota Exceeded` before executing vector search or calling any cloud models.

### ⚡ Running the Automated Evaluation Harness
Execute the self-contained verification runner from the repository root:

```bash
python scripts/verify_phase_07_capstone.py
```

Expected output:
```text
======================================================================
 🧪 PHASE 07 CAPSTONE: RESILIENT AI GATEWAY AUTOMATED VERIFICATION
======================================================================

[✅ PASS] Test Case 1: The Exact Cache Hit (SHA-256)
[✅ PASS] Test Case 2: The Semantic Cache Hit (Vector Similarity)
[✅ PASS] Test Case 3: Primary Provider 429 Outage Simulation
[✅ PASS] Test Case 4: Client Disconnect Cancellation Propagation
[✅ PASS] Test Case 5: Tenant Quota Enforcement (Token Bucket)

======================================================================
 Summary: 5/5 Capstone Acceptance Tests Passing
======================================================================
```

---

### 🔗 Architecture & Implementation References
- [Lesson 00: LLM Serving Fundamentals & The Inference Lifecycle](../00-llm-serving-fundamentals-and-the-inference-lifecycle.md)
- [Lesson 01: Multi-Provider AI Gateways & Rate Limiting](../01-resilient-ai-gateways-and-rate-limiting.md)
- [Lesson 02: High-Performance Token Streaming & Backpressure](../02-high-performance-token-streaming-and-backpressure.md)
- [Lesson 03: Dual-Tier Caching & Asynchronous Batch APIs](../03-dual-tier-caching-and-batch-apis.md)
- [Lesson 04: Continuous Batching, PagedAttention & RadixAttention](../04-vllm-continuous-batching-and-radixattention.md)
- [Production Reference: Python AI Gateway Engine](../examples/gateway_service.py)
- [Production Reference: C# .NET 9 Polly v8 Gateway](../examples/ResilientAgentService.cs)
- [Reference Implementation: AgentForge Gateway Service](../../agent-forge/agent_forge/gateway/)
- [Automated Verification Harness: scripts/verify_phase_07_capstone.py](../../scripts/verify_phase_07_capstone.py)

---

## 🧭 Navigation

- **[← Phase 07 Hub: Orientation & Navigation](../README.md)**
- **[Lesson 00: LLM Serving Fundamentals & The Inference Lifecycle](../00-llm-serving-fundamentals-and-the-inference-lifecycle.md)**
- **[Lesson 01: Multi-Provider AI Gateways & Rate Limiting](../01-resilient-ai-gateways-and-rate-limiting.md)**
- **[Next Phase: Phase 08 — AI-Augmented SDLC & Leadership →](../../08-ai-augmented-sdlc-and-leadership/README.md)**
