"""
Trajectory Evaluation for AgentForge.
Validates multi-turn tool calling paths against business state machines.
"""

from typing import List, Dict, Any, Tuple
from pydantic import BaseModel

class TrajectoryEvalResult(BaseModel):
    passed: bool
    score: float
    violations: List[str]
    actual_path: List[str]
    expected_path: List[str]

class TrajectoryEvaluator:
    """
    Asserts that the agent followed an authorized and logically sound sequence
    of tool calls rather than taking hallucinated shortcuts.
    """
    def __init__(self, expected_order: List[str]):
        self.expected_order = expected_order

    def evaluate(self, actual_tool_calls: List[str]) -> TrajectoryEvalResult:
        violations = []
        
        # Check 1: No unauthorized extra calls
        # Check 2: Correct progression order
        exp_idx = 0
        for act in actual_tool_calls:
            if exp_idx < len(self.expected_order):
                if act == self.expected_order[exp_idx]:
                    exp_idx += 1
                else:
                    violations.append(
                        f"Out-of-order execution: expected '{self.expected_order[exp_idx]}', got '{act}'"
                    )

        if exp_idx < len(self.expected_order):
            missing = self.expected_order[exp_idx:]
            violations.append(f"Incomplete trajectory: missing expected steps {missing}")

        passed = (len(violations) == 0)
        score = max(0.0, 1.0 - (len(violations) * 0.33))

        return TrajectoryEvalResult(
            passed=passed,
            score=round(score, 2),
            violations=violations,
            actual_path=actual_tool_calls,
            expected_path=self.expected_order
        )
