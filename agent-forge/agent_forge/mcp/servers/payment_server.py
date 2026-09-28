"""
Payment MCP Server for AgentForge.
Exposes payment transaction inspection and refund execution with idempotency guarantees.
"""

from typing import Dict, Any, List
import json
import uuid
from ..protocol import MCPToolDefinition
from ...runtime.state_models import ToolResult

class PaymentMCPServer:
    def __init__(self):
        # Simulated database of transactions (showing a duplicate charge on order 9182)
        self._transactions_db = {
            "9182": [
                {
                    "transaction_id": "tx_9182_a",
                    "order_id": "9182",
                    "amount": 49.00,
                    "status": "Captured",
                    "timestamp": "2026-09-20T10:14:02Z",
                    "gateway": "Stripe"
                },
                {
                    "transaction_id": "tx_9182_b",
                    "order_id": "9182",
                    "amount": 49.00,
                    "status": "Captured",
                    "timestamp": "2026-09-20T10:14:05Z",
                    "gateway": "Stripe"
                }
            ]
        }
        # Idempotency storage: idempotency_key -> refund_record
        self._idempotency_records: Dict[str, Dict[str, Any]] = {}

    def list_tools(self) -> List[MCPToolDefinition]:
        return [
            MCPToolDefinition(
                name="payment_get_transactions",
                description="Fetches payment charge transactions associated with an order ID.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string", "description": "The unique order identifier"}
                    },
                    "required": ["order_id"]
                }
            ),
            MCPToolDefinition(
                name="payment_issue_refund",
                description="Issues a monetary refund for a specific transaction ID.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "transaction_id": {"type": "string", "description": "The charge transaction ID to refund"},
                        "amount": {"type": "number", "description": "The refund amount in USD"},
                        "reason": {"type": "string", "description": "Reason for the refund"}
                    },
                    "required": ["transaction_id", "amount"]
                }
            )
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> ToolResult:
        if name == "payment_get_transactions":
            order_id = arguments.get("order_id", "").strip()
            txs = self._transactions_db.get(order_id, [])
            return ToolResult(
                tool_call_id=arguments.get("_call_id", ""),
                name=name,
                content=json.dumps({"order_id": order_id, "transactions_found": len(txs), "transactions": txs})
            )

        if name == "payment_issue_refund":
            tx_id = arguments.get("transaction_id", "").strip()
            amount = float(arguments.get("amount", 0.0))
            reason = arguments.get("reason", "Customer request")
            idempotency_key = arguments.get("_idempotency_key")

            # Check Idempotency Cache
            if idempotency_key and idempotency_key in self._idempotency_records:
                cached_refund = self._idempotency_records[idempotency_key]
                return ToolResult(
                    tool_call_id=arguments.get("_call_id", ""),
                    name=name,
                    content=json.dumps({
                        "status": "SUCCESS (IDEMPOTENT REPLAY)",
                        "message": "Refund already processed previously for this key.",
                        "refund_details": cached_refund
                    })
                )

            # Process new refund
            refund_id = f"ref_{uuid.uuid4().hex[:8]}"
            refund_record = {
                "refund_id": refund_id,
                "transaction_id": tx_id,
                "amount_refunded": amount,
                "reason": reason,
                "status": "Completed",
                "processed_at": "2026-09-28T12:00:00Z"
            }

            if idempotency_key:
                self._idempotency_records[idempotency_key] = refund_record

            return ToolResult(
                tool_call_id=arguments.get("_call_id", ""),
                name=name,
                content=json.dumps({
                    "status": "SUCCESS",
                    "message": f"Successfully refunded ${amount:.2f} for transaction {tx_id}.",
                    "refund_details": refund_record
                })
            )

        return ToolResult(
            tool_call_id=arguments.get("_call_id", ""),
            name=name,
            content=f"Unknown tool: {name}",
            is_error=True
        )
