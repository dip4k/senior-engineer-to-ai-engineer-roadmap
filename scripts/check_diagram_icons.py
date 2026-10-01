import re
from pathlib import Path

ROOT = Path(".")
phases = [
    "00-foundations-and-token-mechanics",
    "01-prompt-and-context-engineering",
    "02-rag-and-knowledge-systems",
    "03-tools-and-model-context-protocol",
    "04-agentic-systems-and-orchestration"
]

UNICODE_EMOJI_PATTERN = re.compile(r"[\U00010000-\U0010ffff\u2600-\u27bf\u2300-\u23ff]")

for ph in phases:
    p = ROOT / ph
    print(f"\n==========================================")
    print(f"=== {ph} ===")
    print(f"==========================================")
    for md in sorted(p.rglob("*.md")):
        if any(part in ("bin", "obj", ".venv", "node_modules") for part in md.parts):
            continue
        text = md.read_text(encoding="utf-8")
        lines = text.splitlines()
        inside = False
        start = 0
        cur = []
        for i, ln in enumerate(lines, 1):
            if ln.strip().startswith("```mermaid"):
                inside = True
                start = i
                cur = []
            elif inside and ln.strip() == "```":
                inside = False
                code = "\n".join(cur)
                if "xychart-beta" in code:
                    continue
                first_line = cur[0].strip() if cur else ""
                node_labels = []
                if first_line.startswith("sequenceDiagram"):
                    participants = re.findall(r'(?:participant|actor)\s+\w+\s+as\s+([^\n]+)', code)
                    for lbl in participants:
                        node_labels.append(lbl.strip())
                elif first_line.startswith("stateDiagram"):
                    state_labels = re.findall(r'state\s+"([^"]+)"\s+as\s+\w+', code)
                    for lbl in state_labels:
                        node_labels.append(lbl.strip())
                else:
                    # Flowchart / graph
                    raw_labels = re.findall(r'\["([^"]+)"\]|\("([^"]+)"\)|\{"([^"]+)"\}|\[\(([^)]+)\)\]|\(\[([^\]]+)\]\)|\[([^\]\n]+)\]', code)
                    for match in raw_labels:
                        lbl = next(m for m in match if m)
                        if lbl.strip() != "*":
                            node_labels.append(lbl.strip())
                
                labels_with_emoji = [l for l in node_labels if UNICODE_EMOJI_PATTERN.search(l)]
                rel_path = md.relative_to(ROOT)
                if len(labels_with_emoji) < len(node_labels):
                    print(f"  MISSING: {rel_path}:{start} ({first_line}) -> {len(labels_with_emoji)}/{len(node_labels)} icons")
                    for missing in [l for l in node_labels if not UNICODE_EMOJI_PATTERN.search(l)]:
                        print(f"    - {missing}")
            elif inside:
                cur.append(ln)

