# Phase 03 Examples: Tools & Model Context Protocol (MCP)

Production reference implementations demonstrating Model Context Protocol (MCP) servers, defensive tool sandboxing, and Semantic Kernel auto-invocation filters.

## Files

| File | Language | Purpose | Key Patterns |
|---|---|---|---|
| [`mcp_database_server.py`](./mcp_database_server.py) | Python 3.11+ | FastMCP Safe Database Server | Read-only connection pooling, AST query validation via SQLGlot, bounded pagination |
| [`SemanticKernelTools.cs`](./SemanticKernelTools.cs) | C# / .NET 9 | SK Enterprise Tool Execution | `[KernelFunction]` annotations, `IFunctionInvocationFilter` audit logging, approval gates |
