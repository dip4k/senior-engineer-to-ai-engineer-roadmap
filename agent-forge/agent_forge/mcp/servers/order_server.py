"""
Order MCP Server for AgentForge.
Exposes order lookup and item verification tools.
"""

from typing import Dict, Any, List
import json
from ..protocol import MCPToolDefinition
from ...runtime.state_models import ToolResult

class OrderMCPServer:
    def __init__(self):
        # Simulated database of orders
        self._orders_db = {
            "9182": {
                "order_id": "9182",
                "customer_id": "cust_481",
                "status": "Delivered",
                "created_at": "2026-09-20T10:14:00Z",
                "items": [
                    {"sku": "KEYBOARD-RGB-PRO", "name": "Mechanical Keyboard", "price": 49.00, "qty": 1}
                ],
                "total_amount": 49.00
            }
        }

    def list_tools(self) -> List[MCPToolDefinition]:
        return [
            MCPToolDefinition(
                name="order_get_order",
                description="Retrieves full details for an e-commerce order by order ID.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string", "description": "The unique order identifier"}
                    },
                    "required": ["order_id"]
                }
            )
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> ToolResult:
        if name == "order_get_order":
            order_id = arguments.get("order_id", "").strip()
            order = self._orders_db.get(order_id)
            if not order:
                return ToolResult(
                    tool_call_id=arguments.get("_call_id", ""),
                    name=name,
                    content=json.dumps({"error": f"Order {order_id} not found."}),
                    is_error=True
                )
            return ToolResult(
                tool_call_id=arguments.get("_call_id", ""),
                name=name,
                content=json.dumps(order)
            )
        
        return ToolResult(
            tool_call_id=arguments.get("_call_id", ""),
            name=name,
            content=f"Unknown tool: {name}",
            is_error=True
        )
