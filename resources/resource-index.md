# Master AI Engineering Resource Index

> **A verified, curated compendium of documentation, courses, technical blogs, architectural whitepapers, and production libraries for Senior Developers and AI Architects.**

---

## 📑 Index Overview

1. [Official Provider Documentation & SDKs](#1-official-provider-documentation-sdks)
2. [Model Context Protocol (MCP) Standards](#2-model-context-protocol-mcp-standards)
3. [Official Courses & Video Masterclasses](#3-official-courses-video-masterclasses)
4. [Practitioner Blogs & Architectural Essays](#4-practitioner-blogs-architectural-essays)
5. [Seminal Papers & Architecture Whitepapers](#5-seminal-papers-architecture-whitepapers)
6. [Production Frameworks, Libraries & Tools](#6-production-frameworks-libraries-tools)
7. [AI Security, Safety & Governance](#7-ai-security-safety-governance)
8. [External Roadmap References](#8-external-roadmap-references)

---

## 1. Official Provider Documentation & SDKs

### Google AI & Google Cloud
- **[Google AI for Developers](https://ai.google.dev/)**: Central hub for Gemini 2.0 & 2.5 models, multimodal capabilities, and APIs.
- **[Google GenAI Python SDK (`google-genai`)](https://github.com/googleapis/python-genai)**: The current official unified SDK for Gemini (replaces legacy `google-generativeai`).
- **[Gemini API Documentation](https://ai.google.dev/gemini-api/docs)**: Reference for multimodal streaming, structured outputs, code execution, and context caching.
- **[Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/)**: Code-first multi-agent orchestration framework with first-class MCP support and `agents-cli`.
- **[Google Vertex AI Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs)**: Enterprise grounding with Google Search and BigQuery, model garden, and dedicated agent endpoints.

### Anthropic & Claude
- **[Anthropic Claude Documentation](https://docs.anthropic.com/)**: Primary reference for Claude 3.7 Sonnet (hybrid reasoning & extended thinking) and Claude 3.5 Haiku.
- **[Anthropic Claude Code CLI](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)**: Official agentic coding assistant CLI with native MCP integration and terminal tool execution.
- **[Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)**: Authoritative guidance on XML boundaries, system instructions, and extended thinking budgets.
- **[Anthropic Tool Use & Function Calling Guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)**: Detailed specifications for JSON tool definition schemas, parallel tool calls, and error handling.
- **[Claude Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)**: Mechanics of 5-minute ephemeral prefix caching, achieving 90% cost and 80% latency reductions.
- **[Anthropic Interactive Courses (GitHub)](https://github.com/anthropics/courses)**: Interactive developer tutorials on Tool Use, Prompt Engineering, and Model Context Protocol.

### Microsoft & Azure AI
- **[Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-services/)**: Enterprise model catalog, fine-tuning, hosted agent services, and evaluation pipelines.
- **[Microsoft Semantic Kernel](https://learn.microsoft.com/semantic-kernel/)**: Enterprise AI orchestration SDK for C# / .NET 9, Python, and Java with dependency-injected plugins.
- **[Azure AI Search Documentation](https://learn.microsoft.com/azure/search/)**: Vector search, hybrid search (BM25 + Dense), semantic reranking, and chunking.
- **[Azure AI Agent Service](https://learn.microsoft.com/azure/ai-services/agents/)**: Cloud-native agent hosting with isolated execution sandboxes and Microsoft Entra ID governance.

### OpenAI Platform
- **[OpenAI Documentation](https://platform.openai.com/docs/)**: API reference for frontier reasoning models (o1, o3-mini) and multimodal models (GPT-4o, GPT-4o-mini).
- **[OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)**: Model-level tool-calling specifications, strict JSON mode, and multi-turn function execution loops.
- **[OpenAI Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs)**: Constrained grammar decoding and 100% strict JSON schema enforcement.
- **[OpenAI Reasoning Models Guide](https://platform.openai.com/docs/guides/reasoning)**: Test-time compute mechanics, reasoning tokens, and `reasoning_effort` tuning.

---

## 2. Model Context Protocol (MCP) Standards

- **[Model Context Protocol Official Site](https://modelcontextprotocol.io/)**: Protocol specifications, architecture overviews, and getting-started tutorials.
- **[MCP Specification (JSON-RPC 2.0)](https://spec.modelcontextprotocol.io/)**: Complete open standard governing Transports (`stdio`, `SSE`), Tools, Resources, Prompts, and Reverse Sampling.
- **[MCP GitHub Organization](https://github.com/modelcontextprotocol)**: Official repositories including TypeScript SDK, Python SDK, Kotlin SDK, and reference servers.
- **[FastMCP Python Library](https://github.com/jlowin/fastmcp)**: High-level, ergonomic framework for authoring production-ready MCP servers with Pydantic typing.
- **[Anthropic MCP Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/mcp)**: Guide to connecting Claude Desktop, Cursor, and Claude Code to external tools via MCP.

---

## 3. Official Courses & Video Masterclasses

### DeepLearning.AI Courses (Andrew Ng & Frontier Labs)
- **[MCP: Build Rich-Context AI Apps with Anthropic](https://www.deeplearning.ai/short-courses/mcp-build-rich-context-ai-apps-with-anthropic/)**: Hands-on course building and deploying MCP servers with Anthropic engineers.
- **[Reasoning with o1](https://www.deeplearning.ai/short-courses/reasoning-with-o1/)**: Taught in partnership with OpenAI; covers test-time compute, reasoning tokens, and task delegation.
- **[Claude Code: A Highly Agentic Coding Assistant](https://www.deeplearning.ai/short-courses/claude-code-a-highly-agentic-coding-assistant/)**: Official Anthropic course on terminal agent orchestration, repo mapping, and MCP tool execution.
- **[Building toward Computer Use with Anthropic](https://www.deeplearning.ai/short-courses/building-toward-computer-use-with-anthropic/)**: Multimodal UI navigation, coordinate grounding, and desktop agent execution.
- **[Agent Skills with Anthropic](https://www.deeplearning.ai/short-courses/agent-skills-with-anthropic/)**: Building modular, reusable agent instruction folders and subagent delegation workflows.
- **[Reinforcement Fine-Tuning LLMs with GRPO](https://www.deeplearning.ai/short-courses/reinforcement-fine-tuning-llms-with-grpo/)**: Group Relative Policy Optimization (the algorithm powering DeepSeek R1 and reasoning models).
- **[ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/)**: Foundational prompting tactics by Isa Fulford & Andrew Ng.

### Andrej Karpathy's Academy
- **[Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)**: The gold-standard video series building micrograd, makemore, WaveNet, and a full GPT from scratch.
- **[Intro to Large Language Models (YouTube)](https://www.youtube.com/watch?v=zjkBMFhNj_g)**: 1-hour executive and technical breakdown of pretraining, RLHF, and inference mechanics.
- **[Let's build GPT: from scratch, in code, spelled out (YouTube)](https://www.youtube.com/watch?v=kCc8FmEb1nY)**: Line-by-line implementation of nanoGPT.
- **[nanoGPT GitHub Repository](https://github.com/karpathy/nanoGPT)**: The simplest, fastest repository for training and finetuning medium-sized GPTs.
- **[llm.c GitHub Repository](https://github.com/karpathy/llm.c)**: LLM training in raw, dependency-free C/CUDA.

### Community & Open-Source Courses
- **[Hugging Face LLM Course](https://huggingface.co/learn/llm-course/)**: Practical deep dive into tokenizers, fine-tuning (PEFT/LoRA), and quantization.
- **[The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/)**: Intuitive visual breakdown of Scaled Dot-Product Attention.

---

## 4. Practitioner Blogs & Architectural Essays

- **[Hamel Husain's Applied AI Blog](https://hamel.dev/blog/)**:
  - *[Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)*: Why offline evals separate toy prototypes from durable software.
  - *[LLM Evals FAQ](https://hamel.dev/blog/posts/evals-faq/)*: Binary pass/fail criteria, synthetic dataset curation, and LLM-as-a-judge pitfalls.
  - *[How Do I Evaluate Agentic Workflows?](https://hamel.dev/blog/posts/evals-faq/how-do-i-evaluate-agentic-workflows.html)*: Trajectory evaluations, intermediate states, and tool-call assertions.
- **[Eugene Yan's Applied LLM Patterns](https://eugeneyan.com/)**:
  - *[Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/)*: Retrieval, routing, guardrails, and caching architectures.
- **[Lilian Weng's AI Safety & Systems Writing](https://lilianweng.github.io/)**:
  - *[LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)*: Planning (Subgoal decomposition), Memory, and Tool use taxonomy.
  - *[Adversarial Attacks on LLMs](https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/)*: Jailbreaking, prompt injections, and defensive boundaries.
- **[Chip Huyen's AI Engineering Architecture](https://huyenchip.com/)**:
  - *[Building LLM applications for production](https://huyenchip.com/2023/04/11/llm-engineering.html)*: Latency, cost, prompt engineering, and evaluation trade-offs.
- **[Simon Willison's Weblog](https://simonwillison.net/)**:
  - Comprehensive documentation and ongoing tracking of Prompt Injection vulnerabilities and AI security.

---

## 5. Seminal Papers & Architecture Whitepapers

| Paper / Document | Authors / Organization | Core Contribution |
|---|---|---|
| **[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** | Vaswani et al. (Google Brain / Research) | Introduced the Transformer architecture and Multi-Head Self-Attention. |
| **[Retrieval-Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401)** | Lewis et al. (Facebook AI Research) | Combined parametric neural network weights with non-parametric retrieval memory. |
| **[ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)** | Yao et al. (Princeton / Google Brain) | Interleaving thought generation (reasoning) with action execution (tools). |
| **[DeepSeek-R1 Technical Report](https://arxiv.org/abs/2501.12948)** | DeepSeek-AI | Pure reinforcement learning (GRPO) for reasoning capabilities without supervised fine-tuning. |
| **[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)** | Anthropic Applied AI Team | Pragmatic taxonomy of workflows (Chaining, Routing, Orchestrator) vs autonomous agents. |
| **[Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)** | Anthropic Applied AI Team | Prepending document context before chunking and embedding to cut retrieval failures. |
| **[CodeAct: Executable Code as Unified Action Space](https://arxiv.org/abs/2402.01030)** | Wang et al. (UIUC / Princeton) | Proved executable Python code outperforms JSON tool calls for multi-turn agent tasks. |
| **[SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770)** | Jimenez et al. (Princeton NLP) | The industry-standard benchmark evaluating autonomous code generation on real repositories. |

---

## 6. Production Frameworks, Libraries & Tools

### Orchestration & Agent Frameworks
- **[PydanticAI](https://github.com/pydantic/pydantic-ai)**: Type-safe, ergonomic Python agent framework built by the Pydantic team with dependency injection and validated streaming.
- **[OpenAI Agents SDK (`openai-agents`)](https://github.com/openai/openai-agents-python)**: Official production multi-agent framework featuring dynamic handoffs, guardrails, and code sandboxes.
- **[Microsoft Semantic Kernel (.NET / C# & Python)](https://github.com/microsoft/semantic-kernel)**: Enterprise integration framework built by Microsoft for connecting AI to existing codebases and DI containers.
- **[Google ADK (Agent Development Kit)](https://github.com/google/adk-python)**: Code-first multi-agent development framework with native MCP tool calling and `agents-cli`.
- **[LangGraph](https://github.com/langchain-ai/langgraph)**: Cyclical computational graph framework for durable, stateful agent loops with Postgres/Redis checkpointing and HITL.
- **[LiteLLM](https://github.com/BerriAI/litellm)**: High-throughput API gateway calling 100+ LLMs via unified OpenAI schema with fallback routing and semantic caching.

### High-Throughput Serving & Optimization
- **[vLLM](https://github.com/vllm-project/vllm)**: High-throughput, low-latency LLM serving engine featuring PagedAttention and continuous batching.
- **[SGLang](https://github.com/sgl-project/sglang)**: High-performance serving engine featuring RadixAttention trie KV-cache reuse for multi-turn agents.

### Agentic Coding & Developer Platforms
- **[Claude Code CLI](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)**: Terminal-native agentic coding tool with MCP support, subagent delegation, and repo mapping.
- **[Aider](https://github.com/Aider-AI/aider)**: Terminal pair programming agent using Tree-sitter repo maps and Git auto-commits.
- **[OpenHands](https://github.com/All-Hands-AI/OpenHands)**: Open-source autonomous software development platform powered by CodeAct loops.

### Evaluation & Observability
- **[Langfuse](https://github.com/langfuse/langfuse)**: Open source LLM engineering platform for tracing, evals, prompt management, and metrics.
- **[Arize Phoenix](https://github.com/Arize-ai/phoenix)**: AI observability, OpenTelemetry tracing, evaluation, and vector retrieval visualization.
- **[DeepEval](https://github.com/confident-ai/deepeval)**: Production unit-testing framework for LLMs with Pytest integration and synthetic dataset generation.
- **[Promptfoo](https://github.com/promptfoo/promptfoo)**: CLI and CI/CD testing tool for prompt regression tests, red-teaming, and model comparison.
- **[Ragas](https://github.com/explodinggradients/ragas)**: Automated evaluation framework for RAG systems (Faithfulness, Answer Relevancy, Context Recall).

---

## 7. AI Security, Safety & Governance

### Internal Repository Deep-Dive Guides
- **[AI Governance, Compliance & The EU AI Act Guide](ai-governance-and-compliance-guide.md)**: Field guide on EU AI Act enforcement, GPAI compliance, risk classification, and GDPR crypto-shredding.
- **[The Top 15 Beginner Mistakes in AI Engineering](beginner-mistakes-cheatsheet.md)**: Battle-tested prevention guide for runaway agent loops, prefix taint, SQL prompt injections, and vibe-check releases.
- **[Topics & Resource Map](topics-and-resource-map.md)**: Comprehensive phase-by-phase mapping of topics from Foundations (00) to Agentic SDLC (08).

### Industry Standards & Guardrail Frameworks
- **[OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)**: The industry standard catalog of vulnerabilities (Prompt Injection, Insecure Output Handling, Excessive Agency).
- **[NIST AI Risk Management Framework (AI RMF)](https://www.nist.gov/itl/ai-risk-management-framework)**: Federal standard for governance, mapping, measuring, and managing AI system risks.
- **[NeMo Guardrails (NVIDIA)](https://github.com/NVIDIA/NeMo-Guardrails)**: Open-source programmable safety rails and semantic boundaries around LLMs.
- **[Llama Guard 3 (Meta)](https://github.com/meta-llama/llama-guard)**: Fine-tuned safety classifier for input/output moderation across safety categories.

---

## 8. External Roadmap References

- **[roadmap.sh AI Engineer](https://roadmap.sh/ai-engineer)**: Developer community guide covering foundational computer science, machine learning, and data progressions.
- **[AI Engineering Roadmap by Mohsen Bahrami](https://github.com/mohsen-bahrami-mb/AI-Engineering-Roadmap)**: Clean, structured curriculum index prioritizing direct official documentation and open tools.

