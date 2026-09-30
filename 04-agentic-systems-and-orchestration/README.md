# Phase 04: Agentic Systems & Orchestration

> **A Guide to Designing, Scaling, and Operating Deterministic Workflows, Autonomous Agents, and Multi-Agent Systems.**

---

## 🎯 Phase Engineering Goal

This phase covers how to build **resilient, stateful, distributed agent loops**. 

You will transition from viewing foundation models as basic request-response endpoints to building reliable agent systems. By the end of this phase, you will understand:
1. **Deterministic Workflows**: Using core workflow patterns (Prompt Chaining, Routing, Parallelization, Evaluator-Optimizer) to build reliable systems.
2. **Execution Governors**: Hardening reasoning loops with cycle detection and budget limits to prevent infinite loops and runaway costs.
3. **Stateful Durability**: Implementing Write-Ahead Logs (WAL), resuming from crashes, and session recovery.
4. **Agent Memory**: Organizing working context, short-term buffers, and long-term memory.
5. **Multi-Agent Coordination**: Delegating tasks between specialized agents.
6. **Code Execution Sandboxing**: Safely running model-generated code in isolated environments.

---

## 🗺️ Learning Path & System Topology

Phase 04 accommodates two distinct engineering learning profiles:

```mermaid
flowchart TD
    classDef core fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef track fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef lab fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;

    Start(["Start Phase 04"]) --> L1["Lesson 01: Workflows vs Agents & Patterns"]:::core
    L1 --> L2["Lesson 02: ReAct Loops & Governors"]:::core
    L2 --> L3["Lesson 03: Stateful Sessions & Durability"]:::core
    
    subgraph FastTrack["⚡ Fast Track: Application Engineer"]
        direction TB
        L3 --> Lab1["Lab 1: Stateful Agent with Approval"]:::lab
        L3 --> Lab3["Lab 3: Infinite Loop Detection"]:::lab
    end
    
    subgraph EnterpriseTrack["🏢 Enterprise Track: Platform Architect"]
        direction TB
        L3 --> L4["Lesson 04: Agent Memory Systems"]:::core
        L4 --> L5["Lesson 05: Multi-Agent Coordination"]:::core
        L5 --> L6["Lesson 06: Code Execution Sandboxes"]:::core
        L6 --> L7["Lesson 07: Modern Agent Platforms"]:::core
        L7 --> Capstone["Capstone: Code Review Agent Engine"]:::lab
    end

    Lab3 --> Done(["Phase 04 Mastery"])
    Capstone --> Done
```

### Modular Curriculum Directory

| Lesson | Title | Tier Badge | Concept |
|:---:|---|:---:|---|
| **01** | [Workflows vs. Agents & Patterns](01-workflows-vs-agents-and-orchestration-patterns.md) | `HIGH ROI / CORE` | Chaining, routing, parallel voting, orchestrator-worker architectures. |
| **02** | [ReAct Loops & Execution Governors](02-react-loops-and-execution-governors.md) | `HIGH ROI / CORE` | The ReAct loop (Thought, Action, Observation), preventing infinite loops, error recovery. |
| **03** | [Stateful Sessions & Durable WAL](03-stateful-sessions-and-durable-wal-persistence.md) | `IMPORTANT / NEXT` | Event-sourcing, Write-Ahead Logs (WAL), crash recovery. |
| **04** | [Agent Memory Systems](04-agent-memory-systems-and-cognitive-architectures.md) | `IMPORTANT / NEXT` | Working context, session memory, long-term semantic memory. |
| **05** | [Multi-Agent Coordination](05-multi-agent-coordination-and-a2a-protocols.md) | `ADVANCED / SPECIALIZED` | Handoff mechanisms, agent-to-agent delegation, multi-agent frameworks. |
| **06** | [Code-as-Action & Sandboxing](06-codeact-and-sandboxed-execution-runtimes.md) | `ADVANCED / SPECIALIZED` | Writing and executing code on the fly securely, microVMs. |
| **07** | [Agent Development Platforms](07-agent-development-platforms-and-adks.md) | `REFERENCE / AWARENESS` | Overview of tools like LangGraph, Semantic Kernel, and modern Agent SDKs. |

---

## 🔗 Curriculum Dependency Graph

```mermaid
flowchart LR
    P03["Phase 03: Tools & Model Context Protocol"] --> P04
    
    P04 --> P05["Phase 05: AI Security & Guardrails"]
    P04 --> P06["Phase 06: GenAI Evals & Observability"]
    P04 --> P07["Phase 07: High-Throughput Serving & LLMOps"]
```

* **Required Prior Knowledge**:
  * [Phase 01: Prompt & Context Engineering](../01-prompt-and-context-engineering/README.md): Few-shot exemplars, structured JSON schemas, in-context learning.
  * [Phase 02: Enterprise Retrieval & Knowledge Systems](../02-rag-and-knowledge-systems/README.md): Embedding vector search, hybrid retrieval.
  * [Phase 03: Tools & Model Context Protocol (MCP)](../03-tools-and-model-context-protocol/README.md): JSON-RPC 2.0 tool schemas, execution boundaries.

---

## 🧭 Navigation

### Phase Progression
* **Previous Phase**: [← Phase 03: Tools & Model Context Protocol (MCP)](../03-tools-and-model-context-protocol/README.md)
* **Next Phase**: [Phase 05: AI Security & Guardrails →](../05-ai-security-and-guardrails/README.md)

### Direct Chapter & Lesson Directory
* **[Lesson 01: Workflows vs. Agents & Orchestration Patterns](01-workflows-vs-agents-and-orchestration-patterns.md)**
* **[Lesson 02: Autonomous ReAct Loops & Execution Governors](02-react-loops-and-execution-governors.md)**
* **[Lesson 03: Stateful Sessions, Durable WAL & Distributed Sagas](03-stateful-sessions-and-durable-wal-persistence.md)**
* **[Lesson 04: Agent Memory Systems & Cognitive Architectures](04-agent-memory-systems-and-cognitive-architectures.md)**
* **[Lesson 05: Multi-Agent Coordination & Protocols](05-multi-agent-coordination-and-a2a-protocols.md)**
* **[Lesson 06: Code-as-Action (CodeAct) & Execution Sandboxes](06-codeact-and-sandboxed-execution-runtimes.md)**
* **[Lesson 07: Modern Agent Development Platforms](07-agent-development-platforms-and-adks.md)**
