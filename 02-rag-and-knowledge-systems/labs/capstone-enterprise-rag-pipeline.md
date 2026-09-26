# Capstone Engineering Challenge: Enterprise RAG Pipeline

### Challenge Objective
Build a complete, standalone, production-grade **Enterprise Hybrid RAG Engine** with:
1. Multi-stage Hybrid Retrieval (BM25 + Dense Vectors fused via Reciprocal Rank Fusion).
2. Cross-Encoder Reranking with strict relevance thresholding.
3. Automated Citation Extraction and Hallucination Verification.

### Architectural Specifications & Acceptance Criteria

| Requirement | Production Standard |
|---|---|
| **1. Ingestion & Chunking** | Parse 10 multi-page enterprise policy documents (markdown / PDF). Apply recursive character chunking (target 500 chars, 50 overlap). |
| **2. Hybrid Retrieval (Solves Low Recall & Keyword Misses)** | Implement both BM25 and Dense Cosine Search. Combine Top-20 hits using Reciprocal Rank Fusion (k=60). |
| **3. Reranking & Pruning** | Rerank top 20 candidates using a Cross-Encoder (Cohere API or local SentenceTransformer `cross-encoder/ms-marco-MiniLM-L-6-v2`). Filter out any chunk with score < 0.70. |
| **4. Grounded Synthesis** | Assemble prompt with explicit XML tags `<context>`. Generate answer requiring format `[DocTitle:ChunkId]`. |
| **5. Automated Citation Verifier (Solves Hallucination)** | Deterministic post-processor checking:<br>1. Did the response include at least one valid citation?<br>2. Are cited chunk IDs present in the retrieved set?<br>3. Does the cited chunk contain the claimed entities/numbers?<br>If verification fails, reject output and trigger an explicit abstention statement: *"Insufficient verified evidence."* |

### Implementation Blueprint & Hands-On Steps:

1. **Step 1: Ingestion & Vector / Sparse Indexing:**
   - Index policy markdown files into an in-memory or embedded database (Qdrant, Chroma, or SQLite-vss + BM25Okapi).
   - Verify that chunks preserve parent metadata (`document_id`, `section_title`, `chunk_id`).

2. **Step 2: Hybrid Query Execution & RRF Merging:**
   - Execute parallel dense vector search (top 20) and sparse BM25 search (top 20).
   - Merge results using Reciprocal Rank Fusion formula: $RRF(d) = \sum \frac{1}{60 + \text{rank}(d)}$.

3. **Step 3: Cross-Encoder Reranking & Quality Cutoff:**
   - Score the top 20 fused candidates with a cross-encoder model.
   - Discard low-relevance candidates (< 0.70 threshold) to prevent context pollution.

4. **Step 4: Citation Extraction & Deterministic Guard:**
   - Synthesize answer with strict instruction to cite every factual claim via `[DocTitle:ChunkId]`.
   - Run a deterministic validator checking that citations exist and cited text contains matching entities.
   - If unverified, return explicit abstention response instead of hallucinating.

### Evaluation Protocol
To complete Phase 02, write and run an evaluation test suite containing 20 test questions:
- 10 in-domain answerable questions (Target: 100% precision, 0 hallucinations).
- 5 out-of-domain unanswerable questions (Target: 100% correct abstention, zero guesses).
- 5 adversarial trick questions with contradictory or negated premises (Target: 100% detection of contradiction).

---
[Return to Module 02](../README.md#9-capstone-engineering-challenge)
