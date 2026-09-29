# Claude Code Development Guide — Ai_Native_Engineer

Welcome to the **AI-Native Engineer** repository! This project serves as an architectural masterclass and production codebase (`agent-forge`) for building enterprise-grade, deterministic agentic systems (Software 3.0).

---

## ⚡ Quick Start Commands

```bash
# 🧪 Run full AgentForge unit & integration test suite
python -m unittest agent-forge/tests/test_all.py

# 🧪 Run Lab Verification Harness (Labs 01-07)
python scripts/verify_lab.py --all
python scripts/verify_lab.py --lab 1   # Verify specific lab (1-7)

# 📡 Run Frontier Content Scout & Gap Analysis
python scripts/refresh_content_scout.py --summary

# 🔎 Generate Web Search Query List for Content Refresh
python scripts/refresh_content_scout.py --queries-only
```

---

## 🏛️ Codebase Layout

- **`agent-forge/`**: Core production agent framework:
  - `retrieval/`: BM25 sparse + dense vector store with Reciprocal Rank Fusion (`HybridRetriever`) and ACORN-1 graph traversal.
  - `runtime/`: Durable agent orchestrator (`DurableOrchestrator`), event-store WAL (`EventStore`), and state models.
  - `mcp/`: Model Context Protocol servers (`PaymentMCPServer`, `OrderServer`, `PolicyServer`) and ABAC `PolicyEngine`.
  - `gateway/`: Streaming token bucket rate limiter (`TokenBucketLimiter`), model router, and semantic cache.
  - `observability/`: OpenTelemetry GenAI semantic conventions distributed tracer (`GenAITracer`).
  - `evals/`: Binary evaluators (groundedness, faithfulness) and trajectory step scoring.
- **`labs/`**: Labs 01 through 07 covering multi-tenant RAG, MCP tool execution, WAL orchestration, failure defenses, OTel tracing, dual-LLM quarantine, and ML fairness.
- **`00-` to `08-`**: 9-phase master curriculum modules with comprehensive READMEs, code examples, and architecture guides.
- **`interview/`**: Senior AI Platform Engineer interview guides and scenario questions.
- **`scripts/`**: Automated verification and content freshness scouts.

---

## 🧭 Slash Commands for Claude Code

You can use the following custom commands in `.claude/commands/`:
- `/coach`: Launches the general model-driven AI Engineering practice session (roadmaps, live web search, dynamic katas without repo labs).
- `/practice`: Starts an interactive guided practice session on a specific repo module or lab.
- `/verify-lab`: Runs automated evaluation checks on your lab solution against acceptance criteria.
- `/refresh-content`: Runs the content scout, searches the web for frontier advancements, and outputs gap analysis.
- `/quiz`: Quizzes you on high-stakes AI architecture trade-offs from the interview prep sheets.
- `/architect`: Guides you through designing a new agentic system or MCP tool in `agent-forge`.

---

## 🛡️ Coding & Architectural Standards

1. **Python Standards**: Python 3.12+ features, strict typing, and Pydantic v2 `BaseModel` models.
2. **Determinism**: Never build unrestricted open loops. Every agent loop must have bounded turn counts, progressive token budget decay, and action fingerprinting.
3. **Write-Ahead Logging (WAL)**: Every agent decision, tool call, and observation must be persisted to the `EventStore` before committing external side-effects.
4. **Zero-Trust Tooling**: All MCP tools must validate schemas and reject hazardous queries (`DROP`, `DELETE`, `UPDATE`) through the `PolicyEngine`.
5. **Web Search & Discovery**: Use web search tools to inspect real-time changes in protocols (MCP, A2A, AG-UI) and frontier model capabilities (Claude 3.7 Sonnet, Gemini 2.5/3, o3/o4-mini, DeepSeek-R1).
