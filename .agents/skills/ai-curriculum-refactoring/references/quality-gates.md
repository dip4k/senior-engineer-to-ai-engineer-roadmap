# Quality Gates & Verification Standards

This document establishes the **Dual-Lens Quality Review** and **15-Point Quality Gate Checklist** used by the `ai-curriculum-architect` in **VALIDATION MODE** prior to finalizing any refactored lesson or phase.

---

## 👓 The Dual-Lens Quality Review

Every lesson and phase must pass inspection through two distinct reviewer perspectives before the 13-point checklist is applied:

### Lens A: The AI Learner (Software Engineer, New to AI Terminology)
The learner knows software engineering vocabulary well but has never met AI terms such as token, embedding, or attention. Test every paragraph by asking: "Could this reader follow it if they had never heard any AI term before this lesson?"
- **"Is every AI term defined in plain English before it is used?"**  
  *If the learner must look a word up elsewhere, the lesson fails this lens.*
- **"Does the explanation pass the 'Coffee Test' and `<prose_mechanics>`?"**  
  *If a sentence exceeds 28 words, stacks multiple academic adjectives (e.g. 'token arrays fed to a probabilistic autoregressive model'), or relies on passive academic nouns instead of plain software action verbs, the lesson fails this lens. Depth comes from failure modes, memory math, and code—never from academic vocabulary.*
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

## 🚦 The 15-Point Quality Checklist

| # | Inspection Dimension | Acceptance Criteria | Failure Symptoms |
|---|---|---|---|
| **01** | **Learning Objective** | Clear, outcome-oriented architectural objective at the top. | Vague intro ("In this section we talk about RAG"). |
| **02** | **Prerequisites & Term Ledger** | All prerequisite concepts have been taught in earlier lessons/phases. The lesson header lists `New AI terms introduced` and `AI terms assumed from earlier lessons`; every AI term used appears in one of the two lists and the assumed ones link to where they are taught. | Introducing KV cache eviction without explaining token generation; an AI term used with no definition and no ledger entry. |
| **03** | **Terminology & Prose Control** | Every AI term gets a plain-English definition and analogy on first use (software terms are not re-explained); all acronyms expanded on first use; concept explained before name; lesson titles and main headings avoid unexpanded abbreviations; strictly obeys `<prose_mechanics>` (max 28 words/sentence, active voice, zero academic jargon stacking). | Unanchored acronym soup (`HNSW + RRF + CRAG`), isolated abbreviations in titles (`# BM25 and HNSW`), run-on sentences (>28 words), or academic jargon stacking (`probabilistic autoregressive model`). |
| **04** | **Intuition & Progression (Tripartite Arc)** | Starts with an accessible mental model / analogy (ELI10); applies the Tripartite Pedagogy rhythm (🧒 Analogy → ⚙️ Engineering Mechanics → ⚠️ What happens if you skip this?); every analogy ends with a "where this analogy breaks" note; includes an Old vs Modern evolution table when a real naive predecessor exists; concludes with "Quick Check to See if it Clicked" (mandatory). | Dense academic jargon dump without an intuitive mental model, missing the failure mode analysis, or jumping straight to code without cognitive grounding. |
| **05** | **Technical Depth** | Deep systems mechanics preserved (algorithms, protocols, math). | Superficial bullet points that sound like marketing copy. |
| **06** | **Conciseness & Structural Flexibility** | Low fluff; high signal-to-noise ratio. Prose word count is within the declared tier budget (Tier 1: 800–1,500; Tier 2: 1,200–2,500; Tier 3 and 4: 1,500–3,000). Non-applicable sections of the 11-part template are omitted or merged rather than padded with artificial filler. | 500 words of passive prose explaining a 50-word concept, or forcing boilerplate text to mechanically fill every template section. |
| **07** | **Diagram & Visual Styling** | Modern `flowchart TD`/`LR` with theme-adaptive contrast across both Light and Dark modes. Subgraphs must be transparent (`fill:none`), and node backgrounds must not be overridden with `fill` at all (if a custom fill is unavoidable, an explicit contrasting text `color` is mandatory). Apply high-contrast semantic borders (`stroke:#2563eb` Blue for Ingestion, `stroke:#16a34a` Green for Query/Success, `stroke:#d97706` Amber for Gates, `stroke:#dc2626` Red for Quarantine, `stroke:#7c3aed` Purple for Models). Use native Mermaid structural shapes paired with universal Unicode icons (`[("🗄️ Database")]`, `{"🛡️ Guard"}`, `["⚡ MCP"]`, `["🔌 API"]`, `["🧠 LLM"]`, `(["👤 User"])`); ban FontAwesome (`fa:fa-...`) or external web fonts. Labels use bold titles and descriptions with `<br/>`. Step-by-step prose walkthrough directly beneath. **Strict node budget: 4 to 8 nodes per diagram (max 10)**. Multi-phase or complex systems must be **split into modular, focused diagrams**. Multi-subgraph diagrams must use symmetric column pinning (`~~~`) or explicit node-to-node edges; Subgraph ID chaining (`A --> B --> C`) is strictly prohibited. **Renderer Invariants (No Broken Images / Truncation)**: Subgraph titles must be <= 35 characters to prevent SVG text clipping; ban nested `direction LR/TB` inside subgraphs (crashes Dagre/webviews); ban literal unescaped `&` in node labels (use `and` to prevent SVG XML parser errors). **Anti-Bloat Rules**: Ban cross-subgraph criss-crossing lines (spaghetti), single-node subgraph wrappers, bidirectional double-headed arrows (`<-->`, `<==>`), and backwards loops across subgraphs. | Broken diagram (syntax crash, broken image), truncated subgraph headers (`tier 1 : ...`), text overflowing diagram borders, single-node subgraph wrappers, backwards-looping edge collisions, hardcoded white/pastel fills causing invisible text or blinding glare in dark mode, diagram exceeding 10 nodes without splitting, missing prose walkthrough, subgraph ID chaining, or disconnected subgraphs cascading diagonally into a staircase. |
| **08** | **Code Integrity** | Python 3.12+, Pydantic v2 schemas, type-annotated, runnable. | Untyped `dict` payloads, pseudo-code with broken syntax. |
| **09** | **Trade-off Analysis** | Explicit matrix comparing latency, cost, recall, and complexity. | Blanket claims like "this approach is always best." |
| **10** | **Production & Failures** | Concrete failure modes, anti-patterns, and OTel telemetry. | Happy-path only; no discussion of errors or rate limits. |
| **11** | **Link Integrity** | All relative Markdown links resolve to real files and line anchors. | Broken `404` relative paths to non-existent markdown files. |
| **12** | **Surrounding Fit & Navigation** | Every lesson concludes with a standardized `## 🧭 Navigation` footer with reciprocal links (`← Previous`, `Phase Hub`, `Next →`, `Capstone Lab`). Phase README includes a Master Lesson Navigation Table and a Direct Chapter & Lesson Directory. | Standalone essay with no clear entry or exit point, missing lesson footer navigation, or phase README lacking direct chapter links. |
| **13** | **Zero-LaTeX & Clean Markdown** | Pure GitHub Flavored Markdown (GFM). Zero LaTeX delimiters (`$$`, `$`, `\frac`, `\begin{array}`). Formulas in text code blocks; Unicode symbols (`→`, `⟷`, `Σ`, `≈`, `α`). Zero meta-directive leaks: no internal directives, compliance tags, or quality labels (`(Zero-LaTeX)`, `(Pure Markdown)`, `(Refactored)`, `[MUST-HAVE]`) in learner-facing headings or prose. | Broken math rendering, raw LaTeX tags, or internal agent directives/tags visible in standard previewers. |
| **14** | **Accuracy & Verifiability** | Every number is sourced, derived, or marked *(illustrative)*; model and product names were verified in the current session and dated ("as of"); every citation and external link was opened; every code block was executed with output recorded in the report. See [accuracy-policy.md](./accuracy-policy.md). | Unlabelled statistics, invented paper titles or API fields, stale model names, code that was never run. |
| **15** | **Tier & Header Block** | Exactly one canonical tier badge (`🟢 Core`, `🟡 Engineering Depth`, `🔵 Advanced`, `⚫ Deep Dive`); header block has read time, prerequisites, Core Concept and the two term-ledger lines. See [lesson-template.md](./lesson-template.md). | Missing tier, legacy badge format, no ledger, ledger that does not match the terms actually used. |

---

## 🔍 Defect Classification & Severity Triage

When reporting audit findings in **VALIDATION MODE**, group issues into three tiers:

> **Automated vs. Human Gates**: Gates that are mechanical (word count, link integrity, LaTeX presence, term ledger format, `Last verified` age) should be run first via `scripts/validate_lesson.py`. Only the following require human judgment: (1) analogy quality and break-note, (2) trade-off honesty, (3) failure mode coverage, (4) code output correctness, (5) Quick Check quality, (6) phase fit. Run the script first; human reviewers focus on the six judgment gates.

### 🔴 Critical (Blocks Merge)
- Factual technical inaccuracies or non-functional code examples.
- Broken Mermaid diagram (syntax error, failed SVG generation, broken image icon).
- Missing core prerequisites that make comprehension impossible.
- Broken file links or non-existent lab references.
- Inclusion of raw LaTeX math delimiters (`$$`, `$`, `\frac`, etc.) or unescaped multiple dollar signs that break standard Markdown previewers.
- Leaking internal meta-directives, refactoring tags, or compliance labels (`(Zero-LaTeX)`, `(Refactored)`, `[MUST-HAVE]`) into learner-facing headings or text.
- Unbounded loops or security anti-patterns presented as best practices.
- Fabricated citation, URL, API field or model name; code block that fails when run.
- **Analogy missing its "where this analogy breaks" note.** Readers carry the analogy too far and build incorrect mental models that persist across all downstream lessons.

### 🟡 Important (Requires Remediation)
- Diagram present without an accompanying prose walkthrough.
- Diagram violating renderer invariants: subgraph titles > 35 characters (truncating/overflowing), nested `direction LR/TB` inside subgraphs, or literal `&` inside node labels.
- Diagram over 10 nodes, or bloated layout (spaghetti lines across subgraphs, single-node subgraph wrappers, backwards-looping edges across clusters).
- Acronym or AI term introduced without a plain-English definition on first mention, or missing term ledger.
- Unlabelled number presented as fact; code block never executed.
- Missing or legacy tier badge.
- Missing failure-mode analysis or lack of a trade-off table.
- Monolithic README exceeding 500 lines without modular lesson breakdown.
- Lesson exceeding its tier word budget (split it).

### 🟢 Minor (Editorial Polish)
- Minor formatting inconsistencies or markdown linting warnings.
- Stylistic phrasing that could be more concise.
- Supplementary resource link could be updated to a newer version.
