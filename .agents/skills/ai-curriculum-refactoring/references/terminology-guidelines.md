# Technical Terminology & Editorial Guidelines

This document establishes the editorial rules for handling technical jargon, acronyms, and terminology across the curriculum.

---

## 0. The Learner Baseline: Software Terms Known, AI Terms Unknown

- **Software engineering terms** (cache, index, RPC, idempotency, tracing) are assumed known. Use them freely as bridges.
- **AI engineering terms** (token, embedding, context window, attention, KV cache, RAG, agent, eval, hallucination, quantization) are assumed unknown. Teach each one from zero, in this order: plain-English definition, analogy, tiny example, formal name, then math or code.
- **Term Ledger**: each lesson header lists `New AI terms introduced` and `AI terms assumed from earlier lessons` (with links). Using an AI term that is in neither list is a defect.
- **Bridge, don't substitute**: "a KV cache is like a memoization table in GPU memory" is a bridge. Follow it with what is actually cached and why. Never let the bridge be the whole explanation.

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
1. **Physical Reality**: Allocating static contiguous GPU VRAM for the maximum possible sequence length can waste a large share of memory to fragmentation (quantify with a cited source or label it *(illustrative)*).
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
[ai-engineering-glossary-by-practice.md](../../../../ai-engineering-glossary-by-practice.md).

---

## 6. Lesson Titles & Main Headings (No Isolated Acronyms)

Lesson titles and top-level headings must **never use unexpanded, isolated abbreviations or acronyms**.

### ❌ Bad Headings & Titles:
- `# Hybrid Search: BM25, HNSW & Vector Memory Physics`
- `# Implementing MCP with SSE`
- `# ACORN and RRF in RAG`

### ✅ Good Headings & Titles:
- `# Hybrid Search: Lexical Keyword Matching (BM25), Vector Proximity Graphs (HNSW) & Memory Physics`
- `# Tools & Protocols: Model Context Protocol (MCP) JSON-RPC Architecture`
- `# Predicate Filtering: Multi-Tenant Security & ACORN Graph Navigation`

### The Rule:
1. **Lead with Plain Language**: Start with descriptive, standard software engineering concepts (e.g. "Lexical Keyword Matching", "Vector Proximity Graphs", "Multi-Tenant Security").
2. **Include Acronym in Parentheses**: Place the industry-standard acronym in parentheses after the descriptive phrase (e.g. `(BM25)`, `(HNSW)`, `(MCP)`).
3. **Anchor in Core Concept Subtitle**: Immediately below the title, provide a 1–2 sentence `Core Concept` callout explaining what the mechanism does in plain systems terms before introducing formulas or code.

---

## 7. The Plain-English "Coffee Test" & Ban on Academic Jargon Stacking

Real engineering depth comes from architectural trade-offs, memory bottlenecks, failure modes, and runnable code—**never from dense academic vocabulary**.

```xml
<prose_mechanics>
  <rule id="one_concept_per_sentence">Max 1 new AI concept per sentence. Never stack unfamiliar terms.</rule>
  <rule id="sentence_length_ceiling">Hard ceiling: 28 words per sentence. Target average: 12-18 words.</rule>
  <rule id="action_verbs">Use plain Anglo-Saxon verbs (build, run, guess, drop, check, save) over Latinate abstractions (instantiate, execute, hypothesize, evict, verify, persist).</rule>
  <rule id="active_voice">Target 80%+ active voice: Subject -> Verb -> Object ("The engine drops the cache", NOT "The cache is evicted by the engine").</rule>
  <rule id="ban_jargon_stacking">Never stack 2+ abstract AI adjectives before a noun.</rule>
</prose_mechanics>
```

### 7.1 Ban on Academic Jargon Stacking
Never stack two or more abstract, academic AI adjectives or theoretical phrases in a single clause.
- ❌ **Academic Stack**: *"A Context AST compiles down to token arrays fed to a probabilistic autoregressive model."*
- ✅ **Plain Software English**: *"A Context AST prepares text for an AI that predicts the next words based on odds, rather than running deterministic code."*

### 7.2 The "Coffee Test" (Peer-to-Peer Whiteboard Tone)
Write like a Senior Principal Engineer explaining a system to a smart backend or systems colleague over coffee or at a whiteboard.
- If you would feel pretentious saying the sentence out loud to a colleague, rewrite it.
- Prefer active verbs over passive academic nouns (*"the AI predicts the next word based on odds"* rather than *"probabilistic autoregressive sequence generation"*).

### 7.3 Canonical Jargon Translation Table
Always substitute academic ML textbook phrasing and inflated Latinate vocabulary with plain software engineering equivalents:

| Academic / Inflated Jargon | Plain-English Software Translation |
|---|---|
| *"Probabilistic autoregressive model"* | *"An AI that predicts the next words based on odds, rather than running deterministic code"* |
| *"Autoregressive next-token prediction"* | *"Predicting the next word one by one based on probabilities"* |
| *"Stochastic decoding trajectory"* | *"Random variations in what the model outputs"* |
| *"High-dimensional semantic vector embedding"* | *"A list of numbers that captures what the text means"* |
| *"Prefix KV cache eviction under VRAM pressure"* | *"Discarding saved prompt calculations when GPU memory runs out"* |
| *"Parametric vs. non-parametric knowledge"* | *"What the model learned during training vs. the fresh documents you feed it"* |
| *"In-context demonstration trajectory conditioning"* | *"Guiding model behavior with concrete input-output examples"* |
| *"Token arrays fed to the attention mechanism"* | *"The list of tokens passed to the AI"* |
| *"Deterministic adjudication"* | *"Standard code / if-statements"* |
| *"Heterogeneous multi-agent topology"* | *"Multiple specialized agents working together"* |
| *"Utilize"* / *"Utilization"* | *"Use"* |
| *"Commence"* / *"Initiate"* | *"Start"* |
| *"Ascertain"* / *"Elucidate"* | *"Check"* / *"Explain"* |
| *"Necessitate"* | *"Require"* / *"Need"* |
| *"Manifestation"* / *"Instantiation"* | *"Example"* / *"Instance"* |
| *"Subsumed under"* | *"Part of"* / *"Included in"* |
| *"Topological space"* (in RAG) | *"The map of where concepts sit relative to each other"* |



