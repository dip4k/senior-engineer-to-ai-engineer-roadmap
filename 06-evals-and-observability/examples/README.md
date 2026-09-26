# Phase 06 Examples: Evals & Observability

Production evaluation and observability implementations demonstrating binary LLM-as-a-Judge rubrics with OpenTelemetry/Langfuse, and CI/CD automated regression tests in xUnit.

## Files

| File | Language | Purpose | Key Patterns |
|---|---|---|---|
| [`production_eval_runner.py`](./production_eval_runner.py) | Python 3.11+ | LLM-as-a-Judge with Langfuse | Binary rubrics, G-Eval framework, structured JSON output validation, trace publishing |
| [`EvalHarnessTests.cs`](./EvalHarnessTests.cs) | C# / .NET 9 | xUnit Automated Evaluation Suite | Deterministic assertions, LLM-as-judge assertions, CI/CD pull request gate |
