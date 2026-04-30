# -*- coding: utf-8 -*-
"""Scan QLC+ source and emit QLC_ENGINE_REFERENCE.md."""
from __future__ import annotations
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "qlcplus-QLC-_5.2.1 Source Code"
OUT = ROOT / "_docs" / "QLC_ENGINE_REFERENCE.md"
ENUM_BLOCK = re.compile(
    r"(?:enum\s+class\s+(\w+)|enum\s+(\w+))\s*(?::\s*\w+)?\s*\{([^}]+)\}",
    re.MULTILINE | re.DOTALL,
)
ENUM_ITEM = re.compile(r"^\s*(\w+)\s*(?:=\s*[^,}]+)?\s*,?\s*$", re.MULTILINE)
LOAD_XML = re.compile(r"\b(bool|void)\s+(\w+)\s*::\s*loadXML\s*\([^)]*\)", re.MULTILINE)
HARDCODED = [
    (r"m_elapsedBeats\s*\+=\s*1000", "ChaserRunner beat tick +1000 millibeats"),
    (r"applyFunctionsTime", "VCSpeedDial applyFunctionsTime"),
]

def _scan_enums():
    found = {}
    if not SRC.is_dir():
        return found
    for h in SRC.rglob("*.h"):
        if "test" in h.parts:
            continue
        try:
            text = h.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in ENUM_BLOCK.finditer(text):
            name = m.group(1) or m.group(2) or "anon"
            body = m.group(3)
            items = [x.group(1) for x in ENUM_ITEM.finditer(body)]
            if items and len(items) <= 40:
                key = f"{h.relative_to(SRC).as_posix()}::{name}"
                found[key] = items[:40]
    return dict(sorted(found.items()))

def _scan_loadxml():
    rows = []
    if not SRC.is_dir():
        return rows
    for cpp in SRC.rglob("*.cpp"):
        if "test" in cpp.parts:
            continue
        try:
            text = cpp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in LOAD_XML.finditer(text):
            rows.append((cpp.relative_to(SRC).as_posix(), m.group(2)))
    return sorted(set(rows))[:200]

def _scan_hardcoded():
    hits = defaultdict(list)
    if not SRC.is_dir():
        return hits
    for pat, desc in HARDCODED:
        rx = re.compile(pat)
        for cpp in SRC.rglob("*.cpp"):
            if "test" in cpp.parts:
                continue
            try:
                lines = cpp.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            for i, line in enumerate(lines, 1):
                if rx.search(line):
                    hits[desc].append(f"{cpp.relative_to(SRC).as_posix()}:{i}")
    return hits

def build_markdown():
    lines = [
        "# QLC+ 5.2.1 Engine Reference (auto-generated)",
        "",
        f"Generated from `{SRC.name}/`.",
        "",
        "## SpeedDial Visibility (project)",
        "| Bit | Value | Element |",
        "|-----|-------|---------|",
        "| 0 | 1 | PlusMinus |",
        "| 1 | 2 | Dial |",
        "| 2 | 4 | Tap |",
        "| 6 | 64 | Milliseconds |",
        "| 7 | 128 | Multipliers |",
        "| 8 | 256 | Apply |",
        "| 9 | 512 | Beats |",
        "",
        "## Beat chaser",
        "- `m_elapsedBeats += 1000` per beat tick; sub-beat step holds unreliable for Tempo=Beats.",
        "",
        "## Enums (sample)",
        "",
    ]
    for key, items in list(_scan_enums().items())[:80]:
        lines.append(f"### `{key}`")
        lines.append(", ".join(items[:25]))
        lines.append("")
    lines.append("## loadXML (sample)")
    for path, name in _scan_loadxml()[:120]:
        lines.append(f"- `{path}` -> `{name}`")
    lines.append("")
    lines.append("## Pattern hits")
    for desc, locs in _scan_hardcoded().items():
        lines.append(f"### {desc}")
        for loc in locs[:15]:
            lines.append(f"- `{loc}`")
        lines.append("")
    lines.append("Regenerate: `python _generate_engine_ref.py`")
    lines.append("")
    return "\n".join(lines)

def main():
    OUT.write_text(build_markdown(), encoding="utf-8")
    print("OK:", OUT.name)

if __name__ == "__main__":
    main()
