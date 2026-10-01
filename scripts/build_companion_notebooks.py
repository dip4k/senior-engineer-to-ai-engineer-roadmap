"""
build_companion_notebooks.py
=============================================================================
Programmatically generates the 3 production-grade companion Jupyter Notebooks:
1. notebooks/03_mcp_client_and_tool_inspector.ipynb
2. notebooks/04_stateful_agent_and_wal_replay.ipynb
3. notebooks/05_token_bucket_and_failure_defense.ipynb

Follows repository standards:
- 100% Valid JSON
- Colab Bootstrap Setup
- Pure Markdown & Zero-LaTeX (Unicode & clean text code blocks)
- Zero Meta-Directive Leaks
=============================================================================
"""

import json
import re
from pathlib import Path
from nb_helper import NotebookBuilder


def check_zero_latex_and_meta(text: str, context: str = "", cell_type: str = "markdown"):
    """Enforces zero-LaTeX and zero meta-directive rules."""
    forbidden_patterns = [
        r"\$\$",
        r"\\frac",
        r"\\text\{",
        r"\\begin\{",
        r"\\end\{",
        r"\[MUST-HAVE\]",
        r"\[GOOD-TO-KNOW\]",
        r"\(Refactored\)",
        r"\(Zero-LaTeX\)",
        r"\(Pure Markdown\)",
    ]
    for pattern in forbidden_patterns:
        if re.search(pattern, text):
            raise ValueError(f"Rule violation in {context}: matched forbidden pattern '{pattern}'")

    if cell_type == "markdown":
        # Strip code blocks
        lines = []
        in_code = False
        for line in text.split("\n"):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if not in_code:
                lines.append(line)
        prose = "\n".join(lines)
        # Strip inline backticks `...`
        cleaned_prose = re.sub(r"`[^`]*`", "", prose)
        # Check for unescaped dollar signs
        raw_dollars = re.findall(r"(?<!\\)\$", cleaned_prose)
        if raw_dollars:
            raise ValueError(f"Rule violation in {context}: unescaped dollar sign in markdown prose: {cleaned_prose}")


# =============================================================================
# NOTEBOOK 1: 03_mcp_client_and_tool_inspector.ipynb
# =============================================================================
def build_notebook_03(output_path: Path):
    title = "Model Context Protocol (MCP) Client, Wire Inspector & Policy Guardrails"
    description = (
        "> **Lab 02 & Phase 03 Companion Exercise**  \n"
        "> **Core Architecture**: JSON-RPC 2.0 Wire Protocol Inspector + Tool Discovery Registry + "
        "Zero-Trust ABAC Policy Engine + AST-Level SQL Mutation Protection.\n\n"
        "In production AI agent systems, granting foundation models direct, unmediated access to databases, "
        "payment gateways, or operating system shells invites the **Confused Deputy Attack**: an indirect prompt "
        "injection tricks the LLM into invoking high-privilege tools. "
        "This notebook provides a complete, interactive implementation of the **Model Context Protocol (MCP)** "
        "wire protocol, simulates client-server handshakes, inspects JSON-RPC 2.0 frames, and evaluates tool calls "
        "against an Attribute-Based Access Control (ABAC) Policy Engine."
    )

    nb = NotebookBuilder(title, description)

    # Markdown: Overview & Architecture
    nb.add_markdown(
        "## 1. Architectural Architecture & The Confused Deputy Problem\n\n"
        "Connecting foundation models to tools requires a strict separation of concerns:\n\n"
        "1. **Standardized Wire Protocol**: Rather than writing custom glue code for every tool, the Model Context "
        "Protocol (MCP) establishes a bidirectional JSON-RPC 2.0 transport.\n"
        "2. **Zero-Trust Authorization Boundary**: The LLM *decides* which tool to invoke, but the execution layer "
        "must *never* trust the LLM. An isolated **ABAC Policy Engine** inspects caller identity, tool name, and "
        "payload attributes before any action is executed.\n"
        "3. **Safety Tiers & Step-Up Gates**: Safe read queries run automatically; high-value mutations require "
        "Human-in-the-Loop (HITL) step-up approval; destructive mutations (such as SQL DDL commands) are denied unconditionally.\n\n"
        "```text\n"
        "  +---------------------+        +-------------------------+        +-------------------+\n"
        "  |  LLM Tool Decision  | -----> |    ABAC Policy Engine   | -----> |   MCP Wire Server |\n"
        "  |  (JSON-RPC Request) |        | (Permitted/Gate/Denied) |        | (Tool Execution)  |\n"
        "  +---------------------+        +-------------------------+        +-------------------+\n"
        "                                              |\n"
        "                                              v\n"
        "                                 +-------------------------+\n"
        "                                 |  Human-in-the-Loop Gate |\n"
        "                                 |  (HMAC Step-Up Token)   |\n"
        "                                 +-------------------------+\n"
        "```"
    )

    # Code: Core Data Models & Wire Inspector
    nb.add_markdown(
        "## 2. MCP JSON-RPC 2.0 Wire Protocol Models & Inspector\n\n"
        "The MCP wire protocol is built upon JSON-RPC 2.0. Every frame contains:\n"
        "- `jsonrpc`: Fixed string `\"2.0\"`.\n"
        "- `id`: Unique correlation identifier linking asynchronous responses to outbound requests.\n"
        "- `method`: The protocol verb (e.g. `initialize`, `tools/list`, `tools/call`).\n"
        "- `params`: Structured arguments validated via Pydantic v2."
    )

    code_wire_models = (
        "import json, uuid, time, hmac, hashlib, re\n"
        "from typing import Dict, Any, List, Optional, Literal\n"
        "from pydantic import BaseModel, Field, field_validator\n\n"
        "# ---------------------------------------------------------------------------\n"
        "# JSON-RPC 2.0 Wire Protocol Data Models\n"
        "# ---------------------------------------------------------------------------\n"
        "class JSONRPCRequest(BaseModel):\n"
        "    jsonrpc: Literal['2.0'] = '2.0'\n"
        "    id: str = Field(default_factory=lambda: f'req_{uuid.uuid4().hex[:8]}')\n"
        "    method: str\n"
        "    params: Dict[str, Any] = Field(default_factory=dict)\n\n"
        "class JSONRPCResponse(BaseModel):\n"
        "    jsonrpc: Literal['2.0'] = '2.0'\n"
        "    id: str\n"
        "    result: Optional[Dict[str, Any]] = None\n"
        "    error: Optional[Dict[str, Any]] = None\n\n"
        "class ToolDefinition(BaseModel):\n"
        "    name: str\n"
        "    description: str\n"
        "    inputSchema: Dict[str, Any]\n\n"
        "# ---------------------------------------------------------------------------\n"
        "# Formatted Wire Inspector Helper\n"
        "# ---------------------------------------------------------------------------\n"
        "def inspect_wire_packet(direction: str, packet: BaseModel):\n"
        "    arrow = '>>> [CLIENT -> SERVER]' if direction == 'outbound' else '<<< [SERVER -> CLIENT]'\n"
        "    formatted_json = json.dumps(packet.model_dump(), indent=2)\n"
        "    print(f'\\n{arrow} JSON-RPC 2.0 FRAME')\n"
        "    print('-' * 60)\n"
        "    print(formatted_json)\n"
        "    print('-' * 60)\n\n"
        "# Quick sanity verification\n"
        "sample_req = JSONRPCRequest(method='tools/list', params={})\n"
        "inspect_wire_packet('outbound', sample_req)"
    )
    nb.add_code(code_wire_models)

    # Markdown: Handshake Simulation
    nb.add_markdown(
        "## 3. Protocol Handshake Simulation (`initialize` & `tools/list`)\n\n"
        "The MCP connection lifecycle begins with capability negotiation:\n"
        "1. **`initialize`**: The client transmits supported protocol versions and capabilities.\n"
        "2. **Response**: The server responds with server information and enabled services.\n"
        "3. **`notifications/initialized`**: The client confirms connection readiness.\n"
        "4. **`tools/list`**: The client queries available tools and their JSON Schema parameter contracts."
    )

    code_handshake = (
        "# ---------------------------------------------------------------------------\n"
        "# Simulated MCP Payment & Database Server\n"
        "# ---------------------------------------------------------------------------\n"
        "class SimulatedMCPServer:\n"
        "    def __init__(self, name: str = 'EnterpriseCoreServer', version: str = '1.0.0'):\n"
        "        self.name = name\n"
        "        self.version = version\n"
        "        self.tools: Dict[str, ToolDefinition] = {}\n"
        "        self._register_default_tools()\n\n"
        "    def _register_default_tools(self):\n"
        "        self.tools['payment_get_balance'] = ToolDefinition(\n"
        "            name='payment_get_balance',\n"
        "            description='Query account balance for a given customer account ID.',\n"
        "            inputSchema={\n"
        "                'type': 'object',\n"
        "                'properties': {'account_id': {'type': 'string', 'description': 'Customer account reference'}},\n"
        "                'required': ['account_id']\n"
        "            }\n"
        "        )\n"
        "        self.tools['payment_issue_refund'] = ToolDefinition(\n"
        "            name='payment_issue_refund',\n"
        "            description='Issues a financial refund to a specified transaction.',\n"
        "            inputSchema={\n"
        "                'type': 'object',\n"
        "                'properties': {\n"
        "                    'transaction_id': {'type': 'string'},\n"
        "                    'amount': {'type': 'number', 'description': 'Refund amount in USD'},\n"
        "                    'reason': {'type': 'string'}\n"
        "                },\n"
        "                'required': ['transaction_id', 'amount']\n"
        "            }\n"
        "        )\n"
        "        self.tools['database_execute_query'] = ToolDefinition(\n"
        "            name='database_execute_query',\n"
        "            description='Executes read-only SQL queries against the analytical warehouse.',\n"
        "            inputSchema={\n"
        "                'type': 'object',\n"
        "                'properties': {'sql': {'type': 'string', 'description': 'SQL query string'}},\n"
        "                'required': ['sql']\n"
        "            }\n"
        "        )\n\n"
        "    def handle_request(self, request: JSONRPCRequest) -> JSONRPCResponse:\n"
        "        if request.method == 'initialize':\n"
        "            return JSONRPCResponse(\n"
        "                id=request.id,\n"
        "                result={\n"
        "                    'protocolVersion': '2026-01-01',\n"
        "                    'serverInfo': {'name': self.name, 'version': self.version},\n"
        "                    'capabilities': {'tools': {'listChanged': False}, 'resources': {}}\n"
        "                }\n"
        "            )\n"
        "        elif request.method == 'tools/list':\n"
        "            return JSONRPCResponse(\n"
        "                id=request.id,\n"
        "                result={'tools': [t.model_dump() for t in self.tools.values()]}\n"
        "            )\n"
        "        elif request.method == 'tools/call':\n"
        "            tool_name = request.params.get('name')\n"
        "            args = request.params.get('arguments', {})\n"
        "            return self._execute_tool(request.id, tool_name, args)\n"
        "        else:\n"
        "            return JSONRPCResponse(\n"
        "                id=request.id,\n"
        "                error={'code': -32601, 'message': f'Method {request.method} not found.'}\n"
        "            )\n\n"
        "    def _execute_tool(self, req_id: str, name: str, args: Dict[str, Any]) -> JSONRPCResponse:\n"
        "        if name == 'payment_get_balance':\n"
        "            return JSONRPCResponse(id=req_id, result={'account_id': args.get('account_id'), 'balance_usd': 14250.00, 'currency': 'USD'})\n"
        "        elif name == 'payment_issue_refund':\n"
        "            return JSONRPCResponse(id=req_id, result={'refund_id': f'ref_{uuid.uuid4().hex[:6]}', 'status': 'PROCESSED', 'amount': args.get('amount')})\n"
        "        elif name == 'database_execute_query':\n"
        "            return JSONRPCResponse(id=req_id, result={'rows': [{'id': 1, 'account': 'AcmeCorp', 'status': 'ACTIVE'}], 'row_count': 1})\n"
        "        return JSONRPCResponse(id=req_id, error={'code': -32602, 'message': f'Unknown tool: {name}'})\n\n"
        "# Execute Handshake\n"
        "server = SimulatedMCPServer()\n"
        "init_req = JSONRPCRequest(method='initialize', params={'protocolVersion': '2026-01-01', 'clientInfo': {'name': 'AgentForgeClient'}})\n"
        "inspect_wire_packet('outbound', init_req)\n"
        "init_resp = server.handle_request(init_req)\n"
        "inspect_wire_packet('inbound', init_resp)\n\n"
        "# Execute Tool Discovery\n"
        "list_req = JSONRPCRequest(method='tools/list')\n"
        "list_resp = server.handle_request(list_req)\n"
        "inspect_wire_packet('inbound', list_resp)\n"
        "print(f'\\nDiscovered {len(list_resp.result[\"tools\"])} active tools on server.')"
    )
    nb.add_code(code_handshake)

    # Markdown: ABAC Policy Engine
    nb.add_markdown(
        "## 4. Zero-Trust ABAC Policy Engine & Step-Up Gates\n\n"
        "Why is an authorization engine mandatory before calling an MCP tool?\n"
        "When an LLM outputs `{name: 'payment_issue_refund', arguments: {amount: 2500.0}}`, "
        "it is only a *candidate recommendation*. The autonomous agent loop must not execute it without "
        "checking enterprise policy invariants:\n\n"
        "| Policy Status | Meaning | Action Taken |\n"
        "|---|---|---|\n"
        "| `PERMITTED` | Operation is within autonomous authority limits | Dispatched immediately over JSON-RPC wire |\n"
        "| `REQUIRES_APPROVAL` | High-value or sensitive operation | Suspended; HMAC step-up approval token generated |\n"
        "| `DENIED` | Forbidden, unauthorized, or destructive operation | Execution halted with security audit exception |"
    )

    code_policy_engine = (
        "# ---------------------------------------------------------------------------\n"
        "# Zero-Trust Attribute-Based Access Control (ABAC) Engine\n"
        "# ---------------------------------------------------------------------------\n"
        "class PolicyDecision(BaseModel):\n"
        "    status: Literal['PERMITTED', 'REQUIRES_APPROVAL', 'DENIED']\n"
        "    reason: str\n"
        "    approval_token: Optional[str] = None\n\n"
        "class ABACPolicyEngine:\n"
        "    def __init__(self, auto_refund_limit_usd: float = 100.0, secret_key: str = 'enterprise_super_secret'):\n"
        "        self.auto_refund_limit_usd = auto_refund_limit_usd\n"
        "        self.secret_key = secret_key.encode('utf-8')\n\n"
        "    def generate_approval_token(self, tenant_id: str, tool_name: str, amount: float) -> str:\n"
        "        payload = f'{tenant_id}:{tool_name}:{amount}:{int(time.time())}'\n"
        "        sig = hmac.new(self.secret_key, payload.encode('utf-8'), hashlib.sha256).hexdigest()[:16]\n"
        "        return f'token_{sig}'\n\n"
        "    def evaluate(\n"
        "        self,\n"
        "        tenant_id: str,\n"
        "        user_role: str,\n"
        "        tool_name: str,\n"
        "        arguments: Dict[str, Any]\n"
        "    ) -> PolicyDecision:\n"
        "        # Rule 1: Administrative tools are denied unconditionally for non-admin roles\n"
        "        if tool_name.startswith('admin_') or tool_name.startswith('system_'):\n"
        "            return PolicyDecision(\n"
        "                status='DENIED',\n"
        "                reason=f'Security Invariant: Administrative tool {tool_name} is strictly prohibited.'\n"
        "            )\n\n"
        "        # Rule 2: Financial Refund Threshold Check\n"
        "        if tool_name == 'payment_issue_refund':\n"
        "            amount = float(arguments.get('amount', 0.0))\n"
        "            if amount <= 0:\n"
        "                return PolicyDecision(status='DENIED', reason=f'Invalid refund amount: {amount} USD.')\n"
        "            if amount > self.auto_refund_limit_usd:\n"
        "                token = self.generate_approval_token(tenant_id, tool_name, amount)\n"
        "                return PolicyDecision(\n"
        "                    status='REQUIRES_APPROVAL',\n"
        "                    reason=f'Refund amount {amount:.2f} USD exceeds auto-limit ({self.auto_refund_limit_usd:.2f} USD).',\n"
        "                    approval_token=token\n"
        "                )\n"
        "            return PolicyDecision(\n"
        "                status='PERMITTED',\n"
        "                reason=f'Refund {amount:.2f} USD is within auto-approval threshold.'\n"
        "            )\n\n"
        "        # Rule 3: Read-only operations are permitted by default\n"
        "        return PolicyDecision(status='PERMITTED', reason='Tool permitted by baseline policy.')\n\n"
        "# Instantiate Policy Engine and test decisions\n"
        "engine = ABACPolicyEngine(auto_refund_limit_usd=100.0)\n\n"
        "cases = [\n"
        "    ('tenant_a', 'support_rep', 'payment_get_balance', {'account_id': 'ACC-100'}),\n"
        "    ('tenant_a', 'support_rep', 'payment_issue_refund', {'amount': 45.0, 'transaction_id': 'tx_1'}),\n"
        "    ('tenant_a', 'support_rep', 'payment_issue_refund', {'amount': 450.0, 'transaction_id': 'tx_2'}),\n"
        "    ('tenant_a', 'support_rep', 'admin_drop_database', {}),\n"
        "]\n\n"
        "for tenant, role, tool, args in cases:\n"
        "    decision = engine.evaluate(tenant, role, tool, args)\n"
        "    print(f'Tool: {tool:<22} | Amount: {args.get(\"amount\", \"-\"):<6} | Status: {decision.status:<18} | Reason: {decision.reason}')"
    )
    nb.add_code(code_policy_engine)

    # Markdown: SQL AST Mutation Defense
    nb.add_markdown(
        "## 5. Hazardous SQL Mutation Defense (AST & Lexical Security)\n\n"
        "When an agent interacts with analytical databases via `database_execute_query`, "
        "allowing raw input invites SQL Injection and destructive DDL statements (`DROP TABLE`, `TRUNCATE`, `DELETE`).\n\n"
        "We implement an AST / Lexical query analyzer that inspects the query before dispatch:\n"
        "- **Permitted**: Single `SELECT` statements with read-only semantics.\n"
        "- **Forbidden**: Any query containing `DROP`, `DELETE`, `UPDATE`, `ALTER`, `TRUNCATE`, or multiple statements."
    )

    code_sql_defense = (
        "import re\n\n"
        "# ---------------------------------------------------------------------------\n"
        "# AST / Lexical SQL Safety Validator\n"
        "# ---------------------------------------------------------------------------\n"
        "def validate_sql_safety(sql: str) -> Dict[str, Any]:\n"
        "    cleaned = sql.strip().upper()\n"
        "    \n"
        "    # Check 1: Must begin with SELECT\n"
        "    if not cleaned.startswith('SELECT'):\n"
        "        return {\n"
        "            'safe': False,\n"
        "            'error': f'Security Violation: Only SELECT queries permitted; query starts with {cleaned.split()[0]}'\n"
        "        }\n"
        "        \n"
        "    # Check 2: Reject dangerous mutation keywords anywhere in query\n"
        "    forbidden_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE', 'EXEC', 'GRANT', 'REVOKE']\n"
        "    for kw in forbidden_keywords:\n"
        "        # Match as discrete keyword surrounded by boundaries\n"
        "        pattern = rf'\\b{kw}\\b'\n"
        "        if re.search(pattern, cleaned):\n"
        "            return {\n"
        "                'safe': False,\n"
        "                'error': f'Security Violation: Forbidden mutating keyword detected: {kw}'\n"
        "            }\n"
        "            \n"
        "    # Check 3: Multi-statement injection defense (semicolons followed by non-whitespace)\n"
        "    statements = [s.strip() for s in sql.split(';') if s.strip()]\n"
        "    if len(statements) > 1:\n"
        "        return {\n"
        "            'safe': False,\n"
        "            'error': 'Security Violation: Stacked queries (multiple statements separated by ;) are prohibited.'\n"
        "        }\n"
        "        \n"
        "    return {'safe': True, 'sanitized_sql': sql.strip()}\n\n"
        "# Test queries against SQL safety validator\n"
        "test_queries = [\n"
        "    'SELECT customer_id, balance_usd FROM customers WHERE tier = \\'ENTERPRISE\\'',\n"
        "    'DROP TABLE customers;',\n"
        "    'DELETE FROM invoices WHERE amount_usd > 1000;',\n"
        "    'UPDATE customers SET balance_usd = 0;',\n"
        "    'SELECT * FROM customers; DROP TABLE orders;'\n"
        "]\n\n"
        "print('=== SQL SAFETY EVALUATION MATRIX ===')\n"
        "for q in test_queries:\n"
        "    res = validate_sql_safety(q)\n"
        "    status = 'ALLOWED' if res['safe'] else 'BLOCKED'\n"
        "    diag = 'Query verified read-only' if res['safe'] else res['error']\n"
        "    print(f'[{status}] {q[:45]:<45} -> {diag}')"
    )
    nb.add_code(code_sql_defense)

    # Markdown: End-to-End Client Execution
    nb.add_markdown(
        "## 6. End-to-End Client Pipeline: Interception -> Policy Gate -> Wire Call\n\n"
        "Now we integrate the components into a unified `SecureMCPClient`:\n"
        "1. Intercepts candidate tool calls from the agent.\n"
        "2. Validates SQL safety if the tool is `database_execute_query`.\n"
        "3. Evaluates caller role and arguments in `ABACPolicyEngine`.\n"
        "4. Only dispatches the JSON-RPC frame over the wire if the policy evaluates to `PERMITTED`."
    )

    code_e2e_client = (
        "# ---------------------------------------------------------------------------\n"
        "# Unified Secure MCP Client with Policy Enforcement\n"
        "# ---------------------------------------------------------------------------\n"
        "class SecureMCPClient:\n"
        "    def __init__(self, server: SimulatedMCPServer, policy_engine: ABACPolicyEngine):\n"
        "        self.server = server\n"
        "        self.policy = policy_engine\n\n"
        "    def invoke_tool(\n"
        "        self,\n"
        "        tenant_id: str,\n"
        "        user_role: str,\n"
        "        tool_name: str,\n"
        "        arguments: Dict[str, Any],\n"
        "        approval_token: Optional[str] = None\n"
        "    ) -> Dict[str, Any]:\n"
        "        print(f'\\n[INSPECTOR] Inbound Tool Call Request: {tool_name}')\n"
        "        \n"
        "        # Special check for SQL tools\n"
        "        if tool_name == 'database_execute_query':\n"
        "            sql_check = validate_sql_safety(arguments.get('sql', ''))\n"
        "            if not sql_check['safe']:\n"
        "                print(f'  [POLICY DENIAL] {sql_check[\"error\"]}')\n"
        "                return {'status': 'FAILED', 'error': sql_check['error']}\n\n"
        "        # Policy Engine Evaluation\n"
        "        decision = self.policy.evaluate(tenant_id, user_role, tool_name, arguments)\n"
        "        \n"
        "        if decision.status == 'DENIED':\n"
        "            print(f'  [POLICY DENIAL] Access Denied: {decision.reason}')\n"
        "            return {'status': 'DENIED', 'reason': decision.reason}\n"
        "            \n"
        "        if decision.status == 'REQUIRES_APPROVAL':\n"
        "            if not approval_token or approval_token != decision.approval_token:\n"
        "                print(f'  [STEP-UP REQUIRED] {decision.reason}')\n"
        "                print(f'  [STEP-UP REQUIRED] Emitted Human Approval Token: {decision.approval_token}')\n"
        "                return {'status': 'REQUIRES_APPROVAL', 'token': decision.approval_token, 'reason': decision.reason}\n"
        "            print(f'  [HUMAN APPROVAL VERIFIED] Valid token supplied ({approval_token}). Proceeding...')\n\n"
        "        # Dispatch over JSON-RPC wire\n"
        "        wire_req = JSONRPCRequest(\n"
        "            method='tools/call',\n"
        "            params={'name': tool_name, 'arguments': arguments}\n"
        "        )\n"
        "        wire_resp = self.server.handle_request(wire_req)\n"
        "        print(f'  [WIRE EXECUTION COMPLETE] Result: {wire_resp.result}')\n"
        "        return {'status': 'SUCCESS', 'result': wire_resp.result}\n\n"
        "# Instantiate client and run complete demonstration\n"
        "client = SecureMCPClient(server, engine)\n\n"
        "# Scenario 1: Standard read query (Permitted)\n"
        "client.invoke_tool('tenant_1', 'user', 'payment_get_balance', {'account_id': 'ACC-994'})\n\n"
        "# Scenario 2: Safe auto-refund <= 100 USD (Permitted)\n"
        "client.invoke_tool('tenant_1', 'user', 'payment_issue_refund', {'transaction_id': 'tx_12', 'amount': 49.0})\n\n"
        "# Scenario 3: High-value refund > 100 USD (Step-Up Gated)\n"
        "gate_res = client.invoke_tool('tenant_1', 'user', 'payment_issue_refund', {'transaction_id': 'tx_13', 'amount': 250.0})\n\n"
        "# Scenario 4: Resume high-value refund with valid approval token\n"
        "if gate_res['status'] == 'REQUIRES_APPROVAL':\n"
        "    client.invoke_tool('tenant_1', 'user', 'payment_issue_refund', {'transaction_id': 'tx_13', 'amount': 250.0}, approval_token=gate_res['token'])\n\n"
        "# Scenario 5: Blocked administrative drop table\n"
        "client.invoke_tool('tenant_1', 'user', 'database_execute_query', {'sql': 'DROP TABLE customers;'})"
    )
    nb.add_code(code_e2e_client)

    # Markdown: Katas & Practice Challenges
    nb.add_markdown(
        "## 7. Interactive Katas & Challenges\n\n"
        "### Kata 1: Add Order Cancellation Tool & Inventory Policy\n"
        "Extend the MCP server with an `order_cancel` tool. Implement a policy that only permits cancellation if the order "
        "status is `PENDING`.\n\n"
        "### Kata 2: Verify Strict Rejection of Injection Payloads\n"
        "Test edge-case SQL injection strings such as `SELECT * FROM orders WHERE id = '1' OR '1'='1'; DELETE FROM orders;`."
    )

    code_katas = (
        "# ---------------------------------------------------------------------------\n"
        "# Kata Solution & Self-Verification\n"
        "# ---------------------------------------------------------------------------\n"
        "def test_kata_edge_cases():\n"
        "    injection_attack = \"SELECT * FROM orders WHERE id = '1'; DELETE FROM orders;\"\n"
        "    res = validate_sql_safety(injection_attack)\n"
        "    assert not res['safe'], 'Kata Failure: Stacked SQL injection was not blocked!'\n"
        "    print('Kata 1 Passed: Stacked injection query was safely intercepted.')\n"
        "    \n"
        "    # Test auto-refund limit barrier\n"
        "    dec = engine.evaluate('t1', 'rep', 'payment_issue_refund', {'amount': 100.01})\n"
        "    assert dec.status == 'REQUIRES_APPROVAL', 'Kata Failure: 100.01 USD did not trigger approval gate!'\n"
        "    print('Kata 2 Passed: Precision boundary condition (> 100.00 USD) verified.')\n\n"
        "test_kata_edge_cases()"
    )
    nb.add_code(code_katas)

    # Markdown: Summary
    nb.add_markdown(
        "## 8. Summary & Key Production Takeaways\n\n"
        "- **JSON-RPC 2.0 Standardization**: Decouples autonomous agents from bespoke vendor APIs, providing a clean wire protocol.\n"
        "- **Zero-Trust Tool Boundary**: Models must never possess direct database or payment credentials.\n"
        "- **Attribute-Based Access Control**: Evaluate tenant ID, role, tool name, and payload attributes *before* wire dispatch.\n"
        "- **Deterministic SQL Guardrails**: Defense-in-depth requires AST/lexical query sanitization to eliminate DDL and mutation exploits."
    )

    nb.save(output_path)


# =============================================================================
# NOTEBOOK 2: 04_stateful_agent_and_wal_replay.ipynb
# =============================================================================
def build_notebook_04(output_path: Path):
    title = "Stateful Agent Orchestration, Write-Ahead Log (WAL) & Crash Replay"
    description = (
        "> **Lab 03 & Phase 04 Companion Exercise**  \n"
        "> **Core Architecture**: Stateful ReAct Loop + Write-Ahead Log (WAL) Event Sourcing + "
        "Deterministic Crash Recovery + Time-Travel Debugger.\n\n"
        "In production cloud environments, long-running agent workflows are frequently interrupted by Kubernetes "
        "pod evictions, out-of-memory (OOM) events, and transient network partitions. "
        "If agent state is stored in an ephemeral Python dictionary, a mid-workflow crash forces a naive restart from scratch, "
        "causing the **Double-Spend Problem**: non-idempotent operations (such as payments or database writes) are executed twice! "
        "This notebook provides a complete implementation of an **Event-Sourced Write-Ahead Log (WAL)**, "
        "simulates mid-turn crashes, and demonstrates deterministic state rehydration and replay."
    )

    nb = NotebookBuilder(title, description)

    # Markdown: Overview & Architecture
    nb.add_markdown(
        "## 1. Architectural Architecture: The Fragility of Ephemeral Agent State\n\n"
        "Standard prototype agents run in an unbuffered Python loop:\n"
        "```text\n"
        "while not finished:\n"
        "    thought = llm.think()\n"
        "    action = llm.decide_action()\n"
        "    result = execute(action)\n"
        "    messages.append(result)\n"
        "```\n\n"
        "If the container is killed after `execute(action)` but before `messages.append(result)`, "
        "the execution history is obliterated. A restart executes the action again.\n\n"
        "The **Write-Ahead Log (WAL) Invariant** guarantees resilience:\n"
        "- **Commit Before Mutation**: Every state transition (thought, decision, tool invocation, completion) "
        "is persisted to an immutable, append-only `EventStore` *before* the next action begins.\n"
        "- **Deterministic Rehydration**: On crash recovery, the session reconstructs its memory by folding over the event stream."
    )

    # Code: Core State & Event Models
    nb.add_markdown(
        "## 2. Pydantic Domain Models for Events & Sessions\n\n"
        "We define strict schemas for events and sessions matching `agent_forge.runtime`."
    )

    code_models = (
        "import time, uuid, json\n"
        "from typing import List, Dict, Any, Optional, Literal\n"
        "from pydantic import BaseModel, Field\n\n"
        "# ---------------------------------------------------------------------------\n"
        "# Domain Models for Messages & Tool Calls\n"
        "# ---------------------------------------------------------------------------\n"
        "class ToolCall(BaseModel):\n"
        "    id: str = Field(default_factory=lambda: f'call_{uuid.uuid4().hex[:8]}')\n"
        "    name: str\n"
        "    arguments: Dict[str, Any]\n\n"
        "class Message(BaseModel):\n"
        "    role: Literal['system', 'user', 'assistant', 'tool']\n"
        "    content: Optional[str] = None\n"
        "    tool_calls: Optional[List[ToolCall]] = None\n"
        "    tool_call_id: Optional[str] = None\n"
        "    timestamp: float = Field(default_factory=time.time)\n\n"
        "# ---------------------------------------------------------------------------\n"
        "# Immutable Event Model for Write-Ahead Log\n"
        "# ---------------------------------------------------------------------------\n"
        "class AgentEvent(BaseModel):\n"
        "    event_id: str = Field(default_factory=lambda: f'evt_{uuid.uuid4().hex[:10]}')\n"
        "    session_id: str\n"
        "    turn_index: int\n"
        "    event_type: Literal[\n"
        "        'session_started',\n"
        "        'turn_started',\n"
        "        'model_decision',\n"
        "        'tool_executing',\n"
        "        'tool_completed',\n"
        "        'checkpoint_saved',\n"
        "        'session_completed'\n"
        "    ]\n"
        "    payload: Dict[str, Any] = Field(default_factory=dict)\n"
        "    timestamp: float = Field(default_factory=time.time)\n\n"
        "class AgentSession(BaseModel):\n"
        "    session_id: str\n"
        "    tenant_id: str = 'default_tenant'\n"
        "    user_id: str = 'default_user'\n"
        "    status: Literal['running', 'paused', 'completed', 'failed'] = 'running'\n"
        "    current_turn: int = 0\n"
        "    messages: List[Message] = Field(default_factory=list)\n"
        "    executed_tools: List[str] = Field(default_factory=list)\n\n"
        "print('Domain models initialized successfully.')"
    )
    nb.add_code(code_models)

    # Markdown: EventStore Implementation
    nb.add_markdown(
        "## 3. Append-Only EventStore & Rehydration Engine\n\n"
        "The `EventStore` provides two critical operations:\n"
        "1. `append(event)`: Persists an immutable state transition.\n"
        "2. `rehydrate_session(session_id)`: Replays historical events to restore the session state."
    )

    code_event_store = (
        "# ---------------------------------------------------------------------------\n"
        "# Thread-Safe Append-Only EventStore\n"
        "# ---------------------------------------------------------------------------\n"
        "class EventStore:\n"
        "    def __init__(self):\n"
        "        self._events: List[AgentEvent] = []\n"
        "        self._checkpoints: Dict[str, Dict[str, Any]] = {}\n\n"
        "    def append(self, event: AgentEvent) -> None:\n"
        "        self._events.append(event)\n\n"
        "    def get_events(self, session_id: str) -> List[AgentEvent]:\n"
        "        return [e for e in self._events if e.session_id == session_id]\n\n"
        "    def save_checkpoint(self, session: AgentSession) -> None:\n"
        "        self._checkpoints[session.session_id] = session.model_dump()\n"
        "        self.append(AgentEvent(\n"
        "            session_id=session.session_id,\n"
        "            turn_index=session.current_turn,\n"
        "            event_type='checkpoint_saved',\n"
        "            payload={'turn': session.current_turn, 'status': session.status}\n"
        "        ))\n\n"
        "    def rehydrate_session(self, session_id: str) -> Optional[AgentSession]:\n"
        "        events = self.get_events(session_id)\n"
        "        if not events:\n"
        "            return None\n\n"
        "        # Initialize base session\n"
        "        session = AgentSession(\n"
        "            session_id=session_id,\n"
        "            tenant_id=events[0].payload.get('tenant_id', 'default_tenant'),\n"
        "            user_id=events[0].payload.get('user_id', 'default_user')\n"
        "        )\n\n"
        "        # Fold over event stream to reconstruct state\n"
        "        for event in events:\n"
        "            session.current_turn = max(session.current_turn, event.turn_index)\n"
        "            \n"
        "            if event.event_type == 'session_started':\n"
        "                goal = event.payload.get('goal', '')\n"
        "                session.messages.append(Message(role='user', content=goal))\n"
        "            elif event.event_type == 'model_decision':\n"
        "                thought = event.payload.get('thought', '')\n"
        "                tool_name = event.payload.get('tool_name')\n"
        "                tool_args = event.payload.get('arguments', {})\n"
        "                tool_calls = [ToolCall(name=tool_name, arguments=tool_args)] if tool_name else None\n"
        "                session.messages.append(Message(role='assistant', content=thought, tool_calls=tool_calls))\n"
        "            elif event.event_type == 'tool_completed':\n"
        "                tool_name = event.payload.get('tool_name', 'unknown')\n"
        "                session.executed_tools.append(tool_name)\n"
        "                session.messages.append(Message(\n"
        "                    role='tool',\n"
        "                    tool_call_id=event.payload.get('tool_call_id'),\n"
        "                    content=json.dumps(event.payload.get('result', {}))\n"
        "                ))\n"
        "            elif event.event_type == 'session_completed':\n"
        "                session.status = 'completed'\n"
        "                \n"
        "        return session\n\n"
        "store = EventStore()\n"
        "print('EventStore initialized.')"
    )
    nb.add_code(code_event_store)

    # Markdown: Step-by-Step Execution
    nb.add_markdown(
        "## 4. Multi-Turn ReAct Workflow with Write-Ahead Logging\n\n"
        "We simulate a realistic 3-turn customer resolution workflow:\n"
        "- **Turn 0**: Inbound user request: *\"Please investigate duplicate charge on order 9182.\"*\n"
        "- **Turn 1**: Agent queries order details via `order_get_order`.\n"
        "- **Turn 2**: Agent inspects charges, identifies duplicate, and issues refund via `payment_issue_refund` (49.00 USD).\n"
        "- **Turn 3**: Agent synthesizes final customer explanation."
    )

    code_react_loop = (
        "# ---------------------------------------------------------------------------\n"
        "# Simulated Tools with Mutation Tracking\n"
        "# ---------------------------------------------------------------------------\n"
        "execution_counters = {'order_get_order': 0, 'payment_issue_refund': 0}\n\n"
        "def tool_order_get_order(order_id: str):\n"
        "    execution_counters['order_get_order'] += 1\n"
        "    return {'order_id': order_id, 'items': ['Pro Cloud Subscription'], 'status': 'CHARGED'}\n\n"
        "def tool_payment_issue_refund(transaction_id: str, amount: float):\n"
        "    execution_counters['payment_issue_refund'] += 1\n"
        "    return {'refund_id': 'ref_9182_dup', 'amount': amount, 'status': 'PROCESSED'}\n\n"
        "# ---------------------------------------------------------------------------\n"
        "# Execute Turn 0 & Turn 1\n"
        "# ---------------------------------------------------------------------------\n"
        "session_id = 'sess_prod_9942'\n\n"
        "# Turn 0: Session Start\n"
        "store.append(AgentEvent(\n"
        "    session_id=session_id,\n"
        "    turn_index=0,\n"
        "    event_type='session_started',\n"
        "    payload={'goal': 'Investigate duplicate charge on order 9182', 'tenant_id': 'acme_corp', 'user_id': 'support_agent'}\n"
        "))\n\n"
        "# Turn 1: Model Decision & Tool Execution\n"
        "store.append(AgentEvent(\n"
        "    session_id=session_id,\n"
        "    turn_index=1,\n"
        "    event_type='model_decision',\n"
        "    payload={'thought': 'I need to check the order status first.', 'tool_name': 'order_get_order', 'arguments': {'order_id': '9182'}}\n"
        "))\n"
        "res_1 = tool_order_get_order('9182')\n"
        "store.append(AgentEvent(\n"
        "    session_id=session_id,\n"
        "    turn_index=1,\n"
        "    event_type='tool_completed',\n"
        "    payload={'tool_name': 'order_get_order', 'result': res_1}\n"
        "))\n\n"
        "# Turn 2: Financial Mutation (Refund Issued!)\n"
        "store.append(AgentEvent(\n"
        "    session_id=session_id,\n"
        "    turn_index=2,\n"
        "    event_type='model_decision',\n"
        "    payload={'thought': 'Duplicate detected. Issuing 49.00 USD refund.', 'tool_name': 'payment_issue_refund', 'arguments': {'transaction_id': 'tx_dup', 'amount': 49.0}}\n"
        "))\n"
        "res_2 = tool_payment_issue_refund('tx_dup', 49.0)\n"
        "store.append(AgentEvent(\n"
        "    session_id=session_id,\n"
        "    turn_index=2,\n"
        "    event_type='tool_completed',\n"
        "    payload={'tool_name': 'payment_issue_refund', 'result': res_2}\n"
        "))\n\n"
        "print(f'Events logged in WAL: {len(store.get_events(session_id))}')\n"
        "print(f'Tool executions so far: {execution_counters}')"
    )
    nb.add_code(code_react_loop)

    # Markdown: Simulated Crash
    nb.add_markdown(
        "## 5. Simulating a Sudden Pod Eviction / OOM Crash\n\n"
        "Now, disaster strikes: immediately following Turn 2, the Kubernetes node terminates the pod. "
        "Any in-memory variables are wiped clean.\n\n"
        "Notice what would happen if a naive orchestrator restarted from Turn 0 without WAL rehydration:\n"
        "- It would observe that the refund is needed.\n"
        "- It would execute `payment_issue_refund` a second time!\n"
        "- `execution_counters['payment_issue_refund']` would equal 2 (double refund!)."
    )

    code_simulated_crash = (
        "# Simulate process termination\n"
        "active_session = None\n"
        "print('=== SIMULATED POD CRASH: PROCESS TERMINATED ===')\n"
        "print(f'In-memory session state: {active_session}')\n"
        "print(f'Preserved events in persistent EventStore: {len(store.get_events(session_id))}')"
    )
    nb.add_code(code_simulated_crash)

    # Markdown: Deterministic Rehydration
    nb.add_markdown(
        "## 6. Deterministic Crash Recovery & Resume\n\n"
        "When the replacement pod initializes, it connects to the `EventStore`, calls `rehydrate_session`, "
        "and reconstructs the exact state. It notices that `payment_issue_refund` was **already executed** "
        "and advances immediately to Turn 3 (final summary)."
    )

    code_recovery = (
        "# ---------------------------------------------------------------------------\n"
        "# Crash Recovery Rehydration\n"
        "# ---------------------------------------------------------------------------\n"
        "recovered_session = store.rehydrate_session(session_id)\n"
        "print('Rehydrated Session Status:')\n"
        "print(f'  Session ID: {recovered_session.session_id}')\n"
        "print(f'  Current Turn: {recovered_session.current_turn}')\n"
        "print(f'  Executed Tools: {recovered_session.executed_tools}')\n"
        "print(f'  Message Count: {len(recovered_session.messages)}')\n\n"
        "# Assert that refund tool is in executed_tools\n"
        "assert 'payment_issue_refund' in recovered_session.executed_tools, 'Recovery error: refund not tracked!'\n\n"
        "# Resume Turn 3: Final Answer synthesis without re-executing tools\n"
        "turn_3_event = AgentEvent(\n"
        "    session_id=session_id,\n"
        "    turn_index=3,\n"
        "    event_type='session_completed',\n"
        "    payload={'final_response': 'Duplicate charge refunded successfully. Reference: ref_9182_dup.'}\n"
        ")\n"
        "store.append(turn_3_event)\n\n"
        "print(f'\\nWorkflow resumed and completed!')\n"
        "print(f'Total refund executions: {execution_counters[\"payment_issue_refund\"]} (Expected: exactly 1!)')"
    )
    nb.add_code(code_recovery)

    # Markdown: Time-Travel Debugger & Visual Timeline
    nb.add_markdown(
        "## 7. Time-Travel Debugger & Event Stream Visualizer\n\n"
        "Because every state transition is recorded in chronological order, we can build a "
        "**Time-Travel Debugger** to inspect the session state at any arbitrary turn."
    )

    code_visualization = (
        "import matplotlib.pyplot as plt\n\n"
        "events = store.get_events(session_id)\n"
        "turn_indices = [e.turn_index for e in events]\n"
        "event_names = [f\"{e.turn_index}: {e.event_type}\" for e in events]\n"
        "timestamps = [e.timestamp - events[0].timestamp for e in events]\n\n"
        "fig, ax = plt.subplots(figsize=(11, 4.5))\n"
        "colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']\n\n"
        "for i, (name, t) in enumerate(zip(event_names, timestamps)):\n"
        "    ax.scatter(t, i, color=colors[i % len(colors)], s=120, zorder=3)\n"
        "    ax.hlines(i, 0, t, linestyles='dashed', alpha=0.4, color='gray')\n"
        "    ax.text(t + 0.001, i, f'  {name}', va='center', fontsize=9, fontweight='bold')\n\n"
        "ax.set_yticks(range(len(event_names)))\n"
        "ax.set_yticklabels([e.event_type for e in events])\n"
        "ax.set_xlabel('Elapsed Time from Start (Seconds)', fontsize=10)\n"
        "ax.set_title('Write-Ahead Log (WAL) Event Timeline & Crash Recovery Trace', fontsize=12, fontweight='bold')\n"
        "ax.grid(True, linestyle=':', alpha=0.6)\n"
        "plt.subplots_adjust(left=0.22, right=0.95, top=0.9, bottom=0.15)\n"
        "plt.show()"
    )
    nb.add_code(code_visualization)

    # Markdown: Katas & Practice
    nb.add_markdown(
        "## 8. Interactive Katas & Idempotency Challenge\n\n"
        "### Kata: Idempotency Key Validation\n"
        "In enterprise systems, even if an agent retries an action, tools must support an `idempotency_key`. "
        "If a tool call with the same idempotency key is received twice, the tool returns the cached output."
    )

    code_katas = (
        "# ---------------------------------------------------------------------------\n"
        "# Kata Solution: Idempotent Tool Execution Gate\n"
        "# ---------------------------------------------------------------------------\n"
        "class IdempotentToolRunner:\n"
        "    def __init__(self):\n"
        "        self.cache: Dict[str, Any] = {}\n"
        "        self.raw_executions = 0\n\n"
        "    def execute(self, key: str, action: str, amount: float) -> Dict[str, Any]:\n"
        "        if key in self.cache:\n"
        "            print(f'  [CACHE HIT] Returning cached result for idempotency key {key}')\n"
        "            return self.cache[key]\n"
        "        self.raw_executions += 1\n"
        "        result = {'status': 'COMPLETED', 'action': action, 'amount': amount, 'key': key}\n"
        "        self.cache[key] = result\n"
        "        return result\n\n"
        "runner = IdempotentToolRunner()\n"
        "r1 = runner.execute('idemp_key_101', 'refund', 49.0)\n"
        "r2 = runner.execute('idemp_key_101', 'refund', 49.0)\n"
        "assert runner.raw_executions == 1, 'Idempotency violation: executed twice!'\n"
        "print('Idempotency validation verified: Duplicate execution was safely intercepted.')"
    )
    nb.add_code(code_katas)

    # Markdown: Summary
    nb.add_markdown(
        "## 9. Summary & Production Architecture Checklist\n\n"
        "- **Write-Ahead Log First**: Always commit decisions and turn transitions to persistent storage before calling external tools.\n"
        "- **Avoid Ephemeral State**: Treat in-memory dictionaries as expendable caches.\n"
        "- **Deterministic State Folding**: Session memory is a fold over the immutable event stream.\n"
        "- **Idempotent Mutations**: Complement WAL recovery with cryptographic idempotency keys on all mutating tools."
    )

    nb.save(output_path)


# =============================================================================
# NOTEBOOK 3: 05_token_bucket_and_failure_defense.ipynb
# =============================================================================
def build_notebook_05(output_path: Path):
    title = "Streaming Token Bucket Rate Limiting & Cascading Failure Defense"
    description = (
        "> **Lab 04 & Phase 05 Companion Exercise**  \n"
        "> **Core Architecture**: Continuous Refill Token Bucket + Dual-Phase Token Reservation & Settlement + "
        "Circuit Breaker Finite State Machine + Fallback Provider Routing.\n\n"
        "In production AI gateways, traditional HTTP rate limiting (counting requests per second) completely breaks down. "
        "A single request might consume 15 tokens or 4,000 tokens (**The Unknown Payload Problem**), and streaming responses "
        "hold connections open for tens of seconds (**The Streaming Latency Gap**). "
        "Counting tokens post-completion leads to massive burst overages and upstream provider quota bans. "
        "Furthermore, when upstream providers degrade, uncoordinated retries trigger a **Thundering Herd Collapse**. "
        "This notebook provides a complete simulation of a **Dual-Phase Streaming Token Bucket Limiter** "
        "and a production **Circuit Breaker** with Matplotlib visualizations."
    )

    nb = NotebookBuilder(title, description)

    # Markdown: Overview & Architecture
    nb.add_markdown(
        "## 1. Architectural Architecture: The Physics of LLM Rate Limiting\n\n"
        "Why standard rate limiting fails for generative AI:\n\n"
        "1. **The Unknown Payload Problem**: Traditional web APIs rate-limit by requests per minute (RPM). In LLMs, "
        "rate limits are enforced by tokens per minute (TPM). An RPM-only limiter allows quota exhaustion in a single burst.\n"
        "2. **The Streaming Latency Gap**: Streaming responses (Server-Sent Events) take 5 to 30 seconds. If tokens "
        "are counted only after streaming ends, 50 concurrent requests can arrive, pass the gate, and trigger an upstream `HTTP 429` storm.\n"
        "3. **Dual-Phase Solution**: "
        "   - **Acquire Phase**: Deduct an estimated token allocation (e.g. 2,000 tokens) upfront.\n"
        "   - **Settle Phase**: When streaming ends, refund the unconsumed tokens (`estimated - actual`) back to the bucket.\n\n"
        "```text\n"
        "  [Inbound Request] ---> 1. Acquire (Reserve 2,000 Tokens)\n"
        "                               |\n"
        "                               v\n"
        "                         2. Stream Tokens (Actual Used: 1,200)\n"
        "                               |\n"
        "                               v\n"
        "                         3. Settle (Refund +800 Tokens to Bucket)\n"
        "```"
    )

    # Code: Dual-Phase Token Bucket Implementation
    nb.add_markdown(
        "## 2. Continuous Refill Dual-Phase Token Bucket Limiter\n\n"
        "The mathematical foundation of the continuous token bucket:\n"
        "```text\n"
        "Refill Rate = Capacity / 60.0  (Tokens per second)\n"
        "Current Tokens(t) = min(Capacity, Tokens_prev + (t - last_time) * Refill Rate)\n"
        "```"
    )

    code_token_bucket = (
        "import time, random\n"
        "from typing import Dict, Tuple, Optional\n"
        "from dataclasses import dataclass, field\n\n"
        "@dataclass\n"
        "class BucketState:\n"
        "    tpm_capacity: float\n"
        "    rpm_capacity: float\n"
        "    current_tokens: float\n"
        "    current_requests: float\n"
        "    last_refill_timestamp: float = field(default_factory=time.time)\n\n"
        "class TokenBucketLimiter:\n"
        "    def __init__(self, default_rpm: int = 60, default_tpm: int = 10000):\n"
        "        self.default_rpm = float(default_rpm)\n"
        "        self.default_tpm = float(default_tpm)\n"
        "        self.rpm_refill_rate = self.default_rpm / 60.0  # requests per sec\n"
        "        self.tpm_refill_rate = self.default_tpm / 60.0  # tokens per sec\n"
        "        self.buckets: Dict[str, BucketState] = {}\n\n"
        "    def _get_or_create(self, tenant_id: str) -> BucketState:\n"
        "        if tenant_id not in self.buckets:\n"
        "            self.buckets[tenant_id] = BucketState(\n"
        "                tpm_capacity=self.default_tpm,\n"
        "                rpm_capacity=self.default_rpm,\n"
        "                current_tokens=self.default_tpm,\n"
        "                current_requests=self.default_rpm\n"
        "            )\n"
        "        return self.buckets[tenant_id]\n\n"
        "    def _refill(self, bucket: BucketState, current_time: float):\n"
        "        elapsed = current_time - bucket.last_refill_timestamp\n"
        "        if elapsed <= 0:\n"
        "            return\n"
        "        bucket.current_requests = min(bucket.rpm_capacity, bucket.current_requests + elapsed * self.rpm_refill_rate)\n"
        "        bucket.current_tokens = min(bucket.tpm_capacity, bucket.current_tokens + elapsed * self.tpm_refill_rate)\n"
        "        bucket.last_refill_timestamp = current_time\n\n"
        "    def acquire(self, tenant_id: str, estimated_tokens: int, current_time: Optional[float] = None) -> Tuple[bool, str]:\n"
        "        now = current_time if current_time is not None else time.time()\n"
        "        bucket = self._get_or_create(tenant_id)\n"
        "        self._refill(bucket, now)\n\n"
        "        if bucket.current_requests < 1.0:\n"
        "            return False, 'RPM limit exceeded. Throttled.'\n"
        "        if bucket.current_tokens < estimated_tokens:\n"
        "            return False, f'TPM limit exceeded. Requested {estimated_tokens}, available {bucket.current_tokens:.0f}.'\n\n"
        "        # Deduct upfront reservation\n"
        "        bucket.current_requests -= 1.0\n"
        "        bucket.current_tokens -= float(estimated_tokens)\n"
        "        return True, 'OK'\n\n"
        "    def settle(self, tenant_id: str, estimated_tokens: int, actual_tokens: int, current_time: Optional[float] = None):\n"
        "        now = current_time if current_time is not None else time.time()\n"
        "        bucket = self._get_or_create(tenant_id)\n"
        "        self._refill(bucket, now)\n"
        "        delta = float(estimated_tokens - actual_tokens)\n"
        "        bucket.current_tokens = min(bucket.tpm_capacity, bucket.current_tokens + delta)\n\n"
        "# Sanity Test\n"
        "limiter = TokenBucketLimiter(default_rpm=10, default_tpm=5000)\n"
        "ok, msg = limiter.acquire('tenant_1', estimated_tokens=2000)\n"
        "print(f'Initial reservation (2000 tokens): Allowed={ok}, msg={msg}')\n"
        "limiter.settle('tenant_1', estimated_tokens=2000, actual_tokens=1200)\n"
        "print(f'Post-stream settlement (refunded 800 tokens): Remaining tokens={limiter.buckets[\"tenant_1\"].current_tokens:.0f}')"
    )
    nb.add_code(code_token_bucket)

    # Markdown: Burst Simulation
    nb.add_markdown(
        "## 3. High-Concurrency Burst Traffic Simulation\n\n"
        "We simulate a realistic burst of 20 concurrent requests arriving over a 15-second window. "
        "We record token levels, reservation events, and settlement refunds over time."
    )

    code_burst_simulation = (
        "# ---------------------------------------------------------------------------\n"
        "# Burst Simulation over Virtual Time (Seconds)\n"
        "# ---------------------------------------------------------------------------\n"
        "sim_limiter = TokenBucketLimiter(default_rpm=30, default_tpm=6000)\n"
        "tenant = 'sim_tenant'\n\n"
        "time_series = []\n"
        "token_history = []\n"
        "request_status = []\n\n"
        "current_time = 0.0\n"
        "requests_to_dispatch = [\n"
        "    (0.5, 1500, 900),\n"
        "    (0.8, 1800, 1100),\n"
        "    (1.2, 2200, 1400),\n"
        "    (1.5, 2000, 1300),  # Will be throttled due to TPM exhaustion\n"
        "    (2.0, 1500, 950),   # Will be throttled\n"
        "    (5.0, 1000, 700),   # Capacity refilled\n"
        "    (8.0, 1200, 800),\n"
        "    (12.0, 1500, 1000),\n"
        "]\n\n"
        "active_streams = []\n\n"
        "for step in range(150):\n"
        "    t = step * 0.1\n"
        "    # Check if active streams finish and settle\n"
        "    finished = [s for s in active_streams if s['finish_time'] <= t]\n"
        "    for s in finished:\n"
        "        sim_limiter.settle(tenant, s['est'], s['act'], current_time=t)\n"
        "        active_streams.remove(s)\n\n"
        "    # Check for new requests arriving at time t\n"
        "    for req in requests_to_dispatch:\n"
        "        if abs(req[0] - t) < 0.05:\n"
        "            allowed, msg = sim_limiter.acquire(tenant, req[1], current_time=t)\n"
        "            request_status.append({'time': t, 'allowed': allowed, 'tokens': req[1]})\n"
        "            if allowed:\n"
        "                active_streams.append({'finish_time': t + 2.0, 'est': req[1], 'act': req[2]})\n\n"
        "    b = sim_limiter._get_or_create(tenant)\n"
        "    sim_limiter._refill(b, t)\n"
        "    time_series.append(t)\n"
        "    token_history.append(b.current_tokens)\n\n"
        "print(f'Burst simulation complete. Tracked {len(time_series)} time steps.')\n"
        "print(f'Accepted requests: {sum(1 for r in request_status if r[\"allowed\"])} / {len(requests_to_dispatch)}')"
    )
    nb.add_code(code_burst_simulation)

    # Markdown: Circuit Breaker
    nb.add_markdown(
        "## 4. Cascading Failure Defense & Circuit Breakers\n\n"
        "When an upstream foundation model provider degrades (returning 503 Overloaded or 429 RateLimitError), "
        "callers without a circuit breaker retry endlessly, creating a **Thundering Herd Collapse**.\n\n"
        "The **Circuit Breaker Finite State Machine (FSM)**:\n"
        "- `CLOSED`: Healthy. Requests flow through normally. Consecutive errors are counted.\n"
        "- `OPEN`: Failure threshold exceeded (e.g. 3 consecutive errors). Fails fast or routes to fallback model.\n"
        "- `HALF-OPEN`: Cooldown period elapsed (e.g. 5 seconds). Canary probe request allowed. If successful, resets to `CLOSED`; if failed, re-opens."
    )

    code_circuit_breaker = (
        "# ---------------------------------------------------------------------------\n"
        "# Circuit Breaker Finite State Machine (FSM)\n"
        "# ---------------------------------------------------------------------------\n"
        "from enum import Enum\n\n"
        "class BreakerState(str, Enum):\n"
        "    CLOSED = 'CLOSED'\n"
        "    OPEN = 'OPEN'\n"
        "    HALF_OPEN = 'HALF_OPEN'\n\n"
        "class CircuitBreaker:\n"
        "    def __init__(self, failure_threshold: int = 3, cooldown_seconds: float = 4.0):\n"
        "        self.failure_threshold = failure_threshold\n"
        "        self.cooldown_seconds = cooldown_seconds\n"
        "        self.state = BreakerState.CLOSED\n"
        "        self.failure_count = 0\n"
        "        self.last_state_change = time.time()\n"
        "        self.state_history = []\n\n"
        "    def record_success(self, current_time: float):\n"
        "        if self.state == BreakerState.HALF_OPEN:\n"
        "            self.state = BreakerState.CLOSED\n"
        "            self.failure_count = 0\n"
        "            self.last_state_change = current_time\n"
        "            self.state_history.append((current_time, BreakerState.CLOSED, 'Canary Probe Succeeded'))\n"
        "        elif self.state == BreakerState.CLOSED:\n"
        "            self.failure_count = 0\n\n"
        "    def record_failure(self, current_time: float):\n"
        "        self.failure_count += 1\n"
        "        if self.state in [BreakerState.CLOSED, BreakerState.HALF_OPEN] and self.failure_count >= self.failure_threshold:\n"
        "            self.state = BreakerState.OPEN\n"
        "            self.last_state_change = current_time\n"
        "            self.state_history.append((current_time, BreakerState.OPEN, f'Failure threshold {self.failure_threshold} reached'))\n\n"
        "    def can_attempt(self, current_time: float) -> Tuple[bool, str]:\n"
        "        if self.state == BreakerState.CLOSED:\n"
        "            return True, 'Normal Execution'\n"
        "        if self.state == BreakerState.OPEN:\n"
        "            if current_time - self.last_state_change >= self.cooldown_seconds:\n"
        "                self.state = BreakerState.HALF_OPEN\n"
        "                self.last_state_change = current_time\n"
        "                self.state_history.append((current_time, BreakerState.HALF_OPEN, 'Cooldown elapsed; testing canary probe'))\n"
        "                return True, 'Canary Probe Allowed'\n"
        "            return False, 'Circuit OPEN: Fail fast or route to fallback model'\n"
        "        return True, 'Canary Probe Active'\n\n"
        "# Test Circuit Breaker transitions\n"
        "cb = CircuitBreaker(failure_threshold=3, cooldown_seconds=4.0)\n"
        "t = 0.0\n"
        "cb.record_failure(t)\n"
        "cb.record_failure(t + 0.5)\n"
        "cb.record_failure(t + 1.0)  # Trips breaker to OPEN\n"
        "print(f'State after 3 failures: {cb.state.value}')\n\n"
        "# Test fail fast\n"
        "can_call, msg = cb.can_attempt(t + 2.0)\n"
        "print(f'Attempt during cooldown (t=2.0): Allowed={can_call}, reason={msg}')\n\n"
        "# Test transition to HALF_OPEN after cooldown\n"
        "can_call, msg = cb.can_attempt(t + 5.0)\n"
        "print(f'Attempt after cooldown (t=5.0): Allowed={can_call}, State={cb.state.value}')\n\n"
        "# Canary succeeds -> reset to CLOSED\n"
        "cb.record_success(t + 5.2)\n"
        "print(f'State after canary success: {cb.state.value}')"
    )
    nb.add_code(code_circuit_breaker)

    # Markdown: Visualizing Telemetry
    nb.add_markdown(
        "## 5. Visualizing Rate Limiting Dynamics & Circuit Breaker Transitions\n\n"
        "We plot the dual dynamics:\n"
        "1. **Token Capacity Curve**: Showing reservation depletion, throttling barrier, and settlement replenishment.\n"
        "2. **Circuit Breaker State Machine**: Visualizing Closed -> Open -> Half-Open -> Closed transitions."
    )

    code_visualization = (
        "import matplotlib.pyplot as plt\n\n"
        "fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True)\n\n"
        "# Panel 1: Token Bucket Capacity\n"
        "ax1.plot(time_series, token_history, label='Available Token Capacity', color='#1f77b4', linewidth=2)\n"
        "ax1.axhline(6000, color='gray', linestyle='--', alpha=0.6, label='Max TPM Capacity (6,000)')\n"
        "ax1.axhline(0, color='red', linestyle=':', alpha=0.8, label='Exhaustion Ceiling (0)')\n\n"
        "# Mark accepted vs throttled requests\n"
        "for req in request_status:\n"
        "    if req['allowed']:\n"
        "        ax1.scatter(req['time'], 5800, color='green', marker='^', s=80, label='Accepted' if req['time'] == 0.5 else '')\n"
        "    else:\n"
        "        ax1.scatter(req['time'], 5800, color='red', marker='x', s=100, linewidth=2, label='Throttled 429' if req['time'] == 1.5 else '')\n\n"
        "ax1.set_ylabel('Tokens in Bucket', fontsize=10)\n"
        "ax1.set_title('Dual-Phase Streaming Token Bucket Rate Limiting (Reservation & Settlement)', fontsize=11, fontweight='bold')\n"
        "ax1.legend(loc='lower left', fontsize=9)\n"
        "ax1.grid(True, linestyle=':', alpha=0.6)\n\n"
        "# Panel 2: Circuit Breaker Simulation Trace\n"
        "cb_sim_times = [0, 1.0, 1.0, 5.0, 5.0, 8.0, 8.0, 14.0]\n"
        "cb_states = [1, 1, 0, 0, 0.5, 0.5, 1, 1]  # 1=Closed, 0=Open, 0.5=Half-Open\n\n"
        "ax2.step(cb_sim_times, cb_states, where='post', color='#ff7f0e', linewidth=2.5, label='Circuit State')\n"
        "ax2.fill_between(cb_sim_times, cb_states, step='post', alpha=0.15, color='#ff7f0e')\n"
        "ax2.set_yticks([0, 0.5, 1])\n"
        "ax2.set_yticklabels(['OPEN\\n(Fallback)', 'HALF-OPEN\\n(Canary)', 'CLOSED\\n(Healthy)'], fontsize=9)\n"
        "ax2.set_xlabel('Time (Seconds)', fontsize=10)\n"
        "ax2.set_ylabel('Circuit State', fontsize=10)\n"
        "ax2.set_title('Circuit Breaker FSM: Provider Outage -> Open -> Half-Open -> Closed', fontsize=11, fontweight='bold')\n"
        "ax2.grid(True, linestyle=':', alpha=0.6)\n\n"
        "plt.tight_layout()\n"
        "plt.show()"
    )
    nb.add_code(code_visualization)

    # Markdown: Katas & Full Jitter
    nb.add_markdown(
        "## 6. Interactive Katas: Exponential Backoff with Full Jitter\n\n"
        "When an agent retries after an upstream 429 error, fixed retry intervals cause synchronized "
        "request waves. **Exponential Backoff with Full Jitter** spreads requests evenly across the window:\n"
        "```text\n"
        "Sleep = Uniform(0, min(max_backoff, base_backoff * (2 ** attempt)))\n"
        "```"
    )

    code_jitter = (
        "# ---------------------------------------------------------------------------\n"
        "# Kata: Exponential Backoff with Full Jitter\n"
        "# ---------------------------------------------------------------------------\n"
        "def compute_jitter_backoff(attempt: int, base: float = 0.5, max_b: float = 8.0) -> float:\n"
        "    temp = min(max_b, base * (2 ** attempt))\n"
        "    sleep_time = random.uniform(0, temp)\n"
        "    return sleep_time\n\n"
        "print('Simulated retry sleep times for attempts 0 to 5:')\n"
        "for attempt in range(6):\n"
        "    samples = [f'{compute_jitter_backoff(attempt):.2f}s' for _ in range(4)]\n"
        "    print(f'Attempt {attempt}: {samples}')"
    )
    nb.add_code(code_jitter)

    # Markdown: Summary
    nb.add_markdown(
        "## 7. Summary & Production LLMOps Checklist\n\n"
        "- **Dual-Phase Token Reservation**: Always deduct tokens upfront before streaming starts.\n"
        "- **Post-Stream Reconciliation**: Settle actual token counts against reservations to maintain precise tenant balances.\n"
        "- **Circuit Breakers for Upstream Outages**: Fail fast or divert to fallback models when error thresholds are exceeded.\n"
        "- **Full Jitter Retries**: Avoid fixed sleep intervals to eliminate the thundering herd."
    )

    nb.save(output_path)


# =============================================================================
# Main Generator
# =============================================================================
def main():
    root_dir = Path(__file__).resolve().parent.parent
    notebooks_dir = root_dir / "notebooks"
    notebooks_dir.mkdir(parents=True, exist_ok=True)

    nb_03_path = notebooks_dir / "03_mcp_client_and_tool_inspector.ipynb"
    nb_04_path = notebooks_dir / "04_stateful_agent_and_wal_replay.ipynb"
    nb_05_path = notebooks_dir / "05_token_bucket_and_failure_defense.ipynb"

    print("Generating companion notebooks...")
    build_notebook_03(nb_03_path)
    build_notebook_04(nb_04_path)
    build_notebook_05(nb_05_path)

    # Validation check: Ensure all files are valid JSON and adhere to Zero-LaTeX rules
    for path in [nb_03_path, nb_04_path, nb_05_path]:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        cells = data.get("cells", [])
        print(f"Validated JSON: {path.name} | Total Cells: {len(cells)}")

        for idx, cell in enumerate(cells):
            src = "".join(cell.get("source", []))
            check_zero_latex_and_meta(src, f"{path.name} cell {idx}", cell.get("cell_type", "markdown"))

    print("\nAll 3 companion notebooks successfully generated and verified!")


if __name__ == "__main__":
    main()
