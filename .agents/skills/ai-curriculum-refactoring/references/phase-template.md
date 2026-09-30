# Phase README Architectural Specification

This document defines how Phase READMEs must be structured.

---

## 🚫 The Anti-Pattern: The Monolithic README

In early iterations, phase directories often contain an 800+ line `README.md` that crams all lesson content, documentation snippets, cheat sheets, and code listings into a single file.

**Consequences of the Monolith**:
- Overwhelming cognitive load for the learner.
- Inability to link directly to specific lessons.
- Hard to update and maintain.
- Blurs the line between high-level architecture and low-level code mechanics.

---

## ✅ The Target Pattern: The Orientation & Navigation Hub

A Phase `README.md` must serve as an **Architectural Orientation Hub**, guiding the learner through self-contained, modular lesson files (`01-....md`, `02-....md`).

### Standard Phase README Structure

```markdown
# Phase <XX>: <Phase Title>

> **Architectural overview and learning progression for Lead Developers and Solutions Architects.**

---

## 🎯 Phase Engineering Goal
Explain the overarching production capability delivered by this phase:
- What end-to-end system does this phase prepare the engineer to architect?
- What major production challenges are addressed?

---

## 🧒 Phase Mental Model & Real-World Intuition
Start with an accessible, high-impact mental model (ELI10) that grounds the entire phase:
- Frame the system using a relatable, human-scale analogy (e.g. *Closed-Book vs. Open-Book Exam*, *The Detective and the Library*, *Operating System Kernel vs. User Space*).
- Contrast the intuitive mental model directly with the probabilistic realities of neural models.

---

## 🗺️ Phase Blueprint & System Topology

Include an authoritative, modern Mermaid diagram using semantic UI color styling:

```mermaid
flowchart TD
    subgraph PHASE1["Phase 1: Ingestion & Preparation (Offline Prep)"]
        D["1. Source Records<br>(Raw Documents)"] --> P["2. Structural Parsing<br>(Clean Layout)"]
        P --> E["3. Dual-Indexing<br>(Lexical + Semantic)"]
    end

    subgraph PHASE2["Phase 2: Execution & Serving (Online Runtime)"]
        Q["User Request"] --> R["4. Search & Rerank<br>(RRF + Cross-Encoder)"]
        R --> S["5. Model Synthesis<br>(Grounded Citations)"]
        S --> G{"6. Verification Gate<br>Factual Grounding?"}
        G -- "Yes" --> OUT["Verified Output"]
        G -- "No" --> ABSTAIN["Quarantine & Abstain"]
    end

    style PHASE1 fill:none,stroke:#2563eb,stroke-width:2px
    style PHASE2 fill:none,stroke:#16a34a,stroke-width:2px

    style G stroke:#d97706,stroke-width:2px
    style OUT stroke:#16a34a,stroke-width:2px
    style ABSTAIN stroke:#dc2626,stroke-width:2px
    style S stroke:#7c3aed,stroke-width:2px
```

### Visual Architecture Walkthrough:
Walk through the numbered steps in 3–5 bullet points.

---

## 📊 Evolution: Naive Prototype vs. Modern Production Architecture

Every phase README must contrast the early/naive approach against the modern production standard:

| Architecture Layer | Naive Prototype (2023) | Modern Enterprise Standard (2026) |
|---|---|---|
| **Data Ingestion** | Blind token slicing | Layout-aware semantic parsing + contextual prepending |
| **Search / Storage** | Single vector store | Hybrid dual-indexing (Dense + BM25) with predicate filtering |
| **Scoring & Merging** | Heuristic distance thresholds | Reciprocal Rank Fusion (RRF) + Cross-Encoder attention |
| **Output Attestation** | Unverified generation | Groundedness verification gates & inline source citations |

---

## 📚 Modular Curriculum Lessons (Master Navigation Table)

| # | Lesson / Module | Tier | Est. Time | Core Systems Focus | Key Engineering Outcome |
|---|---|---|---|---|---|
| **01** | [Foundational Primitive](./01-<topic>.md) | `🟢 Core` | ~18 min | Architectural or mathematical core | Measurable baseline capability |
| **02** | [Core Implementation / Deep Dive](./02-<topic>.md) | `⚫ Deep Dive` | ~22 min | Deterministic system mechanism | Fault-tolerant execution pattern |
| **03** | [Advanced Scaling](./03-<topic>.md) | `🟡 Engineering Depth` | ~20 min | High-concurrency / distributed optimization | Production throughput & latency SLA |
| **04** | [Production Defense / Telemetry](./04-<topic>.md) | `🔵 Advanced` | ~22 min | Guardrails, evaluations, or observability | Enterprise compliance & failure recovery |

### Exemplar Lesson Maps by Curricular Phase:
- **Phase 00 (Foundations)**: Tokenization & BPE → Attention & KV Cache Memory → Prefill vs. Decode Physics → Chunked Prefill & FlashAttention.
- **Phase 01 (Context)**: In-Context Learning → Constrained Grammar Decoding → JSON Schema Marshaling → Context Pruning ASTs.
- **Phase 02 (Retrieval)**: Document Parsing → Dense/Sparse Indexing → Hybrid Search & RRF → Cross-Encoder Reranking → GraphRAG.
- **Phase 03 (Tools & MCP)**: JSON-RPC 2.0 Wire Protocol → MCP Stdio/SSE Servers → ABAC Policy Gates → Tool Idempotency.
- **Phase 04 (Agents)**: Bounded ReAct Loops → Event-Sourced Write-Ahead Logs → Crash Replay & State Hydration → Multi-Agent Supervisors.
- **Phase 05 (Security)**: Prompt Injection Vectors → Dual-LLM Quarantine → Tool Execution Firewalls → Automated Red-Teaming.
- **Phase 06 (Evals & OTel)**: Synthetic Test Datasets → LLM-as-a-Judge Calibration → OpenTelemetry GenAI Spans → CI/CD Evaluation Gates.
- **Phase 07 (Serving)**: Continuous Batching Engines → PagedAttention Internals → AWQ/GPTQ Quantization → Speculative Decoding.
- **Phase 08 (SDLC)**: Spec-Driven Code Generation → Agentic Pull Request Reviewers → Enterprise AI Governance.

---

## 🛠️ Associated Hands-On Labs

Point to the executable implementation and automated verification harness:
- **Lab Location**: `labs/lab-XX-<topic>.md` or `agent-forge/<module>/`
- **Verification Command**:
  ```bash
  python scripts/verify_lab.py --lab <XX>
  ```

---

## 📋 Prerequisites & Cross-Phase Dependencies

- **Required Prior Knowledge**: Link to preceding phases across the 00–08 roadmap (e.g., "Requires Phase 01: Context Engineering & Token Mechanics").
- **Downstream Beneficiaries**: Explain where these skills are leveraged later (e.g., "Feeds into Phase 04: Stateful Agent Orchestration").

---

## 📚 Curated Primary Sources & Verification References
Only list authoritative primary sources:
- Original arXiv whitepapers
- Official protocol standards (MCP, OpenTelemetry GenAI)
- Official engineering blogs (Anthropic Research, OpenAI Engineering, Google DeepMind)

---

## 🧭 Navigation (Mandatory)

### Phase Progression
- **Previous Phase**: **[← Phase <XX-1>: <Title>](../<phase-prev>/README.md)**
- **Next Phase**: **[Phase <XX+1>: <Title> →](../<phase-next>/README.md)**

### Direct Chapter & Lesson Directory
- **[Lesson 01: <Title>](./01-<topic>.md)**
- **[Lesson 02: <Title>](./02-<topic>.md)**
- **[Lesson 03: <Title>](./03-<topic>.md)**
- **[Lesson 04: <Title>](./04-<topic>.md)**
- **[Platform Appendix: <Title>](./reference/<topic>.md)**
- **[Hands-On Capstone Lab: <Title>](./labs/<lab-topic>.md)**
```
