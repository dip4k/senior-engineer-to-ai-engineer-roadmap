# Accuracy & Verifiability Policy

Beginners cannot tell a wrong explanation from a right one. Everything the curriculum states must therefore be true, checkable, or clearly labelled as illustrative. This policy is enforced by quality gate 14.

---

## 1. Numbers

Every quantitative claim (latency, bandwidth, memory, cost, recall, speed-up, percentage, price, context size) must be one of:

| Label | How to write it | When to use |
|---|---|---|
| **Sourced** | Figure plus a link to a primary source and an "as of YYYY-MM" date for anything that changes. | Hardware specs, model limits, benchmark results, prices. |
| **Derived** | Show the arithmetic in a `text` block so the learner can reproduce it. | Memory footprints, token budgets, cost estimates. |
| **Illustrative** | Mark inline with *(illustrative)* and keep round orders of magnitude. | Teaching examples where the exact value does not matter. |

Forbidden: a precise-looking number with no label (for example "+12% recall" or "wastes 60–80% of memory") and any number recalled from memory that has not been verified in this session.

## 2. Model, product and version names

- Teach the **concept** first. Name a model only when it adds value.
- Put model names in a table headed `As of YYYY-MM` and link the provider's official model page.
- Before naming any model, API parameter or product feature, verify it with a web search against an official source in the current session. Never rely on memory, because the landscape moves faster than training data.
- Prefer stable families and capabilities ("a reasoning model with an adjustable thinking budget") over version strings in prose.

## 3. Citations and links

- Cite only sources that were actually opened and read. Never invent a paper title, author, year, venue, arXiv number, URL or API field name.
- If a source cannot be verified, omit the claim or list it in the report under **Unverified Claims**.
- Source preference: see [research-guidelines.md](./research-guidelines.md).
- Every relative link must resolve to a real file. Every external link must have been fetched at least once.

## 4. Code

- Every code block must be **executed** before the lesson is reported complete. Record the exact command and the observed output in the report under **Code Verification**.
- Teaching code must run offline with the standard library and Pydantic v2 only (no API keys, no network, no GPU), unless the lesson is explicitly about a live service. In that case, mark the block `# requires: <what>` and describe the expected output.
- Show the expected output directly under the block.
- Keep blocks short (about 60 lines). Split long listings and link to `agent-forge/` for the full implementation.
- Never use pseudo-code in a `python` fence.

## 5. Analogies

Every analogy ends with a one-line **Where this analogy breaks** note. An analogy that is left unqualified becomes a false mental model.

Example: *The Idea Galaxy places similar sentences close together. Where this breaks: real embeddings have hundreds or thousands of dimensions, and "close" is measured by angle, not by eyeballing a 3D map.*

## 6. Claims about how models behave

- State mechanisms only as far as the evidence goes. Use "typically", "in most current models" or "often" for behaviour that varies by model.
- Do not present opinion or folklore (for example "always use temperature 0 for facts") as fact.
- When unsure, say so in the lesson or ask the user. Do not guess.

## 7. Freshness

- Anything labelled "as of" gets re-verified whenever the lesson is touched.
- Research mode owns freshness updates. See [research-guidelines.md](./research-guidelines.md).

## 8. Severity

| Finding | Severity |
|---|---|
| Fabricated citation, URL, API field or model name | 🔴 Critical |
| Code block that fails when run | 🔴 Critical |
| Unlabelled number presented as fact | 🟡 Important |
| Code block never executed | 🟡 Important |
| Analogy missing its "where this breaks" note | 🟡 Important |
| Missing "as of" date on a model table | 🟡 Important |
