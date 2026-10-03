# AI Engineering Glossary

> Auto-maintained by the `ai-curriculum-architect` agent in **INTEGRATE mode**.
> Each entry links to the lesson that **owns** the term — where it is taught from zero.
> Software engineering terms are not in this glossary; they are assumed known.

To add a term: run the agent in INTEGRATE mode after approving new research. It appends new terms alphabetically and links them to the owning lesson.

---

## A

**Agent** — A program that uses an LLM to decide what to do next, calls tools, observes the results, and loops until the task is done or a turn limit is hit.
→ [Phase 04: Agentic Systems and Orchestration](./04-agentic-systems-and-orchestration/README.md)

**Attention** — The mechanism inside a transformer that lets every token in a sequence look at every other token and decide how much weight to give it when predicting the next token.
→ [Phase 00: Foundations — Transformer and Hardware Physics](./00-foundations-and-token-mechanics/02-transformer-and-hardware-physics.md)

---

## B

**BM25** — A keyword-based scoring function that ranks documents by how often query words appear in them, adjusted for document length. Best for exact-word matches.
→ [Phase 02: Retrieval — Hybrid Search](./02-rag-and-knowledge-systems/README.md)

---

## C

**Context window** — The maximum number of tokens an LLM can read at one time (both input and output together). Sending more tokens than the limit causes the model to silently drop the oldest content.
→ [Phase 00: Foundations — Tokenization and BPE Mechanics](./00-foundations-and-token-mechanics/01-tokenization-and-bpe-mechanics.md)

**Cosine similarity** — A number between -1 and 1 that measures how similar two vectors are by the angle between them, ignoring their length. Two vectors pointing in the same direction score 1.
→ [Phase 02: Retrieval — Embeddings](./02-rag-and-knowledge-systems/README.md)

---

## E

**Embedding** — A fixed-length list of numbers produced by an embedding model that represents what a piece of text means. Texts with similar meaning get similar numbers.
→ [Phase 02: Retrieval — Embeddings](./02-rag-and-knowledge-systems/README.md)

**Embedding model** — A neural network that converts text (as tokens) into an embedding vector. Documents and queries must use the same model or their vectors cannot be compared.
→ [Phase 02: Retrieval — Embeddings](./02-rag-and-knowledge-systems/README.md)

**Eval** — A test that measures whether an AI system produces a correct, grounded, or useful output. Evals can be written rules, human labels, or another LLM acting as a judge.
→ [Phase 06: Evals and Observability](./06-evals-and-observability/README.md)

---

## F

**Fine-tuning** — Continuing to train a pre-trained model on a smaller dataset so it specializes in a new task or domain, changing its weights.
→ [Phase 07: Production Deployment and LLMOps](./07-production-deployment-and-llmops/README.md)

**Few-shot prompting** — Giving an LLM a small number of input-output examples inside the prompt so it learns the pattern for the current request without retraining.
→ [Phase 01: Prompt and Context Engineering](./01-prompt-and-context-engineering/README.md)

---

## G

**Grounding** — Anchoring a model's output in specific, retrievable source documents so claims can be checked and cited, reducing hallucination.
→ [Phase 02: Retrieval — RAG](./02-rag-and-knowledge-systems/README.md)

---

## H

**Hallucination** — When a model generates a confident, fluent statement that is factually wrong or not supported by the provided context. Not a bug in code; a statistical property of token prediction.
→ [Phase 00: Foundations — What is an LLM](./00-foundations-and-token-mechanics/00-what-is-an-llm.md)

**HNSW (Hierarchical Navigable Small World)** — A graph-based approximate nearest neighbor index used by vector databases to find the closest embedding vectors quickly without scanning all of them.
→ [Phase 02: Retrieval — Hybrid Search](./02-rag-and-knowledge-systems/README.md)

---

## K

**KV cache** — A GPU-resident memory table that stores the key and value matrices computed for tokens already processed, so the model does not recompute them on every new token. The main driver of VRAM cost at inference time.
→ [Phase 00: Foundations — KV Cache, VRAM, and Bandwidth Physics](./00-foundations-and-token-mechanics/03-kv-cache-vram-and-bandwidth-physics.md)

---

## L

**LLM (Large Language Model)** — A neural network trained on large amounts of text that predicts the next token based on all tokens seen so far. The word "large" refers to the number of trainable parameters, not a fixed threshold.
→ [Phase 00: Foundations — What is an LLM](./00-foundations-and-token-mechanics/00-what-is-an-llm.md)

---

## M

**MCP (Model Context Protocol)** — An open wire protocol (JSON-RPC 2.0) that lets an LLM call external tools, APIs, and data sources through a standardized interface. Equivalent to a syscall table for AI agents.
→ [Phase 03: Tools and Model Context Protocol](./03-tools-and-model-context-protocol/README.md)

---

## P

**Prompt** — The full text sent to an LLM as input, including system instructions, few-shot examples, conversation history, and the user's current request.
→ [Phase 01: Prompt and Context Engineering](./01-prompt-and-context-engineering/README.md)

---

## Q

**Quantization** — Reducing the number of bits used to store each model weight (e.g., from 16-bit floats to 4-bit integers). Shrinks memory footprint and speeds up inference at the cost of a small, measurable quality loss.
→ [Phase 00: Foundations — SLMs and Quantization Mechanics](./00-foundations-and-token-mechanics/05-slms-and-quantization-mechanics.md)

---

## R

**RAG (Retrieval-Augmented Generation)** — A pattern where relevant documents are retrieved from a knowledge base and injected into the LLM prompt at query time, grounding the response in current, specific information without retraining.
→ [Phase 02: Retrieval and Knowledge Systems](./02-rag-and-knowledge-systems/README.md)

**Reasoning model** — An LLM that generates a chain-of-thought trace before its final answer, trading extra token cost and latency for higher accuracy on multi-step problems.
→ [Phase 00: Foundations — Test-Time Compute and Reasoning Models](./00-foundations-and-token-mechanics/04-test-time-compute-and-reasoning-models.md)

**Relevance threshold** — A minimum similarity score below which a retrieval result is discarded rather than passed to the LLM. Prevents the model from answering from unrelated documents.
→ [Phase 02: Retrieval — Embeddings](./02-rag-and-knowledge-systems/README.md)

**RRF (Reciprocal Rank Fusion)** — A score merging function that combines ranked lists from different retrieval systems (e.g., keyword and vector) by summing reciprocal rank positions, without needing to calibrate scores across systems.
→ [Phase 02: Retrieval — Hybrid Search](./02-rag-and-knowledge-systems/README.md)

---

## S

**Speculative decoding** — A serving technique where a small draft model predicts several tokens ahead, and the main model verifies them in one forward pass. Reduces latency without changing output quality.
→ [Phase 07: Production Deployment and LLMOps](./07-production-deployment-and-llmops/README.md)

**System prompt** — The part of the LLM input that sets persistent instructions, persona, and constraints before the conversation history or user message. Processed first; often cached by inference engines.
→ [Phase 01: Prompt and Context Engineering](./01-prompt-and-context-engineering/README.md)

---

## T

**Temperature** — A parameter (0.0 to 2.0) that controls how random the model's token sampling is. Zero means the model always picks the highest-probability token. Higher values increase variety and creativity at the cost of consistency.
→ [Phase 01: Prompt and Context Engineering](./01-prompt-and-context-engineering/README.md)

**Token** — The basic unit of text an LLM reads and writes. A token is roughly 3-4 characters of English text on average. Models charge per token and stop when they hit their context window limit.
→ [Phase 00: Foundations — Tokenization and BPE Mechanics](./00-foundations-and-token-mechanics/01-tokenization-and-bpe-mechanics.md)

**Tokenizer** — A program that converts raw text into a sequence of tokens before it reaches the LLM. The same text produces different token counts with different tokenizers.
→ [Phase 00: Foundations — Tokenization and BPE Mechanics](./00-foundations-and-token-mechanics/01-tokenization-and-bpe-mechanics.md)

---

## V

**Vector** — A fixed-length list of numbers. In AI context, the output of an embedding model that represents a piece of text as a point in high-dimensional space.
→ [Phase 02: Retrieval — Embeddings](./02-rag-and-knowledge-systems/README.md)

**VRAM** — Video Random Access Memory: the high-bandwidth memory on a GPU. The main constraint when running or serving an LLM. Model weights, KV cache, and activations all compete for the same VRAM budget.
→ [Phase 00: Foundations — KV Cache, VRAM, and Bandwidth Physics](./00-foundations-and-token-mechanics/03-kv-cache-vram-and-bandwidth-physics.md)

---

## W

**WAL (Write-Ahead Log)** — An event log written before an agent executes a tool call or state transition, so the agent can replay from the last committed state after a crash. The AI equivalent of a database WAL.
→ [Phase 04: Agentic Systems and Orchestration](./04-agentic-systems-and-orchestration/README.md)

---

*This glossary is seeded with terms from Phases 00–04. New terms are added by the `ai-curriculum-architect` agent in INTEGRATE mode. Each entry is one plain-English sentence — no jargon stacking.*
