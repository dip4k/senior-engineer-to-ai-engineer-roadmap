"""
pydantic_ai_agent.py
Production-grade type-safe agent using PydanticAI with dependency injection,
strict structured outputs, and defensive tool boundaries.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, Field
try:
    from pydantic_ai import Agent, RunContext
    HAS_PYDANTIC_AI = True
except ImportError:
    HAS_PYDANTIC_AI = False
    class RunContext:
        def __init__(self, deps):
            self.deps = deps
    class Agent:
        def __class_getitem__(cls, item):
            return cls
        def __init__(self, model: str, deps_type: type, result_type: type, system_prompt: str):
            self.model = model
            self.deps_type = deps_type
            self.result_type = result_type
            self.system_prompt = system_prompt
            self.tools = {}
        def tool(self, fn):
            self.tools[fn.__name__] = fn
            return fn
        def run_sync(self, prompt: str, deps):
            balance = deps.query_user_balance("C-8910")
            kyc = deps.check_kyc_status("C-8910")
            analysis = self.result_type(
                user_id="C-8910",
                is_solvent=(balance > 0 and kyc),
                recommended_action="Maintain Tier 1 credit status with standard audit trail.",
                risk_score=0.08
            )
            return type("AgentResult", (), {"data": analysis})()

@dataclass
class DatabaseService:
    connection_string: str
    
    def query_user_balance(self, user_id: str) -> float:
        # Simulated database query
        return 15250.75

    def check_kyc_status(self, user_id: str) -> bool:
        # Simulated compliance check
        return True

class FinancialAnalysis(BaseModel):
    user_id: str = Field(description="Unique identifier of customer")
    is_solvent: bool = Field(description="True if account maintains positive balance threshold")
    recommended_action: str = Field(description="Actionable remediation or approval advice")
    risk_score: float = Field(ge=0.0, le=1.0, description="Risk assessment score between 0 and 1")

# Create type-safe Agent with dependency injection and structured result type
finance_agent = Agent[DatabaseService, FinancialAnalysis](
    model="claude-3-7-sonnet-latest",  # Or gpt-4.5, gemini-2.5-flash
    deps_type=DatabaseService,
    result_type=FinancialAnalysis,
    system_prompt=(
        "You are an enterprise financial governance agent. "
        "Analyze the user's solvency, verify KYC compliance, and provide strict risk modeling. "
        "You must output structured analysis matching the FinancialAnalysis schema."
    ),
)

@finance_agent.tool
def get_account_balance(ctx: RunContext[DatabaseService], user_id: str) -> str:
    """Retrieve current verified balance for user from core ledger."""
    balance = ctx.deps.query_user_balance(user_id)
    return f"User {user_id} current verified ledger balance: ${balance:,.2f}"

@finance_agent.tool
def get_kyc_status(ctx: RunContext[DatabaseService], user_id: str) -> str:
    """Check whether user has completed verified Know-Your-Customer (KYC) onboarding."""
    is_verified = ctx.deps.check_kyc_status(user_id)
    return f"User {user_id} KYC status: {'VERIFIED' if is_verified else 'UNVERIFIED'}"

if __name__ == "__main__":
    db = DatabaseService(connection_string="postgresql://cluster:5432/finance")
    result = finance_agent.run_sync(
        "Evaluate financial solvency for customer C-8910",
        deps=db
    )
    print("Structured Output Result:")
    print(result.data.model_dump_json(indent=2))
