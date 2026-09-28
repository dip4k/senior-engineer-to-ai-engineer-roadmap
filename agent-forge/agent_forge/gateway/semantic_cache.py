"""
Semantic Cache for AgentForge Gateway.
Uses embedding vector similarity to bypass upstream LLM inference for identical or
semantically near-duplicate queries.
"""

from typing import List, Dict, Any, Optional, Tuple
import math

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

class SemanticCache:
    def __init__(self, similarity_threshold: float = 0.95):
        self.similarity_threshold = similarity_threshold
        # List of (query_text, embedding_vector, cached_response)
        self._entries: List[Tuple[str, List[float], str]] = []

    def lookup(self, query_text: str, query_embedding: List[float]) -> Optional[Tuple[str, float]]:
        """
        Returns cached response and similarity score if a match above threshold is found.
        """
        best_match = None
        best_score = -1.0

        for text, emb, response in self._entries:
            score = cosine_similarity(query_embedding, emb)
            if score > best_score:
                best_score = score
                best_match = response

        if best_score >= self.similarity_threshold:
            return best_match, best_score
        return None

    def store(self, query_text: str, query_embedding: List[float], response: str) -> None:
        """Stores a new query and response pair in the cache."""
        self._entries.append((query_text, query_embedding, response))
