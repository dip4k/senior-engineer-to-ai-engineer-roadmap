# Golden Engineering Lesson

> **Purpose:** Demonstrates how to teach an AI engineering problem through failure modes, engineering options, trade-offs, and production decisions.
>
> This example intentionally focuses less on explaining a single technology and more on engineering judgment.
>
> Real lessons must also carry the header block with the term ledger, the canonical tier badge, every number sourced or marked illustrative, and the navigation footer (see [golden-lesson.md](./golden-lesson.md) and [lesson-template.md](../references/lesson-template.md)). Define each AI term in plain English before using it.

<!--
WHAT MAKES THIS LESSON GOLDEN — FOR AGENT AND AUTHOR EYES ONLY

Engineering lessons teach judgment, not just mechanics. Three decisions define this category:

1. FAILURE-MODE-FIRST STRUCTURE (Rule: curriculum-principles.md Rule 3; gate #10)
   The lesson opens with what goes wrong in production before it explains how to fix it.
   Engineers are motivated by pain. "Your RAG system looks fine in dev and breaks in prod"
   is a stronger opening than "Here is how to evaluate a RAG system." Lead with the
   failure, then earn the solution.

2. SYMPTOM → ROOT CAUSE → FIX PATTERN (Rule: quality-gates.md gate #10)
   Every failure mode in this lesson follows a three-part pattern: what the engineer
   observes (symptom), why it happens (root cause), and what to do about it (fix).
   This is the same format as a good incident postmortem. Learners remember this structure
   because they already use it in on-call contexts.

3. PRODUCTION DECISION FRAMING (Rule: curriculum-principles.md Rule 6)
   Every recommendation in this lesson is framed as a decision under constraints: "if
   latency matters more than cost, choose X; if recall matters more, choose Y." There are
   no unconditional best practices. This trains engineers to think like architects rather
   than recipe followers.
-->


# Evaluating a RAG System

## The Problem

A RAG system can appear to work during development.

You ask a few questions.

The system retrieves documents.

The LLM generates reasonable answers.

It is tempting to conclude:

> "The RAG system is working."

But this only tells us that the system produced some acceptable outputs for a few examples.

It does not tell us:

* whether the right documents were retrieved
* whether important information was missed
* whether the answer is supported by the retrieved context
* how performance changes as the knowledge base grows
* whether a change to chunking improves or damages retrieval

For production systems, we need a way to **measure retrieval and answer quality systematically**.

---

# Start by Separating the Pipeline

A RAG system has multiple stages:

```text
Question
   │
   ▼
Retrieval
   │
   ▼
Retrieved Context
   │
   ▼
Generation
   │
   ▼
Final Answer
```

A bad final answer does not necessarily mean the LLM is the problem.

Consider:

```text
Correct document exists
        │
        ▼
Retriever fails to find it
        │
        ▼
LLM receives incomplete context
        │
        ▼
LLM generates weak answer
```

If we only evaluate the final answer, we may incorrectly blame the generation model.

Evaluation should therefore examine the individual stages.

---

# 1. Retrieval Quality

The first question is:

> **Did we retrieve the information needed to answer the question?**

Suppose the expected document is:

```text
Enterprise Refund Policy
```

The retriever returns:

```text
General Refund Policy
Payment FAQ
Cancellation Guide
Product Documentation
```

These documents may look relevant, but the required document was missed.

This is a retrieval failure.

---

## Useful Retrieval Measurements

Depending on the evaluation design, teams may measure concepts such as:

* precision
* recall
* hit rate
* ranking quality

The exact metric depends on what the application considers important.

For example, if missing the correct document is particularly costly, recall may be especially important.

The key idea is:

> **Measure whether the retrieval system finds the information that should have been retrieved.**

---

# 2. Answer Grounding

Retrieving the correct document is not enough.

Suppose the retrieved context says:

> Enterprise customers can request refunds within 30 days.

But the generated answer says:

> Enterprise customers can request refunds within 60 days.

The retrieval succeeded.

The generated answer is still wrong.

This is a generation or grounding problem.

A useful evaluation question is:

> **Is the generated answer supported by the provided context?**

---

# 3. Answer Relevance

An answer can be factually supported but still fail to answer the user's question.

User:

> "How long do I have to request a refund?"

Answer:

> "Our company has several refund policies depending on the product."

This may be related to the topic but does not directly answer the question.

Therefore evaluation should also consider whether the answer addresses the user's request.

---

# A Simple Evaluation Model

Think about quality as multiple dimensions:

```text
                 RAG Quality
                     │
        ┌────────────┼────────────┐
        │            │            │
   Retrieval      Grounding    Relevance
     Quality        Quality      Quality
```

These dimensions answer different questions.

| Dimension | Question                                              |
| --------- | ----------------------------------------------------- |
| Retrieval | Did we find the right information?                    |
| Grounding | Is the answer supported by the retrieved information? |
| Relevance | Does the answer actually address the user's question? |

Do not collapse all three into one vague concept called "accuracy."

---

# Build an Evaluation Dataset

The evaluation process should start with representative questions.

For example:

```text
Question
Expected relevant documents
Expected answer characteristics
Known edge cases
```

A dataset might contain:

| Question                                                   | Expected Information        | Difficulty |
| ---------------------------------------------------------- | --------------------------- | ---------- |
| What is the refund period?                                 | Refund policy               | Easy       |
| What is the enterprise refund process?                     | Enterprise policy           | Medium     |
| Can an enterprise customer get a refund after renewal?     | Renewal + enterprise policy | Hard       |
| What happens when the purchase was made through a partner? | Partner policy              | Hard       |

The important point is that the dataset should represent **real application behavior**, not only easy demonstration questions.

---

# Evaluate Changes Against the Same Dataset

Suppose the team changes the chunking strategy.

Without an evaluation dataset:

```text
Old system → "Looks good"
New system → "Looks good"
```

There is no reliable way to determine whether the change helped.

With an evaluation dataset:

```text
                   Evaluation Set
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
          Old Version         New Version
              │                   │
              └─────────┬─────────┘
                        ▼
                    Compare
```

Now engineering changes can be evaluated against a consistent baseline.

This is the foundation of regression testing for AI systems.

---

# Human Evaluation vs Automated Evaluation

Not every quality dimension is easy to measure automatically.

### Human evaluation

People inspect outputs against defined criteria.

Useful when:

* quality is subjective
* domain expertise is required
* the evaluation dataset is still being developed

### Automated evaluation

Software evaluates outputs using deterministic checks or model-based evaluators.

Useful when:

* evaluations need to run frequently
* regression testing is required
* large numbers of examples must be evaluated

In practice, production AI systems often combine both approaches.

---

# The Engineering Trade-off

A perfect evaluation system can itself become expensive.

Suppose every pull request runs:

```text
1,000 evaluation questions
        ×
multiple model calls
        ×
large context
```

The evaluation pipeline may become slow and expensive.

Therefore evaluation systems themselves need engineering decisions around:

* dataset size
* sampling
* execution frequency
* model selection
* parallelism
* cost
* latency
* failure thresholds

The goal is not to maximize the number of evaluations.

The goal is to create a **reliable feedback loop at an acceptable cost**.

---

# Production Evaluation Loop

A mature workflow might look like:

```text
Change
  │
  ▼
Run Evaluation Dataset
  │
  ├── Retrieval Metrics
  │
  ├── Grounding Metrics
  │
  └── Answer Relevance
          │
          ▼
      Compare Baseline
          │
          ▼
    Accept / Investigate
```

For important applications, this can become part of CI/CD or controlled release workflows.

---

# Common Failure Modes

### "The demo works"

A small number of successful examples does not establish production quality.

### "The LLM gave the right answer"

A correct answer does not prove that the system consistently retrieves correct information.

### "Similarity score is high"

A high similarity score does not necessarily mean the retrieved content is sufficient to answer the question.

### "We changed the prompt and it looks better"

Without a regression dataset, an apparent improvement may actually damage other scenarios.

### "Evaluation says 95%"

A metric is meaningful only when you understand:

* what was measured
* how the dataset was created
* what the threshold means
* what failures are hidden by the aggregate number

---

# Engineering Decision Framework

When introducing evaluation into a RAG system, ask:

### 1. What can fail?

Identify the pipeline stages.

### 2. What does success mean?

Define observable quality criteria.

### 3. What representative scenarios exist?

Build the evaluation dataset.

### 4. Which metrics capture those scenarios?

Select appropriate measurements.

### 5. How frequently should evaluation run?

Balance feedback speed and cost.

### 6. What should block a release?

Define meaningful thresholds rather than arbitrary numbers.

---

# Key Insight

AI evaluation should not be treated as a final testing step added after development.

It should become a **feedback mechanism for engineering decisions**.

```text
Build
  ↓
Evaluate
  ↓
Learn
  ↓
Change
  ↓
Evaluate Again
  ↺
```

This changes AI development from:

> "Does this demo look good?"

to:

> **"Can we measure whether this change improves the system?"**

---

# Key Takeaways

* RAG quality has multiple dimensions.
* Retrieval and generation should be evaluated separately.
* A representative evaluation dataset is essential for regression testing.
* Human and automated evaluation serve different purposes.
* Evaluation itself has cost and latency trade-offs.
* AI evaluation should support engineering decisions, not simply produce a score.
