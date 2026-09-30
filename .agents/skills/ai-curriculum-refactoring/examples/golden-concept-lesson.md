# Golden Concept Lesson

> **Purpose:** Demonstrates how to teach a foundational AI concept clearly to a software engineer who knows software terms but has never met AI terms.
>
> This is a quality reference, not a mandatory lesson structure. Real lessons must also carry the header block with the term ledger, the canonical tier badge, a "where this analogy breaks" note, a Quick Check and the navigation footer (see [golden-lesson.md](./golden-lesson.md) and [lesson-template.md](../references/lesson-template.md)).

# Tokens and Context

## What Problem Are We Solving?

When working with traditional applications, developers usually think about input in terms of characters, strings, objects, or messages.

LLMs work differently.

Before a model processes text, the text is converted into smaller units called **tokens**.

This matters because LLM usage is affected by the number of tokens in the input and output.

For example, an application might send:

```text
System instructions
        +
Conversation history
        +
Retrieved documents
        +
Current user request
        ↓
      Model
        ↓
      Response
```

All of this contributes to the model's context.

So a seemingly simple user request can become expensive or even exceed the model's context limit when the application sends too much surrounding information.

---

## The Core Idea

A **token** is a unit of text processed by an LLM.

A token is not necessarily:

* one character
* one word
* one sentence

Depending on the tokenizer and language, a token may represent part of a word, a complete word, punctuation, or another piece of text.

Conceptually:

```text
"Understanding AI systems"

        ↓ tokenization

["Understanding", " AI", " systems"]
```

The exact tokenization depends on the model and tokenizer.

The important engineering idea is:

> **LLMs operate on tokens rather than directly processing the original text as humans perceive it.**

---

## Context Is More Than the User's Message

A common mistake is to think of context as:

```text
User message → Model
```

Production AI applications usually provide much more:

```text
                 ┌─ System instructions
                 │
                 ├─ Conversation history
                 │
User request ────┼─ Retrieved knowledge
                 │
                 ├─ Tool results
                 │
                 └─ Other application context
                          │
                          ▼
                        Model
```

The complete input consumes part of the model's available context.

This creates an important design constraint.

More context is **not automatically better**.

Irrelevant or redundant information can increase cost, latency, and noise.

---

## Why This Matters in Application Design

Imagine an AI support application that keeps sending the entire conversation history.

A conversation may start small:

```text
Turn 1 → 500 tokens
Turn 2 → 1,000 tokens
Turn 3 → 1,500 tokens
...
```

As the conversation grows, repeatedly sending all previous messages can become expensive.

The application may eventually need techniques such as:

* summarization
* compaction
* selective history
* retrieval of relevant past information
* context pruning

This is a **context engineering** problem.

---

## Mental Model

Think of the model's context as a limited working area.

```text
┌─────────────────────────────────────────┐
│              Context Window             │
│                                         │
│ System instructions                     │
│ Conversation history                    │
│ Retrieved knowledge                     │
│ Tool results                            │
│ Current request                         │
│                                         │
│              Available space             │
└─────────────────────────────────────────┘
```

The application must decide what deserves space inside that working area.

That decision is often more important than simply increasing the amount of information provided.

---

## Common Mistakes

### Mistake 1: Treating tokens as words

Tokens and words are related but not equivalent.

Never build application logic assuming:

> 1 word = 1 token

Token usage varies with the model, language, and content.

### Mistake 2: Sending everything

More context can introduce:

* unnecessary cost
* higher latency
* irrelevant information
* conflicting instructions
* reduced signal-to-noise ratio

### Mistake 3: Ignoring output tokens

Applications often focus only on input tokens.

Output tokens also contribute to usage and latency.

---

## Engineering Implications

When designing an AI application, token usage should be considered alongside:

* context limits
* latency
* model cost
* conversation length
* retrieval strategy
* prompt size
* output length

This becomes particularly important for agentic applications because a single user request may trigger multiple model calls.

For example:

```text
User Request
    ↓
Planner call
    ↓
Tool call
    ↓
Observation
    ↓
Reasoning call
    ↓
Another tool
    ↓
Final response
```

Token consumption can accumulate across the entire execution.

---

## When Should You Care About Token Optimization?

Token optimization becomes especially important when:

* conversations are long
* agents perform multiple model calls
* large documents are retrieved
* tool results are large
* applications serve many users
* model costs are significant
* latency is important

The goal is not:

> "Use as few tokens as possible."

The goal is:

> **Provide the model with the information it needs, while minimizing unnecessary context.**

---

## Key Takeaways

* LLMs process text as tokens.
* Token usage affects cost and latency.
* Context includes much more than the current user message.
* More context does not automatically produce better results.
* Context management becomes increasingly important in long-running and agentic applications.
* Good AI application design treats context as an engineering resource.
