---
name: lab-verifier-and-eval
description: >-
  Automated evaluation, grading, and test runner skill for Labs 01 through 07.
  Use when the user asks to verify their code for a lab, run tests, assess
  groundedness, or check compliance with architectural acceptance criteria.
---

# 🧪 Lab Verifier & Evaluation Skill

Use this skill to automatically grade, test, and provide diagnostic feedback on learner implementations for Labs 01 through 07.

## 🚀 Execution Commands

Execute the evaluation harness directly:
```bash
# Verify all labs
python scripts/verify_lab.py --all

# Verify a single lab
python scripts/verify_lab.py --lab 1  # Multi-Tenant Hybrid RAG
python scripts/verify_lab.py --lab 2  # Tool Execution with MCP
python scripts/verify_lab.py --lab 3  # Stateful Agent Orchestration (WAL)
python scripts/verify_lab.py --lab 4  # Agent Failure Defense & Rate Limiting
python scripts/verify_lab.py --lab 5  # AI Observability & Tracing (OTel)
python scripts/verify_lab.py --lab 6  # Dual-LLM Quarantine & Guardrails
python scripts/verify_lab.py --lab 7  # Hybrid ML Fairness & Explainability
```

## 📋 Rubric & Acceptance Criteria

| Lab | Focus | Acceptance Requirement |
|:---|:---|:---|
| **Lab 01** | Multi-Tenant Hybrid RAG | Sparse BM25 + Dense vector search with Reciprocal Rank Fusion (RRF `k=60`). Queries for Tenant A must never return Tenant B documents. |
| **Lab 02** | Tool Execution with MCP | MCP server exposes typed tools via JSON-RPC. PolicyEngine permits safe queries, triggers approval for high-risk actions, and denies dangerous commands. |
| **Lab 03** | Stateful Agent Orchestration | Agent events are appended to `EventStore` WAL. Crash recovery can reconstruct full session state from recorded log events. |
| **Lab 04** | Agent Failure Defense | Streaming `TokenBucketLimiter` manages upfront token reservation and post-stream settlement. Throttles requests exceeding TPM/RPM. |
| **Lab 05** | AI Observability & Tracing | `GenAITracer` records spans conforming to OpenTelemetry GenAI semantic conventions, capturing duration and model metadata. |
| **Lab 06** | Dual-LLM Quarantine | Untrusted external inputs are isolated in an unprivileged execution perimeter, denying direct access to admin operations. |
| **Lab 07** | ML Fairness & Explainability | Disparate Impact Ratio calculated within 0.80–1.25 range; SHAP/Feature importance explanations generated. |
