# Master AI Engineering Resource Index

> **A verified, curated compendium of documentation, courses, technical blogs, architectural whitepapers, and production libraries for Senior Developers and AI Architects.**

---

## 📑 Index Overview

1. [Official Provider Documentation & SDKs](#1-official-provider-documentation--sdks)
2. [Model Context Protocol (MCP) Standards](#2-model-context-protocol-mcp-standards)
3. [Foundational Courses & Video Masterclasses](#3-foundational-courses--video-masterclasses)
4. [Practitioner Blogs & Expert Newsletters](#4-practitioner-blogs--expert-newsletters)
5. [Seminal Papers & Architecture Whitepapers](#5-seminal-papers--architecture-whitepapers)
6. [Production Frameworks, Libraries & Tools](#6-production-frameworks-libraries--tools)
7. [AI Security, Safety & Governance](#7-ai-security-safety--governance)
8. [External Roadmap References](#8-external-roadmap-references)

---

## 1. Official Provider Documentation & SDKs

### Google AI & Google Cloud
- **[Google AI for Developers](https://ai.google.dev/)**: Central hub for Gemini APIs, models, and quickstarts.
- **[Gemini API Documentation](https://ai.google.dev/gemini-api/docs)**: Reference for multimodal prompts, structured outputs, function calling, and system instructions.
- **[Gemini Context Caching Guide](https://ai.google.dev/gemini-api/docs/caching)**: Architecture and billing mechanics of long-context prefix caching.
- **[Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/)**: Official documentation for Google's code-first multi-agent orchestration framework.
- **[Google ADK GitHub Repository](https://github.com/google/adk-python)**: Python, TypeScript, Go, and Kotlin SDKs for ADK.
- **[Google Vertex AI Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs)**: Enterprise grounding with Google Search and BigQuery, model garden, and endpoints.

### Anthropic & Claude
- **[Anthropic Claude Documentation](https://docs.anthropic.com/)**: Primary reference for Claude 3.5 & 3.7 models, prompt design, and APIs.
- **[Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)**: Authoritative guidance on XML tagging, prompt formatting, and few-shot reasoning.
- **[Building Effective Agents (Anthropic Blog)](https://www.anthropic.com/engineering/building-effective-agents)**: The industry-defining architectural paper on workflows vs autonomous agents.
- **[Claude Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)**: Mechanics of prefix caching for Claude, minimizing latency and cost.
- **[Claude Tool Use & Function Calling](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview)**: Schema definitions, error recovery, and tool selection.
- **[Claude Academy](https://academy.claude.com/)**: Free structured courses on the 4D AI Fluency Framework (Delegation, Description, Discernment, Diligence).

### Microsoft & Azure AI
- **[Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-services/)**: Enterprise catalog, fine-tuning, hosted agent services, and evaluation pipelines.
- **[Microsoft Semantic Kernel](https://learn.microsoft.com/semantic-kernel/)**: Enterprise AI orchestration SDK for C# / .NET, Python, and Java.
- **[Azure AI Search Documentation](https://learn.microsoft.com/azure/search/)**: Vector search, hybrid search (BM25 + Dense), semantic reranking, and chunking.
- **[Microsoft Foundry Agent Service](https://learn.microsoft.com/azure/ai-services/agents/)**: Cloud-native agent hosting, tool execution, and state persistence.

### OpenAI Platform
- **[OpenAI Documentation](https://platform.openai.com/docs/)**: API reference for GPT-4o, o1, and o3 reasoning models.
- **[OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)**: Systematic tactics for prompting, reasoning, and context optimization.
- **[OpenAI Function Calling & Structured Outputs](https://platform.openai.com/docs/guides/function-calling)**: Strict mode schema adherence via constrained sampling.

---

## 2. Model Context Protocol (MCP) Standards

- **[Model Context Protocol Official Site](https://modelcontextprotocol.io/)**: Protocol specifications, getting started guides, and architecture overviews.
- **[MCP GitHub Organization](https://github.com/modelcontextprotocol)**: Official repositories including `python-sdk`, `typescript-sdk`, and core specifications.
- **[MCP Specification (JSON-RPC 2.0)](https://spec.modelcontextprotocol.io/)**: The complete RFC-level standard for Transports, Tools, Resources, Prompts, and Sampling.
- **[DeepLearning.AI — Building Rich Context AI Apps with MCP](https://www.deeplearning.ai/courses/mcp-build-rich-context-ai-apps-with-anthropic/)**: Free hands-on course taught with Anthropic engineers.
- **[Anthropic MCP Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/mcp)**: How Claude Desktop and Claude Code interface with external MCP servers.

---

## 3. Foundational Courses & Video Masterclasses

### Andrej Karpathy's Academy
- **[Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)**: The gold-standard video series building micrograd, makemore, WaveNet, and a full GPT from scratch.
- **[Intro to Large Language Models (YouTube)](https://www.youtube.com/watch?v=zjkBMFhNj_g)**: 1-hour executive & technical overview of pretraining, fine-tuning, RLHF, and LLM psychology.
- **[Let's build GPT: from scratch, in code, spelled out (YouTube)](https://www.youtube.com/watch?v=kCc8FmEb1nY)**: Line-by-line implementation of nanoGPT.
- **[nanoGPT GitHub Repository](https://github.com/karpathy/nanoGPT)**: The simplest, fastest repository for training/finetuning medium-sized GPTs.
- **[llm.c GitHub Repository](https://github.com/karpathy/llm.c)**: LLM training in simple, raw C/CUDA without 245MB of PyTorch dependencies.

### DeepLearning.AI (Andrew Ng & Partners)
- **[ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/)**: Core mental models of prompting by Isa Fulford & Andrew Ng.
- **[Building Systems with the ChatGPT API](https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/)**: Chaining prompts, moderation, and evaluation workflows.
- **[Functions, Tools and Agents with LangChain](https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/)**: Primitives of tool calling and agent loops.
- **[Multi AI Agent Systems with crewAI](https://www.deeplearning.ai/short-courses/multi-ai-agent-systems-with-crewai/)**: Role-playing autonomous agent collaboration patterns.

### Hugging Face & Community Courses
- **[Hugging Face LLM Course](https://huggingface.co/learn/llm-course/)**: Practical deep dive into tokenizers, datasets, fine-tuning (PEFT/LoRA), and quantization.
- **[The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/)**: The most intuitive visual guide to Attention and Transformer internals.

---

## 4. Practitioner Blogs & Expert Newsletters

- **[Hamel Husain's Engineering Blog](https://hamel.dev/blog/)**:
  - *[Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)*: Why offline evals are the difference between toy demos and profitable software.
  - *[LLM Evals FAQ](https://hamel.dev/blog/posts/evals-faq/)*: Binary pass/fail criteria, synthetic dataset generation, and LLM-as-a-judge pitfalls.
  - *[How Do I Evaluate Agentic Workflows?](https://hamel.dev/blog/posts/evals-faq/how-do-i-evaluate-agentic-workflows.html)*: Trajectory, intermediate states, and tool-call unit testing.
- **[Eugene Yan's Applied LLM Patterns](https://eugeneyan.com/)**:
  - *[Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/)*: Retrieval, routing, guardrails, and caching architectures.
- **[Lilian Weng (Head of Safety Systems at OpenAI)](https://lilianweng.github.io/)**:
  - *[LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)*: Planning (Subgoal decomposition), Memory, and Tool use taxonomy.
  - *[Adversarial Attacks on LLMs](https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/)*: Jailbreaking, backdoor attacks, and robustness.
- **[Chip Huyen's AI Architecture Writing](https://huyenchip.com/)**:
  - *[Building LLM applications for production](https://huyenchip.com/2023/04/11/llm-engineering.html)*: Latency, cost, prompt engineering, and evaluation trade-offs.
- **[Simon Willison's Weblog](https://simonwillison.net/)**:
  - Creator of Datasette and pioneer in cataloging and analyzing *Prompt Injection* attacks.

---

## 5. Seminal Papers & Architecture Whitepapers

| Paper / Document | Authors / Organization | Core Contribution |
|---|---|---|
| **[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** | Vaswani et al. (Google Brain / Research) | Introduced the Transformer architecture and Multi-Head Self-Attention. |
| **[Retrieval-Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401)** | Lewis et al. (Facebook AI Research) | Combined parametric neural networks with non-parametric retrieval memory. |
| **[ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)** | Yao et al. (Princeton / Google Brain) | Interleaving thought generation (reasoning) with action execution (tools). |
| **[Self-RAG: Learning to Retrieve, Generate, and Critique](https://arxiv.org/abs/2310.11511)** | Asai et al. | Adaptive retrieval on-demand with self-reflection tokens. |
| **[Corrective RAG (CRAG)](https://arxiv.org/abs/2401.15884)** | Yan et al. | Evaluates document retrieval quality and triggers web fallbacks when retrieval is poor. |
| **[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)** | Anthropic Applied AI Team | Pragmatic taxonomy of workflows (Chaining, Routing, Orchestrator) vs open agents. |

---

## 6. Production Frameworks, Libraries & Tools

### Orchestration & Agent Frameworks
- **[Semantic Kernel (.NET / C# & Python)](https://github.com/microsoft/semantic-kernel)**: Enterprise integration framework built by Microsoft for connecting AI to existing code.
- **[Google ADK (Agent Development Kit)](https://github.com/google/adk-python)**: Code-first multi-agent development framework.
- **[LangGraph](https://github.com/langchain-ai/langgraph)**: Graph-based state machine framework for durable, cyclical agent workflows with human-in-the-loop.
- **[PydanticAI](https://github.com/pydantic/pydantic-ai)**: Production agent framework built on top of Pydantic for type-safe, validated agent responses.
- **[LiteLLM](https://github.com/BerriAI/litellm)**: Universal I/O proxy calling 100+ LLMs in standard OpenAI schema with load balancing and fallbacks.

### Evaluation & Observability
- **[Langfuse](https://github.com/langfuse/langfuse)**: Open source LLM engineering platform for tracing, evals, prompt management, and metrics.
- **[Arize Phoenix](https://github.com/Arize-ai/phoenix)**: AI observability, OpenTelemetry tracing, evaluation, and vector retrieval visualization.
- **[Ragas](https://github.com/explodinggradients/ragas)**: Automated evaluation framework for RAG systems (Faithfulness, Answer Relevancy, Context Precision).
- **[Promptfoo](https://github.com/promptfoo/promptfoo)**: CLI and CI/CD testing tool for prompt engineering, security testing, and model comparison.

---

## 7. AI Security, Safety & Governance

- **[OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)**: The industry standard catalog of vulnerabilities (Prompt Injection, Insecure Output Handling, Excessive Agency).
- **[NIST AI Risk Management Framework (AI RMF)](https://www.nist.gov/itl/ai-risk-management-framework)**: Federal standard for governance, mapping, measuring, and managing AI system risks.
- **[NeMo Guardrails (NVIDIA)](https://github.com/NVIDIA/NeMo-Guardrails)**: Open-source toolkit for adding programmable safety rails and semantic boundaries around LLMs.
- **[Llama Guard (Meta)](https://github.com/meta-llama/llama-guard)**: Fine-tuned safety classifier for input/output moderation across safety categories.

---

## 8. External Roadmap References

General reference guides across the broader developer ecosystem:
- **[roadmap.sh AI Engineer](https://roadmap.sh/ai-engineer)**: Developer community guide covering foundational computer science, machine learning, and data progressions.
- **[Prince Singh's Ultimate AI Engineer Roadmap (2026)](https://github.com/PrinceSinghhub/Ultimate-AI-Engineer-Roadmap-2026)**: Open-source repository covering academic ML and deep learning curricula.
- **[The Complete AI Engineering Roadmap (2026) by Tech Chick](https://medium.com/)**: Practitioner article outlining Python scripting and prototype construction workflows.

