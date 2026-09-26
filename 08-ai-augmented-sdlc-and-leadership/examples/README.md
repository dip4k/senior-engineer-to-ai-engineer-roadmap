# Phase 08 Examples: AI-Augmented SDLC & Leadership

Production templates, machine-readable agent directives, CI/CD review workflows, and architecture governance specifications for AI-native software engineering.

## Files

| File | Type | Purpose | Key Invariants |
|---|---|---|---|
| [`AGENT.md`](./AGENT.md) | Markdown Specification | Repository Context & Rules Contract | Hexagonal architecture boundaries, build/test commands, deterministic typing, approved tooling allowlist |
| [`ADR-042-kafka-event-ingestion.md`](./ADR-042-kafka-event-ingestion.md) | Architectural Decision Record | Enterprise Architecture Governance | Context, decision drivers, considered options, rationale, and compliance verification |
| [`pr_review_workflow.yml`](./pr_review_workflow.yml) | GitHub Actions CI/CD | Multi-Agent Pull Request Reviewer | Automated diff extraction, parallel security/architecture checks, inline PR feedback |
| [`generate_adr.py`](./generate_adr.py) | Python CLI Tool | Semantic Commit & ADR Generator | Staged diff extraction, LLM synthesis, Michael Nygard markdown ADR formatting |
