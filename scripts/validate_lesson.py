"""
validate_lesson.py — Automated Curriculum Lint Gate (LINT mode)

Runs mechanical quality checks on one or all curriculum lesson files.
Call this before any human review step to catch defects a script can find.

Usage:
    python scripts/validate_lesson.py --file path/to/lesson.md
    python scripts/validate_lesson.py --phase 02
    python scripts/validate_lesson.py --all
    python scripts/validate_lesson.py --all --report   # writes LINT_REPORT.md

Exit code: 0 = all pass, 1 = one or more failures.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
PHASE_DIRS = [d for d in sorted(REPO_ROOT.iterdir()) if d.is_dir() and re.match(r"^\d{2}-", d.name)]
REPORTS_DIR = REPO_ROOT / ".curriculum-reports"

# Tier word budgets (prose only — code/diagrams/tables excluded from count)
TIER_BUDGETS: dict[str, tuple[int, int]] = {
    "🟢 Core":              (800,  1500),
    "🟡 Engineering Depth": (1200, 2500),
    "🔵 Advanced":          (1500, 3000),
    "⚫ Deep Dive":          (1500, 3000),
}

VALID_TIER_BADGES = set(TIER_BUDGETS.keys())

# Lessons whose Last verified date is older than this are flagged as RESEARCH candidates
FRESHNESS_DAYS = 180

# LaTeX patterns that must never appear in lesson files
LATEX_PATTERNS = [
    re.compile(r"\$\$"),
    re.compile(r"(?<!\$)\$(?!\$)[^\n]+?\$"),   # inline $...$
    re.compile(r"\\frac\{"),
    re.compile(r"\\text\{"),
    re.compile(r"\\begin\{"),
    re.compile(r"\\end\{"),
]

# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

class Gate:
    def __init__(self, name: str, passed: bool, detail: str = "") -> None:
        self.name = name
        self.passed = passed
        self.detail = detail

    def __repr__(self) -> str:  # noqa: D105
        icon = "✅" if self.passed else "❌"
        return f"{icon} {self.name}" + (f": {self.detail}" if self.detail else "")


class LessonResult:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.gates: list[Gate] = []

    @property
    def passed(self) -> bool:
        return all(g.passed for g in self.gates)

    @property
    def fail_count(self) -> int:
        return sum(1 for g in self.gates if not g.passed)


# ---------------------------------------------------------------------------
# Gate implementations
# ---------------------------------------------------------------------------

def _strip_non_prose(text: str) -> str:
    """Remove fenced code blocks, Mermaid diagrams, and GFM tables before counting words."""
    # Remove fenced code/mermaid blocks
    text = re.sub(r"```[\s\S]*?```", " ", text)
    # Remove HTML comments
    text = re.sub(r"<!--[\s\S]*?-->", " ", text)
    # Remove GFM table rows (lines starting with |)
    text = re.sub(r"^\|.*\|$", " ", text, flags=re.MULTILINE)
    # Remove blockquote markers
    text = re.sub(r"^>+\s*", " ", text, flags=re.MULTILINE)
    return text


def check_tier_badge(content: str) -> Gate:
    """Gate: exactly one valid tier badge must appear in the header block."""
    found = [badge for badge in VALID_TIER_BADGES if badge in content]
    if len(found) == 1:
        return Gate("Tier badge", True, found[0])
    if len(found) == 0:
        return Gate("Tier badge", False, "no valid tier badge found")
    return Gate("Tier badge", False, f"multiple tier badges: {found}")


def check_word_budget(content: str, tier_badge: str | None) -> Gate:
    """Gate: prose word count must be within the declared tier budget."""
    if tier_badge is None:
        return Gate("Word budget", False, "cannot check — no valid tier badge")
    prose = _strip_non_prose(content)
    word_count = len(prose.split())
    lo, hi = TIER_BUDGETS.get(tier_badge, (0, 0))
    if lo <= word_count <= hi:
        return Gate("Word budget", True, f"{word_count} words (budget {lo}–{hi})")
    direction = "over" if word_count > hi else "under"
    return Gate("Word budget", False, f"{word_count} words is {direction} budget {lo}–{hi} for {tier_badge}")


def check_latex(content: str) -> Gate:
    """Gate: no LaTeX math delimiters."""
    # Strip HTML comments first so annotation blocks don't trigger
    clean = re.sub(r"<!--[\s\S]*?-->", "", content)
    for pattern in LATEX_PATTERNS:
        if pattern.search(clean):
            return Gate("Zero-LaTeX", False, f"found pattern {pattern.pattern!r}")
    return Gate("Zero-LaTeX", True)


def check_term_ledger(content: str) -> Gate:
    """Gate: header block must contain both term ledger lines."""
    has_new = bool(re.search(r"\*\*New AI terms introduced\*\*", content))
    has_assumed = bool(re.search(r"\*\*AI terms assumed from earlier lessons\*\*", content))
    if has_new and has_assumed:
        return Gate("Term ledger", True)
    missing = []
    if not has_new:
        missing.append("'New AI terms introduced'")
    if not has_assumed:
        missing.append("'AI terms assumed from earlier lessons'")
    return Gate("Term ledger", False, f"missing: {', '.join(missing)}")


def check_last_verified(content: str) -> Gate:
    """Gate: header must have a Last verified date, and it must not be stale."""
    match = re.search(r"\*\*Last verified\*\*:\s*(\d{4}-\d{2}-\d{2})", content)
    if not match:
        return Gate("Last verified", False, "field missing from header block")
    try:
        verified_date = datetime.strptime(match.group(1), "%Y-%m-%d").date()
    except ValueError:
        return Gate("Last verified", False, f"invalid date format: {match.group(1)}")
    age = (date.today() - verified_date).days
    if age > FRESHNESS_DAYS:
        return Gate(
            "Last verified",
            False,
            f"{match.group(1)} is {age} days old (>{FRESHNESS_DAYS}): flag as RESEARCH candidate",
        )
    return Gate("Last verified", True, f"{match.group(1)} ({age} days ago)")


def check_navigation_footer(content: str) -> Gate:
    """Gate: lesson must end with a Navigation section."""
    if "## 🧭 Navigation" in content:
        return Gate("Navigation footer", True)
    return Gate("Navigation footer", False, "## 🧭 Navigation section not found")


def check_quick_check(content: str) -> Gate:
    """Gate: lesson must contain a Quick Check section."""
    if re.search(r"Quick Check", content, re.IGNORECASE):
        return Gate("Quick Check", True)
    return Gate("Quick Check", False, "no Quick Check section found")


def check_analogy_break_note(content: str) -> Gate:
    """Gate (CRITICAL): every lesson with an analogy must have a 'where this analogy breaks' note."""
    has_analogy = bool(re.search(r"[Aa]nalogy|[Tt]hink of|[Ii]magine", content))
    if not has_analogy:
        return Gate("Analogy break-note", True, "no analogy section detected — skipped")
    has_break = bool(re.search(r"[Ww]here this analogy breaks|[Ww]here the analogy breaks", content))
    if has_break:
        return Gate("Analogy break-note", True)
    return Gate(
        "Analogy break-note",
        False,
        "CRITICAL: analogy found but no 'Where this analogy breaks' note — blocks merge",
    )


# ---------------------------------------------------------------------------
# Per-file runner
# ---------------------------------------------------------------------------

def lint_file(path: Path) -> LessonResult:
    result = LessonResult(path)
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        result.gates.append(Gate("File read", False, str(exc)))
        return result

    tier_gate = check_tier_badge(content)
    tier_badge = None
    for badge in VALID_TIER_BADGES:
        if badge in content:
            tier_badge = badge
            break

    result.gates.extend([
        tier_gate,
        check_word_budget(content, tier_badge),
        check_latex(content),
        check_term_ledger(content),
        check_last_verified(content),
        check_navigation_footer(content),
        check_quick_check(content),
        check_analogy_break_note(content),
    ])
    return result


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def find_lesson_files(phase: str | None = None) -> list[Path]:
    """Return all markdown lesson files (not READMEs) in the target scope."""
    paths: list[Path] = []
    dirs = PHASE_DIRS
    if phase:
        dirs = [d for d in PHASE_DIRS if d.name.startswith(phase.zfill(2) + "-")]
    for d in dirs:
        for md in sorted(d.rglob("*.md")):
            if md.name.lower() == "readme.md":
                continue
            paths.append(md)
    return paths


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_results(results: list[LessonResult]) -> None:
    total = len(results)
    failed = [r for r in results if not r.passed]
    print(f"\n{'='*72}")
    print(f"  CURRICULUM LINT REPORT — {date.today()}")
    print(f"  {total} lessons checked | {len(failed)} with failures")
    print(f"{'='*72}\n")
    for r in results:
        icon = "✅" if r.passed else f"❌ ({r.fail_count} failure(s))"
        print(f"{icon}  {r.path.relative_to(REPO_ROOT)}")
        for g in r.gates:
            if not g.passed:
                print(f"       {g}")
    print()


def write_report(results: list[LessonResult]) -> Path:
    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / "LINT_REPORT.md"
    total = len(results)
    failed_count = sum(1 for r in results if not r.passed)
    lines = [
        f"# Curriculum Lint Report — {date.today()}",
        "",
        f"> {total} lessons checked | **{failed_count} with failures**",
        "",
        "| Lesson | Tier | Word Budget | LaTeX | Term Ledger | Last Verified | Nav Footer | Quick Check | Analogy Break |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        row_parts = [f"`{r.path.relative_to(REPO_ROOT)}`"]
        gate_map = {g.name: g for g in r.gates}
        for name in ("Tier badge", "Word budget", "Zero-LaTeX", "Term ledger", "Last verified", "Navigation footer", "Quick Check", "Analogy break-note"):
            g = gate_map.get(name)
            if g is None:
                row_parts.append("—")
            elif g.passed:
                row_parts.append("✅")
            else:
                row_parts.append(f"❌ {g.detail[:40]}" if g.detail else "❌")
        lines.append("| " + " | ".join(row_parts) + " |")

    lines += ["", "---", "", "## Failures Detail", ""]
    for r in results:
        if not r.passed:
            lines.append(f"### {r.path.relative_to(REPO_ROOT)}")
            for g in r.gates:
                if not g.passed:
                    lines.append(f"- **{g.name}**: {g.detail}")
            lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="AI Curriculum Lesson Lint Gate")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=Path, help="Lint a single lesson file")
    group.add_argument("--phase", type=str, help="Lint all lessons in a phase (e.g. 02)")
    group.add_argument("--all", action="store_true", help="Lint all lessons in every phase")
    parser.add_argument("--report", action="store_true", help="Write LINT_REPORT.md to .curriculum-reports/")
    args = parser.parse_args()

    if args.file:
        files = [args.file.resolve()]
    elif args.phase:
        files = find_lesson_files(phase=args.phase)
    else:
        files = find_lesson_files()

    if not files:
        print("No lesson files found for the given scope.")
        return 1

    results = [lint_file(f) for f in files]
    print_results(results)

    if args.report:
        path = write_report(results)
        print(f"Report written to: {path}")

    return 1 if any(not r.passed for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
