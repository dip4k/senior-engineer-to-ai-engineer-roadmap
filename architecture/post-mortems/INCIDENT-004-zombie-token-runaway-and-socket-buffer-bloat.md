# INCIDENT-004: Zombie Token Runaway & Socket Buffer Bloat in SSE Streaming

## Metadata
* **Incident Date:** 2026-06-15
* **Severity Level:** `SEV-1` (GPU Cluster Saturation & Uncontrolled Inference Bleed)
* **Incident Commander:** Principal Infrastructure & LLMOps Architect
* **Time to Detect (TTD):** 42 minutes
* **Time to Mitigate (TTM):** 18 minutes

---

## 1. Executive Summary & Impact

On Friday at 21:15 UTC, following the rollout of deep reasoning models (16,384 max output tokens for complex code generation), our production AI Gateway experienced catastrophic inference queue saturation.

End users submitting long reasoning queries experienced Time To First Token (TTFT) latencies of 15–30 seconds. Frustrated users closed browser tabs, refreshed web pages, or closed laptop lids. 

While the downstream client HTTP Server-Sent Events (SSE) connections were severed at the ingress load balancer, the **API Gateway failed to propagate client cancellation signals upstream to our self-hosted GPU inference cluster (vLLM on 32× NVIDIA H100 GPUs)**. 

The inference cluster continued autoregressively generating all 16,384 tokens to completion for thousands of abandoned requests ("zombie tokens"). Over the next **42 minutes**, over **4,200 zombie generation jobs** clogged GPU worker queues, writing gigabytes of unread token chunks into overflowing OS socket buffers.

```text
Active Live Users: 120
Orphaned "Zombie" Inference Jobs Running on H100s: 4,218
GPU Worker Queue Saturation: 100% (All Tensor Cores pinned at 99% compute)
P99 TTFT for Legitimate Users: Spiked from 140ms to 32,500ms
```

### Blast Radius Metrics
* **Financial Waste:** **$38,400 in unread GPU compute** burned over 42 minutes.
* **Service Availability:** P99 TTFT degraded by 23,000% (from 140ms to 32.5s); 85% of legitimate user queries timed out with HTTP 504.
* **Memory Exhaustion:** Gateway pods suffered kernel Out-Of-Memory (OOMKilled) crashes due to unbounded TCP socket buffers buffering unconsumed SSE token payloads.

---

## 2. Root Cause Analysis (The 5 Whys)

1. **Why did GPU worker queues saturate when live traffic was falling?**  
   Because the GPU inference engines were executing 4,200 long-context generation jobs for clients that had already disconnected.
2. **Why did the inference engines continue generating tokens after clients left?**  
   Because the internal inference engine (vLLM) never received an `abort_request(request_id)` RPC call from the AI Gateway.
3. **Why didn't the AI Gateway cancel the background inference task?**  
   Because the gateway's token streaming endpoint iterated over the upstream generator inside a standard Python loop without polling `await request.is_disconnected()`.
4. **Why wasn't an exception raised when writing to the closed socket?**  
   Because intermediate TCP socket buffers and reverse proxies absorbed writes without throwing `ConnectionResetError` or `BrokenPipeError` until the TCP socket buffer completely filled.
5. **Why were long reasoning models deployed without active cancellation?**  
   Because initial load testing used synthetic `curl` clients that ran to completion, failing to simulate realistic browser behaviors (tab closures, page refreshes, and network drops during 30-second reasoning chains).

---

## 3. The Broken Flow vs. Inoculated Architecture

```mermaid
flowchart TD
    subgraph BrokenFlow["Broken: Silent Disconnect Flow"]
        ClientA["📱 Browser Client<br>(Closes tab after 8s)"] -.->|TCP FIN / Drop| LB1["⚖️ Ingress Load Balancer<br>(Silently buffers)"]
        LB1 -.->|No Signal| Gate1["🚪 API Gateway<br>(Iterates blindly without disconnect check)"]
        Gate1 -->|Requests continue| GPU1["🔥 H100 GPU Cluster (vLLM)<br>(Generates all 16k tokens • 100% compute waste)"]
    end

    subgraph InoculatedFlow["Fixed: Active Abort Flow"]
        ClientB["📱 Browser Client<br>(Closes tab after 8s)"] -.->|TCP FIN / Drop| LB2["⚖️ Ingress Load Balancer"]
        LB2 -->|TCP Socket Severed| Gate2["🚪 API Gateway<br>• SSE Heartbeat Probe<br>• request.is_disconnected() == True"]
        Gate2 -->|Raise asyncio.CancelledError| Cancel["🛑 Task Cancellation Context"]
        Cancel -->|RPC engine.abort(request_id)| GPU2["⚡ H100 GPU Cluster (vLLM)<br>(KV Cache freed immediately • Zero compute waste)"]
    end
```

#### Diagram Walkthrough:
1. **Broken Flow (Incident State)**: When a user closed their browser, intermediary proxies absorbed connection termination without notifying the gateway. The gateway continued streaming tokens from the GPU cluster until max token limits were reached, burning compute on non-existent consumers.
2. **Inoculated Flow (Production Fix)**: The gateway continuously probes connection liveness via periodic SSE comment heartbeats and `request.is_disconnected()` checks on every token. Upon disconnect detection, the gateway immediately dispatches an `engine.abort(request_id)` RPC call to vLLM, instantly evicting the KV cache and stopping GPU execution.

---

## 4. Immediate Triage & Containment

1. **Flushed Inference Queues (T+15m):** Executed administrative control plane command on vLLM orchestrator to flush all waiting request queues (`vllm admin flush-queue`).
2. **Rebooted Saturated Pods (T+22m):** Scaled down and restarted all API Gateway pods to purge bloated TCP socket buffers and release stranded memory.
3. **Hard Concurrency Throttle (T+28m):** Temporarily capped per-user concurrent generation requests to `1` and restricted `max_tokens` to `4,096` while deploying the permanent code inoculation.

---

## 5. Permanent Architectural Inoculations

### Inoculation 1: Active Disconnect Detection & Upstream Cancellation
Updated the streaming generator in the AI Gateway to poll socket status on every token yield and guarantee upstream abortion in a `finally` block:

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio

@app.post("/v1/chat/completions")
async def stream_chat_completion(request: Request, payload: ChatPayload):
    request_id = str(uuid.uuid4())
    
    async def token_generator():
        try:
            async for token_chunk in vllm_engine.generate(payload, request_id=request_id):
                # Check if client connection was severed
                if await request.is_disconnected():
                    raise asyncio.CancelledError("Client disconnected")
                
                yield f"data: {token_chunk.to_json()}\n\n"
        except (asyncio.CancelledError, GeneratorExit):
            # MANDATORY: Abort upstream inference immediately
            await vllm_engine.abort(request_id)
            raise
        finally:
            # Ensure engine resources are freed even on unexpected exceptions
            await vllm_engine.abort(request_id)

    return StreamingResponse(
        token_generator(), 
        media_type="text/event-stream",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"}
    )
```

### Inoculation 2: Periodic SSE Comment Heartbeats
Configured the gateway to interleave active comment heartbeats (`: keep-alive\n\n`) every 10 seconds during reasoning phases to force socket writes and detect dead TCP pipes immediately rather than waiting for completion.

### Inoculation 3: Reverse Proxy Unbuffered Streaming (`X-Accel-Buffering: no`)
Configured NGINX and Envoy ingress proxies to disable HTTP response buffering for `/sse` routes. This prevents proxies from absorbing up to 4MB of generated tokens in memory before noticing that the client closed the connection.

### Inoculation 4: Automated Chaos Test in CI/CD
Added an automated integration test in CI/CD:
* Test client initiates an inference request with `max_tokens: 8192`.
* Test client terminates TCP socket after 3 tokens.
* Assertion verifies that GPU inference engine receives `abort_request` within < 250ms and that zero further tokens are generated.

---

## 6. SRE Lessons Learned

* **Streaming changes failure semantics:** In request-response APIs, once a request reaches the backend, completing it is usually safe and cheap. In autoregressive token generation, completing an unread request costs real dollars and GPU capacity on every single token step.
* **Never trust TCP writes without liveness probes:** High-throughput streaming services must treat network disconnections as high-priority control events that halt compute immediately.
