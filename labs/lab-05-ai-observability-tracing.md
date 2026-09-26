# Lab 5: AI Observability & Tracing

[🔙 Back to Module 06: Evals & Observability](../06-evals-and-observability/README.md)

## Objective
Implement full distributed tracing for an AI application using OpenTelemetry conventions.

## Architectural Requirements
1. Instrument LLM API calls with OpenTelemetry spans matching GenAI semantic conventions.
2. Record prompt tokens, completion tokens, model name, and temperature as span attributes.
3. Create parent-child spans linking HTTP incoming requests, vector search queries, and model invocations.
4. Export trace data to a local collector, Langfuse instance, or Jaeger dashboard.

## Verification Criteria
Complete trace waterfall displays latency breakdown across retrieval, prompt processing, and token generation.
