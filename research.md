# AI Engineering Curriculum Research & Freshness Roadmap

> **Operating Mode**: RESEARCH MODE (Controlled Frontier Scout)  
> **Auditor**: AI Curriculum Architect  
> **Status**: Verified Industry Standards (2025–2026)  
> **Target Audience**: Senior Developers, Staff AI Platform Engineers, and Solutions Architects  
> **Protocol**: `Research → Verify → Classify → Evaluate → Recommend → Human Approval → Integrate`  
> **Rule**: Do not modify existing curriculum files until explicit human approval.

---

## 1. Executive Summary & Frontier Landscape

AI Engineering has matured from prompt crafting and toy demonstrations into **distributed systems engineering for probabilistic runtimes (Software 3.0)**. 

Through live primary-source web research across official specifications, academic papers, and enterprise cloud frameworks, this document establishes the authoritative frontier baseline across the repository:

1. **Protocol Standardization Under Open Governance**:
   - **Model Context Protocol (MCP)**: Formally transitioned from Anthropic to the **Agentic AI Foundation (AAIF)** under the **Linux Foundation** (December 2025). The current authoritative specification is the **2026-07-28 Stateless Release**, introducing stateless HTTP-native transports, the AWS-contributed **Tasks** extension for long-running workflows, and authorization hardening.
   - **Google Agent-to-Agent (A2A) Protocol**: Standardized at `a2a-protocol.org` for multi-agent interoperability across heterogeneous frameworks (Google ADK, LangGraph, AutoGen) and polyglot runtimes.
   - **Anthropic Agent Skills**: Formalized as modular instruction packs (`SKILL.md`), bridging human playbooks to autonomous execution engines.
2. **Inference & Hardware Breakthroughs**:
   - **Multi-Head Latent Attention (MLA)**: DeepSeek-V2/V3/R1 architecture compressing Key-Value tensors into compact latent vectors via matrix absorption, providing MQA-level memory efficiency with standard MHA expressiveness.
   - **Test-Time Compute & Pure RL Reasoning**: DeepSeek-R1 Group Relative Policy Optimization (GRPO) and OpenAI o-series scaling laws proving that reasoning emerges from rule-based verification rewards without separate critic models.
   - **Speculative Decoding Standard**: **EAGLE-3** and **Parallel EAGLE (P-EAGLE)** integrated into vLLM and SGLang, generating draft tokens in a single forward pass to break the autoregressive memory bandwidth wall.
   - **RadixAttention (SGLang)**: Automatic tree-based prefix KV-cache sharing across branching sessions, delivering dramatic latency advantages for high-overlap multi-turn agents and RAG.
3. **Retrieval & Grounding Modernization**:
   - **Late Chunking (Jina AI)**: Passing full documents through long-context encoders before pooling token embeddings across chunk boundaries, eliminating semantic boundary blindspots.
   - **Contextual Retrieval (Anthropic)**: Prepending LLM-generated chunk-specific situational summaries before embedding and indexing, reducing retrieval failures by 30–40%.
   - **Hybrid Retrieval Standard**: Dense HNSW + Sparse BM25 fused via Reciprocal Rank Fusion (RRF `k=60`) followed by cross-encoder full-attention reranking.
4. **Observability & Evaluation Governance**:
   - **OpenTelemetry GenAI Semantic Conventions**: Formally split in June 2026 (v1.42.0) into the dedicated repository `open-telemetry/semantic-conventions-genai`, standardizing `gen_ai.operation.name`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, and `gen_ai.usage.output_tokens`.
   - **Hamel Husain 3-Level Evaluation Hierarchy**: Unit assertions (Level 1) → Model-based binary judges (Level 2) → Production telemetry & trajectory FSM analysis (Level 3).
5. **Security & Regulatory Mandates**:
   - **OWASP GenAI Top 10 (2025/2026)**: LLM01 Prompt Injection (direct and indirect cross-modal injection) confirmed as the #1 threat; Dual-LLM Privilege Quarantine and hardware microVM sandboxing (Firecracker/E2B) established as mandatory defenses.
   - **EU AI Act & ISO 42001**: Legal enforcement requiring reproducible evaluation suites, algorithmic fairness testing (Fairlearn), and cryptographic canary token monitoring.

---

## 2. Topic Classification & Action Matrix

Every research finding is classified according to the skill's taxonomy:

| Domain / Topic | Proposed Action | Target Phase / File | Primary Source & Spec | Architectural Rationale & Justification |
|:---|:---:|:---|:---|:---|
| **Stateless MCP (2026-07-28 Spec)** | `UPDATE_EXISTING` | Phase 03 & `agent-forge/mcp` | `modelcontextprotocol.io` / AAIF Linux Foundation | Upgrade from legacy stateful SSE to stateless HTTP transport, header caching hints, and Tasks extension. |
| **Google A2A Protocol** | `UPDATE_EXISTING` | Phase 04 & Phase 03 | `a2a-protocol.org` / Google ADK | Document cross-framework agent messaging contracts across Python, Go, and .NET. |
| **Agent Skills Specification (`SKILL.md`)** | `NEW_TOPIC` | Phase 08 & Phase 04 | Anthropic Agent Skills Spec / Claude Code | Standardize modular instruction playbooks as machine-readable repository contracts. |
| **Multi-Head Latent Attention (MLA)** | `NEW_TOPIC` | Phase 00 / Lesson 03 | DeepSeek-V3 Technical Report (arXiv:2412.19437) | Explain low-rank KV tensor compression and projection absorption as an alternative to GQA. |
| **Group Relative Policy Optimization (GRPO)** | `UPDATE_EXISTING` | Phase 00 / Lesson 04 | DeepSeek-R1 Paper (arXiv:2501.12948) | Detail critic-less group relative advantage calculations and rule-based rewards in reasoning models. |
| **Late Chunking Implementation** | `NEW_TOPIC` | Phase 02 / Lesson 02 | Jina AI (arXiv:2409.04701) | Add full mechanical derivation and code implementation (currently completely missing from Phase 02). |
| **Contextual Retrieval** | `NEW_TOPIC` | Phase 02 / Lesson 01 | Anthropic Research (2024) | Prepend LLM-generated document-level context to chunks before embedding to resolve ambiguous pronouns. |
| **RadixAttention & Tree-Based KV Reuse** | `UPDATE_EXISTING` | Phase 07 & Phase 01 | SGLang Paper (arXiv:2312.07104) | Full serving engine implementation of radix-tree KV pooling for multi-turn agent sessions. |
| **Speculative Decoding (EAGLE-3 / P-EAGLE)** | `NEW_TOPIC` | Phase 07 / Lesson 04 | vLLM / SGLang Upstream (arXiv:2401.15077) | Parallel draft token generation in a single forward pass, doubling inference TPS. |
| **Dedicated OTel GenAI Repo Splitting** | `UPDATE_EXISTING` | Phase 06 & `agent-forge/observability` | `open-telemetry/semantic-conventions-genai` (v1.42.0+) | Update import namespaces and attribute definitions to match the dedicated OpenTelemetry repository. |
| **Dual-LLM Quarantine Pattern** | `UPDATE_EXISTING` | Phase 05 & `labs/lab-06` | Simon Willison / OWASP GenAI LLM01 | Reconcile untrusted ingestion boundary, canary tokens, and structural privilege separation. |
| **OpenAI Agents SDK & Google ADK Lifecycle** | `UPDATE_EXISTING` | Phase 04 / Lesson 05 | OpenAI Platform / Google `agents-cli` | Align framework sections with official SDKs rather than deprecated third-party wrappers. |
| **Legacy Model References (`gpt-4-32k`, `ada-002`)** | `UPDATE_EXISTING` | Repo-wide & Examples | Upstream Provider APIs | Replace deprecated models with `claude-3-7-sonnet`, `gpt-4o`, `o3-mini`, `gemini-2.0-flash`, `deepseek-r1`. |
| **Unbuildable C# Examples** | `UPDATE_EXISTING` | `examples/*.cs` across 00–07 | .NET 9 / Microsoft Semantic Kernel 1.x | Scaffold `.csproj` project files and Microsoft.SemanticKernel NuGet references for polyglot CI. |
| **Missing Root Requirements** | `NEW_TOPIC` | Root Directory | Modern Python Tooling | Add root `pyproject.toml` or `requirements.txt` unifying dependencies across standalone examples. |

---

## 3. Phase-by-Phase Upgraded Topics & Roadmap

### Phase 00: Foundations & Token Mechanics
*Current State*: Modularized into 5 lessons, but missing MLA and deep GRPO mechanics.
*   **Multi-Head Latent Attention (MLA) Deep Dive**:
    - *The Physics*: Multi-Head Attention (MHA) consumes unscalable VRAM during decoding (`2 × 2 × Layers × H_KV × d_k × SeqLen`). Multi-Query Attention (MQA) and Grouped-Query Attention (GQA) reduce heads, sacrificing model expressiveness.
    - *The MLA Innovation*: Projects Key and Value vectors into a low-dimensional compressed latent space (`d_c = 512`), storing only the latent vector in the KV cache. Up-projections are absorbed into the Query and Output projection weights during inference forward passes.
    - *Systems Takeaway*: Delivers MQA-level memory footprints with MHA-level representation capacity.
*   **Group Relative Policy Optimization (GRPO) in Test-Time Compute**:
    - Contrast Proximal Policy Optimization (PPO), which requires an expensive value/critic model occupying GPU memory, with GRPO.
    - GRPO samples a group of candidate outputs `{o_1, o_2, ..., o_G}` for each prompt and evaluates relative advantages against the group mean using deterministic rule-based verification (math solver check, AST syntax validator, test runner).
    - Teaches why test-time compute scaling is stable without human reward model drift.

### Phase 01: Prompt & Context Engineering
*Current State*: Modularized into 5 lessons; strong Context AST and caching.
*   **OpenAI `developer` Message Role vs. System Role**:
    - Formally distinguish `role: "system"` from `role: "developer"` in OpenAI APIs, explaining how developer messages anchor immutable constraints above user turns.
*   **Assistant Prefilling Restrictions in Reasoning Models**:
    - Document why frontier reasoning models (OpenAI o1/o3, DeepSeek-R1) return HTTP 400 errors if assistant message prefilling is attempted, and how to structure few-shot reasoning prompts within user messages.
*   **Contextual Retrieval Augmentation (Anthropic)**:
    - Teach the context preparation pattern: using an offline batch LLM to synthesize a 50–100 token document context header prepended to every chunk before token budgeting and caching.

### Phase 02: Enterprise Retrieval & Knowledge Systems (RAG)
*Current State*: Monolithic README (6.8K words); Late Chunking completely missing from body.
*   **Late Chunking Mechanical Derivation & Implementation (Marquee Addition)**:
    - *Naive Chunking*: Cuts raw text into 512-token chunks -> Encodes each chunk independently -> Embeddings lose cross-chunk antecedents, pronoun referents, and global topic context.
    - *Late Chunking Pipeline*:
      1. Feed the entire document (up to 8,192 tokens) through a long-context transformer encoder (e.g. `jina-embeddings-v3`).
      2. Extract the full sequence of contextualized token embeddings from the final layer.
      3. Apply chunk span boundaries post-encoding.
      4. Mean-pool the contextualized token vectors across each chunk span.
    - *Result*: Every chunk vector retains full awareness of the entire document's semantic structure without fine-tuning.
*   **Contextual Retrieval Integration**:
    - Prepending situational context headers before BM25 inverted index tokenization to resolve ambiguous queries in sparse search.
*   **Two-Stage Retrieval Pipeline Topology**:
    - Stage 1: Parallel Dense (HNSW) + Sparse (BM25) search with Reciprocal Rank Fusion (`k=60`).
    - Stage 2: Cross-Encoder full-attention reranking (`O((L_q + L_d)^2)`) on the top-50 candidates to produce top-5 high-precision chunks.

### Phase 03: Tools & Model Context Protocol (MCP)
*Current State*: Monolithic README (8.6K words); references early stateful MCP.
*   **Stateless MCP 2026 Specification (AAIF / Linux Foundation)**:
    - *Governance*: Transition from Anthropic proprietary project to Linux Foundation Agentic AI Foundation.
    - *Wire Protocol*: Stateless JSON-RPC 2.0 over Streamable HTTP/SSE.
    - *Cacheable Requests*: HTTP `MCP-Cache-Key` and `E-Tag` headers allowing API gateways to cache tool schema discovery (`tools/list`) and resource declarations (`resources/list`).
    - *The Tasks Extension (AWS contribution)*: Asynchronous long-running agent tasks supporting progress polling, cancellation, and durable checkpointing.
*   **ABAC Execution Policies & Sandboxing**:
    - Enforce Attribute-Based Access Control (ABAC) per tenant, role, and environment before tool arguments are dispatched to execution sandboxes (Firecracker microVMs or gVisor).

### Phase 04: Stateful Agent Orchestration
*Current State*: Monolithic README (18.8K words); loop engineering buried in Section 5.1.
*   **Loop Engineering as Core Foundation (Section Reorganization)**:
    - Elevate Action Hashing (SHA-256 fingerprinting of tool calls), Action Frequency Tracking, and Progressive Budget Decay from comparative analysis into the primary loop design section.
*   **Google Agent-to-Agent (A2A) Protocol (`a2a-protocol.org`)**:
    - Implement typed JSON-RPC handoff contracts between autonomous agents across different teams and runtimes (e.g. Python procurement agent handing off to Go compliance agent).
*   **OpenAI Agents SDK & Google ADK Modernization**:
    - Ground agent recipes in official enterprise toolchains: Google ADK + `agents-cli` and OpenAI Agents SDK, replacing legacy LangChain wrappers.

### Phase 05: AI Security & Guardrails
*Current State*: Monolithic README (8.3K words); LaTeX formulas throughout.
*   **OWASP Top 10 for GenAI 2025/2026 Alignment**:
    - LLM01: Prompt Injection (Direct, Indirect, Cross-modal).
    - LLM02: Sensitive Information Disclosure & PII token vaults.
    - LLM07: System Prompt Leakage & canary token trips.
*   **Dual-LLM Privilege Quarantine Architecture**:
    - Separation of Untrusted Ingress LLM (quarantined, zero tools, outputs sanitized JSON) from Privileged Orchestrator LLM (governed tools, trusted system directives).

### Phase 06: GenAI Evals & Observability
*Current State*: Monolithic README (6.6K words); OTel namespace update needed.
*   **Dedicated OpenTelemetry GenAI Semantic Conventions (`semantic-conventions-genai`)**:
    - Update attribute mappings to reflect the June 2026 repository split:
      - `gen_ai.operation.name`: `chat`, `text_completion`, `embeddings`, `execute_tool`.
      - `gen_ai.request.model`, `gen_ai.response.model`.
      - `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`.
      - Opt-in tracing for prompts/completions to avoid enterprise PII leakage.
*   **Hamel Husain 3-Level Evaluation Flywheel**:
    - Formalize the hierarchy: Level 1 (Deterministic code assertions), Level 2 (Model-based binary rubric judges with G-Eval chain-of-thought), Level 3 (Production trajectory monitoring).

### Phase 07: High-Throughput Serving & LLMOps
*Current State*: Monolithic README (12K words); missing modern speculative decoding mechanics.
*   **RadixAttention Deep Dive (SGLang & vLLM)**:
    - Trie-based data structures maintaining KV-cache blocks across multiple requests.
    - Automatic prefix matching for system prompts, few-shot examples, and multi-turn agent histories without explicit client cache tokens.
*   **Speculative Decoding with EAGLE-3 & P-EAGLE**:
    - Traditional speculative decoding: Autoregressive draft model generates K tokens sequentially (limited by draft model memory bandwidth) -> Target model verifies in parallel.
    - P-EAGLE (Parallel EAGLE): Generates multiple draft tokens in a **single forward pass** using feature-level representations -> Eliminates draft sequential overhead, achieving 2.5–3.5x wall-clock speedups on Hopper/Blackwell GPUs.
*   **Dynamic Multi-LoRA Serving (S-LoRA)**:
    - Host unified 70B base model while dynamically swapping 100+ low-rank LoRA adapter matrices in unified GPU memory.

### Phase 08: AI-Augmented SDLC & Leadership
*Current State*: Monolithic README (11.7K words); tool matrices need 2026 alignment.
*   **Spec-Driven Development (SDD) & Agent Skills**:
    - From prompt chatting to formal specifications: `SPEC.md`, architectural invariants, and machine-readable codebase contracts (`AGENT.md`).
    - Standardize modular Agent Skills (`SKILL.md`) as executable team engineering playbooks for code review, database migration, and security auditing.
*   **Verified Agentic Engineering (TDD Invariant Gates)**:
    - Autonomous coding agents operating inside tight test-driven verification loops: write failing test -> implement minimal code -> run linter -> verify pass -> submit PR.

---

## 4. Hands-On Practice Labs & Capstones Roadmap

### Lab Suite Reconciliation
The repository currently contains two competing lab architectures. We recommend establishing the root `labs/lab-01` through `lab-07` suite as the **canonical, automated curriculum labs**, while preserving Phase 04's internal labs as specialized exercises:

| Lab | Canonical Name | Target Microservice / Pattern | Verification Test (`scripts/verify_lab.py`) |
|:---:|:---|:---|:---|
| **01** | **Multi-Tenant Hybrid RAG** | `agent_forge/retrieval/hybrid_engine.py` | `verify_lab_01`: BM25 + Dense HNSW + RRF `k=60` with tenant-isolated filtering. |
| **02** | **Tool Execution with MCP** | `agent_forge/mcp/policy_engine.py` | `verify_lab_02`: FastMCP server exposing JSON-RPC tools with ABAC authorization. |
| **03** | **Stateful Agent Orchestration** | `agent_forge/runtime/orchestrator.py` | `verify_lab_03`: ReAct loop with Write-Ahead Log (WAL) event sourcing & crash recovery. |
| **04** | **Agent Failure Defense** | `agent_forge/gateway/rate_limiter.py` | `verify_lab_04`: Token-bucket limiter with reservation and post-stream settlement. |
| **05** | **AI Observability & Tracing** | `agent_forge/observability/tracer.py` | `verify_lab_05`: OpenTelemetry GenAI span generation with standard attributes. |
| **06** | **Dual-LLM Quarantine** | `agent_forge/runtime/quarantine.py` | `verify_lab_06`: Isolating untrusted inputs from privileged tool execution perimeters. |
| **07** | **Hybrid ML Fairness & Evals** | `agent_forge/evals/fairness.py` | `verify_lab_07`: Fairlearn Disparate Impact Ratio audit and TreeSHAP explainability. |

---

## 5. Models & Code Reference Modernization

To prevent the curriculum from teaching deprecated APIs, all lesson code blocks and examples must align with modern production SDKs:

### Model Identifier Upgrades
| Deprecated / Legacy Model | Modern Production Model (2025–2026) | Provider & Context Window | Primary Use Case |
|:---|:---|:---|:---|
| `gpt-4-32k` / `gpt-4-0613` | `gpt-4o` / `gpt-4o-mini` | OpenAI (128K context) | High-speed structured extraction & general orchestration |
| `o1-preview` / manual CoT | `o3-mini` / `o3` | OpenAI (200K context, configurable reasoning effort) | Deep algorithmic math, planning, and code verification |
| `claude-3-opus-20240229` | `claude-3-7-sonnet-20250219` | Anthropic (200K context, hybrid reasoning) | Architecture design, coding agents, complex system analysis |
| `text-embedding-ada-002` | `text-embedding-3-large` / `jina-embeddings-v3` | OpenAI (3072 dims) / Jina AI (8192 context, Late Chunking) | Production dense vector retrieval & Late Chunking |
| `google-generativeai` (SDK) | `google-genai` (SDK) + `gemini-2.0-flash` | Google Cloud (1M–2M context, native thinking) | Multimodal ingestion, long-context reasoning, context caching |
| Generic 70B Dense Model | `deepseek-r1` / `deepseek-v3` | DeepSeek / Self-hosted vLLM (128K context, MLA + MoE) | High-throughput open-weights reasoning & cost optimization |
| Edge toy models | `phi-4` (14B) / `gemma-2-9b` | Microsoft / Google (4-bit AWQ/GPTQ quantized) | Local client-side and edge-device inference |

### Upstream SDK Dependencies
- **Python**: Enforce `python >= 3.12`, `pydantic >= 2.10`, `fastmcp >= 0.4.0`, `google-genai >= 0.1.0`, `opentelemetry-api >= 1.28.0`, and `vllm >= 0.7.0`.
- **C# / .NET 9**: Add `.csproj` harnesses referencing `Microsoft.SemanticKernel >= 1.35.0` and `System.Text.Json`.

---

## 6. Senior & Staff AI Engineer System Design Interview Q&A

Modern Staff AI Engineer interviews focus heavily on distributed systems failure modes, hardware realities, and probabilistic trade-offs:

### Question 1: How do you architect a multi-tenant inference gateway to handle KV cache memory exhaustion under concurrent 100K-token requests?
*   **Model Answer**:
    - *Hardware Bottleneck*: Autoregressive decoding is memory-bandwidth bound. A 100K token context across 50 concurrent sessions exceeds GPU High Bandwidth Memory (HBM3e).
    - *Architectural Solution*:
      1. Deploy **PagedAttention** (vLLM) to eliminate physical memory fragmentation and allocate non-contiguous physical RAM pages.
      2. Implement **Chunked Prefill**: Split massive 100K prompts into smaller chunks (e.g. 512 tokens), interleaving prompt prefill with ongoing decode steps to prevent GPU idle bubbles.
      3. Enable **Prefix Caching & RadixAttention**: Index common system prompts in a trie to share KV activations across tenants without recomputation.
      4. Gateway-level **Token-Bucket Governor**: Require clients to reserve maximum expected context tokens upfront, enforcing HTTP 429 backpressure before requests hit the GPU queue.

### Question 2: Why does naive chunking degrade retrieval precision in RAG, and how does Late Chunking mathematically solve it?
*   **Model Answer**:
    - *Naive Failure*: Splitting text before embedding severs cross-chunk self-attention. A pronoun ("It achieved 40% growth") in Chunk 2 loses connection to the entity ("Project Apollo") in Chunk 1, causing vector representations to collapse.
    - *Late Chunking Mechanics*: Pass the complete document through a long-context transformer encoder *first*. Every token's vector representation attends to all other tokens in the document via full bidirectional attention. Once contextualized embeddings are produced, chunk boundaries are applied and token vectors are mean-pooled.
    - *Trade-off*: Late chunking requires long-context embedding models and higher encode latency during ingestion, but completely preserves semantic coherence without needing an LLM rewrite step.

### Question 3: How do you guarantee deterministic state recovery in autonomous agents when an external tool execution crashes mid-flight?
*   **Model Answer**:
    - *The Problem*: If an agent is midway through a multi-step financial transaction and the pod crashes, re-running the prompt from scratch triggers duplicate API mutations and state corruption.
    - *Architectural Solution*:
      1. **Event-Sourced Write-Ahead Log (WAL)**: Every state transition (Prompt -> Thought -> Tool Call -> Tool Result) is assigned a monotonic sequence number and appended to an append-only event store (e.g. PostgreSQL or Redis stream) before execution.
      2. **Idempotency Keys**: All tool executions carry a deterministic UUID generated from `SHA256(session_id + step_number + tool_name + args)`. Downstream services reject duplicate keys.
      3. **Distributed Saga Pattern**: For non-idempotent operations, pair each mutating tool with an explicit compensating transaction tool (e.g. `reserve_funds` paired with `release_funds`).
      4. **Rehydration**: On crash recovery, replay the WAL to reconstruct the agent's exact in-memory state graph without re-invoking already completed external tools.

---

## 7. Next Steps & Recommendations

1. **Awaiting User Review**: This report captures the complete, up-to-date industry roadmap across all phases.
2. **Phase 02 Next Up**: Begin refactoring Phase 02 (`02-rag-and-knowledge-systems`) to decompose its 6.8K-word monolithic README into 6 modular 4-tier lessons and add the missing **Late Chunking deep-dive**.
3. **Preserve Content Depth**: Adhere strictly to the core axiom: *"Do not teach less. Teach better."*
