# -*- coding: utf-8 -*-
"""
Colored outer+inner segment chasers (HTP-safe vs white chase 71).

Scenes 2100–2227, 2300–2539; chasers 2060–2067, 2070–2084.
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import (
    INNER_BARS,
    OUTER_BARS,
    RGB_SEGS,
    SWEEP_COLORS,
    chaser_xml,
    fv_rgb_colored,
    inject_before_monitor,
    load_qxw,
    save_qxw,
    scene_xml,
    strip_functions,
)

HOLD_MS = 214

OUTER_FIX = OUTER_BARS
INNER_FIX = INNER_BARS
WHITE_RGB = (255, 255, 255)

COLOR_BY_KEY: dict[str, tuple[int, int, int]] = {name: rgb for name, rgb in SWEEP_COLORS}

SPLIT_OI_RGB: list[tuple[str, tuple[int, int, int], tuple[int, int, int]]] = [
    ("RED / BLUE", COLOR_BY_KEY["RED"], COLOR_BY_KEY["BLUE"]),
    ("BLUE / RED", COLOR_BY_KEY["BLUE"], COLOR_BY_KEY["RED"]),
    ("GOLD / PUR", COLOR_BY_KEY["GOLD"], COLOR_BY_KEY["PURPLE"]),
    ("PUR / GOLD", COLOR_BY_KEY["PURPLE"], COLOR_BY_KEY["GOLD"]),
    ("CYAN / ORA", COLOR_BY_KEY["CYAN"], COLOR_BY_KEY["ORANGE"]),
    ("ORA / CYAN", COLOR_BY_KEY["ORANGE"], COLOR_BY_KEY["CYAN"]),
    ("GRN / RED", COLOR_BY_KEY["GREEN"], COLOR_BY_KEY["RED"]),
    ("YEL / BLUE", COLOR_BY_KEY["YELLOW"], COLOR_BY_KEY["BLUE"]),
    ("WHT / RED", WHITE_RGB, COLOR_BY_KEY["RED"]),
    ("WHT / BLUE", WHITE_RGB, COLOR_BY_KEY["BLUE"]),
    ("WHT / PUR", WHITE_RGB, COLOR_BY_KEY["PURPLE"]),
    ("WHT / CYAN", WHITE_RGB, COLOR_BY_KEY["CYAN"]),
    ("GOLD / CYN", COLOR_BY_KEY["GOLD"], COLOR_BY_KEY["CYAN"]),
    ("PUR / ORA", COLOR_BY_KEY["PURPLE"], COLOR_BY_KEY["ORANGE"]),
    ("GRN / PUR", COLOR_BY_KEY["GREEN"], COLOR_BY_KEY["PURPLE"]),
]

SCENE_SOLID_BASE = 2100
SCENE_SPLIT_BASE = 2300
CH_SOLID_BASE = 2060
CH_SPLIT_BASE = 2070


def _fv_seg(seg: int, rgb: tuple[int, int, int]) -> str:
    return fv_rgb_colored(RGB_SEGS, {seg}, rgb)


def _solid_scene(color_idx: int, step: int) -> str:
    name_c, rgb = SWEEP_COLORS[color_idx]
    k = step // 2
    if step % 2 == 0:
        fv = _fv_seg(k, rgb)
        pairs = [(i, fv) for i in OUTER_FIX]
        tag = f"{name_c} - O{k + 1} S{step:02d}"
    else:
        fv = _fv_seg(k, rgb)
        pairs = [(i, fv) for i in INNER_FIX]
        tag = f"{name_c} - I{k + 1} S{step:02d}"
    return scene_xml(SCENE_SOLID_BASE + color_idx * 16 + step, f"RING OI {tag}", pairs)


def _split_scene(split_idx: int, step: int) -> str:
    label, outer_rgb, inner_rgb = SPLIT_OI_RGB[split_idx]
    k = step // 2
    if step % 2 == 0:
        fv = _fv_seg(k, outer_rgb)
        pairs = [(i, fv) for i in OUTER_FIX]
        tag = f"{label} - O{k + 1} S{step:02d}"
    else:
        fv = _fv_seg(k, inner_rgb)
        pairs = [(i, fv) for i in INNER_FIX]
        tag = f"{label} - I{k + 1} S{step:02d}"
    return scene_xml(SCENE_SPLIT_BASE + split_idx * 16 + step, f"RING OI {tag}", pairs)


def _colored_oi_ids() -> list[int]:
    return (
        list(range(CH_SOLID_BASE, CH_SOLID_BASE + 8))
        + list(range(CH_SPLIT_BASE, CH_SPLIT_BASE + 15))
        + list(range(SCENE_SOLID_BASE, SCENE_SOLID_BASE + 128))
        + list(range(SCENE_SPLIT_BASE, SCENE_SPLIT_BASE + 240))
    )


def build_xml() -> str:
    parts: list[str] = []
    for ci in range(8):
        for s in range(16):
            parts.append(_solid_scene(ci, s))
    for si in range(15):
        for s in range(16):
            parts.append(_split_scene(si, s))
    for ci, (name_c, _) in enumerate(SWEEP_COLORS):
        sid0 = SCENE_SOLID_BASE + ci * 16
        steps = list(range(sid0, sid0 + 16))
        parts.append(
            chaser_xml(CH_SOLID_BASE + ci, f"RING OI CHASE - {name_c}", steps, "Loop", HOLD_MS)
        )
    for si, (label, _, _) in enumerate(SPLIT_OI_RGB):
        sid0 = SCENE_SPLIT_BASE + si * 16
        steps = list(range(sid0, sid0 + 16))
        safe = label.replace("/", "-")
        parts.append(
            chaser_xml(CH_SPLIT_BASE + si, f"RING OI CHASE - {safe}", steps, "Loop", HOLD_MS)
        )
    return "\n".join(parts) + "\n"


def main() -> None:
    text = strip_functions(load_qxw(), set(_colored_oi_ids()))
    save_qxw(inject_before_monitor(text, build_xml()))
    print("OK: colored O+I scenes 2100-2227, 2300-2539; chasers 2060-2067, 2070-2084")


if __name__ == "__main__":
    main()
