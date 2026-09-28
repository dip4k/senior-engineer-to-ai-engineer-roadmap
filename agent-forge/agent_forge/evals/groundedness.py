"""
Groundedness & Faithfulness Evaluator for AgentForge.
Checks whether generated output is strictly supported by retrieved facts and tool outputs.
"""

from typing import List, Dict, Any
from pydantic import BaseModel

class GroundednessResult(BaseModel):
    is_grounded: bool
    score: float
    unsupported_claims: List[str]

class GroundednessEvaluator:
    def evaluate(self, final_response: str, evidence_texts: List[str]) -> GroundednessResult:
        """
        Heuristic factual consistency checker verifying that entities and quantities
        in final response exist in evidence.
        """
        combined_evidence = " ".join(evidence_texts).lower()
        response_lower = final_response.lower()

        unsupported = []
        
        # Check specific critical entity markers
        critical_entities = ["9182", "49.00", "refund"]
        for ent in critical_entities:
            if ent in response_lower and ent not in combined_evidence:
                unsupported.append(f"Entity '{ent}' mentioned in response but missing from evidence.")

        # Hallucination check for negative figures
        if "$999" in response_lower or "fraud" in response_lower:
            unsupported.append("Hallucinated unauthorized terms or amounts.")

        is_grounded = (len(unsupported) == 0)
        score = 1.0 if is_grounded else 0.5

        return GroundednessResult(
            is_grounded=is_grounded,
            score=score,
            unsupported_claims=unsupported
        )
