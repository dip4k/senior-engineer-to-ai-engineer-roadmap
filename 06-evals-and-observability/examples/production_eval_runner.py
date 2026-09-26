"""
production_eval_runner.py
Production-grade Level 2 LLM-as-a-Judge evaluation harness with binary rubrics,
Pydantic output parsing, and OpenTelemetry instrumentation via Langfuse.
"""

from __future__ import annotations

import os
import sys
import time
from typing import List, Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from langfuse import Langfuse
from langfuse.openai import openai as instrumented_openai

# Initialize Langfuse client for observability
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY", "sk-lf-test"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
)

# ---------------------------------------------------------------------------
# Structured Models for Binary Rubric
# ---------------------------------------------------------------------------
class BinaryCriterionEvaluation(BaseModel):
    criterion_name: str = Field(..., description="Name of the evaluated criterion")
    reasoning: str = Field(..., description="Step-by-step chain of thought justification")
    passed: bool = Field(..., description="True if criterion is satisfied, False otherwise")

class JudgeEvaluationReport(BaseModel):
    evaluations: List[BinaryCriterionEvaluation] = Field(..., description="List of criterion evaluations")
    overall_score: float = Field(..., ge=0.0, le=1.0, description="Fraction of passed criteria")
    summary: str = Field(..., description="Executive summary of the judge's assessment")

# ---------------------------------------------------------------------------
# Evaluation System Prompts
# ---------------------------------------------------------------------------
JUDGE_SYSTEM_PROMPT = """You are an expert autonomous AI Judge conducting strict technical evaluation.
You grade Candidate Responses based on explicit, discrete BINARY criteria.
Do not use continuous 1-5 scales. Each criterion is strictly 1 (Pass) or 0 (Fail).

Evaluation Protocol:
1. Carefully read the User Query, the Reference Context (Ground Truth), and the Candidate Response.
2. For each criterion, articulate a rigorous step-by-step chain-of-thought analysis in 'reasoning'.
3. Assign 'passed: true' ONLY if the candidate completely satisfies the rule without violation.
4. Calculate the overall_score as the exact ratio of passed criteria over total criteria.
"""

class ProductionEvaluator:
    def __init__(self, judge_model: str = "gpt-4o"):
        self.judge_model = judge_model
        # Use Langfuse-instrumented OpenAI client for automated trace capture
        self.client = instrumented_openai

    def evaluate_response(
        self,
        test_case_id: str,
        user_query: str,
        reference_context: str,
        candidate_response: str,
        rubric_criteria: List[dict]
    ) -> JudgeEvaluationReport:
        """
        Executes a binary rubric evaluation against a candidate response.
        """
        trace = langfuse.trace(
            name="llm_as_a_judge_evaluation",
            user_id="ci_cd_runner",
            metadata={"test_case_id": test_case_id, "judge_model": self.judge_model}
        )

        criteria_formatted = "\n".join(
            [f"- {c['name']}: {c['description']} (FAIL IF: {c['fail_condition']})" 
             for c in rubric_criteria]
        )

        user_content = f"""
### USER QUERY:
{user_query}

### REFERENCE CONTEXT / GROUND TRUTH:
{reference_context}

### CANDIDATE RESPONSE TO GRADE:
{candidate_response}

### BINARY CRITERIA TO ENFORCE:
{criteria_formatted}
"""

        start_time = time.perf_counter()
        
        # Invoke Judge LLM with Pydantic Structured Output constraint
        completion = self.client.beta.chat.completions.parse(
            model=self.judge_model,
            messages=[
                {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            response_format=JudgeEvaluationReport,
            temperature=0.0, # Deterministic zero-temperature for judging
            name="judge_completion"
        )
        
        latency_ms = (time.perf_counter() - start_time) * 1000
        report: JudgeEvaluationReport = completion.choices[0].message.parsed

        # Post evaluation score directly to Langfuse trace
        trace.score(
            name="binary_rubric_accuracy",
            value=report.overall_score,
            comment=report.summary
        )

        trace.update(
            output=report.model_dump(),
            metadata={"latency_ms": latency_ms}
        )

        return report

# ---------------------------------------------------------------------------
# Test Execution Harness
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    evaluator = ProductionEvaluator()

    rubric = [
        {
            "name": "Faithfulness",
            "description": "Every factual statement must be grounded in the reference context.",
            "fail_condition": "Contains claims or figures not present in reference."
        },
        {
            "name": "Tool Schema Precision",
            "description": "Output parameters must match required API signatures.",
            "fail_condition": "Omits mandatory parameters or invents fictitious keys."
        },
        {
            "name": "Conciseness",
            "description": "Direct, zero-fluff answers without repetitive polite filler.",
            "fail_condition": "Exceeds 150 words when under 50 words is sufficient."
        }
    ]

    mock_query = "What is the refund policy for Enterprise Tier subscriptions?"
    mock_context = (
        "Enterprise Tier subscriptions are non-refundable after the initial 14-day evaluation window. "
        "Cancellation requests must be submitted via email to enterprise-support@domain.com."
    )
    mock_candidate = (
        "Hello! I would be delighted to assist you with your question regarding refunds! "
        "According to our official corporate policies, Enterprise Tier subscriptions cannot be refunded "
        "once the initial 14-day evaluation window has elapsed. To cancel, please send an email to "
        "enterprise-support@domain.com. Have a fantastic day!"
    )

    print(f"Executing evaluation for: '{mock_query}'...")
    result = evaluator.evaluate_response(
        test_case_id="TC-REFUND-001",
        user_query=mock_query,
        reference_context=mock_context,
        candidate_response=mock_candidate,
        rubric_criteria=rubric
    )

    print("\n================ EVALUATION REPORT ================")
    print(f"Overall Score: {result.overall_score * 100:.1f}%")
    print(f"Summary: {result.summary}\n")
    for ev in result.evaluations:
        status = "PASSED" if ev.passed else "FAILED"
        print(f"[{status}] {ev.criterion_name}: {ev.reasoning}")
    print("====================================================")
    
    # Flush all traces to Langfuse backend
    langfuse.flush()
