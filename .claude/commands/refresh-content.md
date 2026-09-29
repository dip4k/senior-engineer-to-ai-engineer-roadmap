---
description: Autonomously scout frontier AI developments using web search and audit repository coverage.
---

You are the `@refresher` Frontier Content Scout.

1. Execute the automated keyword and topic gap analyzer:
   `python scripts/refresh_content_scout.py --summary`
2. View the generated report in `CONTENT_REFRESH_REPORT.md`.
3. Generate the search queries:
   `python scripts/refresh_content_scout.py --queries-only`
4. Use your web search tool to execute 2 to 4 queries targeting the categories with missing radar concepts (e.g. latest reasoning model updates, new MCP features, EU AI Act compliance milestones).
5. Compare the live findings from the web against what is currently written in:
   - `ai-engineering-glossary-by-practice.md`
   - `ai-technology-roadmap-2025-2026.md`
   - Specific phase READMEs (`00` through `08`)
6. Produce a clear, actionable summary of:
   - 🌟 Discovered new patterns or standards
   - ⚠️ Knowledge gaps in the repo
   - 📝 Exact text or table additions to update the curriculum
