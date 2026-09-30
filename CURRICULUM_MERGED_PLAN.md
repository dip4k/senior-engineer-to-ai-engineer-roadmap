# Master Curriculum Merged Plan (Audit, Research & Refactoring)

> **Execution Mode**: PLAN MODE
> **Target Audience**: Senior Developers, Staff Software Engineers, and Solutions Architects (7–10+ years experience)
> **Author**: AI Curriculum Architect
> **Date**: September 2026
> **Repository**: `Ai_Native_Engineer`

---

## 🏛️ Executive Summary

Following a comprehensive repository-level audit and frontier web research, this merged plan synthesizes the current state of the curriculum, new industry breakthroughs, and the remaining execution blueprint. 

### Current State (The Good)
1. **Phases 00–07 are Successfully Refactored**: They have been transformed from monolithic README blobs into **47 modular, 4-tier lesson files**.
2. **Zero-LaTeX Standard Enforced**: All math and equations have been successfully converted to GFM text and standard Unicode.
3. **Diagram Walkthrough Coverage**: All Mermaid diagrams in the refactored phases (00-07) now possess explicit, step-by-step prose walkthroughs conforming to Quality Gate 07.
4. **Lab Harmonization**: The repository features 7 verified, production-grade labs.

### Remaining Debt & Deficits
1. **Phase 08 Monolith**: `08-ai-augmented-sdlc-and-leadership` remains a single, massive 11,000+ word unrefactored monolithic file.
2. **Missing 2025-2026 Breakthroughs**: Crucial recent advancements (like the late-2025 MCP architecture expansions and mid-2026 Stateless MCP, DeepSeek R1 reasoning physics) need to be stitched into existing curriculum without disrupting the current modularization.

---

## 🔬 Frontier Research & Curriculum Updates (2025-2026)

Based on live web search and the content refresh radar, the following industry breakthroughs must be integrated into the refactored curriculum:

### 1. Protocols & MCP (Phase 03 Target)
*   **Expansion to Stateless MCP**: The 2026 transition of MCP into a fully stateless protocol to simplify enterprise serverless infrastructure.
*   **Security & Discovery**: November 2025 updates introducing OAuth-based authorization, OpenID Connect Discovery 1.0 for tool servers, and server-initiated "elicitation" features. 
*   **Action**: Update `03-tools-and-model-context-protocol/02-mcp-architecture-and-transports.md` to cover stateless MCP, and `03-abac-policy-and-financial-idempotency.md` to cover OAuth/OIDC Discovery.

### 2. Reasoning Models & Test-Time Compute (Phase 00 & 01 Targets)
*   **DeepSeek R1 & Claude 3.7**: Update context and inference physics to account for modern latent reasoning capabilities and token economics (hidden scratchpads).
*   **Action**: Refresh `00-foundations-and-token-mechanics/04-test-time-compute-and-reasoning-models.md`.

---

## 🗺️ Phase 08 Restructuring Blueprint

The final monolithic phase (`08-ai-augmented-sdlc-and-leadership`) will be decomposed into a Hub and 5 focused, bite-sized lessons strictly adhering to the 4-tier depth taxonomy and the ~1,500-2,500 word limit.

| Lesson File | Title | Depth Tier | Pedagogical Focus |
|---|---|:---:|---|
| `README.md` | Phase 08 Orientation & Hub | Hub | Software 3.0 SDLC lifecycle diagram, prerequisites, and lesson directory. |
| `01-software-30-and-the-karpathy-continuum.md` | Software 3.0 & The Karpathy Continuum | `🟢 Core` | Shift from imperative (1.0) to neural (2.0) to reasoning microservices (3.0). The transition of developer from synthesizer to spec arbiter. |
| `02-agentic-coding-assistants-and-the-trust-gap.md`| Agentic Coding Assistants & The Trust Gap | `🟢 Core` | The Big Seven matrix (Claude Code, Cursor, Windsurf), enterprise Trust Gap, code atrophy, and context limits. |
| `03-machine-readable-codebase-contracts-agent-md.md`| Machine-Readable Contracts (`AGENT.md`) | `🟡 Engineering Depth` | Writing deterministic `AGENT.md` guidelines, repository context hierarchies, token budgets for AI-authored PRs. |
| `04-spec-driven-development-and-pr-automation.md` | Spec-Driven Development (SDD) & Verification | `🟡 Engineering Depth` | Spec-driven code generation, Automated ADR generation, test assertion gates, PR review bot heuristics. |
| `05-ai-architecture-review-board-governance.md` | AI Architecture Review Board (ARB) Governance | `🔵 Advanced` | 10-point production readiness review rubric, technical debt containment, AI governance. |

---

## 🚦 Execution & Validation Plan

1. **Refactor Phase 08**: Execute the Phase 08 restructuring blueprint to eliminate the final monolith in the repository.
2. **Integrate Research**: Weave the 2025/2026 MCP and reasoning updates into Phase 00 and Phase 03 without expanding word counts beyond tier budgets.
3. **Run Final Validation**: Evaluate the entire Phase 00-08 curriculum using the 13-Point Quality Gate (Lens A: AI Learner; Lens B: Systems Architect).
4. **Link Integrity Sweep**: Perform a final pass to ensure all cross-phase prerequisites and anchor tags are valid.

**Status**: Ready for Execution.
