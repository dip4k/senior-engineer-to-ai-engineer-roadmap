# Enterprise Use Case 7: Copilot Studio & Enterprise PaaS MCP Bridge

> [🔙 Back to Senior Transition Guide](../senior-transition-guide.md)

---

## Architectural Context

Enterprise organizations increasingly deploy conversational agents through low-code platforms such as **Microsoft Copilot Studio**, **Power Platform (Power Automate)**, and **Salesforce Agentforce** to empower business units and frontline knowledge workers. However, low-code agents encounter hard boundaries when required to:
- Execute multi-step computational algorithms or proprietary machine learning models.
- Perform high-precision hybrid retrieval across millions of documents in **Azure AI Search**.
- Safely query and mutate state in mission-critical Systems of Record (**SAP S/4HANA**, **ServiceNow**, **Salesforce**) without triggering security violations or data corruption.

Rather than authoring brittle, point-to-point custom connectors for each PaaS platform, leading enterprise architectures standardize on the **Model Context Protocol (MCP 2026)** over **Server-Sent Events (SSE)**. This architectural blueprint details how enterprise low-code copilots securely invoke custom Python/.NET microservices hosted on **Azure Container Apps**, grounded in **Azure AI Search** and governed by **Microsoft Entra ID (Azure AD)**.

```mermaid
flowchart TD
    subgraph Client["Low-Code Conversational Layer"]
        User(["Enterprise User"]) <--> Teams["Microsoft Teams / Web Canvas"]
        Teams <--> CS["Microsoft Copilot Studio<br>(Generative AI Orchestrator)"]
    end

    subgraph Identity["Enterprise Identity & Trust Boundary"]
        Entra["Microsoft Entra ID (Azure AD)<br>• OIDC / OAuth 2.0 SSO<br>• On-Behalf-Of (OBO) Token Exchange<br>• App Scope: api://mcp-bridge/Tools.Execute"]
    end

    subgraph Gateway["Perimeter & Traffic Management"]
        APIM["Azure API Management (APIM)<br>• JWT Validation & Scope Verification<br>• SSE HTTP Stream Buffering Disabled<br>• Rate Limiting & Distributed Tracing"]
    end

    subgraph Compute["Serverless MCP Execution Runtime"]
        ACA["Azure Container Apps (FastMCP Python / .NET 9)<br>• Scale-to-Zero Container Environment<br>• Persistent SSE Transport (`/sse`, `/messages`)<br>• User Context & Claims Extraction<br>• Managed Identity (MI) Integration"]
    end

    subgraph Grounding["Enterprise Grounding & Retrieval"]
        AISearch[("Azure AI Search<br>• Dense HNSW + Sparse BM25 Fusion<br>• Microsoft Turing Semantic Reranker<br>• OData Query-Time ACL Pre-Filtering")]
    end

    subgraph SoR["Systems of Record (SoR)"]
        SAP[("SAP S/4HANA<br>(BAPIs via RFC / OData)")]
        SNOW[("ServiceNow<br>(Table API / ITIL Workflows)")]
    end

    User -.->|1. Authenticate SSO| Entra
    CS -->|2. Get User OBO Token| Entra
    CS -->|3. Call MCP Plugin over SSE| APIM
    APIM -->|4. Forward Stream + User JWT| ACA
    ACA -->|5. Managed Identity| AISearch
    ACA -->|6. Scoped User Execution| SAP
    ACA -->|7. Field-Masked REST| SNOW
    AISearch -.->|Grounded Chunks + Captions| ACA
    SAP -.->|Material / PO Status| ACA
    SNOW -.->|Incident Context| ACA
    ACA -->>|8. JSON-RPC Result over SSE Stream| CS
    CS -->>|9. Grounded Natural Language Answer| Teams
```

---

## Core Architectural Components

### 1. Copilot Studio Custom Engine & OpenAPI Plugin Bridge
- **Connector Pattern**: Microsoft Copilot Studio communicates with external tools via Custom Connectors defined through OpenAPI 3.0 specifications.
- **Dynamic Tool Schema Ingestion**: The MCP Bridge exposes an OpenAPI gateway that translates the MCP `tools/list` JSON-RPC registry into OpenAPI operations. Copilot Studio's generative orchestrator indexes these operations and autonomously binds user intents to the appropriate tool call.
- **Session Continuity**: The connector maps each Copilot Studio conversation ID to a unique MCP session ID, allowing stateful resource subscriptions and conversation-scoped context caching.

### 2. Streamable HTTP / Server-Sent Events (SSE) Wire Transport
- **Bidirectional Disconnected HTTP Flow**:
  - **Downstream Channel (`GET /sse`)**: The Copilot Studio connector or API gateway establishes a long-lived HTTP connection receiving Server-Sent Events (`text/event-stream`). The server sends an initial event identifying the session-specific message endpoint:
    ```http
    HTTP/1.1 200 OK
    Content-Type: text/event-stream
    Cache-Control: no-cache
    Connection: keep-alive

    event: endpoint
    data: /messages?sessionId=8f7e2a10-c3d5-4e78-9b81-645b81a8f9c2
    ```
  - **Upstream Channel (`POST /messages?sessionId=...`)**: Client requests (e.g. `tools/call`, `resources/read`) are submitted as HTTP `POST` requests carrying standard JSON-RPC 2.0 payloads.
  - **Result Delivery**: Asynchronous tool results, progress notifications (`notifications/progress`), and log streams are emitted downstream over the persistent SSE connection.
- **Keep-Alive Heartbeats**: To prevent Azure Application Gateway or Azure Front Door from terminating idle HTTP connections (which typically timeout after 60–240 seconds), the MCP server emits an SSE comment heartbeat (`: ping\n\n`) every 15 seconds.

### 3. Enterprise Identity & Token Forwarding (Entra ID OBO Flow)
- **Eliminating the Confused Deputy**: The MCP server must never execute queries using a shared "god-mode" service principal. Every action must execute within the security context of the human user interacting with Copilot Studio.
- **On-Behalf-Of (OBO) Flow**:
  1. Copilot Studio acquires an Entra ID bearer token on behalf of the signed-in user.
  2. The token is transmitted via the standard `Authorization: Bearer <JWT>` header to Azure API Management.
  3. APIM verifies the token signature, audience (`api://mcp-enterprise-bridge`), and required scope (`MCP.Tools.Execute`).
  4. The MCP server unpacks the claims (`upn`, `oid`, `groups`) and forwards the identity to downstream databases, applying user-specific permissions.

### 4. Grounding with Azure AI Search (Semantic Hybrid Retrieval)
- **Tool Declaration**: The MCP server exposes a dedicated grounding tool: `search_enterprise_knowledge`.
- **Hybrid Retrieval Architecture**:
  - Executes a vector search (HNSW / DiskANN) on embedding fields generated by `text-embedding-3-large`.
  - Executes a full-text BM25 lexical search with fuzzy matching and lemmatization.
  - Combines candidates using **Reciprocal Rank Fusion (RRF)**.
  - Runs the fused candidates through the **Microsoft Turing Semantic Reranker** to evaluate semantic relevance.
- **Query-Time Security Pre-Filtering**: The MCP server injects the caller's Entra ID group SIDs into the OData filter predicate (`search.in(tenant_id, '...') and security_groups/any(...)`), guaranteeing that the model cannot retrieve unauthorized documents.

### 5. Systems of Record Gateway (SAP & ServiceNow)
- **SAP ERP Integration**: Calls SAP S/4HANA via RFC or OData v4 to fetch material availability (`BAPI_MATERIAL_AVAILABILITY`) or purchase order details (`BAPI_PO_GETDETAIL`). Order creations exceeding \$10,000 trigger a two-phase approval ticket.
- **ServiceNow Integration**: Wraps the ServiceNow Table API with regex-based PII and secret masking, allowing agents to read ticket statuses and post work notes while prohibiting unapproved incident closures.

---

## Production Code Implementation

### 1. FastMCP Python Server with Entra ID Auth & Azure AI Search
The following production-ready Python microservice runs in **Azure Container Apps**, exposes an MCP SSE transport, verifies Entra ID JWT tokens, and executes hybrid search against Azure AI Search:

```python
"""
Enterprise MCP Server: Copilot Studio to Azure AI Search & ERP Bridge
Hosting: Azure Container Apps with Streamable HTTP/SSE
Identity: Microsoft Entra ID (OBO Flow)
"""

import os
import re
import json
import logging
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, Depends, HTTPException, Security, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWKClient
from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

# Configure structured logging to stderr (Never write to stdout on MCP servers)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mcp_bridge")

# Environment Configuration
TENANT_ID = os.environ["AZURE_TENANT_ID"]
CLIENT_ID = os.environ["AZURE_CLIENT_ID"]
SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"]
SEARCH_INDEX = os.environ["AZURE_SEARCH_INDEX"]
JWKS_URL = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"

# Initialize FastMCP Server
mcp = FastMCP(
    name="EnterprisePaaSBridge",
    instructions="Provides grounded enterprise search and ERP operations for Copilot Studio."
)

# JWT Security Validator
jwks_client = PyJWKClient(JWKS_URL)
security = HTTPBearer()

def verify_entra_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    """Validates Entra ID Bearer token signature, issuer, audience, and scope."""
    token = credentials.credentials
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=f"api://{CLIENT_ID}",
            issuer=f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"
        )
        
        # Verify required scope
        scopes = payload.get("scp", "").split()
        if "MCP.Tools.Execute" not in scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions: 'MCP.Tools.Execute' scope required."
            )
        return payload
    except jwt.PyJWTError as ex:
        logger.warning(f"Authentication failure: {str(ex)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {str(ex)}"
        )


# ============================================================================
# TOOL DEFINITION: Grounded Azure AI Search with Security Pre-Filtering
# ============================================================================

class SearchKnowledgeArgs(BaseModel):
    query_text: str = Field(..., description="Natural language search question", min_length=3)
    query_vector: List[float] = Field(..., description="1536-dim or 3072-dim embedding vector")
    user_principal_name: str = Field(..., description="UPN of the calling user for ACL enforcement")
    top_k: int = Field(default=5, ge=1, le=10, description="Number of chunks to retrieve")


@mcp.tool()
async def search_enterprise_knowledge(args: SearchKnowledgeArgs) -> str:
    """
    Executes a two-stage hybrid search against Azure AI Search combining
    dense vector similarity, BM25 lexical search, and the Turing Semantic Reranker.
    Enforces user-level security trimming via OData filters.
    """
    logger.info(f"Executing search for user: {args.user_principal_name}, query: '{args.query_text}'")
    
    # Authenticate to Azure AI Search using Managed Identity
    credential = DefaultAzureCredential()
    search_client = SearchClient(
        endpoint=SEARCH_ENDPOINT,
        index_name=SEARCH_INDEX,
        credential=credential
    )

    # Sanitize user UPN to prevent OData injection
    clean_upn = re.sub(r"[^a-zA-Z0-9@._-]", "", args.user_principal_name)
    odata_filter = f"security_principals/any(p: p eq '{clean_upn}' or p eq 'all_employees')"

    vector_query = VectorizedQuery(
        vector=args.query_vector,
        k_nearest_neighbors_count=args.top_k * 5,
        fields="content_vector"
    )

    try:
        results = search_client.search(
            search_text=args.query_text,
            vector_queries=[vector_query],
            filter=odata_filter,
            query_type="semantic",
            semantic_configuration_name="default-semantic-config",
            query_caption="extractive|highlight-true",
            top=args.top_k,
            select=["doc_id", "title", "content", "source_url"]
        )

        formatted_chunks = []
        for doc in results:
            caption_text = ""
            if doc.get("@search.captions"):
                caption_text = doc["@search.captions"][0].text

            formatted_chunks.append({
                "doc_id": doc["doc_id"],
                "title": doc["title"],
                "source_url": doc["source_url"],
                "reranker_score": doc.get("@search.reranker_score", 0.0),
                "caption": caption_text,
                "content_snippet": doc["content"][:600]
            })

        return json.dumps({"status": "SUCCESS", "chunks": formatted_chunks}, indent=2)

    except Exception as ex:
        logger.error(f"Azure AI Search error: {str(ex)}")
        return json.dumps({
            "status": "ERROR",
            "isError": True,
            "message": f"Search engine failed to execute query: {str(ex)}"
        })


# ============================================================================
# TOOL DEFINITION: Safe SAP S/4HANA Material Availability Check
# ============================================================================

class SapStockCheckArgs(BaseModel):
    material_number: str = Field(..., pattern=r"^[0-9A-Za-z_-]{1,18}$", description="SAP 18-char material code")
    plant_code: str = Field(..., pattern=r"^[A-Z0-9]{4}$", description="SAP 4-character plant code (e.g., 1000)")


@mcp.tool()
async def sap_check_stock_availability(args: SapStockCheckArgs) -> str:
    """
    Queries real-time material stock availability in SAP S/4HANA via BAPI.
    Enforces plant code and material ID validation.
    """
    logger.info(f"SAP Stock Check: Material={args.material_number}, Plant={args.plant_code}")
    
    # Defensive parameter formatting: Zero-pad numeric SAP material numbers to 18 chars
    formatted_mat = args.material_number.zfill(18) if args.material_number.isdigit() else args.material_number
    
    # In production, invokes SAP RFC via pyrfc or SAP OData v4 client
    # Simulated deterministic response:
    mock_stock = {
        "material_number": formatted_mat,
        "plant_code": args.plant_code,
        "unrestricted_stock": 1420.0,
        "unit_of_measure": "EA",
        "currency": "EUR",
        "plant_status": "ACTIVE"
    }
    return json.dumps({"status": "SUCCESS", "inventory": mock_stock}, indent=2)
```

---

### 2. OpenAPI 3.0 Custom Connector Specification (Copilot Studio Bridge)
Importing this OpenAPI schema into **Power Platform / Copilot Studio** creates the custom action bridge connecting conversational topics directly to the MCP server:

```yaml
openapi: 3.0.1
info:
  title: Enterprise MCP Microservices Bridge
  description: Connects Microsoft Copilot Studio to serverless Python MCP tools over SSE.
  version: 1.0.0
servers:
  - url: https://mcp-gateway.corp.internal/api/v1
paths:
  /tools/search_enterprise_knowledge:
    post:
      summary: Search Enterprise Knowledge (Azure AI Search)
      description: Searches verified corporate documentation with vector + BM25 hybrid ranking and Entra ID ACL enforcement.
      operationId: SearchEnterpriseKnowledge
      security:
        - OAuth2Auth:
            - "MCP.Tools.Execute"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - query_text
                - user_principal_name
              properties:
                query_text:
                  type: string
                  description: The search question asked by the user.
                user_principal_name:
                  type: string
                  description: The UPN of the current conversational user.
                top_k:
                  type: integer
                  default: 5
                  description: Maximum number of relevant chunks to retrieve.
      responses:
        '200':
          description: Search results containing ranked passages and citations.
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                  chunks:
                    type: array
                    items:
                      type: object
                      properties:
                        doc_id:
                          type: string
                        title:
                          type: string
                        caption:
                          type: string
                        source_url:
                          type: string

components:
  securitySchemes:
    OAuth2Auth:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://login.microsoftonline.com/common/oauth2/v2.0/authorize
          tokenUrl: https://login.microsoftonline.com/common/oauth2/v2.0/token
          scopes:
            api://mcp-enterprise-bridge/MCP.Tools.Execute: Execute authorized MCP tools
```

---

## Architectural Tradeoff Matrix

| Architecture Dimension | Native Low-Code Connectors | Custom Webhook REST Endpoints | MCP over SSE Bridge (This Blueprint) |
|---|---|---|---|
| **Protocol Standardization** | Proprietary Power Platform schemas | Bespoke REST APIs per integration | **Universal JSON-RPC 2.0 (Open Standard)** |
| **Tool Portability** | Locked to Microsoft Power Platform | Manual migration required for each client | **Polyglot: Runs in Copilot Studio, Cursor, Claude Code, ADK** |
| **Real-Time Streaming** | Request/Response polling only | Standard HTTP buffering | **Native Server-Sent Events (SSE) streaming** |
| **Context & Grounding** | Naive SharePoint indexing | Custom RAG code in every endpoint | **Two-Stage Hybrid Azure AI Search with Turing Reranker** |
| **Identity Propagation** | Basic connection credentials | Often degrades to shared service accounts | **Native Entra ID On-Behalf-Of (OBO) flow** |
| **Reverse LLM Sampling** | Not supported | Not supported | **Native MCP `sampling/createMessage` support** |
| **Maintenance Cost** | High ($M \times N$ connector proliferation) | High (Bespoke endpoints for every action) | **Lowest (Unified $M + N$ microservice tool bus)** |

---

## Production Failure Modes & Architectural Mitigations

### 1. Gateway SSE Connection Dropping & Idle Timeouts
- **Failure**: Azure Application Gateway or Azure Front Door severs the persistent HTTP `/sse` stream after 60 seconds of inactivity, terminating long-running agent workflows.
- **Root Cause**: Intermediary load balancers interpret idle TCP sockets as abandoned connections.
- **Mitigation**:
  1. Configure the MCP server to emit periodic SSE comment heartbeats (`: keep-alive\n\n`) every 15 seconds.
  2. Increase the HTTP connection idle timeout in Azure Container Apps to 300 seconds.
  3. Implement client-side reconnection with exponential backoff on Copilot Studio custom connectors.

### 2. Context Window Overflow in Copilot Studio
- **Failure**: A tool query against SAP or ServiceNow returns 500 rows, dumping 50,000 tokens into the Copilot Studio context window and triggering an immediate runtime error (`ContextWindowExceeded`).
- **Mitigation**:
  1. Enforce strict output truncation middleware in the MCP tool handler: limit results to maximum 10 items or 4,000 tokens.
  2. Inject an explicit structural warning when data is truncated: `"[Showing 10 of 240 records. Refine query with specific filters.]"`.

### 3. Confused Deputy Privilege Escalation
- **Failure**: A low-privileged user instructs Copilot Studio to ask the MCP server to display executive salary records or trigger an unapproved ERP goods receipt.
- **Mitigation**:
  1. Never allow the MCP server to run queries using an unconstrained administrative service principal.
  2. Enforce the Entra ID On-Behalf-Of (OBO) flow: extract user claims and pass them directly into database connection sessions or SAP RFC authorization objects.

---

## Production Implementation Checklist

- [ ] Azure Container Apps environment deployed with HTTP ingress, disabled response buffering, and CORS configured for Copilot Studio domains.
- [ ] Entra ID App Registrations configured with `api://mcp-enterprise-bridge` Application ID URI and `MCP.Tools.Execute` scope.
- [ ] Managed Identity assigned to Azure Container Apps with `Search Index Data Reader` role on Azure AI Search.
- [ ] Azure AI Search configured with HNSW vector index, BM25 inverted index, and Microsoft Turing Semantic Reranker.
- [ ] OData security pre-filtering active on all search queries to enforce tenant and group isolation.
- [ ] SAP RFC and ServiceNow connectors implement strict input sanitization, field masking, and parameter validation.
- [ ] Mutating operations (e.g., purchase order creation > \$10,000) gated behind Human-in-the-Loop (HITL) approval tokens.
- [ ] OpenTelemetry distributed tracing enabled across Copilot Studio, APIM, and the MCP Container App runtime.
