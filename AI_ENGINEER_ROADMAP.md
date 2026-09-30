# AI Engineer Roadmap

> A simple, practical roadmap for software engineers transitioning to AI engineering. Every category, topic, and subtopic is explained in simple, everyday terms (ELI10) without confusing abbreviations.

---

## Table of Contents

- [1. AI & LLM Fundamentals](#1-ai--llm-fundamentals)
  - [1.1 Role Foundations: AI Engineer vs. ML Engineer](#11-role-foundations-ai-engineer-vs-ml-engineer)
  - [1.2 What Is a Large Language Model (LLM)](#12-what-is-a-large-language-model-llm)
  - [1.3 Generation Mechanics & Sampling Parameters](#13-generation-mechanics--sampling-parameters)
  - [1.4 Model Families, APIs & Open-Source Options](#14-model-families-apis--open-source-options)
- [2. Prompt & Context Engineering](#2-prompt--context-engineering)
  - [2.1 Prompt Engineering Techniques](#21-prompt-engineering-techniques)
  - [2.2 Context Engineering & Compaction](#22-context-engineering--compaction)
  - [2.3 Structured Outputs & Schema Contracts](#23-structured-outputs--schema-contracts)
- [3. Embeddings & Vector Search](#3-embeddings--vector-search)
  - [3.1 Embeddings & Semantic Search](#31-embeddings--semantic-search)
  - [3.2 Vector Databases & Indexing](#32-vector-databases--indexing)
  - [3.3 Hybrid Search & Ranking](#33-hybrid-search--ranking)
- [4. Retrieval-Augmented Generation (RAG)](#4-retrieval-augmented-generation-rag)
  - [4.1 Basic RAG Pipeline](#41-basic-rag-pipeline)
  - [4.2 Document Ingestion & Chunking](#42-document-ingestion--chunking)
  - [4.3 Advanced RAG & Retrieval Quality](#43-advanced-rag--retrieval-quality)
- [5. AI Agents & Stateful Orchestration](#5-ai-agents--stateful-orchestration)
  - [5.1 Agent Fundamentals & the ReAct Loop](#51-agent-fundamentals--the-react-loop)
  - [5.2 Agent Tools & Function Calling](#52-agent-tools--function-calling)
  - [5.3 State, Memory & Checkpoints](#53-state-memory--checkpoints)
  - [5.4 Stateful Workflows & State Machines](#54-stateful-workflows--state-machines)
  - [5.5 Model Context Protocol (MCP)](#55-model-context-protocol-mcp)
  - [5.6 Multi-Agent Coordination & Agent-to-Agent (A2A)](#56-multi-agent-coordination--agent-to-agent-a2a)
- [6. Reliability, Safety & Guardrails](#6-reliability-safety--guardrails)
  - [6.1 Failure Engineering & Fallbacks](#61-failure-engineering--fallbacks)
  - [6.2 Bounded Execution & Loop Prevention](#62-bounded-execution--loop-prevention)
  - [6.3 Human-in-the-Loop (HITL) & Approval Gates](#63-human-in-the-loop-hitl--approval-gates)
  - [6.4 Guardrails & Prompt Injection Defense](#64-guardrails--prompt-injection-defense)
- [7. Evaluation & Observability](#7-evaluation--observability)
  - [7.1 Deterministic & Metric-Based Evals](#71-deterministic--metric-based-evals)
  - [7.2 LLM-as-a-Judge & Model-Based Evals](#72-llm-as-a-judge--model-based-evals)
  - [7.3 Agent Trajectory & Behavior Evaluation](#73-agent-trajectory--behavior-evaluation)
  - [7.4 Observability, Tracing & Golden Signals](#74-observability-tracing--golden-signals)
- [8. Production, Inference & Systems Optimization](#8-production-inference--optimization)
  - [8.1 Latency, Cost & Caching Optimization](#81-latency-cost--caching-optimization)
  - [8.2 Serving, KV Cache & Continuous Batching](#82-serving-kv-cache--continuous-batching)
  - [8.3 Multi-Modal AI Systems](#83-multi-modal-ai-systems)
  - [8.4 Enterprise Capstone: Production Agent Architecture](#84-enterprise-capstone-production-agent-architecture)

---

## 1. **AI & LLM Fundamentals**
### Learn how smart computer brains read your text and guess the next words.

### 1.1 **Role Foundations: AI Engineer vs. ML Engineer**
> An AI Engineer uses pre-trained models and tools to build practical apps, while an ML Engineer trains models and manages math algorithms from scratch.

- **1.1.1 AI Engineer Focus** -> Connecting existing Large Language Models to databases, tools, APIs, and user interfaces to solve business problems.
- **1.1.2 Machine Learning (ML) Engineer Focus** -> Training, fine-tuning, and mathematically tuning raw neural network architectures on massive GPU clusters.
- **1.1.3 Artificial General Intelligence (AGI) vs Narrow AI** -> Narrow AI does specific tasks like writing text or recognizing images; AGI refers to a theoretical future system that can do any intellectual task as well as a human.

### 1.2 **What Is a Large Language Model (LLM)**
> An LLM is a giant computer program trained on billions of books and websites to guess the next word in a sentence.

- **1.2.1 Tokens** -> Word puzzle pieces (around 3 to 4 letters) that the AI reads and writes instead of entire words.
- **1.2.2 Context Window** -> The short-term memory limit showing how much text the AI can see at one time before forgetting earlier lines.
- **1.2.3 Hallucinations** -> Confident false answers made up by the AI because it only knows how to sound realistic, not check real facts.
- **1.2.4 In-Context Learning** -> How an LLM temporarily picks up new skills or styles just from reading your prompt without retraining its brain.

### 1.3 **Generation Mechanics & Sampling Parameters**
> Models write one tiny piece at a time by constantly recalculating probabilities controlled by specific dials.

- **1.3.1 Autoregressive Generation** -> Writing one word chunk at a time where each new word depends on everything written previously.
- **1.3.2 Temperature** -> A creativity dial where zero gives the most predictable, boring answer and higher numbers make the AI more adventurous.
- **1.3.3 Top-P (Nucleus Sampling)** -> A filter that tells the AI to only pick from words that make up the top percentage of total probability, preventing gibberish.
- **1.3.4 Top-K Sampling** -> A filter that forces the AI to consider only the top K most likely next words, cutting out weird wild guesses.
- **1.3.5 Stop Sequences** -> Special marker phrases or symbols that tell the AI to immediately stop writing more text.

### 1.4 **Model Families, APIs & Open-Source Options**
> You usually do not train models from scratch; instead, you call existing models over the internet through APIs or run open models on your own servers.

- **1.4.1 Commercial Cloud APIs (Application Programming Interfaces)** -> Ready-to-use cloud models like OpenAI GPT-4o, Anthropic Claude, and Google Gemini paid per token.
- **1.4.2 Open-Weight Models & Local Hosting** -> Downloadable models like Meta Llama and Mistral that you can run on your own computers using tools like Ollama for total privacy.
- **1.4.3 Small vs. Large Models (Model Tiers)** -> Small models are cheap and lightning fast for easy chores, while large models are smarter but slower and pricier.

---

## 2. **Prompt & Context Engineering**
### Learn how to talk to models clearly so they give you structured, dependable answers.

### 2.1 **Prompt Engineering Techniques**
> Giving the AI crystal-clear instructions so it does what you want instead of making random guesses.

- **2.1.1 System Prompts** -> Secret setup instructions that define the AI's identity, rules, and boundaries before any human speaks.
- **2.1.2 Zero-Shot vs. Few-Shot Prompting** -> Zero-shot gives instructions with no examples; few-shot provides two or three examples so the model copies the exact pattern.
- **2.1.3 Chain-of-Thought (CoT)** -> Asking the AI to explain its thinking step-by-step before giving the final answer, which avoids silly math and logic mistakes.
- **2.1.4 Role & Persona Prompting** -> Telling the AI to act like a specific professional, like a senior security engineer or a tax lawyer, to get deeper answers.

### 2.2 **Context Engineering & Compaction**
> Packing the AI's limited memory window with only the most helpful background notes for the current task.

- **2.2.1 Context Composition** -> Assembling the system rules, conversation history, and fresh facts into a single clean message.
- **2.2.2 Context Overflow & Compaction** -> Shrinking or summarizing older chat history so the conversation does not exceed the model's memory limits.
- **2.2.3 Context Relevance & Noise Pruning** -> Keeping out useless chatter so the AI does not get distracted by background noise.

### 2.3 **Structured Outputs & Schema Contracts**
> Forcing the AI to reply in computer-friendly formats like JSON (JavaScript Object Notation) instead of messy free text.

- **2.3.1 JSON Mode & Schema Enforcement** -> Setting strict rules that guarantee the AI fills out every required field in a predefined data format.
- **2.3.2 Pydantic Validation** -> Using code checks to ensure numbers are actually numbers and required text fields are not missing.
- **2.3.3 Malformed Output Recovery** -> Automatically asking the AI to fix its mistake or retrying whenever it returns broken data.

---

## 3. **Embeddings & Vector Search**
### Learn how to turn words into lists of numbers so computers can search ideas by meaning.

### 3.1 **Embeddings & Semantic Search**
> Translating sentences into long lists of numbers called vectors that measure what ideas mean.

- **3.1.1 Vectors** -> Lists of numbers that act like GPS coordinates for an idea inside the computer's memory space.
- **3.1.2 Semantic Similarity** -> Mathematical matching showing that "dog" and "puppy" mean almost the same thing even though they are spelled differently.
- **3.1.3 Embedding Dimensions** -> The length of the number list; longer lists capture finer details but take up more storage space.
- **3.1.4 Embedding Models** -> Dedicated programs that turn raw text into vectors; you must always use the same model to save and search.

### 3.2 **Vector Databases & Indexing**
> Special digital filing cabinets designed to quickly find number lists that are close together.

- **3.2.1 Approximate Nearest Neighbor (ANN)** -> A fast math shortcut that finds the closest matching vectors in milliseconds across millions of items.
- **3.2.2 Popular Vector Databases** -> Specialized storage tools like Chroma, Qdrant, Pinecone, Weaviate, and pgvector (PostgreSQL vector extension).
- **3.2.3 Metadata Filtering** -> Tagging documents with labels like date, user, or category so you only search through relevant folders.

### 3.3 **Hybrid Search & Ranking**
> Combining classic word matching with modern meaning search so you get the best of both worlds.

- **3.3.1 Keyword Search (BM25 - Best Matching 25)** -> A classic search formula that ranks documents by counting exact matching words, numbers, and IDs.
- **3.3.2 Hybrid Search** -> Blending keyword search (exact word matches) with vector search (concept matches) for top-tier accuracy.
- **3.3.3 Reciprocal Rank Fusion (RRF)** -> A simple math formula that merges two ranked search lists into one master list without needing extra AI calls.

---

## 4. **Retrieval-Augmented Generation (RAG)**
### Giving the AI an open book of your private documents so it answers with real facts instead of making things up.

### 4.1 **Basic RAG Pipeline**
> Looking up the right page in your company notes and handing it to the AI before asking it to write an answer.

- **4.1.1 Document Indexing** -> Converting your company articles and manuals into searchable vectors inside a vector database.
- **4.1.2 Candidate Retrieval** -> Finding the top matching paragraphs from your database using vector similarity search.
- **4.1.3 Prompt Augmentation** -> Sticking the retrieved paragraphs directly inside the prompt so the AI can read them before answering.
- **4.1.4 Groundedness & Hallucination Defense** -> Making sure the AI's final answer only uses facts found in your notes rather than its own imagination.
- **4.1.5 RAG vs. Fine-Tuning** -> RAG gives the model fresh facts at query time without changing its brain; fine-tuning changes model weights permanently to learn style or vocabulary.

### 4.2 **Document Ingestion & Chunking**
> Cleaning and preparing messy files like PDFs, spreadsheets, and web pages so the computer can read them smoothly.

- **4.2.1 Document Parsing** -> Stripping out headers, footers, and messy formatting from PDFs and scanned images.
- **4.2.2 Chunking Strategies** -> Chopping big documents into smaller, bite-sized paragraphs (by size, sentence, or hierarchy) so they fit neatly into the AI's memory.
- **4.2.3 Index Freshness & Sync** -> Keeping your search index up to date whenever source documents are edited, added, or deleted.

### 4.3 **Advanced RAG & Retrieval Quality**
> Measuring and polishing search results with smart sorting models so the AI gets the best possible clues.

- **4.3.1 Re-Ranking** -> Running a specialized sorting model over your top search results to score how well each paragraph actually answers the question.
- **4.3.2 Precision@K & Recall@K** -> Precision measures how clean your top search results are; Recall measures whether you missed any key documents.
- **4.3.3 Mean Reciprocal Rank (MRR)** -> A metric that checks how close the very first correct answer was to the top of the search results list.
- **4.3.4 Retrieval Quality Frameworks (RAGAS)** -> Automated tools that test if your RAG pipeline finds the right documents and generates truthful answers.

---

## 5. **AI Agents & Stateful Orchestration**
### Turning an AI from a talking assistant into a worker that can browse tools, take actions, and solve multi-step problems.

### 5.1 **Agent Fundamentals & the ReAct Loop**
> An AI inside a loop that can think, pick a tool, look at the result, and repeat until the job is done.

- **5.1.1 What is an AI Agent vs Chatbot** -> A chatbot only talks back and forth; an AI agent plans, decides, and executes external actions autonomously.
- **5.1.2 The ReAct Loop (Reason + Act)** -> A repeating cycle where the AI reasons about what to do, takes an action, and examines the result.
- **5.1.3 Agent Harness** -> The outer code wrapper you write to run the agent loop, enforce safety rules, and stop runaway behavior.
- **5.1.4 Stop Conditions** -> Explicit triggers that tell the agent its mission is accomplished and it should return the final answer.

### 5.2 **Agent Tools & Function Calling**
> Giving the AI permission to invoke specific code functions in the real world.

- **5.2.1 Tool Schemas** -> Clear descriptions that tell the AI what each tool does, what arguments it needs, and what it returns.
- **5.2.2 Execution Sandboxing** -> Running risky code or tools inside safe, isolated containers so a bug cannot harm your servers.
- **5.2.3 Tool Failure Recovery** -> Teaching the agent how to read tool error messages and try an alternative tool instead of giving up.

### 5.3 **State, Memory & Checkpoints**
> Helping the agent remember what it already accomplished so it does not lose its place or repeat work.

- **5.3.1 Short-Term Memory** -> The current chat window holding recent user messages and immediate tool outputs.
- **5.3.2 Long-Term Episodic vs. Semantic Memory** -> Episodic memory stores specific past events and past conversations; semantic memory stores timeless facts and learned user preferences.
- **5.3.3 Checkpoints & Session Persistence** -> Saved snapshots of the agent's work after every tool call so it can pick back up if the computer crashes.

### 5.4 **Stateful Workflows & State Machines**
> Connecting multiple steps like a train schedule so complex jobs follow strict, predictable tracks.

- **5.4.1 State Machines** -> A clear diagram of allowed steps (like PLAN -> SEARCH -> APPROVE -> FINISH) that keeps the agent on track.
- **5.4.2 Write-Ahead Log (WAL)** -> Saving the agent's next planned step to disk before running it, ensuring no steps get mysteriously lost.
- **5.4.3 Parallel Tool Calls** -> Asking the model to call several independent tools simultaneously to cut down waiting time.

### 5.5 **Model Context Protocol (MCP)**
> A universal USB cable for AI that lets agents plug into databases, servers, and tools without custom wiring.

- **5.5.1 MCP Server** -> A small program that exposes internal tools and private data (like a database or file system) using a standard protocol.
- **5.5.2 MCP Client** -> The AI agent or application that connects to MCP servers to discover and invoke tools dynamically.
- **5.5.3 MCP Host & Tools** -> The user environment (like Claude Desktop, an IDE, or an agent runtime) that manages the MCP connections securely.

### 5.6 **Multi-Agent Coordination & Agent-to-Agent (A2A)**
> Dividing difficult projects among a team of specialized AI workers instead of asking one agent to do everything.

- **5.6.1 Orchestrator-Worker Pattern** -> One manager agent plans the work and hands smaller jobs to specialized worker agents.
- **5.6.2 Agent-to-Agent (A2A) Protocols** -> Standard rules for how two different AI agents pass messages and hand off tasks to each other.
- **5.6.3 Shared State & Conflict Resolution** -> Using locks and task queues so two agents working at the same time do not accidentally overwrite each other.

---

## 6. **Reliability, Safety & Guardrails**
### Making sure your AI apps do not crash, loop forever, spend too much money, or do dangerous things.

### 6.1 **Failure Engineering & Fallbacks**
> Preparing for when tools break, networks fail, or the AI gives a confusing response.

- **6.1.1 Retries with Exponential Backoff** -> Trying a failed network request again while waiting twice as long between each attempt.
- **6.1.2 Dynamic Fallbacks** -> Automatically switching to a simpler model or alternate tool if the primary one goes down or errors out.
- **6.1.3 Idempotency Keys** -> Unique receipt codes that make sure retrying a tool call (like charging a credit card) never happens twice.
- **6.1.4 Degraded Modes** -> Answering with partial information safely when an external service is unavailable instead of crashing completely.

### 6.2 **Bounded Execution & Loop Prevention**
> Putting strict speed limits and seatbelts on AI agents so they never go rogue or waste budget.

- **6.2.1 Iteration Limits** -> A hard maximum cap on loop cycles (usually 5 to 10 turns) to prevent infinite thinking loops.
- **6.2.2 Token & Cost Budgets** -> Setting a dollar spending limit per task so a runaway query does not drain your bank account.
- **6.2.3 Timeout Limits** -> Killing tool calls or agent runs that take too long to respond so users are not left waiting forever.

### 6.3 **Human-in-the-Loop (HITL) & Approval Gates**
> Requiring a real person to review and click 'approve' before the AI performs any dangerous or permanent action.

- **6.3.1 Approval Gates** -> Deliberate pause buttons where the agent stops and waits for a human to confirm before deleting data or sending money.
- **6.3.2 Risk-Based Autonomy** -> Letting the AI do safe chores (reading files) freely, but strictly locking down dangerous actions (modifying databases).
- **6.3.3 Escalation Rules** -> Explicit instructions telling the agent to stop and ask for help whenever its confidence is low or it feels stuck.

### 6.4 **Guardrails & Prompt Injection Defense**
> Security checkpoints that scan what enters and exits the AI to catch bad inputs and harmful outputs.

- **6.4.1 Prompt Injections & Jailbreaks** -> Tricks where malicious users hide commands in their text to make the AI ignore its safety instructions.
- **6.4.2 Input & Output Guardrails** -> Scanning user questions for toxic or hacking text, and scanning AI replies for leaked passwords or confidential files.
- **6.4.3 Dual-LLM Quarantine** -> Using a small guard model to inspect untrusted text from the web before letting the main reasoning model touch it.

---

## 7. **Evaluation & Observability**
### Proving your AI system actually works well and watching every step in production like a flight recorder.

### 7.1 **Deterministic & Metric-Based Evals**
> Fast, automated code checks that grade whether your AI is giving exact, expected answers.

- **7.1.1 Schema & Invariant Checks** -> Testing that responses always match the required format and never violate hard rules.
- **7.1.2 Exact Match & String Tests** -> Checking if critical answers contain exact expected words, IDs, or formulas.
- **7.1.3 Golden Datasets** -> A curated test bank of real-world questions paired with verified answers used to test system improvements.

### 7.2 **LLM-as-a-Judge & Model-Based Evals**
> Using a capable model like GPT-4 or Claude to grade another model's answers against an explicit scoring rubric.

- **7.2.1 Evaluation Rubrics** -> Clear grading guidelines given to the judge model defining what counts as a good or bad answer.
- **7.2.2 Faithfulness & Groundedness Evals** -> Measuring whether an answer was backed up 100% by the retrieved documents or made up out of thin air.
- **7.2.3 Judge Calibration & Bias Checks** -> Making sure the judge model grades fairly and does not prefer long-winded answers over concise ones.

### 7.3 **Agent Trajectory & Behavior Evaluation**
> Grading the agent's full path of tool choices to see if it took smart, efficient steps rather than stumbling around.

- **7.3.1 Trajectory Steps** -> Reviewing the chronological list of every tool call, argument, and observation the agent made.
- **7.3.2 Tool Selection Accuracy** -> Measuring whether the agent called the most appropriate tool for the job or picked tools randomly.
- **7.3.3 Efficiency Scoring** -> Checking whether the agent finished the task in 3 smart steps or wasted time and money taking 12 clumsy steps.

### 7.4 **Observability, Tracing & Golden Signals**
> A live dashboard showing every thought, tool call, token count, and dollar spent for every user request.

- **7.4.1 Distributed Tracing** -> Recording an entire agent journey as a tree of steps so you can see which specific tool or prompt caused a delay.
- **7.4.2 Spans & Traces** -> A trace is the complete story of a user request; a span is one single chapter, like a database query or model call.
- **7.4.3 OpenTelemetry (OTel) GenAI Conventions** -> An industry-standard format for logging AI token counts, model names, and response durations.
- **7.4.4 Golden Signals (Cost, Latency, Errors)** -> Live alerts that sound if your response time slows down, errors spike, or token costs jump.

---

## 8. **Production, Inference & Systems Optimization**
### Making your AI apps lightning fast, inexpensive to run, and ready for millions of real users.

### 8.1 **Latency, Cost & Caching Optimization**
> Cutting your monthly AI bill and speeding up response times without sacrificing quality.

- **8.1.1 Model Routing** -> Directing simple tasks to tiny, cheap models and saving expensive flagship models only for hard reasoning.
- **8.1.2 Semantic Caching** -> Saving answers to common questions so if someone asks the same idea in different words, you answer instantly for free.
- **8.1.3 Prompt Caching** -> Storing the model's memory of long static prompts on the server so you do not pay or wait to re-read them every time.
- **8.1.4 Async & Parallel Processing** -> Firing off multiple independent tool lookups at the same time instead of waiting for them one by one.

### 8.2 **Serving, KV Cache & Continuous Batching**
> Understanding how the hardware and servers hosting AI models handle heavy traffic.

- **8.2.1 KV Cache (Key-Value Cache)** -> A GPU memory trick that stores the mathematical notes of past tokens so the model does not recalculate them from scratch.
- **8.2.2 Continuous Batching (vLLM)** -> A smart server trick that squeezes multiple user requests into the GPU simultaneously without waiting for previous requests to finish.
- **8.2.3 Rate Limiting & Load Shedding** -> Gracefully slowing down or queueing requests so your app does not crash when hitting API quotas.
- **8.2.4 Speculative Decoding** -> Using a tiny model to draft several words quickly and a big model to verify them all in one fast pass.

### 8.3 **Multi-Modal AI Systems**
> Expanding beyond plain text so your AI can see pictures, listen to voices, and inspect videos.

- **8.3.1 Vision Processing** -> Feeding images, diagrams, and scanned forms to the model so it can describe what it sees and extract data.
- **8.3.2 Speech-to-Text (STT) & Text-to-Speech (TTS)** -> Transcribing spoken words into written text and turning written replies back into natural human speech.
- **8.3.3 Cross-Modal Reasoning** -> Asking the AI questions that require checking both a picture and written instructions at the exact same time.

### 8.4 **Enterprise Capstone: Production Agent Architecture**
> Bringing all eight categories together into one deterministic, fault-tolerant enterprise system.

- **8.4.1 End-to-End Pipeline Integration** -> Connecting Document Ingestion -> RAG Retrieval -> Agent Reasoning -> Tool Execution -> Guardrails -> Output.
- **8.4.2 Auditability & Compliance** -> Storing complete execution logs and human approval timestamps for corporate governance and regulatory review.
- **8.4.3 CI/CD Evaluation Gates** -> Automatically running your test suite of evals before deploying any new prompt, model version, or tool to production.
