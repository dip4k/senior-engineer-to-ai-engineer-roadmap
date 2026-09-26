"""
pydantic_ai_agent.py
Production-grade type-safe agent using PydanticAI with dependency injection,
strict structured outputs, and defensive tool boundaries.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

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
    model="claude-3-7-sonnet-latest",  # Or gpt-4o, gemini-2.0-flash
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
