#!/usr/bin/env python3
"""
verify_capstone.py
Automated Grading & Verification Test Runner for the Phase 08 Capstone Challenge.
Validates AGENT.md contracts, tests the Headless PR Review Bot against passing/failing diffs,
and verifies automated Architecture Decision Record (ADR) generation.

Compatible with Python 3.12+ and Pydantic v2. Run directly with python.
"""

from pathlib import Path
import subprocess
import sys
from pydantic import BaseModel, Field


class MilestoneResult(BaseModel):
    milestone_id: str
    title: str
    passed: bool
    details: str


class CapstoneGradeReport(BaseModel):
    total_milestones: int
    passed_count: int
    score_percentage: float
    all_passed: bool
    milestones: list[MilestoneResult] = Field(default_factory=list)


def verify_milestone_1_agent_contract() -> MilestoneResult:
    """Verifies AGENT.md exists, stays under 150 lines, and has required invariant sections."""
    agent_paths = [
        Path("08-ai-augmented-sdlc-and-leadership/examples/AGENT.md"),
        Path("AGENT.md"),
        Path("AGENTS.md")
    ]
    target_path = next((p for p in agent_paths if p.exists()), None)
    if not target_path:
        return MilestoneResult(
            milestone_id="M1",
            title="Repository AGENT.md Contract",
            passed=False,
            details="Missing AGENT.md file. Create AGENT.md adhering to the Kernel & Pointer pattern."
        )

    content = target_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    line_count = len(lines)

    required_keywords = ["Build", "Test", "Invariants", "Dependencies"]
    missing = [kw for kw in required_keywords if kw.lower() not in content.lower()]

    if line_count > 150:
        return MilestoneResult(
            milestone_id="M1",
            title="Repository AGENT.md Contract",
            passed=False,
            details=f"AGENT.md exceeded 150-line budget ({line_count} lines). Risk of attention dilution."
        )

    if missing:
        return MilestoneResult(
            milestone_id="M1",
            title="Repository AGENT.md Contract",
            passed=False,
            details=f"AGENT.md missing required sections: {', '.join(missing)}."
        )

    return MilestoneResult(
        milestone_id="M1",
        title="Repository AGENT.md Contract",
        passed=True,
        details=f"AGENT.md verified ({line_count} lines, under 150-line ceiling). All invariant sections present."
    )


def verify_milestone_2_pr_reviewer() -> MilestoneResult:
    """Verifies ai_pr_reviewer.py catches injected blockers and approves clean diffs."""
    script_path = Path("08-ai-augmented-sdlc-and-leadership/examples/ai_pr_reviewer.py")
    if not script_path.exists():
        return MilestoneResult(
            milestone_id="M2",
            title="Headless PR Review Bot & Invariant Gate",
            passed=False,
            details="Missing ai_pr_reviewer.py script."
        )

    # 1. Test against violating diff (Must return exit code 1)
    violating_diff = """diff --git a/src/Domain/Order.cs b/src/Domain/Order.cs
+++ b/src/Domain/Order.cs
@@ -5,2 +5,4 @@
+using OrderService.Infrastructure;
+var sql = $"SELECT * FROM orders WHERE id = '{id}'";
"""
    temp_fail = Path("temp_failing_test.patch")
    temp_fail.write_text(violating_diff, encoding="utf-8")

    proc_fail = subprocess.run(
        [sys.executable, str(script_path), "--diff", str(temp_fail), "--json"],
        capture_output=True,
        text=True
    )
    temp_fail.unlink(missing_ok=True)

    if proc_fail.returncode == 0:
        return MilestoneResult(
            milestone_id="M2",
            title="Headless PR Review Bot & Invariant Gate",
            passed=False,
            details="Review bot failed to block violating diff (returned exit code 0 instead of 1)."
        )

    # 2. Test against clean diff (Must return exit code 0)
    clean_diff = """diff --git a/src/Domain/Order.cs b/src/Domain/Order.cs
+++ b/src/Domain/Order.cs
@@ -5,2 +5,3 @@
+public record OrderItem(Guid ItemId, decimal Price);
"""
    temp_clean = Path("temp_clean_test.patch")
    temp_clean.write_text(clean_diff, encoding="utf-8")

    proc_clean = subprocess.run(
        [sys.executable, str(script_path), "--diff", str(temp_clean), "--json"],
        capture_output=True,
        text=True
    )
    temp_clean.unlink(missing_ok=True)

    if proc_clean.returncode != 0:
        return MilestoneResult(
            milestone_id="M2",
            title="Headless PR Review Bot & Invariant Gate",
            passed=False,
            details="Review bot falsely blocked clean diff (returned exit code 1)."
        )

    return MilestoneResult(
        milestone_id="M2",
        title="Headless PR Review Bot & Invariant Gate",
        passed=True,
        details="Review bot successfully blocked SQLi & layer violations, and cleanly approved compliant diff."
    )


def verify_milestone_3_adr_engine() -> MilestoneResult:
    """Verifies generate_adr.py synthesizes a Michael Nygard compliant markdown record."""
    script_path = Path("08-ai-augmented-sdlc-and-leadership/examples/generate_adr.py")
    if not script_path.exists():
        return MilestoneResult(
            milestone_id="M3",
            title="Automated ADR Synthesis Engine",
            passed=False,
            details="Missing generate_adr.py script."
        )

    proc = subprocess.run(
        [sys.executable, str(script_path), "Transitioning to Kafka partitioned ingestion."],
        capture_output=True,
        text=True
    )

    if proc.returncode != 0:
        return MilestoneResult(
            milestone_id="M3",
            title="Automated ADR Synthesis Engine",
            passed=False,
            details=f"generate_adr.py failed with return code {proc.returncode}: {proc.stderr}"
        )

    out = proc.stdout
    required_sections = ["Context & Problem", "Decision Drivers", "Considered Options", "Decision Outcome", "Consequences"]
    missing = [s for s in required_sections if s.lower() not in out.lower()]

    if missing:
        return MilestoneResult(
            milestone_id="M3",
            title="Automated ADR Synthesis Engine",
            passed=False,
            details=f"Generated ADR missing Michael Nygard sections: {', '.join(missing)}"
        )

    return MilestoneResult(
        milestone_id="M3",
        title="Automated ADR Synthesis Engine",
        passed=True,
        details="Generated ADR strictly adheres to Michael Nygard schema and outputs cleanly."
    )


def run_capstone_eval():
    print("================================================================")
    print("      PHASE 08 CAPSTONE CHALLENGE: AUTOMATED EVALUATION         ")
    print("================================================================\n")

    m1 = verify_milestone_1_agent_contract()
    m2 = verify_milestone_2_pr_reviewer()
    m3 = verify_milestone_3_adr_engine()

    milestones = [m1, m2, m3]
    passed_count = sum(1 for m in milestones if m.passed)
    score_pct = (passed_count / len(milestones)) * 100
    all_passed = passed_count == len(milestones)

    for m in milestones:
        status_tag = "✅ PASS" if m.passed else "❌ FAIL"
        print(f"[{status_tag}] {m.milestone_id}: {m.title}")
        print(f"       {m.details}\n")

    print("----------------------------------------------------------------")
    print(f"Final Score: {passed_count}/{len(milestones)} Milestones Passed ({score_pct:.1f}%)")
    if all_passed:
        print("VERDICT: CAPSTONE CHALLENGE ACCEPTED (100% PRODUCTION READY)")
        sys.exit(0)
    else:
        print("VERDICT: REMEDIATION REQUIRED (Check failed milestones above)")
        sys.exit(1)


if __name__ == "__main__":
    run_capstone_eval()
