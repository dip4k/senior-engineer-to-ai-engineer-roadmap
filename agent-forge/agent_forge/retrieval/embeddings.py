"""
Deterministic Embedding Generator for AgentForge Retrieval.
Produces unit-normalized 64-dimensional dense vectors using a token hash projection
using pure Python standard library (no external C-extensions required).
"""

from typing import List
import math
import hashlib

def l2_norm(vector: List[float]) -> float:
    return math.sqrt(sum(x * x for x in vector))

def normalize(vector: List[float]) -> List[float]:
    norm = l2_norm(vector)
    if norm == 0.0:
        return vector
    return [x / norm for x in vector]

def dot_product(v1: List[float], v2: List[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2))

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    norm1 = l2_norm(v1)
    norm2 = l2_norm(v2)
    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0
    return dot_product(v1, v2) / (norm1 * norm2)

class EmbeddingGenerator:
    def __init__(self, dimension: int = 64):
        self.dimension = dimension

    def generate(self, text: str) -> List[float]:
        """
        Generates a unit-normalized dense embedding vector for the input text.
        Semantically overlapping tokens produce higher cosine similarity.
        """
        tokens = text.lower().replace("-", " ").replace("_", " ").split()
        vector = [0.0] * self.dimension

        if not tokens:
            return vector

        for token in tokens:
            # Deterministic hash projection to dimension indices
            h = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
            idx = h % self.dimension
            sign = 1.0 if ((h >> 8) % 2 == 0) else -1.0
            vector[idx] += sign * (1.0 + len(token) * 0.1)

            # Secondary projection for bigrams
            idx2 = (h >> 4) % self.dimension
            vector[idx2] += sign * 0.5

        return normalize(vector)

    def generate_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.generate(t) for t in texts]
