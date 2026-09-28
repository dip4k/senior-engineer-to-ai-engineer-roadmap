"""
Durable Agent Orchestrator for AgentForge.
Executes multi-turn agent loops with event-sourced WAL, tool repair,
infinite loop safeguards, and human-in-the-loop pause/resume.
"""

from typing import List, Dict, Any, Optional
import hashlib
import time
from .state_models import AgentSession, Message, ToolCall, ToolResult, AgentEvent
from .event_store import EventStore

class DurableOrchestrator:
    def __init__(
        self,
        event_store: EventStore,
        gateway: Any,
        mcp_client: Any,
        policy_engine: Any,
        tracer: Optional[Any] = None
    ):
        self.event_store = event_store
        self.gateway = gateway
        self.mcp_client = mcp_client
        self.policy_engine = policy_engine
        self.tracer = tracer

    def _generate_idempotency_key(self, session_id: str, turn: int, tool_name: str, args: Dict[str, Any]) -> str:
        raw = f"{session_id}:{turn}:{tool_name}:{str(sorted(args.items()))}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def run(self, session: AgentSession, user_input: Optional[str] = None) -> str:
        """
        Executes or resumes an agent session until completion, failure,
        or pause for human approval.
        """
        # If this is a fresh invocation, record start
        if session.current_turn == 0 and user_input:
            session.messages.append(Message(role="user", content=user_input))
            self.event_store.append(AgentEvent(
                session_id=session.session_id,
                turn_index=0,
                event_type="session_started",
                payload={"user_id": session.user_id, "tenant_id": session.tenant_id, "prompt": user_input}
            ))

        while session.status == "running" and session.current_turn < session.max_turns:
            session.current_turn += 1
            turn = session.current_turn
            
            # Start turn event
            self.event_store.append(AgentEvent(
                session_id=session.session_id,
                turn_index=turn,
                event_type="turn_started",
                payload={"turn": turn}
            ))

            # Span for model decision
            span = None
            if self.tracer:
                span = self.tracer.start_span(f"gen_ai.agent.turn_{turn}", attributes={
                    "session_id": session.session_id,
                    "turn_index": turn
                })

            # Call Model Gateway with structured envelope
            tools_schema = self.mcp_client.get_tools_schema()
            response = self.gateway.generate(
                session_id=session.session_id,
                tenant_id=session.tenant_id,
                messages=session.messages,
                tools=tools_schema
            )

            # Record model decision
            self.event_store.append(AgentEvent(
                session_id=session.session_id,
                turn_index=turn,
                event_type="model_decision",
                payload={
                    "content": response.content,
                    "tool_calls": [tc.model_dump() for tc in response.tool_calls] if response.tool_calls else None,
                    "usage": response.usage
                }
            ))

            if response.tool_calls:
                # Add assistant message containing the tool calls
                session.messages.append(Message(
                    role="assistant",
                    content=response.content,
                    tool_calls=response.tool_calls
                ))

                for tool_call in response.tool_calls:
                    # 1. Zero-Trust Policy Check
                    auth_result = self.policy_engine.evaluate(
                        tenant_id=session.tenant_id,
                        user_id=session.user_id,
                        tool_name=tool_call.name,
                        arguments=tool_call.arguments
                    )

                    if auth_result.status == "REQUIRES_APPROVAL":
                        session.status = "paused_for_approval"
                        session.pending_tool_call = tool_call
                        self.event_store.append(AgentEvent(
                            session_id=session.session_id,
                            turn_index=turn,
                            event_type="human_approval_required",
                            payload={"tool_call": tool_call.model_dump(), "reason": auth_result.reason}
                        ))
                        self.event_store.save_checkpoint(session)
                        if span:
                            span.end()
                        return f"Action requires managerial approval: {auth_result.reason}. Tool call {tool_call.name} suspended."

                    if auth_result.status == "DENIED":
                        result_msg = f"ERROR: Authorization Denied: {auth_result.reason}"
                        session.messages.append(Message(
                            role="tool",
                            tool_call_id=tool_call.id,
                            content=result_msg
                        ))
                        self.event_store.append(AgentEvent(
                            session_id=session.session_id,
                            turn_index=turn,
                            event_type="tool_completed",
                            payload={"tool_call_id": tool_call.id, "content": result_msg, "error": True}
                        ))
                        continue

                    # 2. Idempotency Key Injection
                    idempotency_key = self._generate_idempotency_key(
                        session.session_id, turn, tool_call.name, tool_call.arguments
                    )
                    tool_call.arguments["_idempotency_key"] = idempotency_key

                    # 3. Tool Execution via MCP
                    self.event_store.append(AgentEvent(
                        session_id=session.session_id,
                        turn_index=turn,
                        event_type="tool_executing",
                        payload={"tool": tool_call.name, "arguments": tool_call.arguments}
                    ))

                    tool_span = None
                    if self.tracer:
                        tool_span = self.tracer.start_span(f"gen_ai.tool.{tool_call.name}", attributes={
                            "gen_ai.tool.name": tool_call.name,
                            "idempotency_key": idempotency_key
                        })

                    tool_result = self.mcp_client.execute_tool(tool_call.name, tool_call.arguments)

                    if tool_span:
                        tool_span.end()

                    # 4. Append Tool Result
                    session.messages.append(Message(
                        role="tool",
                        tool_call_id=tool_call.id,
                        content=tool_result.content
                    ))
                    self.event_store.append(AgentEvent(
                        session_id=session.session_id,
                        turn_index=turn,
                        event_type="tool_completed",
                        payload={
                            "tool_call_id": tool_call.id,
                            "content": tool_result.content,
                            "error": tool_result.is_error
                        }
                    ))

                # Checkpoint turn
                self.event_store.save_checkpoint(session)
                if span:
                    span.end()

            else:
                # No more tools -> Terminal response reached
                session.messages.append(Message(role="assistant", content=response.content))
                session.status = "completed"
                self.event_store.append(AgentEvent(
                    session_id=session.session_id,
                    turn_index=turn,
                    event_type="session_completed",
                    payload={"final_answer": response.content}
                ))
                self.event_store.save_checkpoint(session)
                if span:
                    span.end()
                return response.content or "Task completed."

        if session.current_turn >= session.max_turns:
            session.status = "failed"
            self.event_store.append(AgentEvent(
                session_id=session.session_id,
                turn_index=session.current_turn,
                event_type="session_failed",
                payload={"error": "Maximum iteration limit reached. Halting to prevent infinite loop."}
            ))
            return "Execution stopped: maximum iteration limit reached."

        return "Session paused or ended."
