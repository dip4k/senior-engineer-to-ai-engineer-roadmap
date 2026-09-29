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

## ⚡ Execution Commands

Antigravity agents can run these verified scripts via `run_command`:
```bash
# Verify all lab implementations
python scripts/verify_lab.py --all

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
   - Every agent loop must be bounded by a maximum turn counter and budget decay.
   - Use the `EventStore` WAL to record transitions before external mutations.
3. **Web Search & Knowledge Verification**:
   - When asked about new models, protocol specifications, or benchmarks, use `search_web` to ground findings with authoritative sources (Anthropic, Linux Foundation, Google, OpenAI, OpenTelemetry).
