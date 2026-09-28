"""
BM25 (Best Matching 25) Sparse Lexical Search Engine for AgentForge.
Provides exact keyword, acronym, and identifier matching.
"""

from typing import List, Dict, Any, Tuple
import math
from collections import Counter

class BM25Index:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: List[Dict[str, Any]] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_length: float = 0.0
        self.doc_freqs: Dict[str, int] = Counter()
        self.corpus_size: int = 0

    def _tokenize(self, text: str) -> List[str]:
        return text.lower().replace("-", " ").replace("_", " ").replace(".", " ").split()

    def add_documents(self, docs: List[Dict[str, Any]], text_field: str = "content") -> None:
        self.documents = docs
        self.corpus_size = len(docs)
        self.doc_lengths = []
        self.doc_freqs = Counter()

        tokenized_corpus = []
        total_length = 0

        for doc in docs:
            tokens = self._tokenize(doc.get(text_field, ""))
            tokenized_corpus.append(tokens)
            length = len(tokens)
            self.doc_lengths.append(length)
            total_length += length
            
            # Count unique terms in doc for document frequency
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self.doc_freqs[token] += 1

        self.avg_doc_length = total_length / self.corpus_size if self.corpus_size > 0 else 0.0

    def search(self, query: str, top_k: int = 5, text_field: str = "content") -> List[Tuple[Dict[str, Any], float]]:
        query_tokens = self._tokenize(query)
        scores: List[float] = [0.0] * self.corpus_size

        for token in query_tokens:
            if token not in self.doc_freqs:
                continue

            # Robertson-Spärck Jones IDF
            n_q = self.doc_freqs[token]
            idf = math.log((self.corpus_size - n_q + 0.5) / (n_q + 0.5) + 1.0)

            for doc_idx, doc in enumerate(self.documents):
                doc_tokens = self._tokenize(doc.get(text_field, ""))
                freq = doc_tokens.count(token)
                if freq == 0:
                    continue

                doc_len = self.doc_lengths[doc_idx]
                numerator = freq * (self.k1 + 1.0)
                denominator = freq + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_length))
                scores[doc_idx] += idf * (numerator / denominator)

        # Sort descending by score
        ranked_indices = sorted(range(self.corpus_size), key=lambda i: scores[i], reverse=True)
        results = []
        for idx in ranked_indices[:top_k]:
            if scores[idx] > 0.0:
                results.append((self.documents[idx], scores[idx]))
        return results
