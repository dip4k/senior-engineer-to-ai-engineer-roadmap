---
trigger: always_on
---

# Always-On Production AI Engineering Rules

1. **Deterministic Foundations over Vibe Coding**:
   - Treat Large Language Models as probabilistic microservices bounded by deterministic harnesses.
   - Every external action, tool call, or state transition must be validated with formal Pydantic v2 schemas.
   - Guard against unbounded execution loops: always enforce maximum turn limits (`max_turns <= 10`) and budget decay.

2. **Code & Architecture Integrity**:
   - Write idiomatic Python 3.12+ with explicit type annotations.
   - Maintain compatibility with the existing `agent-forge` test suite (`python -m unittest agent-forge/tests/test_all.py`).
   - Run `python scripts/verify_lab.py --all` to ensure lab evaluation benchmarks remain green.

3. **Zero-Trust Security & Quarantine**:
   - Never pass untrusted user or retrieval input directly to privileged tool execution layers without sanitization and policy evaluation.
   - In MCP tools, mutations (`DROP`, `DELETE`, `UPDATE`) must either be denied or gated by human-in-the-loop approvals.
   - All state transitions must support idempotency keys to prevent duplicate execution during network retries.
