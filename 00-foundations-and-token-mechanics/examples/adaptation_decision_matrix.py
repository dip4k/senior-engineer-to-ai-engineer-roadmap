"""
adaptation_decision_matrix.py
-------------------------------------------------------------------------------
Production-grade Decision Matrix & Cost Optimization Engine for LLM Adaptation.

Mathematically models and compares the 4 core adaptation and inference strategies:
  1. Prompt Caching (Prefix KV-Cache reuse)
  2. RAG (Retrieval-Augmented Generation with Vector Indexing)
  3. LoRA / QLoRA Fine-Tuning (Parameter-Efficient Low-Rank Adaptation)
  4. Test-Time Compute (Reasoning Models / Extended System 2 Thinking)

Calculates exact multi-month Total Cost of Ownership (TCO), latency profiles,
break-even thresholds, and outputs deterministic architectural recommendations.
-------------------------------------------------------------------------------
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional
import json
import math


class TaskVariability(Enum):
    LOW = "low"            # Fixed schema, highly repetitive tasks (e.g. classification, formatting)
    MEDIUM = "medium"      # Semi-structured, moderate domain variation (e.g. customer support)
    HIGH = "high"          # Unbounded, novel inputs, multi-hop logical deductions (e.g. complex coding, theorem proving)


class KnowledgeDynamics(Enum):
    STATIC = "static"          # Stable domain knowledge (e.g. code syntax, legal structure)
    PERIODIC = "periodic"      # Changes weekly or monthly (e.g. product catalogs)
    REAL_TIME = "real_time"    # Changes minute-by-minute (e.g. live financial tickers, inventory)


@dataclass
class WorkloadProfile:
    name: str
    monthly_requests: int
    prompt_tokens_per_request: int
    completion_tokens_per_request: int
    latency_sla_ms: int
    task_variability: TaskVariability
    knowledge_dynamics: KnowledgeDynamics
    accuracy_criticality: float  # 0.0 to 1.0 (1.0 = zero-tolerance for reasoning errors)
    requires_citation: bool = False
    planning_horizon_months: int = 12


@dataclass
class CostBreakdown:
    strategy_name: str
    upfront_setup_cost_usd: float
    monthly_recurring_cost_usd: float
    total_horizon_cost_usd: float
    cost_per_request_usd: float
    estimated_ttft_ms: float
    estimated_tps: float
    pros: List[str]
    cons: List[str]
    is_disqualified: bool = False
    disqualification_reason: Optional[str] = None


class AdaptationDecisionEngine:
    """
    Evaluates hardware and API economics across Prompt Caching, RAG,
    LoRA/QLoRA Fine-Tuning, and Test-Time Compute Reasoning.
    """

    # Baseline cloud API and compute rates (2026 enterprise standard)
    RATES = {
        "frontier_standard": {
            "input_per_m": 3.00,        # Claude 3.7 Sonnet / GPT-4.5 base input
            "output_per_m": 15.00,      # Standard output
            "cache_write_per_m": 3.75,  # 25% write surcharge
            "cache_read_per_m": 0.30,   # 90% read discount
        },
        "frontier_reasoning": {
            "input_per_m": 3.00,
            "output_per_m": 15.00,      # Thinking tokens billed at output rate
            "average_thinking_tokens": 4096,
        },
        "slm_hosted": {
            "input_per_m": 0.20,        # Phi-4 / Qwen 2.5 14B hosted endpoint
            "output_per_m": 0.60,
        },
        "rag_infrastructure": {
            "embedding_per_m": 0.02,    # text-embedding-3-small
            "vector_db_monthly_base": 75.00,
            "retrieved_chunks_tokens": 1500,
        },
        "lora_compute": {
            "gpu_training_hour_cost": 4.50,  # 8x A100/H100 PCIe node per hour
            "training_hours_required": 12.0,  # Typical 7B-14B QLoRA convergence
            "dataset_curation_fixed": 3500.0, # Data engineering & human-in-the-loop audit
        }
    }

    def __init__(self, rates: Optional[Dict[str, Any]] = None):
        self.rates = rates or self.RATES

    def evaluate_prompt_caching(self, profile: WorkloadProfile) -> CostBreakdown:
        cfg = self.rates["frontier_standard"]
        
        # In prompt caching, the static prefix (typically 75% of prompt) is cached.
        # Assume 85% cache hit rate in production with 15-minute TTL.
        cached_prefix_tokens = int(profile.prompt_tokens_per_request * 0.75)
        dynamic_tokens = profile.prompt_tokens_per_request - cached_prefix_tokens
        cache_hit_rate = 0.88

        # Monthly costs
        requests = profile.monthly_requests
        # Cache write cost (12% misses require full write, plus TTL re-hydration)
        cache_writes = requests * (1.0 - cache_hit_rate) + (24 * 30 * 4)  # 4 re-hydrations per hour
        write_cost = (cache_writes * cached_prefix_tokens / 1_000_000.0) * cfg["cache_write_per_m"]

        # Cache reads
        cache_reads = requests * cache_hit_rate
        read_cost = (cache_reads * cached_prefix_tokens / 1_000_000.0) * cfg["cache_read_per_m"]

        # Dynamic input tokens & completion tokens
        dynamic_in_cost = (requests * dynamic_tokens / 1_000_000.0) * cfg["input_per_m"]
        completion_cost = (requests * profile.completion_tokens_per_request / 1_000_000.0) * cfg["output_per_m"]

        monthly_total = write_cost + read_cost + dynamic_in_cost + completion_cost
        horizon_total = monthly_total * profile.planning_horizon_months
        unit_cost = monthly_total / requests if requests > 0 else 0.0

        # Latency estimation: Cache hits bypass 75% of prefill
        ttft = 120.0 + (dynamic_tokens * 0.04)

        return CostBreakdown(
            strategy_name="Prompt Caching (Prefix KV-Cache)",
            upfront_setup_cost_usd=0.0,
            monthly_recurring_cost_usd=round(monthly_total, 2),
            total_horizon_cost_usd=round(horizon_total, 2),
            cost_per_request_usd=round(unit_cost, 5),
            estimated_ttft_ms=round(ttft, 1),
            estimated_tps=75.0,
            pros=[
                "Zero model weights modified (zero training risk or catastrophic forgetting)",
                "Immediate 80-90% input cost reduction on static prefixes",
                "Sub-150ms TTFT due to pre-computed KV-cache in GPU VRAM",
                "Trivial to deploy with native SDK cache_control tags"
            ],
            cons=[
                "Context window is still physically occupied by the prompt tokens",
                "Cache prefix taint invalidates entire cache if prefix changes",
                "Subject to provider eviction TTLs (typically 5-10 minutes of inactivity)"
            ]
        )

    def evaluate_rag(self, profile: WorkloadProfile) -> CostBreakdown:
        cfg = self.rates["frontier_standard"]
        rag_cfg = self.rates["rag_infrastructure"]

        # Disqualification check
        is_disqualified = False
        disq_reason = None
        if profile.knowledge_dynamics == KnowledgeDynamics.STATIC and profile.prompt_tokens_per_request < 1500:
            is_disqualified = True
            disq_reason = "Overkill: Knowledge base is static and fits easily inside standard prompt context."

        requests = profile.monthly_requests
        retrieved_tokens = rag_cfg["retrieved_chunks_tokens"]
        total_input_tokens = profile.prompt_tokens_per_request + retrieved_tokens

        # Monthly costs
        monthly_input_cost = (requests * total_input_tokens / 1_000_000.0) * cfg["input_per_m"]
        monthly_completion_cost = (requests * profile.completion_tokens_per_request / 1_000_000.0) * cfg["output_per_m"]
        monthly_embedding_queries = (requests * 150 / 1_000_000.0) * rag_cfg["embedding_per_m"]
        vector_db_cost = rag_cfg["vector_db_monthly_base"]

        monthly_total = monthly_input_cost + monthly_completion_cost + monthly_embedding_queries + vector_db_cost
        upfront_cost = 1500.0  # Indexing pipeline, chunking evaluation & embedding setup
        horizon_total = upfront_cost + (monthly_total * profile.planning_horizon_months)
        unit_cost = monthly_total / requests if requests > 0 else 0.0

        # Latency: Vector search (50-100ms) + Re-ranker (80ms) + LLM Prefill
        ttft = 180.0 + (total_input_tokens * 0.06)

        return CostBreakdown(
            strategy_name="Retrieval-Augmented Generation (RAG)",
            upfront_setup_cost_usd=upfront_cost,
            monthly_recurring_cost_usd=round(monthly_total, 2),
            total_horizon_cost_usd=round(horizon_total, 2),
            cost_per_request_usd=round(unit_cost, 5),
            estimated_ttft_ms=round(ttft, 1),
            estimated_tps=70.0,
            pros=[
                "Guarantees real-time knowledge freshness without retraining",
                "Provides deterministic source citations and audit trails",
                "Access control / RBAC can be enforced at document chunk level",
                "Decouples data storage from model parameters"
            ],
            cons=[
                "High latency overhead (retrieval + re-ranking + expanded prefill)",
                "Vulnerable to retrieval failures, semantic chunk fragmentation, and context rot",
                "Ongoing infrastructure burden (vector database indexing, sync pipelines)"
            ],
            is_disqualified=is_disqualified,
            disqualification_reason=disq_reason
        )

    def evaluate_lora_fine_tuning(self, profile: WorkloadProfile) -> CostBreakdown:
        lora_cfg = self.rates["lora_compute"]
        slm_cfg = self.rates["slm_hosted"]

        # Disqualification checks
        is_disqualified = False
        disq_reason = None
        if profile.knowledge_dynamics == KnowledgeDynamics.REAL_TIME:
            is_disqualified = True
            disq_reason = "Disqualified: Fine-tuning cannot reliably memorize rapidly changing real-time data."
        elif profile.requires_citation:
            is_disqualified = True
            disq_reason = "Disqualified: Fine-tuning embeds knowledge parametrically, unable to emit verifiable source citations."

        requests = profile.monthly_requests

        # Fine-tuning encodes few-shot examples and domain rules directly into weights!
        # This dramatically reduces required prompt tokens (typically by 75-85%).
        compact_prompt_tokens = max(100, int(profile.prompt_tokens_per_request * 0.20))

        # Fine-tuned model served on dedicated or cheaper SLM endpoint (e.g. Phi-4 / Qwen 14B QLoRA)
        monthly_input_cost = (requests * compact_prompt_tokens / 1_000_000.0) * slm_cfg["input_per_m"]
        monthly_output_cost = (requests * profile.completion_tokens_per_request / 1_000_000.0) * slm_cfg["output_per_m"]
        monthly_hosting_fixed = 150.0  # Dedicated LoRA adapter serving instance overhead

        monthly_recurring = monthly_input_cost + monthly_output_cost + monthly_hosting_fixed

        # Upfront training & data curation cost
        compute_cost = lora_cfg["gpu_training_hour_cost"] * lora_cfg["training_hours_required"]
        upfront_cost = compute_cost + lora_cfg["dataset_curation_fixed"]

        horizon_total = upfront_cost + (monthly_recurring * profile.planning_horizon_months)
        unit_cost = monthly_recurring / requests if requests > 0 else 0.0

        # Latency: Much smaller prompt prefill + high-throughput SLM decode
        ttft = 65.0 + (compact_prompt_tokens * 0.02)

        return CostBreakdown(
            strategy_name="LoRA / QLoRA Fine-Tuning (PEFT)",
            upfront_setup_cost_usd=round(upfront_cost, 2),
            monthly_recurring_cost_usd=round(monthly_recurring, 2),
            total_horizon_cost_usd=round(horizon_total, 2),
            cost_per_request_usd=round(unit_cost, 5),
            estimated_ttft_ms=round(ttft, 1),
            estimated_tps=95.0,
            pros=[
                "Eliminates thousands of few-shot prompt tokens per request, slashing variable costs",
                "Internalizes complex domain syntax, tone, and proprietary DSL formatting",
                "Sub-100ms TTFT and highest throughput via compact SLM architecture",
                "Full air-gapped on-premise portability (zero third-party data exfiltration)"
            ],
            cons=[
                "High upfront data curation and validation cost ($3.5k-$10k)",
                "Catastrophic forgetting risk if adapter overfits to narrow task distribution",
                "Cannot store dynamic facts or provide verifiable source citations"
            ],
            is_disqualified=is_disqualified,
            disqualification_reason=disq_reason
        )

    def evaluate_test_time_compute(self, profile: WorkloadProfile) -> CostBreakdown:
        cfg = self.rates["frontier_reasoning"]

        # Disqualification check
        is_disqualified = False
        disq_reason = None
        if profile.latency_sla_ms < 3000:
            is_disqualified = True
            disq_reason = f"Disqualified: Latency SLA ({profile.latency_sla_ms}ms) violates reasoning TTFT minimum (~3,000ms - 25,000ms)."

        requests = profile.monthly_requests
        thinking_tokens = cfg["average_thinking_tokens"]

        # In reasoning models (o3, Claude 3.7 Thinking), thinking tokens are billed as output tokens!
        total_billable_output = profile.completion_tokens_per_request + thinking_tokens

        monthly_input_cost = (requests * profile.prompt_tokens_per_request / 1_000_000.0) * cfg["input_per_m"]
        monthly_output_cost = (requests * total_billable_output / 1_000_000.0) * cfg["output_per_m"]

        monthly_recurring = monthly_input_cost + monthly_output_cost
        horizon_total = monthly_recurring * profile.planning_horizon_months
        unit_cost = monthly_recurring / requests if requests > 0 else 0.0

        # Latency: Multi-step tree search / CoT generation requires seconds
        ttft = 3500.0 + (thinking_tokens * 8.0)

        return CostBreakdown(
            strategy_name="Test-Time Compute (Reasoning Models)",
            upfront_setup_cost_usd=0.0,
            monthly_recurring_cost_usd=round(monthly_recurring, 2),
            total_horizon_cost_usd=round(horizon_total, 2),
            cost_per_request_usd=round(unit_cost, 5),
            estimated_ttft_ms=round(ttft, 1),
            estimated_tps=60.0,
            pros=[
                "State-of-the-art accuracy on multi-step logic, formal math, and complex code refactoring",
                "Internal self-verification and backtracking eliminates subtle algorithmic hallucinations",
                "Decouples reasoning performance from model size through dynamic search scaling",
                "Zero training or vector database infrastructure overhead"
            ],
            cons=[
                "50:1 cost asymmetry: thousands of hidden thinking tokens billed at premium output rates",
                "Severe latency profile (TTFT ranges from 4s to 45s; unusable for interactive real-time UIs)",
                "Overkill for routine extraction, classification, or standard CRUD operations"
            ],
            is_disqualified=is_disqualified,
            disqualification_reason=disq_reason
        )

    def recommend(self, profile: WorkloadProfile) -> Dict[str, Any]:
        evaluations = [
            self.evaluate_prompt_caching(profile),
            self.evaluate_rag(profile),
            self.evaluate_lora_fine_tuning(profile),
            self.evaluate_test_time_compute(profile),
        ]

        # Multi-factor architectural scoring
        qualified = [e for e in evaluations if not e.is_disqualified]
        
        # Scoring function balancing Cost, Latency SLA, and Task Fit
        scored_options = []
        for opt in qualified:
            # Latency penalty: penalize if estimated TTFT approaches or exceeds SLA
            latency_ratio = opt.estimated_ttft_ms / max(1.0, profile.latency_sla_ms)
            if latency_ratio > 1.0:
                continue  # Hard SLA breach

            # Cost score (normalized against planning horizon)
            cost_penalty = opt.total_horizon_cost_usd

            # Suitability bonus based on task variability & requirements
            suitability_score = 100.0
            if opt.strategy_name.startswith("Test-Time") and profile.task_variability == TaskVariability.HIGH and profile.accuracy_criticality >= 0.8:
                suitability_score += 150.0  # Massive reasoning advantage
            elif opt.strategy_name.startswith("LoRA") and profile.task_variability == TaskVariability.LOW and profile.monthly_requests > 50_000:
                suitability_score += 120.0  # Massive throughput / token elimination advantage
            elif opt.strategy_name.startswith("RAG") and profile.knowledge_dynamics in (KnowledgeDynamics.PERIODIC, KnowledgeDynamics.REAL_TIME):
                suitability_score += 130.0  # Knowledge synchronization advantage
            elif opt.strategy_name.startswith("Prompt Caching") and profile.task_variability == TaskVariability.LOW:
                suitability_score += 80.0

            final_score = suitability_score - (cost_penalty / 1000.0)
            scored_options.append((final_score, opt))

        scored_options.sort(key=lambda x: x[0], reverse=True)
        recommended = scored_options[0][1] if scored_options else evaluations[0]

        return {
            "workload": {
                "name": profile.name,
                "monthly_requests": profile.monthly_requests,
                "prompt_tokens": profile.prompt_tokens_per_request,
                "completion_tokens": profile.completion_tokens_per_request,
                "latency_sla_ms": profile.latency_sla_ms,
                "task_variability": profile.task_variability.value,
                "knowledge_dynamics": profile.knowledge_dynamics.value,
            },
            "recommendation": {
                "selected_strategy": recommended.strategy_name,
                "rationale": self._generate_rationale(recommended, profile),
                "horizon_months": profile.planning_horizon_months,
                "projected_tco_usd": recommended.total_horizon_cost_usd,
                "unit_cost_usd": recommended.cost_per_request_usd,
                "estimated_ttft_ms": recommended.estimated_ttft_ms
            },
            "comparative_analysis": [
                {
                    "strategy": e.strategy_name,
                    "is_disqualified": e.is_disqualified,
                    "disqualification_reason": e.disqualification_reason,
                    "upfront_setup_usd": e.upfront_setup_cost_usd,
                    "monthly_recurring_usd": e.monthly_recurring_cost_usd,
                    "total_horizon_cost_usd": e.total_horizon_cost_usd,
                    "cost_per_request_usd": e.cost_per_request_usd,
                    "estimated_ttft_ms": e.estimated_ttft_ms,
                    "pros": e.pros,
                    "cons": e.cons
                }
                for e in evaluations
            ]
        }

    def _generate_rationale(self, choice: CostBreakdown, profile: WorkloadProfile) -> str:
        name = choice.strategy_name
        if "Prompt Caching" in name:
            return (
                f"Prompt Caching is the optimal strategy because request volume ({profile.monthly_requests:,}/mo) "
                f"features high prefix repetition with low task variability. It slashes input token costs by ~88% "
                f"without incurring the upfront data engineering and maintenance debt of fine-tuning."
            )
        elif "RAG" in name:
            return (
                f"RAG is recommended due to knowledge dynamics ({profile.knowledge_dynamics.value}) and verification requirements. "
                f"Dynamic external knowledge must be cited and updated in real-time, which parameter-based adaptation cannot guarantee."
            )
        elif "LoRA" in name:
            return (
                f"LoRA / QLoRA Fine-Tuning achieves the lowest multi-month TCO (${choice.total_horizon_cost_usd:,} over {profile.planning_horizon_months} mos). "
                f"At {profile.monthly_requests:,} requests/mo, eliminating {int(profile.prompt_tokens_per_request * 0.8):,} prompt tokens per call "
                f"amortizes the ${choice.upfront_setup_cost_usd:,.2f} upfront training investment within months."
            )
        else:
            return (
                f"Test-Time Compute Reasoning is required because task variability is high and accuracy criticality is {profile.accuracy_criticality * 100:.0f}%. "
                f"The problem demands multi-step verification and error recovery that standard pattern-matching models fail on."
            )


# -----------------------------------------------------------------------------
# Runnable Verification & Enterprise Scenarios
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    engine = AdaptationDecisionEngine()

    scenarios = [
        WorkloadProfile(
            name="Tier-1 High-Volume E-Commerce Customer Support",
            monthly_requests=500_000,
            prompt_tokens_per_request=3_500,  # Large policy & catalog rules in prompt
            completion_tokens_per_request=300,
            latency_sla_ms=1200,
            task_variability=TaskVariability.LOW,
            knowledge_dynamics=KnowledgeDynamics.STATIC,
            accuracy_criticality=0.7,
            requires_citation=False,
            planning_horizon_months=12
        ),
        WorkloadProfile(
            name="Autonomous Multi-Repo Security Vulnerability Auditor",
            monthly_requests=10_000,
            prompt_tokens_per_request=8_000,
            completion_tokens_per_request=1_500,
            latency_sla_ms=60_000,  # Async background queue: 60-second SLA
            task_variability=TaskVariability.HIGH,
            knowledge_dynamics=KnowledgeDynamics.STATIC,
            accuracy_criticality=0.98,
            requires_citation=False,
            planning_horizon_months=6
        ),
        WorkloadProfile(
            name="Real-Time Legal & Compliance Discovery Assistant",
            monthly_requests=40_000,
            prompt_tokens_per_request=1_200,
            completion_tokens_per_request=600,
            latency_sla_ms=2500,
            task_variability=TaskVariability.MEDIUM,
            knowledge_dynamics=KnowledgeDynamics.PERIODIC,
            accuracy_criticality=0.95,
            requires_citation=True,
            planning_horizon_months=12
        )
    ]

    print("=" * 80)
    print("ENTERPRISE LLM ADAPTATION DECISION MATRIX & TCO CALCULATOR")
    print("=" * 80)

    for scenario in scenarios:
        result = engine.recommend(scenario)
        print(f"\n[SCENARIO]: {result['workload']['name']}")
        print(f"  • Monthly Volume: {result['workload']['monthly_requests']:,} reqs | Latency SLA: {result['workload']['latency_sla_ms']}ms")
        print(f"  • RECOMMENDED STRATEGY: >>> {result['recommendation']['selected_strategy']} <<<")
        print(f"  • Projected Horizon TCO: ${result['recommendation']['projected_tco_usd']:,.2f} ({result['recommendation']['horizon_months']} months)")
        print(f"  • Cost Per Request: ${result['recommendation']['unit_cost_usd']:.5f} | Estimated TTFT: {result['recommendation']['estimated_ttft_ms']}ms")
        print(f"  • Architectural Rationale: {result['recommendation']['rationale']}")
        print("\n  Strategy Breakdown:")
        for comp in result["comparative_analysis"]:
            status = "DISQUALIFIED" if comp["is_disqualified"] else f"${comp['total_horizon_cost_usd']:,.2f}"
            note = f"({comp['disqualification_reason']})" if comp["is_disqualified"] else f"TTFT: {comp['estimated_ttft_ms']}ms"
            print(f"    - {comp['strategy']:<42} : {status:<14} | {note}")
        print("-" * 80)
