# Phase 08 Restructuring Plan: AI-Augmented SDLC & Leadership

## 1. Audit Findings
During the audit of the `08-ai-augmented-sdlc-and-leadership` directory, the following structural and editorial issues were identified:
1. **Monolithic Architecture**: The entire phase is housed within a single massive `README.md` (over 1,600 lines, ~99KB). This severely impacts cognitive load and navigability.
2. **Meta-Directive Leaks**: Learner-facing text contains internal quality gate tags and compliance markers, such as `[MUST-HAVE] 🔴` and `[GOOD-TO-KNOW] 🟡 (Tool Comparison)`.
3. **Overloaded Scope**: The document attempts to cover executive mental models, extensive tool comparisons, SDLC end-to-end deep dives, architectural codebase design, testing strategies, and engineering leadership all in one file.
4. **Missing ROI Tiers**: The curriculum lacks proper alignment to the standard Effort vs. ROI Depth tiers, relying instead on ad-hoc tagging.

## 2. Research Discoveries (2025-2026)
Recent web research into the state of Agentic Development reveals:
- **Shift to Agentic SDLC (ASDLC)**: A fundamental transition from "AI-assisted" coding (copilots) to "Agentic Development" where AI agents autonomously plan, execute, and iterate on multi-step tasks.
- **Spec-Driven Development**: The engineering bottleneck has shifted from syntax to system architecture. Success now hinges on "orchestration"—designing clear machine-readable specifications and context planes for agents.
- **Tool Landscape Consolidation**: Multi-tool workflows are standard. **Cursor** dominates as the AI-native daily-driver IDE, **Claude Code** is the premier CLI orchestration agent for deep architectural reasoning, **Windsurf/Devin** focus on asynchronous delegated execution, and **GitHub Copilot** serves as the enterprise baseline utility.
- **Governance and Observability**: With increased autonomy, technical leadership is focused on human-in-the-loop oversight, audit trails, preventing "silent failures," and updating DORA metrics for the AI era.

## 3. Proposed Restructuring Plan
To resolve the monolith, the phase will be decomposed into a standard Orientation Hub (`README.md`) and five dedicated lessons. Each lesson is mapped to an Effort vs ROI tier.

### Target Lesson Breakdown

#### `README.md` (Orientation Hub)
- **Role**: Entry point for Phase 08.
- **Contents**: Phase overview, Master Lesson Navigation Table, learning paths tailored for ICs vs. Tech Leads, and Capstone challenge introduction.

#### `01-ai-native-sdlc-and-mental-model.md`
- **ROI Tier**: `HIGH ROI / CORE`
- **Focus**: The paradigm shift from AI-Assisted to AI-Native (Agentic) SDLC.
- **Key Topics**: The Karpathy Continuum (Software 1.0 -> 3.0), the developer as Verification Arbiter, and the SDLC evolution spectrum.

#### `02-agentic-coding-tools-landscape.md`
- **ROI Tier**: `IMPORTANT / NEXT`
- **Focus**: The 2026 Developer Toolchain.
- **Key Topics**: The Big Seven Matrix (Cursor, Claude Code, Windsurf, Devin, GitHub Copilot, etc.), LSP vs. MCP protocol integration, and optimal multi-tool workflows.

#### `03-architecting-ai-friendly-codebases.md`
- **ROI Tier**: `HIGH ROI / CORE`
- **Focus**: Designing systems that autonomous agents can reason about.
- **Key Topics**: Explicit typing, modular boundaries, machine-readable contracts (OpenAPI/Protobuf), and implementing `AGENT.md` context hierarchies.

#### `04-ai-augmented-tdd-and-verification.md`
- **ROI Tier**: `HIGH ROI / CORE`
- **Focus**: Overcoming the "Trust Gap" and ensuring code safety.
- **Key Topics**: AI-driven Red-Green-Refactor loops, automated PR review agents, CI invariants, and AI-augmented Incident Response (RCA).

#### `05-engineering-leadership-in-ai-era.md`
- **ROI Tier**: `ADVANCED / SPECIALIZED`
- **Focus**: Leading teams through the Software 3.0 transition.
- **Key Topics**: Adapting DORA metrics for probabilistic code generation, solving the Junior Developer Apprenticeship Dilemma, and enterprise technical governance.
