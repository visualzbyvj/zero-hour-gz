# -*- coding: utf-8 -*-
"""BUMP scenes3070-3071, decay3072, BO+HIT3073, helper3074."""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import (
    FX_4CELL,
    FX_A55,
    FX_COB,
    FX_PANEL,
    INNER_CW,
    OUTER_CW,
    RGB_SEGS,
    WHITE_CW,
    WHITE_SEGS,
    chaser_xml,
    fv_str,
    inject_before_monitor,
    load_qxw,
    save_qxw,
    scene_xml,
    strip_functions,
    fv_rgb_colored,
    fv_white,
    panel_led_matrix_rgb,
)

IDS = {3070, 3071, 3072, 3073, 3074}


def full_rig_scene(fid: int, name: str, rgb: tuple[int, int, int]) -> str:
    all_rgb = set(range(RGB_SEGS))
    all_w = set(range(WHITE_SEGS))
    pairs: list[tuple[int, str]] = []
    for i in range(4):
        pairs.append((OUTER_CW[i], fv_rgb_colored(RGB_SEGS, all_rgb, rgb)))
        pairs.append((INNER_CW[i], fv_rgb_colored(RGB_SEGS, all_rgb, rgb)))
        pairs.append((WHITE_CW[i], fv_white(WHITE_SEGS, all_w)))
    bl = [(0, 0), (1, 0), (2, 0), (3, 0)] + [(c, 255) for c in range(4, 12)]
    for fx in FX_4CELL:
        pairs.append((fx, fv_str(bl)))
    cob = [(0, 0), (1, rgb[0]), (2, rgb[1]), (3, rgb[2]), (4, 0), (5, 0), (6, 0)]
    for fx in FX_COB:
        pairs.append((fx, fv_str(cob)))
    a55 = [(0, 0), (1, rgb[0]), (2, rgb[1]), (3, rgb[2])] + [(c, 0) for c in range(4, 10)]
    for fx in FX_A55:
        pairs.append((fx, fv_str(a55)))
    pv = panel_led_matrix_rgb(rgb)
    for fx in FX_PANEL:
        pairs.append((fx, pv))
    return scene_xml(fid, name, pairs)


def dim_warm_scene() -> str:
    rgb = (180, 140, 100)
    return full_rig_scene(3074, "BUMP DECAY - DIM WARM", rgb)


def main() -> None:
    text = strip_functions(load_qxw(), IDS)
    parts = [
        full_rig_scene(3070, "BUMP WHITE - FULL RIG", (255, 255, 255)),
        full_rig_scene(3071, "BUMP WARM - FULL RIG", (255, 170, 0)),
        dim_warm_scene(),
        chaser_xml(
            3072,
            "BUMP DECAY",
            [3070, 3074, 126],
            "SingleShot",
            100,
            step_hold=[100, 200, 100],
            step_fade_out=[0, 0, 300],
        ),
        chaser_xml(
            3073,
            "BO THEN HIT",
            [126, 3070],
            "SingleShot",
            429,
            step_hold=[429, 429],
        ),
    ]
    save_qxw(inject_before_monitor(text, "\n".join(parts) + "\n"))
    print("OK: bump3070-3074 + chasers3072-3073")


if __name__ == "__main__":
    main()
