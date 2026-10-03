# Scripts Directory Guide

This directory contains automated harnesses, quality assurance linters, notebook generators, and content freshness scouts for the **AI-Native Engineer** repository.

---

## 🛠️ Verification & Quality Assurance Linters

### `validate_lesson.py` (Standard Lesson Gate Linter)
- **Purpose**: Fast, automated check of mechanical quality gates for individual lessons or entire phases during **REFACTOR** and **LINT** modes.
- **Checks**:
  - Valid canonical tier badge (`🟢 Core`, `🟡 Engineering Depth`, `🔵 Advanced`, `⚫ Deep Dive`)
  - Prose word budget compliance
  - Zero-LaTeX delimiters (`$$`, `\frac`, etc.)
  - Mandatory term ledger format
  - `Last verified: YYYY-MM-DD` date freshness (warns if > 180 days old)
  - Navigation footer and Quick Check presence
  - Analogy break-note existence (Critical gate)
- **Usage**:
  ```bash
  # Lint a single lesson file
  python scripts/validate_lesson.py --file 00-foundations-and-token-mechanics/01-tokenization-and-bpe-mechanics.md

  # Lint all lessons in Phase 02
  python scripts/validate_lesson.py --phase 02

  # Lint entire curriculum and generate markdown report in .curriculum-reports/LINT_REPORT.md
  python scripts/validate_lesson.py --all --report
  ```

---

### `lint_curriculum.py` (Deep Baseline Analyzer)
- **Purpose**: Deep repository-wide quality-gate analyzer that inspects prose sentence lengths, vocabulary inflation, syntax validation, and model name freshness.
- **Usage**:
  ```bash
  python scripts/lint_curriculum.py
  python scripts/lint_curriculum.py --phase 0 --detail
  python scripts/lint_curriculum.py --report
  ```

---

### `check_diagram_icons.py` (Mermaid Styling Linter)
- **Purpose**: Scans all Mermaid diagrams across the curriculum to ensure compliance with diagram guidelines: theme-adaptive palettes, no FontAwesome icons (`fa:fa-...`), transparent subgraph backgrounds (`fill:none`), and clean Unicode structural icons.
- **Usage**:
  ```bash
  python scripts/check_diagram_icons.py
  ```

---

## 🧪 Lab & Capstone Verification Suites

### `verify_lab.py` (Labs 01–07 Automated Evaluator)
- **Purpose**: Runs automated unit and integration tests against all student lab implementations.
- **Usage**:
  ```bash
  # Run all lab tests
  python scripts/verify_lab.py --all

  # Verify a single lab (1 to 7)
  python scripts/verify_lab.py --lab 1
  ```

---

### `verify_phase_07_capstone.py` (Phase 07 vLLM & Serving Benchmark)
- **Purpose**: Automated evaluation suite specifically validating Phase 07 continuous batching, streaming token-bucket rate limiter, and model routing components.
- **Usage**:
  ```bash
  python scripts/verify_phase_07_capstone.py
  ```

---

## 📡 Content Freshness & Scouts

### `refresh_content_scout.py` (Frontier AI Gap Analyzer)
- **Purpose**: Automated scout that analyzes the current repository content against frontier industry topics (reasoning models, speculative decoding, MCP standards, modern serving frameworks) and identifies curriculum gaps.
- **Usage**:
  ```bash
  # Print gap analysis summary
  python scripts/refresh_content_scout.py --summary

  # Detailed breakdown
  python scripts/refresh_content_scout.py
  ```

---

## 📓 Companion Notebook Builders & Utilities

- **`build_companion_notebooks.py`**: Compiles companion Jupyter notebooks from curriculum lesson code blocks.
- **`generate_foundations_rag_notebooks.py`**: Generates interactive runnable Colab notebooks for Phases 00 and 02.
- **`generate_nb_06.py` / `generate_nb_07.py`**: Generates dedicated notebooks for evaluation and serving benchmarks.
- **`generate_nb_rag_full_flow.py`**: Generates the end-to-end multi-tenant RAG workflow notebook.
- **`patch_colab_bootstrap.py`**: Adds Google Colab environment setup cells and dependency installers.
- **`test_notebook_execution.py`**: Headless notebook runner validating that all `.ipynb` files execute without errors.
- **`nb_helper.py`**: Shared helper module for AST parsing and code cell formatting in notebooks.
