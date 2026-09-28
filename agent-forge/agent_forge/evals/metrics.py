"""
Platform and Quality Metrics for AgentForge Evals.
"""

from typing import List, Dict, Any
from pydantic import BaseModel

class QualityScorecard(BaseModel):
    task_success: bool
    trajectory_score: float
    groundedness_score: float
    total_tokens: int
    total_cost_usd: float
    total_duration_ms: float
    all_passed: bool

    def summary(self) -> str:
        status_icon = "✅ PASSED" if self.all_passed else "❌ FAILED"
        return (
            f"\n📊 EVALUATION SCORECARD: {status_icon}\n"
            f"  • Task Success: {'Yes' if self.task_success else 'No'}\n"
            f"  • Trajectory Score: {self.trajectory_score * 100:.1f}%\n"
            f"  • Groundedness Score: {self.groundedness_score * 100:.1f}%\n"
            f"  • Total Tokens: {self.total_tokens:,}\n"
            f"  • Total Incurred Cost: ${self.total_cost_usd:.6f}\n"
            f"  • Execution Duration: {self.total_duration_ms:.1f}ms\n"
        )
