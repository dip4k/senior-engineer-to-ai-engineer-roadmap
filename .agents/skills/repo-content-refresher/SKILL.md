---
name: repo-content-refresher
description: >-
  Autonomous content scout and updater. Use when the user asks to refresh,
  enhance, or audit repository content by using web search tools to compare new
  industry AI engineering breakthroughs against what is currently covered.
---

# 📡 Repository Content Refresher & Frontier Scout Skill

Use this skill to autonomously discover, benchmark, and integrate frontier AI engineering developments into this repository.

## 🎯 Goal
Maintain this repository as the premier, authoritative resource for modern production AI engineering (2025–2026/2027+) by identifying new foundation models, protocol revisions, agent patterns, and enterprise standards not yet fully represented.

---

## 🔄 Automated Workflow

### Step 1: Run the Repository Scout
Execute the automated keyword and topic gap analyzer:
```bash
python scripts/refresh_content_scout.py --summary
```
This inspects all modules (`00` to `08`), `agent-forge/`, `labs/`, `use-cases/`, and the glossary to produce a baseline coverage report in `CONTENT_REFRESH_REPORT.md`.

### Step 2: Formulate Frontier Web Search Queries
Run:
```bash
python scripts/refresh_content_scout.py --queries-only
```
Review the suggested search queries targeting:
1. **New Foundation Models & Reasoning**: Anthropic Claude 3.7 / 4 Sonnet/Opus thinking tokens, OpenAI o3/o4-mini, DeepSeek-R1, Google Gemini 2.5 / 3 Flash/Pro.
2. **Protocol Standards**: Model Context Protocol (MCP) spec revisions, Agent-to-Agent (A2A) protocol, AG-UI streaming protocol.
3. **Context Engineering**: Active context AST compilation, prompt caching economics, hierarchical memory-as-a-service.
4. **Agent Orchestration**: Write-Ahead Log durability, deterministic FSMs, action fingerprinting.
5. **Security & Governance**: EU AI Act enforcement deadlines, OWASP LLM Top 10 revisions, dual-LLM quarantine patterns.

### Step 3: Execute Web Searches Using Agent Tools
Use your agent's web search capability (`search_web` or browser) to query the top 3–5 queries with highest missing scores.
Example:
- Query: `Anthropic Claude 3.7 thinking tokens reasoning mechanics`
- Query: `Model Context Protocol MCP specification updates 2025 2026`
- Query: `EU AI Act General Purpose AI GPAI enforcement guidelines 2026`

### Step 4: Compare & Identify Knowledge Gaps
Compare the web findings against current repository contents:
- **Is this concept completely missing?** (e.g. A newly announced wire transport for MCP, or a new reasoning token API).
- **Is an existing section outdated?** (e.g. Model pricing changed, context window limits increased, deprecated SDK methods).
- **Does it require code changes in `agent-forge/`?** (e.g. Adding support for a new MCP tool format).

### Step 5: Draft Enhancements & Updates
1. **Glossary Update**: Add the new term and 1–2 sentence explanation into [ai-engineering-glossary-by-practice.md](../../../ai-engineering-glossary-by-practice.md).
2. **Module Deep-Dive**: Update the relevant phase README (`00` to `08`) with architectural trade-offs, Mermaid diagrams, and code snippets.
3. **Roadmap Sync**: Keep [ai-technology-roadmap-2025-2026.md](../../../ai-technology-roadmap-2025-2026.md) aligned.
4. **Verification**: Run `python scripts/verify_lab.py --all` to ensure no existing tests are broken.
