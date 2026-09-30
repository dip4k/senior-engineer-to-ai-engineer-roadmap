# Report Templates & Locations

Reports are working artifacts for the maintainer. They never live next to learner content.

## Location

```text
.curriculum-reports/
├── CURRICULUM_AUDIT.md                 (repository-wide audit)
├── CURRICULUM_REFACTORING_PLAN.md      (repository-wide plan)
├── CURRICULUM_RESEARCH.md              (repository-wide research)
├── FINAL_CURRICULUM_REVIEW.md          (repository-wide validation)
└── phase-<NN>/
    ├── PHASE_<NN>_AUDIT.md
    ├── PHASE_<NN>_REFACTORING_PLAN.md
    ├── PHASE_<NN>_RESEARCH.md
    ├── REFACTORING_REPORT.md
    └── VALIDATION_REPORT.md
```

Generated reports are **local working artifacts**: the repository `.gitignore` already excludes `*AUDIT*.md`, `*PLAN*.md`, `*RESEARCH*.md`, `*REFACTORING_REPORT*.md`, `*VALIDATION_REPORT*.md` and `CURRICULUM_*.md`. They are for the maintainer to read and are not committed. Copy one elsewhere if you want to keep it.

Every report starts with: date, scope (phase and lessons), mode, and the reference-file versions used (the git commit of `.agents/`).

## Audit report

1. Executive summary (3–5 sentences)
2. Findings table per step of [audit-protocol.md](./audit-protocol.md): file, line, finding, severity, proposed action
3. Term-ledger gaps (AI terms used before they are taught)
4. Prerequisite graph problems
5. Prioritised remediation list and recommended lesson order

## Plan report

1. Target lesson list with tier, split, merge and move decisions
2. Migration map (old file → new file)
3. New lessons to write (for example a Lesson 00 primer) and why
4. Risks and open questions for the user

## Refactoring report (9 sections)

1. **Curriculum Changes**: structural additions, re-orderings, realignments
2. **Content Changes**: concepts rewritten, simplified, clarified
3. **Advanced Content**: engineering depth preserved or added
4. **Diagram Changes**: created, updated, split; node counts
5. **Duplication Removed**: redundant explanations eliminated
6. **Files Changed**: modified, created, deleted (exact paths)
7. **Link Changes**: updated relative paths and navigation anchors
8. **Cross-Phase Changes**: upstream and downstream adjustments
9. **Remaining Recommendations**: follow-ups, lab updates, research items

Add three mandatory appendices:

- **Code Verification**: each code block, the command run, pass or fail, observed output
- **Unverified Claims**: anything omitted or softened because it could not be verified
- **Term Ledger**: terms introduced and terms assumed, per lesson

## Validation report

- Verdict per lesson against the 15-point gate, reviewed through Lens A and Lens B
- Findings grouped as 🔴 Critical (blocks merge), 🟡 Important (requires remediation), 🟢 Minor (polish)
- Residual risks
