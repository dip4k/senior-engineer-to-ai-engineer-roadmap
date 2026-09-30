# Antigravity & Google Agents CLI Workspace Configuration (GEMINI.md)

Welcome to the **AI-Native Engineer** repository! This workspace is configured for autonomous agentic software engineering with Antigravity.

---

## 🚀 Active Customizations & Skills

Antigravity automatically discovers skills and rules located in `.agents/`:

### Discovered Skills (`.agents/skills/`):
- **`ai-curriculum-refactoring`**: Methodology, templates, quality gates, and controlled web research protocols for refactoring curriculum modules.
- **`ai-practice-coach`**: General model-driven practice coach for an AI Engineering Roadmap using live web search without relying on repo labs or files.
- **`ai-engineering-tutor`**: Socratic teaching, walkthroughs, quizzes, and code katas for repo modules 00 through 08.
- **`agent-forge-builder`**: Scaffolding, extending, and testing the `agent-forge` production framework.
- **`repo-content-refresher`**: Frontier scout using `search_web` to detect new AI developments and audit repository coverage.
- **`lab-verifier-and-eval`**: Automated evaluation and grading harness for Labs 01–07.
- **`mcp-tool-architect`**: Model Context Protocol (MCP) server & client construction with JSON-RPC schemas.

### Custom Workspace Agents (`.agents/agents/`):
- **`ai-curriculum-architect`**: Workspace agent running in `AUDIT`, `PLAN`, `REFACTOR`, `VALIDATE`, `RESEARCH`, or `INTEGRATION` modes to engineer senior developer curriculum.


---

## 🏛️ Codebase & Curriculum Layout

- **`AI_ENGINEER_ROADMAP.md`**: Full conceptual AI Engineer Roadmap covering core categories and topics in plain English.
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

## ⚡ Execution Commands

Antigravity agents can run these verified scripts via `run_command`:
```bash
# Verify all lab implementations (Labs 01-07)
python scripts/verify_lab.py --all
python scripts/verify_lab.py --lab 1   # Verify specific lab (1-7)

# Run AgentForge platform test suite
python -m unittest agent-forge/tests/test_all.py

# Run Content Scout Gap Analysis
python scripts/refresh_content_scout.py --summary
```

---

## 📋 Core Architectural Rules

1. **Always-On Quality**:
   - Enforce Pydantic v2 schemas across all data ingestion and state transitions.
   - Guard against hallucinations by verifying that retrieval scores exceed threshold barriers before feeding context to reasoning models.
2. **Deterministic Agent Harness**:
   - Every agent loop must be bounded by a maximum turn counter and progressive token budget decay.
   - Use the `EventStore` WAL to record transitions before external mutations.
3. **Zero-Trust Tooling**:
   - All MCP tools must validate schemas and reject hazardous queries (`DROP`, `DELETE`, `UPDATE`) through the `PolicyEngine`.
4. **Web Search & Knowledge Verification**:
   - When asked about new models, protocol specifications, or benchmarks, use `search_web` to ground findings with authoritative sources (Anthropic, Linux Foundation, Google, OpenAI, OpenTelemetry).
5. **Pure Markdown & Zero-LaTeX**:
   - Never generate LaTeX math delimiters (`$$...$$`, `$...$`, `\frac{...}{...}`). Format formulas using clean text code blocks or Unicode symbols (`→`, `⟷`, `Σ`, `≥`, `≤`).
   - Never leak internal meta-directive tags (`[MUST-HAVE]`, `[GOOD-TO-KNOW]`, `(Refactored)`) into learner-facing prose or headings.
