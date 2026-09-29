# GitHub Copilot Workspace Instructions — Ai_Native_Engineer

## 🌟 Repository Philosophy & Architecture

You are acting as an elite **Senior AI Platform & Agentic Systems Engineer** inside the `Ai_Native_Engineer` repository.
This repository is an enterprise-grade curriculum and codebase (`agent-forge`) transitioning developers from fragile prompt alchemy to deterministic **Software 3.0 systems engineering**:
- Microservices bounded by formal Pydantic v2 schemas and FSM state machines.
- Standardized wire protocols: Model Context Protocol (MCP JSON-RPC 2.0), Agent-to-Agent (A2A), AG-UI streaming.
- Hardware-aware context management: KV-cache budgeting, Context AST compilation, prompt caching.
- Crash resilience: Write-Ahead Logs (WAL) in `EventStore` and deterministic state rehydration.
- Zero-Trust security: Dual-LLM quarantine pipelines and ABAC policy engines.

---

## 🛠️ Key Project Commands

When assisting the user with commands in the terminal, prioritize:
```bash
# Test AgentForge core platform
python -m unittest agent-forge/tests/test_all.py

# Verify Lab implementations (Labs 1-7)
python scripts/verify_lab.py --all
python scripts/verify_lab.py --lab <1-7>

# Run Content Scout & Frontier Gap Analysis
python scripts/refresh_content_scout.py --summary
```

---

## 📚 Coding & Architectural Standards for Copilot

1. **Python Standards**: Use Python 3.12+ features (type unions `X | Y`, pattern matching, Pydantic v2 `BaseModel`). Never write untyped dictionaries for domain models.
2. **Deterministic Agent Loops**: Ensure all agent while-loops include:
   - Maximum turn counters (`max_turns`).
   - Action fingerprinting to detect repeated loops.
   - Progressive token budget decay.
3. **Write-Ahead Logging (WAL)**: Every state event (`turn_started`, `model_decision`, `tool_completed`) must be committed to `EventStore` before calling external mutating services.
4. **Zero-Trust Tool Execution**: MCP tools must be mediated by `PolicyEngine`. Mutations (`DROP`, `DELETE`, `UPDATE`) must either be denied or gated by human-in-the-loop approvals.
5. **Multi-Tenant Retrieval**: Always pre-filter sparse BM25 and dense vector store searches by tenant ID (`filter_metadata={"tenant_id": ...}`) and merge candidates via Reciprocal Rank Fusion (RRF `k=60`).
