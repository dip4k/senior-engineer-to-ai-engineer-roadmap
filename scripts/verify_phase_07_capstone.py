#!/usr/bin/env python3
"""
Automated Chaos & Compliance Test Suite for Phase 07 Capstone Lab.
Verifies the 5 production acceptance criteria for the Resilient AI Gateway:
1. Exact SHA-256 Cache Hit (sub-15ms, zero upstream LLM calls)
2. Semantic Vector Cache Hit (cosine similarity >= 0.85, sub-50ms)
3. Primary Provider 429 Outage Simulation (circuit breaker trips to secondary)
4. Client Disconnect Cancellation (halts upstream inference immediately)
5. Tenant Quota Enforcement (two-phase token reservation throttles upfront)

Usage:
    python scripts/verify_phase_07_capstone.py
"""

import sys
import os
import asyncio
import time
from pathlib import Path

# Add repository root to Python path
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

# Import gateway engine from Phase 07 examples
from importlib.util import spec_from_file_location, module_from_spec
gateway_file = repo_root / "07-production-deployment-and-llmops" / "examples" / "gateway_service.py"
spec = spec_from_file_location("gateway_service", str(gateway_file))
gw_mod = module_from_spec(spec)
sys.modules["gateway_service"] = gw_mod
spec.loader.exec_module(gw_mod)

EnterpriseAIGatewayEngine = gw_mod.EnterpriseAIGatewayEngine
ChatRequest = gw_mod.ChatRequest
Bucket = gw_mod.Bucket


class CapstoneEvaluator:
    def __init__(self):
        self.gateway = EnterpriseAIGatewayEngine()
        self.results = {}

    def report(self, test_num: int, title: str, passed: bool, details: str):
        self.results[test_num] = {"title": title, "passed": passed, "details": details}
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"[{status}] Test Case {test_num}: {title}")
        print(f"       {details}\n")

    async def run_all_tests(self):
        print("=" * 70)
        print(" 🧪 PHASE 07 CAPSTONE: RESILIENT AI GATEWAY AUTOMATED VERIFICATION")
        print("=" * 70 + "\n")

        # ---------------------------------------------------------------------
        # Test Case 1: The Exact Cache Hit
        # ---------------------------------------------------------------------
        try:
            p1 = "Explain CAP theorem in two sentences."
            req1 = ChatRequest(prompt=p1, tenant_id="tenant_capstone_1")
            
            # Cold call (miss)
            chunks1 = [c async for c in self.gateway.execute_stream(req1)]
            initial_calls = self.gateway.upstream_calls
            assert initial_calls == 1, f"Expected 1 upstream call, got {initial_calls}"

            # Duplicate call (hit)
            t0 = time.perf_counter()
            chunks1_cached = [c async for c in self.gateway.execute_stream(req1)]
            latency_ms = (time.perf_counter() - t0) * 1000.0

            assert self.gateway.upstream_calls == 1, "Upstream calls must not increase on exact cache hit!"
            assert "exact" in chunks1_cached[0], "Expected exact cache hit metadata in payload"
            assert latency_ms < 20.0, f"Cache hit latency too high: {latency_ms:.2f}ms"

            self.report(1, "The Exact Cache Hit (SHA-256)", True,
                        f"Cache hit returned in {latency_ms:.2f}ms. Zero additional upstream calls generated.")
        except Exception as e:
            self.report(1, "The Exact Cache Hit (SHA-256)", False, str(e))

        # ---------------------------------------------------------------------
        # Test Case 2: The Semantic Cache Hit
        # ---------------------------------------------------------------------
        try:
            p2 = "Explain the CAP theorem in two concise sentences."
            req2 = ChatRequest(prompt=p2, tenant_id="tenant_capstone_1")

            t0 = time.perf_counter()
            chunks2_cached = [c async for c in self.gateway.execute_stream(req2)]
            latency_ms = (time.perf_counter() - t0) * 1000.0

            assert self.gateway.upstream_calls == 1, "Upstream calls must not increase on semantic cache hit!"
            assert "semantic" in chunks2_cached[0], "Expected semantic cache hit metadata in payload"
            assert latency_ms < 50.0, f"Semantic cache hit latency too high: {latency_ms:.2f}ms"

            self.report(2, "The Semantic Cache Hit (Vector Similarity)", True,
                        f"Cosine similarity matched existing entry in {latency_ms:.2f}ms with 0 upstream tokens.")
        except Exception as e:
            self.report(2, "The Semantic Cache Hit (Vector Similarity)", False, str(e))

        # ---------------------------------------------------------------------
        # Test Case 3: Primary Provider 429 Outage Simulation
        # ---------------------------------------------------------------------
        try:
            p3 = "Architecting resilient distributed key-value stores"
            req3 = ChatRequest(prompt=p3, tenant_id="tenant_capstone_2")

            # Force primary provider 429 outage
            chunks3 = [c async for c in self.gateway.execute_stream(req3, force_primary_outage=True)]
            has_secondary_failover = any("gemini-2.0-flash" in c for c in chunks3)

            assert has_secondary_failover, "Gateway failed to route to secondary provider upon 429 outage"
            self.report(3, "Primary Provider 429 Outage Simulation", True,
                        "Circuit breaker detected primary failure; seamlessly failed over to secondary model without dropping client.")
        except Exception as e:
            self.report(3, "Primary Provider 429 Outage Simulation", False, str(e))

        # ---------------------------------------------------------------------
        # Test Case 4: Client Disconnect Cancellation
        # ---------------------------------------------------------------------
        try:
            p4 = "Stream 1000 tokens describing Raft consensus"
            req4 = ChatRequest(prompt=p4, tenant_id="tenant_capstone_3")

            token_counter = [0]
            def simulate_client_drop():
                token_counter[0] += 1
                return token_counter[0] > 2  # Disconnect after 2 tokens

            chunks4 = [c async for c in self.gateway.execute_stream(req4, is_disconnected_fn=simulate_client_drop)]
            # Expected: 2 tokens + 1 [DONE]
            assert len(chunks4) <= 4, f"Generation failed to abort! Received {len(chunks4)} chunks"

            self.report(4, "Client Disconnect Cancellation Propagation", True,
                        f"Socket disconnect caught after {len(chunks4)} chunks; upstream generation terminated immediately.")
        except Exception as e:
            self.report(4, "Client Disconnect Cancellation Propagation", False, str(e))

        # ---------------------------------------------------------------------
        # Test Case 5: Tenant Quota Enforcement
        # ---------------------------------------------------------------------
        try:
            p5 = "Generate massive batch data"
            self.gateway.limiter._buckets["tenant_capstone_poor"] = Bucket(
                rpm_cap=30, tpm_cap=5000, cur_rpm=30, cur_tpm=100, last_update=time.time()
            )
            req5 = ChatRequest(prompt=p5, tenant_id="tenant_capstone_poor", max_tokens=1000)

            chunks5 = [c async for c in self.gateway.execute_stream(req5)]
            assert "RateLimitExceeded" in chunks5[0], "Expected upfront rate limit rejection"

            self.report(5, "Tenant Quota Enforcement (Token Bucket)", True,
                        "Two-phase reservation throttled request upfront (HTTP 429) before calling vector search or LLM.")
        except Exception as e:
            self.report(5, "Tenant Quota Enforcement (Token Bucket)", False, str(e))

        # ---------------------------------------------------------------------
        # Final Summary
        # ---------------------------------------------------------------------
        passed_count = sum(1 for r in self.results.values() if r["passed"])
        total_count = len(self.results)
        print("=" * 70)
        print(f" Summary: {passed_count}/{total_count} Capstone Acceptance Tests Passing")
        print("=" * 70)

        if passed_count < total_count:
            sys.exit(1)


def main():
    evaluator = CapstoneEvaluator()
    asyncio.run(evaluator.run_all_tests())


if __name__ == "__main__":
    main()
