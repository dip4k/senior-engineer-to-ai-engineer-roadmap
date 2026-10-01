"""
nb_helper.py
=============================================================================
Helper utility to programmatically generate clean, valid Jupyter Notebooks (.ipynb)
for the AI-Native Engineer curriculum and companion Colab exercises.
=============================================================================
"""

import json
from pathlib import Path
from typing import List, Optional


class NotebookBuilder:
    def __init__(self, title: str, description: str):
        self.cells: List[dict] = []
        self.add_markdown(f"# {title}\n\n{description}")
        self._add_colab_bootstrap()

    def _add_colab_bootstrap(self):
        bootstrap_code = (
            "# %% [Setup] Colab & Environment Bootstrap\n"
            "import os, sys\n"
            "try:\n"
            "    is_colab = 'google.colab' in str(get_ipython())\n"
            "except NameError:\n"
            "    is_colab = False\n\n"
            "if is_colab:\n"
            "    print('Running in Google Colab.')\n"
            "    repo_dir = '/content/repo'\n"
            "    if not os.path.exists(repo_dir):\n"
            "        print('Cloning repository...')\n"
            "        !git clone --depth 1 https://github.com/dip4k/senior-engineer-to-ai-engineer-roadmap.git /content/repo\n"
            "    %cd /content/repo\n"
            "    !pip install -q --no-warn-conflicts -r agent-forge/requirements.txt -r notebooks/requirements-notebooks.txt\n"
            "    if os.path.abspath('agent-forge') not in sys.path:\n"
            "        sys.path.insert(0, os.path.abspath('agent-forge'))\n"
            "else:\n"
            "    # Local environment setup: locate repo root and agent-forge\n"
            "    repo_root = os.path.abspath('..') if os.path.exists('../agent-forge') else os.path.abspath('.')\n"
            "    af_path = os.path.join(repo_root, 'agent-forge')\n"
            "    if os.path.exists(af_path) and af_path not in sys.path:\n"
            "        sys.path.insert(0, af_path)\n"
            "    print(f'Running locally with agent-forge in path: {af_path}')\n"
        )
        self.add_code(bootstrap_code)

    def add_markdown(self, markdown_text: str):
        lines = [line + "\n" for line in markdown_text.strip().split("\n")]
        # Remove trailing newline from last line to match standard formatting
        if lines:
            lines[-1] = lines[-1].rstrip("\n")
        self.cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": lines
        })

    def add_code(self, code_text: str):
        lines = [line + "\n" for line in code_text.strip().split("\n")]
        if lines:
            lines[-1] = lines[-1].rstrip("\n")
        self.cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": lines
        })

    def save(self, output_path: str | Path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        notebook_data = {
            "cells": self.cells,
            "metadata": {
                "language_info": {
                    "name": "python",
                    "version": "3.12"
                },
                "colab": {
                    "provenance": []
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(notebook_data, f, indent=2)
        print(f"✅ Generated notebook: {output_path} ({len(self.cells)} cells)")


if __name__ == "__main__":
    print("Notebook builder utility ready.")
