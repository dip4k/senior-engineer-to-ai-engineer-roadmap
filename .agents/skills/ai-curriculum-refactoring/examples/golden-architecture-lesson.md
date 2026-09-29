# Golden Architecture Lesson

> **Purpose:** Demonstrates how to explain an AI architecture by starting from the problem, identifying responsibilities, showing interactions, and discussing trade-offs.
>
> This is a quality reference, not a mandatory structure.

# Retrieval-Augmented Generation Architecture

## The Problem

Suppose we are building an enterprise support assistant.

The assistant needs to answer questions using company documentation:

* product manuals
* support policies
* internal procedures
* troubleshooting guides

We could place all this information directly into the model prompt.

That approach does not scale well.

The knowledge base may contain thousands or millions of documents, while a user typically needs only a small subset of them for a particular question.

We therefore need a mechanism to **retrieve relevant information before generating the answer**.

This is the basic idea behind Retrieval-Augmented Generation, commonly called **RAG**.

---

## The Core Architecture

A simplified RAG system looks like this:

```text
                 ┌──────────────────┐
                 │   Knowledge Base │
                 └────────┬─────────┘
                          │
                     Ingestion
                          │
                          ▼
                 ┌──────────────────┐
                 │ Document Chunks  │
                 └────────┬─────────┘
                          │
                     Embedding
                          │
                          ▼
                 ┌──────────────────┐
                 │ Search / Vector  │
                 │     Storage      │
                 └──────────────────┘


User Question
      │
      ▼
┌──────────────┐
│ Query        │
│ Processing   │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Retrieval        │
│                  │
│ Relevant chunks  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Prompt Assembly  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│       LLM        │
└────────┬─────────┘
         │
         ▼
      Answer
```

There are two major flows:

1. **Ingestion** — prepare knowledge for retrieval.
2. **Query-time retrieval** — find relevant knowledge and provide it to the model.

Keeping these flows separate is an important architectural concept.

---

## 1. Ingestion Flow

Documents first need to be prepared.

```text
Documents
    ↓
Parsing
    ↓
Cleaning
    ↓
Chunking
    ↓
Embedding
    ↓
Storage
```

### Parsing

The system extracts usable content from source documents.

The source might be:

* PDF
* HTML
* Markdown
* Word documents
* database records
* application APIs

### Chunking

Large documents are divided into smaller pieces.

Why?

Because retrieval normally needs to identify the relevant portion of a document rather than return an entire 100-page document.

Chunking therefore affects retrieval quality.

### Embedding

Each chunk can be converted into a vector representation.

The vector allows the retrieval system to compare semantic relationships between content.

### Storage

The chunks and associated metadata are stored so they can later be retrieved.

Metadata might include:

```text
Document ID
Department
Product
Version
Security classification
Created date
Updated date
```

Metadata becomes important when retrieval needs filtering.

---

# 2. Query-Time Flow

When the user asks a question:

```text
User Question
      ↓
Query Processing
      ↓
Retrieve Candidates
      ↓
Filter / Rank
      ↓
Relevant Context
      ↓
Prompt
      ↓
LLM
      ↓
Answer
```

The important point is that the LLM is not directly searching the entire knowledge base.

The retrieval layer first narrows the available information.

---

## Retrieval Is a Separate Engineering Problem

A common mistake is to think:

> "We added embeddings, so we have RAG."

Embeddings are only one part of retrieval.

A production retrieval pipeline may include:

```text
Query
  │
  ├── Keyword Search
  │
  ├── Semantic Search
  │
  ├── Metadata Filtering
  │
  └── Other Retrieval Strategies
          │
          ▼
     Candidate Results
          │
          ▼
       Reranking
          │
          ▼
   Final Context
```

The appropriate design depends on the application's data and requirements.

---

## Example

Consider the question:

> "What is the refund policy for enterprise customers?"

A simple semantic search might retrieve:

1. General refund policy
2. Enterprise refund policy
3. Product cancellation policy
4. Payment FAQ

The system may then use metadata or reranking to identify the most useful documents.

The final prompt could contain only the relevant information:

```text
System Instructions

User Question:
What is the refund policy for enterprise customers?

Retrieved Context:
[Relevant enterprise refund policy]

Generate an answer using the provided context.
```

The model then generates the response.

---

# Where Things Can Go Wrong

A RAG system can fail even when the LLM itself is working correctly.

### Failure: Poor document parsing

Important content may be lost during extraction.

### Failure: Poor chunking

A concept may be split across chunks, making individual chunks difficult to retrieve.

### Failure: Poor retrieval

The correct document may exist but never reach the model.

### Failure: Too much retrieved context

The model may receive many irrelevant documents.

### Failure: Stale knowledge

The source document may have changed but the retrieval index may still contain the old version.

### Failure: Incorrect generation

The model may produce an answer that is not supported by the retrieved information.

This is why RAG should be treated as a **pipeline**, not a single feature.

---

# Important Architecture Decision

One of the first questions should be:

> **Do we actually need RAG?**

If the required information is structured and deterministic, a normal API or database query may be better.

For example:

```text
"What is order #12345 status?"
```

A deterministic application API is generally more appropriate than semantic retrieval.

Whereas:

```text
"What is the process for handling damaged orders?"
```

may require searching through documentation.

The architecture should therefore be driven by the information-access problem.

---

# Production Considerations

Production RAG systems commonly need to consider:

### Freshness

How quickly must changes to source data become searchable?

### Access control

Should every user be able to retrieve every document?

### Retrieval quality

Are relevant documents consistently retrieved?

### Latency

How much time can retrieval add to the request?

### Cost

How expensive are embedding, storage, retrieval, reranking, and model calls?

### Evaluation

How do we know whether retrieval is actually working?

These concerns should be addressed based on the application's requirements rather than added as generic checklist items.

---

# Key Architectural Insight

RAG is best understood as:

> **A knowledge retrieval architecture that supplies relevant external information to a generative model at runtime.**

It is not:

> "A vector database connected to an LLM."

The vector store is only one possible component of the retrieval architecture.

---

# Key Takeaways

* RAG separates knowledge retrieval from generation.
* The architecture has ingestion and query-time flows.
* Chunking, retrieval, filtering, ranking, and freshness all affect quality.
* Embeddings are useful but are not the complete retrieval solution.
* Deterministic application queries may be better than RAG for structured data.
* Production RAG should be designed as an end-to-end retrieval pipeline.
