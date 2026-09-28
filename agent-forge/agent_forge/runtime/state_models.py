"""
Core data models and state representations for AgentForge runtime.
Uses Pydantic for validation, schema enforcement, and serialization.
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
import time
import uuid

class ToolCall(BaseModel):
    id: str = Field(default_factory=lambda: f"call_{uuid.uuid4().hex[:8]}")
    name: str
    arguments: Dict[str, Any]

class ToolResult(BaseModel):
    tool_call_id: str
    name: str
    content: str
    is_error: bool = False
    execution_time_ms: float = 0.0

class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None
    timestamp: float = Field(default_factory=time.time)

class AgentEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:10]}")
    session_id: str
    turn_index: int
    event_type: Literal[
        "session_started",
        "turn_started",
        "model_decision",
        "tool_executing",
        "tool_completed",
        "human_approval_required",
        "checkpoint_saved",
        "session_completed",
        "session_failed"
    ]
    timestamp: float = Field(default_factory=time.time)
    payload: Dict[str, Any] = Field(default_factory=dict)

class AgentSession(BaseModel):
    session_id: str
    tenant_id: str
    user_id: str
    status: Literal["running", "paused_for_approval", "completed", "failed"] = "running"
    current_turn: int = 0
    max_turns: int = 10
    messages: List[Message] = Field(default_factory=list)
    variables: Dict[str, Any] = Field(default_factory=dict)
    pending_tool_call: Optional[ToolCall] = None
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
