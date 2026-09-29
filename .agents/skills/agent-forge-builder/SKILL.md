---
name: agent-forge-builder
description: >-
  Specialized skill for engineering, extending, testing, and debugging the
  agent-forge microservices framework in this repository. Use when building or
  modifying gateway, retrieval, runtime, mcp, evals, or observability components.
---

# 🏗️ Agent Forge Builder Skill

Use this skill when developing, refactoring, or extending the `agent-forge/` microservices codebase.

## 📁 Architecture Overview

```
agent-forge/
├── agent_forge/
│   ├── gateway/          # Rate limiting (TokenBucketLimiter), model routing, semantic cache
│   ├── retrieval/        # Dense vector store, BM25, HybridRetriever, ACORN-1 search
│   ├── runtime/          # DurableOrchestrator, EventStore (WAL), AgentSession models
│   ├── mcp/              # JSON-RPC protocol, PolicyEngine, Payment/Order/Policy servers
│   ├── observability/    # GenAITracer, Span, OpenTelemetry GenAI semantic conventions
│   └── evals/            # Groundedness judge, trajectory evaluation, metrics
└── tests/
    └── test_all.py       # Comprehensive unit and integration test suite
```

## 🛠️ Step-by-Step Development Procedures

### 1. Adding a New MCP Tool
1. Create or open a server in `agent_forge/mcp/servers/`.
2. Define the tool specification in `list_tools()` with `name`, `description`, and JSON Schema `input_schema`.
3. Implement execution in `call_tool(name, arguments)`.
4. Configure ABAC permission rules in `agent_forge/mcp/policy_engine.py`:
   - Identify whether the tool is read-only (`PERMITTED`), requires human approval (`REQUIRES_APPROVAL`), or requires high privilege (`DENIED` by default).
5. Add test coverage in `tests/test_all.py`.

### 2. Extending the Durable Orchestrator
1. Open `agent_forge/runtime/orchestrator.py`.
2. When creating new agent execution phases, record an `AgentEvent` in `self.event_store.append(...)`.
3. Support argument repair via `_validate_and_repair_tool_arguments`.
4. Enforce idempotency by passing `_idempotency_key` to all mutation tools.

### 3. Running Verification
Always verify changes using both test suites:
```bash
# AgentForge unit tests
python -m unittest agent-forge/tests/test_all.py

# Full curriculum lab checks
python scripts/verify_lab.py --all
```
