# Quality Gates & Verification Standards

This document establishes the **Dual-Lens Quality Review** and **13-Point Quality Gate Checklist** used by the `ai-curriculum-architect` in **VALIDATION MODE** prior to finalizing any refactored lesson or phase.

---

## 👓 The Dual-Lens Quality Review

Every lesson and phase must pass inspection through two distinct reviewer perspectives before the 13-point checklist is applied:

### Lens A: The AI Learner (Senior / Staff Software Engineer Transitioning to AI)
The learner approaches the material with deep engineering maturity but healthy skepticism toward AI hype:
- **"Do I understand *why* this problem exists and why my current toolkit fails?"**  
  *The lesson must not assume compliance; it must show why standard relational queries, synchronous APIs, or deterministic caches fail.*
- **"Is the mental model intuitive and grounded in systems I already understand?"**  
  *The bridge between Software 2.0 and Software 3.0 must be explicit (e.g. KV Cache ⟷ Paged Memory; Vector Index ⟷ Inverted Index).*
- **"Can I take this architecture and code and adapt it to my production systems tomorrow?"**  
  *No toy pseudocode. Code must use Python 3.12+, typed Pydantic v2 schemas, and standard production error handling.*
- **"Did this teach me what fails in production so my on-call rotation isn't a nightmare?"**  
  *The failure modes, anti-patterns, and edge cases must be candidly discussed.*

### Lens B: The Senior Systems Architect (Principal / Staff AI Architect Reviewer)
The architect reviews the material for technical rigor, scalability, and lasting durability:
- **"Are the trade-offs technically accurate, honest, and defensible?"**  
  *No silver bullets. Every architectural pattern must display its latency, compute, memory, and cost costs.*
- **"Is this free of vendor marketing, transient framework trivia, and ephemeral hype?"**  
  *Concepts, wire protocols (JSON-RPC, SSE), and algorithms must take precedence over wrapper libraries.*
- **"Are memory footprint, latency budgets, and hardware physics acknowledged?"**  
  *GPU VRAM, KV cache growth, network serialization overhead, and batching constraints must be respected.*
- **"Does this meet enterprise engineering standards for production AI infrastructure?"**  
  *Zero-trust security boundaries, OpenTelemetry distributed tracing, and automated evaluation gates must be integrated.*

---

## 🚦 The 13-Point Quality Checklist

| # | Inspection Dimension | Acceptance Criteria | Failure Symptoms |
|---|---|---|---|
| **01** | **Learning Objective** | Clear, outcome-oriented architectural objective at the top. | Vague intro ("In this section we talk about RAG"). |
| **02** | **Prerequisites** | All prerequisite concepts have been taught in earlier lessons/phases. | Introducing KV cache eviction without explaining token generation. |
| **03** | **Terminology Control** | All acronyms expanded on first use; concept explained before name. | Unanchored acronym soup (`HNSW + RRF + CRAG`). |
| **04** | **Conceptual Progression** | Follows natural arc: Problem → Why Naive Fails → Mental Model → Solution → Trade-offs. | Jumping straight to code without explaining the problem. |
| **05** | **Technical Depth** | Deep systems mechanics preserved (algorithms, protocols, math). | Superficial bullet points that sound like marketing copy. |
| **06** | **Conciseness** | Low fluff; high signal-to-noise ratio. | 500 words of passive prose explaining a 50-word concept. |
| **07** | **Diagram Value** | Visual topology with step-by-step prose walkthrough. Multi-subgraph diagrams must use `flowchart TD` with symmetric column pinning (`~~~`) or explicit node-to-node edges to guarantee flush vertical stacking. Subgraph ID chaining (`A --> B --> C`) is strictly prohibited. | Giant unannotated spaghetti diagram, diagram without text, subgraph ID chaining, or disconnected subgraphs cascading diagonally into a staircase. |
| **08** | **Code Integrity** | Python 3.12+, Pydantic v2 schemas, type-annotated, runnable. | Untyped `dict` payloads, pseudo-code with broken syntax. |
| **09** | **Trade-off Analysis** | Explicit matrix comparing latency, cost, recall, and complexity. | Blanket claims like "this approach is always best." |
| **10** | **Production & Failures** | Concrete failure modes, anti-patterns, and OTel telemetry. | Happy-path only; no discussion of errors or rate limits. |
| **11** | **Link Integrity** | All relative Markdown links resolve to real files and line anchors. | Broken `404` relative paths to non-existent markdown files. |
| **12** | **Surrounding Fit** | Lesson connects cleanly to preceding and succeeding lessons in the phase. | Standalone essay with no clear entry or exit point. |
| **13** | **Zero-LaTeX & Clean Markdown** | Pure GitHub Flavored Markdown (GFM). Zero LaTeX delimiters (`$$`, `$`, `\frac`, `\begin{array}`). Formulas in text code blocks; Unicode symbols (`→`, `⟷`, `Σ`, `≈`, `α`). Zero meta-directive leaks: no internal directives, compliance tags, or quality labels (`(Zero-LaTeX)`, `(Pure Markdown)`, `(Refactored)`, `[MUST-HAVE]`) in learner-facing headings or prose. | Broken math rendering, raw LaTeX tags, or internal agent directives/tags visible in standard previewers. |

---

## 🔍 Defect Classification & Severity Triage

When reporting audit findings in **VALIDATION MODE**, group issues into three tiers:

### 🔴 Critical (Blocks Merge)
- Factual technical inaccuracies or non-functional code examples.
- Missing core prerequisites that make comprehension impossible.
- Broken file links or non-existent lab references.
- Inclusion of raw LaTeX math delimiters (`$$`, `$`, `\frac`, etc.) or unescaped multiple dollar signs that break standard Markdown previewers.
- Leaking internal meta-directives, refactoring tags, or compliance labels (`(Zero-LaTeX)`, `(Refactored)`, `[MUST-HAVE]`) into learner-facing headings or text.
- Unbounded loops or security anti-patterns presented as best practices.

### 🟡 Important (Requires Remediation)
- Diagram present without an accompanying prose walkthrough.
- Acronym introduced without explanation on first mention.
- Missing failure-mode analysis or lack of a trade-off table.
- Monolithic README exceeding 500 lines without modular lesson breakdown.
- Lesson exceeding word budget (>3,500 words) without justification.

### 🟢 Minor (Editorial Polish)
- Minor formatting inconsistencies or markdown linting warnings.
- Stylistic phrasing that could be more concise.
- Supplementary resource link could be updated to a newer version.
