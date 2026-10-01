### Lab 2: Multi-Agent Swarm with Dynamic Handoffs (A2A Protocol) 🔴

#### Scenario & Enterprise Problem
In customer support operations, inquiries frequently span multiple organizational units (e.g., "My bill was charged twice, and my API key is broken"). Routing all messages through a monolithic central supervisor causes quadratic token growth (O(N^2)) and high latency. Agents must be able to directly transfer execution to peer agents along with an isolated, strongly typed context contract.

#### Architectural Mechanics
- **Mesh Communication**: Agents communicate via typed handoff functions (`transfer_to_billing`, `transfer_to_tech_support`).
- **Context Isolation**: When transferring control, the active agent does not dump its entire conversation history. It packages a concise `HandoffContract` (< 300 tokens) containing verified facts, customer ID, and pending sub-goals.
- **Pointer Mutation**: The swarm execution engine updates `active_agent = next_agent` without returning to a central supervisor.

#### Runnable Implementation

```python
"""
lab2_agent_swarm.py
Hands-on Lab 2: Multi-Agent Swarm with Dynamic Handoffs (A2A Protocol).
Demonstrates execution pointer mutation and context isolation.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class HandoffContract:
    target_agent: str
    reason: str
    customer_id: str
    verified_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SwarmMessage:
    sender: str
    content: str


class Agent:
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions

    def process(self, query: str, contract: Optional[HandoffContract]) -> tuple[str, Optional[HandoffContract]]:
        raise NotImplementedError


class TriageAgent(Agent):
    def __init__(self):
        super().__init__("TriageAgent", "Classify requests and route to specialized teams.")

    def process(self, query: str, contract: Optional[HandoffContract]) -> tuple[str, Optional[HandoffContract]]:
        print(f"[{self.name}] Analyzing query: '{query}'")
        if "charge" in query.lower() or "refund" in query.lower() or "invoice" in query.lower():
            print(f"[{self.name}] Routing to Billing Specialist with verified customer ID.")
            handoff = HandoffContract(
                target_agent="BillingAgent",
                reason="User reports billing discrepancy",
                customer_id="CUST-4091",
                verified_data={"flagged_invoice": "INV-2024-09"}
            )
            return "Transferring to Billing Specialist.", handoff
        return "Query resolved by Triage.", None


class BillingAgent(Agent):
    def __init__(self):
        super().__init__("BillingAgent", "Handle customer invoices, charges, and refunds.")

    def process(self, query: str, contract: Optional[HandoffContract]) -> tuple[str, Optional[HandoffContract]]:
        print(f"[{self.name}] Received control. Customer: {contract.customer_id}, Invoice: {contract.verified_data.get('flagged_invoice')}")
        # Execute specialized domain action with isolated context:
        resolution = (
            f"Billing Specialist investigated Invoice {contract.verified_data.get('flagged_invoice')} "
            f"for Customer {contract.customer_id}: Duplicate charge of $79.00 reversed successfully."
        )
        return resolution, None


class EnterpriseSwarmRunner:
    def __init__(self, agents: Dict[str, Agent], initial_agent: str):
        self.agents = agents
        self.active_agent_name = initial_agent

    def execute(self, user_query: str) -> str:
        current_contract: Optional[HandoffContract] = None
        max_hops = 5
        hops = 0

        while hops < max_hops:
            hops += 1
            agent = self.agents[self.active_agent_name]
            print(f"\n--- Turn {hops}: Active Execution Pointer -> {agent.name} ---")
            
            response, handoff = agent.process(user_query, current_contract)
            
            if handoff is None:
                print(f"[{agent.name}] Task completed with zero further handoffs.")
                return response
            
            # Pointer Mutation:
            self.active_agent_name = handoff.target_agent
            current_contract = handoff

        raise RuntimeError("Swarm exceeded maximum permitted handoff hops (Cycle Prevention).")


# Verification Routine:
if __name__ == "__main__":
    agents = {
        "TriageAgent": TriageAgent(),
        "BillingAgent": BillingAgent()
    }
    swarm = EnterpriseSwarmRunner(agents, initial_agent="TriageAgent")
    result = swarm.execute("I noticed a double charge of $79 on invoice INV-2024-09, please help.")
    print(f"\nFinal Swarm Deliverable:\n  {result}")
```

---

[Return to Module 04: Agentic Systems & Orchestration](../README.md#7-hands-on-practice-labs--common-problem-solutions-must-have-)
