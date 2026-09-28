"""
Trace and Cost Exporter for AgentForge Observability.
Formats OpenTelemetry GenAI spans into visual ASCII trees and audit reports.
"""

from typing import List, Dict, Any
from .tracer import Span

class ConsoleTraceExporter:
    @staticmethod
    def render_tree(span: Span, indent: int = 0) -> str:
        prefix = "  " * indent + "├── " if indent > 0 else "📦 "
        attr_summary = []
        if "gen_ai.request.model" in span.attributes:
            attr_summary.append(f"model={span.attributes['gen_ai.request.model']}")
        if "gen_ai.tool.name" in span.attributes:
            attr_summary.append(f"tool={span.attributes['gen_ai.tool.name']}")
        if "idempotency_key" in span.attributes:
            attr_summary.append(f"key={span.attributes['idempotency_key']}")
        if "gen_ai.usage.input_tokens" in span.attributes:
            attr_summary.append(f"tokens={span.attributes['gen_ai.usage.input_tokens']}in/{span.attributes.get('gen_ai.usage.output_tokens',0)}out")

        attr_str = f" [{', '.join(attr_summary)}]" if attr_summary else ""
        lines = [f"{prefix}{span.name} ({span.duration_ms:.1f}ms){attr_str}"]

        for child in span.children:
            lines.append(ConsoleTraceExporter.render_tree(child, indent + 1))

        return "\n".join(lines)

    @staticmethod
    def print_trace_summary(root_spans: List[Span]) -> None:
        print("\n" + "=" * 80)
        print("🔍 OPENTELEMETRY GenAI DISTRIBUTED TRACE WATERFALL")
        print("=" * 80)
        for root in root_spans:
            print(ConsoleTraceExporter.render_tree(root))
        print("=" * 80 + "\n")
