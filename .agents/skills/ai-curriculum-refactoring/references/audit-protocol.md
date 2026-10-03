# Audit Protocol (10 Steps)

Used in **AUDIT MODE**. Read-only: never modify curriculum files. Output goes to `.curriculum-reports/` using the template in [report-templates.md](./report-templates.md).

Work on one phase at a time. For each step, record findings with file path, line reference and severity (see [quality-gates.md](./quality-gates.md)).

| # | Step | What to inspect | Typical findings |
|---|---|---|---|
| 1 | **Inventory & structure** | List every lesson, lab, example and README in scope. Record word count (prose only, excluding fenced code), diagram count, and whether each has a header block and navigation footer. | Missing files, monolithic README, missing nav footer. |
| 2 | **Learner baseline & term ledger** | Extract every AI-specific term per lesson. Check each is defined in plain English before use and listed in the ledger. | AI term used before it is taught, missing ledger, jargon walls. |
| 3 | **Prerequisites & ordering** | Build the prerequisite graph across phases 00–08. Check that each lesson only relies on earlier material. | Advanced topic before its foundation, circular dependency. |
| 4 | **Overlap & duplication** | Find concepts explained in more than one place. | Same explanation in two phases, duplicated cheat sheets. |
| 5 | **Tier, pacing & length** | Compare each lesson's prose word count and tier badge to the budgets in [lesson-template.md](./lesson-template.md). | Tier badge missing or legacy, lesson over budget, stub lessons. |
| 6 | **Accuracy & freshness** | Apply [accuracy-policy.md](./accuracy-policy.md): unlabelled numbers, unverified model names, invented citations, stale "as of" dates. | Unsourced statistics, outdated model names. |
| 7 | **Diagrams** | Count nodes per diagram, check theme-adaptive styling, walkthrough present, no cluster-to-cluster edges. See [diagram-guidelines.md](./diagram-guidelines.md). | Over 10 nodes, pastel fills, missing walkthrough. |
| 8 | **Code** | Check typing, Pydantic v2, no pseudo-code. **Run every block.** Record pass or fail. | Untyped dicts, broken snippets, never-run code. |
| 9 | **Navigation & links** | Resolve every relative link. Check reciprocal navigation and phase hub directory. | Broken links, one-way navigation. |
| 10 | **Format hygiene & automation** | Run `python scripts/validate_lesson.py --phase <NN>` and `python scripts/lint_curriculum.py --phase <NN>` to check mechanical gates automatically: LaTeX delimiters, meta-directive leaks, heading style, acronym-only titles, GFM validity, word budgets, and link integrity. | `$$` blocks, `[MUST-HAVE]` tags, titles like `# BM25 and HNSW`, broken links. |

## Audit output rules

- Group findings as 🔴 Critical, 🟡 Important, 🟢 Minor.
- Propose one action per finding from the taxonomy (KEEP, REWRITE, REORGANIZE, SIMPLIFY, MOVE, MERGE, REMOVE).
- Finish with a prioritised remediation list and a recommended order of lessons to refactor.
- End the audit with **STOP: present the report and wait for the user.** Do not start planning or editing.
