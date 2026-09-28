"""
Policy MCP Server for AgentForge.
Exposes enterprise customer care and dispute policies.
"""

from typing import Dict, Any, List
import json
from ..protocol import MCPToolDefinition
from ...runtime.state_models import ToolResult

class PolicyMCPServer:
    def list_tools(self) -> List[MCPToolDefinition]:
        return [
            MCPToolDefinition(
                name="policy_get_refund_rules",
                description="Fetches customer support guidelines and refund authorization rules for a specific region.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "region": {"type": "string", "description": "The geographical region (e.g., 'US', 'EU')"}
                    },
                    "required": ["region"]
                }
            )
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> ToolResult:
        if name == "policy_get_refund_rules":
            region = arguments.get("region", "US").upper()
            rules = {
                "region": region,
                "duplicate_charge_policy": "Duplicate charges for the identical amount within 10 minutes are auto-refundable if under $100.00.",
                "damaged_goods_policy": "Requires photo verification and manager approval if item value exceeds $50.00.",
                "cancellation_window_hours": 24,
                "auto_approval_limit_usd": 100.00
            }
            return ToolResult(
                tool_call_id=arguments.get("_call_id", ""),
                name=name,
                content=json.dumps(rules)
            )

        return ToolResult(
            tool_call_id=arguments.get("_call_id", ""),
            name=name,
            content=f"Unknown tool: {name}",
            is_error=True
        )
