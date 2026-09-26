# Phase 01 Examples: Prompt & Context Engineering

Production reference implementations demonstrating context window isolation, Anthropic prompt caching, and strongly typed structured outputs with Pydantic and Semantic Kernel.

## Files

| File | Language | Purpose | Key Patterns |
|---|---|---|---|
| [`context_pipeline.py`](./context_pipeline.py) | Python 3.11+ | Production Context Pipeline | Pydantic v2 validation, Anthropic 5-min ephemeral prompt caching, token bounding |
| [`StrictJsonPipeline.cs`](./StrictJsonPipeline.cs) | C# / .NET 9 | Strict JSON Schema Pipeline | Azure OpenAI, Semantic Kernel, JSON schema validation, retry loop |
