# 🏛️ AI Architecture Decision Records (ADRs)
### Definitive Architectural Trade-Offs, Decision Rubrics & Systemic Contracts

> **Formal records documenting high-stakes architectural choices, trade-offs, and technical policies across the AI-Native engineering stack.**  
> [Home / Master Curriculum](../../README.md) • [Production Readiness Review (PRR)](../production-readiness-review.md) • [Enterprise AI System Designs](../enterprise-ai-system-designs.md) • [Production Post-Mortems](../post-mortems/README.md)

---

## 🎯 Purpose of AI ADRs

In modern AI systems engineering, there is rarely a single "correct" answer. Every major architectural decision involves a tension between **latency, cost, reasoning capacity, operational complexity, and data privacy**.

Without formal Architecture Decision Records (ADRs):
* Engineering teams waste weeks litigating the same debates repeatedly (e.g., *"Should we use a dedicated vector DB or Postgres?"*).
* Developers chase unproven hype (e.g., deploying slow multi-agent swarms where a SQL query suffices).
* Systems accumulate hidden architectural debt with undocumented negative consequences.

These ADRs provide **battle-tested, defensible decisions** ready for Architectural Review Boards (ARBs).

---

## 📑 ADR Repository Index

| ADR ID | Decision Title | Phase Alignment | Status | Primary Decision Driver |
| :---: | :--- | :---: | :---: | :--- |
| [**ADR-001**](./ADR-001-pgvector-vs-dedicated-vector-database.md) | **PostgreSQL `pgvector 0.7+` vs. Dedicated Vector Engines (Qdrant / Milvus)** | `Phase 02` (Retrieval) | `ACCEPTED` | Operational simplicity & unified ACID transactions vs. 100M+ high-QPS sharding. |
| [**ADR-002**](./ADR-002-model-context-protocol-vs-bespoke-api-integrations.md) | **Model Context Protocol (MCP) vs. Bespoke REST / gRPC Tool Bindings** | `Phase 03` (Tools & MCP) | `ACCEPTED` | Vendor-neutral tool interoperability, client-side schema caching & microVM isolation. |
| [**ADR-003**](./ADR-003-test-time-compute-vs-domain-slm-routing.md) | **Frontier Reasoning Models (Test-Time Compute) vs. Local Domain SLMs** | `Phase 00` • `Phase 07` | `ACCEPTED` | High-complexity System 2 verification vs. sub-50ms unit economics at scale. |
| [**ADR-004**](./ADR-004-radixattention-kv-cache-vs-external-memory-stores.md) | **RadixAttention Shared KV-Cache Prefill vs. External Semantic Memory Stores** | `Phase 00` • `Phase 07` | `ACCEPTED` | Prefill latency & GPU bandwidth reduction vs. cross-session episodic knowledge persistence. |
| [**ADR-005**](./ADR-005-agent-to-agent-a2a-vs-model-context-protocol-mcp.md) | **Agent-to-Agent (A2A) Protocol vs. Model Context Protocol (MCP) Boundary** | `Phase 04` • `Phase 03` | `ACCEPTED` | Horizontal inter-agent federation & capability cards vs. vertical deterministic tool execution. |
| [**ADR-006**](./ADR-006-native-fp8-precision-vs-4bit-weight-quantization.md) | **Native FP8 Precision (E4M3/E5M2) vs. 4-Bit Weight Quantization (AWQ/GPTQ)** | `Phase 00` • `Phase 07` | `ACCEPTED` | Native Hopper/Blackwell Tensor Core throughput & FP8 KV-cache vs. 4-bit register unpack overhead. |

---

## 📐 Standard AI ADR Template

When authoring a new ADR for this repository or your enterprise organization, use this standardized structure:

```markdown
# ADR-XXX: [Title: Short Description of Decision]

## Status
[PROPOSED | ACCEPTED | DEPRECATED | SUPERSEDED by ADR-YYY]

## Context & Problem Statement
* What technical dilemma or business constraint requires a decision?
* What are the physical constraints (memory bandwidth, latency SLAs, unit economics)?

## Decision Drivers
* Driver 1 (e.g., P99 Latency SLA < 200ms)
* Driver 2 (e.g., Cloud token expenditure budget < $0.005 per user interaction)
* Driver 3 (e.g., Operational overhead of running a dedicated database cluster)

## Considered Alternatives
* **Alternative A:** [Description]
* **Alternative B:** [Description]
* **Alternative C:** [Description]

## Decision Outcome
* **Chosen Option:** [Option X]
* **Justification & Trade-Off Analysis:** Why this option wins despite its weaknesses.

## Architectural Trade-Off Scorecard
| Criterion | Option A | Option B | Option C |
| :--- | :---: | :---: | :---: |
| Latency SLA | ... | ... | ... |
| Infrastructure Cost | ... | ... | ... |
| Operational Complexity | ... | ... | ... |

## Negative Consequences & Mitigations
* **Consequence 1:** [Downside] → **Mitigation:** [How we protect against it]
* **Consequence 2:** [Downside] → **Mitigation:** [How we protect against it]

## References & Seminal Papers
* [Link to benchmark, research paper, or RFC]
```
