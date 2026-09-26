# Lab 4: Agent Failure Defense

[🔙 Back to Module 04: Agentic Systems](../04-agentic-systems-and-orchestration/README.md)

## Objective
Implement defensive engineering controls to handle production agent failures.

## Architectural Requirements
1. **Loop Detection**: Calculate rolling SHA-256 hashes of agent action sequences; terminate execution if the same action repeats 3 times.
2. **Blast Radius Control**: Wrap all state mutations in a reversible transaction pattern or generate a dry-run preview before execution.
3. **Context Compaction**: Monitor token count; when context exceeds 75% of window capacity, run a summarization pass that condenses intermediate scratchpad steps while preserving original user intent.

## Verification Criteria
The agent terminates on infinite loops within 3 iterations and successfully executes compaction without dropping system directives.
