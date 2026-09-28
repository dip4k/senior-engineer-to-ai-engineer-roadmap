"""
In-Memory Dense Vector Store with ACORN-1 Predicate Graph Traversal
and Tombstone Compaction for AgentForge.
"""

from typing import List, Dict, Any, Tuple, Optional, Set
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
    neighbors: List[str] = Field(default_factory=list)  # Adjacency list for graph navigation

class VectorStore:
    def __init__(self, max_edges: int = 4):
        self.documents: Dict[str, VectorDocument] = {}
        self.max_edges = max_edges
        self._tombstones: Set[str] = set()

    def add_documents(self, docs: List[VectorDocument]) -> None:
        """Adds documents and incrementally links them into an NSW proximity graph."""
        for doc in docs:
            self.documents[doc.id] = doc

        # Build bidirectional proximity edges between documents
        doc_list = list(self.documents.values())
        for doc in doc_list:
            if not doc.embedding:
                continue
            scored_peers = []
            for peer in doc_list:
                if peer.id != doc.id and peer.embedding:
                    sim = cosine_similarity(doc.embedding, peer.embedding)
                    scored_peers.append((peer.id, sim))

            # Keep top M nearest neighbors
            scored_peers.sort(key=lambda x: x[1], reverse=True)
            doc.neighbors = [pid for pid, _ in scored_peers[:self.max_edges]]

    def soft_delete(self, doc_id: str) -> bool:
        """
        Marks document as deleted via tombstone.
        The node remains in the graph for navigation routing, but is omitted from search results.
        """
        if doc_id in self.documents:
            self._tombstones.add(doc_id)
            return True
        return False

    def compact(self) -> int:
        """
        Purges tombstoned documents and rewires graph edges.
        Returns the number of reclaimed nodes.
        """
        reclaimed_count = len(self._tombstones)
        if reclaimed_count == 0:
            return 0

        # Remove tombstoned documents
        for doc_id in self._tombstones:
            if doc_id in self.documents:
                del self.documents[doc_id]

        self._tombstones.clear()

        # Rebuild edges for remaining documents
        active_docs = list(self.documents.values())
        for doc in active_docs:
            doc.neighbors = [nid for nid in doc.neighbors if nid in self.documents]

        return reclaimed_count

    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[VectorDocument, float]]:
        """
        Linear scan search baseline (filtering out tombstones).
        """
        scored_candidates: List[Tuple[VectorDocument, float]] = []

        for doc_id, doc in self.documents.items():
            if doc_id in self._tombstones or not doc.embedding:
                continue

            if filter_metadata:
                match = all(doc.metadata.get(k) == v for k, v in filter_metadata.items())
                if not match:
                    continue

            score = cosine_similarity(query_vector, doc.embedding)
            scored_candidates.append((doc, score))

        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        return scored_candidates[:top_k]

    def standard_graph_search(
        self,
        query_vector: List[float],
        entry_point_id: str,
        filter_metadata: Optional[Dict[str, Any]] = None,
        top_k: int = 3
    ) -> List[Tuple[VectorDocument, float]]:
        """
        Standard 1-hop greedy graph traversal.
        Vulnerable to Graph Disconnection when filter predicates isolate nodes.
        """
        if entry_point_id not in self.documents:
            return []

        visited: Set[str] = set()
        candidates: List[Tuple[VectorDocument, float]] = []
        curr_id = entry_point_id

        while curr_id and curr_id not in visited:
            visited.add(curr_id)
            curr_doc = self.documents[curr_id]

            # Check metadata filter
            matches_filter = True
            if filter_metadata:
                matches_filter = all(curr_doc.metadata.get(k) == v for k, v in filter_metadata.items())

            if matches_filter and curr_id not in self._tombstones:
                sim = cosine_similarity(query_vector, curr_doc.embedding)
                candidates.append((curr_doc, sim))

            # Find best immediate neighbor matching filter
            best_neighbor = None
            best_sim = -1.0
            for nid in curr_doc.neighbors:
                if nid not in visited and nid in self.documents:
                    n_doc = self.documents[nid]
                    if filter_metadata:
                        if not all(n_doc.metadata.get(k) == v for k, v in filter_metadata.items()):
                            continue  # Skips non-matching node; fails if all neighbors non-matching!
                    sim = cosine_similarity(query_vector, n_doc.embedding)
                    if sim > best_sim:
                        best_sim = sim
                        best_neighbor = nid

            curr_id = best_neighbor

        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:top_k]

    def acorn1_search(
        self,
        query_vector: List[float],
        entry_point_id: str,
        filter_metadata: Optional[Dict[str, Any]] = None,
        top_k: int = 3
    ) -> List[Tuple[VectorDocument, float]]:
        """
        ACORN-1: Predicate-guided 2-hop neighborhood exploration.
        If immediate 1-hop neighbors do not satisfy the filter, inspects 2-hop neighbors
        to navigate across non-matching clusters without graph disconnection.
        """
        if entry_point_id not in self.documents:
            return []

        visited: Set[str] = set()
        matched_results: List[Tuple[VectorDocument, float]] = []
        frontier: List[str] = [entry_point_id]

        while frontier:
            curr_id = frontier.pop(0)
            if curr_id in visited or curr_id not in self.documents:
                continue

            visited.add(curr_id)
            curr_doc = self.documents[curr_id]

            # Evaluate filter on current node
            is_valid = True
            if filter_metadata:
                is_valid = all(curr_doc.metadata.get(k) == v for k, v in filter_metadata.items())

            if is_valid and curr_id not in self._tombstones:
                sim = cosine_similarity(query_vector, curr_doc.embedding)
                matched_results.append((curr_doc, sim))

            # 1-Hop Neighbor Exploration
            next_hops = []
            for nid in curr_doc.neighbors:
                if nid in self.documents and nid not in visited:
                    n_doc = self.documents[nid]
                    n_valid = True
                    if filter_metadata:
                        n_valid = all(n_doc.metadata.get(k) == v for k, v in filter_metadata.items())

                    if n_valid:
                        next_hops.append(nid)
                    else:
                        # ACORN-1 Extension: Explore 2-hop neighborhood of invalid node
                        for nnid in n_doc.neighbors:
                            if nnid in self.documents and nnid not in visited:
                                nn_doc = self.documents[nnid]
                                if filter_metadata:
                                    if all(nn_doc.metadata.get(k) == v for k, v in filter_metadata.items()):
                                        next_hops.append(nnid)

            frontier.extend(next_hops)
            if len(matched_results) >= top_k * 2:
                break

        matched_results.sort(key=lambda x: x[1], reverse=True)
        return matched_results[:top_k]
