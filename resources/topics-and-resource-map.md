# AI Engineering & Agentic AI — Comprehensive Resource Map

> **A definitive, phase-by-phase reference mapping core topics directly to authoritative official documentation, free courses, GitHub repositories, and seminal engineering guides.**

---

## 📑 Index of Phases

| Phase | Domain | Primary Focus |
|:---:|:---|:---|
| **0** | [AI / LLM Foundations](#phase-0--ai--llm-foundations) | Transformer mechanics, tokens, sampling, embeddings, inference economics |
| **1** | [Prompt Engineering](#phase-1--prompt-engineering) | Prompt hierarchy, system instructions, few-shot, XML, chaining |
| **2** | [Structured Output & Tool Calling](#phase-2--structured-output--function-calling) | JSON Schema, function calling, tool execution, validation & retry |
| **3** | [RAG Fundamentals](#phase-3--rag-fundamentals) | Embeddings, vector search, chunking, metadata indexing, retrieval |
| **4** | [Advanced RAG](#phase-4--advanced-rag) | Hybrid search, BM25, reranking, query transformation, GraphRAG |
| **5** | [Model Context Protocol (MCP)](#phase-5--mcp) | MCP Host, Client, Server, tools, transports, security |
| **6** | [AI Security & Guardrails](#phase-6--ai-security--guardrails) | Injections, data poisoning, least privilege, sandboxing, guardrails |
| **7** | [AI Agents](#phase-7--ai-agents) | Agentic loop, planning, tool selection, reflection, multi-agent |
| **8** | [Context Engineering](#phase-8--context-engineering) | Context windows, compaction, summarization, prompt caching |
| **9** | [Memory & Sessions](#phase-9--memory--sessions) | Short/long-term memory, semantic/episodic, session state, checkpointing |
| **10** | [Agent Reliability](#phase-10--agent-reliability) | Retries, circuit breakers, idempotency, loop limits, graceful degradation |
| **11** | [Evaluations](#phase-11--evals) | Golden datasets, regression evals, LLM-as-a-judge, trajectory metrics |
| **12** | [Observability & Tracing](#phase-12--observability--tracing) | OpenTelemetry GenAI spans, metrics, latency, token costs, debugging |
| **13** | [Claude / Anthropic Ecosystem](#phase-13--claude--anthropic) | Claude 3.5/3.7, Messages API, prompt caching, MCP, Claude Code |
| **14** | [Gemini / Google GenAI](#phase-14--gemini--google-genai) | Gemini models, GenAI SDK (Python & .NET), context caching, grounding |
| **15** | [Google ADK](#phase-15--google-adk) | Agent Development Kit, agents-cli, multi-agent, deployment |
| **16** | [Google Cloud Enterprise AI](#phase-16--google-cloud-enterprise-ai) | Vertex AI, Cloud Run, BigQuery grounding, enterprise security |
| **17** | [AI Application Architecture](#phase-17--ai-application-architecture) | AI Gateways, event-driven AI, microservices, .NET & Python integration |
| **18** | [AI Cost & Performance](#phase-18--ai-cost--performance) | Token optimization, model routing, caching, latency vs cost |
| **19** | [AI CI/CD & SDLC](#phase-19--ai-cicd--sdlc) | Versioning, automated evals, canary deploy, feedback loop |
| **20** | [AI Governance](#phase-20--ai-governance) | Responsible AI, NIST RMF, data lineage, compliance |
| **21** | [A2A & Interoperability](#phase-21--a2a--agent-interoperability) | Agent-to-Agent protocol, discovery, multi-agent federation |
| **22** | [Advanced Agent Engineering](#phase-22--advanced-agent-engineering) | Reflection, critic loops, durable execution, replay, sandboxing |
| **23** | [AI System Design & Interview Mastery](#phase-23--ai-system-design--interview-mastery) | HLD/LLD, scalability, reliability, enterprise architectural blueprints |

---

## Phase 0 — AI / LLM Foundations

### Core Topics
- LLM fundamentals & Transformer architecture
- Scaled Dot-Product Attention & Multi-Head Attention mechanics
- Tokens, Byte-Pair Encoding (BPE), and vocabulary tokenization
- Model parameters, precision (FP16, BF16, FP8, INT4), and Quantization (AWQ, GPTQ)
- Sampling parameters: Temperature, Top-P, Top-K, Min-P, Seed
- Vector embeddings & Semantic similarity spaces
- Multimodal foundation models (Text, Vision, Audio)
- Reasoning & Thinking models (OpenAI o1, o3, o4-mini, Claude 4 Opus, Claude 3.7 Sonnet extended thinking, Gemini 2.5 Thinking, DeepSeek-R1)
- Thinking token economics: Reasoning token pricing, hidden scratchpad billing, and inference budget caps
- Small Language Models (SLMs) on device and edge: Microsoft Phi-4, Google Gemma 2, Alibaba Qwen 2.5
- Test-Time Compute: Reasoning tokens, thinking budgets, and inference scaling laws
- Inference mechanics: Prefill vs. Decode phases, TTFT vs. Tokens-Per-Second (TPS)
- Physical hardware realities: Memory bandwidth ceilings & KV-cache VRAM allocation
- AI economics: Token cost structures, batch discounts, and prompt caching amortization

### Curated Resources
- [Google AI for Developers](https://ai.google.dev/) — *Official Gemini 2.0/2.5 APIs, models, and quickstarts*
- [Anthropic Claude Documentation](https://docs.anthropic.com/) — *Claude 3.7 Sonnet models, hybrid reasoning, and capabilities*
- [DeepSeek-R1 Research Paper](https://arxiv.org/abs/2501.12948) — *Incentivizing reasoning capability in LLMs via reinforcement learning (GRPO)*
- [DeepLearning.AI — Reasoning with o1](https://www.deeplearning.ai/short-courses/reasoning-with-o1/) — *Test-time compute, chain-of-thought, and reasoning budgets with OpenAI*
- [DeepLearning.AI — Reinforcement Fine-Tuning LLMs with GRPO](https://www.deeplearning.ai/short-courses/reinforcement-fine-tuning-llms-with-grpo/) — *Group Relative Policy Optimization behind DeepSeek R1*
- [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/) — *Open-source models, tokenization, and inference*
- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/) — *Intuitive visual walkthrough of Attention*
- [Andrej Karpathy — Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) — *Masterclass building GPT from scratch*

---

## Phase 1 — Prompt Engineering

### Core Topics
- Prompt hierarchy & Role boundaries (System / Developer / User / Assistant)
- Zero-shot and Few-shot prompting patterns
- Role prompting & Persona calibration
- XML delimiters & Structured prompt layout (Anthropic standards)
- Prompt templates & Variable injection
- Prompt chaining & Sequential task decomposition
- Chain-of-Thought (CoT) & Reasoning prompts
- Tool-use prompting & Schema framing
- System prompt optimization & Token budget discipline

### Curated Resources
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — *XML tags, system prompts, few-shot patterns*
- [Google Prompt Design Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) — *Gemini prompt optimization and multimodal guidance*
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) — *Systematic prompt tactics and reasoning strategies*
- [DeepLearning.AI — ChatGPT Prompt Engineering](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/) — *Developer fundamentals by Andrew Ng & Isa Fulford*
- [Anthropic Prompting Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables) — *Production prompt templates and variables*

---

## Phase 2 — Structured Output & Function Calling

### Core Topics
- Deterministic JSON output vs. free-form text
- JSON Schema (Draft 2020-12) & Pydantic / Zod contracts
- Constrained grammar decoding & Finite State Machine (FSM) logit masking
- Strict mode schema adherence (`strict: true`)
- Function calling & Tool definitions
- Tool arguments validation & Parameter binding
- Parallel vs. Sequential tool calls
- Tool execution loops & Result ingestion
- Error self-healing: Feeding syntax/schema errors back into context

### Curated Resources
- [Gemini Function Calling](https://ai.google.dev/gemini-api/docs/function-calling) — *Tool declarations and execution with Gemini*
- [Gemini Structured Output](https://ai.google.dev/gemini-api/docs/structured-output) — *Guaranteed JSON schema enforcement*
- [Claude Tool Use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) — *Tool definitions, tool choices, and streaming*
- [Google GenAI Python SDK](https://github.com/googleapis/python-genai) — *Official Python SDK for Gemini*
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python) — *Official Python SDK for Claude*

---

## Phase 3 — RAG Fundamentals

### Core Topics
- Vector embeddings & Dimensionality
- Dense vector similarity search (Cosine, Dot Product, Euclidean)
- Vector databases & ANN indexing (HNSW, IVFFlat)
- Document ingestion & Layout-aware parsing
- Chunking strategies: Fixed-size, Recursive, Semantic, Document-structure
- Metadata filtering & Partitioning
- Vector indexing & Storage tiers
- Top-K candidate retrieval
- Context window construction & XML tagging
- Grounded generation & Direct citation attribution

### Curated Resources
- [Hamel Husain — Mastering LLMs](https://hamel.dev/blog/posts/course/) — *Practical, engineering-first LLM & RAG guide*
- [DeepLearning.AI Courses](https://www.deeplearning.ai/courses/) — *Short courses on vector databases and RAG*
- [LlamaIndex Documentation](https://docs.llamaindex.ai/) — *Data framework for LLM knowledge ingestion*
- [LangChain Documentation](https://python.langchain.com/docs/) — *RAG chains, splitters, and vector stores*
- [Pinecone Learn](https://www.pinecone.io/learn/) — *Vector search mechanics, indexing algorithms, and metrics*
- [FAISS GitHub](https://github.com/facebookresearch/faiss) — *Facebook AI Similarity Search library*

---

## Phase 4 — Advanced RAG

### Core Topics
- Naive RAG limitations (Keyword misses, semantic drift, lost-in-the-middle)
- Hybrid search: BM25 (sparse lexical) + HNSW (dense semantic)
- Reciprocal Rank Fusion (RRF) candidate merging
- Cross-Encoder reranking (Cohere, ms-marco) & Threshold pruning
- Query transformation: Expansion, Decomposition, HyDE (Hypothetical Document Embeddings)
- Multi-query generation & Step-back prompting
- Parent-child chunking & Hierarchical retrieval
- Context compression & Token compaction
- GraphRAG: Knowledge graphs, Entity-Relation triples
- Corrective RAG (CRAG) & Self-RAG reflection loops
- Multi-hop retrieval & Query routing across heterogeneous indexes
- Multi-tenant data isolation & Document-level RBAC

### Curated Resources
- [LlamaIndex Advanced RAG Guide](https://docs.llamaindex.ai/) — *Rerankers, query engines, and hybrid pipelines*
- [Microsoft GraphRAG GitHub](https://github.com/microsoft/graphrag) — *Modular graph-based RAG pipeline*
- [Pinecone Learning Center — Hybrid Search](https://www.pinecone.io/learn/) — *Combining dense and sparse retrieval*
- [Hamel Husain — Creating a Great RAG System](https://hamel.dev/blog/posts/course/) — *Evaluation and retrieval optimization*

---

## Phase 5 — Model Context Protocol (MCP)

### Core Topics
- MCP architecture & Protocol specifications (JSON-RPC 2.0 wire format)
- Linux Foundation donation & open governance ecosystem (10,000+ public/community MCP servers)
- Stateless Core architecture specification (July 2026 revision)
- MCP Host (Orchestrator), MCP Client, and MCP Server topology
- Primitives: Tools (actions), Resources (data), Prompts (templates)
- MCP Tasks Extension: Long-running asynchronous tasks, progress notifications, and task cancellation
- MCP Apps: Interactive UI rendering, tool frontends, and human-in-the-loop widgets
- Standardized tool discovery (`tools/list`), dynamic schema negotiation, and `ttlMs` client-side caching
- Transports: `stdio` (local subprocess) vs. `SSE` / HTTP (remote microservices)
- FastMCP Python framework for high-level schema definition
- Agent Skills: Modular folder-based instructions and MCP capability extensions
- Reverse Sampling: Server requesting LLM completions through Host
- Enterprise authentication & authorization: OAuth 2.1 authorization code flow with PKCE, TLS/mTLS configuration
- Ephemeral container sandboxing (Docker, gVisor) for tool execution
- Production MCP servers (10K+ ecosystem) & Enterprise gateway patterns

### Curated Resources
- [Model Context Protocol — Official Documentation](https://modelcontextprotocol.io/) — *Official architecture, Linux Foundation governance, and quickstarts*
- [MCP Specification & Governance](https://modelcontextprotocol.io/specification/latest) — *Stateless Core (July 2026), Tasks extension, OAuth 2.1, and JSON-RPC 2.0 standard*
- [MCP GitHub Organization](https://github.com/modelcontextprotocol) — *Core SDKs (TypeScript, Python, Kotlin) and 10K+ server registry*
- [FastMCP GitHub Repository](https://github.com/jlowin/fastmcp) — *High-level framework for building MCP servers*
- [DeepLearning.AI — MCP: Build Rich-Context AI Apps](https://www.deeplearning.ai/short-courses/mcp-build-rich-context-ai-apps-with-anthropic/) — *Hands-on MCP apps with Anthropic engineers*
- [DeepLearning.AI — Agent Skills with Anthropic](https://www.deeplearning.ai/short-courses/agent-skills-with-anthropic/) — *Modular instruction folders and subagent tooling*
- [DeepLearning.AI — Claude Code: Agentic Coding](https://www.deeplearning.ai/short-courses/claude-code-a-highly-agentic-coding-assistant/) — *Terminal agent orchestration and MCP integration*

---

## Phase 6 — AI Security & Guardrails

### Core Topics
- The OWASP Top 10 for LLM Applications & Agentic Systems
- Direct prompt injections: Delimiter escapes, Jailbreak bypasses
- Indirect prompt injections: Poisoned RAG documents, Webhooks, Emails
- Data poisoning & Embedding manipulation
- Excessive agency & Preventing the Confused Deputy problem
- Dual-LLM Privilege Separation (Quarantine Pattern)
- Cryptographic canary tokens for prompt leak detection
- PII tokenization, redaction & Egress data vaulting
- Hallucination mitigation: Citation grounding & NLI entailment verification
- Multi-tier guardrails (NeMo Guardrails, Meta Llama Guard 3)
- Tool authorization & Human-in-the-Loop (HITL) step-up gates
- Ephemeral execution sandboxes (gVisor, WASM)

### Curated Resources
- [OWASP GenAI Security Project](https://genai.owasp.org/) — *Top 10 risks, mitigation checklists, and governance*
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — *Authoritative risk classification*
- [Anthropic — Mitigating Jailbreaks & Prompt Injections](https://www.anthropic.com/research) — *Research on frontier model defense*
- [Google Secure AI Framework (SAIF)](https://saif.google/) — *Enterprise framework for secure AI systems*
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — *Federal standards for AI governance*

---

## Phase 7 — AI Agents

### Core Topics
- Defining agents: Deterministic workflows vs. Autonomous loops
- The Anthropic 5 Workflow Patterns: Chaining, Routing, Parallel, Orchestrator-Workers, Evaluator-Optimizer
- The ReAct (Reasoning + Acting) loop
- Planning and Subgoal decomposition (Plan-and-Solve)
- Modern Agent Frameworks:
  - **PydanticAI**: Type-safe agents, dependency injection, and validated streaming
  - **OpenAI Agents SDK**: Handoffs, guardrails, and isolated code sandboxes
  - **LangGraph**: Cyclical state machines, durable Postgres/Redis checkpoints, time travel
  - **Google ADK**: Code-first agents with `agents-cli` scaffolding and Cloud Run deployment
  - **Microsoft Semantic Kernel**: Enterprise C#/.NET plugins, DI containers, and `AgentGroupChat`
- Tool selection, execution, and observation feedback
- State tracking, termination conditions, and timeout budgets
- Loop Engineering: Convergence detection, oscillation mitigation, and infinite-loop tripwires
- CodeAct architecture: Executing executable Python code actions vs. structured JSON tool calls
- Harness Engineering: Test harnesses, sandboxed workspace runtimes, and environment injection for agent self-validation
- Durable execution for agents: Temporal.io workflow state machines and DBOS transactional serverless runtimes
- AutoGen architectural bifurcation: AutoGen v0.4 (async event-driven architecture) vs. AG2 (multi-agent continuation fork)
- Multi-Agent Topologies: Supervisor, Hierarchical Teams, Swarm / Dynamic Handoff, Debate
- Human-in-the-Loop (HITL) pause, approval, and resume patterns

### Curated Resources
- [PydanticAI Official Documentation](https://ai.pydantic.dev/) — *Type-safe agent framework by the Pydantic team*
- [OpenAI Agents SDK (`openai-agents`)](https://github.com/openai/openai-agents-python) — *Official production framework for multi-agent handoffs*
- [Hugging Face smolagents](https://github.com/huggingface/smolagents) — *Minimalist CodeAct agent framework executing Python actions*
- [Building Effective Agents (Anthropic Engineering)](https://www.anthropic.com/engineering/building-effective-agents) — *The foundational workflow vs. agent taxonomy*
- [Google ADK Documentation](https://google.github.io/adk-docs/) — *Code-first multi-agent framework*
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) — *Durable stateful agent orchestration*
- [Microsoft Semantic Kernel](https://learn.microsoft.com/semantic-kernel/) — *Enterprise AI orchestration for C# and Python*
- [AG-UI (Agentic GUI Protocol)](https://github.com/ag-ui/ag-ui) — *Standardized agent UI interaction layer and human-in-the-loop frontend integration*

---

## Phase 8 — Context Engineering

### Core Topics
- Context windows as dynamic, finite memory systems
- Context Abstract Syntax Tree (AST): Hierarchical token layout and structured semantic zoning
- Context budgeting: Deterministic token allocations for instructions, tools, retrieved RAG, and scratchpad
- Context rot & Attention degradation under prolonged multi-turn sessions
- Maximum Effective Context Window (MECW) vs. advertised theoretical limits
- Context construction: System instructions, few-shot examples, dynamic state
- Context prioritization & Dynamic re-anchoring
- Context compression: LLMLingua-2, token pruning, task-agnostic compression
- Hierarchical conversation summarization
- Context routing: Directing specialized prompts to specialized sub-agents
- Context isolation & Cross-tenant contamination prevention
- Mitigating "Lost-in-the-Middle" attention valleys
- Tool loadout pruning: Dynamic reduction of tool schemas to prevent attention dilution
- Anthropic Contextual Retrieval: Prepended contextual explanation chunks for RAG
- Just-In-Time (JIT) tool & context discovery: Fetching specialized schemas and context slices on-demand
- Tool-result pruning & Intermediate scratchpad management
- Prompt Caching & Prefix Caching mechanics (Anthropic, Gemini, OpenAI)

### Curated Resources
- [Anthropic Prompt Caching Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) — *Architecture and economics of prefix caching*
- [Anthropic Contextual Retrieval Guide](https://www.anthropic.com/news/contextual-retrieval) — *Optimizing RAG retrieval using chunk-specific context prepending*
- [Gemini Context Caching Guide](https://ai.google.dev/gemini-api/docs/caching?lang=python) — *Explicit context caching and TTL management*
- [Google Gemini Caching API Reference](https://ai.google.dev/api/caching) — *REST and SDK caching primitives*
- [Microsoft LLMLingua-2 Repository](https://github.com/microsoft/LLMLingua) — *Task-agnostic prompt compression and token pruning*

---

## Phase 9 — Memory & Sessions

### Core Topics
- Conversation history tracking & Window sliding
- 4-Tier Memory Taxonomy: Ephemeral Working Memory, Short-Term Session Buffer, Long-Term Episodic Memory, Persistent Semantic Knowledge
- Session management & Distributed session stores (Redis, PostgreSQL)
- Working memory (scratchpad & ephemeral state)
- Short-term memory (active session turns)
- Long-term memory: Semantic (facts), Episodic (past experiences), Procedural (tool rules)
- Autonomous memory platforms: Mem0 (personalized memory layer) and Letta (stateful agent OS)
- Temporal Knowledge Graph memory: Zep and Graphiti for evolving episodic relationship tracking
- Hippocampal associative memory: HippoRAG for neurobiology-inspired multi-hop recall
- Memory retrieval via vector search & Reciprocal Rank Fusion
- Forgetting curves & decay mechanisms: Ebbinghaus curve modeling for recency-frequency decay
- Memory summarization, compaction, and lifecycle management
- Session pause, resumption, and checkpointing
- Session forking: Speculative branching and rollback
- Standardized memory interoperability: MCP `server-memory` reference protocol for cross-agent recall
- Memory governance & Data privacy compliance: Crypto-shredding of tenant keys for GDPR right to be forgotten

### Curated Resources
- [Google ADK Sessions & Memory Guide](https://google.github.io/adk-docs/sessions/) — *Stateful sessions and memory management*
- [Google ADK Memory Module](https://google.github.io/adk-docs/sessions/memory/) — *Long-term memory persistence*
- [Mem0 Official Documentation](https://docs.mem0.ai/) — *Production memory layer for personalized AI agents*
- [Letta Documentation](https://docs.letta.com/) — *Operating system for building stateful LLM agents with tiered memory*
- [Zep & Graphiti Knowledge Graphs](https://github.com/getzep/graphiti) — *Dynamic temporal knowledge graphs for agent memory*
- [HippoRAG Research Paper](https://arxiv.org/abs/2405.14831) — *Neurobiologically inspired long-term associative memory for LLMs*
- [Agent Engineering Roadmap — Memory](https://github.com/audi0417/agent-engineering-roadmap) — *Memory patterns for autonomous agents*

---

## Phase 10 — Agent Reliability

### Core Topics
- Non-deterministic failure modes & Error cascade prevention
- Exponential backoff with decorrelated jitter (HTTP 429 & 500 handling)
- Explicit timeout budgets per step and per workflow
- Circuit breaker patterns for model endpoints and tool calls
- Idempotency keys for tool operations & Preventing duplicate transactions
- Distributed rate limiting (Token Bucket, Sliding Window)
- Dynamic token budgeting & Loop iteration caps
- Fallback models: Primary (High reasoning) $\to$ Secondary (High speed)
- Graceful degradation: Partial task completion & Fallback responses
- Durable execution & Checkpointed state graphs
- Human escalation triggers & Emergency stop mechanisms

### Curated Resources
- [Google ADK Documentation](https://google.github.io/adk-docs/) — *Resilience, callbacks, and error handling*
- [Microsoft Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/) — *Integration with Polly enterprise resilience policies*
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/) — *Failure tracing and distributed monitoring*

---

## Phase 11 — Evals

### Core Topics
- Shifting from subjective "vibe checks" to deterministic continuous evaluation
- Golden datasets: Composition (50% Core, 25% Edge, 15% Adversarial, 10% Known Failures)
- Level 1: Deterministic unit tests (JSON Schema, regex, latency ceilings)
- Level 2: Model-based evaluation (LLM-as-a-Judge with discrete binary rubrics)
- Level 3: Online telemetry & Production feedback loops
- RAG evaluation: Retrieval precision, Context recall, Faithfulness, Groundedness
- Agent trajectory evaluation: Tool selection accuracy, Step efficiency, Loop detection
- Avoiding judge biases: Position bias, Verbosity bias, Self-enhancement bias
- Synthetic test data generation via stronger teacher models (Evol-Instruct)
- Automated CI/CD evaluation gates blocking regressive PRs

### Curated Resources
- [Hamel Husain — AI Evals FAQ](https://hamel.dev/blog/posts/evals-faq/) — *Binary pass/fail criteria and evaluation design*
- [Hamel Husain — Evals Getting Started Guide](https://hamel.dev/notes/llm/evals/start/) — *Practical evaluation walkthrough*
- [Hamel Husain — LLM-as-a-Judge Guide](https://hamel.dev/blog/posts/llm-judge/) — *Step-by-step rubric creation and debiasing*
- [Inspect AI (UK AI Safety Institute)](https://inspect.aisi.org.uk/) — *Open-source framework for LLM evaluation*
- [Google ADK Evaluation Guide](https://google.github.io/adk-docs/evaluate/) — *Evaluating ADK multi-agent systems*

---

## Phase 12 — Observability & Tracing

### Core Topics
- OpenTelemetry (OTel) GenAI Semantic Conventions (`gen_ai.system`, `gen_ai.usage.*`)
- Distributed trace spans: Tracing parent-child relationships across multi-step agents
- Correlation IDs, Session IDs, and Agent Run IDs
- LLM call traces, Retrieval traces, and Tool invocation spans
- The Six Golden Signals: TTFT, TPS, Cache Hit Rate, Token Ratio, Fallback Rate, Cost
- Waterfall latency analysis & Identifying execution bottlenecks
- Production debugging workflows & Trace log isolation
- Enterprise observability platforms: Langfuse, Arize Phoenix, LangSmith

### Curated Resources
- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — *Official W3C / CNCF specification*
- [Langfuse Documentation & Architecture](https://langfuse.com/docs) — *Open-source AI observability and tracing*
- [Arize Phoenix](https://phoenix.arize.com/) — *Vector retrieval diagnostics and evaluation tracing*
- [Google ADK Observability](https://google.github.io/adk-docs/) — *Built-in telemetry and logging in ADK*

---

## Phase 13 — Claude / Anthropic Ecosystem

### Core Topics
- Claude models: Claude 3.7 Sonnet, 3.5 Haiku, Claude 3.7 Sonnet (Hybrid Reasoning), Claude Sonnet 4, Claude 4 Opus
- Extended context windows: 1M+ token context windows with high recall fidelity
- Anthropic Messages API & Streaming responses
- Anthropic Python and TypeScript SDKs
- Strict tool use & Structured JSON output schemas
- Native prompt caching breakpoints (`cache_control: {"type": "ephemeral"}`)
- Claude Desktop & Claude Code CLI agent integration
- Agent Skills & Model Context Protocol (MCP) implementations
- Context compaction, server-side auto-compaction, and multi-turn conversation management

### Curated Resources
- [Anthropic Claude Documentation](https://docs.anthropic.com/) — *Comprehensive guide to Claude models and APIs*
- [Claude API Reference](https://docs.anthropic.com/en/api/overview) — *Endpoint specs, parameters, and headers*
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python) — *Async client, streaming, and tool support*
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) — *Official recipes and code examples*
- [Claude Prompt Engineering & Templates](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables) — *System templates and variables*

---

## Phase 14 — Gemini / Google GenAI

### Core Topics
- Gemini models: Gemini 2.0 Flash, 2.5 Flash, 2.5 Pro (Thinking / Long Context)
- Gemini Thinking Mode: Explicit thinking budget control (`thinking_budget`) and chain-of-thought inspection
- Ultra-long context processing: 2M+ token active context windows with multimodal ingestion
- Google GenAI SDK: Python (`google-genai`) and C# / .NET (`Google.GenAI`)
- High-performance Function Calling & Native Structured Outputs
- Native Multimodal inputs: Text, Audio, Images, Video, PDF
- Streaming API contracts & Disconnect truncation
- Vertex AI Enterprise Grounding (Google Search & BigQuery)
- Explicit Context Caching APIs (TTL-based cache creation) & Storage-based caching
- Google Interactions API & Real-time Live API (WebSockets)

### Curated Resources
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs) — *Official developer reference*
- [Google GenAI Python SDK](https://github.com/googleapis/python-genai) — *Official next-generation Python SDK*
- [Google GenAI .NET SDK](https://github.com/googleapis/dotnet-genai) — *Official .NET SDK for C# enterprise services*
- [Gemini Context Caching Guide](https://ai.google.dev/gemini-api/docs/caching) — *Architecture and pricing of context caching*

---

## Phase 15 — Google ADK (Agent Development Kit)

### Core Topics
- Google ADK architecture: Code-first multi-agent orchestration
- Python ADK core primitives: Agents, Tools, Sessions, Runners
- Custom tool definitions & Pydantic argument schemas
- Seamless Model Context Protocol (MCP) tool integration
- Stateful session management & Memory persistence
- Agent callbacks, Event listeners, and Lifecycle hooks
- Multi-agent topologies: Sequential, Parallel, Hierarchical, Loop
- Automated agent evaluation using ADK evaluation harnesses
- `agents-cli`: Scaffolding, Evaluation, Deployment, and Publishing
- Packaging Agent Skills and custom domain extensions

### Curated Resources
- [Google ADK Documentation](https://google.github.io/adk-docs/) — *Official guides, codelabs, and tutorials*
- [ADK Community & Tutorials](https://google.github.io/adk-docs/community/) — *Community recipes and examples*
- [ADK Coding with AI & Agents CLI](https://google.github.io/adk-docs/tutorials/coding-with-ai/) — *Automating agent creation with CLI*
- [Agents CLI Quickstart Tutorial](https://google.github.io/agents-cli/guide/quickstart-tutorial/) — *Scaffold and deploy your first agent*
- [Google ADK GitHub Repository](https://github.com/google/adk-python) — *Official Python SDK source code*

---

## Phase 16 — Google Cloud Enterprise AI

### Core Topics
- Google Cloud Vertex AI Model Garden & Private Endpoints
- Vertex AI Agent Engine & Managed Agent Runtimes
- Serverless container hosting on Cloud Run (HTTP/2, SSE streaming)
- Enterprise Kubernetes orchestration on Google Kubernetes Engine (GKE) with GPU node pools
- IAM security, Workload Identity, and Service Account scoping
- Secret Manager integration for secure API key injection
- Storage & Ingestion: Cloud Storage (GCS) and BigQuery vector search
- Enterprise grounding pipelines & Data access governance
- Cloud Logging, Cloud Monitoring, and Cloud Trace OTel integration

### Curated Resources
- [Google Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs) — *Enterprise platform documentation*
- [Vertex AI Agent Engine Overview](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview) — *Managed agent hosting*
- [Google Cloud Architecture Center](https://cloud.google.com/architecture) — *Reference architectures for AI workloads*
- [BigQuery Vector Search](https://cloud.google.com/bigquery/docs/vector-search-intro) — *In-database vector indexing and search*

---

## Phase 17 — AI Application Architecture

### Core Topics
- Enterprise AI system decomposition: Client $\to$ Gateway $\to$ Agent $\to$ Tools $\to$ LLM
- Intelligent AI Gateways: Multi-provider routing, load balancing, rate limiting
- Model Gateways (LiteLLM, Portkey, Azure APIM)
- RAG service, Tool service, and Memory service separation
- Polyglot enterprise integration: Python agent orchestrator + C#/.NET 9 / Java backend
- Microsoft Semantic Kernel & Enterprise Dependency Injection
- Asynchronous event-driven agent architectures (Kafka, RabbitMQ, Redis Streams)
- Long-running background agents & Durable task polling
- Human-in-the-Loop (HITL) step-up approval workflows

### Curated Resources
- [Microsoft Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/) — *Enterprise AI integration for .NET, Python, and Java*
- [Microsoft AI Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/) — *Enterprise solution blueprints*
- [Google Cloud Architecture Center](https://cloud.google.com/architecture) — *Distributed AI system patterns*
- [Agentic Engineering Playbook](https://github.com/AnkitParekh007/Agentic-Engineering-Playbook) — *Production patterns for agentic systems*

---

## Phase 18 — AI Cost & Performance

### Core Topics
- Token optimization: Pruning, Compaction, Stop-word stripping
- Model tiering & Complexity-based routing (Flash/Haiku vs. Pro/Sonnet/o-Series)
- Exact SHA-256 caching + Semantic vector caching
- High-throughput Server-Sent Events (SSE) streaming with disconnect truncation
- Parallel tool invocation & Asynchronous execution
- Vector index tuning (HNSW `M` and `efSearch` parameters)
- Amortized cost per request, cost per task, and cost per successful outcome
- Real-time spend velocity monitors, anomaly alerts, and hard budget circuits

### Curated Resources
- [Anthropic Documentation — Cost & Latency](https://docs.anthropic.com/) — *Token efficiency best practices*
- [Gemini Context Caching Guide](https://ai.google.dev/gemini-api/docs/caching) — *Slashing input costs via memory caching*
- [Hamel Husain — Mastering LLMs](https://hamel.dev/blog/posts/course/) — *Latency and cost optimization*

---

## Phase 19 — AI CI/CD & SDLC

### Core Topics
- Prompt versioning & Machine-readable contracts (`AGENT.md`)
- Model checkpoint versioning & Regression tracking
- Automated evaluation gates in GitHub Actions and Azure DevOps
- Test-Driven Development (TDD) for autonomous coding agents
- AST-driven AI pull request review bots
- Canary deployments & Shadow traffic evaluation for model updates
- Instant rollback strategies on quality regression
- Automated feedback loops: Mining production failures into golden datasets

### Curated Resources
- [Google Agents CLI](https://google.github.io/agents-cli/) — *CI/CD evaluation and deployment commands*
- [Inspect AI Framework](https://inspect.aisi.org.uk/) — *Automated benchmark pipelines in CI*
- [OpenTelemetry Documentation](https://opentelemetry.io/) — *Continuous telemetry feedback*

---

## Phase 20 — AI Governance

### Core Topics
- Responsible AI frameworks & Ethical AI guidelines
- NIST AI Risk Management Framework (RMF 1.0) & EU AI Act compliance
- Model cards, System cards, and Transparency documentation
- Data governance: Classification, Retention, and Data residency
- Context and data lineage: Tracing source documents to generated tokens
- PII sanitization, masking, and Token vaulting
- Human oversight, Accountability boundaries, and Audit logging
- Vendor risk assessment & Foundation model provider SLA evaluation

### Curated Resources
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — *Federal standards for trustworthy AI*
- [Google Secure AI Framework (SAIF)](https://saif.google/) — *Practical security and risk management*
- [OWASP GenAI Security Project](https://genai.owasp.org/) — *Enterprise compliance and security guides*
- [Microsoft Responsible AI](https://www.microsoft.com/en-us/ai/responsible-ai) — *Principles, governance, and tools*

---

## Phase 21 — A2A & Agent Interoperability

### Core Topics
- Agent-to-Agent (A2A) communication protocols & A2A v1.0 Linux Foundation standardization
- Tri-protocol stack architecture: MCP (Agent-to-Tool), A2A (Agent-to-Agent federation), AG-UI (Agent-to-Human UI)
- AG-UI (Agentic GUI Protocol): Standardized agent-to-user interface protocol for streaming widgets and approvals
- Agent Communication Protocol (ACP) merger & specification unification
- Standardized message envelopes: Sender, Recipient, Authorization tokens, Payloads
- Dynamic agent capability discovery & Manifest publishing
- Agent task delegation, Contract negotiation, and Handoffs
- Multi-agent federation across heterogeneous frameworks (ADK, LangGraph, Semantic Kernel)
- Protocol comparison: MCP (Tool-to-Agent) vs. A2A (Agent-to-Agent) vs. AG-UI (Agent-to-User)
- Cross-tenant agent authorization & Least privilege delegation

### Curated Resources
- [A2A Protocol GitHub Repository](https://github.com/a2aproject/A2A) — *Open specification for Agent-to-Agent communication*
- [A2A Protocol Documentation & v1.0 Spec](https://a2a-protocol.org/) — *Linux Foundation architecture and message standard*
- [AG-UI Protocol Specification](https://ag-ui.org/) — *Standardized agent UI interaction layer and rich client components*
- [Agent Communication Protocol (ACP)](https://github.com/agent-communication-protocol/acp) — *Standardized agent messaging and communication protocol*
- [Google ADK A2A Documentation](https://google.github.io/adk-docs/) — *Multi-agent communication patterns*

---

## Phase 22 — Advanced Agent Engineering

### Core Topics
- Advanced planning: Tree of Thoughts (ToT), Monte Carlo Tree Search (MCTS)
- Verbal reinforcement learning & Episodic self-reflection (Reflexion)
- Critic and Reviewer loops for code generation and analysis
- Dynamic tool discovery via vector search over tool manifests
- Context routing & Dynamic tool filtering
- Durable agents: SQLite / Redis checkpointing, Saga pattern with compensation
- Long-running background agents & Distributed task dispatch
- Execution replay & Time-travel debugging
- Ephemeral execution sandboxing (gVisor runsc, WASM)

### Curated Resources
- [Google ADK Documentation](https://google.github.io/adk-docs/) — *Durable agents and advanced state*
- [Anthropic Research — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — *Orchestration principles*
- [LangGraph Documentation](https://docs.langchain.com/oss/python/langgraph/overview) — *State graphs and durable checkpointing*
- [LlamaIndex Workflows](https://docs.llamaindex.ai/) — *Event-driven async agent orchestration*

---

## Phase 23 — AI System Design / Interview Mastery

### Core Topics
- AI system requirement scoping (Functional, Latency, Throughput, Cost, Security)
- High-Level Design (HLD) & Low-Level Design (LLD) blueprints
- Foundation model selection decision trees
- End-to-end Enterprise Hybrid RAG architecture design
- High-throughput Resilient Multi-Provider AI Gateway design
- Autonomous Multi-Turn Coding & Refactoring Agent with MCP design
- Enterprise Multi-Agent Customer Operations Platform design
- Architectural tradeoff matrices: Serverless vs. Self-Hosted vLLM, RAG vs. Fine-Tuning
- Mental math & Hardware formulas: KV-cache VRAM, Latency breakdown, RRF

### Curated Resources
- [AI Engineering Roadmap 2026 — GitHub](https://github.com/mohsen-bahrami-mb/AI-Engineering-Roadmap/blob/main/README.md) — *System design references*
- [Agentic Engineering Playbook — GitHub](https://github.com/AnkitParekh007/Agentic-Engineering-Playbook) — *Production blueprints*
- [Google Cloud Architecture Center](https://cloud.google.com/architecture) — *Enterprise reference architectures*
- [Microsoft Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/) — *Baseline AI architectures*

---

## 🏛️ Core GitHub Repositories to Bookmark

Keep these permanently bookmarked for implementation patterns and current standards:

| Repository | Focus & Architecture Value |
|---|---|
| [**`pydantic/pydantic-ai`**](https://github.com/pydantic/pydantic-ai) | Type-safe Python agent framework with dependency injection and validated streaming |
| [**`openai/openai-agents-python`**](https://github.com/openai/openai-agents-python) | Official production multi-agent framework featuring dynamic handoffs and sandboxes |
| [**`anthropics/anthropic-cookbook`**](https://github.com/anthropics/anthropic-cookbook) | Definitive code patterns for Claude, prompt caching, tool use, and evals |
| [**`anthropics/courses`**](https://github.com/anthropics/courses) | Interactive developer courses for Anthropic Claude, MCP, and tool use |
| [**`google/adk-python`**](https://github.com/google/adk-python) | Google's code-first multi-agent orchestration framework |
| [**`googleapis/python-genai`**](https://github.com/googleapis/python-genai) | Official next-generation SDK for Google Gemini models |
| [**`modelcontextprotocol/servers`**](https://github.com/modelcontextprotocol/servers) | Reference MCP servers (SQLite, Filesystem, GitHub, PostgreSQL) |
| [**`microsoft/semantic-kernel`**](https://github.com/microsoft/semantic-kernel) | Enterprise AI orchestration for C#/.NET, Python, and Java |
| [**`langchain-ai/langgraph`**](https://github.com/langchain-ai/langgraph) | Cyclic state machine runtime for stateful agent workflows |
| [**`run-llama/llama_index`**](https://github.com/run-llama/llama_index) | Production RAG, hybrid search, and knowledge ingestion |
| [**`microsoft/graphrag`**](https://github.com/microsoft/graphrag) | Modular graph-based retrieval augmented generation |
| [**`UKGovernmentBEIS/inspect_ai`**](https://github.com/UKGovernmentBEIS/inspect_ai) | Framework for large language model evaluation and safety testing |
| [**`mohsen-bahrami-mb/AI-Engineering-Roadmap`**](https://github.com/mohsen-bahrami-mb/AI-Engineering-Roadmap) | Comprehensive AI engineering reference guide |
| [**`huggingface/smolagents`**](https://github.com/huggingface/smolagents) | Minimalist library for building code-centric agents with CodeAct |
| [**`letta-ai/letta`**](https://github.com/letta-ai/letta) | Stateful LLM agent operating system with tiered memory management |
| [**`browser-use/browser-use`**](https://github.com/browser-use/browser-use) | Open-source framework enabling AI agents to interact with web browsers |
| [**`sgl-project/sglang`**](https://github.com/sgl-project/sglang) | High-performance LLM and vision model serving framework with RadixAttention |

---

## ⚡ The 80/20 Priority Reading Order

If you want to maintain an optimal 80/20 learning velocity, bookmark and study these top 18 resources first:

```
01. Anthropic Documentation (Prompt design, tools, caching)
02. Google AI Developer Docs (Gemini APIs, multimodal, grounding)
03. MCP Official Specification & Guides (modelcontextprotocol.io)
04. Google ADK Documentation (Agents, tools, sessions, evals)
05. Anthropic Cookbook (Production patterns and recipes)
06. Google ADK GitHub Repository (adk-python)
07. Google GenAI Python & .NET SDKs
08. Hamel Husain — Mastering LLMs Course
09. Hamel Husain — AI Evals FAQ & LLM-as-a-Judge Guide
10. DeepLearning.AI Short Courses (Agents, MCP, RAG)
11. OWASP GenAI Security Project & LLM Top 10
12. OpenTelemetry GenAI Semantic Conventions
13. Microsoft Semantic Kernel (.NET & Python enterprise AI)
14. LlamaIndex Documentation (Advanced RAG & ingestion)
15. LangGraph Documentation (Cyclic agent state machines)
16. Google Cloud Architecture Center (Enterprise AI reference)
17. Azure Architecture Center (Baseline OpenAI & AI search architectures)
18. Agent Engineering Roadmap GitHub Repository
```

> [!NOTE]
> **Source of Truth Rule**: Vendor documentation (Google AI, Anthropic, Microsoft, MCP) should always be treated as the source of truth for rapidly changing foundation models, SDKs, and API protocols. Community repositories, blogs, and courses provide design patterns and intuition, but always verify current API syntax against official documentation.
