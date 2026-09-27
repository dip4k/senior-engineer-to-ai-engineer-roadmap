# Phase 06: Evals, Observability & Telemetry

> **A Master-Class for Senior Engineers, Tech Leads, and AI Architects on Moving from Superficial "Vibe Checks" to Deterministic Continuous Evaluation, Agent Trajectory Analysis, and OpenTelemetry-Native Distributed Observability.**

---

> Curriculum taxonomy aligns with the [3-tier classification defined in the root README](../README.md) (`[MUST-HAVE]` 🔴, `[GOOD-TO-HAVE]` 🟡, `[KNOWLEDGE-BASE]` 🔵).

---

```mermaid
flowchart TD
    A["THE CONTINUOUS EVALUATION FLYWHEEL<br/>Trace Logs • Edge Cases • Golden Sets • CI/CD Gates"]
    
    A --> B["OBSERVABILITY<br/>• OpenTelemetry Spans<br/>• TTFT & Token Rates<br/>• Cache Hit Tracking<br/>• Distributed Traces"]
    A --> C["EVALUATIONS<br/>• Level 1: Unit Tests<br/>• Level 2: LLM-as-Judge<br/>• Level 3: Online User<br/>• Trajectory Analysis"]
    
    B --> D["DETERMINISTIC PRODUCTION CONFIDENCE<br/>Zero-Regression Deploys • Cost Gates • Quality SLAs"]
    C --> D
```

---

## 📑 Table of Contents

1. [Executive Summary & Lead Mental Model [MUST-HAVE] 🔴](#-executive-summary--lead-mental-model-must-have-)
2. [Why This Matters for Senior & Lead Developers [MUST-HAVE] 🔴](#️-why-this-matters-for-senior--lead-developers-must-have-)
3. [The Three Levels of Evals (The Hamel Husain Framework) [MUST-HAVE] 🔴](#-the-three-levels-of-evals-the-hamel-husain-framework-must-have-)
4. [Agent & Trajectory Evaluation [GOOD-TO-HAVE] 🟡](#-agent--trajectory-evaluation-good-to-have-)
5. [Curation of Evaluation Datasets [MUST-HAVE] 🔴](#-curation-of-evaluation-datasets-must-have-)
6. [Observability, Distributed Tracing & OpenTelemetry [MUST-HAVE] 🔴](#-observability-distributed-tracing--opentelemetry-must-have-)
7. [Key Telemetry & Performance Metrics [MUST-HAVE] 🔴](#-key-telemetry--performance-metrics-must-have-)
8. [Evaluation Methodologies Comparison [MUST-HAVE] 🔴](#️-evaluation-methodologies-comparison-must-have-)
9. [Production Failure Modes, Biases & Anti-Patterns [MUST-HAVE] 🔴](#️-production-failure-modes-biases--anti-patterns-must-have-)
10. [Production-Grade Code Implementations [MUST-HAVE] 🔴](#-production-grade-code-implementations-must-have-)
11. [Curated Verified Resources & Seminal Reading [KNOWLEDGE-BASE] 🔵](#-curated-verified-resources--seminal-reading-knowledge-base-)
12. [Capstone Challenge: Automated CI/CD Evaluation Pipeline [MUST-HAVE] 🔴](#-capstone-challenge-automated-cicd-evaluation-pipeline-must-have-)

---

## 🎯 Executive Summary & Lead Mental Model [MUST-HAVE] 🔴

Why does your AI product need evals? Let's talk about the dreaded "vibe check". 

You tweak your system prompt. You go to a chat playground. You test three or four messages, squint at the screen, and think, "Yeah, the vibes are good." Two days later, a customer files Bug #1. Your agent is hallucinating a JSON payload schema that completely breaks the frontend. You realize you have no idea if your new prompt just broke 10 other things.

As Hamel Husain points out repeatedly, **probabilistic components require deterministic harnesses**. You cannot control the stochastic behavior of neural nets through prompt optimism. You control it through continuous regression matrices, golden datasets harvested from production anomalies, and distributed OpenTelemetry tracing.

```mermaid
flowchart LR
    subgraph Probabilistic["PROBABILISTIC ENGINE"]
        A["Stochastic Neural Net<br/>• Temperature sampling<br/>• Shifting token distributions<br/>• Latent reasoning paths"]
    end
    
    subgraph Deterministic["DETERMINISTIC SOFTWARE"]
        B["Deterministic Harness<br/>• Automated JSON Assertions<br/>• Binary Rubric Judges<br/>• Distributed Span Traces"]
    end
    
    A --> B
    B -- "Continuous Feedback" --> A
```

---

## 🔬 The Three Levels of Evals (The Hamel Husain Framework) [MUST-HAVE] 🔴

Effective evaluation follows a hierarchical pyramid of speed, cost, and diagnostic resolution:

```mermaid
flowchart TD
    L1["<b>Level 1: Deterministic Code & Unit Tests (Foundation)</b><br/>JSON schema validation, regex syntax, exact substring, latency/token bounds"]
    L2["<b>Level 2: Model-Based Evals (LLM-as-a-Judge)</b><br/>Binary rubrics, ground-truth reference scoring, G-Eval reasoning chains"]
    L3["<b>Level 3: Online Human & Production Telemetry</b><br/>Implicit signals, A/B traffic splits, shadow deployment metrics"]
    
    L1 -->|"Pass Deterministic Gates"| L2
    L2 -->|"Pass Benchmark SLAs"| L3
```

### Level 1: Deterministic Code & Unit Tests [MUST-HAVE] 🔴

This is where you should start. It's fast and it's free. If your model output fails a Level 1 schema check or latency threshold, it should never be sent to an expensive LLM judge. Use Pydantic assertions, simple substring exact matches, and latency checks.

```python
# Conceptual Level 1 Assertion Gate
def evaluate_level_1(response: AgentResponse) -> EvalResult:
    # 1. Structural schema validation
    try:
        parsed_payload = ToolCallPayload.model_validate_json(response.raw_text)
    except ValidationError as err:
        return EvalResult(passed=False, score=0.0, reason=f"Schema violation: {err}")

    # 2. Deterministic operational thresholds
    if response.latency_ms > 2500:
        return EvalResult(passed=False, score=0.0, reason="Latency SLA breach (>2500ms)")

    if response.usage.completion_tokens > 450:
        return EvalResult(passed=False, score=0.0, reason="Token budget overflow (>450 tokens)")

    return EvalResult(passed=True, score=1.0, reason="All Level 1 deterministic checks passed")
```

---

### Level 2: Model-Based Evaluation (LLM-as-a-Judge) [MUST-HAVE] 🔴

When testing conversational nuance, faithfulness, or tone alignment, deterministic code fails. You need a stronger model to act as a judge.

> [!CAUTION]
> Never prompt an LLM judge with: *"Rate this response on a scale of 1 to 5 for helpfulness."*
> Continuous Likert scales produce severe drift. A score of "3" from GPT-4 today may equal a "4" tomorrow.

Instead, use **Discrete Binary Pass/Fail Rubrics** equipped with Chain-of-Thought reasoning steps. 

```markdown
### BINARY EVALUATION RUBRIC

| Criteria: Grounded Faithfulness | Description |
|---------------------------------|-------------|
| **PASS (1)** | Every factual assertion in the Generated Response can be directly derived from the provided Context Documents. No extraneous claims. |
| **FAIL (0)** | The Generated Response contains at least one claim, figure, date, or assumption not present in or strictly deducible from Context. |
```

---

### Level 3: Online Human & Production Telemetry [GOOD-TO-HAVE] 🟡

Level 3 operates continuously on live production traffic, capturing the ultimate ground truth: real human interaction and system telemetry.

```mermaid
flowchart TD
    A["PRODUCTION USER INTERACTION"]
    A --> B["EXPLICIT SIGNALS<br/>• Thumbs Up / Down<br/>• 5-Star Ratings<br/>• User Feedback Modal<br/>• Inline Text Edits"]
    A --> C["IMPLICIT SIGNALS<br/>• Copy-to-Clipboard<br/>• Regeneration / Retry<br/>• Dwell Time on Output<br/>• Follow-up Clarifying"]
    B --> D["ANOMALY EXTRACTION PIPELINE<br/>(Flagged for Golden Dataset)"]
    C --> D
```

---

## 🤖 Agent & Trajectory Evaluation [GOOD-TO-HAVE] 🟡

Evaluating a multi-step autonomous agent is completely different from a single-turn chatbot. A single turn produces text; an agent executes a **state trajectory**.

```mermaid
flowchart LR
    A["Turn 1:<br/>USER REQUEST"] --> B["Plan"] --> C["Tool Call:<br/>search_customer(id='C-104')"]
    C --> D["Turn 2:<br/>TOOL RESULT"] --> E["Reflect"] --> F["Tool Call:<br/>fetch_invoices(cust='C-104')"]
    F --> G["Turn 3:<br/>TOOL RESULT"] --> H["Synthesize"] --> I["FINAL ANSWER"]
```

### The SWE-bench Evaluation Harness Paradigm

When evaluating agents that write code or manipulate environments, you use a **Decoupled Evaluation Harness** (like SWE-bench). Here’s the brilliant part: the agent never grades itself. It's totally blind to the evaluation layer.

```mermaid
flowchart TD
    subgraph AgentSpace["1. Untrusted Agent Scaffold"]
        direction TB
        Agent["Autonomous Agent (Claude Code / Aider)"] --> Patch["Emits Git Patch (patch.diff)"]
    end

    subgraph HarnessSpace["2. Deterministic SWE-bench Evaluation Harness"]
        direction TB
        Base["Base Layer: Ubuntu OS + Compiler Tools"] --> Env["Environment Layer: Conda / Virtualenv Dependencies"]
        Env --> Inst["Instance Layer: Repo checked out at exact commit SHA"]
        
        Inst --> Apply["Apply patch.diff"]
        Apply --> Run["Execute eval.sh in Disposable Docker Container"]
        
        Run --> F2P{"FAIL_TO_PASS Check<br/>Did failing tests now pass?"}
        Run --> P2P{"PASS_TO_PASS Check<br/>Did existing tests remain green?"}
    end

    Patch --> Apply
    F2P & P2P --> Score["Deterministic Binary Result: 1.0 or 0.0"]
```

**The Dual-Assertion Verification Paradigm**:
* **`FAIL_TO_PASS`**: Tests that reproduced the initial bug and failed on the unpatched codebase. The agent's patch *must cause these tests to turn green*.
* **`PASS_TO_PASS`**: The comprehensive existing regression suite. All existing tests *must remain 100% green*.

---

## 🔍 Observability, Distributed Tracing & OpenTelemetry [MUST-HAVE] 🔴

When an autonomous agent fails, an error log stating `InternalServerError: Agent failed after 30s` is worse than useless. You need to know the exact tool call that timed out, the prompt at step 4, the token counts, and the distributed span hierarchy.

This is where OpenTelemetry Generative AI Semantic Conventions come in. 

```mermaid
flowchart TD
    Root["Root Trace: POST /api/v1/agent/execute [Span: agent_orchestrator]"]
    
    Root --> Router["Span: intent_router [gen_ai.system: anthropic]"]
    Router --> Plan["Span: planning_decomposition"]
    
    Root --> Step1["Span: agent_step_1 [Turn 1]"]
    Step1 --> LLM1["Span: chat_completion [claude-3-7-sonnet]"]
    Step1 --> Tool1["Span: tool_execution [db_query_customers]"]
    
    Root --> Step2["Span: agent_step_2 [Turn 2]"]
    Step2 --> LLM2["Span: chat_completion [claude-3-7-sonnet]"]
    Step2 --> SubAgent["Span: sub_agent_dispatch [FinancialAnalysisAgent]"]
    SubAgent --> SubLLM["Span: chat_completion [o3-mini]"]
    SubAgent --> Tool2["Span: tool_execution [calculate_depreciation]"]
    
    Root --> Synthesize["Span: final_synthesis [gen_ai.system: anthropic]"]
    
    classDef rootStyle fill:#2d3748,stroke:#4a5568,color:#fff,stroke-width:2px;
    classDef spanStyle fill:#1a365d,stroke:#2b6cb0,color:#fff;
    classDef toolStyle fill:#234e52,stroke:#319795,color:#fff;
    classDef llmStyle fill:#44337a,stroke:#6b46c1,color:#fff;
    
    class Root rootStyle;
    class Router,Plan,Step1,Step2,Synthesize spanStyle;
    class Tool1,Tool2 toolStyle;
    class LLM1,LLM2,SubAgent,SubLLM llmStyle;
```

---

## ⚠️ Production Failure Modes, Biases & Anti-Patterns [MUST-HAVE] 🔴

### Anti-Pattern 1: Position Bias & Verbosity Bias in Pairwise Evaluation
LLM judges systematically favor the candidate presented in position `Option A` over `Option B` (up to 65% win-rate bias). They also heavily equate length with quality, meaning 600 words of superficial text often beats a crisp 50-word accurate answer.

**The Fix**:
* Implement symmetric pairwise swapping: run both `(A, B)` and `(B, A)`.
* Explicitly penalize verbosity in judge instructions.

---

### Anti-Pattern 2: Test Set Contamination & Metric Goodharting
Developers inspect failed evaluation cases, then hardcode specific prompt instructions or few-shot examples that directly address those exact inputs. The system overfits to the evaluation dataset, and generalization in production crashes.

**The Fix**:
* Split evaluation datasets into **Train/Dev** (used for prompt iteration) and **Held-Out Test** (used strictly for release gating, never inspected by developers).

---

## 💻 Production-Grade Code Implementations [MUST-HAVE] 🔴

See [`examples/`](./examples/) for runnable evaluation harnesses and observability test suites.

## 📚 Curated Verified Resources & Seminal Reading [KNOWLEDGE-BASE] 🔵

* **Hamel Husain**: [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)
* **OpenTelemetry**: [Semantic Conventions for Generative AI Systems](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
* **G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment** (Liu et al., 2023)

## 🏆 Capstone Challenge: Automated CI/CD Evaluation Pipeline [MUST-HAVE] 🔴

Build and configure a fully automated, production-grade CI/CD Evaluation Pipeline that runs a **50-test benchmark** against an enterprise customer support agent on every GitHub Pull Request.

👉 **[View the Capstone Challenge](./labs/capstone-cicd-evaluation-pipeline.md)**
