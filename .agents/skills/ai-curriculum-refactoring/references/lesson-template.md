# Standard Lesson Anatomy & Template Guide

This document defines the **11-Part Default Lesson Structure**, depth tier parameters, word count budgets, and split/merge rules.  
Remember: **This is a default structure, not a rigid checklist.** Omit or merge sections that do not add value for a specific topic.

---

## 🏷️ Depth Tier Parameters & Word Count Budgets

Every lesson must target a specific depth tier and respect its cognitive word budget:

| Tier | Badge | Word Budget | Focus & Scope |
|---|---|---|---|
| **Tier 1** | `🟢 Core` | ~800–1,500 words | Single core concept, intuition, failure of naive approach, working baseline implementation. |
| **Tier 2** | `🟡 Engineering Depth` | ~1,200–2,500 words | Architectural core: edge cases, failure modes, scale constraints, concurrency, and OTel telemetry. |
| **Tier 3** | `🔵 Advanced` | ~1,500–3,000 words | High-scale or specialized production patterns (speculative decoding, GraphRAG, distributed sagas). |
| **Tier 4** | `⚫ Deep Dive` | ~1,500–3,000 words | Internal mechanics, mathematical proofs, hardware memory layouts, wire protocols. |

---

## ✂️ Split & Merge Rules (Section 27 Standard)

To maintain optimal cognitive load and reading momentum:

### When to Split a Lesson:
- **Word Count Exceeded**: The lesson exceeds ~3,500 words without justification.
- **Multiple Core Primitives**: The lesson attempts to teach two or more major architectural primitives simultaneously (e.g. teaching BM25, HNSW, and Cross-Encoders in a single monolithic file).
- **Split Strategy**: Divide into a `🟢 Core` conceptual introduction followed by one or more `🟡 Engineering Depth` or `⚫ Deep Dive` implementation files.

### When to Merge Lessons:
- **Fragmented Stubs**: Adjacent files are under ~500 words and cover trivial fragments of the same concept.
- **Artificial Separation**: Splitting the "theory" and "code" into separate disconnected markdown files when they belong in the same unified narrative arc.
- **Merge Strategy**: Consolidate into a single coherent `🟢 Core` or `🟡 Engineering Depth` lesson.

---

## 📋 The Parameterized 11-Part Anatomy

```markdown
# Lesson <XX>: <Clear, Specific Title>

> **[Tier: 🟢 Core | 🟡 Engineering Depth | 🔵 Advanced | ⚫ Deep Dive]**  
> **One-sentence executive summary defining the engineering objective.**

---

## 🎯 What You Will Learn
- Specific architectural capability (e.g., *Phase 00: Calculate KV cache memory footprint per concurrent session*, *Phase 02: Implement hybrid RRF retrieval*, *Phase 04: Build an event-sourced agent state machine*, *Phase 05: Build a dual-LLM quarantine pipeline*, *Phase 07: Tune vLLM continuous batching*)
- Specific failure mode avoided (e.g., *Prevent GPU memory allocation blowout*, *Prevent exact identifier loss in vector space*, *Prevent infinite agent loops and budget loss*, *Prevent prompt injection data leaks*)
- Trade-off mastered (e.g., *Balance latency vs. precision*, *Token spend vs. context window size*, *Throughput vs. model perplexity*)

---

## 1. The Problem
Describe the production scenario that necessitates this pattern.
- What engineering requirement, traffic load, or business constraint triggers the need?
- What happens if we do nothing or rely on standard application logic?

---

## 2. The Core Idea & Why Naive Fails
The fundamental technical solution and the post-mortem of naive attempts.
- State the solution clearly without wrapping it in buzzwords.
- Explain why the intuitive/naive implementation breaks at scale (e.g., OOM crashes, semantic drift on exact IDs, unbounded agent loops).
- **Why the Problem Exists**: Root constraints (hardware memory bandwidth, quadratic attention complexity, non-deterministic token generation).

---

## 3. Mental Model
An intuitive conceptual bridge for experienced software engineers.
- Compare to traditional engineering concepts (e.g., database indexes, caching tiers, network protocols, message brokers, compiler ASTs, DMZ perimeters).
- Use a crisp text diagram or miniature Mermaid diagram to anchor the mental model.

---

## 4. How It Works (Step-by-Step Mechanics)
Step-by-step technical mechanics.
- Ingestion, indexing, scoring, network wire exchange, or state transition flow.
- Numbered sequence showing exact data transformations from input to output.

---

## 5. Concrete Scenario & Code Example
A realistic, production-relevant enterprise example (finance, healthcare, legal, e-commerce, developer infrastructure).
- Clean, type-annotated Python (Pydantic v2, Python 3.12+).
- Illustrates the core algorithm, schema, or protocol without depending on bloated external frameworks.

---

## 6. Engineering Solutions & Production Patterns
The battle-tested architectural improvements.
- Algorithmic refinements (e.g., PagedAttention, Reciprocal Rank Fusion, WAL event logging, Dual-LLM quarantine, Continuous Batching).
- How state is persisted, quarantined, or validated.

---

## 7. Architecture & Telemetry View
End-to-end distributed system topology.
- Mermaid flowchart or sequence diagram with clear data flows.
- **Visual Walkthrough**: Step-by-step numbered prose explanation of the diagram.
- **OpenTelemetry Spans**: Code sample showing OTel GenAI semantic conventions in practice.

---

## 8. Common Failure Modes & Anti-Patterns
A structured matrix or list of real-world landmines:
- **Anti-Pattern 1**: Description, root cause, and engineering fix.
- **Anti-Pattern 2**: Description, root cause, and engineering fix.

---

## 9. Production View & Evaluation
How to evaluate and benchmark this component in production:
- **Key Metrics**: Latency (p50/p95/p99), cost per 1k requests, throughput, groundedness/faithfulness score.
- **Automated CI/CD Evaluation**: How to test this component automatically before deployment (e.g., synthetic datasets, LLM-as-a-judge regression gates).

---

## 10. When Should You Use It? (Trade-off Matrix)
A concise decision matrix guiding when to adopt, when to avoid, and what alternatives exist:
- Latency vs. precision.
- Dollar cost vs. accuracy.
- Hardware dependencies (GPU VRAM vs. CPU RAM).

---

## 💡 11. Interview Perspective (Optional / Recommended)
3–5 senior architectural interview questions and justification models:
- **Question 1**: *"How would you design a system that handles X constraint under Y load?"*
- **Architectural Justification**: Clear defense of the trade-off, failure modes, and recovery strategies.

---

## 12. Key Takeaways & Verified Resources
- 3–4 bulleted principles to remember.
- Primary source references: original research papers (arXiv links), official specs, authoritative provider documentation.

---

## 🧭 Navigation (Mandatory)
- **[← Previous Lesson: <Title>](./<prev-lesson>.md)**
- **[Phase <XX> Hub](./README.md)**
- **[Next Lesson: <Title> →](./<next-lesson>.md)**
- **[Capstone Lab: <Title>](./labs/<lab-file>.md)**
```

---

## ✂️ Structural Flexibility Guidelines

| Section | Can be Omitted When... | Can be Merged When... |
|---|---|---|
| **3. Mental Model** | The concept is a direct extension of an already-covered mental model. | Merged with **2. The Core Idea** for concise lessons. |
| **Why Naive Fails** | The topic is an extension of an existing pattern rather than a replacement. | Merged with **1. The Problem** if the problem *is* the failure of the naive approach. |
| **7. Architecture View** | The topic is an algorithmic or mathematical utility (e.g., BM25 formula) rather than a distributed service. | Integrated into **4. How It Works**. |
| **9. Evaluation** | The component is purely infrastructural (e.g. token counting utility). | Merged with **7. Telemetry View**. |
| **11. Interview Perspective** | The lesson is a brief reference or foundational primer. | Omitted in Tier 1 (`🟢 Core`) lessons when covered in adjacent engineering depth lessons. |

---

## 🚫 Formatting & Math Guidelines (Zero LaTeX)

All lesson markdown files must render without requiring KaTeX/MathJax plugins:
- **No LaTeX Math Blocks**: Never use `$$...$$` or `$...$`.
- **Formulas**: Place mathematical equations in fenced text blocks (```text).
- **Symbols**: Use standard Unicode (`→`, `⟷`, `Σ`, `≈`, `α`, `≤`, `≥`, `×`, `Δ`).
- **Complexity**: Write `O(N)` and `O(log N)` directly as monospace text.
- **Tables**: Use standard Markdown pipe tables; avoid LaTeX arrays or unescaped `$$` cost indicators.
- **Zero Meta-Directive Leaks**: Never include internal directives, quality gate reminders, or refactoring tags in learner-facing section titles or prose (e.g. do NOT name a section `### The Attention Formula (Zero-LaTeX):` or `### Step 1 (Refactored)`). Write clean, authoritative titles (`### The Attention Formula`).
