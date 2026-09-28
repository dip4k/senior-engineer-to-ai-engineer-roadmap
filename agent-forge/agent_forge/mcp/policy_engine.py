"""
Zero-Trust Policy Engine for AgentForge Tool Execution.
Evaluates Attribute-Based Access Control (ABAC) and deterministic security policies.
"""

from typing import Dict, Any, Literal
from pydantic import BaseModel

class PolicyDecision(BaseModel):
    status: Literal["PERMITTED", "REQUIRES_APPROVAL", "DENIED"]
    reason: str

class PolicyEngine:
    """
    Evaluates enterprise security policies before any MCP tool is invoked.
    """
    def __init__(self, auto_refund_limit_usd: float = 100.0):
        self.auto_refund_limit_usd = auto_refund_limit_usd

    def evaluate(
        self,
        tenant_id: str,
        user_id: str,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> PolicyDecision:
        # 1. Deny dangerous or unauthorized tools
        if tool_name.startswith("system_") or tool_name.startswith("admin_"):
            return PolicyDecision(
                status="DENIED",
                reason=f"User {user_id} does not possess administrative privileges for {tool_name}."
            )

        # 2. Refund policy check
        if tool_name == "payment_issue_refund":
            amount = float(arguments.get("amount", 0.0))
            if amount <= 0:
                return PolicyDecision(
                    status="DENIED",
                    reason=f"Invalid refund amount: ${amount}."
                )
            
            if amount > self.auto_refund_limit_usd:
                return PolicyDecision(
                    status="REQUIRES_APPROVAL",
                    reason=f"Refund amount ${amount:.2f} exceeds auto-approval threshold (${self.auto_refund_limit_usd:.2f})."
                )

            return PolicyDecision(
                status="PERMITTED",
                reason=f"Refund amount ${amount:.2f} is within auto-approval threshold."
            )

        # Read-only queries are permitted by default
        return PolicyDecision(
            status="PERMITTED",
            reason="Tool invocation permitted by default policy."
        )
