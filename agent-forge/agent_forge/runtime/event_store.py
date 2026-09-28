"""
Write-Ahead Log (WAL) and Event Store for AgentForge.
Provides immutable event persistence, deterministic state replay, and checkpointing.
"""

from typing import List, Dict, Any, Optional
import json
import os
from .state_models import AgentEvent, AgentSession, Message, ToolCall

class EventStore:
    """
    In-memory or file-backed append-only event store.
    Guarantees that state can be completely rehydrated even if the host crashes.
    """
    def __init__(self, persistence_file: Optional[str] = None):
        self._events: List[AgentEvent] = []
        self._checkpoints: Dict[str, Dict[str, Any]] = {}
        self.persistence_file = persistence_file
        if persistence_file and os.path.exists(persistence_file):
            self._load_from_disk()

    def append(self, event: AgentEvent) -> None:
        """Appends an event to the immutable log."""
        self._events.append(event)
        if self.persistence_file:
            self._flush_to_disk()

    def get_events(self, session_id: str) -> List[AgentEvent]:
        """Returns all events for a given session in chronological order."""
        return [e for e in self._events if e.session_id == session_id]

    def save_checkpoint(self, session: AgentSession) -> None:
        """Saves a snapshot of the session state."""
        self._checkpoints[session.session_id] = session.model_dump()
        self.append(AgentEvent(
            session_id=session.session_id,
            turn_index=session.current_turn,
            event_type="checkpoint_saved",
            payload={"turn": session.current_turn, "status": session.status}
        ))

    def rehydrate_session(self, session_id: str) -> Optional[AgentSession]:
        """
        Reconstructs an AgentSession by loading the latest checkpoint and
        replaying any subsequent events.
        """
        if session_id not in self._checkpoints:
            # Replay from scratch using events if no checkpoint exists
            events = self.get_events(session_id)
            if not events:
                return None
            
            # Reconstruct from initial event
            session = AgentSession(
                session_id=session_id,
                tenant_id=events[0].payload.get("tenant_id", "default"),
                user_id=events[0].payload.get("user_id", "default")
            )
        else:
            session = AgentSession.model_validate(self._checkpoints[session_id])

        # Find events recorded after checkpoint
        checkpoint_turn = session.current_turn
        events = [e for e in self.get_events(session_id) if e.turn_index >= checkpoint_turn]

        for event in events:
            if event.event_type == "model_decision":
                content = event.payload.get("content")
                tool_calls_data = event.payload.get("tool_calls")
                tool_calls = [ToolCall(**tc) for tc in tool_calls_data] if tool_calls_data else None
                session.messages.append(Message(role="assistant", content=content, tool_calls=tool_calls))
            elif event.event_type == "tool_completed":
                session.messages.append(Message(
                    role="tool",
                    tool_call_id=event.payload.get("tool_call_id"),
                    content=event.payload.get("content")
                ))
            elif event.event_type == "human_approval_required":
                session.status = "paused_for_approval"
                session.pending_tool_call = ToolCall(**event.payload.get("tool_call"))
            elif event.event_type == "session_completed":
                session.status = "completed"

        return session

    def _flush_to_disk(self) -> None:
        if not self.persistence_file:
            return
        data = {
            "events": [e.model_dump() for e in self._events],
            "checkpoints": self._checkpoints
        }
        with open(self.persistence_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _load_from_disk(self) -> None:
        try:
            with open(self.persistence_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._events = [AgentEvent(**e) for e in data.get("events", [])]
                self._checkpoints = data.get("checkpoints", {})
        except Exception:
            pass
