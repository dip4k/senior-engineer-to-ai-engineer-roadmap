"""
production_token_profiler.py
Production-grade tokenization profiler, latency forecaster, and cost auditor
supporting standard frontier models and test-time compute reasoning tokens.
"""

from typing import Dict, Any, Optional

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False

class ProductionTokenProfiler:
    PROVIDER_RATES = {
        "claude-3-7-sonnet": {"input_per_m": 3.00, "output_per_m": 15.00, "encoding": "cl100k_base", "is_reasoning": True},
        "o3-mini": {"input_per_m": 1.10, "output_per_m": 4.40, "encoding": "o200k_base", "is_reasoning": True},
        "gpt-4o": {"input_per_m": 2.50, "output_per_m": 10.00, "encoding": "o200k_base", "is_reasoning": False},
        "gemini-2.0-flash": {"input_per_m": 0.10, "output_per_m": 0.40, "encoding": "cl100k_base", "is_reasoning": False},
        "deepseek-r1": {"input_per_m": 0.55, "output_per_m": 2.19, "encoding": "cl100k_base", "is_reasoning": True},
    }

    def __init__(self, model_key: str = "claude-3-7-sonnet"):
        if model_key not in self.PROVIDER_RATES:
            raise ValueError(f"Unsupported model: {model_key}. Permitted: {list(self.PROVIDER_RATES.keys())}")
        self.model_key = model_key
        self.config = self.PROVIDER_RATES[model_key]
        if HAS_TIKTOKEN:
            self.encoder = tiktoken.get_encoding(self.config["encoding"])
        else:
            self.encoder = None

    def _count_tokens(self, text: str) -> int:
        if self.encoder:
            return len(self.encoder.encode(text, disallowed_special=()))
        # Fast fallback approximation (1 token ~= 4 chars)
        return max(1, len(text) // 4)

    def profile_payload(
        self,
        system_prompt: str,
        user_prompt: str,
        max_expected_output: int,
        reasoning_budget_tokens: int = 0
    ) -> Dict[str, Any]:
        system_tokens = self._count_tokens(system_prompt)
        user_tokens = self._count_tokens(user_prompt)
        total_input_tokens = system_tokens + user_tokens

        # For reasoning models (o3-mini, Claude 3.7 extended thinking), reasoning tokens count towards output billing
        total_output_tokens = max_expected_output + (reasoning_budget_tokens if self.config["is_reasoning"] else 0)

        # Financial modeling
        input_cost = (total_input_tokens / 1_000_000.0) * self.config["input_per_m"]
        max_output_cost = (total_output_tokens / 1_000_000.0) * self.config["output_per_m"]

        # Latency forecasting (empirical hardware baseline)
        estimated_ttft_ms = 220 + (total_input_tokens * 0.06)
        estimated_decode_ms = total_output_tokens * 14.0  # ~71 tokens/sec

        return {
            "model": self.model_key,
            "encoding": self.config["encoding"],
            "is_reasoning_model": self.config["is_reasoning"],
            "exact_bpe_active": HAS_TIKTOKEN,
            "system_tokens": system_tokens,
            "user_tokens": user_tokens,
            "total_input_tokens": total_input_tokens,
            "reasoning_budget_tokens": reasoning_budget_tokens,
            "max_expected_output_tokens": max_expected_output,
            "total_billable_output_tokens": total_output_tokens,
            "estimated_cost_usd": {
                "input": round(input_cost, 6),
                "max_output": round(max_output_cost, 6),
                "total_worst_case": round(input_cost + max_output_cost, 6)
            },
            "latency_forecast_ms": {
                "estimated_ttft": round(estimated_ttft_ms, 1),
                "estimated_decode": round(estimated_decode_ms, 1),
                "total_estimated_turn_time": round(estimated_ttft_ms + estimated_decode_ms, 1)
            }
        }

if __name__ == "__main__":
    import json
    profiler = ProductionTokenProfiler("claude-3-7-sonnet")
    sys_prompt = "You are an enterprise financial auditor. Adhere to strict GAAP compliance." * 20
    user_query = "Analyze the attached corporate filing for anomalies in Q3 EBITDA." * 5
    report = profiler.profile_payload(
        sys_prompt,
        user_query,
        max_expected_output=1500,
        reasoning_budget_tokens=2048
    )
    print(json.dumps(report, indent=2))
