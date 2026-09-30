# Lesson 03: Model Context Protocol (MCP) Server Primitives: Tools, Resources, Prompts & Elicitation

> **Tier**: `🟡 Engineering Depth`  
> **Estimated Reading Time**: 50 minutes  
> **Prerequisites**: [Lesson 02: MCP Architecture, Transports & Lifecycle](02-mcp-architecture-transports-and-lifecycle.md)  
> **Target Audience**: Senior Software Engineers, Systems Architects  
> 
> **Core Concept**: An MCP server exposes distinct types of capabilities to AI applications: **Tools** (executable actions that query or mutate state), **Resources** (passive, read-only data attached via URI schemas), **Prompts** (reusable prompt templates for user workflows), and **Elicitation** (pausing execution to request missing parameters or human confirmation). Think of it like a REST API: tools are POST/PUT mutations, resources are GET queries, and prompts are dynamic request templates.
> 
> **Term Ledger**:
> - `New AI terms introduced`: `MCP Tool`, `MCP Resource`, `MCP Prompt`, `Elicitation`, `Resource URI`.
> - `AI terms assumed from earlier lessons`: `MCP Host`, `MCP Client`, `MCP Server`, `JSON-RPC 2.0`.

---

## 1. Conceptual Foundation & Mental Model

In classic web and API development, architectures separate concerns into distinct abstractions:
- **HTTP POST / RPC**: For executing stateful actions (mutations).
- **HTTP GET / REST**: For fetching passive representations of state (queries).
- **Templates / Views**: For structuring dynamic user presentation (rendering).
- **OAuth / Webhooks**: For delegating authentication and human step-up authorization.

The Model Context Protocol (MCP) organizes capabilities into **Foundational Primitives**:

```text
+-----------------------------------------------------------------------------------------+
|                                 The Core MCP Primitives                                 |
+-----------------------------------------------------------------------------------------+
| 1. TOOLS       | Active Execution | Model-initiated actions and database mutations      |
| 2. RESOURCES   | Passive Context  | Host-attached documents, URI schemas, and live feeds|
| 3. PROMPTS     | Reusable Logic   | Parameterized workflow templates for user/host UIs  |
| 4. ELICITATION | Human-in-the-Loop| Server pauses to request user input or auth approval|
+-----------------------------------------------------------------------------------------+
```

Understanding when to expose a capability as a **Tool** versus a **Resource** or **Prompt** is the hallmark of senior AI systems architecture. Exposing everything as a Tool wastes model tokens and introduces severe operational risk.

> **Where this analogy breaks**: In standard REST APIs, the client knows the exact HTTP method and URL paths ahead of time. In an MCP system, the foundation model decides whether and when to call a Tool based on statistical token prediction and semantic descriptions. Furthermore, Resources can be dynamically subscribed to for push notifications, unlike traditional pull-only REST GET requests.

---

## 2. Architecture & Wire Specifications of the 5 Primitives

The following sequence traces how an enterprise Host negotiates each primitive with an MCP Server:

```mermaid
sequenceDiagram
    autonumber
    participant Host as 💻 Host Application (Client)
    participant Server as ⚡ MCP Server
    actor User as 👤 Human Operator

    Note over Host,Server: 1. Passive Context: Resources
    Host->>Server: JSON-RPC resources/read (uri: "schema://enterprise/catalog")
    Server-->>Host: Resource contents (Markdown Table of DDL)
    
    Note over Host,Server: 2. Reusable Templates: Prompts
    Host->>Server: JSON-RPC prompts/get (name: "optimize_slow_query", arguments: {...})
    Server-->>Host: Prompt messages array injected into UI
    
    Note over Host,Server: 3. Active Execution: Tools
    Host->>Server: JSON-RPC tools/call (name: "execute_query", arguments: {...})
    
    Note over Host,Server: 4. Human-in-the-Loop: Elicitation (v2026 Spec)
    alt High Risk Mutation Requires Approval
        Server->>Host: JSON-RPC elicitation/request (mode: "form", schema: {...})
        Host->>User: Renders UI Modal: "Confirm table drop for customer_staging?"
        User-->>Host: Submits signed approval
        Host-->>Server: JSON-RPC elicitation/response (status: "APPROVED")
    end
    
    Note over Host,Server: 5. Reverse Reasoning: Sampling
    alt Server Requires Intermediate Model Completion
        Server->>Host: JSON-RPC sampling/createMessage (messages: [...])
        Host-->>Server: Model response text (mediated without exposing API key)
    end
    
    Server-->>Host: Final tools/call result { content: [...], isError: false }
```

### Prose Walkthrough
1. **Passive Context via Resources (Lines 1–2)**: The host reads dynamic system state (such as database schemas) into the context window *before* the model runs, avoiding expensive exploratory tool calls.
2. **Prompts Primitive (Lines 3–4)**: The server exposes curated prompt recipes. When a user selects a prompt in Cursor or Claude Desktop, the server populates system and user messages deterministically.
3. **Tools Primitive (Line 5)**: The model issues an active mutation or query command over JSON-RPC.
4. **Elicitation Gate (Lines 6–9)**: If the requested tool action is destructive or requires credentials, the server initiates an `elicitation/request`. The host presents a modal dialog to the user. Only when the human authorizes it does execution proceed.
5. **Sampling Primitive (Lines 10–11)**: If the server needs an LLM to summarize a text fragment, it asks the Host to run an inference step via `sampling/createMessage`, shielding proprietary API keys from the server.
6. **Result Payload (Line 12)**: The server completes execution and returns a structured result envelope.

---

## 3. Deep Dive into the 5 MCP Primitives

### Primitive 1: Tools (`tools/list` & `tools/call`)
Tools represent callable functions that produce side effects or fetch computed results.
* **Discovery (`tools/list`)**: Returns an array of tool objects with a `name`, `description`, and `inputSchema` compliant with JSON Schema Draft 2020-12.
* **Invocation (`tools/call`)**: Requires `name` and an `arguments` map.
* **Error Semantics**: If a tool fails (e.g., SQL syntax error or connection timeout), the server **must not** return a top-level JSON-RPC protocol error (`-32603`) if the tool executed. Instead, it must return a valid result object with `"isError": true`:
  ```json
  {
    "jsonrpc": "2.0",
    "id": 42,
    "result": {
      "content": [
        {
          "type": "text",
          "text": "DATABASE_ERROR: Column 'created_at' does not exist in table 'users'."
        }
      ],
      "isError": true
    }
  }
  ```
  This distinction allows the model to inspect the error text and self-correct on its next turn.

### Primitive 2: Resources (`resources/list` & `resources/read`)
Resources provide passive data context to the model, analogous to reading a file or GET-ing a REST endpoint.
* **URI Identification**: Every resource is addressed via a unique URI scheme (`postgres://customers/schema`, `file:///logs/app.log`, `git://repo/commit/head`).
* **MIME Types**: Resources declare content formats (`application/json`, `text/markdown`, `text/plain`).
* **Live Subscriptions**: Clients can subscribe to dynamic resources via `resources/subscribe`. When the underlying asset changes, the server fires a `notifications/resources/updated` event.

### Primitive 3: Prompts (`prompts/list` & `prompts/get`)
Prompts allow MCP servers to expose pre-engineered prompt workflows directly into the Host's UI or slash-command menu (e.g., `/optimize-sql`, `/triage-incident`).
* **Dynamic Arguments**: Prompts declare required input arguments (e.g., `table_name`, `severity_level`).
* **Message Templates**: Calling `prompts/get` returns an array of structured prompt messages (`role: "user" | "assistant"`) ready for direct inclusion in the LLM's conversation history.

### Primitive 4: Sampling (`sampling/createMessage`)
Historically, if a tool needed an LLM completion (e.g., to generate an embedding or extract entities from an unstructured PDF), the tool developer had to hardcode an API key into the tool service. This presented immense security risks:
- API keys leaked into logs or environment variables.
- The host application lost visibility into nested LLM token spending.

With **Sampling**, the server asks the **Host** to generate an LLM completion on its behalf:
- The server sends `sampling/createMessage` with messages, max tokens, and temperature.
- The Host reviews the request, verifies token quotas, applies its own security guardrails, invokes its primary foundation model, and returns the generated text to the server.
- **Zero API credentials exist inside the MCP server process.**

### Primitive 5: Elicitation (`elicitation/request`) (v2025/2026 HITL Standard)
Standardized in the **v2026-07-28 specification**, Elicitation is the formal protocol primitive for **Human-in-the-Loop (HITL)** interaction. It transforms AI execution from an unmonitored script into a governed, interactive collaboration.

Elicitation supports two primary interaction modes:
1. **Form Mode (`mode: "form"`)**: The server passes a JSON Schema describing required input or confirmation fields. The host client renders an in-app form (e.g., confirmation checkbox, date picker, or budget ceiling selector).
2. **URL Mode (`mode: "url"`)**: The server returns a secure external URL. The client opens a secure browser window for interactions that must bypass model context completely (e.g., OAuth 2.0 step-up consent, SSO login, banking 2FA).

```json
// Example: Server initiates Form Mode Elicitation
{
  "jsonrpc": "2.0",
  "id": "elicit-01",
  "method": "elicitation/request",
  "params": {
    "mode": "form",
    "title": "Production Service Restart Authorization",
    "description": "An agent has requested an automated restart of the Payment Gateway service.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "authorized_by": { "type": "string", "description": "Operator employee ID" },
        "confirm_service_drop": { "type": "boolean", "const": true }
      },
      "required": ["authorized_by", "confirm_service_drop"]
    }
  }
}
```

---

## 4. Multi-Language SDK Implementations

### 1. Python Implementation: MCP Primitive Dispatcher

In production Python, MCP servers can be authored using the standard library with Pydantic v2, or using higher-level frameworks like `fastmcp`. Below is a self-contained, typed implementation demonstrating the 3 core server primitives running offline:

```python
"""
enterprise_mcp_server.py
Production Python MCP Server exposing Tools, Resources, and Prompts.
Implements the 3 core primitives using pure Python 3.12+ and Pydantic v2.
"""

from typing import Any, Callable, Dict
import json
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# 1. MCP Resource: Passive Catalog Context
# ---------------------------------------------------------------------------

class ResourceDefinition(BaseModel):
    uri: str
    name: str
    description: str
    mime_type: str = "text/plain"


# ---------------------------------------------------------------------------
# 2. MCP Tool: Active Query Execution with Typed Schemas
# ---------------------------------------------------------------------------

class SpendQueryRequest(BaseModel):
    service_name: str = Field(description="Cloud service name, e.g., 'EC2', 'BigQuery'")
    days: int = Field(default=7, ge=1, le=90, description="Historical query window in days")


# ---------------------------------------------------------------------------
# 3. Pure Python 3.12+ MCP Primitive Dispatcher
# ---------------------------------------------------------------------------

class McpPrimitiveServer:
    def __init__(self, name: str, version: str) -> None:
        self.name = name
        self.version = version
        self._resources: Dict[str, tuple[ResourceDefinition, Callable[[], str]]] = {}
        self._tools: Dict[str, tuple[type[BaseModel], Callable[..., Any]]] = {}
        self._prompts: Dict[str, str] = {}

    def register_resource(self, uri: str, name: str, description: str, handler: Callable[[], str]) -> None:
        defn = ResourceDefinition(uri=uri, name=name, description=description)
        self._resources[uri] = (defn, handler)

    def register_tool(self, name: str, schema: type[BaseModel], handler: Callable[..., Any]) -> None:
        self._tools[name] = (schema, handler)

    def register_prompt(self, name: str, template: str) -> None:
        self._prompts[name] = template

    def handle_read_resource(self, uri: str) -> Dict[str, Any]:
        if uri not in self._resources:
            return {"isError": True, "content": f"Resource not found: {uri}"}
        defn, handler = self._resources[uri]
        return {
            "contents": [{"uri": uri, "mimeType": defn.mime_type, "text": handler()}],
            "isError": False
        }

    def handle_call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self._tools:
            return {"isError": True, "content": f"Unknown tool: {name}"}
        schema, handler = self._tools[name]
        validated = schema.model_validate(arguments)
        result = handler(validated)
        return {"content": [{"type": "text", "text": json.dumps(result)}], "isError": False}


# ---------------------------------------------------------------------------
# 4. Usage Demonstration
# ---------------------------------------------------------------------------

server = McpPrimitiveServer("FinOpsServer", "2.0.0")

# Register Resource
server.register_resource(
    uri="schema://finops/catalog",
    name="FinOps Catalog",
    description="Schema of cloud billing tables",
    handler=lambda: "cloud_spend(timestamp, service, cost_usd)"
)

# Register Tool
def execute_spend_query(req: SpendQueryRequest) -> Dict[str, Any]:
    return {"service": req.service_name, "spend_usd": 1420.50, "status": "OK"}

server.register_tool("query_cloud_spend", SpendQueryRequest, execute_spend_query)

# Register Prompt
server.register_prompt(
    "budget_anomaly_triage",
    "You are a FinOps Architect. Query cloud spend and propose remediations."
)

# Test invocations offline
res = server.handle_read_resource("schema://finops/catalog")
call = server.handle_call_tool("query_cloud_spend", {"service_name": "BigQuery", "days": 14})
print(f"Resource Loaded: {not res['isError']}")
print(f"Tool Result: {call['content'][0]['text']}")
```

---

### 2. TypeScript SDK: `@modelcontextprotocol/sdk`

The official TypeScript SDK provides end-to-end type safety using [Zod](https://zod.dev/):

```typescript
// server.ts
// Production TypeScript MCP Server using @modelcontextprotocol/sdk
// Install: npm install @modelcontextprotocol/sdk zod

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "enterprise-audit-server",
  version: "1.0.0",
});

// Expose a typed Tool with Zod validation
server.registerTool(
  "query-audit-log",
  {
    description: "Fetches security audit events for a target principal.",
    inputSchema: z.object({
      principalId: z.string().regex(/^usr_[a-zA-Z0-9]+$/),
      maxEvents: z.number().int().min(1).max(100).default(20),
    }),
  },
  async ({ principalId, maxEvents }) => {
    // Simulated database query
    const events = [
      { event: "LOGIN_SUCCESS", ip: "192.168.1.10", timestamp: "2026-03-29T12:00:00Z" }
    ];
    return {
      content: [{ type: "text", text: JSON.stringify(events) }],
    };
  }
);

// Connect over local stdio
const transport = new StdioServerTransport();
await server.connect(transport);
```

---

### 3. C# / .NET 9: Microsoft Semantic Kernel Plugin Architecture

In .NET 9 enterprise architectures, tools are exposed through Semantic Kernel plugins:

```csharp
// TelemetryPlugin.cs
// Production C# .NET 9 Function Calling Plugin
using System.ComponentModel;
using System.Text.Json;
using Microsoft.SemanticKernel;

public sealed class TelemetryPlugin
{
    [KernelFunction, Description("Queries health metrics for an enterprise container cluster.")]
    public static string GetClusterHealth(
        [Description("Cluster namespace identifier.")] string clusterNamespace,
        [Description("Include pod logs if unhealthy.")] bool includeDiagnostics = false)
    {
        var healthReport = new
        {
            Namespace = clusterNamespace,
            Status = "HEALTHY",
            ActiveNodes = 12,
            CpuSaturation = 0.64
        };
        return JsonSerializer.Serialize(healthReport);
    }
}
```

---

### 4. Meta Llama Stack: MCP Tool Engine Provider

In the open-weights ecosystem, Meta Llama Stack provides first-class support for the Model Context Protocol, enabling Llama 3.1 and 3.3 models to consume standard MCP servers as dynamic tool providers. Below is a typed Pydantic v2 configuration model validating an MCP tool group registration:

```python
"""
llama_stack_mcp_config.py
Configuring an MCP Server endpoint using Pydantic v2 schemas.
Compatible with Meta Llama Stack tool group declarations.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field


class McpEndpointConfig(BaseModel):
    uri: str
    protocol_version: str = "2026-07-28"


class ToolGroupRegistration(BaseModel):
    toolgroup_id: str
    provider_id: str = "model-context-protocol"
    mcp_endpoint: McpEndpointConfig
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Verify configuration schema offline
config = ToolGroupRegistration(
    toolgroup_id="enterprise::observability_mcp",
    mcp_endpoint=McpEndpointConfig(uri="http://localhost:8080/mcp")
)
print(f"Registered ToolGroup: {config.toolgroup_id} for MCP URI: {config.mcp_endpoint.uri}")
```

---

## 5. Systems Failure Modes & Anti-Patterns

### Failure Mode 1: Tool Overloading (Using Tools Where Resources Belong)
* **Root Cause**: Exposing static documentation, API schemas, or configuration tables as dynamic Tools (`get_table_schema`, `read_config`). The model burns 2–3 reasoning turns calling exploratory tools before attempting the user's primary objective.
* **Production Fix**: Expose static or slowly changing assets as **Resources** (`schema://`, `docs://`). Hosts automatically bind resources into initial context or allow direct retrieval with zero tool-calling latency.

### Failure Mode 2: Returning Unstructured String Errors
* **Root Cause**: When a tool fails, returning a raw Python stack trace as plain text. The model cannot determine whether the database query succeeded with no rows or crashed, leading to hallucinated recovery attempts.
* **Production Fix**: Always format error results with `"isError": true` and a structured error prefix:
  ```json
  { "content": [{ "type": "text", "text": "ERROR_AUTH: Token expired." }], "isError": true }
  ```

### Failure Mode 3: Silent Side Effects without Elicitation
* **Root Cause**: Providing an agent with unrestricted mutating tools (`delete_staging_database`, `revoke_all_tokens`) without an approval step. A prompt injection in untrusted input executes the mutation immediately.
* **Production Fix**: Gate all state-changing or destructive tools with **Elicitation (Form Mode)** or an ephemeral cryptographic HMAC step-up approval token.

---

## 6. Architectural Trade-off Matrix: Primitive Selection

| Primitive | Primary Purpose | State Mutation | Token Cost Model | Host UI Presentation |
|---|---|:---:|---|---|
| **Tool** | Dynamic computation or side-effect execution | Permitted (Should be audited/gated) | Incurred per invocation (arguments + result payload) | Rendered as tool call / execution badge |
| **Resource** | Passive context ingestion (Schemas, DDL, files) | Strictly Read-Only | Fixed cost incurred when resource is loaded | Rendered as document preview / context chip |
| **Prompt** | Reusable parameterized workflow injection | None (Template only) | Zero until rendered into conversation history | Rendered as slash-command / dropdown recipe |
| **Sampling** | Host-mediated LLM completion for servers | None | Consumes Host's model quota (Zero server API key) | Internal background execution |
| **Elicitation** | Human-in-the-Loop approval & missing inputs | Intercepts mutations | Minimal (JSON Schema form definition) | Rendered as interactive modal dialog |

---

## 7. Hands-On Lab Exercise

### Objective
Build a multi-primitive MCP server in Python or TypeScript that exposes a database schema as a Resource, a read query as a Tool, and gates service restarts behind an Elicitation form.

### Acceptance Criteria
1. Expose `schema://inventory/database` returning a Markdown table of database columns.
2. Expose a tool `get_inventory_levels(sku: str)` validating that SKU matches `^SKU-[0-9]{5}$`.
3. If an invalid SKU is supplied, return `isError: true` with an explanatory diagnostic message.
4. Expose a parameterized prompt `triage_inventory_shortage(sku: str, threshold: int)` returning an expert triage instruction.

---

## 8. Enterprise Production Checklist

- [ ] Static schemas and catalogs are exposed as **Resources**, reserving **Tools** strictly for computations and mutations.
- [ ] Tool error responses return `"isError": true` inside the result envelope rather than crashing the JSON-RPC pipe.
- [ ] Server-initiated LLM reasoning uses the **Sampling** primitive to avoid embedding API keys in tool services.
- [ ] Mutating or destructive operations enforce Human-in-the-Loop verification via **Elicitation**.
- [ ] All tool schemas declare `"additionalProperties": false` and use strict regex patterns or enums for discrete parameters.

---

## 9. Quick Check

A software architect wants an AI coding assistant to be aware of a team's 50-page coding standards document. The engineer suggests adding a tool called `get_coding_standard(rule_name: str)`. Why is this an anti-pattern under MCP design guidelines, and which primitive should be used instead?

<details>
<summary>Suggested Answer</summary>

**Why it is an anti-pattern**: Using a Tool for static documentation forces the model to perform active reasoning turns, emits tool calls, and incurs network roundtrips just to read static rules. If the model does not know what rule name to search for, it either guesses or skips checking entirely.

**Correct Primitive**: Use an **MCP Resource** (such as `docs://engineering/standards/python`). Resources are designed for passive context ingestion. The host application can inspect the resource catalog, bind the document into the context window at session start, or attach it when relevant, with zero tool-calling turns.

</details>

---

## 🧭 Navigation

| Previous | Hub | Next | Capstone Lab |
|---|---|---|---|
| [← Lesson 02: MCP Architecture & Transports](02-mcp-architecture-transports-and-lifecycle.md) | [Phase 03 Overview](README.md) | [Lesson 04: Host Orchestration & Governors →](04-reverse-sampling-and-host-orchestration.md) | [Capstone Lab: MCP Tool Server →](labs/capstone-mcp-tool-server.md) |
