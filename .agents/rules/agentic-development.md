---
trigger: model_decision
description: "Guidelines for implementing autonomous agents, Write-Ahead Logs, MCP servers, and multi-agent coordination."
---

# Agentic Development Guidelines

1. **State Persistence & Replay (WAL)**:
   - When building or extending agents in `agent-forge/runtime/`, never rely exclusively on in-memory variables.
   - Append every state event (`session_started`, `model_decision`, `tool_completed`, `checkpoint_saved`) to `EventStore`.
   - Ensure the orchestrator can rehydrate and resume mid-workflow after unexpected process terminations.

2. **Model Context Protocol (MCP)**:
   - Every MCP server must adhere to JSON-RPC 2.0 standards.
   - Implement `list_tools()` returning formal schemas with input constraints.
   - Connect all tool executions through `PolicyEngine.evaluate()` before firing side effects.

3. **Tool Argument Repair**:
   - High-performance agents should gracefully repair common LLM argument deviations (e.g. converting `"$49.00"` to `49.00`) while logging a warning event to the trace.

4. **Multi-Tenant RAG & Search**:
   - Enforce pre-filtering by tenant ID (`filter_metadata={"tenant_id": tenant_id}`) in vector search and BM25 search.
   - Always merge lexical and dense rankings using Reciprocal Rank Fusion (RRF with `k=60`).
