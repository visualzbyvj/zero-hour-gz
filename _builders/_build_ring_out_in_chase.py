# -*- coding: utf-8 -*-
"""
Function ID 71 — combined outer+inner within-bar segment chase.
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import chaser_xml, inject_before_monitor, load_qxw, save_qxw, strip_functions

HOLD_MS = 214


def build_chaser_xml() -> str:
    steps: list[int] = []
    for k in range(8):
        steps.append(1550 + k)
        steps.append(1558 + k)
    return chaser_xml(71, "RING CHASE - OUTER+INNER CW", steps, "Loop", HOLD_MS)


def main() -> None:
    text = strip_functions(load_qxw(), {71})
    save_qxw(inject_before_monitor(text, build_chaser_xml() + "\n"))
    print("OK: Chaser 71 RING CHASE - OUTER+INNER CW")


if __name__ == "__main__":
    main()
