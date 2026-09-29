# Phase 05: AI Security & Guardrails — Standardized Refactoring Report

**Refactoring Date**: September 2026  
**Curriculum Architect**: AI Curriculum Architect  
**Target Scope**: `05-ai-security-and-guardrails/`  
**Governing Standard**: `references/quality-gates.md` (13-Point Quality Gate & 9-Section Report Standard)

---

## 1. Curriculum Changes
* **Decomposed Monolith into 7 Modular Lessons**: Replaced the unsegmented **1,259-line (71 KB) monolithic `README.md`** with an authoritative **7-lesson curriculum**, a lean **Phase Hub `README.md`**, and dedicated references.
* **Preserved 100% of Existing Technical Assets ("Zero-Loss Guarantee")**: Every formula, architecture diagram, failure mode, and runnable code implementation from the original file was preserved, expanded, and mapped to a specific modular lesson.
* **Added Dedicated AI Red Teaming Lesson**: Created **Lesson 07** (`07-ai-red-teaming-and-vulnerability-evaluation.md`) to operationalize the 20-vector Capstone attack benchmark suite into automated CI/CD release gates with **Promptfoo**, **Microsoft PyRIT**, and **NVIDIA Garak**.
* **Elevated Regulated AI & Explainable AI**: Moved algorithmic fairness (Fairlearn) and TreeSHAP adverse action notice generation into a standalone deep-dive lesson (**Lesson 06**), preserving its high-value mathematical and Python code assets without cluttering runtime prompt injection defenses.
* **Integrated 2026 Industry Security Standards**:
  - Upgraded threat modeling to the **OWASP Top 10 for LLM Applications 2026 Edition** (grounded in 7,714 analyzed incidents).
  - Introduced the **OWASP Top 10 for Agentic Applications (2026)** (ASI01 to ASI10).
  - Introduced the **OWASP Model Context Protocol (MCP) Security Top 10** for tool-binding defense.
* **Structured 2 Distinct Learning Pathways**: Added role-tailored tracks in the Phase Hub:
  - *Track A: Application Security & Tool Gateway Architect* (Lessons 01, 02, 03, 04, 05, 07, Capstone).
  - *Track B: Enterprise Regulated AI, FinTech & Compliance Architect* (Lessons 01, 02, 03, 04, 06, 07, Capstone).

---

## 2. Content Changes
* **Beginner AI Scaffolding with Senior Systems Rigor**: In strict accordance with the instructional requirement, every AI-specific term or acronym is expanded upon first mention with an intuitive, beginner-friendly mental model:
  - *Large Language Model (LLM)*: Explained as a probabilistic state machine where inputs and control instructions share the same memory buffer.
  - *In-Context Learning (ICL)*: Explained as dynamic runtime parameter injection into the prompt buffer.
  - *Natural Language Inference (NLI)*: Explained as automated contract assertion testing comparing an API response against a specification.
  - *Greedy Coordinate Gradient (GCG)*: Explained as query payload fuzzing targeting transformer attention weights.
  - *Tree Shapley Additive Explanations (TreeSHAP)*: Explained as distributed tracing calculating the exact contribution of each feature to a score.
  - *Model Context Protocol (MCP)*: Explained as standardized microservice API contracts over JSON-RPC 2.0.
  - *Small Language Model (SLM)*: Explained as a high-throughput edge proxy filter (e.g., Envoy) executing sub-25ms pre-flight inspection.
* **Zero Meta-Directive Leaks**: Purged all 23 instances of leaked author planning tags (`[MUST-HAVE] 🔴`, `[GOOD-TO-KNOW] 🟡`) from headings and callouts.
* **Pure Markdown & Zero-LaTeX Conversion**: Converted all 11 raw LaTeX expressions (`$$...$$`, `$...$`, `\Delta_{\text{DP}}`, `\phi_i(x)`, `\arg\max`) into clean text code blocks and native Unicode symbols (`DIR ≥ 0.80`, `Δ_DP ≤ 0.10`, `Δ_EO ≤ 0.05`).
* **Production Failure Modes Paired to Lessons**: Distributed the 5 original production anti-patterns into dedicated sections across their relevant lessons:
  - *Anti-Pattern 1 (Raw String Concatenation & Delimiter Blindness)* → Lesson 02.
  - *Anti-Pattern 2 (Naked Shell / Dynamic SQL Tool Execution)* → Lesson 05.
  - *Anti-Pattern 3 (Security Through Obscurity in System Prompts)* → Lesson 01.
  - *Anti-Pattern 4 (Autonomous State Mutation Without Re-Authentication)* → Lesson 05.
  - *Anti-Pattern 5 (Embedding-Only Search Vulnerability to RAG Injection)* → Lesson 02.

---

## 3. Advanced Content Added
* **Tiered Latency-Aware Guardrail Pipelines**: Formally specified the 3-tier production latency architecture balancing safety and SLAs:
  - *Tier 0 (<1ms)*: Deterministic regex and token bounds.
  - *Tier 1 (10–25ms)*: High-speed SLMs using **Google ShieldGemma 2B** and **Meta Prompt Guard**.
  - *Tier 2 (100–300ms)*: Deep categorical moderation using **Meta Llama Guard 3 (1B/8B/11B Vision)** and **NVIDIA NeMo Colang 2.0**.
* **Model Context Protocol (MCP) Protocol-Level Security**: Formulated defenses against tool poisoning (shadowing legitimate tools with malicious definitions), rogue MCP servers, scope creep, and unvetted sampling requests.
* **Declarative CI/CD Security Release Gates with Promptfoo**: Provided complete `promptfooconfig.yaml` suites and GitHub Actions workflow configurations (`.github/workflows/ai-security-eval.yml`) asserting zero tolerance for security regressions.
* **Multi-Turn Adaptive Red Teaming with Microsoft PyRIT**: Documented programmatic Python scripts orchestrating multi-turn adversarial exploit graphs against autonomous agents.
* **Multimodal Visual Injections**: Detailed visual injection mechanics including low-contrast OCR evasion, transparent font injection, and adversarial pixel perturbations.

---

## 4. Diagram Changes
* **Prose Walkthroughs Added for All 15 Diagrams**: Every Mermaid diagram across the phase now includes a complete, numbered, step-by-step prose walkthrough explaining data flows, security boundaries, and failure edges:
  1. *Traditional Computing vs. LLM Computing* (Lesson 01).
  2. *Von Neumann vs. Harvard Architecture Duality* (Lesson 01).
  3. *Lead Architect's Trust Boundary Model* (Lesson 01 & Hub).
  4. *OWASP Agentic Security Threat Spectrum* (Lesson 01).
  5. *Indirect Prompt Injection Workflow* (Lesson 02).
  6. *Extrinsic vs. Intrinsic Hallucination Taxonomy* (Lesson 03).
  7. *Active NLI Verification Loop* (Lesson 03).
  8. *Context-Free Grammar (CFG) Logit Masking* (Lesson 03).
  9. *Multi-Layer Guardrail Defense Pipeline* (Lesson 04 & Hub).
  10. *Tiered Latency Budget Pipeline* (Lesson 04).
  11. *The Confused Deputy Attack Flow* (Lesson 05).
  12. *Dual-LLM Privilege Separation Topology* (Lesson 05).
  13. *Dual-LLM Execution Sequence Diagram* (Lesson 05).
  14. *Two-Phase HITL Cryptographic HMAC Token Proposal* (Lesson 05).
  15. *The Regulated Applicant Pipeline & TreeSHAP Attribution Bridge* (Lesson 06).

---

## 5. Duplication Removed
* **Eliminated Redundant Framework Listings**: Replaced scattered, duplicated descriptions of Llama Guard and NeMo with a unified, comparative tradeoff matrix in Lesson 04.
* **Resolved Conceptual Overlap Between Ingress and Tool Execution**: Clearly separated prompt-level input validation (Lessons 02 & 04) from agentic tool execution proxies (Lesson 05).
* **Consolidated Anti-Patterns**: Removed duplicate failure mode descriptions and integrated each directly into the lesson introducing the defensive mechanism.

---

## 6. Files Changed

| File Path | Action | Description |
|---|:---:|---|
| `05-ai-security-and-guardrails/PHASE_5_AUDIT.md` | **Created** | Comprehensive phase and curriculum audit report. |
| `05-ai-security-and-guardrails/PHASE_5_RESEARCH.md` | **Created** | Frontier research scout documenting 2026 industry standards. |
| `05-ai-security-and-guardrails/FINDINGS_VALIDATION.md` | **Created** | Formal findings validation and conflict resolution report. |
| `05-ai-security-and-guardrails/PHASE_5_REFACTORING_PLAN.md` | **Created** | Merged refactoring plan with line-by-line zero-loss migration mapping. |
| `05-ai-security-and-guardrails/01-threat-modeling-and-owasp-top-10.md` | **Created** | Lesson 01: Attention plane duality, OWASP LLM 2026, and Agentic ASI01–10. |
| `05-ai-security-and-guardrails/02-prompt-injection-defenses-and-jailbreaks.md` | **Created** | Lesson 02: Injections, GCG suffixes, dynamic XML delimiters, canary honeytokens. |
| `05-ai-security-and-guardrails/03-hallucination-mitigation-and-active-grounding.md` | **Created** | Lesson 03: Extrinsic vs intrinsic, offset citations, NLI loops, CFG decoding. |
| `05-ai-security-and-guardrails/04-guardrail-architectures-and-defensive-pipelines.md` | **Created** | Lesson 04: Tiered latency pipelines, ShieldGemma, Llama Guard 3, NeMo Colang. |
| `05-ai-security-and-guardrails/05-defensive-agent-architecture-and-privilege-separation.md` | **Created** | Lesson 05: Dual-LLM quarantine, least agency, WASM sandboxes, MCP security. |
| `05-ai-security-and-guardrails/06-regulated-ai-bias-mitigation-and-explainable-ai.md` | **Created** | Lesson 06: EU AI Act, Fairlearn CI/CD suite, TreeSHAP + bounded adverse action code. |
| `05-ai-security-and-guardrails/07-ai-red-teaming-and-vulnerability-evaluation.md` | **Created** | Lesson 07: Automated red teaming with Garak, PyRIT, and Promptfoo CI/CD gates. |
| `05-ai-security-and-guardrails/README.md` | **Updated** | Modernized Phase Hub with Master Lesson Directory and Learning Tracks. |
| `05-ai-security-and-guardrails/REFACTORING_REPORT.md` | **Created** | Standardized 9-section refactoring report. |
| `05-ai-security-and-guardrails/examples/guardrail_pipeline.py` | **Preserved** | Python multi-stage guardrail pipeline implementation. |
| `05-ai-security-and-guardrails/examples/GuardrailMiddleware.cs` | **Preserved** | C# ASP.NET Core Semantic Kernel guardrail middleware implementation. |
| `05-ai-security-and-guardrails/labs/capstone-security-guardrails.md` | **Preserved** | Capstone specification and 20-vector adversarial attack benchmark suite. |

---

## 7. Link Changes
* **Reciprocal Navigation Footers**: Added standard `## 🧭 Navigation` footers (`[← Previous]`, `[Phase Hub]`, `[Next →]`, `[Capstone Lab]`) across all 7 modular lessons.
* **Internal Anchor Updates**: Replaced broken internal anchor links from the old monolith with direct relative links to the modular lesson files.
* **Verified Lab and Example Links**: Cross-referenced `labs/capstone-security-guardrails.md` and `examples/` across the relevant lessons and the Phase Hub.

---

## 8. Cross-Phase Changes
* **Upstream Continuity (Phase 03 & 04)**: Bound Lesson 05 directly to Phase 03's Model Context Protocol (MCP) wire protocol lessons and Phase 04's autonomous ReAct loops.
* **Downstream Continuity (Phase 06)**: Connected Lesson 07's Promptfoo CI/CD assertions to Phase 06's LLM-as-a-judge evaluation frameworks and OpenTelemetry distributed tracing conventions.

---

## 9. Remaining Recommendations
* **Automated CI/CD Execution**: Consider adding a sample GitHub Actions workflow runner in `.github/workflows/` that executes `test_fairness_cicd.py` and `promptfooconfig.yaml` in local development environments.
* **Llama Guard 3 Vision Lab Extension**: Future lab iterations could incorporate an optional multimodal challenge testing defense against low-contrast OCR invoice injections.
