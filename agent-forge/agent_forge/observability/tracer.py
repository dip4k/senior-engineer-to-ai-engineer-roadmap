"""
OpenTelemetry GenAI Semantic Conventions Tracer for AgentForge.
Provides standardized distributed tracing for LLM inference, tool execution,
hybrid retrieval, and agent turn loops.
"""

from typing import Dict, Any, List, Optional
import time
import uuid

class Span:
    def __init__(self, name: str, parent: Optional["Span"] = None, attributes: Optional[Dict[str, Any]] = None):
        self.span_id: str = f"span_{uuid.uuid4().hex[:8]}"
        self.name: str = name
        self.parent: Optional["Span"] = parent
        self.children: List["Span"] = []
        self.attributes: Dict[str, Any] = attributes or {}
        self.start_time: float = time.time()
        self.end_time: Optional[float] = None
        self.duration_ms: float = 0.0

        if parent:
            parent.children.append(self)

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value

    def end(self) -> None:
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000.0

class GenAITracer:
    def __init__(self, service_name: str = "agent-forge-platform"):
        self.service_name = service_name
        self.root_spans: List[Span] = []
        self._current_span: Optional[Span] = None

    def start_span(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> Span:
        span = Span(name=name, parent=self._current_span, attributes=attributes)
        if not self._current_span:
            self.root_spans.append(span)
        self._current_span = span
        return span

    def end_span(self, span: Span) -> None:
        span.end()
        if self._current_span == span:
            self._current_span = span.parent
