# -*- coding: utf-8 -*-
"""Soft-fade clones3100-3155 of key ring chasers (1750-1757, 1770-1777, 2850-2889)."""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import (
    extract_function_block,
    inject_before_monitor,
    load_qxw,
    make_soft_chaser,
    save_qxw,
    strip_functions,
)

NEW_IDS = list(range(3100, 3156))
SOURCES = (
    list(range(1750, 1758))
    + list(range(1770, 1778))
    + list(range(2850, 2890))
)


def main() -> None:
    if len(SOURCES) != len(NEW_IDS):
        raise SystemExit("SOURCES and NEW_IDS length mismatch")
    text = strip_functions(load_qxw(), set(NEW_IDS))
    blocks: list[str] = []
    for src, nid in zip(SOURCES, NEW_IDS):
        raw = extract_function_block(text, src)
        if "Type=\"Chaser\"" not in raw:
            raise SystemExit(f"ID {src} is not a Chaser")
        blocks.append(make_soft_chaser(raw, nid))
    save_qxw(inject_before_monitor(text, "\n".join(blocks) + "\n"))
    print("OK: soft ring FX 3100-3155")


if __name__ == "__main__":
    main()
