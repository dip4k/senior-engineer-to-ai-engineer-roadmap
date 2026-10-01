#!/usr/bin/env python3
"""
ai_pr_reviewer.py
Automated Headless PR Review Bot & Invariant Gate.
Enforces Builder-Validator Chain, catches OWASP vulnerabilities, hexagonal layer
breaches, and banned dependencies before pull request merge.

Compatible with Python 3.12+ and Pydantic v2. Run directly with python.
"""

import argparse
from enum import Enum
import json
from pathlib import Path
import re
import sys
from pydantic import BaseModel, Field


class FindingSeverity(str, Enum):
    BLOCKER = "BLOCKER"
    WARNING = "WARNING"
    NIT = "NIT"


class ReviewFinding(BaseModel):
    file_path: str
    line_number: int
    severity: FindingSeverity
    category: str
    rule_id: str
    description: str
    suggested_fix: str


class PRReviewSummary(BaseModel):
    total_findings: int
    blockers_count: int
    warnings_count: int
    nits_count: int
    verdict: str
    findings: list[ReviewFinding] = Field(default_factory=list)


def parse_diff_lines(diff_text: str) -> list[ReviewFinding]:
    """Inspects unified git diff for architectural and security invariants."""
    findings: list[ReviewFinding] = []
    current_file = ""
    current_line_num = 0

    for raw_line in diff_text.splitlines():
        # Track file name from diff header
        if raw_line.startswith("+++ b/"):
            current_file = raw_line.replace("+++ b/", "").strip()
            continue
        elif raw_line.startswith("@@ "):
            # Parse target line number from @@ -A,B +C,D @@
            match = re.search(r"\+(\d+)", raw_line)
            if match:
                current_line_num = int(match.group(1)) - 1
            continue

        if not raw_line.startswith("+") or raw_line.startswith("+++"):
            if not raw_line.startswith("-"):
                current_line_num += 1
            continue

        current_line_num += 1
        added_content = raw_line[1:].strip()

        # Rule 1: Secret detection (Hardcoded API keys / tokens)
        secret_patterns = [
            (r"sk_live_[a-zA-Z0-9]{20,}", "Stripe / OpenAI Live Secret Key"),
            (r"ghp_[a-zA-Z0-9]{30,}", "GitHub Personal Access Token"),
            (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
        ]
        for pattern, desc in secret_patterns:
            if re.search(pattern, added_content):
                findings.append(ReviewFinding(
                    file_path=current_file,
                    line_number=current_line_num,
                    severity=FindingSeverity.BLOCKER,
                    category="Security / Secret Leak",
                    rule_id="SEC-001",
                    description=f"Hardcoded credential detected: {desc}.",
                    suggested_fix="Inject credential at runtime via environment variables or secret manager."
                ))

        # Rule 2: SQL Injection / Unparameterized Query
        if re.search(r"SELECT\s+.*FROM\s+", added_content, re.IGNORECASE):
            if re.search(r"f[\"'].*\{.*\}[\"']", added_content) or re.search(r"\$[\"'].*\{.*\}[\"']", added_content):
                findings.append(ReviewFinding(
                    file_path=current_file,
                    line_number=current_line_num,
                    severity=FindingSeverity.BLOCKER,
                    category="Security / SQL Injection",
                    rule_id="SEC-002",
                    description="Raw interpolated SQL string detected in query handler.",
                    suggested_fix="Use parameterized SQL queries or compiled ORM criteria."
                ))

        # Rule 3: Hexagonal Layer Boundary Breach
        if "domain" in current_file.lower():
            banned_domain_imports = [
                ("infrastructure", "Domain layer cannot reference Infrastructure components"),
                ("entityframeworkcore", "Domain layer cannot reference Entity Framework Core packages"),
                ("sqlalchemy", "Domain layer cannot reference SQLAlchemy ORM packages"),
                ("api", "Domain layer cannot reference API presentation layer"),
            ]
            for banned_sub, reason in banned_domain_imports:
                if banned_sub in added_content.lower() and ("import " in added_content.lower() or "using " in added_content.lower()):
                    findings.append(ReviewFinding(
                        file_path=current_file,
                        line_number=current_line_num,
                        severity=FindingSeverity.BLOCKER,
                        category="Architecture / Hexagonal Boundary",
                        rule_id="ARCH-001",
                        description=f"Hexagonal boundary violation: {reason}.",
                        suggested_fix="Extract an abstract port interface into the Domain contracts namespace."
                    ))

        # Rule 4: Banned Dependency Enforcement (per AGENT.md)
        banned_libs = [
            ("newtonsoft.json", "Newtonsoft.Json is banned. Use System.Text.Json with native AOT."),
            ("automapper", "AutoMapper is banned. Use explicit extension methods or Mapperly."),
        ]
        for banned_pkg, reason in banned_libs:
            if banned_pkg in added_content.lower() and ("packageReference" in added_content or "using " in added_content):
                findings.append(ReviewFinding(
                    file_path=current_file,
                    line_number=current_line_num,
                    severity=FindingSeverity.BLOCKER,
                    category="Governance / Banned Dependency",
                    rule_id="GOV-001",
                    description=f"Prohibited dependency introduced: {reason}",
                    suggested_fix="Remove dependency and adopt approved enterprise tooling."
                ))

    return findings


def evaluate_diff(diff_text: str) -> PRReviewSummary:
    """Evaluates diff and produces structured summary report."""
    findings = parse_diff_lines(diff_text)
    blockers = sum(1 for f in findings if f.severity == FindingSeverity.BLOCKER)
    warnings = sum(1 for f in findings if f.severity == FindingSeverity.WARNING)
    nits = sum(1 for f in findings if f.severity == FindingSeverity.NIT)

    verdict = "MERGE BLOCKED (Blockers Detected)" if blockers > 0 else "APPROVED FOR HUMAN ARBITRATION"

    return PRReviewSummary(
        total_findings=len(findings),
        blockers_count=blockers,
        warnings_count=warnings,
        nits_count=nits,
        verdict=verdict,
        findings=findings
    )


def main():
    parser = argparse.ArgumentParser(description="AI PR Reviewer & Invariant Gate")
    parser.add_argument("--diff", type=str, help="Path to unified diff patch file")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()

    if args.diff and Path(args.diff).exists():
        diff_text = Path(args.diff).read_text(encoding="utf-8")
    else:
        # Fallback sample diff containing real architectural & security violations
        diff_text = """diff --git a/src/OrderService.Domain/Order.cs b/src/OrderService.Domain/Order.cs
--- a/src/OrderService.Domain/Order.cs
+++ b/src/OrderService.Domain/Order.cs
@@ -10,4 +10,6 @@ namespace OrderService.Domain;
+using Microsoft.EntityFrameworkCore;
+using OrderService.Infrastructure;
+var apiKey = "sk_live_99410294102941024abcdef";
+var query = $"SELECT * FROM orders WHERE id = '{orderId}'";
"""
        if not args.json:
            print("Notice: No diff file provided. Running self-test against verified sample diff.")

    summary = evaluate_diff(diff_text)

    if args.json:
        print(summary.model_dump_json(indent=2))
    else:
        print("\n========================================================")
        print("             AI PR REVIEW BOT: INVARIANT REPORT         ")
        print("========================================================")
        print(f"Verdict:   {summary.verdict}")
        print(f"Blockers:  {summary.blockers_count}")
        print(f"Warnings:  {summary.warnings_count}")
        print(f"Nits:      {summary.nits_count}")
        print("--------------------------------------------------------")

        for idx, f in enumerate(summary.findings, start=1):
            print(f"[{idx}] {f.severity.value} ({f.rule_id}) - {f.category}")
            print(f"    Location: {f.file_path}:{f.line_number}")
            print(f"    Issue:    {f.description}")
            print(f"    Remedy:   {f.suggested_fix}\n")

    # Exit code 1 if blockers detected to fail CI gate
    if summary.blockers_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
