"""
Unit & Integration Test Suite for AgentForge Platform Core.
Run via: python tests/test_all.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent_forge.gateway.rate_limiter import TokenBucketLimiter
from agent_forge.gateway.semantic_cache import SemanticCache
from agent_forge.retrieval.vector_store import VectorStore, VectorDocument, cosine_similarity
from agent_forge.retrieval.embeddings import EmbeddingGenerator
from agent_forge.retrieval.hybrid_engine import HybridRetriever
from agent_forge.runtime.state_models import AgentSession, ToolCall
from agent_forge.runtime.event_store import EventStore
from agent_forge.runtime.orchestrator import DurableOrchestrator
from agent_forge.mcp.policy_engine import PolicyEngine
from agent_forge.mcp.servers.payment_server import PaymentMCPServer
from agent_forge.evals.groundedness import GroundednessEvaluator
from agent_forge.observability.tracer import GenAITracer

class TestAgentForgeCore(unittest.TestCase):

    def test_streaming_token_bucket_limiter(self):
        """Tests upfront reservation and post-stream settlement."""
        limiter = TokenBucketLimiter(default_rpm=10, default_tpm=5000)
        tenant = "test_tenant"

        # 1. Acquire with estimated 2000 tokens
        allowed, msg = limiter.acquire(tenant, estimated_tokens=2000)
        self.assertTrue(allowed)
        self.assertEqual(msg, "OK")

        # 2. Settle with actual 1200 tokens (800 unspent tokens returned)
        limiter.settle(tenant, estimated_tokens=2000, actual_tokens=1200)

        # 3. Should still have capacity for another 3500 tokens
        allowed, _ = limiter.acquire(tenant, estimated_tokens=3500)
        self.assertTrue(allowed)

        # 4. Should be throttled on excessive demand
        allowed, msg = limiter.acquire(tenant, estimated_tokens=5000)
        self.assertFalse(allowed)
        self.assertIn("limit exceeded", msg)

    def test_tombstone_and_compaction(self):
        """Tests that deleted nodes are excluded from search and reclaimed on compaction."""
        store = VectorStore()
        gen = EmbeddingGenerator(dimension=8)
        
        doc1 = VectorDocument(id="doc_1", content="Financial refund rules", embedding=gen.generate("Financial refund rules"))
        doc2 = VectorDocument(id="doc_2", content="Product shipping rules", embedding=gen.generate("Product shipping rules"))
        store.add_documents([doc1, doc2])

        # Verify both appear initially
        results = store.search(gen.generate("refund rules"), top_k=5)
        self.assertEqual(len(results), 2)

        # Soft delete doc_1
        store.soft_delete("doc_1")
        results_after_delete = store.search(gen.generate("refund rules"), top_k=5)
        self.assertEqual(len(results_after_delete), 1)
        self.assertEqual(results_after_delete[0][0].id, "doc_2")

        # Compaction reclaims the slot
        reclaimed = store.compact()
        self.assertEqual(reclaimed, 1)
        self.assertNotIn("doc_1", store.documents)

    def test_acorn1_predicate_traversal_vs_standard(self):
        """
        Tests that ACORN-1 2-hop predicate traversal bypasses non-matching graph nodes
        where standard 1-hop traversal suffers Graph Disconnection.
        """
        store = VectorStore(max_edges=2)
        gen = EmbeddingGenerator(dimension=8)

        # Create a linear chain: Node A (US) -> Node B (EU) -> Node C (US)
        # Query seeks region='US'. Entry point is Node A.
        # In standard 1-hop, from Node A, the only neighbor is Node B (EU).
        # Standard search skips Node B and stops (Graph Disconnection!).
        # ACORN-1 explores Node B's neighbors, discovers Node C (US), and succeeds.
        docA = VectorDocument(id="A", content="Policy A US", metadata={"region": "US"}, embedding=gen.generate("Policy A US"))
        docB = VectorDocument(id="B", content="Policy B EU", metadata={"region": "EU"}, embedding=gen.generate("Policy B EU"))
        docC = VectorDocument(id="C", content="Policy C US", metadata={"region": "US"}, embedding=gen.generate("Policy C US"))
        
        # Explicitly configure neighbors to form the chain A -> B -> C
        docA.neighbors = ["B"]
        docB.neighbors = ["C"]
        docC.neighbors = []

        store.documents = {"A": docA, "B": docB, "C": docC}

        q_vec = gen.generate("Policy US")

        # Standard 1-hop traversal gets stuck at B and misses C
        std_results = store.standard_graph_search(q_vec, entry_point_id="A", filter_metadata={"region": "US"})
        self.assertEqual(len(std_results), 1)
        self.assertEqual(std_results[0][0].id, "A")

        # ACORN-1 2-hop predicate traversal navigates through B to reach C
        acorn_results = store.acorn1_search(q_vec, entry_point_id="A", filter_metadata={"region": "US"})
        self.assertEqual(len(acorn_results), 2)
        found_ids = [r[0].id for r in acorn_results]
        self.assertIn("A", found_ids)
        self.assertIn("C", found_ids)

    def test_tool_call_argument_repair(self):
        """Tests that malformed string amounts ('$49.00') are automatically repaired to floats."""
        event_store = EventStore()
        orchestrator = DurableOrchestrator(
            event_store=event_store,
            gateway=None,
            mcp_client=None,
            policy_engine=None
        )

        malformed_args = {"transaction_id": "tx_123", "amount": "$49.00"}
        repaired, note = orchestrator._validate_and_repair_tool_arguments("payment_issue_refund", malformed_args)
        
        self.assertIsNotNone(note)
        self.assertEqual(repaired["amount"], 49.00)
        self.assertIsInstance(repaired["amount"], float)

    def test_payment_idempotency_protection(self):
        """Tests that repeating a refund with the same idempotency key prevents duplicate execution."""
        server = PaymentMCPServer()
        args = {"transaction_id": "tx_9182_a", "amount": 49.00, "_idempotency_key": "fixed_key_123"}
        
        # First execution: SUCCESS
        res1 = server.call_tool("payment_issue_refund", args)
        self.assertIn("SUCCESS", res1.content)
        self.assertNotIn("IDEMPOTENT REPLAY", res1.content)

        # Second execution: IDEMPOTENT REPLAY
        res2 = server.call_tool("payment_issue_refund", args)
        self.assertIn("IDEMPOTENT REPLAY", res2.content)

    def test_semantic_cache_hit_and_miss(self):
        """Tests that SemanticCache returns cached hits for near-identical vectors and misses for dissimilar vectors."""
        cache = SemanticCache(similarity_threshold=0.90)
        vec_query = [1.0, 0.0, 0.0, 0.0]
        vec_similar = [0.99, 0.05, 0.0, 0.0]
        vec_dissimilar = [0.0, 1.0, 0.0, 0.0]

        cache.store("refund policy", vec_query, "Cached refund guidelines")

        # High similarity -> cache hit
        hit = cache.lookup("similar query", vec_similar)
        self.assertIsNotNone(hit)
        self.assertEqual(hit[0], "Cached refund guidelines")
        self.assertGreaterEqual(hit[1], 0.90)

        # Low similarity -> cache miss
        miss = cache.lookup("shipping query", vec_dissimilar)
        self.assertIsNone(miss)

    def test_hybrid_retrieval_rrf(self):
        """Tests that HybridRetriever indexes and returns Reciprocal Rank Fusion results."""
        retriever = HybridRetriever(rrf_k=60)
        docs = [
            {"id": "doc_refund", "content": "Duplicate charges are eligible for immediate refund within 24 hours."},
            {"id": "doc_shipping", "content": "Standard delivery takes 3 to 5 business days."}
        ]
        retriever.index_documents(docs)

        results = retriever.search("duplicate charge refund", top_k=2)
        self.assertGreater(len(results), 0)
        top_result = results[0]
        self.assertEqual(top_result.id, "doc_refund")
        self.assertGreater(top_result.rrf_score, 0.0)

    def test_mcp_policy_engine_enforcement(self):
        """Tests ABAC policy evaluation for permitted, approval-required, and denied tools."""
        engine = PolicyEngine(auto_refund_limit_usd=100.0)

        # 1. Deny administrative/system tools
        dec_admin = engine.evaluate("tenant_1", "usr_1", "admin_purge_database", {})
        self.assertEqual(dec_admin.status, "DENIED")

        # 2. Permit refund within threshold ($49.00)
        dec_ok = engine.evaluate("tenant_1", "usr_1", "payment_issue_refund", {"amount": 49.00})
        self.assertEqual(dec_ok.status, "PERMITTED")

        # 3. Require approval for refund exceeding threshold ($250.00)
        dec_escalate = engine.evaluate("tenant_1", "usr_1", "payment_issue_refund", {"amount": 250.00})
        self.assertEqual(dec_escalate.status, "REQUIRES_APPROVAL")

        # 4. Deny negative or invalid amounts
        dec_invalid = engine.evaluate("tenant_1", "usr_1", "payment_issue_refund", {"amount": -10.00})
        self.assertEqual(dec_invalid.status, "DENIED")

    def test_opentelemetry_genai_tracer(self):
        """Tests OTel GenAI semantic conventions tracing and parent-child span hierarchy."""
        tracer = GenAITracer(service_name="test-platform")
        root_span = tracer.start_span("agent_forge.pipeline.execute")
        root_span.set_attribute("gen_ai.system", "anthropic")

        child_span = tracer.start_span("gen_ai.tool.payment_refund")
        child_span.set_attribute("gen_ai.tool.name", "payment_issue_refund")
        child_span.set_attribute("gen_ai.usage.input_tokens", 350)
        tracer.end_span(child_span)

        tracer.end_span(root_span)

        self.assertEqual(len(tracer.root_spans), 1)
        self.assertEqual(tracer.root_spans[0].name, "agent_forge.pipeline.execute")
        self.assertEqual(len(root_span.children), 1)
        self.assertEqual(root_span.children[0].attributes["gen_ai.tool.name"], "payment_issue_refund")
        self.assertIsNotNone(root_span.end_time)
        self.assertGreaterEqual(root_span.duration_ms, 0.0)

    def test_groundedness_evaluator(self):
        """Tests contextual groundedness assertion against factual evidence and hallucinations."""
        evaluator = GroundednessEvaluator()
        evidence = ["Order 9182 duplicate charge of 49.00 was confirmed and refund is authorized."]

        # Grounded response containing authentic entity markers
        good_response = "Order 9182 has a verified refund of 49.00 processed."
        res_good = evaluator.evaluate(good_response, evidence)
        self.assertTrue(res_good.is_grounded)
        self.assertEqual(res_good.score, 1.0)
        self.assertEqual(len(res_good.unsupported_claims), 0)

        # Hallucinated response introducing unauthorized fraud claims
        hallucinated_response = "Order 9182 had $999 stolen due to fraudulent activity."
        res_bad = evaluator.evaluate(hallucinated_response, evidence)
        self.assertFalse(res_bad.is_grounded)
        self.assertEqual(res_bad.score, 0.5)
        self.assertGreater(len(res_bad.unsupported_claims), 0)

if __name__ == "__main__":
    unittest.main()
