"""
production_react_agent.py
Enterprise-grade, durable ReAct Agent runtime with SQLite state checkpointing,
execution budgets, cycle detection, and Human-in-the-Loop (HITL) gates.
"""

from __future__ import annotations

import hashlib
import json
import logging
import sqlite3
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("EnterpriseAgent")


class ToolRiskLevel(str, Enum):
    LOW = "LOW"        # Read-only operations (safe to auto-execute)
    HIGH = "HIGH"      # Write, delete, financial, or state-mutating operations (requires HITL)


@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters_schema: Dict[str, Any]
    risk_level: ToolRiskLevel
    func: Callable[..., Any]


@dataclass
class AgentStep:
    turn_index: int
    thought: str
    tool_name: Optional[str]
    tool_args: Optional[Dict[str, Any]]
    observation: Optional[str]
    is_terminal: bool
    timestamp: float = field(default_factory=time.time)


class ExecutionBudgetExceeded(Exception):
    """Raised when the agent exceeds maximum allowed iterations or tokens."""
    pass


class InfiniteLoopDetected(Exception):
    """Raised when an identical tool call signature is repeated cyclically."""
    pass


class AgentCheckpointStore:
    """Durable SQLite storage engine for persisting agent trajectories."""

    def __init__(self, db_path: str = "agent_state.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS session_checkpoints (
                session_id TEXT NOT NULL,
                turn_index INTEGER NOT NULL,
                state_json TEXT NOT NULL,
                created_at REAL NOT NULL,
                PRIMARY KEY (session_id, turn_index)
            )
            """
        )
        self.conn.commit()

    def save_checkpoint(self, session_id: str, turn_index: int, state_data: Dict[str, Any]) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO session_checkpoints (session_id, turn_index, state_json, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (session_id, turn_index, json.dumps(state_data), time.time()),
        )
        self.conn.commit()

    def load_latest_checkpoint(self, session_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT state_json FROM session_checkpoints
            WHERE session_id = ?
            ORDER BY turn_index DESC LIMIT 1
            """,
            (session_id,),
        )
        row = cursor.fetchone()
        if row:
            return json.loads(row[0])
        return None

    def close(self) -> None:
        self.conn.close()


class EnterpriseReActEngine:
    """Production ReAct Orchestrator with defensive engineering guarantees."""

    def __init__(
        self,
        session_id: str,
        system_prompt: str,
        checkpoint_store: AgentCheckpointStore,
        max_iterations: int = 6,
        max_observation_tokens: int = 500,
    ):
        self.session_id = session_id
        self.system_prompt = system_prompt
        self.checkpoint_store = checkpoint_store
        self.max_iterations = max_iterations
        self.max_observation_tokens = max_observation_tokens
        
        self.tools: Dict[str, ToolDefinition] = {}
        self.history: List[AgentStep] = []
        self.call_signature_hashes: List[str] = []

    def register_tool(self, tool: ToolDefinition) -> None:
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name} [Risk: {tool.risk_level.value}]")

    def _hash_tool_call(self, tool_name: str, tool_args: Dict[str, Any]) -> str:
        serialized = json.dumps({"tool": tool_name, "args": tool_args}, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def _compact_observation(self, raw_output: str) -> str:
        """Truncates and sanitizes verbose tool observations to protect context."""
        approx_tokens = len(raw_output) // 4
        if approx_tokens > self.max_observation_tokens:
            char_limit = self.max_observation_tokens * 4
            logger.warning(f"Observation exceeded budget ({approx_tokens} tokens). Truncating.")
            return raw_output[:char_limit] + "\n... [TRUNCATED FOR CONTEXT BUDGET] ..."
        return raw_output

    def _mock_llm_inference(self, prompt: str) -> Dict[str, Any]:
        """
        Simulated LLM call emitting structured ReAct thoughts and actions.
        In production, replace this with Claude 3.7 Sonnet / Gemini 1.5 Pro API calls.
        """
        turn = len(self.history)
        if turn == 0:
            return {
                "thought": "I need to inspect the customer's payment history to diagnose the invoice discrepancy.",
                "tool_name": "fetch_invoices",
                "tool_args": {"customer_id": "CUST-9921", "limit": 5},
                "is_terminal": False,
                "final_answer": None,
            }
        elif turn == 1:
            return {
                "thought": "Invoice #401 shows an unresolved balance of $450.00. I need to issue a credit adjustment.",
                "tool_name": "apply_credit_adjustment",
                "tool_args": {"customer_id": "CUST-9921", "amount": 450.00, "reason": "Overcharge fix"},
                "is_terminal": False,
                "final_answer": None,
            }
        else:
            return {
                "thought": "Credit adjustment applied successfully. I have all facts needed to answer the user.",
                "tool_name": None,
                "tool_args": None,
                "is_terminal": True,
                "final_answer": "Customer CUST-9921 had an overcharge of $450 on Invoice #401. A credit adjustment of $450 has been applied.",
            }

    def run_turn(self, user_objective: str, hitl_approval_callback: Optional[Callable[[str, Dict[str, Any]], bool]] = None) -> str:
        """Executes the autonomous loop until a terminal state or budget exhaustion."""
        logger.info(f"Starting agent session: {self.session_id} for objective: '{user_objective}'")

        while len(self.history) < self.max_iterations:
            turn_idx = len(self.history)
            logger.info(f"--- Iteration {turn_idx + 1} / {self.max_iterations} ---")

            # 1. Prepare Prompt & Invoke LLM
            llm_decision = self._mock_llm_inference(user_objective)
            thought = llm_decision["thought"]
            is_terminal = llm_decision["is_terminal"]

            if is_terminal:
                final_answer = llm_decision["final_answer"]
                step = AgentStep(
                    turn_index=turn_idx,
                    thought=thought,
                    tool_name=None,
                    tool_args=None,
                    observation=None,
                    is_terminal=True,
                )
                self.history.append(step)
                self._save_checkpoint()
                logger.info(f"Task completed successfully: {final_answer}")
                return final_answer

            tool_name = llm_decision["tool_name"]
            tool_args = llm_decision["tool_args"] or {}

            # 2. Cycle Detection Guard
            call_hash = self._hash_tool_call(tool_name, tool_args)
            if call_hash in self.call_signature_hashes[-2:]:
                raise InfiniteLoopDetected(f"Cycle detected: {tool_name} invoked repeatedly with identical arguments.")
            self.call_signature_hashes.append(call_hash)

            # 3. Security Policy & Human-In-The-Loop (HITL) Gate
            tool_def = self.tools.get(tool_name)
            if not tool_def:
                observation = f"ERROR: Tool '{tool_name}' is not registered in system schema."
            else:
                if tool_def.risk_level == ToolRiskLevel.HIGH:
                    logger.warning(f"HIGH RISK ACTION DETECTED: {tool_name}({tool_args})")
                    approved = False
                    if hitl_approval_callback:
                        approved = hitl_approval_callback(tool_name, tool_args)
                    
                    if not approved:
                        observation = f"EXECUTION REJECTED: Human supervisor rejected tool execution for {tool_name}."
                        logger.error(f"HITL rejected execution of {tool_name}.")
                    else:
                        try:
                            raw_result = tool_def.func(**tool_args)
                            observation = self._compact_observation(json.dumps(raw_result))
                        except Exception as ex:
                            observation = f"TOOL EXECUTION ERROR: {str(ex)}"
                else:
                    # Low risk: Auto-execute
                    try:
                        raw_result = tool_def.func(**tool_args)
                        observation = self._compact_observation(json.dumps(raw_result))
                    except Exception as ex:
                        observation = f"TOOL EXECUTION ERROR: {str(ex)}"

            # 4. Commit Step & Persist Checkpoint
            step = AgentStep(
                turn_index=turn_idx,
                thought=thought,
                tool_name=tool_name,
                tool_args=tool_args,
                observation=observation,
                is_terminal=False,
            )
            self.history.append(step)
            self._save_checkpoint()

        raise ExecutionBudgetExceeded(f"Agent failed to reach terminal state within {self.max_iterations} iterations.")

    def _save_checkpoint(self) -> None:
        state_data = {
            "session_id": self.session_id,
            "system_prompt": self.system_prompt,
            "turns": [asdict(step) for step in self.history],
        }
        self.checkpoint_store.save_checkpoint(self.session_id, len(self.history), state_data)
        logger.info(f"Checkpointed turn {len(self.history)} to persistent storage.")


# ============================================================================
# Demo Tool Callables & Execution Verification
# ============================================================================

def fetch_invoices_tool(customer_id: str, limit: int = 5) -> List[Dict[str, Any]]:
    return [
        {"invoice_id": "INV-400", "amount": 120.00, "status": "PAID"},
        {"invoice_id": "INV-401", "amount": 450.00, "status": "DISPUTED"},
    ]

def apply_credit_adjustment_tool(customer_id: str, amount: float, reason: str) -> Dict[str, Any]:
    return {"status": "SUCCESS", "tx_id": "TX-99882", "adjusted_amount": amount, "customer_id": customer_id}


if __name__ == "__main__":
    store = AgentCheckpointStore(db_path=":memory:")
    agent = EnterpriseReActEngine(
        session_id="session-enterprise-001",
        system_prompt="You are an autonomous enterprise billing remediation agent.",
        checkpoint_store=store,
        max_iterations=5,
    )

    # Register low-risk read tool
    agent.register_tool(
        ToolDefinition(
            name="fetch_invoices",
            description="Fetches recent invoices for a customer.",
            parameters_schema={"customer_id": "str", "limit": "int"},
            risk_level=ToolRiskLevel.LOW,
            func=fetch_invoices_tool,
        )
    )

    # Register high-risk write tool
    agent.register_tool(
        ToolDefinition(
            name="apply_credit_adjustment",
            description="Applies a balance credit adjustment to a customer account.",
            parameters_schema={"customer_id": "str", "amount": "float", "reason": "str"},
            risk_level=ToolRiskLevel.HIGH,
            func=apply_credit_adjustment_tool,
        )
    )

    # Human-in-the-Loop Approval Callback
    def human_approver(tool_name: str, tool_args: Dict[str, Any]) -> bool:
        print(f"\n[HITL INTERRUPT] Operator review requested for {tool_name} with args: {tool_args}")
        # In automated demo, we return True; in production, this halts for a webhook/UI button click
        return True

    final_result = agent.run_turn(
        user_objective="Resolve billing discrepancy for customer CUST-9921",
        hitl_approval_callback=human_approver,
    )
    print(f"\n[Execution Complete] Result: {final_result}")
