# INCIDENT-001: The Cascading KV-Cache Stampede

## Metadata
* **Incident Date:** 2026-03-14
* **Severity Level:** `SEV-1` (Critical Production Degradation)
* **Incident Commander:** Staff SRE & AI Infrastructure Lead
* **Time to Detect (TTD):** 8 minutes
* **Time to Mitigate (TTM):** 42 minutes

---

## 1. Executive Summary & Impact

At 14:15 UTC, our customer-facing Enterprise Semantic Search and Copilot platform experienced an immediate 50x spike in latency. Over the next 35 minutes, P99 Time to First Token (TTFT) degraded from **90ms to 4,800ms**, causing 504 Gateway Timeouts across checkout and customer operations.

The incident was triggered by a routine PR deployment that added a dynamic ISO timestamp string (`"Current time: 2026-03-14T14:15:02Z"`) to line 1 of the master system prompt template. This single change modified the first 12 tokens of the prompt on every millisecond turn, instantly dropping our RadixAttention shared KV-cache hit rate from **82% to 0%** across our 64-GPU serving cluster (NVIDIA H100s running SGLang).

The cluster was hit by a massive **KV-Cache Stampede**: 1,200 incoming requests per second, which had previously shared warm cached prefixes, were suddenly forced into full prefill computation simultaneously. High Bandwidth Memory (HBM) saturated, request queues backed up, and GPUs began dropping requests due to queue timeouts.

### Blast Radius Metrics
* **Latency Impact:** P99 TTFT increased from **90ms to 4,800ms** (5,233% increase).
* **Throughput Drop:** System throughput collapsed from 1,450 req/sec to 210 req/sec.
* **Redundant Compute Cost:** Incurred an estimated **\$38,000** in redundant GPU prefill compute cycles over 42 minutes.
* **Customer Impact:** 42,000 corporate end-users encountered gateway timeouts or degraded search fallbacks.

---

## 2. Incident Timeline (UTC)

```
14:12 - PR #1482 merged to main: "Add dynamic current timestamp to agent context for recency grounding."
14:15 - Deployment pipeline finishes rolling out to all 8 Kubernetes inference pods (64 H100 GPUs).
14:16 - RadixAttention prefix cache hit rate plummets from 82.4% to 0.1%.
14:18 - SRE PagerDuty alert fires: "P99 TTFT > 2000ms on /v1/chat/completions."
14:20 - Incident Commander opens bridge. Initial hypothesis: "Upstream Azure OpenAI throttling or DDoS attack."
14:24 - Verification reveals network ingress traffic is normal (1,200 req/sec), but GPU SM (Streaming Multiprocessor) utilization is pinned at 100% across all nodes.
14:28 - SRE inspects SGLang metrics: `cache_hit_rate` is flatlined at 0%. Every request is computing 6,000 prefill tokens from scratch.
14:32 - Root cause identified: PR #1482 inserted dynamic timestamp at token position 0 in the system prompt.
14:36 - Emergency hotfix branch opened: moving timestamp from system prompt prefix to the user message suffix.
14:48 - Hotfix image built and deployed to canary cluster. Prefix cache hit rate instantly recovers to 84%.
14:57 - Full cluster cutover complete. TTFT returns to 88ms. Error rate drops to 0.01%. Incident closed.
```

---

## 3. Root Cause Analysis (The 5 Whys)

1. **Why did customer latency spike by 50x?**  
   Because all 64 H100 GPUs were overwhelmed by simultaneous prefill computation for thousands of concurrent requests.
2. **Why were the GPUs doing full prefill computation instead of using cached KV activations?**  
   Because the RadixAttention cache hit rate dropped from 82% to 0%, meaning no request could reuse memory from previous requests.
3. **Why did the Radix tree fail to match prefixes across requests?**  
   Because the first 12 tokens of the prompt differed on every single request (`2026-03-14T14:15:02.124Z`).
4. **Why was a unique timestamp placed at the beginning of the prompt?**  
   Because an engineer followed a general prompt engineering tutorial recommending: *"Always tell the model what the current date and time is at the start of your system prompt."*
5. **Why was this change allowed into production without flagging the cache invalidation?**  
   Because our CI/CD pipeline tested only answer accuracy on single isolated queries in staging, with zero telemetry or regression gates monitoring **KV-cache prefix hit rates under concurrency**.

---

## 4. Immediate Triage & Containment

1. **Fast Rollback:** Deployed an immediate emergency patch stripping the timestamp from line 1 of the template.
2. **Traffic Throttling:** Engaged Envoy rate-limiting tiers on non-critical background jobs to allow the GPU queues to drain their in-flight backlog.

---

## 5. Architectural Inoculation (Permanent Systemic Guardrails)

To guarantee that this class of hardware failure can never happen again, we deployed three permanent systemic controls:

### 1. The "Static Prefix Invariant" CI/CD Linter
We instituted an automated AST static analysis check in our PR pipeline. All system prompts are compiled and validated against an invariant rule:
```python
# tests/architecture/test_prompt_prefix_invariants.py
def test_system_prompt_prefix_is_static(template):
    """Guarantees that the first 500 tokens of the system prompt are 100% static."""
    prefix_tokens = tokenize(template.get_static_prefix())
    assert len(prefix_tokens) >= 500, "Static prefix must be at least 500 tokens for Radix sharing"
    assert "{" not in template.get_static_prefix(), "Dynamic template variables strictly forbidden in prefix!"
```

### 2. Moving Dynamic Variables to the Tail
Dynamic metadata (current time, session ID, user location) is now strictly appended to the **user turn envelope** at the end of the context window:
```markdown
<!-- CORRECT ARCHITECTURE: Static Prefix First -->
[STATIC SYSTEM PROMPT: Guidelines, Policies, Tools] (Tokens 0 - 2,500) -> 100% KV-Cache Reuse
[USER MESSAGE: "Find my recent orders"]
[DYNAMIC METADATA: {"timestamp": "2026-03-14T14:15:02Z", "tz": "UTC"}] (Tail Tokens)
```

### 3. Automated Cache-Hit Regression Gate
Added a synthetic load test in staging that fires 100 concurrent requests against any modified prompt template. If the verified `cache_hit_rate` falls below **70%**, the deployment automatically fails.
