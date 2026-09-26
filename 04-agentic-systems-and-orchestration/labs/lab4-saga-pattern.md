### Lab 4: Transaction Rollback for Tool Execution Failures (Distributed Saga Pattern) [MUST-HAVE] 🔴

#### Scenario & Enterprise Problem
In autonomous e-commerce fulfillment, an agent must execute three mutating actions:
1. `reserve_inventory(sku, qty)`
2. `charge_payment_method(customer_id, amount)`
3. `create_shipping_manifest(order_id)`

If Step 3 fails due to a carrier API outage, the agent cannot simply throw an unhandled exception. Doing so leaves money deducted from the customer's account and physical inventory locked in warehouse buffers. The agent architecture must implement the **Distributed Saga Pattern** with compensating actions.

#### Architectural Mechanics
- **Forward Action Registry**: Every forward mutating tool `T_k` has an explicitly declared compensating inverse tool `C_k`.
- **Execution Journal**: The orchestrator appends every successfully executed forward action to a durable execution journal.
- **Topological Reversal**: On failure at step N, the Saga Coordinator halts forward execution and invokes compensating tools in reverse order (`C_{N-1} -> C_1`) with idempotency keys.

#### Runnable Implementation

```python
"""
lab4_saga_rollback.py
Hands-on Lab 4: Transaction Rollback for Tool Failures (Distributed Saga Pattern).
Demonstrates forward execution journaling and reverse compensating actions.
"""

from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List


@dataclass
class JournalEntry:
    action_name: str
    compensating_action_name: str
    forward_args: Dict[str, Any]
    compensating_args: Dict[str, Any]
    result: Any
    timestamp: float = field(default_factory=time.time)


class SagaCoordinator:
    def __init__(self):
        self.journal: List[JournalEntry] = []
        self.compensating_registry: Dict[str, Callable[[Dict[str, Any]], bool]] = {}

    def register_compensator(self, name: str, func: Callable[[Dict[str, Any]], bool]) -> None:
        self.compensating_registry[name] = func

    def record_forward_success(
        self,
        action: str,
        compensator: str,
        forward_args: Dict[str, Any],
        compensating_args: Dict[str, Any],
        result: Any
    ) -> None:
        self.journal.append(JournalEntry(
            action_name=action,
            compensating_action_name=compensator,
            forward_args=forward_args,
            compensating_args=compensating_args,
            result=result
        ))
        print(f"  [SAGA JOURNAL] Logged '{action}' -> Compensator '{compensator}'")

    def rollback(self) -> bool:
        print("\n" + "=" * 50)
        print("[SAGA ROLLBACK INITIATED] Rolling back in reverse order...")
        print("=" * 50)
        
        all_succeeded = True
        for entry in reversed(self.journal):
            comp_func = self.compensating_registry.get(entry.compensating_action_name)
            if not comp_func:
                print(f"CRITICAL ERROR: No compensator registered for {entry.compensating_action_name}")
                all_succeeded = False
                continue
            
            print(f"Executing Compensator: {entry.compensating_action_name} with args {entry.compensating_args}")
            try:
                success = comp_func(entry.compensating_args)
                if not success:
                    all_succeeded = False
            except Exception as e:
                print(f"FAILED to execute compensating action {entry.compensating_action_name}: {e}")
                all_succeeded = False

        self.journal.clear()
        return all_succeeded


# Simulated Microservice APIs:
def release_inventory_api(args: Dict[str, Any]) -> bool:
    print(f"  -> SUCCESS: Released {args['qty']} units of SKU {args['sku']} back to available stock.")
    return True

def refund_payment_api(args: Dict[str, Any]) -> bool:
    print(f"  -> SUCCESS: Refunded ${args['amount']} for Transaction {args['txn_id']}.")
    return True


def execute_fulfillment_saga(simulate_carrier_failure: bool = True):
    saga = SagaCoordinator()
    saga.register_compensator("release_inventory", release_inventory_api)
    saga.register_compensator("refund_payment", refund_payment_api)

    order_id = "ORD-99120"
    sku = "SERVER-RACK-42U"
    qty = 2
    total_price = 4500.0

    print("=== Step 1: Forward Action 1 - Reserve Inventory ===")
    reservation_id = "RES-8819"
    saga.record_forward_success(
        action="reserve_inventory",
        compensator="release_inventory",
        forward_args={"sku": sku, "qty": qty},
        compensating_args={"reservation_id": reservation_id, "sku": sku, "qty": qty},
        result={"reservation_id": reservation_id, "status": "RESERVED"}
    )

    print("\n=== Step 2: Forward Action 2 - Charge Credit Card ===")
    txn_id = "TXN-CC-77123"
    saga.record_forward_success(
        action="charge_payment",
        compensator="refund_payment",
        forward_args={"order_id": order_id, "amount": total_price},
        compensating_args={"txn_id": txn_id, "amount": total_price},
        result={"txn_id": txn_id, "status": "SETTLED"}
    )

    print("\n=== Step 3: Forward Action 3 - Schedule Freight Shipping ===")
    if simulate_carrier_failure:
        print("  -> ERROR: Freight Carrier API Timeout (504 Gateway Timeout). Action FAILED!")
        # Trigger Saga Rollback:
        rollback_ok = saga.rollback()
        assert rollback_ok, "Saga rollback encountered errors!"
        print("\n[RESULT] System safely returned to consistent baseline. No orphaned charges or inventory locks.")
        return False

    print("  -> SUCCESS: Shipment Scheduled.")
    return True


if __name__ == "__main__":
    execute_fulfillment_saga(simulate_carrier_failure=True)
```

---

[Return to Module 04: Agentic Systems & Orchestration](../README.md#7-hands-on-practice-labs--common-problem-solutions-must-have-)

