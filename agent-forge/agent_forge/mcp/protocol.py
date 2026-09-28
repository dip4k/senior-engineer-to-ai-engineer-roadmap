"""
Model Context Protocol (MCP 2026) JSON-RPC 2.0 wire protocol simulation.
Supports tools/list, tools/call, and stateless execution semantics.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import uuid

class JSONRPCRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    method: str
    params: Dict[str, Any] = Field(default_factory=dict)

class JSONRPCResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

class MCPToolDefinition(BaseModel):
    name: str
    description: str
    inputSchema: Dict[str, Any]

class MCPClient:
    """
    Client connecting the Agent Orchestrator to distributed MCP Servers.
    """
    def __init__(self):
        self._servers: Dict[str, Any] = {}
        self._tool_to_server: Dict[str, str] = {}

    def register_server(self, server_name: str, server_instance: Any) -> None:
        self._servers[server_name] = server_instance
        for tool in server_instance.list_tools():
            self._tool_to_server[tool.name] = server_name

    def get_tools_schema(self) -> List[Dict[str, Any]]:
        schemas = []
        for server in self._servers.values():
            for tool in server.list_tools():
                schemas.append({
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                })
        return schemas

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        server_name = self._tool_to_server.get(tool_name)
        if not server_name:
            from ..runtime.state_models import ToolResult
            return ToolResult(
                tool_call_id=arguments.get("_call_id", "unknown"),
                name=tool_name,
                content=f"Error: Tool '{tool_name}' not found on any registered MCP server.",
                is_error=True
            )

        server = self._servers[server_name]
        return server.call_tool(tool_name, arguments)
