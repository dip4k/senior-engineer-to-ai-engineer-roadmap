# Phase 03: Tools and Model Context Protocol (MCP)

> **Level**: Advanced Systems Engineering  
> **Estimated Duration**: 4.5–5.5 hours  
> **Prerequisites**: Phase 00 (Inference Latency & KV Physics), Phase 01 (Structured Outputs & JSON Schema), Phase 02 (Enterprise Knowledge Systems)  
> **Downstream Dependencies**: Phase 04 (Stateful Agent Orchestration), Phase 05 (AI Security & Firewalls)  

---

## 1. Phase Mission & Mental Model

Foundation models generate text. By themselves, they cannot execute code, query a database, read a file, or restart a server. 

To make models useful in production, we must connect them to external systems. This phase covers how to build those connections safely and reliably using standard protocols.

```text
The AI Systems Stack:
+-------------------------------------------------------------------------------+
| Autonomous Multi-Agent Orchestration (Phase 04)                               |
+-------------------------------------------------------------------------------+
| TOOLS & MODEL CONTEXT PROTOCOL (Phase 03) <=== [YOU ARE HERE]                 |
|  - JSON-RPC 2.0 Wire Protocols & Framing                                      |
|  - MCP Core: Host, Client, Server Topology                                    |
|  - 5 Primitives: Tools, Resources, Prompts, Sampling, Elicitation              |
|  - Transports: Local standard I/O (stdio) vs HTTP                              |
|  - Sandboxing: Abstract Syntax Tree (AST) validation and MicroVMs              |
|  - Enterprise Bridges: OAuth, identity propagation, and legacy integrations    |
+-------------------------------------------------------------------------------+
| Enterprise Knowledge Systems & RAG (Phase 02)                                 |
+-------------------------------------------------------------------------------+
| Context Engineering & Structured Outputs (Phase 01)                           |
+-------------------------------------------------------------------------------+
| Foundations & Token Mechanics (Phase 00)                                      |
+-------------------------------------------------------------------------------+
```

You will learn how to connect foundation models to deterministic systems of record through standardized wire protocols, execution limits, and defense-in-depth security.

---

## 2. Modular Curriculum Directory

Phase 03 is structured into six self-contained, progressively sequenced lessons:

| Lesson | Title | Tier Badge | Est. Time | Core Systems Concepts |
|:---:|---|:---:|:---:|---|
| **01** | [Function Calling & JSON-RPC Wire Protocols](./01-function-calling-and-json-rpc-wire-protocols.md) | `HIGH ROI / CORE` | 40 min | Function calling mechanics; JSON-RPC 2.0; tool schemas; constrained decoding; tool discovery; data sandboxing. |
| **02** | [MCP Architecture, Transports & Lifecycle](./02-mcp-architecture-transports-and-lifecycle.md) | `HIGH ROI / CORE` | 45 min | Client-Host-Server topology; capability negotiation; local standard I/O pipes (`stdio`); HTTP transports; header routing. |
| **03** | [MCP Server Primitives: Tools, Resources, Prompts](./03-mcp-server-primitives-tools-resources-prompts.md) | `IMPORTANT / NEXT` | 50 min | The core primitives: Tools (`tools/call`), Resources (`schema://`), Prompts (`prompts/get`), Sampling, and Elicitation (Human-in-the-loop); server SDKs. |
| **04** | [Reverse Sampling & Host Orchestration](./04-reverse-sampling-and-host-orchestration.md) | `IMPORTANT / NEXT` | 45 min | Host Client Gateways; reverse completions (`sampling/createMessage`); circuit breakers; protecting against massive tool outputs. |
| **05** | [Sandboxing & Confused Deputy Defenses](./05-sandboxing-security-and-confused-deputy-defenses.md) | `ADVANCED / SPECIALIZED` | 50 min | Confused Deputy attacks; indirect prompt injection; validating database queries; isolated execution environments; execution gates. |
| **06** | [Enterprise Bridges & Serverless MCP](./06-enterprise-paas-bridges-and-serverless-mcp.md) | `REFERENCE / AWARENESS` | 50 min | Connecting to legacy systems (ERP, CRM); OAuth 2.0 identity propagation; serverless response streaming. |

---

## 3. Systems Architecture & Wire Topology

The diagram below illustrates the Model Context Protocol (MCP) ecosystem, showing how local user interfaces and cloud orchestrators interact with enterprise tools and databases:

```mermaid
flowchart TD
    subgraph HostEnv["Host Application Boundary (e.g., IDE or Web App)"]
        User(["Human Operator"]) <--> UI["UI & Session Manager"]
        UI <--> Orchestrator["Agent Orchestrator"]
        Orchestrator <--> LLM["Foundation Model"]
        
        subgraph MCPClientGateway["MCP Client Gateway"]
            ClientMgr["MCP Client Connection Manager"]
            SamplingHandler["Sampling Handler (LLM Callback)"]
            ElicitHandler["Human-in-the-Loop Renderer"]
        end
        
        Orchestrator <--> ClientMgr
        SamplingHandler <--> LLM
        ElicitHandler <--> UI
    end

    subgraph TransportLayer["Transport Protocols"]
        StdioPipe["Standard I/O (Local Pipes)"]
        StreamHTTP["HTTP POST (Remote)"]
    end

    subgraph LocalServers["Local MCP Servers"]
        LocalDB["Database Server"]
        LocalFS["Filesystem Server"]
    end

    subgraph RemoteServers["Remote MCP Microservices"]
        RemoteERP["Enterprise Service"]
        RemoteITIL["IT Management Service"]
    end

    subgraph EnterpriseBackends["Systems of Record"]
        Postgres[("Production Database")]
        GitRepo[("Enterprise Repositories")]
        LegacyERP[("Legacy Systems")]
    end

    ClientMgr <==>|OS Pipe| StdioPipe
    ClientMgr <==>|TLS / JSON-RPC 2.0| StreamHTTP

    StdioPipe <--> LocalDB
    StdioPipe <--> LocalFS

    StreamHTTP <--> RemoteERP
    StreamHTTP <--> RemoteITIL

    LocalDB <--> Postgres
    LocalFS <--> GitRepo
    RemoteERP <--> LegacyERP
    RemoteITIL <--> LegacyERP

    %% Reverse Sampling & Elicitation
    RemoteERP -.->|"sampling/createMessage"| SamplingHandler
    RemoteERP -.->|"elicitation/request (Form)"| ElicitHandler
```

### Architectural Walkthrough
1. **The Host Boundary**: The Host application houses the user interface, session state, and model orchestrator. The internal MCP Client coordinates multiple server connections.
2. **Local Transport (`stdio`)**: Local tools run as child processes. Direct OS pipes provide fast communication with a small attack surface. 
3. **Remote Transport (HTTP)**: Enterprise microservices communicate over HTTP. Self-contained requests allow standard load balancers to scale servers horizontally.
4. **Governed Execution & Callbacks**: Remote tools can request intermediate model responses via **Sampling** or halt destructive actions to demand human authorization via **Elicitation**.

---

## 4. Dual-Track Learning Paths

Choose the path tailored to your engineering objectives:

```mermaid
flowchart TD
    Start(["Start Phase 03"]) --> L1["Lesson 01: Function Calling"]
    L1 --> L2["Lesson 02: MCP Architecture"]
    L2 --> L3["Lesson 03: MCP Server Primitives"]
    
    subgraph FastTrack["⚡ Fast Track: Core Concepts"]
        L3 --> LabQuick["Capstone Lab: Local stdio Mode"]
    end
    
    subgraph EnterpriseTrack["🏢 Enterprise Track: Full Implementation"]
        L3 --> L4["Lesson 04: Reverse Sampling"]
        L4 --> L5["Lesson 05: Sandboxing Defenses"]
        L5 --> L6["Lesson 06: Enterprise Bridges"]
        L6 --> LabFull["Capstone Lab: Dual-Transport Integration"]
    end
    
    LabQuick --> Done(["Phase 03 Mastery"])
    LabFull --> Done
```

* **⚡ Fast Track (1.5–2 hours)**: For developers building basic tools. Covers Lessons 01–03 and the local capstone lab.
* **🏢 Enterprise Track (3.5–4.5 hours)**: For engineers building multi-tenant microservices, serverless backends, and security sandboxes. Covers the full 6-lesson sequence.

---

## 5. Reference Implementations

Tested reference implementations are available in the [`examples/`](./examples/) directory:

1. **Python Database Server** ([`examples/mcp_database_server.py`](./examples/mcp_database_server.py)):
   - Server exposing database schema discovery.
   - Read-only SQL query tool validated against parsed syntax trees.

2. **C# / .NET Tools** ([`examples/SemanticKernelTools.cs`](./examples/SemanticKernelTools.cs)):
   - Native C# tools exposed to models via standard plugins.
   - Middleware for audit logging and security boundaries.

---

## 6. Capstone Engineering Challenge

> **Challenge**: Build an **Enterprise Observability Model Context Protocol (MCP) Server** in Python or TypeScript implementing read-only database inspection, telemetry fetching, and Human-in-the-Loop (HITL) authorization gates.
> 
> 👉 **[Start Capstone Challenge Specification](./labs/capstone-mcp-tool-server.md)**

---

## 7. Standard References

* [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/latest): The schema for Tools, Resources, Prompts, Sampling, and Elicitation.
* [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification): Standard wire protocol for all MCP communication.
* [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/release-notes): The standard for tool parameters.
* [OWASP Top 10 for Large Language Models](https://genai.owasp.org/): Security guide covering Indirect Prompt Injection (LLM01) and Excessive Agency (LLM08).

---

[Start Lesson 01: Function Calling & JSON-RPC Wire Protocols](./01-function-calling-and-json-rpc-wire-protocols.md)
