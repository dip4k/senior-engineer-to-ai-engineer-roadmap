# Phase 01: Prompt & Context Engineering — Controlled Curriculum Research Report

> **Execution Mode**: RESEARCH MODE (Controlled Frontier Scout)  
> **Auditor & Researcher**: AI Curriculum Architect  
> **Target Phase Directory**: `01-prompt-and-context-engineering/`  
> **Date**: September 2026  
> **Target Learner**: Senior Developers, Staff Software Engineers, and Solutions Architects (7–10+ years experience) transitioning to AI Systems Engineering.  
> **Primary Sources**: Upstream Provider Documentation (Anthropic, OpenAI, Google DeepMind), Published Research Papers (NeurIPS, COLM, arXiv), and Upstream Open-Source Runtimes (vLLM, SGLang, XGrammar, Outlines).

---

## 1. Executive Summary

This research report evaluates current industry developments, academic breakthroughs, and production engineering practices relevant to **Phase 01: Prompt & Context Engineering**. 

Phase 01 currently teaches:
- Context as a compiled Abstract Syntax Tree (AST) rather than natural language prompt begging.
- Deterministic 16,000-token context budgeting portfolios and a 4-tier compaction pipeline.
- Physical GPU Key-Value (KV) cache prompt reuse and prefix taint invalidation.
- Finite State Machine (FSM) logit masking for guaranteed JSON compliance.
- Positional attention degradation (Lost-in-the-Middle) and Maximum Effective Context Window (MECW).

### Frontier Research Verdict
The underlying systems thesis of Phase 01 remains exceptionally durable: treating context as a compiled, typed runtime register is the defining paradigm of Software 3.0. However, the ecosystem has advanced significantly between 2024 and 2026 in five critical areas:
1. **Grammar Decoding Acceleration**: Outlines' Python-level FSM compilation has been complemented in high-throughput engines (vLLM, SGLang, TensorRT-LLM) by **XGrammar** (arXiv:2411.15100), which co-designs grammar execution with GPU inference for near-zero token latency overhead.
2. **Provider Prompt Caching Modernization**:
   - **Anthropic**: Transitioned prompt caching from beta to GA in the Messages API, supporting automatic caching via top-level `cache_control`, 1-hour extended TTLs, and a strict caching evaluation order (`tools → system prompt → messages`).
   - **OpenAI**: Formalized automatic prefix caching on 1,024-token minimums with 128-token chunk quantization and introduced the dedicated `developer` message role.
   - **Google Gemini**: Dual-tier caching with automatic Implicit Caching on Gemini 2.5+ alongside user-managed Explicit Context Caching objects for multi-turn sessions.
3. **Reasoning Model Dynamics**: The rise of reasoning models (OpenAI o1/o3-mini, Claude 3.7 Extended Thinking, DeepSeek-R1) introduces dynamic thinking budgets, hidden token generation, cache invalidation risks when toggling reasoning settings, and the strict deprecation of assistant message prefilling.
4. **Empirical Context Benchmarking Beyond NIAH**: The **RULER benchmark** (COLM 2024) scientifically proved that single-needle synthetic Needle-in-a-Haystack (NIAH) tests fail to measure real-world multi-hop tracing and aggregation, validating the need for the Maximum Effective Context Window (MECW) and Boundary Pinning.
5. **Contextual Enrichment via Prompt Caching**: Anthropic's **Contextual Retrieval** demonstrated the power of using cached full documents to economically generate chunk-specific metadata before indexing.

---

## 2. Seven Key Analytical Dimensions

### 2.1. Important Concepts Missing from Phase 1
1. **XGrammar Co-Designed Grammar Decoding**: How production serving engines partition vocabulary into context-independent and context-dependent sets to eliminate FSM CPU-GPU synchronization bottlenecks.
2. **The `developer` Message Role Formalization**: OpenAI's structural separation of developer-level system instructions from model safety guardrails and untrusted user inputs in reasoning models.
3. **Reasoning Model Context Dynamics**: How thinking tokens interact with token budgets, why thinking tokens cannot be cached across API turns, and why assistant message prefilling throws HTTP 400 errors on o-series models.
4. **Chunk Boundary Quantization in Prompt Caching**: OpenAI's 128-token chunk increment rule and why failing to align prefix lengths causes unexpected cache misses.
5. **The RULER Long-Context Evaluation Methodology**: Multi-hop tracing and variable task complexity benchmarks proving attention degradation in production long contexts.
6. **RadixAttention Tree-Based Prefix Caching**: The systems algorithm (from SGLang) for maintaining a radix tree over prompt prefixes to share KV cache blocks across branching multi-turn sessions.

### 2.2. Existing Concepts That Should Be Updated
1. **Anthropic Prompt Caching Mechanics**: Update code from `client.beta.prompt_caching` to the GA Messages API. Document automatic caching (`cache_control` at top-level), 5-minute vs. 1-hour TTL options, and the strict prefix ordering rule (`tools` must remain immutable to preserve `system` cache).
2. **OpenAI Caching & Role Hierarchy**: Update from legacy `system` prompts to the `developer` role for modern reasoning architectures, and document the 50% cached token discount.
3. **Google Gemini Caching Architecture**: Update to explain Gemini's dual model: Implicit Caching (automated on Gemini 2.5+) vs. Explicit Context Caching API (user-managed TTLs and cache resources).
4. **Constrained Decoding Ecosystem**: Expand beyond Outlines to include XGrammar and native OpenAI Structured Outputs (`json_schema` with `strict: true`).

### 2.3. Concepts That Are Now Outdated
1. **Model Strings**: `claude-3-5-sonnet-20241022` and `gpt-4.5` are outdated references in code snippets. Must be modernized to current frontier endpoints (`claude-3-7-sonnet-latest`, `gemini-2.0-flash`, `gpt-4o`, `o3-mini`).
2. **Anthropic Beta Namespace**: `client.beta.prompt_caching.messages.create` has been promoted to the GA Messages API.
3. **Universal Reliance on Assistant Prefilling**: Using `messages=[..., {"role": "assistant", "content": "{\n \"decision\":"}]` to force JSON output fails on OpenAI reasoning models (o1, o3-mini) and DeepSeek-R1. Constrained decoding (FSM / logit masking) is now the universal standard.
4. **Synthetic Single-Needle NIAH as Context Benchmark**: Advertising 100% retrieval on single-word needle tests without acknowledging multi-hop degradation.

### 2.4. Important Architectural Patterns That Should Be Introduced
1. **Radix-Tree Context Hierarchies**: Structuring multi-turn conversations into tree-aligned static prefix blocks to maximize KV cache reuse across branching turns.
2. **Dual-Anchor Framing & Edge-Weighted Positional Reranking**: Interleaving retrieved RAG evidence so that top-confidence chunks sit at the 0% (primacy) and 100% (recency) boundaries of the attention U-curve.
3. **Cached Full-Document Context Enrichment**: Prepending document-level context summaries to segmented RAG chunks by amortizing document prefill through prompt caching.

### 2.5. Emerging Topics Worth Mentioning
1. **Adaptive Thinking Token Budgets**: Dynamically sizing the model's intermediate reasoning scratchpad within the 16K/32K context portfolio.
2. **Context-Free Grammar (CFG) Token Masking**: Compiling complex domain grammars (SQL DDL, EBNF) into token interceptors.
3. **Hybrid Caching Topologies**: Combining client-managed explicit cache IDs for static tenant policies with gateway-managed implicit prefix caches for dynamic sessions.

### 2.6. Topics That Are Temporary Trends and Should NOT Be Added (REJECT)
1. **Prompt Begging & Emotional Incantations**: *"Take a deep breath"*, *"I will tip you $200"*, *"Answer as if you are a Nobel laureate"*. These are transient artifacts of early RLHF alignment and have zero systems engineering value.
2. **Proprietary Prompt Compression SaaS Wrappers**: Third-party closed-source compression proxies that obscure token entropy algorithms and introduce unnecessary network hops.
3. **Heuristic Prompt Mutators**: Brittle Python libraries that randomly shuffle prompt words to test stability, rather than using structured evaluations or compiler ASTs.
4. **Natural Language System Prompt Compilers**: Natural language tools claiming to "auto-write" system prompts without formal schemas, typing, or regression tests.

### 2.7. Topics That Belong in Later Phases (MOVE_TOPIC)
1. **Context Routing & Sub-Agent Orchestration**: Belongs in Phase 04 (`04-agentic-systems-and-orchestration`). In Phase 01, learners must master single-turn context compilation before designing multi-agent supervisor DAGs.
2. **Dynamic Tool Loadout Registry Execution**: Belongs in Phase 03 (`03-tools-and-model-context-protocol`). While tool schema token budgeting is taught in Phase 01, tool invocation handlers and execution loops belong in Phase 03.
3. **Enterprise Semantic Layer & DMN Claims Engine**: Belongs in Phase 02/03 for enterprise data grounding or Phase 04 for deterministic agent actions. Phase 01 should retain only the high-level principle (*"LLM as Semantic Extractor, Code as Deterministic Adjudicator"*).
4. **Multimodal Image Tiling Calculations**: Belongs in an advanced multimodal vision appendix.

---

## 3. Comprehensive Topic Candidate Catalog

Below is the detailed evaluation of every candidate topic audited for Phase 01:

---

### Candidate 01: XGrammar Co-Designed Grammar Decoding Engine
* **Classification**: `NEW_TOPIC`
* **Topic**: Near-Zero Overhead Grammar-Guided Decoding with XGrammar.
* **Why It Matters**: While Outlines popularized FSM-guided decoding, its CPU-level grammar compilation and CPU-GPU synchronization can add 50–200ms latency overhead during the initial prefill phase. XGrammar (developed by the MLC-LLM team and integrated into vLLM, SGLang, and TensorRT-LLM) co-designs the grammar engine with GPU kernels, dividing vocabulary into context-independent and context-dependent tokens for sub-millisecond logit masking.
* **Current Phase 1 Coverage**: Section 14 mentions Outlines and generic FSM logit masking in 5 bullet points, but omits modern production runtimes like XGrammar.
* **Recommended Action**: Introduce XGrammar alongside Outlines in `04-constrained-decoding-and-schema-fsm.md` to show production-scale serving integration.
* **Proposed Location**: Phase 01 / Lesson 04 (`04-constrained-decoding-and-schema-fsm.md`).
* **Prerequisites**: Phase 00 (Logits and softmax sampling); Phase 01 / Lesson 01 (JSON Schema).
* **Stability**: Durable (adopted as standard backend in vLLM, SGLang, and TensorRT-LLM).
* **Recommended Sources**:
  - *XGrammar: Flexible and Efficient Structured Generation to Enable LLM Deployment* (arXiv:2411.15100).
  - GitHub: `mlc-ai/xgrammar`.

---

### Candidate 02: Formalization of the `developer` Message Role
* **Classification**: `UPDATE_EXISTING`
* **Topic**: Transition from `system` to `developer` Message Role for High-Privilege Instructions.
* **Why It Matters**: OpenAI has formally transitioned from `system` to `developer` roles in reasoning models (o1, o3-mini) and modern APIs. The `developer` role explicitly establishes developer-defined invariants that take precedence over user inputs while remaining distinct from the provider's internal safety alignments.
* **Current Phase 1 Coverage**: Section 13 mentions "System / Developer Role" interchangeably without explaining why the distinction was created or which models enforce it.
* **Recommended Action**: Update `01-context-ast-architecture.md` to formally document the 4-tier role hierarchy (`developer`/`system`, `user`, `assistant`, `tool`) and explain role privilege separation.
* **Proposed Location**: Phase 01 / Lesson 01 (`01-context-ast-architecture.md`).
* **Prerequisites**: Basic HTTP client knowledge.
* **Stability**: Durable (adopted across OpenAI platform and modern multi-turn schemas).
* **Recommended Sources**:
  - OpenAI Platform Documentation: *Guides — Model Roles & Developer Messages*.
  - OpenAI API Reference: Chat Completions.

---

### Candidate 03: Modernization of Anthropic Prompt Caching (GA Features & Ordering)
* **Classification**: `UPDATE_EXISTING`
* **Topic**: Anthropic GA Prompt Caching, Automatic Breakpoints, and Strict Prefix Ordering.
* **Why It Matters**: Anthropic promoted prompt caching to GA. Key operational rules:
  1. Strict caching evaluation order: `tools → system prompt → messages`. If tool definitions are modified, system prompt caches are invalidated.
  2. Automatic caching via top-level `cache_control` headers.
  3. 5-minute vs. 1-hour Time-to-Live (TTL) tiers with distinct write/read multipliers (1.25x / 2.0x write; 0.1x read).
* **Current Phase 1 Coverage**: Section 15 and code examples use outdated beta syntax (`client.beta.prompt_caching`), omit the 1-hour TTL, and fail to document the strict caching evaluation order.
* **Recommended Action**: Modernize `03-prefix-and-prompt-caching.md` and `examples/context_pipeline.py` to GA syntax, document caching order invariants, and explain automatic vs. explicit breakpoints.
* **Proposed Location**: Phase 01 / Lesson 03 (`03-prefix-and-prompt-caching.md`).
* **Prerequisites**: Phase 00 (GPU KV-Cache HBM physics); Phase 01 / Lesson 01 (Context AST layers).
* **Stability**: Durable (GA core protocol for Anthropic API).
* **Recommended Sources**:
  - Anthropic Documentation: *Build with Claude — Prompt Caching* (platform.claude.com).
  - Anthropic SDK Releases (Python `anthropic >= 0.40.0`).

---

### Candidate 04: OpenAI Automated Prefix Caching Mechanics & Quantization
* **Classification**: `UPDATE_EXISTING`
* **Topic**: OpenAI 1,024-Token Minimums, 128-Token Chunk Quantization, and Retention.
* **Why It Matters**: Unlike Anthropic's explicit breakpoints, OpenAI caching is implicit and automated. However, it requires an exact character match starting from token 0, enforces a strict 1,024-token minimum threshold, and quantizes cache blocks into 128-token increments. If a static prefix is 1,023 tokens, caching hit rate is 0%.
* **Current Phase 1 Coverage**: Section 15 has a 3-row summary table mentioning 1,024 tokens, but does not explain chunk quantization, retention policies (24-hour default vs. in-memory ZDR), or prefix taint failure modes.
* **Recommended Action**: Expand `03-prefix-and-prompt-caching.md` with explicit technical mechanics for OpenAI automated prefix caching and diagnostic dashboards.
* **Proposed Location**: Phase 01 / Lesson 03 (`03-prefix-and-prompt-caching.md`).
* **Prerequisites**: Phase 00 (Tokenization); Phase 01 / Lesson 01 (Static vs Dynamic Context).
* **Stability**: Durable (enterprise standard for OpenAI API).
* **Recommended Sources**:
  - OpenAI Platform Documentation: *Prompt Caching — How It Works & Best Practices*.

---

### Candidate 05: Google Gemini Dual Caching Architecture (Implicit vs. Explicit)
* **Classification**: `UPDATE_EXISTING`
* **Topic**: Gemini Implicit Prefix Caching vs. Explicit Context Caching API.
* **Why It Matters**: Google Gemini operates two distinct caching mechanisms:
  1. **Implicit Caching**: Automatically enabled on Gemini 2.5+ models for matching prompt prefixes, providing automatic cost reductions.
  2. **Explicit Context Caching**: Programmatically creates a dedicated cache resource with user-specified TTL (1 hour to multiple days) for large corpora (minimum 32,768 tokens), ideal for persistent multi-tenant enterprise data.
* **Current Phase 1 Coverage**: Section 15 lists Gemini in a table with a 32K threshold, but fails to explain the critical architectural distinction between implicit prefix caching and explicit cache resources.
* **Recommended Action**: Detail both Gemini caching tiers in `03-prefix-and-prompt-caching.md`.
* **Proposed Location**: Phase 01 / Lesson 03 (`03-prefix-and-prompt-caching.md`).
* **Prerequisites**: Phase 00 (KV Cache physics); Phase 01 / Lesson 01 (Context AST).
* **Stability**: Durable (standard Google GenAI API architecture).
* **Recommended Sources**:
  - Google Gemini API Documentation: *Context Caching Overview & Guides* (ai.google.dev).
  - Gemini API Optimization Guides (`gemini-api-guides/optimization.md`).

---

### Candidate 06: Reasoning Model Context Dynamics & Thinking Tokens
* **Classification**: `NEW_TOPIC`
* **Topic**: Interaction Between Reasoning Models, Thinking Tokens, and Context Architecture.
* **Why It Matters**: Frontier reasoning models (OpenAI o1/o3-mini, Claude 3.7 Extended Thinking, DeepSeek-R1) generate dynamic internal reasoning tokens ("thinking process") before emitting the final text:
  1. Thinking tokens are billed as output tokens, often generating a 50:1 token inflation over the visible answer.
  2. Thinking tokens cannot be cached across conversational turns; they are generated dynamically per request.
  3. Modifying extended thinking parameters between requests invalidates prompt cache segments.
  4. Assistant message prefilling (e.g. `{"role": "assistant", "content": "{"}`) is explicitly forbidden or returns HTTP 400 errors on reasoning models.
* **Current Phase 1 Coverage**: Mentioned briefly under MECW degradation, but the operational realities (caching invalidation, prefill rejection, thinking budget sizing) are missing.
* **Recommended Action**: Integrate a dedicated engineering section on Reasoning Model Context Dynamics in `02-token-budgeting-and-compaction.md` (budget sizing) and `03-prefix-and-prompt-caching.md` (caching rules).
* **Proposed Location**: Phase 01 / Lessons 02 and 03.
* **Prerequisites**: Phase 00 / Lesson 04 (Test-time compute and reasoning models).
* **Stability**: Durable (industry-wide architecture for reasoning models).
* **Recommended Sources**:
  - Anthropic Documentation: *Extended Thinking & Caching Interactions*.
  - OpenAI Platform Documentation: *Using Reasoning Models (o1, o3)*.

---

### Candidate 07: The RULER Benchmark & Multi-Hop Long-Context Evaluation
* **Classification**: `UPDATE_EXISTING`
* **Topic**: The RULER Benchmark: Empirical Proof of Effective Context Window Degradation.
* **Why It Matters**: Vendor marketing touts 1M–2M token context windows based on simple synthetic Needle-in-a-Haystack (NIAH) retrieval. The RULER benchmark (COLM 2024, Hsieh et al.) proved that while models pass NIAH at 128K, their multi-hop tracing and aggregation accuracy plummets below 50% beyond 32K–64K tokens, scientifically validating the **Maximum Effective Context Window (MECW)** concept.
* **Current Phase 1 Coverage**: Section 6 and 7 critique synthetic NIAH tests intuitively, but lack empirical academic citations and quantitative benchmarks.
* **Recommended Action**: Anchor `05-mecw-and-context-rot.md` in the findings of the RULER benchmark paper.
* **Proposed Location**: Phase 01 / Lesson 05 (`05-mecw-and-context-rot.md`).
* **Prerequisites**: Phase 00 (Attention complexity); Phase 01 / Lesson 02 (Token budgeting).
* **Stability**: Durable (foundational benchmark paper in long-context evaluation).
* **Recommended Sources**:
  - *RULER: What's the Real Context Size of Your Long-Context Language Models?* (Hsieh et al., COLM 2024, arXiv:2404.06654).

---

### Candidate 08: RadixAttention & SGLang Prefix Caching Tree Mechanics
* **Classification**: `ADVANCED_TOPIC`
* **Topic**: RadixAttention: Dynamic KV Cache Reuse via Prefix Trees.
* **Why It Matters**: At the platform infrastructure level, high-performance inference engines do not treat prompts as flat linear buffers. SGLang introduced RadixAttention, which maintains a radix tree over prompt tokens in GPU memory. When multiple requests share sub-prefixes (e.g., few-shot examples or agent tool definitions), RadixAttention automatically reuses intermediate KV cache nodes without requiring manual cache boundaries.
* **Current Phase 1 Coverage**: Mentioned in root repository ADR-004 and incident post-mortems, but completely absent from Phase 01 instructional material.
* **Recommended Action**: Include an Advanced Deep Dive in `03-prefix-and-prompt-caching.md` explaining how RadixAttention implements tree-based KV cache reuse.
* **Proposed Location**: Phase 01 / Lesson 03 (`03-prefix-and-prompt-caching.md`).
* **Prerequisites**: Phase 00 / Lesson 03 (KV cache physics); Phase 01 / Lesson 01 (Context AST).
* **Stability**: Durable (core architecture of SGLang and widely adopted in vLLM).
* **Recommended Sources**:
  - *SGLang: Efficient Execution of Structured Language Model Programs* (Zheng et al., NeurIPS 2024, arXiv:2312.07104).

---

### Candidate 09: Anthropic Contextual Retrieval Integration with Prompt Caching
* **Classification**: `REFERENCE_ONLY`
* **Topic**: Prepending Document-Level Context Summaries via Cached Full Documents.
* **Why It Matters**: To prevent chunk isolation in RAG, Anthropic demonstrated prepending a 50–100 token context summary to every chunk. To make this economically feasible, the full document is loaded as a cached prompt prefix, and individual chunks are passed as ephemeral suffixes. This bridges Phase 01 (Prompt Caching) to Phase 02 (RAG).
* **Current Phase 1 Coverage**: Not covered in Phase 01.
* **Recommended Action**: Add a bridge reference in `03-prefix-and-prompt-caching.md` previewing how prompt caching enables contextual chunk enrichment in Phase 02. Full implementation remains in Phase 02.
* **Proposed Location**: Phase 01 / Lesson 03 (Bridge section to Phase 02).
* **Prerequisites**: Phase 01 / Lesson 03 (Prompt caching).
* **Stability**: Durable (widely adopted RAG enhancement pattern).
* **Recommended Sources**:
  - Anthropic Engineering Blog: *Contextual Retrieval* (September 2024).

---

### Candidate 10: Context Routing & Sub-Agent Orchestration (Section 9)
* **Classification**: `MOVE_TOPIC`
* **Topic**: Triage Classifiers, Sub-Agent Prompt Isolation, and Reducer Synthesis.
* **Why It Matters**: Multi-agent fan-out and synthesis reducers are essential distributed agent patterns, but teaching them in Phase 01 creates cognitive overload before the learner understands tool calling wire protocols (Phase 03) or cyclical agent state graphs (Phase 04).
* **Current Phase 1 Coverage**: Section 9 covers triage routers and sub-agents across 25 lines and a Mermaid diagram.
* **Recommended Action**: **MOVE** entirely to Phase 04 (`04-agentic-systems-and-orchestration`).
* **Proposed Location**: Phase 04 / Lesson 04 (`04-multi-agent-coordination-and-handoffs.md`).
* **Prerequisites**: Phase 03 (Tools & MCP); Phase 04 (Stateful loops).
* **Stability**: Durable.
* **Recommended Sources**:
  - Phase 04 Curriculum Architecture.

---

### Candidate 11: Dynamic Tool Registry Execution & Handlers (Section 8)
* **Classification**: `MOVE_TOPIC`
* **Topic**: Stage-Gated Tool Mounts and Dynamic Tool Execution Registry.
* **Why It Matters**: Managing tool execution handlers (`Callable`), schema registration, and tool dispatch belongs fundamentally in Phase 03 (`03-tools-and-model-context-protocol`). In Phase 01, the only relevant concept is the **token footprint of tool schemas** inside the Context AST.
* **Current Phase 1 Coverage**: Section 8 contains a full Python `DynamicToolLoadoutRegistry` class and execution diagrams.
* **Recommended Action**: Retain tool schema token budgeting in `02-token-budgeting-and-compaction.md`; **MOVE** the tool execution registry, handlers, and runtime dispatching to Phase 03.
* **Proposed Location**: Phase 03 (`03-tools-and-model-context-protocol`).
* **Prerequisites**: Phase 01 (Context AST); Phase 03 (JSON-RPC tool wire specs).
* **Stability**: Durable.
* **Recommended Sources**:
  - Model Context Protocol (MCP) Specification.

---

### Candidate 12: Enterprise Claims Adjudication DMN Rule Engine (Section 16)
* **Classification**: `MOVE_TOPIC`
* **Topic**: Business Rule Management Systems (BRMS), Drools, and DMN Decision Tables.
* **Why It Matters**: Over 160 lines in Section 16 detail e-commerce return policies, damage thresholds, customer tiers, and DMN decision tables. While the systems rule (*"Never force an LLM to evaluate deterministic business logic"*) is essential, the extensive domain implementation overshadows core prompt engineering.
* **Current Phase 1 Coverage**: Section 16 covers 158 lines of markdown plus a 350-line benchmark script in `examples/semantic_layer_decoupling.py`.
* **Recommended Action**: Condense the conceptual takeaway (*"LLM as Semantic Extractor, Code as Deterministic Adjudicator"*) into a 2-page section in `01-context-ast-architecture.md`. Keep the complete 350-line benchmark in `examples/semantic_layer_decoupling.py`.
* **Proposed Location**: Conceptual takeaway in `01-context-ast-architecture.md`; code preserved in `examples/semantic_layer_decoupling.py`.
* **Prerequisites**: Basic software architecture.
* **Stability**: Durable.
* **Recommended Sources**:
  - `examples/semantic_layer_decoupling.py`.

---

### Candidate 13: Multimodal Vision Tiling Math (Section 11)
* **Classification**: `MOVE_TOPIC`
* **Topic**: OpenAI 512x512 Tile Calculations and Anthropic Pixel Surface Area Formulas.
* **Why It Matters**: Image token math is valuable for vision engineers, but interrupts the conceptual flow of compiling text ASTs, token budgeting, and JSON schema logit masking.
* **Current Phase 1 Coverage**: Section 11 covers 36 lines of tile math with heavy formulas (multiplication, ceilings).
* **Recommended Action**: **MOVE** to an optional multimodal appendix or specialized vision section.
* **Proposed Location**: Multimodal Appendix / Phase 01 Supplementary Resources.
* **Prerequisites**: Phase 01 (Token budgeting).
* **Stability**: Rapidly changing (vision tokenizers frequently update tile resolutions).
* **Recommended Sources**:
  - OpenAI Vision API Documentation; Anthropic Claude Vision Guide.

---

### Candidate 14: Emotional Incantations & Jailbreak "Magic Words"
* **Classification**: `NOT_RELEVANT`
* **Topic**: Prompt Begging (*"Think step by step"*, *"I will tip you $200"*, *"Answer or people will die"*).
* **Why It Matters**: These techniques were transient artifacts of early instruction tuning (2022–2023). In production systems (2025–2026), systems rely on typed ASTs, system instructions, few-shot demonstrations, and grammar-constrained decoding. Teaching "magic phrases" degrades curriculum credibility.
* **Current Phase 1 Coverage**: Section 1 explicitly critiques this as dead, but it must never be presented as a viable engineering pattern.
* **Recommended Action**: Maintain strict stance: exclude all prompt begging techniques except as historical context in the executive summary.
* **Proposed Location**: Excluded.
* **Stability**: Obsolete.
* **Recommended Sources**:
  - Industry consensus / Andrej Karpathy's context engineering framing.

---

## 4. Summary Classification Table

| # | Candidate Topic | Classification | Target Phase / Lesson | Recommended Action Summary |
|---|---|:---:|---|---|
| **01** | XGrammar Co-Designed Grammar Decoding | `NEW_TOPIC` | Phase 01 / Lesson 04 | Introduce near-zero latency grammar engine alongside Outlines in vLLM/SGLang. |
| **02** | Formal `developer` Role Formalization | `UPDATE_EXISTING` | Phase 01 / Lesson 01 | Formalize `developer` role vs. `system` and `user` for privilege separation in reasoning models. |
| **03** | Anthropic GA Caching & Ordering Rules | `UPDATE_EXISTING` | Phase 01 / Lesson 03 | Upgrade to GA Messages API, auto `cache_control`, 1-hour TTL, and `tools → system → messages` order. |
| **04** | OpenAI Caching Chunk Quantization | `UPDATE_EXISTING` | Phase 01 / Lesson 03 | Document 1,024-token minimum, 128-token chunk increments, and 50% input discount. |
| **05** | Gemini Dual Caching Architecture | `UPDATE_EXISTING` | Phase 01 / Lesson 03 | Document Implicit Prefix Caching (Gemini 2.5+) vs. Explicit Context Caching API. |
| **06** | Reasoning Model Context Dynamics | `NEW_TOPIC` | Phase 01 / Lessons 02 & 03 | Document thinking token budgets, prefill deprecation, and cache invalidation rules. |
| **07** | RULER Long-Context Benchmark | `UPDATE_EXISTING` | Phase 01 / Lesson 05 | Ground MECW and attention U-curve in empirical multi-hop findings from COLM 2024 paper. |
| **08** | RadixAttention Prefix Tree Mechanics | `ADVANCED_TOPIC` | Phase 01 / Lesson 03 | Deep dive on radix-tree KV cache reuse algorithms in SGLang runtime. |
| **09** | Contextual Retrieval via Caching | `REFERENCE_ONLY` | Phase 01 / Lesson 03 | Add cross-phase bridge showing how cached prompt prefixes generate chunk metadata. |
| **10** | Context Routing & Sub-Agents | `MOVE_TOPIC` | Phase 04 / Lesson 04 | Move triage classifier, sub-agents, and reducers to Phase 04 multi-agent orchestration. |
| **11** | Dynamic Tool Loadout Registry | `MOVE_TOPIC` | Phase 03 / Lesson 03 | Move full tool registry and execution engine to Phase 03; keep schema token cap in Phase 01. |
| **12** | Enterprise DMN Claims Rule Engine | `MOVE_TOPIC` | Phase 01 / Lesson 01 & `examples/` | Condense 160-line claims engine to high-level concept; preserve full benchmark in `examples/`. |
| **13** | Multimodal Vision Tiling Math | `MOVE_TOPIC` | Multimodal Appendix | Move 512 × 512 tile math to specialized appendix to keep text AST progression focused. |
| **14** | Prompt Begging & Magic Phrases | `NOT_RELEVANT` | Excluded | Explicitly exclude obsolete prompt tricks; enforce typed compiler engineering. |

---

## 5. Strategic Recommendations for Phase 01 Refactoring

When authorized to transition Phase 01 into **REFACTOR MODE**, integrate the approved research findings into the 5 target modular lessons:

1. **Lesson 01 (`01-context-ast-architecture.md`)**:
   - Establish the 4-tier role hierarchy including the modern **`developer` role** (Candidate 02).
   - Ground XML delimiter sandboxing and few-shot ICL demonstrations as static AST nodes.
   - Summarize the high-level principle of **decoupling LLM extraction from deterministic rule engines** (Candidate 12).
2. **Lesson 02 (`02-token-budgeting-and-compaction.md`)**:
   - Integrate **Reasoning Model Thinking Token Budgets** into context portfolio allocations (Candidate 06).
   - Detail the 4-tier compaction pipeline and LLMLingua 2 token entropy compression.
   - Cap tool schema token allocations without bloating the lesson with tool execution registries (Candidate 11).
3. **Lesson 03 (`03-prefix-and-prompt-caching.md`)**:
   - Modernize Anthropic prompt caching to GA syntax, 1-hour TTLs, and **strict caching evaluation order** (Candidate 03).
   - Document OpenAI **128-token chunk quantization** and retention policies (Candidate 04).
   - Detail Google Gemini **Implicit Prefix Caching vs. Explicit Context Caching** (Candidate 05).
   - Document reasoning model cache invalidation rules and prefill prohibitions (Candidate 06).
   - Add an Advanced Deep Dive on **RadixAttention prefix trees** from SGLang (Candidate 08).
   - Add a forward bridge to Phase 02 on **Contextual Retrieval** chunk enrichment (Candidate 09).
4. **Lesson 04 (`04-constrained-decoding-and-schema-fsm.md`)**:
   - Introduce **XGrammar co-designed GPU grammar decoding** alongside Outlines (Candidate 01).
   - Document Pydantic v2 strict JSON schema generation and OpenAI native `strict: true`.
   - Analyze the trade-offs of logit masking latency vs. 100% deserialization guarantees.
5. **Lesson 05 (`05-mecw-and-context-rot.md`)**:
   - Ground Maximum Effective Context Window (MECW) in the empirical findings of the **RULER benchmark** (Candidate 07).
   - Detail the attention U-curve (Lost-in-the-Middle) and implement **Boundary Pinning** with edge-weighted positional reranking.

---

## 6. Primary Research Citations & Upstream References

1. **XGrammar**:
   - *XGrammar: Flexible and Efficient Structured Generation to Enable LLM Deployment* (arXiv:2411.15100).
   - Upstream repository: `https://github.com/mlc-ai/xgrammar`.
2. **RULER Benchmark**:
   - *RULER: What's the Real Context Size of Your Long-Context Language Models?* (Hsieh, Sun, Kriman et al., COLM 2024, arXiv:2404.06654).
3. **RadixAttention & SGLang**:
   - *SGLang: Efficient Execution of Structured Language Model Programs* (Zheng, Yin, Xie et al., NeurIPS 2024, arXiv:2312.07104).
4. **Anthropic Documentation**:
   - *Prompt Caching Guide*: `https://platform.claude.com/docs/en/build-with-claude/prompt-caching`.
   - *Extended Thinking & Caching*: `https://platform.claude.com/docs/en/build-with-claude/extended-thinking`.
   - *Contextual Retrieval*: `https://www.anthropic.com/news/contextual-retrieval`.
5. **OpenAI Documentation**:
   - *Prompt Caching*: `https://platform.openai.com/docs/guides/prompt-caching`.
   - *Structured Outputs*: `https://platform.openai.com/docs/guides/structured-outputs`.
   - *Developer Messages & Model Roles*: `https://platform.openai.com/docs/guides/reasoning`.
6. **Google Gemini Documentation**:
   - *Context Caching*: `https://ai.google.dev/gemini-api/docs/caching`.
   - *Gemini API Optimization Guide*: `https://ai.google.dev/gemini-api/docs/optimization`.
