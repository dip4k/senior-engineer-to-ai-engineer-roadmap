# Diagram Architecture & Mermaid Standards

This document establishes the design, syntax, and explanation rules for diagrams across the curriculum.

---

## 1. The Core Diagram Rule

> **Never place a diagram in a lesson without an accompanying step-by-step prose explanation.**

A diagram is a visual anchor, not a replacement for clear instruction. If a reader cannot follow the flow of data or understand what occurs at each boundary, the diagram has failed.

---

## 2. Supported Diagram Types & Topologies

Use native Mermaid syntax within standard markdown code blocks:

| Intent | Diagram Type | Best Practices |
|---|---|---|
| **Data Ingestion & Pipelines** | `flowchart LR` | Left-to-right flow; clean separation between stages. |
| **Multi-Stage Decision Trees** | `flowchart TD` | Top-down decision branches; clearly labeled condition edges. |
| **Tool Calling & Wire Protocols** | `sequenceDiagram` | Show client, gateway, agent runtime, and MCP server actors with request/response payloads. |
| **Agent State Lifecycles** | `stateDiagram-v2` | State transitions (`Idle` → `Planning` → `ToolExecution` → `Quarantine`). |

---

## 3. Structural Rules & Clean Layouts

1. **Node Limit**: Keep diagrams under 10–12 nodes. If a system is more complex, break it into a macro-architecture diagram followed by focused micro-architecture diagrams in subsequent sections.
2. **Subgraphs**: Use `subgraph` blocks to indicate trust boundaries, process boundaries, or infrastructure tiers (e.g., *Client Tier*, *Gateway Tier*, *GPU Inference Engine*).
3. **Escaping**: Always quote labels containing parentheses, brackets, or colons:
   ```mermaid
   nodeA["Client (gRPC / HTTP)"] --> nodeB["Gateway Tier: Token Bucket (100 req/s)"]
   ```
4. **No HTML**: Avoid inline `<br>`, `<b>`, or `<span>` tags inside labels whenever possible to ensure universal rendering across IDEs and GitHub.

---

## 4. Required Prose Walkthrough Pattern

Immediately following any diagram, provide a structured walkthrough using this pattern:

```markdown
### Visual Data Flow Breakdown (Example A: Hybrid Retrieval):
1. **Request Ingestion (Steps 1–2)**: The client query arrives at the Gateway. The token bucket rate limiter reserves tokens against tenant quotas before routing.
2. **Parallel Retrieval (Step 3)**: The query is simultaneously dispatched to the sparse BM25 index (lexical search) and the dense HNSW index (vector search).
3. **Reciprocal Rank Fusion (Step 4)**: Individual ranking scores are merged using the RRF constant k = 60 to yield a single calibrated candidate list.
4. **Cross-Encoder Reranking (Step 5)**: The top 25 candidates are evaluated by a cross-encoder model to determine semantic relevance before passing context to the LLM.
5. **Telemetry & Tracing (Step 6)**: Spans recording retrieval latency, candidate counts, and token costs are emitted to the OpenTelemetry collector.

### Visual Data Flow Breakdown (Example B: Stateful Agent WAL Loop):
1. **Client Event Ingestion**: An incoming task payload enters the agent runtime and is assigned a unique idempotency key.
2. **Pre-Execution Write**: The orchestrator appends a `TaskStarted` event to the Write-Ahead Log (WAL) event store before initiating reasoning.
3. **Bounded Reasoning Loop**: The model proposes a tool call. The orchestrator checks the turn counter (max 10) and budget decay.
4. **ABAC Policy Verification**: The requested MCP tool and arguments are checked against the tenant policy server. If denied, a quarantine event is logged.
5. **Tool Execution & State Commit**: The tool runs, output is captured, and a `ToolCompleted` event is persisted to disk before returning results to the client.
```

