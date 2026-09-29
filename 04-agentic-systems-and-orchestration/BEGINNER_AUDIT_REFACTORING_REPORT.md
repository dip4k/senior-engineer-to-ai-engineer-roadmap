# Phase 04 — Beginner AI Engineer Remediation: Refactoring Report

> **Mode**: REFACTOR | **Date**: 2026-09-29 | **Scope**: Phase 04 Lessons 01–06, README  
> **Trigger**: PHASE_04_BEGINNER_AI_AUDIT.md findings

---

## 1. Curriculum Changes

No structural changes. Lesson sequence (01–07) is unchanged. All changes are inline content improvements.

## 2. Content Changes

### CRITICAL Fix: Inline AI Terminology Definitions at First-Use Sites

| Lesson | Terms Defined | Implementation |
|---|---|---|
| **Lesson 01** | Language Model (LLM / Foundation Model), Token, Context Window, Hallucination, AI Agent | Added "Key AI Terms for This Lesson" subsection after Core Concept — 5 clear definitions with analogies and concrete examples |
| **Lesson 02** | Temperature | Added blockquote definition before Progressive Budget Decay table where temperature values appear without explanation |
| **Lesson 04** | Embedding (Vector Representation), Cosine Similarity | Added "Key AI Terms for This Section" subsection before Long-Term Memory section where code uses `embedding: List[float]` and cosine similarity |
| **Lesson 05** | Auto-Regressive Generation, Self-Attention, Attention Diffusion | Added "Key AI Terms for This Lesson" subsection after Core Concept with concrete analogies |

### IMPORTANT Fix: Anthropomorphic Language Replaced

| File | Line | Original | Fixed |
|---|---|---|---|
| Lesson 01 | 16 | "The model guesses database IDs" | "The model generates statistically plausible but non-existent database IDs" |
| Lesson 01 | 17 | "model repeatedly calls" | "model continues generating tool calls" |
| Lesson 01 | 18 | "A small misunderstanding" | "A small erroneous inference" |
| Lesson 02 | 25 | "the language model does not stop" | "the language model continues generating tool calls...because from the model's perspective, a failed observation is simply more input text to respond to" |
| Lesson 02 | 26 | "model begins to lose track" | "model assigns lower attention probability...a phenomenon researchers call 'Lost in the Middle'" |
| Lesson 02 | 55 | Diagram: "(The Brain)" | Diagram: "(Reasoning Engine)" |
| Lesson 02 | 64 | Prose: "The Model (The Brain)" | Prose: "The Model (The Reasoning Engine)" |
| Lesson 02 | 66 | "reflects on observations" | "processes observations" |
| Lesson 02 | 154 | "a model reasons without tools" | "a model generates text without access to tools, it has no mechanism to verify" |
| Lesson 02 | 239 | "still being mentally stuck" | "still producing semantically equivalent queries that make no real progress" |
| Lesson 04 | 47 | "model misses key instructions" | "model assigns lower attention probability to instructions positioned in the middle" |

### IMPORTANT Fix: LaTeX Leak

| File | Line | Original | Fixed |
|---|---|---|---|
| Lesson 01 | 584 | `($0.95^{10}$)` | `(0.95^10 ≈ 59.9%)` |

### IMPORTANT Fix: Backslash-Escaped Dollar Signs

| File | Lines | Original | Fixed |
|---|---|---|---|
| Lesson 02 | 177, 179 | `\$570`, `\$0.04` | `$570`, `$0.04` |

## 3. Advanced Content

No new advanced content added. Existing technical depth preserved.

## 4. Diagram Changes

| Diagram | Change |
|---|---|
| Lesson 02: Harness vs Loop flowchart | Updated `"Foundation Language Model (The Brain)"` → `"Foundation Language Model (Reasoning Engine)"` |

## 5. Duplication Removed

None — no duplication was identified in the audit.

## 6. Files Changed

| File | Type | Changes |
|---|---|---|
| `01-workflows-vs-agents-and-orchestration-patterns.md` | Modified | Added AI term definitions (5 terms), fixed anthropomorphic language (4 instances), fixed LaTeX leak |
| `02-react-loops-and-execution-governors.md` | Modified | Added transition bridge, temperature definition, fixed anthropomorphic language (6 instances), fixed diagram label, fixed backslash-dollar |
| `03-stateful-sessions-and-durable-wal-persistence.md` | Modified | Added transition bridge from Lesson 02 in Core Concept |
| `04-agent-memory-systems-and-cognitive-architectures.md` | Modified | Added transition bridge from Lesson 03, embedding/cosine similarity definitions, fixed "Lost in the Middle" explanation |
| `05-multi-agent-coordination-and-a2a-protocols.md` | Modified | Added transition bridge, 3 AI term definitions (auto-regressive, self-attention, attention diffusion), fixed "hallucinate" wording |
| `06-codeact-and-sandboxed-execution-runtimes.md` | Modified | Added Core Concept with transition bridge from Lesson 05 |
| `README.md` | Modified | Fixed jargon in prose walkthrough (expanded abbreviations, replaced "cryptographic governors" with plain language) |

## 7. Link Changes

No link changes. All relative paths verified intact.

## 8. Cross-Phase Changes

None. All changes are internal to Phase 04.

## 9. Remaining Recommendations

1. **Lesson 02, Section 5 (Grok-3 / Llama Stack)**: Still feels disconnected from the loop engineering topic. Consider relocating to Lesson 07 as an appendix or callout box (MINOR priority).
2. **Lesson 07 docstring**: Contains backticks inside Python docstring (`CreditRequest`) which causes false positives in markdown code block extraction validators. Not a functional issue — Python code is valid.
3. **Standardized LLM/Foundation Model terminology**: First use in Lesson 01 now defines all three terms as synonyms. Remaining lessons should use "language model" consistently. This is tracked as MINOR.
