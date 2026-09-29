# Phase 01 Reference Implementations: Prompt & Context Engineering

Production reference implementations demonstrating typed Context AST compilation, Anthropic GA prompt caching, deterministic rule engine decoupling, and grammar-constrained JSON decoding with .NET 9 and Python 3.12+.

---

## Reference Implementations

| File | Language | Systems Purpose | Key Architectural Patterns |
|---|---|---|---|
| [`context_pipeline.py`](./context_pipeline.py) | Python 3.12+ | Production Context Pipeline | Anthropic GA Ephemeral Prompt Caching, XML input delimiter sandboxing, Pydantic v2 strict deserialization, cache hit telemetry verification. |
| [`semantic_layer_decoupling.py`](./semantic_layer_decoupling.py) | Python 3.12+ | Deterministic Rule Decoupling | Decoupling canonical ontologies and deterministic rule engines from LLM extraction. Eliminates 85% of token spend and achieves 100% testable execution. |
| [`StrictJsonPipeline.cs`](./StrictJsonPipeline.cs) | C# / .NET 9 | Strict Grammar-Constrained JSON | Standalone console harness using `Azure.AI.OpenAI` / `OpenAI.Chat` with `ChatResponseFormat.CreateJsonSchemaFormat(jsonSchemaIsStrict: true)`. Direct record deserialization without regex stripping. |

---

## Execution Instructions

### Running Python Examples
```bash
# Ensure virtual environment is active and dependencies are installed
pip install pydantic anthropic

# Run Context Pipeline
python examples/context_pipeline.py

# Run Semantic Layer Decoupling Benchmark
python examples/semantic_layer_decoupling.py
```

### Running C# Example
```bash
# Execute standalone .NET 9 console pipeline
dotnet run --project examples/StrictJsonPipeline.cs
```
