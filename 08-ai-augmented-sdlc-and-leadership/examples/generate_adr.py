#!/usr/bin/env python3
"""
generate_adr.py
Automated CLI tool that parses staged git diffs and synthesizes formal
Architectural Decision Records (ADRs) conforming to Michael Nygard template.
"""

import os
import sys
import subprocess
from openai import OpenAI

def get_staged_diff() -> str:
    """Extract git diff of staged files."""
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True, check=True)
    return result.stdout.strip()

def generate_adr(diff: str, problem_context: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""You are a Principal Software Architect.
Analyze the following git diff and problem statement. Generate a formal Architecture Decision Record (ADR)
in Markdown format following this structure:
# ADR-XXX: [Title]
## Status: [Proposed | Accepted]
## Context & Problem Statement
## Decision Drivers
## Considered Options
## Decision Outcome
## Consequences & Trade-offs (Positive / Negative)
## Compliance & Verification

Problem Context:
{problem_context}

Git Diff:
{diff[:8000]}
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content or ""

if __name__ == "__main__":
    staged_diff = get_staged_diff()
    if not staged_diff:
        print("No staged changes found. Run `git add <files>` first.")
        sys.exit(1)
    
    context = sys.argv[1] if len(sys.argv) > 1 else "Refactoring architectural subsystem."
    adr_content = generate_adr(staged_diff, context)
    
    print("\n=== GENERATED ADR ===\n")
    print(adr_content)
