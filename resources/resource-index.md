# Master AI Engineering Resource Index

> **A verified, curated compendium of documentation, courses, technical blogs, architectural whitepapers, and production libraries for Senior Developers and AI Architects.**

---

## 📑 Index Overview

1. [Official Provider Documentation & SDKs](#1-official-provider-documentation--sdks)
2. [Model Context Protocol (MCP) Standards](#2-model-context-protocol-mcp-standards)
3. [Official Courses & Video Masterclasses](#3-official-courses--video-masterclasses)
4. [Practitioner Blogs & Architectural Essays](#4-practitioner-blogs--architectural-essays)
5. [Seminal Papers & Architecture Whitepapers](#5-seminal-papers--architecture-whitepapers)
6. [Production Frameworks, Libraries & Tools](#6-production-frameworks-libraries--tools)
7. [AI Security, Safety & Governance](#7-ai-security-safety--governance)
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
- **[Building Effective Agents (Anthropic Engineering)](https://www.anthropic.com/engineering/building-effective-agents)**: Seminal architectural guide on workflow patterns (Chaining, Routing, Parallelization, Orchestrator-Workers, Evaluator-Optimizer).
- **[Claude Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)**: Mechanics of 5-minute ephemeral prefix caching, achieving 90% cost and 80% latency reductions.
- **[Anthropic Interactive Courses (GitHub)](https://github.com/anthropics/courses)**: Interactive developer tutorials on Tool Use, Prompt Engineering, and Model Context Protocol.

### Microsoft & Azure AI
- **[Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-services/)**: Enterprise model catalog, fine-tuning, hosted agent services, and evaluation pipelines.
- **[Microsoft Semantic Kernel](https://learn.microsoft.com/semantic-kernel/)**: Enterprise AI orchestration SDK for C# / .NET 9, Python, and Java with dependency-injected plugins.
- **[Azure AI Search Documentation](https://learn.microsoft.com/azure/search/)**: Vector search, hybrid search (BM25 + Dense), semantic reranking, and chunking.
- **[Azure AI Agent Service](https://learn.microsoft.com/azure/ai-services/agents/)**: Cloud-native agent hosting with isolated execution sandboxes and Microsoft Entra ID governance.

### OpenAI Platform
- **[OpenAI Documentation](https://platform.openai.com/docs/)**: API reference for frontier reasoning models (o1, o3-mini) and multimodal models (GPT-4.5, o3-mini).
- **[OpenAI Agents SDK (`openai-agents`)](https://github.com/openai/openai-agents-python)**: Official production framework (successor to Swarm) featuring multi-agent handoffs, guardrails, and tracing.
- **[OpenAI Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs)**: Constrained grammar decoding and 100% strict JSON schema enforcement.
- **[OpenAI Reasoning Models Guide](https://platform.openai.com/docs/guides/reasoning)**: Test-time compute mechanics, reasoning tokens, and `reasoning_effort` tuning.

---

## 2. Model Context Protocol (MCP) & Agent-to-Agent (A2A) Standards

- **[Model Context Protocol Official Site](https://modelcontextprotocol.io/)**: Protocol specifications, architecture overviews, and getting-started tutorials.
- **[MCP Specification (JSON-RPC 2.0)](https://spec.modelcontextprotocol.io/)**: Complete open standard governing Transports (`stdio`, `Streamable HTTP`), Tools, Resources, Prompts, and Tasks Extension.
- **[Google Agent-to-Agent (A2A) Protocol Specification](https://a2a-protocol.org/)**: The open standard for cross-vendor multi-agent interoperability, Agent Capability Cards (`agent.json`), and task lifecycles under the **Agentic AI Foundation**.
- **[FastMCP Python Library](https://github.com/jlowin/fastmcp)**: High-level, ergonomic framework for authoring production-ready MCP servers with Pydantic typing.
- **[SWE-bench Harness](https://github.com/swe-bench/SWE-bench)**: The gold-standard benchmark evaluation harness providing decoupled 3-tier Docker environments for evaluating autonomous coding agents.
- **[Anthropic Claude Cookbooks](https://github.com/anthropics/claude-cookbooks)**: Production recipes for orchestrator-worker workflows, prompt caching, tool use, and offline evals.

---

## 3. Official Courses & Video Masterclasses

### DeepLearning.AI Courses (Andrew Ng & Frontier Labs)
- **[AI Agents in LangGraph](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/)** (Harrison Chase & Rotem Weiss): Controllable cyclic graphs, state persistence, agentic search, and human-in-the-loop workflows.
- **[Long-Term Agentic Memory With LangGraph](https://www.deeplearning.ai/short-courses/)**: Implementing durable procedural, episodic, and semantic memory using LangGraph and LangMem.
- **[Multi AI Agent Systems with crewAI](https://www.deeplearning.ai/short-courses/multi-ai-agent-systems-with-crewai/)** (João Moura): Role-playing agents, inter-agent delegation, and structured crew workflows.
- **[Evaluating and Debugging Generative AI](https://www.deeplearning.ai/short-courses/evaluating-debugging-generative-ai/)**: Tracing agent execution, MLOps logging, and systematic failure-mode debugging.
- **[MCP: Build Rich-Context AI Apps with Anthropic](https://www.deeplearning.ai/short-courses/mcp-build-rich-context-ai-apps-with-anthropic/)**: Hands-on course building and deploying MCP servers with Anthropic engineers.
- **[Reasoning with o1](https://www.deeplearning.ai/short-courses/reasoning-with-o1/)**: Taught in partnership with OpenAI; covers test-time compute, reasoning tokens, and task delegation.
- **[Claude Code: A Highly Agentic Coding Assistant](https://www.deeplearning.ai/short-courses/claude-code-a-highly-agentic-coding-assistant/)**: Official Anthropic course on terminal agent orchestration, repo mapping, and MCP tool execution.
- **[Reinforcement Fine-Tuning LLMs with GRPO](https://www.deeplearning.ai/short-courses/reinforcement-fine-tuning-llms-with-grpo/)**: Group Relative Policy Optimization (the algorithm powering DeepSeek R1 and reasoning models).

### Specialized Industry Cohort Courses
- **[AI Evals For Engineers & PMs (Maven)](https://maven.com/parlance-labs/evals)** (Hamel Husain & Shreya Shankar): The industry gold-standard cohort course on Analyze-Measure-Improve evaluation loops, error analysis, and trajectory evaluations.

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
- **[Chip Huyen's AI Engineering Writings](https://huyenchip.com/)**:
  - *AI Engineering: Building Applications with Foundation Models* (O'Reilly, 2025).
  - *[Agents (Jan 2025)](https://huyenchip.com/2025/01/07/agents.html)*: Cognitive architectures, tool interfaces, and autonomous agent loops.
  - *[Common Pitfalls When Building Generative AI Applications (Jan 2025)](https://huyenchip.com/2025/01/16/common-pitfalls.html)*: Architectural anti-patterns in production.
- **[Eugene Yan's Applied LLM Patterns](https://eugeneyan.com/)**:
  - *[Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/)*: Retrieval, routing, guardrails, and caching architectures.
  - *[AlignEval & Cybersecurity Evaluation Harnesses](https://eugeneyan.com/)*: Continuous evaluation and benchmark harness design.
- **[Lilian Weng's AI Safety & Systems Writing](https://lilianweng.github.io/)**:
  - *[LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)*: Planning (Subgoal decomposition), Memory, and Tool use taxonomy.
  - *[Adversarial Attacks on LLMs](https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/)*: Jailbreaking, prompt injections, and defensive boundaries.
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

---

## 6. Production Frameworks, Libraries & Tools

### Orchestration & Agent Frameworks
- **[PydanticAI](https://github.com/pydantic/pydantic-ai)**: Type-safe, ergonomic Python agent framework built by the Pydantic team with dependency injection and validated streaming.
- **[OpenAI Agents SDK (`openai-agents`)](https://github.com/openai/openai-agents-python)**: Official production multi-agent framework featuring dynamic handoffs, guardrails, and code sandboxes.
- **[Microsoft Semantic Kernel (.NET / C# & Python)](https://github.com/microsoft/semantic-kernel)**: Enterprise integration framework built by Microsoft for connecting AI to existing codebases and DI containers.
- **[Google ADK (Agent Development Kit)](https://github.com/google/adk-python)**: Code-first multi-agent development framework with native MCP tool calling and `agents-cli`.
- **[LangGraph](https://github.com/langchain-ai/langgraph)**: Cyclical computational graph framework for durable, stateful agent loops with Postgres/Redis checkpointing and HITL.
- **[LiteLLM](https://github.com/BerriAI/litellm)**: High-throughput API gateway calling 100+ LLMs via unified OpenAI schema with fallback routing and semantic caching.

### Evaluation & Observability
- **[Langfuse](https://github.com/langfuse/langfuse)**: Open source LLM engineering platform for tracing, evals, prompt management, and metrics.
- **[Arize Phoenix](https://github.com/Arize-ai/phoenix)**: AI observability, OpenTelemetry tracing, evaluation, and vector retrieval visualization.
- **[Ragas](https://github.com/explodinggradients/ragas)**: Automated evaluation framework for RAG systems (Faithfulness, Answer Relevancy, Context Precision).
- **[Promptfoo](https://github.com/promptfoo/promptfoo)**: CLI and CI/CD testing tool for prompt regression tests, red-teaming, and model comparison.

---

## 7. AI Security, Safety & Governance

- **[OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)**: The industry standard catalog of vulnerabilities (Prompt Injection, Insecure Output Handling, Excessive Agency).
- **[NIST AI Risk Management Framework (AI RMF)](https://www.nist.gov/itl/ai-risk-management-framework)**: Federal standard for governance, mapping, measuring, and managing AI system risks.
- **[NeMo Guardrails (NVIDIA)](https://github.com/NVIDIA/NeMo-Guardrails)**: Open-source programmable safety rails and semantic boundaries around LLMs.
- **[Llama Guard 3 (Meta)](https://github.com/meta-llama/llama-guard)**: Fine-tuned safety classifier for input/output moderation across safety categories.

---

## 8. External Roadmap References

- **[roadmap.sh AI Engineer](https://roadmap.sh/ai-engineer)**: Developer community guide covering foundational computer science, machine learning, and data progressions.
- **[AI Engineering Roadmap by Mohsen Bahrami](https://github.com/mohsen-bahrami-mb/AI-Engineering-Roadmap)**: Clean, structured curriculum index prioritizing direct official documentation and open tools.
