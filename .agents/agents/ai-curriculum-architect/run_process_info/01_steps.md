Yes. For **Phase 1**, I recommend a controlled workflow where the agent first understands the entire curriculum, then audits Phase 1, researches current developments, creates a plan, and only then modifies Phase 1.

The key is: **don't ask the agent to “improve Phase 1” in one prompt.**

Use these stages:

```text
                    PHASE 1 REFACTORING
                           │
                           ▼
                  1. Repository Audit
                           │
                           ▼
                    2. Phase 1 Audit
                           │
                           ▼
                 3. Current-State Research
                           │
                           ▼
                4. Refactoring Plan
                           │
                    👤 REVIEW
                           │
                           ▼
                5. Phase 1 Refactoring
                           │
                           ▼
                  6. Self Validation
                           │
                           ▼
                    👤 Review Output
                           │
                           ▼
                 7. Final Validation
                           │
                           ▼
                    Phase 1 Complete
```

# 0. Before starting

Your repository should contain:

```text
.agents/
├── agents/
│   └── ai-curriculum-architect/
│       └── agent.md
│
└── skills/
    └── ai-curriculum-refactoring/
        ├── SKILL.md
        ├── references/
        │   ├── curriculum-principles.md
        │   ├── lesson-template.md
        │   ├── phase-template.md
        │   ├── terminology-guidelines.md
        │   ├── diagram-guidelines.md
        │   ├── research-guidelines.md
        │   └── quality-gates.md
        └── examples/
            └── golden-lesson.md
```

Then open the repository in Antigravity and select:

**AI Curriculum Architect**

---

# 1. Repository-wide audit

Even though you're working on Phase 1, **first let the agent understand the whole curriculum**.

This is important because Phase 1 may introduce concepts that are used later.

### Prompt

Use the `ai-curriculum-refactoring` skill.

Run in **AUDIT MODE**.

Do NOT modify any curriculum content.

Audit the entire repository to understand the complete AI Engineering learning journey.

Inspect:

* root README
* phase directories
* phase READMEs
* lessons
* glossary/reference material
* resources
* diagrams
* internal links

Create:

`CURRICULUM_AUDIT.md`

Analyze:

1. Phase ordering
2. Lesson ordering
3. Prerequisites
4. Cross-phase dependencies
5. Duplicate concepts
6. Concepts introduced too early
7. Concepts missing from prerequisites
8. Overly verbose lessons
9. Terminology problems
10. Unexplained abbreviations
11. Diagram problems
12. Missing explanations
13. Advanced concepts appearing too early
14. Potential outdated content
15. Broken internal links
16. Resource problems

For each phase identify its intended role in the overall curriculum.

Do not rewrite or delete any content.

Stop after completing the audit.

### Expected output

```text
CURRICULUM_AUDIT.md
```

### What you should check

Make sure the agent understands:

```text
Phase 1 → foundation
Phase 2 → RAG / knowledge
Phase 3 → ...
...
```

and doesn't misunderstand the purpose of Phase 1.

---

# 2. Audit Phase 1 deeply

Now focus only on Phase 1.

### Prompt

Use:

* `ai-curriculum-refactoring` skill
* `CURRICULUM_AUDIT.md`

Run in **AUDIT MODE**.

Perform a deep audit of:

`01-*`

Identify the exact Phase 1 directory from the repository structure.

Do not modify existing content.

Analyze every Phase 1 lesson for:

### Learning

* learning objective
* prerequisite knowledge
* conceptual progression
* mental models
* explanation quality
* lesson ordering

### Content

* unnecessary verbosity
* missing concepts
* duplicated concepts
* concepts that belong in later phases
* advanced material introduced too early
* shallow explanations
* overly detailed implementation material

### Terminology

* unexplained AI terminology
* unexplained abbreviations
* terminology introduced without context
* inconsistent terminology

### Diagrams

* unnecessary diagrams
* overly complex diagrams
* diagrams without explanation
* missing diagrams where a visual would materially improve understanding

### Engineering

* practical examples
* trade-offs
* failure modes
* production relevance where appropriate

### Resources

* relevance
* duplication
* outdated resources
* missing authoritative resources

Also identify what should be:

* KEEP
* REWRITE
* REORGANIZE
* SIMPLIFY
* MOVE
* MERGE
* REMOVE

Create:

`01-<phase-name>/PHASE_1_AUDIT.md`

Do not modify the lessons.

---

# 3. Research current Phase 1 topics

Now use the web capability.

This is where the Agent checks whether your Phase 1 is still current.

### Prompt

Use the `ai-curriculum-refactoring` skill.

Run in **RESEARCH MODE**.

Research current developments relevant to the concepts taught in Phase 1.

First inspect the existing Phase 1 content so that research does not duplicate existing material.

Use authoritative and recent sources where possible:

* official documentation
* official specifications
* official repositories
* research papers
* major cloud/provider documentation
* reputable engineering sources

Identify:

1. Important concepts missing from Phase 1
2. Existing concepts that should be updated
3. Concepts that are now outdated
4. Important architectural patterns that should be introduced
5. Emerging topics that are worth mentioning
6. Topics that are only temporary trends and should NOT be added
7. Topics that belong in later phases instead

For every candidate topic provide:

* Topic
* Why it matters
* Current Phase 1 coverage
* Recommended action
* Proposed location
* Prerequisites
* Stability: Durable / Emerging / Rapidly changing
* Recommended sources

Classify each as:

KEEP_EXISTING
UPDATE_EXISTING
NEW_TOPIC
MOVE_TOPIC
ADVANCED_TOPIC
REFERENCE_ONLY
NOT_RELEVANT

Create:

`01-<phase-name>/PHASE_1_RESEARCH.md`

Do not modify curriculum content.

Stop after the research report.

---

# 4. Review the research yourself

This is your **first human approval gate**.

You should now have:

```text
CURRICULUM_AUDIT.md

01-.../
├── PHASE_1_AUDIT.md
└── PHASE_1_RESEARCH.md
```

Look specifically for:

### Good

```text
Existing lesson
      ↓
Agent finds new development
      ↓
Determines it is relevant
      ↓
Suggests UPDATE_EXISTING
```

### Bad

```text
New framework released
      ↓
Agent automatically adds lesson
```

You don't want your roadmap to become a news feed.

---

# 5. Create the Phase 1 refactoring plan

Now tell the agent to combine:

* repository audit
* Phase 1 audit
* research

into one target design.

### Prompt

Use:

* `ai-curriculum-refactoring` skill
* `CURRICULUM_AUDIT.md`
* `PHASE_1_AUDIT.md`
* `PHASE_1_RESEARCH.md`

Run in **PLAN MODE**.

Create:

`01-<phase-name>/PHASE_1_REFACTORING_PLAN.md`

Design the target Phase 1 curriculum.

Define:

1. Phase purpose
2. Target learner outcome
3. Prerequisites
4. Target lesson sequence
5. Concepts introduced by each lesson
6. Dependencies between lessons
7. Lessons to rewrite
8. Lessons to merge
9. Lessons to split
10. Content to move
11. Content to remove
12. New lessons required
13. Existing lessons requiring updates
14. Advanced content placement
15. Research findings to integrate
16. Cross-phase references
17. Resource changes

For every major change explain:

* current problem
* proposed change
* reason
* expected learning benefit

IMPORTANT:

The lesson structure is a DEFAULT STRUCTURE, NOT A RIGID TEMPLATE.

Do not force every lesson to contain every section.

Do not rewrite lessons yet.

---

# 6. Review the plan

This is your **second human approval gate**.

You should now have:

```text
01-<phase-name>/
│
├── PHASE_1_AUDIT.md
├── PHASE_1_RESEARCH.md
└── PHASE_1_REFACTORING_PLAN.md
```

Your plan should look conceptually like:

```text
Phase 1
│
├── Lesson 1
│    └── Foundation
│
├── Lesson 2
│    └── Core AI concept
│
├── Lesson 3
│    └── Mental model
│
├── Lesson 4
│    └── Engineering application
│
└── Lesson 5
     └── Production considerations
```

rather than:

```text
Lesson 1
Lesson 2
Lesson 3
Lesson 4
...
```

with no dependency logic.

---

# 7. Create a Git checkpoint

Before allowing the Agent to modify content:

```bash
git status
git add .
git commit -m "chore: baseline before phase 1 curriculum refactor"
```

This gives you a clean rollback point.

---

# 8. Refactor Phase 1

Now give the Agent permission to modify Phase 1.

### Prompt

Use:

* `ai-curriculum-refactoring` skill
* `CURRICULUM_AUDIT.md`
* `PHASE_1_AUDIT.md`
* `PHASE_1_RESEARCH.md`
* `PHASE_1_REFACTORING_PLAN.md`
* `examples/golden-lesson.md`

Run in **REFACTOR MODE**.

Refactor ONLY the Phase 1 directory.

Do not modify unrelated phases.

Follow the approved refactoring plan.

For each lesson:

* preserve valuable technical knowledge
* improve conceptual progression
* explain the problem before introducing terminology
* introduce mental models before implementation details
* control terminology density
* explain important abbreviations at first use
* simplify unnecessarily complex diagrams
* explain every important diagram
* use realistic engineering examples
* explain trade-offs when relevant
* include failure modes when useful
* include production considerations when relevant

IMPORTANT:

The lesson structure is a DEFAULT STRUCTURE, NOT A RIGID TEMPLATE.

Remove sections that do not add value.

Merge overlapping sections.

Add sections when genuinely required.

Reorder sections when it improves understanding.

Do not create artificial sections.

Do not blindly copy the golden lesson structure.

Use it as a quality reference.

Integrate only the research findings approved by the refactoring plan.

Update Phase 1 README/navigation as required.

Update relevant cross-references.

Do not modify other phases unless a broken reference absolutely requires it.

After completing the refactor, run the skill's quality gates.

Create:

`01-<phase-name>/PHASE_1_REFACTORING_REPORT.md`

---

# 9. Let the Agent self-review

Don't immediately accept the output.

Ask it to perform a **read-only review of what it just produced**.

### Prompt

Use the `ai-curriculum-refactoring` skill.

Run in **VALIDATION MODE**.

Review the completed Phase 1 without modifying files.

Validate every lesson against:

### Learning

* clear objective
* logical progression
* correct prerequisites
* understandable mental model

### Content

* technical depth preserved
* unnecessary verbosity removed
* no significant gaps
* no unnecessary repetition

### Terminology

* important terms explained
* abbreviations introduced properly
* no unnecessary jargon

### Structure

* default lesson structure used appropriately
* no artificial sections
* sections removed when they add no value
* sections added where genuinely required

### Diagrams

* useful
* simple
* correctly explained

### Engineering

* examples are realistic
* trade-offs are clear
* failure modes covered where relevant
* production concerns included where relevant

### Curriculum

* lesson ordering is correct
* no premature concepts
* no inappropriate duplication with later phases
* navigation is correct

### Resources

* links are relevant
* authoritative sources preferred
* no unnecessary resource duplication

Classify findings:

CRITICAL
IMPORTANT
MINOR

Update:

`PHASE_1_REFACTORING_REPORT.md`

Do not modify curriculum content during this validation.

---

# 10. Review the actual lessons

Now **you** review the output.

Don't just read the report.

Open 2–3 representative lessons:

```text
Simple lesson
Complex lesson
Research-updated lesson
```

Check:

### 1. Does it sound human?

You want:

> "An embedding converts text into a numerical representation that captures semantic relationships."

Not:

> "In the rapidly evolving landscape of AI, embeddings represent a groundbreaking paradigm..."

### 2. Does it teach before naming?

Good:

```text
Problem
 ↓
Why keyword search isn't enough
 ↓
Semantic representation
 ↓
Embedding
```

Bad:

```text
Embedding
Vector DB
HNSW
ANN
Cosine similarity
```

all introduced in the first paragraph.

### 3. Is the lesson actually shorter?

You want:

```text
Old:
3000 words of explanation

New:
1700 words
+
better mental model
+
better example
```

Not:

```text
Old:
3000 words

New:
3500 words
but prettier Markdown
```

---

# 11. Fix problems with the Skill, not just Phase 1

Suppose you notice:

> Agent still produces huge "Production Considerations" sections.

Don't simply tell it:

> Make this section shorter.

Update:

```text
references/quality-gates.md
```

or:

```text
references/curriculum-principles.md
```

with a reusable rule.

For example:

```markdown
Production considerations should only be included when they materially
affect the engineering decision being taught.

Do not add generic sections covering security, scalability, cost,
observability, and reliability merely because they are considered
important engineering topics.
```

Then rerun validation.

This improves **all future phases**.

---

# 12. Run final Phase 1 validation

After you've made the necessary fixes:

Use the `ai-curriculum-refactoring` skill.

Run in **FINAL VALIDATION MODE**.

Do not modify any files.

Review Phase 1 as a complete learning experience.

Compare:

* original Phase 1
* Phase 1 audit
* Phase 1 research
* Phase 1 refactoring plan
* current Phase 1
* golden lesson

Validate:

1. Learning progression
2. Prerequisites
3. Concept ordering
4. Technical correctness
5. Terminology
6. Conciseness
7. Technical depth
8. Examples
9. Diagrams
10. Failure modes
11. Production considerations
12. Research integration
13. Resource quality
14. Internal links
15. Cross-phase dependencies
16. Navigation
17. Duplication

Classify remaining findings:

CRITICAL
IMPORTANT
MINOR

Create:

`01-<phase-name>/FINAL_PHASE_1_REVIEW.md`

Do not modify the curriculum.

---

# 13. Commit Phase 1

Once you're satisfied:

```bash
git status
git diff
```

Review the changes.

Then:

```bash
git add 01-<phase-name>
git commit -m "refactor: improve phase 1 AI engineering curriculum"
```

Now Phase 1 becomes your **stable reference implementation**.

---

# Final Phase 1 structure

You'll end up with something like:

```text
01-<phase-name>/
│
├── README.md
│
├── 01-lesson.md
├── 02-lesson.md
├── 03-lesson.md
├── ...
│
├── PHASE_1_AUDIT.md
├── PHASE_1_RESEARCH.md
├── PHASE_1_REFACTORING_PLAN.md
├── PHASE_1_REFACTORING_REPORT.md
└── FINAL_PHASE_1_REVIEW.md
```

I would **not necessarily keep all these reports permanently** in the final public repository. They are useful as agent working artifacts. After the curriculum stabilizes, you can move them into something like:

```text
docs/curriculum-refactoring/
```

or remove them if they're only process artifacts.

---

# The complete operating sequence

For every future phase, you can reuse this:

```text
┌───────────────────────────────┐
│ 1. FULL CURRICULUM AUDIT      │
│    Read-only                  │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 2. PHASE AUDIT                │
│    Read-only                  │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 3. WEB RESEARCH               │
│    Current developments       │
└───────────────┬───────────────┘
                ↓
          👤 REVIEW
                ↓
┌───────────────────────────────┐
│ 4. REFACTORING PLAN           │
│    No content changes         │
└───────────────┬───────────────┘
                ↓
          👤 APPROVE
                ↓
┌───────────────────────────────┐
│ 5. REFACTOR PHASE             │
│    Skill-driven               │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 6. SELF VALIDATION             │
│    Read-only                  │
└───────────────┬───────────────┘
                ↓
          👤 REVIEW
                ↓
┌───────────────────────────────┐
│ 7. FIX + FINAL VALIDATION     │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 8. GIT COMMIT                 │
│    Phase complete             │
└───────────────────────────────┘
```

### One important improvement for your workflow

Once Phase 1 is finished, **don't immediately use it only as the next phase's template**.

Instead, update your Skill's `golden-lesson.md` with the best Phase 1 lesson(s) and keep your existing RAG lesson if it demonstrates a different type of lesson.

That gives the Agent multiple examples:

```text
Golden examples
├── Simple concept lesson
├── Architecture lesson
├── Deep engineering lesson
└── RAG lesson
```

This will help prevent the Agent from turning every phase into the **same Markdown-shaped lesson**, while still maintaining a consistent teaching philosophy.
