"""
production_retrieval_pipeline.py
Production-grade Hybrid Search with Reciprocal Rank Fusion (RRF) and Cross-Encoder Reranking.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import numpy as np


@dataclass
class DocumentChunk:
    """Represents a discrete, indexed unit of knowledge."""
    chunk_id: str
    doc_id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    dense_vector: Optional[np.ndarray] = None


@dataclass
class ScoredChunk:
    """Represents a retrieval result with associated scoring diagnostics."""
    chunk: DocumentChunk
    bm25_rank: Optional[int] = None
    dense_rank: Optional[int] = None
    rrf_score: float = 0.0
    rerank_score: Optional[float] = None


class ProductionBM25Index:
    """In-memory BM25 Okapi lexical search engine."""
    
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size: int = 0
        self.avg_doc_len: float = 0.0
        self.doc_lengths: Dict[str, int] = {}
        self.inverted_index: Dict[str, List[str]] = {}
        self.doc_term_frequencies: Dict[str, Counter] = {}
        self.idf: Dict[str, float] = {}
        self.documents: Dict[str, DocumentChunk] = {}

    def _tokenize(self, text: str) -> List[str]:
        """Simple deterministic alphanumeric tokenizer."""
        return [word.lower() for word in text.split() if word.isalnum()]

    def index_documents(self, chunks: List[DocumentChunk]) -> None:
        self.corpus_size = len(chunks)
        total_len = 0

        for chunk in chunks:
            self.documents[chunk.chunk_id] = chunk
            tokens = self._tokenize(chunk.content)
            doc_len = len(tokens)
            self.doc_lengths[chunk.chunk_id] = doc_len
            total_len += doc_len

            term_freq = Counter(tokens)
            self.doc_term_frequencies[chunk.chunk_id] = term_freq

            for term in term_freq.keys():
                if term not in self.inverted_index:
                    self.inverted_index[term] = []
                self.inverted_index[term].append(chunk.chunk_id)

        self.avg_doc_len = total_len / self.corpus_size if self.corpus_size > 0 else 0.0

        # Calculate IDF for all indexed terms
        for term, posting_list in self.inverted_index.items():
            df = len(posting_list)
            # Standard Lucene/BM25 IDF formula
            self.idf[term] = math.log(1.0 + (self.corpus_size - df + 0.5) / (df + 0.5))

    def search(self, query: str, top_k: int = 50) -> List[tuple[DocumentChunk, float]]:
        query_tokens = self._tokenize(query)
        scores: Counter[str] = Counter()

        for term in query_tokens:
            if term not in self.inverted_index:
                continue
            idf_val = self.idf[term]
            for chunk_id in self.inverted_index[term]:
                tf = self.doc_term_frequencies[chunk_id][term]
                doc_len = self.doc_lengths[chunk_id]
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
                scores[chunk_id] += idf_val * (numerator / denominator)

        sorted_results = scores.most_common(top_k)
        return [(self.documents[chunk_id], score) for chunk_id, score in sorted_results]


class EnterpriseRetrievalEngine:
    """Orchestrates Hybrid Search (BM25 + Dense) -> RRF Fusion -> Cross-Encoder Reranking."""

    def __init__(self, chunks: List[DocumentChunk], cohere_api_key: Optional[str] = None):
        self.chunks = {c.chunk_id: c for c in chunks}
        self.bm25_index = ProductionBM25Index()
        self.bm25_index.index_documents(chunks)
        self.cohere_api_key = cohere_api_key

    def _dense_search(self, query_vector: np.ndarray, top_k: int = 50) -> List[tuple[DocumentChunk, float]]:
        """Computes exact cosine similarity across all normalized indexed dense vectors."""
        results: List[tuple[DocumentChunk, float]] = []
        # Query vector L2 normalization
        norm_q = np.linalg.norm(query_vector)
        if norm_q == 0:
            return []
        q_unit = query_vector / norm_q

        for chunk in self.chunks.values():
            if chunk.dense_vector is None:
                continue
            norm_v = np.linalg.norm(chunk.dense_vector)
            if norm_v == 0:
                continue
            v_unit = chunk.dense_vector / norm_v
            cos_sim = float(np.dot(q_unit, v_unit))
            results.append((chunk, cos_sim))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    @staticmethod
    def reciprocal_rank_fusion(
        bm25_results: List[tuple[DocumentChunk, float]],
        dense_results: List[tuple[DocumentChunk, float]],
        k_constant: int = 60,
    ) -> List[ScoredChunk]:
        """Merges ranked lists using reciprocal rank fusion."""
        fusion_map: Dict[str, ScoredChunk] = {}

        # Process BM25 Ranks
        for rank, (chunk, _) in enumerate(bm25_results, start=1):
            if chunk.chunk_id not in fusion_map:
                fusion_map[chunk.chunk_id] = ScoredChunk(chunk=chunk)
            item = fusion_map[chunk.chunk_id]
            item.bm25_rank = rank
            item.rrf_score += 1.0 / (k_constant + rank)

        # Process Dense Ranks
        for rank, (chunk, _) in enumerate(dense_results, start=1):
            if chunk.chunk_id not in fusion_map:
                fusion_map[chunk.chunk_id] = ScoredChunk(chunk=chunk)
            item = fusion_map[chunk.chunk_id]
            item.dense_rank = rank
            item.rrf_score += 1.0 / (k_constant + rank)

        merged = list(fusion_map.values())
        merged.sort(key=lambda x: x.rrf_score, reverse=True)
        return merged

    def rerank_with_cohere(
        self,
        query: str,
        candidates: List[ScoredChunk],
        top_k: int = 5,
        relevance_threshold: float = 0.65,
    ) -> List[ScoredChunk]:
        """Applies Cross-Encoder reranking using Cohere Rerank API (or heuristic fallback)."""
        if not candidates:
            return []

        if self.cohere_api_key:
            import cohere
            co = cohere.ClientV2(api_key=self.cohere_api_key)
            doc_texts = [c.chunk.content for c in candidates]
            
            response = co.rerank(
                model="rerank-v3.5",
                query=query,
                documents=doc_texts,
                top_n=top_k,
            )

            reranked_results: List[ScoredChunk] = []
            for hit in response.results:
                candidate = candidates[hit.index]
                candidate.rerank_score = float(hit.relevance_score)
                if candidate.rerank_score >= relevance_threshold:
                    reranked_results.append(candidate)
            return reranked_results
        else:
            # Fallback simulated Cross-Encoder for development / testing without API keys
            # Uses RRF score normalized to [0, 1] as surrogate
            max_rrf = candidates[0].rrf_score if candidates else 1.0
            results: List[ScoredChunk] = []
            for c in candidates[:top_k]:
                simulated_score = c.rrf_score / max_rrf
                c.rerank_score = round(simulated_score, 4)
                if c.rerank_score >= relevance_threshold:
                    results.append(c)
            return results

    def retrieve(
        self,
        query: str,
        query_vector: np.ndarray,
        first_stage_k: int = 50,
        final_top_k: int = 5,
        relevance_threshold: float = 0.60,
    ) -> List[ScoredChunk]:
        """Complete two-stage retrieval pipeline."""
        bm25_hits = self.bm25_index.search(query, top_k=first_stage_k)
        dense_hits = self._dense_search(query_vector, top_k=first_stage_k)
        rrf_fused = self.reciprocal_rank_fusion(bm25_hits, dense_hits, k_constant=60)
        final_evidence = self.rerank_with_cohere(
            query=query,
            candidates=rrf_fused[:first_stage_k],
            top_k=final_top_k,
            relevance_threshold=relevance_threshold,
        )
        return final_evidence


# =====================================================================
# Verification & Execution Example
# =====================================================================
if __name__ == "__main__":
    np.random.seed(42)
    # Synthetic enterprise knowledge corpus
    test_chunks = [
        DocumentChunk(
            chunk_id="chunk_001",
            doc_id="sec_filing_2024",
            content="In Q3 2024, our European operational division reported revenue of 48.2 million euros.",
            metadata={"source": "10-Q", "year": 2024, "region": "EMEA"},
            dense_vector=np.random.randn(128).astype(np.float32),
        ),
        DocumentChunk(
            chunk_id="chunk_002",
            doc_id="sku_catalog",
            content="Hardware module SKU-90812 is restricted to enterprise datacenter deployments under NDA.",
            metadata={"source": "spec_sheet", "sku": "SKU-90812"},
            dense_vector=np.random.randn(128).astype(np.float32),
        ),
        DocumentChunk(
            chunk_id="chunk_003",
            doc_id="hr_policy",
            content="Standard annual leave entitlement for full-time employees is 25 working days per calendar year.",
            metadata={"source": "employee_handbook", "policy": "pto"},
            dense_vector=np.random.randn(128).astype(np.float32),
        ),
    ]

    engine = EnterpriseRetrievalEngine(chunks=test_chunks)
    mock_query = "What are the deployment restrictions for hardware SKU-90812?"
    mock_vector = np.random.randn(128).astype(np.float32)

    retrieved = engine.retrieve(
        query=mock_query,
        query_vector=mock_vector,
        final_top_k=2,
        relevance_threshold=0.5,
    )

    print(f"--- Retrieved {len(retrieved)} Relevant Chunks ---")
    for idx, item in enumerate(retrieved, start=1):
        print(f"[{idx}] ID: {item.chunk.chunk_id} | Rerank Score: {item.rerank_score}")
        print(f"    Content: {item.chunk.content}")
        print(f"    Ranks: BM25={item.bm25_rank}, Dense={item.dense_rank}, RRF={item.rrf_score:.5f}\n")
