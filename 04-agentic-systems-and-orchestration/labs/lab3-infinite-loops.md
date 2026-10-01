### Lab 3: Detecting & Recovering from Infinite Loops (Cycle & Token Governor) 🔴

#### Scenario & Enterprise Problem
In production, autonomous agents frequently encounter ambiguous API error traces, missing records, or edge-case inputs. The LLM hallucinates slightly modified hypotheses and calls the same tool repeatedly with identical or near-identical parameters. Without deterministic circuit breakers, an agent can spin for hundreds of iterations, burning thousands of dollars in API tokens.

#### Architectural Mechanics
- **Tool Signature Hashing**: Generate a cryptographic signature: `SHA256(tool_name + canonical_json(tool_args))`.
- **Sliding-Window Frequency Monitor**: Maintain a ring buffer of the last N calls (e.g., depth = 6).
- **Multi-Tiered Circuit Breakers**:
  1. *Duplicate Signature Breaker*: If the exact same signature appears 3 times in the window, trip breaker.
  2. *Hard Turn Limit*: Max 8 iterations per session.
  3. *Cumulative Token Budget*: Max 40,000 tokens.
- **Defensive Environmental Feedback**: When tripped, do not crash silently. Inject a synthetic observation into context forcing the model to reformulate its plan or yield gracefully.

#### Runnable Implementation

```python
"""
lab3_loop_governor.py
Hands-on Lab 3: Detecting and Recovering from Infinite Reasoning Loops.
Demonstrates cryptographic tool hashing, sliding windows, and circuit breaking.
"""

from __future__ import annotations
import hashlib
import json
from collections import deque
from typing import Any, Dict, List, Optional


class CircuitBreakerTripped(Exception):
    pass


class AgentExecutionGovernor:
    def __init__(self, max_turns: int = 8, max_identical_calls: int = 3, window_size: int = 6):
        self.max_turns = max_turns
        self.max_identical_calls = max_identical_calls
        self.turn_count = 0
        self.history_window: deque[str] = deque(maxlen=window_size)

    def compute_signature(self, tool_name: str, tool_args: Dict[str, Any]) -> str:
        canonical_args = json.dumps(tool_args, sort_keys=True)
        raw_key = f"{tool_name}:{canonical_args}"
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def record_step(self, tool_name: str, tool_args: Dict[str, Any]) -> None:
        self.turn_count += 1
        if self.turn_count > self.max_turns:
            raise CircuitBreakerTripped(f"Hard iteration limit exceeded ({self.max_turns} turns).")

        sig = self.compute_signature(tool_name, tool_args)
        self.history_window.append(sig)

        identical_count = self.history_window.count(sig)
        if identical_count >= self.max_identical_calls:
            raise CircuitBreakerTripped(
                f"Loop detected! Tool '{tool_name}' invoked {identical_count} times with identical arguments in sliding window."
            )


def simulate_malfunctioning_agent():
    """
    Simulates an agent stuck in a repetitive loop attempting to query a missing record.
    """
    governor = AgentExecutionGovernor(max_turns=8, max_identical_calls=3, window_size=6)
    tool_name = "fetch_customer_record"
    args = {"customer_id": "CUST-MISSING-404"}

    print("=== Simulating Autonomous Agent Reasoning Loop ===")
    for turn in range(1, 10):
        try:
            print(f"Turn {turn}: Agent invoking '{tool_name}' with {args}...")
            # Governor intercepts before tool execution:
            governor.record_step(tool_name, args)
            # Simulated tool response (failure):
            print("  Observation: Error 404 - Record Not Found. Retrying...")
        except CircuitBreakerTripped as cb:
            print(f"\n[GOVERNOR INTERVENTION] {cb}")
            print("[RECOVERY ACTION] Injecting synthetic feedback to force graceful degradation:")
            synthetic_feedback = (
                "[SYSTEM NOTICE]: You have repeated tool 'fetch_customer_record' 3 times with identical parameters "
                "with zero state change. Cease calling this tool. State that the customer record does not exist."
            )
            print(f"  Injected to LLM Context: '{synthetic_feedback}'")
            return "Customer record CUST-MISSING-404 could not be located after exhaustive verification."


if __name__ == "__main__":
    result = simulate_malfunctioning_agent()
    print(f"\nFinal Controlled Deliverable: {result}")
```

---

[Return to Module 04: Agentic Systems & Orchestration](../README.md#7-hands-on-practice-labs--common-problem-solutions-must-have-)
