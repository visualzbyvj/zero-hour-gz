# -*- coding: utf-8 -*-
"""
Ring chase segment scenes 1550-1581 and chasers 1510-1515 (see script header in repo).
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import (
    INNER_BARS,
    OUTER_BARS,
    RGB_SEGS,
    WHITE_SEGS,
    chaser_xml,
    fv_rgb,
    fv_white,
    inject_before_monitor,
    load_qxw,
    save_qxw,
    scene_xml,
    strip_functions,
)

OUTER_FIX = OUTER_BARS
INNER_FIX = INNER_BARS
WHITE_FIX = (15, 16, 18, 21)

SCENE_IDS = list(range(1550, 1582))
CHASER_IDS = list(range(1510, 1516))
OWNED = set(SCENE_IDS + CHASER_IDS)
HOLD_MS = 214


def main() -> None:
    blocks: list[str] = []

    for k in range(8):
        fv_o = fv_rgb(RGB_SEGS, {k})
        pairs_o = [(fx, fv_o) for fx in OUTER_FIX]
        blocks.append(
            scene_xml(1550 + k, f"RING SEG OUTER - dot {k + 1}", pairs_o)
        )

    for k in range(8):
        fv_i = fv_rgb(RGB_SEGS, {k})
        pairs_i = [(fx, fv_i) for fx in INNER_FIX]
        blocks.append(
            scene_xml(1558 + k, f"RING SEG INNER - dot {k + 1}", pairs_i)
        )

    for k in range(16):
        fv_w = fv_white(WHITE_SEGS, {k})
        pairs_w = [(fx, fv_w) for fx in WHITE_FIX]
        blocks.append(
            scene_xml(1566 + k, f"RING SEG WHITE - dot {k + 1}", pairs_w)
        )

    outer_wave = list(range(1550, 1558))
    blocks.append(
        chaser_xml(1510, "RING OUTER WAVE - CW", outer_wave, "Loop", HOLD_MS)
    )
    blocks.append(
        chaser_xml(1511, "RING OUTER WAVE - PP", outer_wave, "PingPong", HOLD_MS)
    )
    inner_wave = list(range(1558, 1566))
    blocks.append(
        chaser_xml(1512, "RING INNER WAVE - CW", inner_wave, "Loop", HOLD_MS)
    )
    blocks.append(
        chaser_xml(1513, "RING INNER WAVE - PP", inner_wave, "PingPong", HOLD_MS)
    )
    blocks.append(
        chaser_xml(1514, "RING FULL PULSE", [1516, 1517], "Loop", 429)
    )
    blocks.append(
        chaser_xml(
            1515,
            "RING OUTER WAVE - Offset",
            [1557, 1556, 1555, 1554, 1553, 1552, 1551, 1550],
            "Loop",
            HOLD_MS,
        )
    )

    text = strip_functions(load_qxw(), OWNED)
    save_qxw(inject_before_monitor(text, "\n".join(blocks) + "\n"))
    print("OK: ring segment chase 1550-1582 + chasers 1510-1515")


if __name__ == "__main__":
    main()
