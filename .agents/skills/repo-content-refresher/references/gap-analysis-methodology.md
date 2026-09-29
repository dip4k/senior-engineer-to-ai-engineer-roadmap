# Frontier Gap Analysis Methodology

This document outlines the rigorous methodology used by the `@refresher` agent to benchmark this repository against frontier industry standards.

## 🎯 8 Architectural Radar Dimensions

1. **Reasoning Models & Inference Scaling**:
   - Tracking reasoning tokens, hidden chain-of-thought, test-time compute scaling (MCTS vs. RLVR), speculative decoding, and native reasoning API signatures.
2. **Context Engineering & Memory Architecture**:
   - Tracking prompt caching SLAs (5-minute TTLs, min prefixes), Context AST compilers, semantic caching ratios, and hierarchical memory stores (Episodic, Working, Long-Term).
3. **Wire Protocols & Tool Ecosystem**:
   - Tracking MCP (tools, resources, prompts, completions, roots), transport shifts (SSE vs. WebSocket vs. Stdio), A2A inter-agent discovery, and AG-UI streaming primitives.
4. **Agent Orchestration & Deterministic Control**:
   - Tracking event-sourced durability (WAL), state checkpoints, progressive budget decay, action loop detection, and human-in-the-loop escalation patterns.
5. **Zero-Trust Security & Quarantine**:
   - Tracking dual-LLM quarantine pipelines, indirect prompt injection defense, ABAC permission engines, taint tracking, and crypto-shredding for compliance.
6. **Evals & GenAI Observability**:
   - Tracking OpenTelemetry GenAI semantic conventions, LLM-as-a-judge calibrators, trajectory step scoring, and automated CI/CD gating.
7. **Production Serving & LLMOps**:
   - Tracking vLLM, SGLang, PagedAttention, TensorRT-LLM, model gateway rate limiting (token-bucket reservation and settlement), and multi-cloud routing.
8. **Enterprise Governance & Regulatory**:
   - Tracking EU AI Act GPAI compliance deadlines, ISO 42001, NIST AI RMF, and audit logging.

## 📋 Evaluation Criteria for Inclusions
Before adding any emerging trend to the repository:
1. **Production Relevance**: Is this used in enterprise production, or is it an ephemeral Twitter hype demo? Only battle-tested or standardizing paradigms are admitted.
2. **Deterministic Architecture**: Does it fit the Software 3.0 philosophy (deterministic harness around probabilistic models)?
3. **Actionable Implementation**: Can it be demonstrated with runnable Python/.NET code or formal architecture diagrams?
