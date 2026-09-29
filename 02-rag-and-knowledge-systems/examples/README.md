# Phase 02 Examples: Enterprise RAG & Knowledge Systems

Production-grade retrieval implementations demonstrating Reciprocal Rank Fusion (RRF), cross-encoder reranking, multi-tenant isolation, and enterprise hybrid search with Azure AI Search and Microsoft Semantic Kernel.

---

## Files Manifest

| File | Language | Purpose | Key Patterns |
|---|---|---|---|
| [`hybrid_rag_pipeline.py`](./hybrid_rag_pipeline.py) | Python 3.12+ | Multi-Tenant Hybrid Search + RRF + Reranking | In-memory BM25 Okapi, L2-normalized dense vector search, Reciprocal Rank Fusion (k=60), Cross-Encoder reranking, Pydantic v2 domain models, and zero cross-tenant leakage verification. |
| [`HybridSearchService.cs`](./HybridSearchService.cs) | C# / .NET 9 | Azure AI Search + Semantic Kernel RAG Service | Multi-stage hybrid query, OData tenant pre-filtering, Microsoft Turing Semantic Ranker, Extractive Captions, and Semantic Kernel chat synthesis. |
| [`EnterpriseRag.csproj`](./EnterpriseRag.csproj) | XML / MSBuild | C# .NET 9 Project Manifest | NuGet package references for `Azure.Search.Documents` and `Microsoft.SemanticKernel` enabling automated CI builds via `dotnet build`. |

---

## Execution & Verification

### Running the Python Pipeline:
```bash
# Execute standalone hybrid retrieval with RRF and tenant isolation
python 02-rag-and-knowledge-systems/examples/hybrid_rag_pipeline.py
```

### Compiling the C# Solution:
```bash
# Compile C# enterprise retrieval service
dotnet build 02-rag-and-knowledge-systems/examples/EnterpriseRag.csproj
```
