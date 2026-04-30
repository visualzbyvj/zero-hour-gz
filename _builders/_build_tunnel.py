# -*- coding: utf-8 -*-
"""Tunnel outer-ring scenes3300-3307 + chasers3320-3329."""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import (
    INNER_BARS,
    OUTER_CW,
    RGB_SEGS,
    SWEEP_COLORS,
    chaser_xml,
    fv_rgb_black,
    fv_rgb_colored,
    inject_before_monitor,
    load_qxw,
    save_qxw,
    scene_xml,
    strip_functions,
)

SCENE_IDS = list(range(3300, 3308))
CH_IDS = list(range(3320, 3330))
OWNED = set(SCENE_IDS + CH_IDS)


def tunnel_pairs(step: int) -> set[int]:
    return [{0, 7}, {1, 6}, {2, 5}, {3, 4}, {2, 5}, {1, 6}, {0, 7}, set()][step % 8]


def tunnel_scene(fid: int, step: int, rgb: tuple[int, int, int]) -> str:
    active = tunnel_pairs(step)
    fvs: list[tuple[int, str]] = []
    for bar in OUTER_CW:
        if active:
            fvs.append((bar, fv_rgb_colored(RGB_SEGS, active, rgb)))
        else:
            fvs.append((bar, fv_rgb_black(RGB_SEGS)))
    inner_black = fv_rgb_black(RGB_SEGS)
    for bar in INNER_BARS:
        fvs.append((bar, inner_black))
    return scene_xml(fid, f"TUNNEL - Step {step + 1}", fvs)


def main() -> None:
    text = strip_functions(load_qxw(), OWNED)
    parts: list[str] = []
    for s in range(8):
        parts.append(tunnel_scene(3300 + s, s, (255, 255, 255)))
    fwd = list(range(3300, 3308))
    breathe = fwd + fwd[-2:0:-1]
    parts.append(chaser_xml(3320, "TUNNEL CONVERGE CW", fwd, "Loop", 200))
    parts.append(chaser_xml(3321, "TUNNEL BREATHE", breathe, "PingPong", 220))
    for ci, (name, _rgb) in enumerate(SWEEP_COLORS):
        steps = [1800 + ci * 32 + i * 4 for i in range(8)]
        parts.append(
            chaser_xml(3322 + ci, f"TUNNEL RING - {name}", steps, "Loop", 200)
        )
    save_qxw(inject_before_monitor(text, "\n".join(parts) + "\n"))
    print("OK: tunnel3300-3307 +3320-3329")


if __name__ == "__main__":
    main()
