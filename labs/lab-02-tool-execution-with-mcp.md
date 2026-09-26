# Lab 2: Tool Execution with MCP

[🔙 Back to Module 03: Tools & MCP](../03-tools-and-model-context-protocol/README.md)

## Objective
Build a standards-compliant Model Context Protocol (MCP) server and client implementing structured tool execution.

## Architectural Requirements
1. Implement an MCP server exposing three tools:
   - `read_query_database`: Executes read-only SQL queries against a sample database.
   - `fetch_api_data`: Makes validated HTTP GET requests to an external service.
   - `write_file_sandbox`: Writes output to an isolated, sandboxed directory.
2. Define strict JSON Schemas for all input arguments.
3. Implement an MCP client that handles JSON-RPC 2.0 communication over `stdio`.
4. Add input validation logic that rejects unsafe SQL statements (e.g., `DROP`, `DELETE`, `UPDATE`).

## Verification Criteria
Client correctly discovers tools, executes read-only operations, and rejects mutation attempts.
