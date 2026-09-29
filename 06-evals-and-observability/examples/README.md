# Phase 06 Examples: Evals & Observability

Production evaluation and observability implementations demonstrating binary LLM-as-a-Judge rubrics with OpenTelemetry/Langfuse, and CI/CD automated regression tests in xUnit.

## Files

| File | Language | Purpose | Key Patterns |
|---|---|---|---|
| [`production_eval_runner.py`](./production_eval_runner.py) | Python 3.12+ | LLM-as-a-Judge with Langfuse | Binary rubrics, G-Eval framework, Pydantic v2 structured output validation, trace publishing |
| [`EvalHarnessTests.cs`](./EvalHarnessTests.cs) | C# / .NET 9 | xUnit Automated Evaluation Suite | Deterministic assertions, semantic embedding similarity, CI/CD pull request gate |

## Cross-Lesson References
- **[Lesson 01: Evaluation Hierarchy & Deterministic Testing](../01-evaluation-hierarchy-and-deterministic-testing.md)**
- **[Lesson 02: Model-Based Evaluations & Judge Architectures](../02-model-based-evaluations-and-judge-architectures.md)**
- **[Lesson 05: OpenTelemetry Distributed Tracing & Agent Spans](../05-opentelemetry-distributed-tracing-and-agent-spans.md)**
- **[Capstone Challenge: Automated CI/CD Evaluation Pipeline](../labs/capstone-cicd-evaluation-pipeline.md)**
