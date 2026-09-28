"""
In-Memory Dense Vector Store for AgentForge.
Provides exact vector similarity search and metadata-filtered search.
"""

from typing import List, Dict, Any, Tuple, Optional
import math
from pydantic import BaseModel, Field

def dot_product(v1: List[float], v2: List[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2))

def l2_norm(v: List[float]) -> float:
    return math.sqrt(sum(x * x for x in v))

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    norm1 = l2_norm(v1)
    norm2 = l2_norm(v2)
    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0
    return dot_product(v1, v2) / (norm1 * norm2)

class VectorDocument(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    embedding: Optional[List[float]] = None

class VectorStore:
    def __init__(self):
        self.documents: List[VectorDocument] = []

    def add_documents(self, docs: List[VectorDocument]) -> None:
        self.documents.extend(docs)

    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[VectorDocument, float]]:
        """
        Performs Cosine Similarity search with metadata filtering.
        """
        scored_candidates: List[Tuple[VectorDocument, float]] = []

        for doc in self.documents:
            if not doc.embedding:
                continue

            # Metadata Filter Check
            if filter_metadata:
                match = True
                for k, v in filter_metadata.items():
                    if doc.metadata.get(k) != v:
                        match = False
                        break
                if not match:
                    continue

            score = cosine_similarity(query_vector, doc.embedding)
            scored_candidates.append((doc, score))

        # Sort descending by score
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        return scored_candidates[:top_k]
