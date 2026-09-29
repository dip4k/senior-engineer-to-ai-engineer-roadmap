# Phase 06: Evals, Observability & Telemetry — Refactoring Report

**Refactoring Date**: September 2026  
**Architect**: AI Curriculum Architect  
**Governing Standard**: `references/quality-gates.md`, `references/curriculum-principles.md`, and `references/lesson-template.md`  
**Execution Scope**: `06-evals-and-observability/`  
**Status**: COMPLETE & VERIFIED  

---

## 1. Curriculum Changes

1. **Decomposed 878-Line Monolith into 7 Modular Lessons**: The single unmaintainable monolithic `README.md` has been successfully restructured into seven standalone, logically sequenced lessons adhering to the 4-tier depth model and 11-part lesson anatomy.
2. **Established Clear Modular Phase Progression**:
   - `01-evaluation-hierarchy-and-deterministic-testing.md` (Tier 1: 🟢 Core)
   - `02-model-based-evaluations-and-judge-architectures.md` (Tier 2: 🟡 Engineering Depth)
   - `03-agent-trajectory-and-state-mutation-evaluations.md` (Tier 2: 🟡 Engineering Depth)
   - `04-evaluation-datasets-and-synthetic-data-curation.md` (Tier 2: 🟡 Engineering Depth)
   - `05-opentelemetry-distributed-tracing-and-agent-spans.md` (Tier 2: 🟡 Engineering Depth)
   - `06-telemetry-metrics-cost-governance-and-golden-signals.md` (Tier 2: 🟡 Engineering Depth)
   - `07-continuous-monitoring-drift-detection-and-canaries.md` (Tier 3: 🔵 Advanced)
   - `labs/capstone-cicd-evaluation-pipeline.md` (Tier 2: 🟡 Capstone Lab)
3. **Dedicated Phase Hub**: Replaced the monolithic essay in `README.md` with an architectural Phase Hub featuring a Master Lesson Navigation Table, Direct Chapter Directory, Cross-Phase Prerequisites, and Curated Bibliography.

---

## 2. Content Changes

1. **Level 1 Deterministic Assertions Expanded**: Elevated Level 1 unit assertions with Pydantic v2 validation, regex format matching, execution latency and token budget bounds, and Abstract Syntax Tree (AST) validation for generated Python code (`ast.parse`) and SQL queries.
2. **Model-Based LLM-as-a-Judge Restructured**: Transformed subjective prompt advice into a rigorous engineering discipline: discrete binary pass/fail rubrics, G-Eval Chain-of-Thought (CoT) reasoning, and the reference-free RAGAS triad (Faithfulness, Relevance, Precision).
3. **Judge Bias Mitigations Formalized**: Replaced vague suggestions with concrete engineering protocols: order-swapped double scoring `(A, B)` and `(B, A)` to neutralize up to 65% position bias, and length-controlled penalty rubrics for verbosity bias.
4. **Golden Dataset Quadrants & Flywheel**: Reorganized test set curation around the 50/25/15/10 operational quadrant distribution (Happy Path, Edge Cases, Adversarial, Known Production Regressions) and an automated production trace anomaly harvesting flywheel.
5. **Modernized Capstone Challenge**: Upgraded the automated CI/CD evaluation runner to Python 3.12+, removed simulated hardcoded sleep latencies, and streamlined the GitHub Actions workflow.

---

## 3. Advanced Content

1. **Statistical Judge Calibration (Cohen’s Kappa & Krippendorff’s Alpha)**: Introduced formal chance-adjusted agreement mathematics ($\kappa \ge 0.80$ production threshold) to detect class-imbalance illusions in LLM judge benchmarks.
2. **Specialized Open-Weight Judge Models**: Integrated open-weight evaluator models (**Prometheus-2**, **M-Prometheus**, **Athene-70B**) to slash evaluation latency and API cost.
3. **Agent Trajectory & State Mutation Mathematics**: Implemented step count DAG efficiency formulas, loop/thrashing cycle detectors, and direct environment state mutation verifiers (database rows, git diffs, HTTP status codes).
4. **Modern 2026 Agent Benchmarks**: Integrated **SWE-bench Verified** (500 human-verified GitHub issues), **TAU-bench** (Sierra/Stanford dynamic enterprise tool use), and the **UK AISI Inspect AI** framework.
5. **Mid-2026 OpenTelemetry GenAI Dedicated Registry (`semantic-conventions-genai` v1.42.0+)**: Implemented official Agent attributes (`gen_ai.agent.name`, `id`, `version`, `description`), W3C `traceparent` context propagation across microservices, message queues, and Model Context Protocol (MCP) channels, and streaming span lifecycles.
6. **Streaming Latency Dynamics & Prefix Caching Physics**: Added Inter-Token Latency (ITL) variance, TTFC vs TTFT differentiation, and prompt prefix caching economics (75–90% cost savings on Anthropic, OpenAI, Gemini).
7. **Tri-Partite Drift Detection & Automated Canaries**: Formulated tabular Population Stability Index (PSI), embedding centroid drift via Maximum Mean Discrepancy (MMD), and implemented automated hourly LLM canary probes to detect silent provider model updates.

---

## 4. Diagram Changes

1. **Continuous Evaluation Flywheel** (`README.md` & `Lesson 01`): Flowchart showing anomaly ingestion, OTel observability, hierarchical evals, and deterministic release confidence, supplemented by a 4-step prose walkthrough.
2. **Inverted Filtering Funnel** (`Lesson 01`): Visualizing the compilation gate from Level 1 deterministic code (<1ms) to Level 2 LLM judges, supplemented by a 5-step prose walkthrough.
3. **Calibrated LLM Judge Engine** (`Lesson 02`): Multi-stage pipeline covering input ingestion, G-Eval CoT, bias mitigations, and Cohen's Kappa calibration gate, supplemented by a 3-step prose walkthrough.
4. **Pairwise Position Bias Resolver** (`Lesson 02`): Dual-inference order-swapping workflow resolving position bias, supplemented by a 4-step prose walkthrough.
5. **Agent Trajectory Evaluation Plane** (`Lesson 03`): Execution trace inspection vs. 4 quantitative trajectory dimensions, supplemented by a 3-step prose walkthrough.
6. **Agent Span Waterfall** (`Lesson 03`): Reconstructing the DAG of an agent's multi-step tool calls and state verifications, supplemented by a 5-step prose walkthrough.
7. **Production Data Quality Flywheel** (`Lesson 04`): Automated mining of production trace anomalies, PII redaction, human tagging, and CI/CD regression gating, supplemented by a 4-step prose walkthrough.
8. **Evol-Instruct Diversification Tree** (`Lesson 04`): In-depth and in-breadth mutation of seed prompts, supplemented by a structured walkthrough.
9. **Curation Pipeline & Split Architecture** (`Lesson 04`): Partitioning into Train/Dev (70%) and Held-Out (30%) sets with Canary Strings, supplemented by a 3-step prose walkthrough.
10. **Agent Distributed Trace Span Hierarchy** (`Lesson 05`): Nested parent-child span tree with W3C `traceparent` propagation, supplemented by a 5-step prose walkthrough.
11. **W3C TraceContext Propagation Across MCP** (`Lesson 05`): Sequence diagram tracing context across API gateway, orchestrator, and Model Context Protocol stdio/SSE channels, supplemented by a 5-step prose walkthrough.
12. **The Six Golden Signals** (`Lesson 06`): Topological chart of TTFT, TPS, Cache Hit Ratio, Token Ratio, Fallback Rate, and Cost, supplemented by a 6-step prose walkthrough.
13. **Streaming Metrics Telemetry Flow** (`Lesson 06`): Sequence diagram tracing browser chunks, TTFT arrival, ITL jitter, and OTel export, supplemented by a 4-step prose walkthrough.
14. **Hybrid ML + GenAI Telemetry Architecture** (`Lesson 07`): Connecting classical MLflow scoring with OpenTelemetry agent spans, supplemented by a 5-step prose walkthrough.
15. **Hourly LLM Canary Audit Loop** (`Lesson 07`): Sequence diagram detailing background probe sweeps detecting silent provider drift, supplemented by a 4-step prose walkthrough.
16. **Capstone CI/CD Gate Architecture** (`labs/capstone-cicd-evaluation-pipeline.md`): End-to-end evaluation flow from benchmark ingestion to exit code gating, supplemented by a 6-step prose walkthrough.

---

## 5. Duplication Removed

1. **Eliminated Redundant Theoretical Summaries**: Removed fragmented, repeated definitions of Level 1 assertions, binary rubrics, and golden datasets that previously cluttered multiple subheadings in the monolith.
2. **Unified Failure Modes & Anti-Patterns**: Rather than isolating anti-patterns at the end of a monolithic document, each anti-pattern is now embedded directly into its relevant lesson (e.g. Likert scale trap in Lesson 02, Blind Agent trap in Lesson 03, Test Set Contamination in Lesson 04).
3. **Cleaned Telemetry Specs**: Consolidated disparate discussions of latency, token usage, and caching into a unified analysis of the Six Golden Signals in Lesson 06.

---

## 6. Files Changed

| File Path | Action | Description |
|---|:---:|---|
| `06-evals-and-observability/PHASE_6_AUDIT.md` | **CREATED** | Comprehensive 6-dimension audit report with Zero-LaTeX and meta-directive analysis. |
| `06-evals-and-observability/PHASE_6_RESEARCH.md` | **CREATED** | Controlled frontier research report on 2026 OTel specs, judge calibration, and benchmarks. |
| `06-evals-and-observability/FINDINGS_VALIDATION.md` | **CREATED** | Formal reconciliation, zero-loss content action matrix, and beginner terminology scaffolding plan. |
| `06-evals-and-observability/PHASE_6_REFACTORING_PLAN.md` | **CREATED** | Complete modular refactoring plan detailing lesson anatomy and migration mappings. |
| `06-evals-and-observability/PLAN_VALIDATION.md` | **CREATED** | 13-Point Quality Gate verification report approving plan execution. |
| `06-evals-and-observability/01-evaluation-hierarchy-and-deterministic-testing.md` | **CREATED** | Lesson 01: Evaluation hierarchy, Level 1 assertions, Pydantic v2, AST parsing, DeepEval. |
| `06-evals-and-observability/02-model-based-evaluations-and-judge-architectures.md` | **CREATED** | Lesson 02: Binary rubrics, G-Eval CoT, bias mitigations, Cohen's Kappa, Prometheus-2. |
| `06-evals-and-observability/03-agent-trajectory-and-state-mutation-evaluations.md` | **CREATED** | Lesson 03: Trajectory dimensions, tool precision, SWE-bench Verified, TAU-bench, Inspect AI. |
| `06-evals-and-observability/04-evaluation-datasets-and-synthetic-data-curation.md` | **CREATED** | Lesson 04: Golden quadrants, anomaly flywheel, Evol-Instruct, canary strings, Goodhart's Law. |
| `06-evals-and-observability/05-opentelemetry-distributed-tracing-and-agent-spans.md` | **CREATED** | Lesson 05: OTel dedicated registry (v1.42.0+), agent spans, W3C traceparent, APM comparison. |
| `06-evals-and-observability/06-telemetry-metrics-cost-governance-and-golden-signals.md` | **CREATED** | Lesson 06: Six Golden Signals, streaming ITL variance, prefix cache economics, cost SLAs. |
| `06-evals-and-observability/07-continuous-monitoring-drift-detection-and-canaries.md` | **CREATED** | Lesson 07: Tri-partite drift, PSI math, MMD embeddings, MLflow bridge, hourly canaries. |
| `06-evals-and-observability/README.md` | **REWRITTEN** | Modernized Phase Hub with Master Navigation Table, direct chapter links, and bibliography. |
| `06-evals-and-observability/labs/capstone-cicd-evaluation-pipeline.md` | **UPDATED** | Upgraded to Python 3.12+, added prose walkthrough, updated reciprocal lesson links. |
| `06-evals-and-observability/examples/README.md` | **UPDATED** | Updated to Python 3.12+ and added cross-lesson navigation anchors. |
| `06-evals-and-observability/REFACTORING_REPORT.md` | **CREATED** | This 9-section standardized post-refactoring report. |

---

## 7. Link Changes

1. **Reciprocal Lesson Navigation**: Every lesson file now terminates with reciprocal Markdown links to `[← Previous Lesson]`, `[Phase Hub]`, `[Next Lesson →]`, and `[Capstone Lab]`.
2. **Internal Anchors Restored**: Fixed legacy broken anchor references in `labs/capstone-cicd-evaluation-pipeline.md` and `examples/README.md`, re-pointing them to canonical modular lesson paths (`01-*.md`, `02-*.md`, etc.).
3. **Phase Hub Master Directory**: Updated all table of contents entries in `README.md` to point directly to the individual lesson files.

---

## 8. Cross-Phase Changes

1. **Upstream Alignment (Phases 00–05)**:
   - Grounded Lesson 06 prefix caching economics directly in Phase 00 (KV Cache memory physics).
   - Grounded Lesson 01 schema assertions directly in Phase 01 (Constrained decoding and JSON Schemas).
   - Grounded Lesson 02 reference-free scoring directly in Phase 02 (RAG retrieval and chunking).
   - Grounded Lesson 03 and Lesson 05 tool tracing directly in Phase 03 (Model Context Protocol JSON-RPC).
   - Grounded Lesson 03 multi-turn trajectory evaluation in Phase 04 (Stateful ReAct agent loops).
   - Grounded Lesson 04 adversarial quadrant curation in Phase 05 (Security and prompt injection defenses).
2. **Downstream Enablement (Phases 07–08)**:
   - Provided telemetry metrics, TTFT budgets, and prefix caching baselines required for **Phase 07: High-Throughput Serving & LLMOps** (vLLM continuous batching, PagedAttention, and model gateways).
   - Provided automated regression gates and CI/CD workflows required for **Phase 08: AI-Augmented SDLC & Leadership**.

---

## 9. Remaining Recommendations

1. **Optional Runnable Pytest Harness**: In a future lab enhancement, scaffold a local Docker container running an OTel collector connected to an in-memory Arize Phoenix instance for live trace visualization during student lab exercises.
2. **Integration with Agent-Forge Framework**: Cross-link Phase 06 telemetry bridges to the repository's `agent-forge/` microservices runtime once Phase 07 serving refactoring is completed.
