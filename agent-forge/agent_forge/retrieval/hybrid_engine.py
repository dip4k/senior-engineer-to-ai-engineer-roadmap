"""
Hybrid Retrieval Engine with Reciprocal Rank Fusion (RRF) for AgentForge.
Merges dense semantic vector search with sparse BM25 lexical search.
"""

from typing import List, Dict, Any, Tuple, Optional
from pydantic import BaseModel
from .embeddings import EmbeddingGenerator
from .vector_store import VectorStore, VectorDocument
from .bm25 import BM25Index

class HybridSearchResult(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any]
    dense_rank: Optional[int] = None
    sparse_rank: Optional[int] = None
    rrf_score: float

class HybridRetriever:
    def __init__(self, rrf_k: int = 60):
        self.rrf_k = rrf_k
        self.embedding_gen = EmbeddingGenerator(dimension=64)
        self.vector_store = VectorStore()
        self.bm25_index = BM25Index()

    def index_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Indexes a list of documents into both the Dense Vector Store and the Sparse BM25 Index.
        """
        # 1. Sparse Index
        self.bm25_index.add_documents(documents, text_field="content")

        # 2. Dense Index
        vector_docs = []
        for doc in documents:
            text = doc["content"]
            emb = self.embedding_gen.generate(text)
            vector_docs.append(VectorDocument(
                id=doc["id"],
                content=text,
                metadata=doc.get("metadata", {}),
                embedding=emb
            ))
        self.vector_store.add_documents(vector_docs)

    def search(
        self,
        query: str,
        top_k: int = 3,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[HybridSearchResult]:
        """
        Executes hybrid retrieval:
        1. Dense Vector Search (Top 20)
        2. Sparse BM25 Search (Top 20)
        3. Reciprocal Rank Fusion (RRF)
        """
        # 1. Dense Search
        query_vector = self.embedding_gen.generate(query)
        dense_results = self.vector_store.search(
            query_vector, top_k=20, filter_metadata=filter_metadata
        )

        # 2. Sparse Search
        sparse_raw = self.bm25_index.search(query, top_k=20, text_field="content")
        # Apply metadata filter to sparse results if needed
        sparse_results = []
        for doc, score in sparse_raw:
            if filter_metadata:
                match = True
                for k, v in filter_metadata.items():
                    if doc.get("metadata", {}).get(k) != v:
                        match = False
                        break
                if not match:
                    continue
            sparse_results.append((doc, score))

        # 3. Reciprocal Rank Fusion (RRF)
        doc_ranks: Dict[str, Dict[str, Any]] = {}

        for rank_0, (vdoc, score) in enumerate(dense_results):
            r = rank_0 + 1
            if vdoc.id not in doc_ranks:
                doc_ranks[vdoc.id] = {
                    "id": vdoc.id,
                    "content": vdoc.content,
                    "metadata": vdoc.metadata,
                    "dense_rank": r,
                    "sparse_rank": None
                }
            else:
                doc_ranks[vdoc.id]["dense_rank"] = r

        for rank_0, (sdoc, score) in enumerate(sparse_results):
            r = rank_0 + 1
            doc_id = sdoc["id"]
            if doc_id not in doc_ranks:
                doc_ranks[doc_id] = {
                    "id": doc_id,
                    "content": sdoc["content"],
                    "metadata": sdoc.get("metadata", {}),
                    "dense_rank": None,
                    "sparse_rank": r
                }
            else:
                doc_ranks[doc_id]["sparse_rank"] = r

        # Calculate RRF Score
        scored_results: List[HybridSearchResult] = []
        for doc_id, entry in doc_ranks.items():
            rrf_score = 0.0
            if entry["dense_rank"] is not None:
                rrf_score += 1.0 / (self.rrf_k + entry["dense_rank"])
            if entry["sparse_rank"] is not None:
                rrf_score += 1.0 / (self.rrf_k + entry["sparse_rank"])

            scored_results.append(HybridSearchResult(
                id=doc_id,
                content=entry["content"],
                metadata=entry["metadata"],
                dense_rank=entry["dense_rank"],
                sparse_rank=entry["sparse_rank"],
                rrf_score=round(rrf_score, 6)
            ))

        # Sort descending by RRF score
        scored_results.sort(key=lambda x: x.rrf_score, reverse=True)
        return scored_results[:top_k]
