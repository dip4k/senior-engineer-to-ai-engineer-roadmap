# Phase 08 Examples: AI-Augmented SDLC & Leadership

Production templates, machine-readable agent directives, CI/CD review workflows, and architecture governance specifications for AI-native software engineering.

## Files

| File | Type | Purpose | Key Invariants |
|---|---|---|---|
| [`AGENT.md`](./AGENT.md) | Markdown Specification | Repository Context & Rules Contract | Linux Foundation `AGENTS.md` compliant, hexagonal boundaries, build/test commands, deterministic typing, approved tooling allowlist |
| [`ADR-042-kafka-event-ingestion.md`](./ADR-042-kafka-event-ingestion.md) | Architectural Decision Record | Enterprise Architecture Governance | Context, decision drivers, considered options, rationale, and compliance verification |
| [`pr_review_workflow.yml`](./pr_review_workflow.yml) | GitHub Actions CI/CD | Dual-Stage Pull Request Reviewer | Deterministic invariant gate via `ai_pr_reviewer.py` + headless Claude Code review via `anthropics/claude-code-action@v1` |
| [`ai_pr_reviewer.py`](./ai_pr_reviewer.py) | Python CLI Tool (Pydantic v2) | Headless PR Invariant Gate Bot | Evaluates unified git diffs for hardcoded secrets, SQL injection, hexagonal layer breaches, and banned dependencies |
| [`generate_adr.py`](./generate_adr.py) | Python CLI Tool (Pydantic v2) | Semantic Commit & ADR Generator | Staged diff extraction, LLM synthesis with deterministic offline fallback, Michael Nygard markdown ADR rendering |

## Quick Verification Commands

Run the Python verification tools directly offline:

```bash
# 1. Run the headless PR reviewer against sample diff (catches 4 critical blockers)
python 08-ai-augmented-sdlc-and-leadership/examples/ai_pr_reviewer.py

# 2. Run the PR reviewer in machine-readable JSON mode
python 08-ai-augmented-sdlc-and-leadership/examples/ai_pr_reviewer.py --json

# 3. Generate a compliant Michael Nygard ADR from staged git diff
python 08-ai-augmented-sdlc-and-leadership/examples/generate_adr.py
```
