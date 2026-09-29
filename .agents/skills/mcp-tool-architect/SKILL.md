---
name: mcp-tool-architect
description: >-
  Specialized skill for designing, scaffolding, validating, and testing Model
  Context Protocol (MCP) servers and clients. Use when building tools, JSON-RPC
  schemas, stdio/SSE transports, or integrating MCP into agent runtimes.
---

# 🔌 MCP Tool Architect Skill

Use this skill when scaffolding new Model Context Protocol (MCP) servers, integrating third-party MCP endpoints, or implementing security policies.

## 📐 Wire Protocol Specifications

MCP communicates using **JSON-RPC 2.0**.
Common protocol requests:
- `tools/list`: Discovers available tools, their descriptions, and JSON Schema definitions.
- `tools/call`: Invokes a specific tool with arguments.
- `resources/list` & `resources/read`: Reads context resources (files, tables, API responses).
- `prompts/list` & `prompts/get`: Provides pre-defined system prompts and context templates.

## 🛠️ Step-by-Step MCP Server Construction

1. **Inherit Base MCP Server**:
   Inspect `agent-forge/agent_forge/mcp/servers/payment_server.py` as an architectural reference.
2. **Define Tools**:
   ```python
   from agent_forge.mcp.protocol import MCPToolDefinition

   tool = MCPToolDefinition(
       name="query_knowledge_base",
       description="Retrieves approved enterprise documentation.",
       input_schema={
           "type": "object",
           "properties": {
               "query": {"type": "string", "description": "The search query"}
           },
           "required": ["query"]
       }
   )
   ```
3. **Bind Policy Engine**:
   Always route execution through `PolicyEngine.evaluate(tenant_id, user_id, tool_name, arguments)` to prevent privilege escalation.
4. **Idempotency**:
   For tools that mutate state (e.g. database updates, charges, refunds), accept an `_idempotency_key` and cache execution results.
5. **Testing**:
   Verify tool discovery and execution via `python scripts/verify_lab.py --lab 2`.
