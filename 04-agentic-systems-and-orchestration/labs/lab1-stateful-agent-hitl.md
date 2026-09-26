### Lab 1: Stateful Agent with Human-in-the-Loop Approval (LangGraph Pattern) [MUST-HAVE] 🔴

#### Scenario & Enterprise Problem
In corporate financial workflows, an AI agent is authorized to retrieve balances, inspect transaction histories, and calculate fee adjustments autonomously. However, any operation that mutates balances by more than \$1,000, alters tax IDs, or initiates bank wires must be halted for explicit human approval before external execution.

#### Architectural Mechanics
- **Graph Topology**: A cyclical state machine consisting of three nodes: `Reasoner`, `RiskEvaluator`, and `ActionExecutor`.
- **Durable Checkpointing**: Every state transition commits to a durable store (`SqliteSaver`, `PostgresSaver`).
- **Interrupt Primitive**: The graph configures an execution breakpoint: `interrupt_before=["ActionExecutor"]`.
- **Operator Resumption**: The human operator inspects the paused graph state via an API or CLI, reviews the proposed tool parameters, and provides an approval or rejection token to resume execution.

#### Runnable Implementation

```python
"""
lab1_hitl_agent.py
Hands-on Lab 1: Stateful Agent with Human-in-the-Loop (HITL) Approval.
Implements the core LangGraph state machine and checkpointing pattern.
"""

from __future__ import annotations
import json
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RiskTier(str, Enum):
    LOW = "LOW"
    HIGH = "HIGH"  # Requires Human Approval


class ExecutionState(str, Enum):
    RUNNING = "RUNNING"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


@dataclass
class WorkflowState:
    session_id: str
    messages: List[Dict[str, str]] = field(default_factory=list)
    pending_tool: Optional[str] = None
    pending_args: Optional[Dict[str, Any]] = None
    risk_tier: RiskTier = RiskTier.LOW
    status: ExecutionState = ExecutionState.RUNNING
    approval_granted: Optional[bool] = None
    execution_result: Optional[str] = None


class EnterpriseHITLGraph:
    """
    Simulates a LangGraph stateful graph with durable checkpointing and interrupt_before.
    """
    def __init__(self):
        # Simulated durable storage checkpoint store (e.g., PostgresSaver)
        self._checkpoints: Dict[str, WorkflowState] = {}

    def save_checkpoint(self, state: WorkflowState) -> None:
        # Serializes state snapshot to durable storage
        self._checkpoints[state.session_id] = state

    def get_checkpoint(self, session_id: str) -> Optional[WorkflowState]:
        return self._checkpoints.get(session_id)

    def node_reasoner(self, state: WorkflowState, user_prompt: str) -> WorkflowState:
        state.messages.append({"role": "user", "content": user_prompt})
        
        # Simulated reasoning evaluation: Detect intent
        if "wire" in user_prompt.lower() or "transfer" in user_prompt.lower():
            state.pending_tool = "execute_wire_transfer"
            state.pending_args = {"amount": 25000.0, "recipient_iban": "DE89370400440532013000"}
            state.risk_tier = RiskTier.HIGH
        else:
            state.pending_tool = "get_account_balance"
            state.pending_args = {"account_id": "ACC-901"}
            state.risk_tier = RiskTier.LOW

        state.messages.append({
            "role": "assistant",
            "thought": f"Identified action {state.pending_tool} with risk tier {state.risk_tier.value}"
        })
        return state

    def run(self, session_id: str, user_prompt: str) -> WorkflowState:
        state = self.get_checkpoint(session_id) or WorkflowState(session_id=session_id)
        state = self.node_reasoner(state, user_prompt)

        # Conditional Edge & Interrupt Gate:
        if state.risk_tier == RiskTier.HIGH and state.approval_granted is None:
            state.status = ExecutionState.AWAITING_APPROVAL
            self.save_checkpoint(state)
            print(f"\n[HITL INTERRUPT] Pausing execution for Session {session_id}.")
            print(f"  Proposed Tool: {state.pending_tool}")
            print(f"  Proposed Arguments: {json.dumps(state.pending_args)}")
            print("  State safely checkpointed to database. Execution halted.")
            return state

        return self._node_action_executor(state)

    def resume(self, session_id: str, approved: bool, reason: str = "") -> WorkflowState:
        state = self.get_checkpoint(session_id)
        if not state:
            raise ValueError(f"Session {session_id} not found.")
        if state.status != ExecutionState.AWAITING_APPROVAL:
            raise RuntimeError(f"Session {session_id} is not in AWAITING_APPROVAL state.")

        state.approval_granted = approved
        if not approved:
            state.status = ExecutionState.REJECTED
            state.execution_result = f"Action rejected by compliance officer: {reason}"
            self.save_checkpoint(state)
            print(f"\n[HITL REJECTED] Action aborted for Session {session_id}: {reason}")
            return state

        print(f"\n[HITL APPROVED] Approval token verified for Session {session_id}. Resuming graph...")
        state.status = ExecutionState.RUNNING
        return self._node_action_executor(state)

    def _node_action_executor(self, state: WorkflowState) -> WorkflowState:
        # Executes the pending tool
        if state.pending_tool == "execute_wire_transfer":
            state.execution_result = f"Successfully wired ${state.pending_args['amount']} to {state.pending_args['recipient_iban']}."
        elif state.pending_tool == "get_account_balance":
            state.execution_result = "Current Account Balance: $148,250.00"
        
        state.status = ExecutionState.COMPLETED
        state.messages.append({"role": "system", "observation": state.execution_result})
        self.save_checkpoint(state)
        return state


# Verification Routine:
if __name__ == "__main__":
    graph = EnterpriseHITLGraph()
    session_id = f"sess_{uuid.uuid4().hex[:8]}"

    print("=== Step 1: Submitting High-Risk Wire Transfer Request ===")
    state = graph.run(session_id, "Please initiate a wire transfer of $25,000 to German vendor DE89370400440532013000")
    assert state.status == ExecutionState.AWAITING_APPROVAL, "Graph failed to pause on high-risk tool!"

    print("\n=== Step 2: Simulating Asynchronous Compliance Review ===")
    resumed_state = graph.resume(session_id, approved=True, reason="Verified against Vendor Invoice #INV-882")
    assert resumed_state.status == ExecutionState.COMPLETED, "Graph failed to complete after approval!"
    print(f"Final Outcome: {resumed_state.execution_result}")
```

---

[Return to Module 04: Agentic Systems & Orchestration](../README.md#7-hands-on-practice-labs--common-problem-solutions-must-have-)
