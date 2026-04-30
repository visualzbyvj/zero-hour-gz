# -*- coding: utf-8 -*-
"""
Generate around-the-ring chase effects for Outer+Inner+White rings.

WHITE pattern effects (1750-1757):
  SWEEP CW/CCW/PP  — single segment dot travels around all 4 bars
  BAR CW/CCW/PP    — whole bar lights up, rotates around
  BAR HALF         — opposite bars alternate
  DUAL CW          — two dots 180° apart sweep CW

COLORED sweep effects (1770-1777):
  SWEEP CW in 8 solid colors — active segments show the color, inactive = black

Function IDs:
  1600-1631  sweep position scenes (32, white)
  1640-1643  bar chase scenes (4, white)
  1644-1645  half ring scenes (2, white)
  1650-1665  dual sweep scenes (16, white)
  1750-1757  white pattern chasers (8)
  1800-2055  colored sweep scenes (8 colors × 32 steps)
  1770-1777  colored sweep CW chasers (8)
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import (
    RGB_SEGS,
    SEG_REVERSED,
    SWEEP_COLORS,
    WHITE_SEGS,
    INNER_CW,
    OUTER_CW,
    WHITE_CW,
    chaser_xml,
    fv_rgb,
    fv_rgb_black,
    fv_rgb_colored,
    fv_white,
    fv_white_black,
    inject_before_monitor,
    load_qxw,
    save_qxw,
    scene_xml,
    strip_functions,
)

RING_FX_IDS = (
    set(range(1600, 1666))
    | set(range(1800, 2056))
    | set(range(1750, 1758))
    | set(range(1770, 1778))
)


def build_sweep_position(step: int) -> tuple:
    bar_idx = step // RGB_SEGS
    local_seg = step % RGB_SEGS
    if SEG_REVERSED[bar_idx]:
        rgb_seg = RGB_SEGS - 1 - local_seg
        wa = WHITE_SEGS - 1 - (local_seg * 2)
        wb = WHITE_SEGS - 1 - (local_seg * 2 + 1)
    else:
        rgb_seg = local_seg
        wa = local_seg * 2
        wb = local_seg * 2 + 1
    return bar_idx, rgb_seg, wa, wb


def build_sweep_scene(
    fid: int,
    step: int,
    rgb: tuple[int, int, int] = (255, 255, 255),
    name_prefix: str = "RING POS",
) -> str:
    bar_idx, rgb_seg, wa, wb = build_sweep_position(step)
    fvs = []
    for i in range(4):
        o_active = {rgb_seg} if i == bar_idx else set()
        i_active = {rgb_seg} if i == bar_idx else set()
        w_active = {wa, wb} if i == bar_idx else set()
        fvs.append((OUTER_CW[i], fv_rgb_colored(RGB_SEGS, o_active, rgb)))
        fvs.append((INNER_CW[i], fv_rgb_colored(RGB_SEGS, i_active, rgb)))
        fvs.append((WHITE_CW[i], fv_white(WHITE_SEGS, w_active)))
    return scene_xml(fid, f"{name_prefix} - Step {step+1}", fvs)


def build_bar_scene(fid: int, active_bars: list[int], name: str) -> str:
    fvs = []
    all_rgb = set(range(RGB_SEGS))
    all_white = set(range(WHITE_SEGS))
    for i in range(4):
        if i in active_bars:
            fvs.append((OUTER_CW[i], fv_rgb(RGB_SEGS, all_rgb)))
            fvs.append((INNER_CW[i], fv_rgb(RGB_SEGS, all_rgb)))
            fvs.append((WHITE_CW[i], fv_white(WHITE_SEGS, all_white)))
        else:
            fvs.append((OUTER_CW[i], fv_rgb_black(RGB_SEGS)))
            fvs.append((INNER_CW[i], fv_rgb_black(RGB_SEGS)))
            fvs.append((WHITE_CW[i], fv_white_black(WHITE_SEGS)))
    return scene_xml(fid, name, fvs)


def build_dual_scene(fid: int, step: int) -> str:
    pos_a = step
    pos_b = (step + 16) % 32
    bar_a, seg_a, wa_a, wb_a = build_sweep_position(pos_a)
    bar_b, seg_b, wa_b, wb_b = build_sweep_position(pos_b)
    fvs = []
    for i in range(4):
        o_active: set[int] = set()
        i_active: set[int] = set()
        w_active: set[int] = set()
        if i == bar_a:
            o_active.add(seg_a)
            i_active.add(seg_a)
            w_active.update([wa_a, wb_a])
        if i == bar_b:
            o_active.add(seg_b)
            i_active.add(seg_b)
            w_active.update([wa_b, wb_b])
        fvs.append((OUTER_CW[i], fv_rgb(RGB_SEGS, o_active)))
        fvs.append((INNER_CW[i], fv_rgb(RGB_SEGS, i_active)))
        fvs.append((WHITE_CW[i], fv_white(WHITE_SEGS, w_active)))
    return scene_xml(fid, f"RING DUAL - Step {step+1}", fvs)


def build_all() -> str:
    blocks: list[str] = []

    for step in range(32):
        blocks.append(build_sweep_scene(1600 + step, step))

    bar_names = ["Front", "Right", "Back", "Left"]
    for i in range(4):
        blocks.append(build_bar_scene(1640 + i, [i], f"RING BAR - {bar_names[i]}"))

    blocks.append(build_bar_scene(1644, [0, 2], "RING HALF - Front+Back"))
    blocks.append(build_bar_scene(1645, [1, 3], "RING HALF - Left+Right"))

    for step in range(16):
        blocks.append(build_dual_scene(1650 + step, step))

    sweep_cw = list(range(1600, 1632))
    sweep_ccw = list(reversed(sweep_cw))
    bar_cw = [1640, 1641, 1642, 1643]
    bar_ccw = list(reversed(bar_cw))
    half_steps = [1644, 1645]
    dual_cw = list(range(1650, 1666))

    blocks.append(chaser_xml(1750, "RING SWEEP CW", sweep_cw, "Loop", 150))
    blocks.append(chaser_xml(1751, "RING SWEEP CCW", sweep_ccw, "Loop", 150))
    blocks.append(chaser_xml(1752, "RING SWEEP PP", sweep_cw, "PingPong", 150))
    blocks.append(chaser_xml(1753, "RING BAR CW", bar_cw, "Loop", 429))
    blocks.append(chaser_xml(1754, "RING BAR CCW", bar_ccw, "Loop", 429))
    blocks.append(chaser_xml(1755, "RING BAR PP", bar_cw, "PingPong", 429))
    blocks.append(chaser_xml(1756, "RING HALF SPIN", half_steps, "Loop", 429))
    blocks.append(chaser_xml(1757, "RING DUAL CW", dual_cw, "Loop", 150))

    for ci, (color_name, rgb) in enumerate(SWEEP_COLORS):
        base = 1800 + ci * 32
        for step in range(32):
            blocks.append(
                build_sweep_scene(
                    base + step,
                    step,
                    rgb=rgb,
                    name_prefix=f"RING C-{color_name}",
                )
            )

    for ci, (color_name, _rgb) in enumerate(SWEEP_COLORS):
        base = 1800 + ci * 32
        step_ids = list(range(base, base + 32))
        blocks.append(
            chaser_xml(1770 + ci, f"RING SWEEP CW - {color_name}", step_ids, "Loop", 150)
        )

    return "\n".join(blocks)


def main() -> None:
    text = strip_functions(load_qxw(), RING_FX_IDS)
    save_qxw(inject_before_monitor(text, build_all() + "\n"))
    print("OK: ring FX scenes + chasers (1750-1757, 1770-1777, 1600-2055)")


if __name__ == "__main__":
    main()
