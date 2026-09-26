"""
production_database_mcp.py
Enterprise-Grade Production FastMCP Server for Database Observability & Safe SQL Querying.

Requirements:
    pip install mcp[cli] pydantic sqlglot aiosqlite
"""

import asyncio
import re
import sys
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP, Context
import sqlglot
from sqlglot import exp

# Initialize FastMCP Server with identity metadata
mcp = FastMCP(
    name="EnterpriseDatabaseInspector",
    dependencies=["pydantic", "sqlglot", "aiosqlite"]
)

# Simulated in-memory database catalog for demonstration
DATABASE_CATALOG: Dict[str, Dict[str, Any]] = {
    "customers": {
        "description": "Master customer entity table containing billing details.",
        "columns": {
            "customer_id": "VARCHAR(32) PRIMARY KEY",
            "company_name": "VARCHAR(255) NOT NULL",
            "tier": "VARCHAR(16) CHECK(tier IN ('STANDARD', 'ENTERPRISE'))",
            "balance_usd": "NUMERIC(12,2) DEFAULT 0.00",
            "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"
        }
    },
    "invoices": {
        "description": "Historical billing invoices and payment tracking.",
        "columns": {
            "invoice_id": "VARCHAR(32) PRIMARY KEY",
            "customer_id": "VARCHAR(32) REFERENCES customers(customer_id)",
            "amount_usd": "NUMERIC(12,2) NOT NULL",
            "status": "VARCHAR(16) CHECK(status IN ('DRAFT', 'PAID', 'OVERDUE'))",
            "due_date": "DATE NOT NULL"
        }
    }
}

# ---------------------------------------------------------------------------
# Pydantic Schemas for Strict Input Validation
# ---------------------------------------------------------------------------

class SchemaInspectionRequest(BaseModel):
    table_name: str = Field(
        ...,
        description="The exact table name to inspect. Must match an existing catalog table.",
        examples=["customers", "invoices"]
    )

    @field_validator("table_name")
    def validate_table_name(cls, v: str) -> str:
        cleaned = v.strip().lower()
        if not re.match(r"^[a-z0-9_]{1,64}$", cleaned):
            raise ValueError("Table name must contain only alphanumeric characters and underscores.")
        return cleaned

class SafeQueryRequest(BaseModel):
    sql_query: str = Field(
        ...,
        description="Read-only SQL query to execute. Must be a single SELECT statement. DDL/DML is strictly forbidden.",
        examples=["SELECT customer_id, company_name FROM customers WHERE tier = 'ENTERPRISE' LIMIT 10;"]
    )
    row_limit: int = Field(
        default=50,
        ge=1,
        le=200,
        description="Maximum rows to return. Hard ceiling of 200 enforced for context preservation."
    )

# ---------------------------------------------------------------------------
# AST-Level SQL Safety Validator
# ---------------------------------------------------------------------------

def validate_sql_safety(sql: str) -> str:
    """
    Parses SQL into an Abstract Syntax Tree (AST) using sqlglot to guarantee
    that no mutating, administrative, or injection statements are executed.
    """
    try:
        parsed_expressions = sqlglot.parse(sql)
    except Exception as err:
        raise ValueError(f"SQL Syntax Error: Unable to parse query expression: {err}")

    if len(parsed_expressions) != 1:
        raise ValueError("Multi-statement queries (separated by semicolons) are strictly prohibited.")

    statement = parsed_expressions[0]
    if statement is None:
        raise ValueError("Empty SQL statement provided.")

    # Enforce SELECT expressions only
    if not isinstance(statement, exp.Select):
        raise ValueError(f"Security Violation: Expected a SELECT query, but received {statement.key.upper()}.")

    # Inspect AST for dangerous sub-nodes (e.g. INTO clauses, CTEs executing updates)
    for node, _, _ in statement.walk():
        if isinstance(node, (exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Create, exp.Alter)):
            raise ValueError(f"Security Violation: Mutating AST node detected ({node.key.upper()}).")

    return sql

# ---------------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------------

@mcp.tool()
async def inspect_table_schema(request: SchemaInspectionRequest, ctx: Context) -> Dict[str, Any]:
    """
    Inspects the column names, data types, constraints, and descriptions
    for a declared database table.
    """
    await ctx.info(f"Inspecting catalog schema for table: {request.table_name}")
    
    if request.table_name not in DATABASE_CATALOG:
        available_tables = list(DATABASE_CATALOG.keys())
        return {
            "is_error": True,
            "error_message": f"Table '{request.table_name}' not found in catalog.",
            "available_tables": available_tables
        }

    return {
        "table_name": request.table_name,
        "metadata": DATABASE_CATALOG[request.table_name]
    }

@mcp.tool()
async def execute_safe_readonly_query(request: SafeQueryRequest, ctx: Context) -> Dict[str, Any]:
    """
    Safely executes a read-only SQL query against the enterprise database.
    Guarantees zero state mutations through AST inspection.
    """
    await ctx.info(f"Validating SQL query safety...")

    try:
        sanitized_sql = validate_sql_safety(request.sql_query)
    except ValueError as val_err:
        await ctx.error(f"SQL validation rejected query: {val_err}")
        return {
            "is_error": True,
            "error": str(val_err)
        }

    await ctx.info(f"Executing verified read-only query with limit={request.row_limit}")
    
    # In production, this executes via asyncpg or aiosqlite connection pools.
    # Simulated mock execution for demonstration:
    mock_results = [
        {"customer_id": "CUST-001", "company_name": "Apex Global Solutions", "tier": "ENTERPRISE", "balance_usd": 14250.00},
        {"customer_id": "CUST-002", "company_name": "NorthStar Logistics", "tier": "ENTERPRISE", "balance_usd": 8500.50}
    ]

    return {
        "status": "SUCCESS",
        "rows_returned": len(mock_results),
        "executed_sql": sanitized_sql,
        "data": mock_results[:request.row_limit]
    }

# ---------------------------------------------------------------------------
# MCP Resources (Passive Context Providers)
# ---------------------------------------------------------------------------

@mcp.resource("schema://database/catalog")
def get_full_database_catalog() -> str:
    """
    Exposes the entire database schema catalog as a passive markdown resource.
    Can be read directly into host context without executing a tool.
    """
    markdown_lines = ["# Enterprise Database Catalog Schema\n"]
    for table, details in DATABASE_CATALOG.items():
        markdown_lines.append(f"## Table: `{table}`")
        markdown_lines.append(f"*{details['description']}*\n")
        markdown_lines.append("| Column | Type / Constraints |")
        markdown_lines.append("|---|---|")
        for col, col_type in details["columns"].items():
            markdown_lines.append(f"| `{col}` | `{col_type}` |")
        markdown_lines.append("\n")
    return "\n".join(markdown_lines)

# ---------------------------------------------------------------------------
# MCP Prompts (Reusable Workflow Templates)
# ---------------------------------------------------------------------------

@mcp.prompt()
def generate_sql_optimization_prompt(target_table: str, performance_issue: str) -> str:
    """
    Generates a parameterized prompt template to guide the model in diagnosing
    slow database queries on a specific enterprise table.
    """
    return f"""You are a Principal Database Administrator reviewing the `{target_table}` table.
The engineering team reported the following performance bottleneck:
"{performance_issue}"

Inspect the schema for `{target_table}` using the `inspect_table_schema` tool.
Analyze existing indexing strategies and recommend:
1. Optimized B-Tree or BRIN index definitions.
2. Query rewrite suggestions.
3. Partitioning recommendations if table volume exceeds 10M rows."""

# ---------------------------------------------------------------------------
# Entrypoint: Supports Stdio or SSE transport based on CLI flag
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # When launched by Claude Desktop or Cursor, default to stdio
    # For remote microservices, pass --sse
    if "--sse" in sys.argv:
        print("Starting FastMCP server on SSE transport (http://0.0.0.0:8000/sse)...", file=sys.stderr)
        mcp.run(transport="sse")
    else:
        # Standard input/output transport
        mcp.run(transport="stdio")
