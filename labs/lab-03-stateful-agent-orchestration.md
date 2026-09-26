# Lab 3: Stateful Agent Orchestration

[🔙 Back to Module 04: Agentic Systems](../04-agentic-systems-and-orchestration/README.md)

## Objective
Construct a state machine-driven workflow with durable checkpointing and dynamic subtask delegation.

## Architectural Requirements
1. Define a directed state graph: `Triage` $\to$ `Specialist` $\to$ `Validator` $\to$ `Output`.
2. Use a state reducer pattern to update shared conversation context without loss of history.
3. Implement session checkpointing to a local SQLite or Redis database.
4. Support execution pause and resumption (simulating asynchronous human approval).

## Verification Criteria
The workflow recovers cleanly from process termination at any step using saved state checkpoints.
