# Phase 02 Examples: RAG & Knowledge Systems

Production-grade retrieval implementations demonstrating Reciprocal Rank Fusion (RRF), cross-encoder re-ranking, and enterprise hybrid search with Azure AI Search and Semantic Kernel.

## Files

| File | Language | Purpose | Key Patterns |
|---|---|---|---|
| [`hybrid_rag_pipeline.py`](./hybrid_rag_pipeline.py) | Python 3.11+ | Hybrid Search + RRF + Cohere Reranking | In-memory BM25 + dense Qdrant vector retrieval, RRF fusion ($k=60$), cross-encoder reranker |
| [`HybridSearchService.cs`](./HybridSearchService.cs) | C# / .NET 9 | Azure AI Search + Semantic Kernel RAG | Semantic Ranker, vector search, ASP.NET Core dependency injection, memory plugin |
