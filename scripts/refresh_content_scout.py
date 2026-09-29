#!/usr/bin/env python3
"""
Repository Content Scout & Gap Analyzer
=======================================
Autonomous tool for scanning the Ai_Native_Engineer repository, formulating
targeted search queries to discover emerging AI engineering developments,
comparing current coverage against the frontier landscape, and generating
a structured Content Refresh & Gap Analysis Report.

Supports:
- Antigravity / Gemini Agentic IDE
- Claude Code CLI
- GitHub Copilot Chat
- Standalone CLI execution
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Domain radar categories to track
RADAR_CATEGORIES = {
    "models_and_reasoning": {
        "title": "Foundation Models & Reasoning Paradigms",
        "search_queries": [
            "latest LLM reasoning models test-time compute 2025 2026",
            "Claude Sonnet Opus reasoning updates Anthropic",
            "OpenAI o3 o4 mini reasoning token mechanics",
            "DeepSeek R1 V3 open weights architecture",
            "speculative decoding test time scaling advancements"
        ],
        "keywords": [
            "reasoning tokens", "thinking tokens", "test-time compute", "chain-of-thought",
            "distillation", "deepseek-r1", "claude 3.7", "claude 4", "o3-mini", "o4-mini",
            "mcts", "speculative decoding", "reinforcement learning from verifiable rewards"
        ]
    },
    "context_engineering": {
        "title": "Context Engineering & Memory Architecture",
        "search_queries": [
            "context engineering prompt caching KV cache optimization 2025 2026",
            "long context compaction context AST hierarchical memory LLM",
            "memory-as-a-service production agent state architecture",
            "late chunking contextual retrieval embedding techniques"
        ],
        "keywords": [
            "context engineering", "kv-cache", "prompt caching", "context ast",
            "hierarchical memory", "compaction", "late chunking", "contextual retrieval",
            "semantic cache", "working memory", "long-term memory", "maas"
        ]
    },
    "protocols_and_mcp": {
        "title": "Protocols & Wire Standards (MCP, A2A, AG-UI)",
        "search_queries": [
            "Model Context Protocol MCP specification updates 2025 2026",
            "Agent to Agent protocol A2A Google Linux Foundation",
            "AG-UI agent user interface streaming protocol standard",
            "MCP enterprise security OAuth sandboxing transport SSE"
        ],
        "keywords": [
            "model context protocol", "mcp", "json-rpc 2.0", "a2a", "ag-ui",
            "tools/call", "resources/read", "prompts/get", "sse transport",
            "stdio transport", "oauth 2.0 mcp", "tool sandboxing"
        ]
    },
    "agentic_orchestration": {
        "title": "Multi-Agent Systems & Orchestration Runtimes",
        "search_queries": [
            "multi-agent orchestration production patterns LangGraph Swarm AutoGen 2026",
            "write-ahead log agent state persistence crash recovery WAL",
            "supervisor worker agent choreography deterministic FSM",
            "action fingerprinting loop prevention progressive budget decay"
        ],
        "keywords": [
            "orchestrator", "supervisor", "swarm", "langgraph", "autogen", "crewai",
            "write-ahead log", "wal", "event sourcing", "fsm", "state machine",
            "action fingerprint", "budget decay", "human-in-the-loop"
        ]
    },
    "security_and_guardrails": {
        "title": "AI Security, Threat Mitigation & Defense",
        "search_queries": [
            "dual-LLM quarantine architecture indirect prompt injection",
            "OWASP Top 10 for LLM Applications 2025 2026 updates",
            "model output firewall crypto-shredding privacy PII scrubbing",
            "adversarial red teaming autonomous agent safety guardrails"
        ],
        "keywords": [
            "dual-llm quarantine", "indirect prompt injection", "jailbreak", "owasp",
            "output firewall", "crypto-shredding", "pii masking", "guardrails",
            "least privilege", "tool execution policy", "taint tracking"
        ]
    },
    "evals_and_observability": {
        "title": "Evaluation, Observability & Telemetry",
        "search_queries": [
            "OpenTelemetry GenAI semantic conventions 2025 2026",
            "LLM-as-a-judge binary evals groundedness answer relevance",
            "agent trajectory evaluation step level grading",
            "production LLM observability tracing Langfuse Arize Phoenix"
        ],
        "keywords": [
            "opentelemetry", "otel genai", "semantic conventions", "llm-as-a-judge",
            "groundedness", "faithfulness", "answer relevance", "trajectory eval",
            "span attributes", "eval gates", "ci/cd evals", "synthetic test generation"
        ]
    },
    "production_llmops": {
        "title": "Production Deployment & Serving (LLMOps)",
        "search_queries": [
            "vLLM SGLang high throughput production serving inference 2025 2026",
            "model gateway semantic caching rate limiting cost routing",
            "prefix caching hardware aware inference GPU memory management",
            "fine-tuning vs RAG vs prompt engineering cost latency tradeoff"
        ],
        "keywords": [
            "vllm", "sglang", "model gateway", "semantic cache", "rate limiting",
            "cost-aware routing", "prefix caching", "batch api", "speculative decoding",
            "gpu vram", "pagedattention"
        ]
    },
    "governance_and_sdlc": {
        "title": "Governance, EU AI Act & AI-Augmented SDLC",
        "search_queries": [
            "EU AI Act General Purpose AI GPAI enforcement guidelines 2025 2026",
            "ISO 42001 AI management system enterprise compliance audit",
            "autonomous agentic coding Claude Code Cursor Windsurf workflows",
            "AI native engineering team structure tech lead transition"
        ],
        "keywords": [
            "eu ai act", "gpai", "iso 42001", "compliance", "audit trail",
            "ai-augmented sdlc", "claude code", "cursor", "windsurf", "tech lead transition"
        ]
    }
}


def scan_repository(repo_root: Path) -> Dict[str, Set[str]]:
    """
    Scans the repository markdown and python files to index covered keywords
    and identify existing architectural topics.
    """
    found_keywords = {category: set() for category in RADAR_CATEGORIES}
    
    # Target files to index
    target_patterns = [
        "README.md",
        "*.md",
        "0*/**/*.md",
        "agent-forge/**/*.py",
        "labs/*.md",
        "use-cases/*.md",
        "interview/*.md"
    ]
    
    all_files = []
    for pattern in target_patterns:
        all_files.extend(repo_root.glob(pattern))
    
    # Deduplicate files
    unique_files = {f.resolve(): f for f in all_files if f.is_file()}.values()
    
    for file_path in unique_files:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore").lower()
            for cat_id, cat_info in RADAR_CATEGORIES.items():
                for kw in cat_info["keywords"]:
                    if kw.lower() in content:
                        found_keywords[cat_id].add(kw)
        except Exception as e:
            continue
            
    return found_keywords


def generate_search_query_plan() -> List[Dict]:
    """Generates the list of search queries with intended category targets."""
    plan = []
    for cat_id, cat_info in RADAR_CATEGORIES.items():
        for query in cat_info["search_queries"]:
            plan.append({
                "category": cat_id,
                "category_title": cat_info["title"],
                "query": query
            })
    return plan


def analyze_gaps(found_keywords: Dict[str, Set[str]]) -> Dict[str, Dict]:
    """Computes coverage stats and highlights uncovered focus areas."""
    analysis = {}
    for cat_id, cat_info in RADAR_CATEGORIES.items():
        total_kw = set(cat_info["keywords"])
        covered_kw = found_keywords.get(cat_id, set())
        missing_kw = total_kw - covered_kw
        coverage_pct = (len(covered_kw) / len(total_kw) * 100) if total_kw else 0
        
        analysis[cat_id] = {
            "title": cat_info["title"],
            "total_count": len(total_kw),
            "covered_count": len(covered_kw),
            "missing_count": len(missing_kw),
            "coverage_pct": round(coverage_pct, 1),
            "covered": sorted(list(covered_kw)),
            "missing": sorted(list(missing_kw)),
            "search_queries": cat_info["search_queries"]
        }
    return analysis


def generate_markdown_report(repo_root: Path, analysis: Dict[str, Dict]) -> str:
    """Formats the gap analysis and scout recommendations into an actionable report."""
    lines = [
        "# 📡 AI Engineering Repository Content Scout & Gap Analysis Report",
        "",
        "> **Automated Frontier Radar & Curriculum Freshness Audit**  ",
        f"> **Generated for Repository**: `{repo_root.name}`  ",
        "> **Standard**: Late 2025 – 2026/2027 Production Systems Engineering Standard",
        "",
        "---",
        "",
        "## 📊 Domain Coverage Overview",
        "",
        "| Category | Coverage Score | Covered Keypoints | Identified Gaps / Refresh Targets |",
        "|:---|:---:|:---:|:---:|"
    ]
    
    for cat_id, data in analysis.items():
        status_emoji = "🟢" if data["coverage_pct"] >= 80 else ("🟡" if data["coverage_pct"] >= 50 else "🔴")
        lines.append(
            f"| **{data['title']}** | {status_emoji} {data['coverage_pct']}% "
            f"({data['covered_count']}/{data['total_count']}) | "
            f"{', '.join(data['covered'][:4])}... | "
            f"{', '.join(data['missing']) if data['missing'] else 'Full baseline coverage'} |"
        )
        
    lines.extend([
        "",
        "---",
        "",
        "## 🔍 Category Deep-Dives & Targeted Search Queries",
        "",
        "Use the provided queries with your agent's `search_web` tool or web browser to discover the newest specifications, SDK releases, and architectural patterns:",
        ""
    ])
    
    for cat_id, data in analysis.items():
        lines.append(f"### 🎯 {data['title']}")
        lines.append(f"- **Coverage**: `{data['coverage_pct']}%` ({data['covered_count']}/{data['total_count']} radar concepts detected)")
        if data["missing"]:
            lines.append(f"- **Missing / Refresh Topics**: `{'`, `'.join(data['missing'])}`")
        else:
            lines.append("- **Status**: Excellent foundational coverage.")
        lines.append("- **Recommended Web Search Queries**:")
        for q in data["search_queries"]:
            lines.append(f"  - 🔎 `\"{q}\"`")
        lines.append("")
        
    lines.extend([
        "---",
        "",
        "## 🛠️ Recommended Action Plan for Content Refresher Agent",
        "",
        "1. **Execute Web Searches**: Run the high-priority queries above using the agent's web search capability.",
        "2. **Cross-Check Specs**: Compare latest official docs (Anthropic MCP docs, Linux Foundation A2A, OpenAI o3/o4 API guides, OpenTelemetry GenAI semantic conventions).",
        "3. **Update Core Files**:",
        "   - Add new terminology to [ai-engineering-glossary-by-practice.md](./ai-engineering-glossary-by-practice.md).",
        "   - Expand relevant phase READMEs (e.g. `03-tools-and-model-context-protocol` or `04-agentic-systems-and-orchestration`).",
        "   - Update or add code examples in `agent-forge/` or `labs/`.",
        "4. **Run Verification**: Ensure all agent forge tests continue to pass (`python -m unittest agent-forge/tests/test_all.py`).",
        ""
    ])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AI Engineering Repo Content Scout & Gap Analyzer")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")
    parser.add_argument("--output", default="CONTENT_REFRESH_REPORT.md", help="Output path for markdown report")
    parser.add_argument("--queries-only", action="store_true", help="Print web search queries as JSON and exit")
    parser.add_argument("--summary", action="store_true", help="Print summary table to stdout")
    args = parser.parse_args()
    
    repo_root = Path(args.repo_root).resolve()
    
    if args.queries_only:
        queries = generate_search_query_plan()
        print(json.dumps(queries, indent=2))
        return
        
    found_keywords = scan_repository(repo_root)
    analysis = analyze_gaps(found_keywords)
    report = generate_markdown_report(repo_root, analysis)
    
    output_path = repo_root / args.output
    output_path.write_text(report, encoding="utf-8")
    print(f"✅ Gap analysis report successfully written to: {output_path}")
    
    if args.summary:
        print("\n=== Coverage Summary ===")
        for cat_id, data in analysis.items():
            print(f"[{data['coverage_pct']:>5.1f}%] {data['title']} (Missing: {len(data['missing'])})")


if __name__ == "__main__":
    main()
