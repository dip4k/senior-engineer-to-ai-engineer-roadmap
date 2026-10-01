"""
test_notebook_execution.py
Tests execution of code cells in the 3 new notebooks with headless matplotlib.
"""

import json
import traceback
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.show = lambda *args, **kwargs: None

notebooks = [
    Path("notebooks/00_token_mechanics_and_kv_cache.ipynb"),
    Path("notebooks/01_prompt_caching_and_budgeting.ipynb"),
    Path("notebooks/02_hybrid_rag_and_rrf_visualizer.ipynb"),
]

for nb_path in notebooks:
    print(f"\n==========================================")
    print(f"Testing execution for: {nb_path.name}")
    print(f"==========================================")
    with open(nb_path, "r", encoding="utf-8") as f:
        nb_data = json.load(f)

    # Simulated environment
    env = {
        "__name__": "__main__",
        "get_ipython": lambda: None,
        "display": lambda x: print(f"[DISPLAY]:\n{x}\n"),
    }

    code_cells = [c for c in nb_data["cells"] if c["cell_type"] == "code"]
    for idx, cell in enumerate(code_cells):
        src = "".join(cell["source"])
        # Skip colab bash lines in local test
        clean_lines = []
        for line in src.split("\n"):
            if line.strip().startswith("!") or line.strip().startswith("%"):
                continue
            clean_lines.append(line)
        clean_src = "\n".join(clean_lines)

        try:
            exec(clean_src, env)
            print(f"  Cell {idx + 1}/{len(code_cells)}: PASS")
        except Exception as e:
            print(f"  Cell {idx + 1}/{len(code_cells)}: FAIL -> {e}")
            traceback.print_exc()
            raise SystemExit(1)

print("\nALL NOTEBOOK CODE CELLS EXECUTED SUCCESSFULLY!")
