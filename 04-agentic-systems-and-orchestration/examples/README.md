# Phase 04 Examples: Agentic Systems & Orchestration

Production-grade agentic implementations demonstrating defensive ReAct execution loops, PydanticAI type-safe agents with dependency injection, and Semantic Kernel multi-agent orchestration.

## Files

| File | Language | Purpose | Key Patterns |
|---|---|---|---|
| [`pydantic_ai_agent.py`](./pydantic_ai_agent.py) | Python 3.11+ | Type-Safe Agent with Dependency Injection | PydanticAI, typed dependency containers (`deps_type`), structured schema returns, tool validation |
| [`react_agent.py`](./react_agent.py) | Python 3.11+ | Defensive ReAct Agent Loop | Token/turn budgeting, observation compaction, SQLite state checkpointing, cycle breaker |
| [`MultiAgentPipeline.cs`](./MultiAgentPipeline.cs) | C# / .NET 9 | SK Multi-Agent Orchestrator | `AgentGroupChat`, custom selection/termination strategy, plugin delegation |
