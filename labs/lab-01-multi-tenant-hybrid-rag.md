# Lab 1: Multi-Tenant Hybrid RAG

[🔙 Back to Module 02: RAG & Knowledge](../02-rag-and-knowledge-systems/README.md)

## Objective
Build an enterprise retrieval pipeline combining lexical search and semantic vector search with tenant-level isolation.

## Architectural Requirements
1. Ingest sample documentation with metadata (`tenant_id`, `department`, `created_at`).
2. Implement sparse search (BM25 / inverted index) and dense vector search (HNSW index).
3. Merge candidate results using Reciprocal Rank Fusion (RRF):
   `RRF_Score = sum(1 / (k + rank_i))` where `k = 60`.
4. Pass top-20 merged candidates to a cross-encoder reranker to extract top-5 final chunks.
5. Enforce strict tenant pre-filtering to ensure queries never return documents belonging to other tenants.

## Verification Criteria
Querying for exact alphanumeric product codes returns 100% precision; queries with unauthorized tenant IDs return zero documents.
