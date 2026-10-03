#!/usr/bin/env python3
"""Mechanical quality-gate linter for the AI Engineering curriculum.

NOTE: For standard single-lesson or phase automated gate validation during REFACTOR and LINT modes,
prefer `scripts/validate_lesson.py`.

This script (`scripts/lint_curriculum.py`) is a deep repository-wide baseline analyzer that additionally
inspects prose sentence lengths, vocabulary inflation, syntax validation, and detailed model name freshness.

Usage:
    python scripts/lint_curriculum.py                  # all phases, summary
    python scripts/lint_curriculum.py --phase 0        # one phase
    python scripts/lint_curriculum.py --detail         # list every finding
    python scripts/lint_curriculum.py --report         # write .curriculum-reports/CURRICULUM_LINT_BASELINE.md
    python scripts/lint_curriculum.py --run            # also execute python code blocks (off by default)
    python scripts/lint_curriculum.py --fail-on critical
"""

from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
import tempfile
import textwrap
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CRITICAL, IMPORTANT, MINOR = "critical", "important", "minor"
SEVERITY_ORDER = {CRITICAL: 0, IMPORTANT: 1, MINOR: 2}

TIERS: dict[str, tuple[int, int]] = {
    "🟢 Core": (800, 1500),
    "🟡 Engineering Depth": (1200, 2500),
    "🔵 Advanced": (1500, 3000),
    "⚫ Deep Dive": (1500, 3000),
}
STUB_WORDS = 500
MAX_NODES = 10
TARGET_NODES = 8
MAX_SEQ_PARTICIPANTS = 5

META_TAGS = re.compile(r"\[MUST-HAVE\]|\[GOOD-TO-KNOW\]|\(Zero-LaTeX\)|\(Pure Markdown\)|\(Refactored\)")
LATEX = re.compile(r"\$\$|\\frac\{|\\text\{|\\begin\{|\\sum\b|\\cdot\b|\\times\b|\\mathbb")
STALE_MODELS = re.compile(
    r"Claude 3(?:\.\d)?|GPT-4o|GPT-4\b|o3-mini|o1-preview|Gemini 1\.5|Gemini 2\.0|Llama-?3(?:\.\d)?", re.I
)
INFLATED_WORDS = re.compile(
    r"\b(utilize|utilizes|utilized|utilizing|"
    r"commence|commences|commenced|commencing|"
    r"ascertain|ascertains|ascertained|"
    r"elucidate|elucidates|elucidated|"
    r"necessitate|necessitates|necessitated|"
    r"subsumed|heretofore|ontological|epistemic|"
    r"synergistic)\b",
    re.I,
)
JARGON_TERMS = re.compile(
    r"\b(probabilistic|autoregressive|stochastic|latent|manifold|parametric|epistemic|orthogonal)\b",
    re.I,
)
MAX_SENTENCE_WORDS = 35
FENCE = re.compile(r"^```(\w*)\s*$")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
NAV_HEADING = re.compile(r"^##\s+.*Navigation", re.I | re.M)


@dataclass
class Finding:
    file: str
    line: int
    severity: str
    rule: str
    message: str


def split_fences(text: str) -> tuple[str, list[tuple[str, str, int]]]:
    """Return (text with code blocks blanked, [(lang, code, start_line)])."""
    out, blocks, cur, lang, start, inside = [], [], [], "", 0, False
    for i, line in enumerate(text.splitlines(), 1):
        m = FENCE.match(line.strip()) if not inside else None
        if not inside and line.strip().startswith("```"):
            inside, lang, start, cur = True, line.strip()[3:].strip(), i, []
            out.append("")
        elif inside and line.strip() == "```":
            blocks.append((lang, "\n".join(cur), start))
            inside = False
            out.append("")
        elif inside:
            cur.append(line)
            out.append("")
        else:
            out.append(line)
    return "\n".join(out), blocks


def prose_word_count(prose: str) -> int:
    body = re.sub(r"<!--.*?-->", "", prose, flags=re.S)
    body = "\n".join(ln for ln in body.splitlines() if not ln.lstrip().startswith("|"))
    return len(body.split())


def flowchart_nodes(code: str) -> int:
    ids: set[str] = set()
    for raw in code.splitlines()[1:]:
        line = raw.strip()
        if not line or line.startswith(("%%", "style ", "classDef", "class ", "linkStyle", "end", "direction", "click ")):
            continue
        if line.startswith("subgraph"):
            continue
        line = re.sub(r'"[^"]*"', '""', line)
        line = re.sub(r"\|[^|]*\|", "", line)
        for part in re.split(r"-\.->|-->|==>|---|~~~|-\.-|--", line):
            m = re.match(r"\s*([A-Za-z_][\w]*)", part)
            if m:
                ids.add(m.group(1))
    return len(ids)


def sequence_participants(code: str) -> int:
    names = set(re.findall(r"^\s*(?:participant|actor)\s+(\w+)", code, re.M))
    for a, b in re.findall(r"^\s*(\w+)\s*[-=]+>>?[+-]?\s*(\w+)\s*:", code, re.M):
        names.update((a, b))
    return len(names)


def check_file(path: Path, run_code: bool) -> tuple[list[Finding], dict]:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="replace")
    prose, blocks = split_fences(text)
    lines = text.splitlines()
    findings: list[Finding] = []
    info: dict = {"file": rel}

    is_lesson = bool(re.match(r"\d\d-", path.name)) and path.parent.parent == ROOT
    is_hub = path.name == "README.md" and path.parent.parent == ROOT
    info["kind"] = "lesson" if is_lesson else "hub" if is_hub else "other"

    def add(line: int, sev: str, rule: str, msg: str) -> None:
        findings.append(Finding(rel, line, sev, rule, msg))

    # --- format hygiene & prose clarity (all files)
    for i, ln in enumerate(prose.splitlines(), 1):
        if META_TAGS.search(ln):
            add(i, CRITICAL, "meta-leak", f"Internal tag in learner text: {META_TAGS.search(ln).group(0)}")
        if LATEX.search(ln):
            add(i, CRITICAL, "latex", f"LaTeX delimiter or command: {LATEX.search(ln).group(0)}")
        m_inf = INFLATED_WORDS.search(ln)
        if m_inf:
            add(i, IMPORTANT, "inflated-vocabulary", f"Inflated academic word '{m_inf.group(0)}' found; replace with plain software equivalent (see terminology-guidelines.md)")
        if not ln.strip().startswith(("#", "|", ">", "<!--")):
            for sent in re.split(r"(?<=[.!?])\s+", ln):
                j_hits = set(w.lower() for w in JARGON_TERMS.findall(sent))
                if len(j_hits) >= 2:
                    add(i, IMPORTANT, "jargon-stacking", f"Academic jargon stacking detected ({', '.join(sorted(j_hits))}) in sentence: '{sent[:60]}...' — simplify using plain software English")
                s_words = re.findall(r"\b\w+\b", sent)
                if len(s_words) > MAX_SENTENCE_WORDS:
                    add(i, MINOR, "run-on-sentence", f"Sentence has {len(s_words)} words (max {MAX_SENTENCE_WORDS}): '{' '.join(s_words[:6])}...' — split into shorter sentences")

    # --- links (all files)
    for i, ln in enumerate(prose.splitlines(), 1):
        for target in LINK.findall(ln):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            tpath = (path.parent / target.split("#")[0]).resolve()
            if not tpath.exists():
                add(i, CRITICAL, "broken-link", f"Relative link does not resolve: {target}")

    # --- code blocks (all files)
    py_blocks = [(c, s) for lang, c, s in blocks if lang in ("python", "py")]
    for code, start in py_blocks:
        code = textwrap.dedent(code)
        try:
            ast.parse(code)
        except SyntaxError as exc:
            add(start, CRITICAL, "code-syntax", f"Python block does not parse: {exc.msg} (line {exc.lineno})")
            continue
        if run_code:
            with tempfile.TemporaryDirectory() as tmp:
                f = Path(tmp) / "block.py"
                f.write_text(code, encoding="utf-8")
                try:
                    r = subprocess.run([sys.executable, str(f)], capture_output=True, text=True, timeout=20, cwd=tmp)
                    if r.returncode != 0:
                        last = (r.stderr.strip().splitlines() or ["non-zero exit"])[-1]
                        add(start, IMPORTANT, "code-run", f"Block failed when run: {last[:120]}")
                except subprocess.TimeoutExpired:
                    add(start, IMPORTANT, "code-run", "Block timed out after 20s")
    if py_blocks and info["kind"] == "lesson" and not any("BaseModel" in c for c, _ in py_blocks):
        add(py_blocks[0][1], IMPORTANT, "code-typing", "Python blocks contain no Pydantic BaseModel (skill requires typed Pydantic v2)")

    # --- diagrams (all files)
    diagram_count = 0
    for lang, code, start in blocks:
        if lang != "mermaid":
            continue
        diagram_count += 1
        head = code.strip().splitlines()[0].strip() if code.strip() else ""
        if head.startswith(("flowchart", "graph")):
            n = flowchart_nodes(code)
            if n > MAX_NODES:
                add(start, IMPORTANT, "diagram-size", f"Diagram has {n} nodes (ceiling {MAX_NODES}, target {TARGET_NODES}); split it")
            for j, ln in enumerate(code.splitlines()):
                if re.match(r"\s*style\s+\w+", ln) and re.search(r"fill:(?!none)", ln):
                    add(start + j + 1, IMPORTANT, "diagram-fill", "Hard-coded fill breaks dark mode; use stroke only (fill:none for subgraphs)")
        elif head.startswith("sequenceDiagram"):
            n = sequence_participants(code)
            if n > MAX_SEQ_PARTICIPANTS:
                add(start, IMPORTANT, "diagram-size", f"Sequence diagram has {n} participants (max {MAX_SEQ_PARTICIPANTS})")
        # walkthrough: a numbered list or 'walkthrough' heading within 30 lines after the fence
        end = start + code.count("\n") + 2
        window = "\n".join(lines[end : end + 30])
        if not (re.search(r"(?m)^\s*1\.\s", window) or re.search(r"walkthrough", window, re.I)):
            add(start, IMPORTANT, "diagram-walkthrough", "No numbered prose walkthrough found directly under the diagram")
    info["diagrams"] = diagram_count

    if not (is_lesson or is_hub):
        return findings, info

    # --- navigation (lessons and hubs)
    if not NAV_HEADING.search(prose):
        add(len(lines), IMPORTANT, "navigation", "Missing '## 🧭 Navigation' footer")

    if is_hub:
        return findings, info

    # --- lesson-only checks
    words = prose_word_count(prose)
    info["words"] = words
    head_text = "\n".join(lines[:14])

    tier_hit = next((t for t in TIERS if t in head_text), None)
    legacy = re.search(r"HIGH ROI|IMPORTANT / NEXT|ADVANCED / SPECIALIZED|REFERENCE / AWARENESS|Tier\s*\d?:", head_text)
    info["tier"] = tier_hit
    if tier_hit is None:
        if legacy:
            add(1, IMPORTANT, "tier", f"Legacy tier label '{legacy.group(0)}'; use one of {', '.join(TIERS)}")
        else:
            add(1, IMPORTANT, "tier", "No tier badge in header block")
    else:
        lo, hi = TIERS[tier_hit]
        if words > hi:
            add(1, IMPORTANT, "word-budget", f"{words} prose words exceeds {tier_hit} budget ({lo}-{hi}); split the lesson")
    if words < STUB_WORDS:
        add(1, MINOR, "stub", f"Only {words} prose words; consider merging")

    if not re.search(r"New AI terms introduced", head_text):
        add(1, IMPORTANT, "term-ledger", "Header lacks 'New AI terms introduced' line")
    if not re.search(r"AI terms assumed from earlier lessons", head_text):
        add(1, IMPORTANT, "term-ledger", "Header lacks 'AI terms assumed from earlier lessons' line")
    if not re.search(r"Read time|Reading Time", head_text, re.I):
        add(1, MINOR, "header", "Header lacks read time")
    if not re.search(r"Core Concept", head_text):
        add(1, IMPORTANT, "core-concept", "Header lacks a 'Core Concept' callout")

    title = next((ln for ln in lines if ln.startswith("# ")), "")
    bare = re.sub(r"\([^)]*\)", "", title)
    acronyms = [w for w in re.findall(r"\b[A-Z]{2,}[A-Z0-9]*\b", bare) if w not in ("AI", "LLM", "LLMs", "ROI")]
    if acronyms:
        add(lines.index(title) + 1 if title in lines else 1, IMPORTANT, "title-acronym", f"Unexpanded acronym in title: {', '.join(acronyms)}")

    if not re.search(r"quick check|clicked", prose, re.I):
        add(len(lines), IMPORTANT, "quick-check", "No Quick Check section")
    if not re.search(r"where this analogy breaks", prose, re.I):
        add(1, MINOR, "analogy-break", "No 'Where this analogy breaks' note")

    if STALE_MODELS.search(prose) and not re.search(r"as of\s+20\d\d", prose, re.I):
        add(1, IMPORTANT, "stale-models", f"Names models ({STALE_MODELS.search(prose).group(0)}) without an 'as of YYYY-MM' date; verify and date them")

    return findings, info


def collect(phase: int | None) -> list[Path]:
    dirs = sorted(d for d in ROOT.iterdir() if d.is_dir() and re.match(r"0[0-8]-", d.name))
    if phase is not None:
        dirs = [d for d in dirs if d.name.startswith(f"{phase:02d}-")]
    files: list[Path] = []
    for d in dirs:
        for p in sorted(d.rglob("*.md")):
            if any(part in ("bin", "obj", "node_modules", ".venv") for part in p.parts):
                continue
            if re.search(r"FINDINGS|AUDIT|_REPORT|VALIDATION", p.name):
                continue  # maintainer reports quote forbidden tags on purpose
            files.append(p)
    return files


def render(all_findings: list[Finding], infos: list[dict], detail: bool) -> str:
    out: list[str] = []
    by_sev = Counter(f.severity for f in all_findings)
    out.append("# Curriculum Lint Baseline")
    out.append("")
    out.append(f"Files checked: {len(infos)}  |  Critical: {by_sev[CRITICAL]}  |  Important: {by_sev[IMPORTANT]}  |  Minor: {by_sev[MINOR]}")
    out.append("")
    out.append("## Findings by rule")
    out.append("")
    out.append("| Rule | Severity | Count | Files |")
    out.append("|---|---|---|---|")
    rules: dict[str, list[Finding]] = defaultdict(list)
    for f in all_findings:
        rules[f.rule].append(f)
    for rule, items in sorted(rules.items(), key=lambda kv: (SEVERITY_ORDER[kv[1][0].severity], -len(kv[1]))):
        out.append(f"| `{rule}` | {items[0].severity} | {len(items)} | {len({i.file for i in items})} |")
    out.append("")
    out.append("## Findings by phase")
    out.append("")
    out.append("| Phase | Lessons | Critical | Important | Minor |")
    out.append("|---|---|---|---|---|")
    phases = sorted({i["file"].split("/")[0] for i in infos})
    for ph in phases:
        ph_f = [f for f in all_findings if f.file.startswith(ph + "/")]
        lessons = sum(1 for i in infos if i["file"].startswith(ph + "/") and i["kind"] == "lesson")
        c = Counter(f.severity for f in ph_f)
        out.append(f"| {ph} | {lessons} | {c[CRITICAL]} | {c[IMPORTANT]} | {c[MINOR]} |")
    out.append("")
    lessons = [i for i in infos if i["kind"] == "lesson"]
    if lessons:
        out.append("## Lessons over budget or without a tier")
        out.append("")
        out.append("| Lesson | Tier | Prose words | Diagrams |")
        out.append("|---|---|---|---|")
        for i in sorted(lessons, key=lambda x: -x.get("words", 0)):
            tier = i.get("tier") or "(none)"
            lo_hi = TIERS.get(i.get("tier") or "", (0, 10**9))
            if i.get("tier") is None or i.get("words", 0) > lo_hi[1]:
                out.append(f"| {i['file']} | {tier} | {i.get('words', 0)} | {i.get('diagrams', 0)} |")
        out.append("")
    if detail:
        out.append("## All findings")
        out.append("")
        for f in sorted(all_findings, key=lambda x: (SEVERITY_ORDER[x.severity], x.file, x.line)):
            out.append(f"- **{f.severity}** `{f.rule}` {f.file}:{f.line}: {f.message}")
        out.append("")
    out.append("Automated checks only. Teaching quality, factual accuracy, analogy quality and term-before-definition ordering need agent validation and human review.")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--phase", type=int, help="Only lint phase N (0-8)")
    ap.add_argument("--detail", action="store_true", help="List every finding")
    ap.add_argument("--report", nargs="?", const=".curriculum-reports/CURRICULUM_LINT_BASELINE.md", help="Write a markdown report")
    ap.add_argument("--run", action="store_true", help="Execute python code blocks (runs repository code)")
    ap.add_argument("--fail-on", choices=[CRITICAL, IMPORTANT, MINOR], help="Exit 1 if findings at or above this severity exist")
    args = ap.parse_args()

    all_findings: list[Finding] = []
    infos: list[dict] = []
    for p in collect(args.phase):
        f, i = check_file(p, args.run)
        all_findings.extend(f)
        infos.append(i)

    text = render(all_findings, infos, args.detail or bool(args.report))
    if args.report:
        target = ROOT / args.report
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text + "\n", encoding="utf-8")
        print(f"Report written to {target.relative_to(ROOT)}")
        print(text.split("## Findings by rule")[0].strip())
    else:
        print(text)

    if args.fail_on:
        limit = SEVERITY_ORDER[args.fail_on]
        if any(SEVERITY_ORDER[f.severity] <= limit for f in all_findings):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
