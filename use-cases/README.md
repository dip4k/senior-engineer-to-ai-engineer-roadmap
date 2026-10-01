# Enterprise AI Architectural Use Cases

> **Production reference blueprints for Tech Leads, Senior Engineers, and Architects deploying enterprise-scale generative AI and autonomous agent systems.**

---

## 📑 Use Case Directory

| # | Use Case | Phase Alignment | Core Focus | Link |
|:---:|:---|:---|:---|:---:|
| **01** | **AI-Assisted SDLC & Software 3.0** | `Phase 08` (SDLC) • `Phase 04` (Agents) | Machine-readable repository directives (`AGENT.md`), Skills/Hooks, AST-driven CI/CD review gates, and automated TDD loops. | [Read Blueprint](./use-case-01-ai-assisted-sdlc.md) |
| **02** | **Enterprise AI Clients & SDK Resilience** | `Phase 01` (Context) • `Phase 07` (Serving) | Distributed rate limiting, connection pooling, and exponential backoff with jitter across multi-cloud SDKs. | [Read Blueprint](./use-case-02-enterprise-sdks-resilience.md) |
| **03** | **MCP Tooling, Sandboxing & Deployment** | `Phase 03` (Tools & MCP) • `Phase 05` (Security) | Model Context Protocol JSON-RPC 2.0 standards (AAIF/Linux Foundation), gVisor sandboxing, and Human-in-the-Loop step-up gates. | [Read Blueprint](./use-case-03-mcp-sandboxing-tooling.md) |
| **04** | **Enterprise Failure Modes & Defense** | `Phase 05` (Security) • `Phase 01` (Context) | Mitigating indirect prompt injection, runaway iteration deadlocks, context drift, and unbounded token spend. | [Read Blueprint](./use-case-04-failure-modes-defense.md) |
| **05** | **OpenTelemetry, Evals & LLMOps** | `Phase 06` (Evals & OTel) • `Phase 07` (Serving) | OpenTelemetry GenAI semantic conventions, discrete binary evaluation gates, and cryptographic canary token leakage filters. | [Read Blueprint](./use-case-05-otel-evals-telemetry.md) |
| **06** | **Agent-to-Agent (A2A) & Multi-Agent Swarms** | `Phase 04` (Agents) • `Phase 03` (MCP) | Hierarchical supervisor orchestration vs peer-to-peer swarm handoffs with asynchronous event messaging (Google A2A). | [Read Blueprint](./use-case-06-agent-swarms-a2a.md) |
| **07** | **Copilot Studio & Enterprise PaaS MCP Bridge** | `Phase 02` (Retrieval) • `Phase 03` (MCP) | Bridging Microsoft Copilot Studio & low-code PaaS to serverless Python/.NET MCP servers over SSE with Azure AI Search grounding. | [Read Blueprint](./use-case-07-copilot-studio-and-paas-mcp-bridge.md) |
| **SYS** | **Enterprise AI System Designs** | `All Phases (00–08)` | Comprehensive architectural blueprints with problem statements, architectures, and trade-off matrices. | [Read System Designs](../architecture/enterprise-ai-system-designs.md) |

---

👉 [Back to Senior Transition Guide](../senior-transition-guide.md) | [Back to Master Curriculum](../README.md)

