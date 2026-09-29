# Phase 01: Prompt & Context Engineering — Deep Curriculum Audit Report

> **Execution Mode**: AUDIT MODE (Read-Only Inspection)  
> **Auditor**: AI Curriculum Architect  
> **Target Phase Directory**: `01-prompt-and-context-engineering/`  
> **Date**: September 2026  
> **Target Learner**: Senior Developers, Staff Software Engineers, and Solutions Architects (7–10+ years experience) transitioning to AI Systems Engineering.  
> **Baseline Reference**: `CURRICULUM_AUDIT.md`, `CURRICULUM_REFACTORING_PLAN.md`, and the `ai-curriculum-refactoring` skill standards.

---

## 1. Executive Summary & Repository Context

A comprehensive architectural and pedagogical audit of **Phase 01 (`01-prompt-and-context-engineering`)** was executed under **AUDIT MODE**. In strict compliance with audit protocols, no curriculum lessons, labs, or supporting code files were modified.

### 1.1. Exact Directory Identification
The canonical Phase 1 directory within the repository structure is:
`c:\Repos\Ai_Native_Engineer\01-prompt-and-context-engineering\`

### 1.2. Scope of Audited Artifacts
The audit inspected the complete Phase 1 payload:
1. **Primary Courseware**: `01-prompt-and-context-engineering/README.md` (1,276 lines, 8,952 words, 77,687 bytes).
2. **Capstone Engineering Lab**: `01-prompt-and-context-engineering/labs/capstone-context-engineering-pipeline.md` (31 lines, 2,713 bytes).
3. **Reference Implementations**:
   - `01-prompt-and-context-engineering/examples/context_pipeline.py` (106 lines, Python 3.11+, Pydantic v2 + Anthropic caching).
   - `01-prompt-and-context-engineering/examples/semantic_layer_decoupling.py` (350 lines, Python 3.11+, DMN rule engine benchmark).
   - `01-prompt-and-context-engineering/examples/StrictJsonPipeline.cs` (73 lines, C# / .NET 9 Semantic Kernel).
   - `01-prompt-and-context-engineering/examples/README.md` (12 lines).

### 1.3. High-Level Audit Verdict: Monolithic Anti-Pattern with Exceptional Technical Substance
Phase 01 possesses world-class engineering intuitions: treating prompt assembly as a compiler AST, enforcing deterministic FSM logit masking over regex parsing, establishing a 4-tier compaction pipeline, and exposing the physical economics of GPU KV-cache prompt reuse.

However, Phase 01 suffers from **critical architectural, pedagogical, and structural defects**:
1. **The Monolithic README Trap**: Phase 01 contains **zero modular lesson files**. All 23 disparate topics, 14 diagrams, 4 code implementations, 3 war stories, and 2 tradeoff matrices are packed into a single 1,276-line file (8,952 words), exceeding cognitive load budgets by more than 2.5x.
2. **Inverted Conceptual Progression**: Foundational syntax primitives—such as the 4-tier enterprise role hierarchy (Section 13) and XML delimiter sandboxing (Section 12)—are taught *after* complex composite systems like Context ASTs (Section 3), Token Budgeting (Section 4), Compaction Pipelines (Section 5), and Tool Loadout Pruning (Section 8).
3. **Out-of-Scope Domain Creep**: Over 160 lines in Section 16 are devoted to an enterprise claims adjudication rule engine (DMN / Drools pattern) and data warehouse semantic layers (Cube / MetricFlow), while Section 9 introduces multi-agent routing (sub-agents, reducers) before the learner has even encountered tool wire protocols (Phase 03) or agent loops (Phase 04).
4. **Pervasive Zero-LaTeX & Markdown Preview Violations**: Over 25 raw LaTeX equations (display math blocks, inline math delimiters, fractions, approximations, multiplications, infinities) and 10+ unescaped currency dollar signs (\$10,000, \$42,000, \$120,000) break GitHub, Antigravity IDE, and standard Markdown previewers.
5. **Diagram Walkthrough Deficit**: Out of 14 Mermaid diagrams, **8 diagrams completely lack an accompanying step-by-step prose walkthrough**, directly violating Quality Gate 07.
6. **Broken Lab Navigation Anchor**: The capstone lab explicitly links back to `../README.md#10-capstone-engineering-challenge`, which is a broken anchor (`404` dead link) because the README anchor is `#23-capstone-engineering-challenge-must-have-`.
7. **Legacy Tier Taxonomy**: The phase relies on legacy `[MUST-HAVE] 🔴`, `[GOOD-TO-KNOW] 🟡`, and `[KNOWLEDGE-BASE] 🔵` labels rather than the authoritative 4-Tier Depth Model (`🟢 Core`, `🟡 Engineering Depth`, `🔵 Advanced`, `⚫ Deep Dive`).

---

## 2. Learning Analysis

### 2.1. Learning Objectives
- **Defect**: The monolithic README does not define outcome-oriented, behavioral learning objectives per topic. It features a sweeping promotional subtitle (Lines 3–4) and an executive summary, but learners are never given precise architectural contracts (e.g. *"By the end of this lesson, you will be able to design a 4-tier compaction pipeline with automated eviction thresholds and write a custom Pydantic AST compiler"*).
- **Remediation**: Every refactored modular lesson must open with a 2–3 sentence outcome-oriented architectural objective matching the golden lesson benchmark.

### 2.2. Prerequisite Knowledge & Gaps
- **Defect**: Phase 01 has zero explicit links back to Phase 00 (`00-foundations-and-token-mechanics`).
- **Missing Prerequisite Bridges**:
  - *BPE Tokenization*: Section 4 discusses token budgets (16,000 tokens), but fails to remind learners why character/word counts do not map 1:1 to tokens (established in `00/02-tokenization-and-bpe-mechanics.md`).
  - *KV-Cache Hardware Physics*: Section 15 discusses prompt caching discounts (90% savings), but does not link back to GPU High-Bandwidth Memory (HBM) bandwidth saturation, arithmetic intensity, or the prefill vs. decode lifecycle established in `00/01-transformer-and-hardware-physics.md` and `00/03-kv-cache-vram-and-bandwidth-physics.md`.
  - *Thinking / Reasoning Models*: Section 7 mentions reasoning models (DeepSeek-R1, o3-mini), but omits the hardware fact taught in `00/04-test-time-compute-and-reasoning-models.md`: hidden reasoning tokens cannot be cached across API turns and alter context budget ceilings.

### 2.3. Conceptual Progression & Cognitive Inversions
The current section ordering within `01-prompt-and-context-engineering/README.md` creates severe cognitive friction:

```text
Current Monolith Sequence:
Sec 3: Context AST 
  → Sec 4: Context Budgeting 
  → Sec 5: 4-Tier Compaction 
  → Sec 6: Lost-in-the-Middle 
  → Sec 7: Context Rot & MECW 
  → Sec 8: Tool Pruning 
  → Sec 9: Context Routing & Sub-Agents 
  → Sec 10: LLMLingua 2 
  → Sec 11: Multimodal 
  → Sec 12: XML Architecture & Delimiters 
  → Sec 13: Role Hierarchy 
  → Sec 14: Constrained Decoding (FSM) 
  → Sec 15: Prompt Caching 
  → Sec 16: Semantic Layer 
  → Sec 17: Classical Prompting (ICL, CoT)
```

**Cognitive Inversions Identified**:
1. **Delimiters after AST**: Context AST (Section 3) and Boundary Pinning (Section 6) heavily rely on XML boundaries (`<regulatory_context>`, `<user_query>`), but Enterprise XML Architecture is not introduced until Section 12!
2. **Roles after Compaction**: The 4-Tier Enterprise Role Hierarchy (`System`, `User`, `Assistant`, `Tool`) is introduced in Section 13, yet the Compaction Pipeline (Section 5) already manipulates `role: "tool"` and `role: "user"` message arrays in code on lines 278 and 1168.
3. **Classical Prompting at the End**: In-Context Learning (Few-Shot ICL) and Chain-of-Thought (CoT) appear in Section 17 as an afterthought, despite being the foundational static anchors of the Context AST Layer 1 described in Section 3.
4. **Sub-Agents before Tool Calling**: Section 9 introduces multi-agent fan-out and reducers before the learner has mastered single-turn tool calling or wire protocols.

### 2.4. Mental Models Evaluation
- **Strengths**:
  - *The Suitcase Analogy (Lines 76–91)*: Packing static boots at the bottom (cached prefix) and fresh clothes at the zipper (dynamic query) is memorable.
  - *The Compiler AST Analogy (Lines 131–136)*: Treating prompts as typed Abstract Syntax Trees rather than concatenated strings is the premier systems mental model for Software 3.0.
  - *The Financial Budget Metaphor (Lines 181–192)*: Allocating token buckets like asset classes is highly effective.
- **Weaknesses**:
  - The "ELI10 Analogy" visual callout boxes (Lines 77–91, 182–192, 369–379, 429–437, 526–535) feel condescending for a target audience of Staff and Principal Engineers (7–10+ years experience). They should be reframed as **Architectural Mental Models** or **Systems Analogies**.
  - Section 14 (Constrained Decoding) lacks a clear compiler parser metaphor (e.g. comparing Pushdown Automaton token masking to compiler lexing and token lookahead).

### 2.5. Explanation Quality & Pacing
- The core conceptual prose is authoritative and compelling.
- However, because the monolithic README isolates all runnable code (Section 21), trade-off matrices (Section 19), and war stories (Section 20) at the bottom of the document (Lines 968–1253), the individual teaching sections in lines 131–733 read as abstract theory without immediate code verification.

### 2.6. Recommended Lesson Ordering
The monolith must be decomposed into **5 focused, modular lessons** following a clean, progressive architectural arc:
1. `01-context-ast-architecture.md` (`🟢 Core`): Primitives, XML delimiters, role hierarchies, Context AST compilation, and prompt begging vs. compilable contexts.
2. `02-token-budgeting-and-compaction.md` (`🟢 Core`): Portfolio allocations (16K/32K), 4-tier compaction pipeline (prune, mask, summarize, externalize), and dynamic payload trimming.
3. `03-prefix-and-prompt-caching.md` (`🟡 Engineering Depth`): GPU KV-cache physics, contiguous prefix matching, provider mechanics (Anthropic, Gemini, OpenAI), prefix taint anti-pattern, and economic optimization.
4. `04-constrained-decoding-and-schema-fsm.md` (`🟡 Engineering Depth`): Mathematical determinism, DFA/FSM logit masking, GBNF grammars, Pydantic v2 schemas, Outlines, and over-constrained schema traps.
5. `05-mecw-and-context-rot.md` (`🔵 Advanced`): Attention dispersion physics, the U-curve (Lost-in-the-Middle), synthetic NIAH vs. multi-hop reasoning, and boundary pinning anchors.

---

## 3. Content Analysis

### 3.1. Unnecessary Verbosity & Scope Bloat
- **Monolithic Bloat**: At 8,952 words, the README is nearly 3x the recommended 3,500-word ceiling.
- **Section 16 Overgrowth**: Section 16 (*The Shared Semantic Layer & Business Logic Decoupling*, Lines 735–893) spends 158 lines explaining e-commerce return policies, damaged shipping ceilings, DMN decision tables, and Drools rules. While the architectural rule (*"Never force an autoregressive probabilistic model to store and evaluate deterministic business logic"*) is brilliant, the extended business code belongs in a dedicated example script, not in the primary context engineering guide.
- **Duplicated Code Snippets**: Compaction logic appears as a diagram (Line 247), text descriptions (Lines 267–308), and a redundant 45-line Python script (Lines 1132–1179).

### 3.2. Missing Concepts
1. **Reasoning Model Prompt Cache Invalidation**: With models like OpenAI o3-mini, Claude 3.7 Sonnet (Thinking mode), and DeepSeek-R1, reasoning/thinking tokens are generated dynamically per turn and cannot be cached. Phase 01 must explicitly document how thinking tokens impact context budgeting and cache reuse.
2. **Chunk Boundary Alignment in Implicit Caching**: OpenAI's prompt caching relies on implicit 128-token chunk boundaries. If a static prefix is 1,023 tokens (just 1 token short of 1,024), caching fails completely. This physical boundary alignment rule is missing.
3. **Automated Context Observability**: How to calculate and log context metrics (Signal-to-Noise Ratio, Cache Hit Rate %, Effective Token Ratio) using OpenTelemetry GenAI spans.
4. **Grammar Compilation Mechanics**: How JSON schemas are mathematically translated into Context-Free Grammars (CFG) or Finite State Machines (FSM) by libraries like Outlines and XGrammar.

### 3.3. Duplicated Concepts Across Phase 1 and Other Phases
- **Prompt Caching**: Explained in Section 15, repeated in Section 21.1, discussed in Section 19, and featured in War Story 1. It is also mentioned in Phase 00 (Section 3.6) and Phase 07 (Section 3.3). Phase 01 must be the authoritative home for prompt context layout and cache breakpoints.
- **Delimiter Isolation & XML**: Detailed in Section 2, Section 3, Section 6, Section 12, and Section 21.
- **Tool Loadout Pruning**: Mentioned in Section 4 (Portfolio table), Section 8 (Dedicated section), and War Story 2.

### 3.4. Concepts That Belong in Later Phases
1. **Context Routing & Sub-Agent Orchestration (Section 9, Lines 492–517)**:
   - *Audit Finding*: Teaching triage routers, sub-agent decomposition (Security Auditor vs. Database Architect), and reducer synthesis nodes in Phase 01 is premature.
   - *Remediation*: **MOVE** to Phase 04 (`04-agentic-systems-and-orchestration`), where multi-agent supervisor and hierarchical routing topologies are systematically taught.
2. **Dynamic Tool Loadout Pruning (Section 8, Lines 404–489)**:
   - *Audit Finding*: Section 8 mounts tools with `ToolDefinition(handler: Callable)`. Managing tool schemas, execution loops, and error dispatching belongs fundamentally in Phase 03 (`03-tools-and-model-context-protocol`).
   - *Remediation*: **SIMPLIFY & MOVE**. Keep the context budget perspective in Phase 01 Lesson 02 (capping tool schema tokens); move the tool registry and execution engine to Phase 03.
3. **Enterprise Semantic Layer & DMN Rule Engine (Section 16, Lines 735–893)**:
   - *Audit Finding*: Detailed integration with business rule management systems (Drools, DMN) and data warehouse semantic layers (Cube, MetricFlow) distracts from the core LLM context runtime.
   - *Remediation*: **SIMPLIFY & MOVE**. Retain the core principle (*"LLM as Semantic Extractor, Code as Deterministic Adjudicator"*) in Lesson 01 as an architectural pattern; preserve the complete 350-line benchmark in `examples/semantic_layer_decoupling.py`.

### 3.5. Advanced Material Introduced Too Early
- **Multimodal Context Assembly (Section 11, Lines 555–591)**: Detailed pixel tiling formulas (OpenAI 512 × 512 tile math, Anthropic ceil((W × H) / 750)) are introduced before the learner has mastered text-based schema decoding and prefix caching. This should be moved to an optional appendix or integrated into specialized vision pipelines.

### 3.6. Shallow Explanations
- **Section 14 (Constrained Grammar Decoding)**: Explains logit masking in 5 short bullet points without showing an actual grammar snippet (GBNF or regex automaton state transition table) or explaining why logit masking can introduce latency during the first-token grammar compilation phase.
- **Section 17.1 (Few-Shot ICL)**: Mentions 2 to 5 input/output pairs in a single short code block without discussing example selection strategies, diversity sampling, or negative demonstration traps.

### 3.7. Overly Detailed Implementation Material
- **C# / .NET 9 Implementation (`StrictJsonPipeline.cs`, Lines 1183–1250)**: Contains 65 lines of ASP.NET Core minimal API boilerplate (`WebApplication.CreateBuilder`, `app.MapPost`), which obscures the actual Semantic Kernel JSON schema configuration. The code should be condensed to a clean, focused class.

---

## 4. Terminology Analysis

### 4.1. Unexplained AI Terminology
- **ICL**: Lines 11, 147, and 897 use the acronym "ICL" (*"Golden Few-Shot Examples (ICL)"*) without expanding it to **In-Context Learning** on first mention.
- **SNR**: Line 126 introduces "Signal-to-Noise Ratio (SNR)", but its practical context application (task-relevant tokens / total tokens) is not grounded until line 382.
- **Prefill vs. Decode**: Lines 175 and 706 reference "prefill compute" and "prefill latency" without defining the transformer prefill phase or linking to Phase 00.
- **NIAH**: Line 328 introduces "Needle in a Haystack (NIAH)" without defining the synthetic benchmark methodology.

### 4.2. Unexplained Abbreviations & Acronyms
- **GBNF (Line 673)**: *"Grammar Compiler (GBNF / Regex)"* — GGML Backus-Naur Form is never expanded.
- **DFA / CFG (Lines 17, 685)**: Deterministic Finite Automaton and Context-Free Grammar are used without context anchors.
- **DMN (Lines 758, 799)**: Decision Model & Notation is used without explanation of what standards body maintains it.
- **HBM (Line 166)**: High-Bandwidth Memory is used without expansion.
- **POCO (Line 962)**: Plain Old CLR Object is used in a diagram walkthrough without expansion.

### 4.3. Terminology Introduced Without Context & Inaccuracies
- **Mathematical Inaccuracy (Line 17)**: The header diagram states *"Pushdown Automaton (DFA) Logit Masking"*. A Pushdown Automaton (PDA) has a stack and parses Context-Free Grammars; a Deterministic Finite Automaton (DFA) has no stack and parses Regular Grammars. Conflating them is technically inaccurate.
- **Boundary Pinning (Line 125)**: Introduced in the problem-solution matrix before explaining the attention U-curve or why models suffer amnesia in long contexts.

### 4.4. Inconsistent Terminology & Badging
- **Legacy Badging Scheme**: The README uses `[MUST-HAVE] 🔴`, `[GOOD-TO-KNOW] 🟡`, and `[KNOWLEDGE-BASE] 🔵` across all headings. The curriculum standard mandates the **4-Tier Depth Model**:
  - `🟢 Core`
  - `🟡 Engineering Depth`
  - `🔵 Advanced`
  - `⚫ Deep Dive`
- **Role Naming**: The text alternates between "System Role", "Developer Role", and "System / Developer Role" without clarifying that OpenAI models (o1, o3-mini) introduced the `developer` role to separate developer-defined system invariants from model-internal meta-prompts.

---

## 5. Diagrams Analysis

Phase 01 contains **14 Mermaid diagrams**. Every diagram was audited for conceptual value, complexity, and prose walkthrough compliance:

| # | Line | Diagram Type | Subject / Topology | Prose Walkthrough Present? | Quality Gate 07 Verdict & Action |
|---|:---:|---|---|:---:|---|
| **01** | 8 | `flowchart TD` | Compiled Context Runtime (3 Layers + FSM) | ❌ **No walkthrough** | **VIOLATION**: Needs 4-step prose walkthrough explaining layer boundaries. |
| **02** | 138 | `flowchart TD` | ContextAST Root Compilation Tree | ⚠️ Partial text | **REDUNDANT**: Highly duplicative of Diagram 01. Merge into a clean AST hierarchy diagram with walkthrough. |
| **03** | 210 | `flowchart LR` | 16K Token Budget Allocation Portfolio | ❌ **No walkthrough** | **UNNECESSARY**: Adds zero structural value beyond the 8-row table directly above it. **REMOVE**. |
| **04** | 248 | `flowchart TD` | 4-Tier Compaction Pipeline (T1–T4 Branches) | ⚠️ Partial text | High value. Needs formal numbered step-by-step walkthrough of the escalation branches. |
| **05** | 316 | `xychart-beta` | Attention Accuracy vs. Token Position (U-Curve) | ⚠️ High-level text | High value. Explains Head, Middle, and Tail bias clearly. Retain with enhanced prose annotations. |
| **06** | 344 | `flowchart TD` | Boundary Pinning Architecture (Top, Middle, Bottom) | ⚠️ Partial text | High value. Add step-by-step walkthrough explaining edge-weighted chunk sorting. |
| **07** | 444 | `flowchart TD` | Stage-Gated Tool Loadouts | ❌ **No walkthrough** | **VIOLATION**: Good diagram, but lacks prose walkthrough. Move tool execution to Phase 03. |
| **08** | 500 | `flowchart TD` | Context Routing & Sub-Agent Orchestration | ❌ **No walkthrough** | **VIOLATION**: Premature topic for Phase 01. **MOVE** to Phase 04 with full walkthrough. |
| **09** | 538 | `flowchart LR` | LLMLingua 2 Classifier Pipeline | ❌ **No walkthrough** | **VIOLATION**: Missing prose walkthrough. Add step-by-step explanation of token entropy classification. |
| **10** | 646 | `flowchart TD` | 4-Tier Enterprise Role Hierarchy | ❌ **No walkthrough** | **VIOLATION**: Needs numbered walkthrough detailing privilege separation between roles. |
| **11** | 672 | `flowchart TD` | Constrained Grammar Decoding (FSM Logit Masking) | ✅ Yes (Steps 1–5) | High value. Compliant with Quality Gate 07. Retain in Lesson 04. |
| **12** | 703 | `flowchart LR` | Prompt Caching: Cold Miss vs. Warm Hit | ❌ **No walkthrough** | **VIOLATION**: Missing prose walkthrough. Needs step-by-step memory traffic comparison. |
| **13** | 745 | `flowchart TD` | Prompt Anti-Pattern vs. Decoupled Semantic Architecture | ⚠️ High-level text | Overly complex business logic. Retain in simplified form in Lesson 01. |
| **14** | 931 | `sequenceDiagram` | Runtime Execution Flow (User, Gateway, Cache, LLM) | ❌ **No walkthrough** | **VIOLATION**: 15 numbered steps with zero explanatory prose below the diagram. |

### 5.1. Summary of Diagram Defects
- **8 out of 14 diagrams (57%) violate Quality Gate 07** by completely lacking an accompanying step-by-step prose walkthrough.
- **Diagram 03** is an unnecessary graphical restatement of an existing Markdown table.
- **Diagrams 01 and 02** duplicate each other's architectural content.

### 5.2. Missing Visuals Where Diagrams Would Materially Improve Understanding
1. **FSM Token-Level Logit Masking (Step-by-Step)**: A diagram illustrating the active vocabulary, raw model logits, the FSM state filter masking illegal tokens with -inf, and the resulting softmax probability distribution.
2. **Prefix Taint & Cache Invalidation**: A diagram contrasting an invalidating prefix change (dynamic timestamp at token 0 destroying 10K cached tokens) versus an append-only dynamic tail (100% prefix reuse).
3. **Positional Reranking (Edge-Weighting)**: A visual showing how 10 RAG chunks are reordered into an attention U-curve (`[Doc 1, Doc 3, ..., Doc 4, Doc 2]`).

---

## 6. Engineering Analysis

### 6.1. Practical Examples Evaluation
- **`examples/context_pipeline.py` (Python)**:
  - *Quality*: High. Demonstrates Anthropic prompt caching breakpoints, Pydantic v2 validation, XML sanitization, and fallback JSON repair.
  - *Defects*: Uses `claude-3-5-sonnet-20241022` (should be updated to modern `claude-3-7-sonnet-latest`); uses `client.beta.prompt_caching` in README text while prompt caching is now GA in the Anthropic Messages API; uses assistant prefill without warning that prefill is deprecated or rejected on OpenAI reasoning models (o-series).
- **`examples/semantic_layer_decoupling.py` (Python)**:
  - *Quality*: Exceptional. Provides a fully runnable, deterministic benchmark comparing prompt-based rule evaluation against pure Python rule evaluation, demonstrating 100% test coverage and 85% token reduction.
  - *Placement*: Belongs as a supporting benchmark script in `examples/`, not embedded across 160 lines in the primary context engineering lesson.
- **`examples/StrictJsonPipeline.cs` (C# / .NET 9)**:
  - *Quality*: Good modern .NET implementation using `Azure.AI.OpenAI` and `ChatResponseFormat.CreateJsonSchemaFormat`.
  - *Defects*: Tangled with ASP.NET Core `WebApplication` boilerplate; should be refactored into a clean console harness with unit tests.

### 6.2. Trade-off Analysis
- **Defect**: Tradeoff matrices are quarantined in Section 19 (Lines 968–989), completely decoupled from the lessons where architectural decisions are made.
- **Missing Trade-off Dimensions**:
  - *Strict JSON Schema vs. Prompted JSON*: Latency overhead of initial schema compilation and logit masking vs. 100% deserialization guarantees.
  - *LLMLingua 2 vs. Heuristic Compaction*: Local CPU inference latency (15–35ms) vs. token cost savings vs. semantic drift risk.
  - *Prompt Caching vs. Stateless Calls*: The 25% cache write surcharge on Anthropic vs. 90% read discount; minimum token thresholds (1,024 on Anthropic, 32,768 on Gemini).

### 6.3. Failure Modes & Anti-Patterns
- **Strengths**: The three War Stories in Section 20 are top-tier engineering lore:
  - *War Story 1*: The $42,000 Weekend Invoice & The Timestamp Bug (Prefix Taint).
  - *War Story 2*: The 45-Second Latency Spike & The 60-Tool Agent (Tool Overload).
  - *War Story 3*: The $120,000 Wire Transfer Disaster & The Middle Void (Lost-in-the-Middle).
- **Missing Production Failure Modes**:
  - *The Over-Constrained Schema Infinite Loop*: What happens when an FSM logit mask forces a model to emit an impossible required field, causing token generation to loop or hang.
  - *Assistant Prefill Rejection*: What happens when newer reasoning models (OpenAI o1/o3-mini, DeepSeek-R1) throw HTTP 400 errors because assistant message prefilling is forbidden.
  - *Cache Thrashing via Floating Nonces*: Subtle prefix contamination caused by request IDs, user UUIDs, or random seeds placed above static instructions.

### 6.4. Production Relevance & Systems Rigor
Phase 01 excels in systems rigor by treating the context window as a compiled runtime register rather than a casual chat prompt. However, this rigor is undermined when the material wanders into business claims adjudication (Section 16) and sub-agent DAG orchestration (Section 9).

---

## 7. Resources Analysis

### 7.1. Relevance of Curated Resources
The curated references in Section 22 (Lines 1254–1271) are authoritative and highly relevant:
- *Lost in the Middle* (Liu et al., 2023)
- *LLMLingua 2* (Pan et al., 2024)
- *Chain-of-Thought Prompting* (Wei et al., 2022)
- Official prompt engineering guides from Anthropic, Google Gemini, and OpenAI.

### 7.2. Outdated References & Model Strings
- **Model Strings**: Code references `claude-3-5-sonnet-20241022` and `gpt-4.5`. These should be updated to current frontier production models (`claude-3-7-sonnet`, `gemini-2.0-flash`, `gpt-4o`).
- **Anthropic Beta Namespace**: Line 1053 uses `client.beta.prompt_caching.messages.create`. Prompt caching is now standard in the GA Messages API with `cache_control: {"type": "ephemeral"}` blocks.
- **Assistant Prefill Caveats**: Claude and open-weights models support assistant prefill, but OpenAI's o-series reasoning models reject it.

### 7.3. Missing Authoritative Resources
The curriculum should add citations to:
1. **Outlines Paper**: *Efficient Guided Generation for Large Language Models* (Willard & Louf, 2023) — foundational paper on FSM-guided logit masking.
2. **SGLang / RadixAttention Paper**: *SGLang: Efficient Execution of Structured Language Model Programs* (Zheng et al., 2024) — automatic KV cache reuse via radix trees.
3. **Google Gemini 2.0 Context Caching Documentation**: Official specifications on explicit cache objects, minimum tokens (32K), and TTL management.
4. **OpenAI Structured Outputs Technical Guide**: Formal documentation of regex-to-DFA compilation for strict JSON decoding.

---

## 8. Zero-LaTeX & Markdown Preview Compliance (Quality Gate 13)

Standard Markdown previewers (VS Code, GitHub Web, Antigravity IDE) fail when encountering raw LaTeX math delimiters (display blocks, inline dollars, text tags, fractions) and unescaped currency dollar signs.

### 8.1. Inventory of LaTeX Violations in `01-prompt-and-context-engineering/README.md`

| Line # | Raw LaTeX Expression Found | Standard GFM Text / Monospace Remediation |
|:---:|---|---|
| **125** | `(0–10%)`, `(90–100%)`, `(20–80%)` | `(0% to 10%)`, `(90% to 100%)`, `(20% to 80%)` |
| **174** | `last N turns` | `last N turns` |
| **202** | `Top-K` | `Top-K` |
| **204** | `(> 0.82)` | `(greater than 0.82)` or `(> 0.82)` |
| **277** | `N=4` | `N = 4` |
| **278** | `(0 to N-5)` | `(0 to N - 5)` |
| **324** | `(0–10%)` | `(0% to 10%)` |
| **325** | `(90–100%)` | `(90% to 100%)` |
| **326** | `20% and 80%` | `20% and 80%` |
| **357** | `Order: [Doc_1, ..., Doc_2]` (raw LaTeX equation) | Monospace text block: `Order: [Doc_1, Doc_3, ..., Doc_2]` |
| **382** | `SNR_context = Task_Relevant / Total` (raw LaTeX fraction) | Fenced text code block: `SNR_context = Task_Relevant_Tokens / Total_Window_Tokens` |
| **384** | `SNR < 0.15` (raw LaTeX math text) | `SNR < 0.15` |
| **562** | `2048 × 2048`, `512 × 512` (LaTeX times) | `2048 × 2048`, `512 × 512` |
| **564** | `512 × 512` (LaTeX times) | `512 × 512` |
| **566** | `Tokens_OpenAI = 85 + (Tiles × 170)` (raw LaTeX formula) | Fenced text block: `OpenAI_Tokens = 85 + (Num_Tiles × 170)` |
| **568** | `1920 × 1080` (LaTeX times) | `1920 × 1080` |
| **569** | `512 × 512` (LaTeX times) | `512 × 512` |
| **570** | `85 + (6 × 170) = 1,105 tokens` (LaTeX mathbf/text) | `85 + (6 × 170) = 1,105 tokens` |
| **574** | `Tokens_Claude ≈ ceil((W × H) / 750)` (LaTeX approx/frac) | Fenced text block: `Claude_Tokens ≈ ceil((Width × Height) / 750)` |
| **576** | `1024 × 768` (LaTeX times) | `1024 × 768` |
| **577** | `(1024 × 768) / 750 ≈ 1,049 tokens` (LaTeX frac/approx) | Fenced text block: `(1024 × 768) / 750 ≈ 1,049 tokens` |
| **580** | `4000 × 3000` (LaTeX times) | `4000 × 3000` |
| **686** | `t` (LaTeX inline math) | `t` |
| **687** | `-inf` (LaTeX infty) | `-inf` or `-infinity` |
| **688** | `(e^(-inf) = 0)` (LaTeX infty) | `(e^(-inf) = 0)` |

### 8.2. Inventory of Unescaped Currency Dollar Signs
Unescaped currency dollar signs trigger LaTeX math parsing in preview engines when two or more appear in the same paragraph:
- **Line 186**: `spend \$8,500 on fine dining` (needs backticks or `\$8,500`).
- **Line 529**: `every word costs \$1.00` (needs `\$1.00`).
- **Line 771**: `under \$50 for Standard or \$150 for Gold` (needs `\$50` and `\$150`).
- **Line 902**: `Refund \$45 for late pizza delivery` (needs `\$45`).
- **Line 906**: `Transfer \$10,000 to external offshore account` (needs `\$10,000`).
- **Line 993**: `The \$42,000 Weekend Invoice` (needs `\$42,000` or plain text).
- **Line 994**: `spent \$42,000 in 48 hours` (needs `\$42,000`).
- **Line 998**: `dropped by \$38,000` (needs `\$38,000`).
- **Line 1011**: `The \$120,000 Wire Transfer Disaster` (needs `\$120,000`).
- **Line 1012**: `approved a \$120,000 foreign currency transfer` (needs `\$120,000`).
- **Line 1014**: `No transactions exceeding \$50,000` (needs `\$50,000`).

---

## 9. Link & Navigation Integrity Audit (Quality Gate 11)

### 9.1. Critical Dead Links
- **Line 30 of `labs/capstone-context-engineering-pipeline.md`**:
  ```markdown
  [Return to Module 01](../README.md#10-capstone-engineering-challenge)
  ```
  *Status*: **BROKEN (404 Anchor)**. In `README.md`, the anchor is `#23-capstone-engineering-challenge-must-have-`. The link fails to resolve.
- **Section 23 of `README.md` (Line 1275)**:
  ```markdown
  See the [full capstone specification](./labs/capstone-context-engineering-pipeline.md)
  ```
  *Status*: Resolves to file, but internal section anchors are misaligned.

### 9.2. Cross-Phase Navigation Deficit
- `00-foundations-and-token-mechanics/README.md` links forward to `../01-prompt-and-context-engineering/README.md`.
- However, Phase 01 currently has **no navigation header or footer connecting forward to Phase 02 (`02-rag-and-knowledge-systems`)** or back to Phase 00.

---

## 10. Content Transformation Taxonomy: Action Mapping

Every section, diagram, and asset in Phase 01 is mapped to a specific transformation action:

| Section # & Title | Current Word Count | Recommended Action | Detailed Architectural Rationale & Destination |
|---|:---:|:---:|---|
| **Header & Runtime Diagram (Lines 1–20)** | ~180 | **REORGANIZE / REWRITE** | Retain as the phase architecture banner in `README.md` (Orientation Hub). Add 4-step prose walkthrough. |
| **Learner Note & TOC (Lines 24–60)** | ~250 | **REWRITE** | Update from legacy 3-tier to 4-Tier Depth Model. Replace monolithic TOC with links to 5 modular lessons. |
| **Sec 1: Executive Summary (Lines 63–101)** | ~400 | **SIMPLIFY / REORGANIZE** | Reframe Karpathy quote and suitcase analogy into staff-level systems metaphors. Place in `README.md` and Lesson 01. |
| **Sec 2: Why Context Engineering Matters (Lines 103–129)** | ~350 | **KEEP / REORGANIZE** | Exceptional systems framing. Exposes string concat failures. Move to `01-context-ast-architecture.md` (Section 1). |
| **Sec 3: The Context AST Pattern (Lines 131–177)** | ~550 | **REWRITE** | Core foundation. Expand with concrete Python Pydantic AST schema, hardware KV-cache behavior, and diagram walkthrough in `01-context-ast-architecture.md`. |
| **Sec 4: Context Budgeting Portfolios (Lines 179–241)** | ~450 | **REWRITE** | Convert budget table to clean text. Remove ELI10 box. Expand pre-flight gatekeeper code in `02-token-budgeting-and-compaction.md`. |
| **Sec 5: 4-Tier Compaction Pipeline (Lines 243–309)** | ~650 | **REWRITE** | Outstanding architecture. Combine diagram, text, and runnable code into `02-token-budgeting-and-compaction.md` with complete walkthrough. |
| **Sec 6: Mitigating Lost-in-the-Middle (Lines 311–359)** | ~500 | **REWRITE** | Clean raw LaTeX equations. Add prose walkthrough to U-curve chart and boundary pinning diagram. Move to `05-mecw-and-context-rot.md`. |
| **Sec 7: Context Rot & MECW (Lines 361–402)** | ~450 | **REWRITE** | Convert SNR formula to text block. Detail 50% rule, attention dispersion, and symptoms in `05-mecw-and-context-rot.md`. |
| **Sec 8: Dynamic Tool Loadout Pruning (Lines 404–489)** | ~650 | **SIMPLIFY / MOVE** | Keep context token footprint perspective in Lesson 02; **MOVE** full tool execution registry and handlers to Phase 03. |
| **Sec 9: Context Routing & Sub-Agents (Lines 492–517)** | ~300 | **MOVE** | Multi-agent DAG routing and reducers belong in Phase 04 (`04-agentic-systems-and-orchestration`). Remove from Phase 01. |
| **Sec 10: LLMLingua 2 Compression (Lines 519–553)** | ~350 | **SIMPLIFY / MERGE** | Merge comparison table and token entropy concepts into `02-token-budgeting-and-compaction.md` as Tier 1/2 compaction alternatives. |
| **Sec 11: Multimodal Context Assembly (Lines 555–591)** | ~400 | **SIMPLIFY / MOVE** | Vision tile calculations are tangential to text context AST compilation. Move to a specialized multimodal guide or appendix. |
| **Sec 12: Enterprise XML Architecture (Lines 593–639)** | ~450 | **REORGANIZE / REWRITE** | Foundational syntax primitive. **MOVE** to `01-context-ast-architecture.md` alongside Context AST layers. |
| **Sec 13: 4-Tier Role Hierarchy (Lines 641–665)** | ~250 | **REORGANIZE / REWRITE** | Foundational privilege primitive. **MOVE** to `01-context-ast-architecture.md` as the wire transport format for AST layers. |
| **Sec 14: Constrained Grammar Decoding (Lines 667–696)** | ~450 | **REWRITE** | Expand into standalone `04-constrained-decoding-and-schema-fsm.md`. Detail Outlines, GBNF grammars, Pydantic v2 schemas, and escape hatches. |
| **Sec 15: Physical Prompt Caching (Lines 698–733)** | ~500 | **REWRITE** | Expand into standalone `03-prefix-and-prompt-caching.md`. Detail GPU KV-cache physics, contiguous prefix matching, and prefix taint. |
| **Sec 16: Shared Semantic Layer & DMN (Lines 735–893)** | ~1,200 | **SIMPLIFY / MOVE** | Retain core architectural takeaway (*"Prompt vs. Rule Engine"*) in Lesson 01; keep 350-line benchmark in `examples/semantic_layer_decoupling.py`. |
| **Sec 17: Classical Prompt Patterns (Lines 894–927)** | ~350 | **REORGANIZE / REWRITE** | Few-Shot ICL and CoT scratchpads belong in `01-context-ast-architecture.md` as static AST nodes. Add reasoning model prefill caveats. |
| **Sec 18: System Architecture Flow (Lines 928–966)** | ~250 | **REORGANIZE / REWRITE** | Place in Phase `README.md` and Lesson 01 with a full 8-step numbered prose walkthrough. |
| **Sec 19: Comparative Tradeoff Matrices (Lines 968–989)** | ~300 | **REORGANIZE / MERGE** | Embed schema tradeoff matrix into Lesson 04; embed prompt caching matrix into Lesson 03. |
| **Sec 20: Production War Stories (Lines 991–1018)** | ~550 | **REORGANIZE / MERGE** | Embed War Story 1 (\$42K Timestamp) in Lesson 03; War Story 2 (60 Tools) in Lesson 02; War Story 3 (\$120K Middle Void) in Lesson 05. |
| **Sec 21: Production Code Implementations (Lines 1020–1253)** | ~1,100 | **REORGANIZE / REWRITE** | Distribute focused, runnable code blocks into corresponding modular lessons (`01` through `04`). |
| **Sec 22: Curated Verified Resources (Lines 1254–1271)** | ~300 | **REORGANIZE / REWRITE** | Distribute authoritative primary source citations into their respective modular lessons. Add Outlines and SGLang papers. |
| **Sec 23 & Lab: Capstone Challenge (Lines 1273–1276 & `labs/`)** | ~400 | **KEEP / REORGANIZE** | Fix broken return anchor in `capstone-context-engineering-pipeline.md`. Link cleanly to modular lesson progression. |
| **`examples/context_pipeline.py`** | 106 lines | **KEEP / SIMPLIFY** | Update model string to `claude-3-7-sonnet-latest`; document reasoning model prefill compatibility. |
| **`examples/semantic_layer_decoupling.py`** | 350 lines | **KEEP** | Retain as reference implementation benchmark script. |
| **`examples/StrictJsonPipeline.cs`** | 73 lines | **SIMPLIFY** | Remove ASP.NET minimal API boilerplate; convert to clean console demonstration. |

---

## 11. Proposed Modular Architecture for Phase 01

To eliminate monolithic cognitive overload and conform to the repository's 4-Tier Depth Model, Phase 01 must be refactored into an **Orientation Hub (`README.md`)** and **5 modular lesson files**:

```text
01-prompt-and-context-engineering/
├── README.md                                  # Phase Orientation, Navigation Hub & System Architecture (~450 words)
├── 01-context-ast-architecture.md             # 🟢 Core (~1,500 words)
├── 02-token-budgeting-and-compaction.md       # 🟢 Core (~1,600 words)
├── 03-prefix-and-prompt-caching.md            # 🟡 Engineering Depth (~1,800 words)
├── 04-constrained-decoding-and-schema-fsm.md  # 🟡 Engineering Depth (~1,800 words)
├── 05-mecw-and-context-rot.md                 # 🔵 Advanced (~1,600 words)
├── labs/
│   └── capstone-context-engineering-pipeline.md # Hands-on engineering challenge (Updated link integrity)
└── examples/
    ├── README.md
    ├── context_pipeline.py
    ├── semantic_layer_decoupling.py
    └── StrictJsonPipeline.cs
```

### 11.1. Detailed Specification of Proposed Modular Lessons

#### Lesson 01: `01-context-ast-architecture.md`
- **Badge**: `🟢 Core`
- **Scope & Objective**: Transforming unstructured prompt strings into typed, compilable Context Abstract Syntax Trees (ASTs).
- **Core Topics**:
  - The naive string concatenation trap (`$"You are an assistant... {docs} {time}"`).
  - Context AST 3-layer architecture: Static Prefix (immutable), Semi-Dynamic Layer (tenant/session), Dynamic Tail (ephemeral).
  - The 4-Tier Enterprise Role Hierarchy (`System`, `User`, `Assistant`, `Tool`) and privilege separation.
  - Enterprise XML delimiter sandboxing and prompt injection isolation (`<instructions>`, `<evidence>`, `<user_query>`).
  - Classical prompt patterns as AST nodes: Few-Shot In-Context Learning (ICL) and Chain-of-Thought (CoT) scratchpads.
  - Architectural principle: LLM as semantic extractor vs. deterministic rule engines (simplified overview).
- **Deliverable Code**: Type-annotated Python 3.12+ `ContextAST` compiler using Pydantic v2.
- **Mermaid Diagram**: Context AST Compilation Pipeline with a 5-step numbered prose walkthrough.

#### Lesson 02: `02-token-budgeting-and-compaction.md`
- **Badge**: `🟢 Core`
- **Scope & Objective**: Designing deterministic context portfolios and multi-tier compaction pipelines to eliminate context overflow crashes.
- **Core Topics**:
  - The context overflow crisis under multi-turn workflows.
  - Context Budget Allocation Portfolios (16K, 32K, 64K target ceilings; headroom budgeting).
  - The 4-Tier Compaction Pipeline:
    - Tier 1: Deterministic pruning (null stripping, array capping, JSON minification).
    - Tier 2: Sliding window and intermediate tool payload masking.
    - Tier 3: Recursive asynchronous LLM summarization.
    - Tier 4: Externalization to cloud object storage (S3/GCS pointers).
  - Tool schema budgeting: Capping tool schema token footprints.
  - Token compression: LLMLingua 2 token entropy classification trade-offs.
  - War Story 2: The 45-Second Latency Spike & The 60-Tool Agent.
- **Deliverable Code**: Production `ContextCompactor` class executing Tier 1 and Tier 2 compaction in Python 3.12+.
- **Mermaid Diagram**: The 4-Tier Compaction Decision Pipeline with an explicit 4-step escalation walkthrough.

#### Lesson 03: `03-prefix-and-prompt-caching.md`
- **Badge**: `🟡 Engineering Depth`
- **Scope & Objective**: Leveraging physical GPU KV-cache reuse across inference requests to cut cloud costs by 90% and reduce TTFT by 80%.
- **Core Topics**:
  - The memory bandwidth wall and why prompt prefill is expensive (bridged from Phase 00).
  - GPU KV-Cache persistence in High-Bandwidth Memory (HBM).
  - Contiguous prefix matching: Why token index 0 determines cache hits.
  - The Prefix Taint Anti-Pattern: How dynamic timestamps or session IDs destroy cache reuse.
  - Cross-Provider Cache Comparison: Anthropic ephemeral breakpoints, Google Gemini explicit context caching, and OpenAI automated prefix matching.
  - Reasoning Model Cache Invalidation: Why o3-mini / Claude 3.7 Thinking tokens cannot be cached across conversational turns.
  - War Story 1: The $42,000 Weekend Invoice & The Timestamp Bug.
- **Deliverable Code**: Multi-turn chat session with Anthropic prompt cache breakpoint headers and cache telemetry verification (`cache_read_input_tokens`).
- **Mermaid Diagram**: GPU Memory Traffic: Cold Cache Prefill vs. Warm HBM Read with step-by-step memory walkthrough.

#### Lesson 04: `04-constrained-decoding-and-schema-fsm.md`
- **Badge**: `🟡 Engineering Depth`
- **Scope & Objective**: Enforcing mathematical JSON schema compliance at the token sampling level using Finite State Machine (FSM) logit masking.
- **Core Topics**:
  - Why naive JSON prompting and "JSON Mode" fail in enterprise microservices (syntax slipping, trailing commas, markdown tick poisoning).
  - Mathematical mechanics: Converting Pydantic / JSON Schema into a Deterministic Finite Automaton (DFA) or GBNF grammar.
  - Logit masking at token step `t`: Masking illegal vocabulary tokens with `-inf` prior to softmax.
  - Framework implementations: Outlines, XGrammar, vLLM guided generation, OpenAI Structured Outputs (`strict: true`).
  - The Over-Constrained Schema Escape Hatch: Avoiding infinite whitespace loops through nullable fields and default enums.
  - Comparative Tradeoff Matrix: Natural language vs. JSON mode vs. FSM logit masking vs. self-healing retries.
- **Deliverable Code**: Pydantic v2 strict schema compilation with Outlines / OpenAI strict mode and fallback repair handler.
- **Mermaid Diagram**: Token-by-Token FSM Logit Masking Loop with an explicit 5-step sampling walkthrough.

#### Lesson 05: `05-mecw-and-context-rot.md`
- **Badge**: `🔵 Advanced`
- **Scope & Objective**: Mitigating positional attention degradation, context rot, and Lost-in-the-Middle amnesia across large context windows.
- **Core Topics**:
  - The Long-Context Illusion: Marketed context windows (128K–2M) vs. Maximum Effective Context Window (MECW).
  - Attention dispersion physics: Signal-to-Noise Ratio (SNR) decay across multi-turn sessions.
  - The Attention U-Curve: Primacy bias (head), recency bias (tail), and the middle void (70% retrieval drop).
  - Why synthetic Needle-in-a-Haystack (NIAH) benchmarks deceive architects: Multi-hop reasoning failure modes.
  - Architectural mitigation: Boundary Pinning (Dual-Anchor Framing) and positional reranking (edge-weighted chunk sorting).
  - The 50% Rule: Establishing production operational ceilings before triggering compaction.
  - War Story 3: The $120,000 Wire Transfer Disaster & The Middle Void.
- **Deliverable Code**: Context reordering algorithm implementing edge-weighted document interleaving (`[Doc_1, Doc_3, ..., Doc_2]`).
- **Mermaid Diagram**: The Attention U-Curve and Boundary Pinning Topology with step-by-step prose walkthrough.

---

## 12. Quality Gate Pre-Refactoring Scorecard

Evaluating Phase 01 against the **13-Point Quality Gate Checklist** prior to refactoring:

| # | Inspection Dimension | Status | Audit Findings & Quality Gap |
|---|---|:---:|---|
| **01** | **Learning Objective** | ❌ **FAIL** | Monolithic README lacks outcome-oriented learning objectives per topic. |
| **02** | **Prerequisites** | ❌ **FAIL** | Zero explicit prerequisite connections to Phase 00 (tokens, KV-cache physics, SLMs). |
| **03** | **Terminology Control** | ❌ **FAIL** | Acronyms used without expansion (ICL, GBNF, DFA, DMN); legacy 3-tier badges used. |
| **04** | **Conceptual Progression** | ❌ **FAIL** | Syntax primitives (roles, XML) placed after complex systems (AST, Compaction, Routing). |
| **05** | **Technical Depth** | ✅ **PASS** | Exceptional systems intuitions (FSM logit masking, KV cache physics, AST compilation). |
| **06** | **Conciseness** | ❌ **FAIL** | Monolithic README is 8,952 words (>2.5x word budget ceiling); 160 lines of DMN claims logic. |
| **07** | **Diagram Value** | ❌ **FAIL** | 8 out of 14 Mermaid diagrams lack an accompanying step-by-step prose walkthrough. |
| **08** | **Code Integrity** | ⚠️ **PARTIAL** | Python code is high quality; C# code is bloated with web application boilerplate. |
| **09** | **Trade-off Analysis** | ⚠️ **PARTIAL** | Trade-off matrices exist but are detached in Section 19 instead of embedded in lessons. |
| **10** | **Production & Failures** | ✅ **PASS** | Top-tier war stories (Timestamp bug, 60 tools, middle void AML transfer). |
| **11** | **Link Integrity** | ❌ **FAIL** | Broken return anchor in `capstone-context-engineering-pipeline.md` (`#10-...`). |
| **12** | **Surrounding Fit** | ❌ **FAIL** | Missing navigation handoffs connecting Phase 00 to Phase 01 and Phase 01 to Phase 02. |
| **13** | **Zero-LaTeX Formatting** | ❌ **FAIL** | 25+ raw LaTeX equations and 10+ unescaped currency dollar signs break markdown rendering. |

**Score**: **2 PASS**, **2 PARTIAL**, **9 FAIL** (Critical remediation required in REFACTOR MODE).

---

## 13. Actionable Remediation Checklist for Refactoring Phase 01

When transitioning Phase 01 into **REFACTOR MODE**, execute the following ordered steps:

1. **Decompose the Monolith**:
   - Split `01-prompt-and-context-engineering/README.md` into an Orientation Hub (`README.md`, ~450 words) and 5 modular lessons (`01` through `05`).
2. **Harmonize Badging to the 4-Tier Depth Model**:
   - Assign `🟢 Core` to Lessons 01 and 02.
   - Assign `🟡 Engineering Depth` to Lessons 03 and 04.
   - Assign `🔵 Advanced` to Lesson 05.
3. **Purge All Raw LaTeX & Escape Currency Dollar Signs**:
   - Convert all display math blocks and inline math expressions into standard text code blocks or clean Unicode characters (`→`, `×`, `≈`, `≤`, `≥`).
   - Escape or backtick all currency dollar amounts (`\$10,000`, `\$42,000`, `\$120,000`).
4. **Enforce Step-by-Step Prose Walkthroughs for All Mermaid Diagrams**:
   - Ensure every retained Mermaid diagram features an explicit, numbered step-by-step prose walkthrough directly beneath the code block.
   - Remove redundant Diagram 03 (Token budget table restatement).
5. **Relocate Out-of-Scope Topics**:
   - Move Context Routing & Sub-Agent Orchestration to Phase 04 (`04-agentic-systems-and-orchestration`).
   - Move full Dynamic Tool Registry handlers to Phase 03 (`03-tools-and-model-context-protocol`).
   - Relocate the bulk of the DMN claims rule engine to `examples/semantic_layer_decoupling.py`.
6. **Fix Link & Navigation Integrity**:
   - Patch the dead return anchor in `labs/capstone-context-engineering-pipeline.md`.
   - Add standardized navigation headers and footers across all 5 lessons (`Previous Lesson` / `Next Lesson` / `Lab`).
   - Connect Phase 01 navigation cleanly to Phase 00 and Phase 02.
7. **Refactor Code Implementations**:
   - Update model strings in `examples/context_pipeline.py` to modern production endpoints (`claude-3-7-sonnet-latest`, `gemini-2.0-flash`).
   - Simplify `examples/StrictJsonPipeline.cs` by removing ASP.NET minimal API boilerplate and focusing purely on Semantic Kernel strict JSON schema generation.
