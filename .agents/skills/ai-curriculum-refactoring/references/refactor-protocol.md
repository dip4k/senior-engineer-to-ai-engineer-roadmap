# Refactoring Protocol (12 Steps)

Used in **REFACTOR MODE**. Applies to one lesson at a time. Start only when the user has approved a plan that names the lesson.

> **Checkpoint A (before step 1)**: confirm the approved plan covers this lesson. If not, stop and ask.

| # | Step | Detail |
|---|---|---|
| 1 | **Confirm scope** | Name the exact files you will touch. Do not edit anything outside that list. |
| 2 | **Load the references** | Read [lesson-template.md](./lesson-template.md), [terminology-guidelines.md](./terminology-guidelines.md) and the golden lesson in `../examples/golden-lesson.md` before writing. |
| 3 | **Build the term list** | Extract every AI term the lesson uses. Sort into: *taught here*, *taught earlier* (link it), *taught later* (defer or replace with a plain description). |
| 4 | **Decide tier, split or merge** | Choose the tier. If the prose would exceed the tier budget, or the lesson teaches two or more major mechanisms, split it. If adjacent stubs share one idea, merge them. |
| 5 | **Write the header block** | Title (plain language, acronym in parentheses), tier, read time, Core Concept, term ledger, prerequisites. |
| 6 | **Open with the problem and mental model** | A concrete scenario, then a plain-English analogy that ends with *Where this analogy breaks*. |
| 7 | **Teach each AI term in order** | Definition → analogy → tiny example → formal name → engineering detail → *what breaks if you skip it*. Use the tripartite block only for the 2–4 core mechanisms. |
| 8 | **Add systems depth and trade-offs** | Keep the original technical depth. Add trade-offs and failure modes. Label every number per [accuracy-policy.md](./accuracy-policy.md). |
| 9 | **Draw diagrams** | Split any flow over 8 nodes. Follow [diagram-guidelines.md](./diagram-guidelines.md). Put a numbered prose walkthrough under each diagram. |
| 10 | **Write and run the code** | Typed Python 3.12+, Pydantic v2, offline. **Run it.** Paste the real output. Fix failures before continuing. |
| 11 | **Add Quick Check and navigation** | A scenario question with a hidden answer, then the reciprocal `## 🧭 Navigation` footer. Update the phase README table and neighbouring lessons' links. |
| 12 | **Validate and report** | Run `python scripts/validate_lesson.py --file <path>` to execute automated gates. Walk the 15-point gate in [quality-gates.md](./quality-gates.md) through both review lenses (focusing on the 6 human-judgment gates). Write the refactoring report. |

> **Checkpoint B (after step 12)**: STOP. Present the report and the `git diff` summary. Do not start the next lesson until the user approves. Never commit or push.

## Preserve, don't delete

- "Do not teach less. Teach better." Move advanced material into a clearly labelled deep-dive section or a separate Deep Dive lesson. Do not silently drop it.
- Record every move, merge, split and removal in the report so the user can audit it.

## When you get stuck

- Fact you cannot verify → omit it, add to **Unverified Claims** in the report.
- Term that needs a prerequisite not yet taught → add a short inline definition with a link, and flag the ordering problem in the report.
- Conflicting guidance → apply [conflict-resolution-checklist.md](./conflict-resolution-checklist.md) and record the decision.
