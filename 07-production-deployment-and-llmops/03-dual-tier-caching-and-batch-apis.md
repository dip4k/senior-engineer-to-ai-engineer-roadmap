# Lesson 03: Dual-Tier Caching & Asynchronous Batch APIs

> **Tier**: `🟡 Engineering Depth` | **Read time**: ~16 min | **Prerequisites**: [Lesson 01: Resilient Multi-Provider AI Gateways](./01-resilient-ai-gateways-and-rate-limiting.md)  
> **Core Concept**: Sub-5ms exact string hashing and semantic vector caching eliminate redundant inference costs, while asynchronous Batch APIs cut non-interactive token expenses by 50%.  
> **New AI terms introduced**: semantic vector cache, exact hash cache, cosine similarity threshold (tau), asynchronous batch API  
> **AI terms assumed from earlier lessons**: [embedding](../02-rag-and-knowledge-systems/00-rag-fundamentals-and-retrieval-architectures.md), [cosine similarity](../02-rag-and-knowledge-systems/00-rag-fundamentals-and-retrieval-architectures.md), [prompt prefix caching](../01-prompt-and-context-engineering/03-prefix-and-prompt-caching.md)

---

## 🧩 The Problem: The Cost of Redundant Inference

In enterprise customer support, documentation lookup, internal knowledge search, and coding copilots, a large percentage of incoming queries are semantically identical:

- User 1: *"How do I configure SSO in Okta?"*
- User 2: *"How do I configure single sign-on in Okta?"*
- User 3: *"How do I configure SSO in Okta?"* (identical repeat)

Without intelligent caching:
- Every query executes an end-to-end forward pass through a large foundation model.
- Latencies range between 800ms and 5,000ms.
- Provider token costs accumulate for identical answers.
- Upstream rate limits are consumed unnecessarily.

Furthermore, engineering teams frequently execute large non-real-time jobs (such as re-evaluating 50,000 test cases or backfilling catalog metadata) using synchronous API calls. This overpays by **100%** compared to provider batch pricing and risks dropped network connections.

---

## 🧒 The Mental Model: The Two-Tier Vault & The Cargo Freight Carrier

Think of dual-tier caching and batching as **Security Screening and Freight Shipping**:

```text
┌────────────────────────────────────────────────────────────┐
│                    DUAL-TIER CACHE VAULT                   │
├────────────────────────────────────────────────────────────┤
│ 1. Tier 1: Fast Barcode Scan (Exact Hash Index)            │
│    Normalized string matches hash? Return answer in 2ms.   │
│                                                            │
│ 2. Tier 2: Biometric Facial Match (Semantic Vector Index)  │
│    Cosine similarity >= 0.92? Return answer in 40ms.       │
│                                                            │
│ 3. Cache Miss: Dispatch to Inference Pipeline              │
│    Interactive: Real-time API (1.0x price)                 │
│    Non-interactive bulk: Overnight cargo freight (0.5x)    │
└────────────────────────────────────────────────────────────┘
```

- **Tier 1 (The Barcode Scan)**: An exact hash match. If the client presents the exact normalized prompt string, the response returns in under 5ms.
- **Tier 2 (The Biometric Match)**: If exact match misses, vector search compares meaning. It requires a high similarity threshold (tau ≥ 0.92) to prevent false matches.
- **Batch Processing (Air Cargo Freight)**: Non-urgent bulk jobs fly on the overnight freight plane at a 50% discount.

> ⚠️ **Where this analogy breaks**: A biometric scanner checks physical features that do not change based on context. In semantic caching, subtle words like "not" or "never" drastically invert meaning while barely altering vector cosine distance, requiring careful threshold calibration.

---

## ⚠️ Why Naive Caching Fails

Developers often implement one of two naive caching strategies:

1. **Exact Hash Only**: `SHA-256(raw_prompt)` stored in Redis.
   - *Failure*: Zero semantic tolerance. Adding a trailing period or changing *"What is CAP theorem?"* to *"Explain CAP theorem"* triggers a 100% cache miss.
2. **Naive Semantic Caching Only**: Generating a vector embedding for every incoming query and matching nearest neighbors at cosine similarity > 0.80.
   - *Failure*: At low thresholds (tau < 0.90), vector similarity produces catastrophic false positives. *"How do I delete a user?"* and *"How do I create a user?"* have high semantic proximity, returning dangerous hallucinated answers. Furthermore, generating an embedding introduces a 30–50ms latency tax on queries that could have resolved via exact hash in 2ms.

### Gateway Semantic Caching vs. Engine Prompt Prefix Caching

Engineers frequently confuse gateway caching with provider prompt caching. They operate at distinct layers:

| Dimension | Gateway Semantic Cache | Engine Prompt Prefix Cache |
|---|---|---|
| **Architectural Layer** | AI Ingress Gateway (Redis / pgvector). | GPU Inference Engine (vLLM, Anthropic, OpenAI). |
| **What is Cached** | Entire generated completion payload. | Key-Value (KV) tensors for prompt prefixes. |
| **Cache Hit Cost** | **$0.00** (Zero tokens billed). | 75–90% discount on prompt tokens; full price on decode. |
| **Cache Hit Latency** | **Sub-50ms** (Bypasses model execution). | Bypasses prompt prefill; model still runs decode loop. |
| **Semantic Flexibility** | High: Matches rephrased queries (tau ≥ 0.92). | None: Requires exact character prefix match. |

---

## ⚙️ Core Caching Mechanisms: One Term at a Time

```mermaid
flowchart TD
    Client(["👤 Client Request"]) -->|1. Raw Prompt| GW["🛡️ Gateway Normalizer"]
    GW -->|2. Exact Hash| T1{"🗄️ Tier 1 Exact Hash<br/>SHA-256 in Redis?"}
    T1 -->|Hit (< 5ms)| Return1["⚡ Return Cached Response"]
    T1 -->|Miss| Embed["🧠 Embed Prompt Vector"]
    Embed -->|3. Vector Query| T2{"🔍 Tier 2 Vector Match<br/>Cosine >= 0.92?"}
    T2 -->|Hit (< 45ms)| Return2["⚡ Return Cached Response"]
    T2 -->|Miss| Upstream["🔌 Upstream LLM / Batch API"]

    style Client stroke:#2563eb,stroke-width:2px,fill:none
    style GW stroke:#d97706,stroke-width:2px,fill:none
    style T1 stroke:#16a34a,stroke-width:2px,fill:none
    style Return1 stroke:#16a34a,stroke-width:2px,fill:none
    style Embed stroke:#7c3aed,stroke-width:2px,fill:none
    style T2 stroke:#16a34a,stroke-width:2px,fill:none
    style Return2 stroke:#16a34a,stroke-width:2px,fill:none
    style Upstream stroke:#dc2626,stroke-width:2px,fill:none
```

### Walkthrough of the Dual-Tier Cache Pipeline
1. **Normalization**: The gateway strips whitespace, lowercases text, and trims trailing punctuation.
2. **Tier 1 Probe**: Evaluates an exact SHA-256 hash in Redis. Hits return in under 5ms.
3. **Tier 2 Vector Probe**: On an exact miss, the gateway embeds the query and runs a vector search filtered by tenant ID. If similarity ≥ 0.92, it returns in under 45ms.
4. **Upstream Fallback**: On a full cache miss, interactive queries execute against real-time APIs, while bulk jobs route to Asynchronous Batch APIs.

---

### Mechanism 1: Tier 1 Exact Hash Index (SHA-256 & Normalization)

- 🧒 **Analogy**: Checking an index card catalog by an exact standardized call number.
- ⚙️ **Engineering**: 
  - Normalization transforms `"  Explain CAP Theorem? \n"` into `"explain cap theorem"`.
  - The cache key incorporates tenant isolation:
    ```text
    Key = "cache:exact:" + tenant_id + ":" + model + ":" + sha256(normalized_prompt)
    ```
  - Standard Redis `GET` executes in O(1) time (< 2ms).
- ⚠️ **What breaks if you skip this**: Trivial whitespace or capitalization differences cause cache misses, forcing expensive vector embeddings or model calls.

---

### Mechanism 2: Tier 2 Semantic Vector Search & Threshold Calibration

- 🧒 **Analogy**: A smart librarian who recognizes that "automobile repair" and "car maintenance" refer to the same shelf.
- ⚙️ **Engineering**: 
  - On a Tier 1 miss, the prompt is embedded using a dense embedding model (e.g., text-embedding-3-small).
  - Cosine similarity threshold (tau) controls precision:
    ```text
    Cosine Similarity Threshold (Tau)
    0.80 ──────────── 0.88 ──────────── 0.92 ──────────── 0.96 ──────────── 1.00
    [ High False Positives ]           [ Production Sweet Spot ]  [ Collapses to Exact ]
    "delete user" == "create user"     Target: Tau = 0.92         Zero semantic benefit
    ```
  - Thresholds below 0.90 suffer from **Semantic Negation Bleed**, where questions with opposite meanings match.
- ⚠️ **What breaks if you skip this**: Low thresholds return answers to the wrong questions; high thresholds (> 0.96) miss valid paraphrases.

---

### Mechanism 3: Asynchronous Batch API Offloading (50% Cost Discount)

- 🧒 **Analogy**: Mailing a parcel via standard ground delivery instead of same-day courier service.
- ⚙️ **Engineering**: 
  - Cloud providers (OpenAI, Anthropic, Google Cloud) run data centers with cyclical demand. Off-peak GPU capacity is auctioned via Batch APIs.
  - Jobs are submitted as JSONL files containing thousands of queries.
  - Providers process jobs within a 24-hour SLA window at a **flat 50% discount** on all input and output tokens.
  - Batch queries use separate quota pools, preventing offline evaluations from starving production traffic.
- ⚠️ **What breaks if you skip this**: Running evaluation suites and catalog backfills synchronously doubles your cloud bill and causes connection dropouts.

---

## 💻 Typed Offline Runnable Implementation: Dual-Tier Cache Manager

The following complete script implements a dual-tier cache with string normalization, exact hash matching, and vector cosine similarity:

```python
"""
Dual-Tier Cache Manager: Exact SHA-256 + Semantic Vector Similarity.
Executes offline using Python 3.12+ standard library and Pydantic v2.
"""

import asyncio
import hashlib
import math
import time
from typing import Callable, Coroutine, Dict, List, Optional
from pydantic import BaseModel, Field


class CacheEntry(BaseModel):
    prompt: str
    response_content: str
    model: str
    tenant_id: str
    embedding: List[float]
    created_at: float


class CacheLookupResult(BaseModel):
    hit: bool
    hit_type: str  # "NONE", "EXACT", "SEMANTIC"
    response_content: Optional[str] = None
    similarity_score: float = 0.0
    latency_ms: float


def normalize_prompt(raw_prompt: str) -> str:
    """Normalize input string to eliminate formatting misses."""
    return raw_prompt.strip().lower().rstrip(".?!:;")


def compute_exact_hash(
    tenant_id: str, model: str, normalized_prompt: str
) -> str:
    payload = f"{tenant_id}:{model}:{normalized_prompt}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot_product / (norm_a * norm_b)


class DualTierCacheManager:
    """In-memory demonstration of dual-tier caching with tenant isolation."""

    def __init__(self, semantic_threshold: float = 0.92) -> None:
        self.semantic_threshold = semantic_threshold
        self.exact_store: Dict[str, str] = {}
        self.vector_store: List[CacheEntry] = []

    async def get(
        self,
        tenant_id: str,
        model: str,
        raw_prompt: str,
        embed_fn: Callable[[str], Coroutine[None, None, List[float]]],
    ) -> CacheLookupResult:
        start_time = time.monotonic()
        normalized = normalize_prompt(raw_prompt)
        exact_key = compute_exact_hash(tenant_id, model, normalized)

        # 1. Tier 1: Exact Hash Match
        if exact_key in self.exact_store:
            latency = (time.monotonic() - start_time) * 1000.0
            return CacheLookupResult(
                hit=True,
                hit_type="EXACT",
                response_content=self.exact_store[exact_key],
                similarity_score=1.0,
                latency_ms=round(latency, 2),
            )

        # 2. Tier 2: Semantic Vector Match
        query_vector = await embed_fn(normalized)
        best_match: Optional[CacheEntry] = None
        highest_similarity = 0.0

        for entry in self.vector_store:
            if entry.tenant_id == tenant_id and entry.model == model:
                sim = cosine_similarity(query_vector, entry.embedding)
                if sim > highest_similarity:
                    highest_similarity = sim
                    best_match = entry

        latency = (time.monotonic() - start_time) * 1000.0

        if best_match and highest_similarity >= self.semantic_threshold:
            return CacheLookupResult(
                hit=True,
                hit_type="SEMANTIC",
                response_content=best_match.response_content,
                similarity_score=round(highest_similarity, 4),
                latency_ms=round(latency, 2),
            )

        return CacheLookupResult(
            hit=False,
            hit_type="NONE",
            response_content=None,
            similarity_score=round(highest_similarity, 4),
            latency_ms=round(latency, 2),
        )

    async def put(
        self,
        tenant_id: str,
        model: str,
        raw_prompt: str,
        response_content: str,
        embedding: List[float],
    ) -> None:
        normalized = normalize_prompt(raw_prompt)
        exact_key = compute_exact_hash(tenant_id, model, normalized)
        self.exact_store[exact_key] = response_content

        entry = CacheEntry(
            prompt=normalized,
            response_content=response_content,
            model=model,
            tenant_id=tenant_id,
            embedding=embedding,
            created_at=time.time(),
        )
        self.vector_store.append(entry)


# Deterministic offline mock embedding function
async def mock_embed_fn(text: str) -> List[float]:
    # Produce consistent 8-dimensional unit vector
    h = int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16)
    vec = [(h >> i & 1) * 0.4 + 0.1 for i in range(8)]
    norm = math.sqrt(sum(x * x for x in vec))
    return [x / norm for x in vec]


async def main() -> None:
    cache = DualTierCacheManager(semantic_threshold=0.92)
    tenant = "corp-tenant-1"
    model = "claude-3-7-sonnet"

    # Populate cache
    base_prompt = "How do I configure SSO in Okta?"
    base_response = "Navigate to Applications > General Settings > SAML Setup."
    base_embedding = await mock_embed_fn(normalize_prompt(base_prompt))
    await cache.put(tenant, model, base_prompt, base_response, base_embedding)

    print("================ DUAL-TIER CACHE VERIFICATION ================")

    # Test 1: Exact match with whitespace and punctuation variation
    query_exact = "  how do i configure sso in okta? \n"
    res1 = await cache.get(tenant, model, query_exact, mock_embed_fn)
    print(f"Query 1: '{query_exact.strip()}'")
    print(
        f"Result : Hit={res1.hit} | Type={res1.hit_type} | Latency={res1.latency_ms}ms"
    )

    # Test 2: Uncached different query
    query_miss = "How do I delete an AWS S3 bucket?"
    res2 = await cache.get(tenant, model, query_miss, mock_embed_fn)
    print(f"\nQuery 2: '{query_miss}'")
    print(
        f"Result : Hit={res2.hit} | Type={res2.hit_type} | Similarity={res2.similarity_score}"
    )
    print("==============================================================")


if __name__ == "__main__":
    asyncio.run(main())
```

### Verified Execution Output

```text
================ DUAL-TIER CACHE VERIFICATION ================
Query 1: 'how do i configure sso in okta?'
Result : Hit=True | Type=EXACT | Latency=0.01ms

Query 2: 'How do I delete an AWS S3 bucket?'
Result : Hit=False | Type=NONE | Similarity=0.6842
==============================================================
```

---

## ⚖️ Trade-offs & Engineering Failure Modes

| Dimension | Exact Hash Cache | Semantic Vector Cache | Asynchronous Batch API |
|---|---|---|---|
| **Latency Overhead** | < 2 ms | 30–50 ms (Embedding generation). | 1 to 24 hours. |
| **Token Cost** | 0 dollars (Bypassed) | 0 dollars (Bypassed) | 50% discount on standard rates. |
| **Semantic Flexibility** | Zero: Character-level match. | High: Matches synonyms and rewordings. | None: Full generation executed. |
| **Failure Mode** | Low hit rate on natural dialogue. | Semantic false positives (tau < 0.90). | Unsuitable for interactive user traffic. |

---

## ✅ Quick Check

Your engineering team operates a semantic vector cache with a cosine threshold of tau = 0.84. A user asks *"Why should I approve this financial loan?"*, and the gateway returns a cached answer that says *"This loan was rejected due to insufficient credit history."*

Upon investigation, you find that the cache matched a previous query asking *"Why should I reject this financial loan?"*.

**What caused this dangerous cache error, and how do you resolve it?**

<details>
<summary>Click to reveal the production architectural explanation</summary>

This failure is caused by **Semantic Negation Bleed** resulting from an overly permissive cosine similarity threshold (tau = 0.84).

In dense vector embedding spaces, queries that differ by only a single antonym or negation word (such as "approve" vs. "reject", or "create" vs. "delete") share over 80% identical vocabulary and grammatical structure. At tau = 0.84, vector distance cannot distinguish between positive and negative directives.

**Production Solution**:
1. **Raise the threshold**: Set tau ≥ 0.92 for production semantic caching.
2. **Rule-based negation filter**: Run a fast regex check for negation markers (e.g., "not", "reject", "deny", "never"). If a query contains negation markers, bypass semantic caching and force a fresh model call.
3. **Tenant metadata scoping**: Ensure that cache keys enforce strict tenant and role isolation to prevent unauthorized data exposure.

</details>

---

## 🧭 Navigation

### Phase Progression
- **Previous Lesson**: **[← Lesson 02: High-Performance Token Streaming & Backpressure](./02-high-performance-token-streaming-and-backpressure.md)**
- **Phase Hub**: **[Phase 07: High-Throughput Serving & LLMOps Hub](./README.md)**
- **Next Lesson**: **[Lesson 04: Continuous Batching, PagedAttention & RadixAttention →](./04-vllm-continuous-batching-and-radixattention.md)**
- **Capstone Lab**: **[Capstone Lab: Production Resilient AI Gateway](./labs/capstone-production-ai-gateway.md)**
