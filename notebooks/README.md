# 📓 Interactive Companion Notebooks: AI Systems Engineering in Action

> **Visual, Executable Labs for High-Performance AI Engineering**  
> Run immediately in **Google Colab** with zero local setup, or execute locally inside JupyterLab / VS Code.

---

## 🧭 Overview & Pedagogical Purpose

While the production framework [`agent-forge/`](../agent-forge/) models enterprise microservices architecture and the canonical [`labs/`](../labs/) verify architectural contracts via headless CLI harnesses, these companion notebooks offer **interactive, visual, and step-by-step experimentation**:

1. **Observe Intermediate Math & Mechanics**: Visualize subword tokenization splits, KV-cache memory bandwidth walls, Reciprocal Rank Fusion rank merging, and token-bucket decay curves.
2. **Zero-Setup Cloud Execution**: Every notebook contains self-contained bootstrap cells that clone the repository shallowly, configure environment paths, and execute with zero external API key requirements by default.
3. **Interactive Debuggers**: Step through simulated mid-flight agent crashes, inspect Model Context Protocol JSON-RPC wire frames, and explore SHAP waterfall plots for algorithmic fairness audits.

---

## 🚀 Companion Notebook Catalog

| Notebook | Topic & Architectural Focus | Target Curriculum Phase & Lab | Colab 1-Click Launch |
| :--- | :--- | :--- | :---: |
| **[`00_token_mechanics_and_kv_cache.ipynb`](./00_token_mechanics_and_kv_cache.ipynb)** | **Token Mechanics, Attention & KV-Cache Sizing**<br>• Byte-Pair Encoding (BPE) subword splitting<br>• Character vs byte vs token ratio comparison<br>• MHA vs GQA vs MLA KV-cache memory calculator<br>• Roofline model: compute vs memory bandwidth ceilings | [Phase 00: Foundations](../00-foundations-and-token-mechanics/README.md) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dip4k/senior-engineer-to-ai-engineer-roadmap/blob/main/notebooks/00_token_mechanics_and_kv_cache.ipynb) |
| **[`01_prompt_caching_and_budgeting.ipynb`](./01_prompt_caching_and_budgeting.ipynb)** | **Prompt Caching Economics & Context Budgeting**<br>• Break-even economics: cold vs cached prefix hit costs<br>• Needle-In-A-Haystack (NIAH) depth vs length heatmap<br>• Context AST token allocation budget portfolio | [Phase 01: Prompt Engineering](../01-prompt-and-context-engineering/README.md) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dip4k/senior-engineer-to-ai-engineer-roadmap/blob/main/notebooks/01_prompt_caching_and_budgeting.ipynb) |
| **[`02_hybrid_rag_and_rrf_visualizer.ipynb`](./02_hybrid_rag_and_rrf_visualizer.ipynb)** | **Hybrid RAG & Reciprocal Rank Fusion (RRF)**<br>• Sparse BM25 keyword search vs Dense vector search<br>• Reciprocal Rank Fusion (RRF `k=60`) rank merging<br>• Multi-tenant strict pre-filtering vs flawed post-filtering | [Phase 02: RAG](../02-rag-and-knowledge-systems/README.md)<br>[Lab 01: Hybrid RAG](../labs/lab-01-multi-tenant-hybrid-rag.md) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dip4k/senior-engineer-to-ai-engineer-roadmap/blob/main/notebooks/02_hybrid_rag_and_rrf_visualizer.ipynb) |
| **[`02_end_to_end_production_rag.ipynb`](./02_end_to_end_production_rag.ipynb)** | **End-to-End Production RAG Pipeline (Open-Source)**<br>• Full Ingestion Flow: parsing, hierarchical & contextual chunking<br>• Open-source embeddings (`sentence-transformers`), `chromadb`, `rank_bm25`<br>• Multi-provider generation: Gemini, Groq, or offline fallback<br>• 3-Paradigm Benchmark: Naive vs Improved vs AI-Assisted RAG | [Phase 02: RAG](../02-rag-and-knowledge-systems/README.md)<br>[Lab 01: Hybrid RAG](../labs/lab-01-multi-tenant-hybrid-rag.md) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dip4k/senior-engineer-to-ai-engineer-roadmap/blob/main/notebooks/02_end_to_end_production_rag.ipynb) |
| **[`03_mcp_client_and_tool_inspector.ipynb`](./03_mcp_client_and_tool_inspector.ipynb)** | **Model Context Protocol (MCP) & Tool Inspector**<br>• JSON-RPC 2.0 message inspector (`tools/list`, `tools/call`)<br>• ABAC Policy Engine evaluation & boundary enforcement<br>• Blocking hazardous mutation queries (`DROP`, `DELETE`) | [Phase 03: Tools & MCP](../03-tools-and-model-context-protocol/README.md)<br>[Lab 02: MCP Execution](../labs/lab-02-tool-execution-with-mcp.md) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dip4k/senior-engineer-to-ai-engineer-roadmap/blob/main/notebooks/03_mcp_client_and_tool_inspector.ipynb) |
| **[`04_stateful_agent_and_wal_replay.ipynb`](./04_stateful_agent_and_wal_replay.ipynb)** | **Stateful Agent ReAct Loop & WAL Crash Replay**<br>• Step-by-step ReAct loop (Thought → Action → Observation)<br>• Write-Ahead Log (WAL) event persistence in `EventStore`<br>• Simulated mid-flight crash & deterministic event replay | [Phase 04: Agentic Systems](../04-agentic-systems-and-orchestration/README.md)<br>[Lab 03: Stateful Agent](../labs/lab-03-stateful-agent-orchestration.md) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dip4k/senior-engineer-to-ai-engineer-roadmap/blob/main/notebooks/04_stateful_agent_and_wal_replay.ipynb) |
| **[`05_token_bucket_and_failure_defense.ipynb`](./05_token_bucket_and_failure_defense.ipynb)** | **Token-Bucket Rate Limiter & Circuit Breakers**<br>• Streaming token bucket capacity & refill mechanics<br>• Upfront reservation vs streaming settlement<br>• Circuit breaker state transitions (Closed → Open → Half-Open) | [Phase 05: Serving & Gateways](../07-production-deployment-and-llmops/README.md)<br>[Lab 04: Failure Defense](../labs/lab-04-agent-failure-defense.md) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dip4k/senior-engineer-to-ai-engineer-roadmap/blob/main/notebooks/05_token_bucket_and_failure_defense.ipynb) |
| **[`06_eval_flywheel_and_trace_trees.ipynb`](./06_eval_flywheel_and_trace_trees.ipynb)** | **OTel GenAI Distributed Tracing & LLM Evals**<br>• OpenTelemetry GenAI semantic conventions distributed tracing<br>• Span parent-child trace trees and waterfall latency plots<br>• LLM-as-a-judge Groundedness & Faithfulness evaluation | [Phase 06: Evals & Observability](../06-evals-and-observability/README.md)<br>[Lab 05: Observability Tracing](../labs/lab-05-ai-observability-tracing.md)<br>[Lab 06: Quarantine Guardrails](../labs/lab-06-dual-llm-quarantine-guardrails.md) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dip4k/senior-engineer-to-ai-engineer-roadmap/blob/main/notebooks/06_eval_flywheel_and_trace_trees.ipynb) |
| **[`07_ml_fairness_and_shap_explainability.ipynb`](./07_ml_fairness_and_shap_explainability.ipynb)** | **ML Fairness, Disparate Impact & SHAP XAI**<br>• Regulated financial credit scoring pipeline<br>• Fairlearn disparate impact metric & 80% (4/5ths) rule audit<br>• SHAP waterfall feature attribution for adverse action notices | [Phase 07: ML Systems](../07-production-deployment-and-llmops/README.md)<br>[Lab 07: ML Fairness & XAI](../labs/lab-07-hybrid-ml-fairness-and-explainability.md) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dip4k/senior-engineer-to-ai-engineer-roadmap/blob/main/notebooks/07_ml_fairness_and_shap_explainability.ipynb) |

---

## 🛠️ Execution Environments

### Option A: Running in Google Colab (Recommended for Fast Exploration)

1. Click any **"Open in Colab"** badge above.
2. The initial bootstrap cell automatically clones the repository shallowly and installs all dependencies:
   ```python
   # %% [Setup] Colab & Environment Bootstrap
   import os, sys
   if 'google.colab' in str(get_ipython()):
       print('Running in Google Colab. Cloning repository...')
       !git clone --depth 1 https://github.com/dip4k/senior-engineer-to-ai-engineer-roadmap.git repo
       %cd repo
       !pip install -q -r agent-forge/requirements.txt -r notebooks/requirements-notebooks.txt
       sys.path.insert(0, os.path.abspath('agent-forge'))
   ```
3. Run cells sequentially (`Shift` + `Enter`). All algorithms and simulations use deterministically generated datasets and mock embeddings so they function offline without external paid API credits.

### Option B: Running Locally

To run the companion notebooks locally on your workstation:

```bash
# 1. Clone repository (if not already done)
git clone https://github.com/dip4k/senior-engineer-to-ai-engineer-roadmap.git
cd senior-engineer-to-ai-engineer-roadmap

# 2. Create and activate a Python virtual environment
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# 3. Install core agent framework and notebook visualization dependencies
pip install -r agent-forge/requirements.txt
pip install -r notebooks/requirements-notebooks.txt

# 4. Launch JupyterLab or VS Code
jupyter lab notebooks/
```

---

## 📊 Alignment with Headless CLI Evaluation Harness

Each companion notebook is matched with a canonical headless lab verification script:

```bash
# Verify all canonical labs headless in CI/CD
python scripts/verify_lab.py --all

# Or verify an individual lab target:
python scripts/verify_lab.py --lab 1   # Hybrid RAG & Tenant Isolation
python scripts/verify_lab.py --lab 2   # MCP Tool Execution & ABAC
python scripts/verify_lab.py --lab 3   # Stateful Agent & WAL Crash Replay
python scripts/verify_lab.py --lab 4   # Token Bucket & Failure Defense
python scripts/verify_lab.py --lab 5   # GenAI Observability & Trace Trees
python scripts/verify_lab.py --lab 6   # Dual-LLM Quarantine Perimeter
python scripts/verify_lab.py --lab 7   # ML Fairness & SHAP Attributions
```

---

## 📚 Related Curricular Resources

- **Canonical Lab Guides**: [`labs/`](../labs/)
- **Microservices Agent Platform**: [`agent-forge/`](../agent-forge/)
- **Master Syllabus**: [`README.md`](../README.md)
- **Conceptual Roadmap**: [`AI_ENGINEER_ROADMAP.md`](../AI_ENGINEER_ROADMAP.md)
- **Production Glossary**: [`ai-engineering-glossary-by-practice.md`](../ai-engineering-glossary-by-practice.md)
