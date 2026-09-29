# Technical Terminology & Editorial Guidelines

This document establishes the editorial rules for handling technical jargon, acronyms, and terminology across the curriculum.

---

## 1. The First-Mention Rule

Never use an abbreviation or acronym without expanding it and providing a one-sentence conceptual anchor on its first appearance in a lesson.

### ✅ Good Multi-Phase Examples:
- **Phase 00**: "In this lesson, we analyze the **Key-Value Cache (KV Cache)**—a GPU memory allocation strategy that caches attention tensors to avoid recomputing previous tokens during autoregressive decoding."
- **Phase 02**: "In this lesson, we implement **Retrieval-Augmented Generation (RAG)**—a pattern where an external search index retrieves relevant domain documents to ground a language model's response before generation."
- **Phase 03**: "We communicate with tools via the **Model Context Protocol (MCP)**—an open JSON-RPC 2.0 wire protocol that standardizes how language models discover and invoke external functions."
- **Phase 04**: "To guarantee crash recovery, the orchestrator writes every state transition to a **Write-Ahead Log (WAL)**—an append-only event store that allows replaying transactions after failure."
- **Phase 06**: "We collect distributed spans using **OpenTelemetry (OTel)**—a vendor-neutral telemetry framework providing standardized GenAI semantic conventions."

### ❌ Bad Examples:
> "We will build an enterprise RAG pipeline using HNSW and RRF."  
> "Initialize the WAL before the FSM invokes the MCP server."

---

## 2. Acronym Collision & Cognitive Overload

Avoid introducing more than two new technical acronyms in a single paragraph.

### ❌ Overloaded Jargon Dump:
> "By combining **CRAG** with **HyDE** and routing queries via an **FSM** into an **HNSW** index with **RRF**, we optimize **NDCG@10** before evaluating with **RAGAS**."

### ✅ Decoupled Engineering Explanation:
> "To improve retrieval precision, we execute query expansion to generate candidate answers before searching. The retrieved documents are then scored across both lexical and vector indexes, merged using **Reciprocal Rank Fusion (RRF)**, and verified for factual consistency before synthesis."

---

## 3. Concept Before Abbreviation & Tool

Always explain **what the system does** before giving it a formal name or naming a library:

### Example A: Vector Search (Phase 02)
1. **Physical Reality**: We need to find similar vectors among 10 million embeddings without calculating dot products against every single vector (O(N) is too slow).
2. **Algorithmic Solution**: Build a multi-layer graph where top layers have long-distance skips and bottom layers have dense local connections (O(log N) traversal).
3. **Formal Name**: This data structure is called **Hierarchical Navigable Small World (HNSW)**.
4. **Tooling Reference**: Implemented natively in engines like Qdrant, Milvus, pgvector, and Faiss.

### Example B: Memory Paging (Phase 07)
1. **Physical Reality**: Allocating static contiguous GPU VRAM for the maximum possible sequence length wastes up to 60-80% of memory due to fragmentation.
2. **Algorithmic Solution**: Partition key-value tensors into fixed-size virtual blocks that map to non-contiguous physical GPU memory via a page table.
3. **Formal Name**: This architecture is called **PagedAttention**.
4. **Tooling Reference**: Implemented natively in high-throughput inference engines like vLLM.

---

## 4. Banned Buzzwords & AI Alchemy Phrases

Remove generic marketing language that conveys zero engineering meaning:

| Banned Phrase | Technical Alternative |
|---|---|
| *"Supercharge your LLM"* | *"Reduce hallucination rates by providing external context"* |
| *"Unleash autonomous AI power"* | *"Implement bounded multi-step tool execution loops"* |
| *"Seamless integration"* | *"Standardized wire protocol via JSON-RPC / MCP"* |
| *"Blazing fast"* | *"Sub-25ms p99 retrieval latency"* |
| *"State-of-the-art magic"* | *"Benchmarked at 0.89 Recall@10 on MTEB"* |

---

## 5. Glossary Synchronization

When defining or refining critical terms, maintain alignment with the repository's master reference:
[ai-engineering-glossary-by-practice.md](file:///c:/Repos/Ai_Native_Engineer/ai-engineering-glossary-by-practice.md).
