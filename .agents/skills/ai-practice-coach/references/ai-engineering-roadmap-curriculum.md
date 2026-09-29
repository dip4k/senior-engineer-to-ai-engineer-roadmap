# Modern AI Engineering Roadmap & Practice Syllabus

This reference outlines the universal roadmap modules and hands-on katas generated dynamically by the `@coach` agent.

---

## 1. LLM Silicon, Compute & Token Mechanics
- **Key Concepts**: Autoregressive decoding, KV-cache VRAM allocation (`2 × 2 × n_layers × d_model × tokens`), Memory-bandwidth-bound vs. Compute-bound operations, Time to First Token (TTFT) vs. Tokens Per Second (TPS), Reasoning tokens (hidden thinking phase, test-time compute scaling).
- **Hands-On Katas**:
  - Implement a KV-cache memory calculator given GPU VRAM, batch size, context window, and model parameters.
  - Write a token streaming simulator with latency profiling (TTFT and inter-token latency percentiles: p50, p95, p99).
  - Web Search Query: `KV cache memory formula LLM inference serving VRAM calculation`

---

## 2. Context Engineering & Memory Architecture
- **Key Concepts**: Context Abstract Syntax Tree (AST), 4-tier compaction (pruning, summarization, semantic extraction, drop), Prompt Caching mechanics (exact prefix matching, 5-minute TTL, minimum cacheable block size), Hierarchical Agent Memory (Working, Short-Term, Long-Term, Memory-as-a-Service).
- **Hands-On Katas**:
  - Build an in-memory Context Compactor that prunes message history to fit a 16,000-token budget while preserving system instructions and the most recent 3 turns.
  - Implement a Prompt Caching optimizer that structures system prompts and static tool schemas at the head of the payload to maximize cache hits.
  - Web Search Query: `Anthropic prompt caching best practices prefix alignment`

---

## 3. Advanced Retrieval & Knowledge Systems (RAG)
- **Key Concepts**: Dense embeddings vs. Sparse BM25, Reciprocal Rank Fusion (RRF with parameter \(k=60\)), Late Chunking (context-aware chunk embeddings), Cross-encoder rerankers, Multi-tenant metadata pre-filtering, GraphRAG & ACORN-1 graph traversal.
- **Hands-On Katas**:
  - Implement Reciprocal Rank Fusion (RRF) from scratch to merge lexical and vector search ranks without third-party libraries.
  - Build a multi-tenant pre-filtering layer that strictly isolates tenant documents before distance calculations.
  - Web Search Query: `Reciprocal Rank Fusion RRF python implementation formula k=60`

---

## 4. Tool Execution & Model Context Protocol (MCP)
- **Key Concepts**: JSON-RPC 2.0 wire protocol, MCP servers and clients, formal JSON Schema validation, tool argument repair, sandboxed execution perimeters, idempotency keys for mutations.
- **Hands-On Katas**:
  - Implement a standalone JSON-RPC 2.0 tool dispatcher that accepts `tools/call` requests and returns standard success and error structures (`code: -32602`, `message: Invalid params`).
  - Build an argument repair wrapper that auto-converts string numbers and formats into strict types before invocation.
  - Web Search Query: `Model Context Protocol JSON-RPC specification Anthropic tools call schema`

---

## 5. Autonomous Agents & Multi-Agent Orchestration
- **Key Concepts**: ReAct loop (Thought-Action-Observation), Finite State Machine (FSM) schemas, Write-Ahead Log (WAL) event streaming, crash replay, progressive budget decay, action loop fingerprinting, supervisor-worker choreography, Agent-to-Agent (A2A) protocol.
- **Hands-On Katas**:
  - Build a resilient agent loop bounded by `max_turns=5` and a token budget, with loop detection that aborts if the exact same tool and arguments are called consecutively.
  - Implement an append-only Event Store WAL that records every state transition and rehydrates the agent state upon process restart.
  - Web Search Query: `LangGraph state persistence checkpointing write ahead log crash recovery`

---

## 6. Security, Red Teaming & Guardrails
- **Key Concepts**: Indirect Prompt Injection, Jailbreak taxonomies, Dual-LLM quarantine architecture, Privilege minimization, Input taint tracking, Output firewalls, PII redaction, Crypto-shredding.
- **Hands-On Katas**:
  - Implement a dual-LLM quarantine validator: an untrusted retrieval processor that strips markdown directives before context is passed to the privileged reasoning model.
  - Write an output firewall that scans generated text for synthetic PII and API keys using regex and policy rules.
  - Web Search Query: `Dual-LLM quarantine architecture indirect prompt injection defense Simon Willison`

---

## 7. Evals, Observability & GenAI Telemetry
- **Key Concepts**: LLM-as-a-judge (Groundedness, Faithfulness, Context Recall, Answer Relevance), Binary scoring vs. Likert scales, OpenTelemetry GenAI Semantic Conventions (`gen_ai.request.model`, `gen_ai.usage.prompt_tokens`), Trajectory step-level grading, Continuous CI/CD eval gates.
- **Hands-On Katas**:
  - Build a binary Groundedness evaluator that takes a context chunk and generated answer and returns `{grounded: bool, reasoning: str}`.
  - Implement an OpenTelemetry-compatible tracing span wrapper for LLM requests measuring latency and token consumption.
  - Web Search Query: `OpenTelemetry GenAI semantic conventions tracing attributes span`

---

## 8. High-Throughput Serving & LLMOps
- **Key Concepts**: PagedAttention, Continuous batching, vLLM / SGLang architecture, Speculative decoding (Draft model + Target model verification), Semantic caching (vector similarity thresholding), Streaming token-bucket rate limiters (reservation and settlement).
- **Hands-On Katas**:
  - Build a Token-Bucket Rate Limiter with upfront reservation for estimated completion tokens and post-stream settlement.
  - Implement an in-memory Semantic Cache that hashes query embeddings and returns cached answers for cosine similarity \(> 0.95\).
  - Web Search Query: `vLLM paged attention continuous batching architecture paper`
