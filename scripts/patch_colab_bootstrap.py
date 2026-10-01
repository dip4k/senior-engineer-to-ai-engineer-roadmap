"""
patch_colab_bootstrap.py
=============================================================================
Patches the Colab & Environment Bootstrap cell across all notebooks in notebooks/
to ensure:
1. Idempotent git clone into /content/repo (avoids 'destination path already exists' errors)
2. Safe %cd /content/repo
3. Resolves dependency conflicts with Colab pre-installed packages (e.g. google-adk opentelemetry pins)
=============================================================================
"""

import json
from pathlib import Path

new_bootstrap_lines = [
    "# %% [Setup] Colab & Environment Bootstrap\n",
    "import os, sys\n",
    "try:\n",
    "    is_colab = 'google.colab' in str(get_ipython())\n",
    "except NameError:\n",
    "    is_colab = False\n",
    "\n",
    "if is_colab:\n",
    "    print('Running in Google Colab.')\n",
    "    repo_dir = '/content/repo'\n",
    "    if not os.path.exists(repo_dir):\n",
    "        print('Cloning repository...')\n",
    "        !git clone --depth 1 https://github.com/dip4k/senior-engineer-to-ai-engineer-roadmap.git /content/repo\n",
    "    %cd /content/repo\n",
    "    !pip install -q --no-warn-conflicts -r agent-forge/requirements.txt -r notebooks/requirements-notebooks.txt\n",
    "    if os.path.abspath('agent-forge') not in sys.path:\n",
    "        sys.path.insert(0, os.path.abspath('agent-forge'))\n",
    "else:\n",
    "    # Local environment setup: locate repo root and agent-forge\n",
    "    repo_root = os.path.abspath('..') if os.path.exists('../agent-forge') else os.path.abspath('.')\n",
    "    af_path = os.path.join(repo_root, 'agent-forge')\n",
    "    if os.path.exists(af_path) and af_path not in sys.path:\n",
    "        sys.path.insert(0, af_path)\n",
    "    print(f'Running locally with agent-forge in path: {af_path}')"
]

notebooks = sorted(list(Path("notebooks").glob("*.ipynb")))
for nb_path in notebooks:
    with open(nb_path, "r", encoding="utf-8") as f:
        nb_data = json.load(f)

    patched = False
    for cell in nb_data["cells"]:
        if cell["cell_type"] == "code" and any("Colab & Environment Bootstrap" in line for line in cell["source"]):
            cell["source"] = new_bootstrap_lines
            patched = True
            break

    if patched:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb_data, f, indent=2)
        print(f"✅ Patched bootstrap in: {nb_path.name}")
    else:
        print(f"⚠️ Bootstrap cell not found in: {nb_path.name}")

print(f"\nAll {len(notebooks)} notebooks checked and patched.")
