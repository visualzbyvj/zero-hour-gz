# -*- coding: utf-8 -*-
"""
Full pattern × color matrix for ring FX around-the-ring effects.

Extends _build_ring_fx.py with colored versions of ALL patterns
(not just SWEEP CW). Reuses existing colored sweep scenes where possible.

New scenes:
  2600-2631  colored bar scenes      (8 colors × 4 positions)
  2640-2655  colored half scenes     (8 colors × 2 positions)
  2700-2827  colored dual scenes     (8 colors × 16 positions)

New chasers:
  2850-2857  SWEEP CCW  × 8 colors  (reuses sweep scenes 1800-2055, reversed)
  2858-2865  SWEEP PP   × 8 colors  (reuses sweep scenes, PingPong)
  2866-2873  DUAL CW    × 8 colors
  2874-2881  BAR CW     × 8 colors
  2882-2889  BAR CCW    × 8 colors  (bar scenes reversed)
  2890-2897  BAR PP     × 8 colors  (bar scenes PingPong)
  2898-2905  HALF SPIN  × 8 colors

Existing (untouched, referenced in VC grid):
  1750-1757  white pattern chasers
  1770-1777  colored SWEEP CW chasers
"""
from _build_ring_fx import build_sweep_position
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import (
    INNER_CW,
    OUTER_CW,
    RGB_SEGS,
    SWEEP_COLORS,
    WHITE_CW,
    WHITE_SEGS,
    chaser_xml,
    fv_rgb_colored,
    fv_white,
    fv_white_black,
    inject_before_monitor,
    load_qxw,
    save_qxw,
    scene_xml,
    strip_functions,
)

BAR_SCENE_BASE = 2600
HALF_SCENE_BASE = 2640
DUAL_SCENE_BASE = 2700

CH_SWEEP_CCW = 2850
CH_SWEEP_PP = 2858
CH_DUAL = 2866
CH_BAR_CW = 2874
CH_BAR_CCW = 2882
CH_BAR_PP = 2890
CH_HALF = 2898


def _bar_scene_colored(fid: int, active_bars: list[int], name: str,
                       rgb: tuple) -> str:
    all_rgb = set(range(RGB_SEGS))
    all_white = set(range(WHITE_SEGS))
    fvs = []
    for i in range(4):
        if i in active_bars:
            fvs.append((OUTER_CW[i], fv_rgb_colored(RGB_SEGS, all_rgb, rgb)))
            fvs.append((INNER_CW[i], fv_rgb_colored(RGB_SEGS, all_rgb, rgb)))
            fvs.append((WHITE_CW[i], fv_white(WHITE_SEGS, all_white)))
        else:
            fvs.append((OUTER_CW[i], fv_rgb_colored(RGB_SEGS, set(), (0, 0, 0))))
            fvs.append((INNER_CW[i], fv_rgb_colored(RGB_SEGS, set(), (0, 0, 0))))
            fvs.append((WHITE_CW[i], fv_white_black(WHITE_SEGS)))
    return scene_xml(fid, name, fvs)


def _dual_scene_colored(fid: int, step: int, name: str, rgb: tuple) -> str:
    pos_a = step
    pos_b = (step + 16) % 32
    bar_a, seg_a, wa_a, wb_a = build_sweep_position(pos_a)
    bar_b, seg_b, wa_b, wb_b = build_sweep_position(pos_b)
    fvs = []
    for i in range(4):
        o_active: set = set()
        i_active: set = set()
        w_active: set = set()
        if i == bar_a:
            o_active.add(seg_a)
            i_active.add(seg_a)
            w_active.update([wa_a, wb_a])
        if i == bar_b:
            o_active.add(seg_b)
            i_active.add(seg_b)
            w_active.update([wa_b, wb_b])
        fvs.append((OUTER_CW[i], fv_rgb_colored(RGB_SEGS, o_active, rgb)))
        fvs.append((INNER_CW[i], fv_rgb_colored(RGB_SEGS, i_active, rgb)))
        fvs.append((WHITE_CW[i], fv_white(WHITE_SEGS, w_active)))
    return scene_xml(fid, name, fvs)


def build_all() -> str:
    blocks: list[str] = []
    bar_names = ["Front", "Right", "Back", "Left"]

    for ci, (cname, rgb) in enumerate(SWEEP_COLORS):
        # Bar scenes: 4 per color
        for pos in range(4):
            fid = BAR_SCENE_BASE + ci * 4 + pos
            blocks.append(_bar_scene_colored(
                fid, [pos], f"RING BAR {cname} - {bar_names[pos]}", rgb))

        # Half scenes: 2 per color
        fid_h0 = HALF_SCENE_BASE + ci * 2
        blocks.append(_bar_scene_colored(
            fid_h0, [0, 2], f"RING HALF {cname} - F+B", rgb))
        blocks.append(_bar_scene_colored(
            fid_h0 + 1, [1, 3], f"RING HALF {cname} - L+R", rgb))

        # Dual scenes: 16 per color
        for step in range(16):
            fid_d = DUAL_SCENE_BASE + ci * 16 + step
            blocks.append(_dual_scene_colored(
                fid_d, step, f"RING DUAL {cname} - S{step + 1}", rgb))

    # Chasers
    for ci, (cname, _rgb) in enumerate(SWEEP_COLORS):
        sweep_base = 1800 + ci * 32
        sweep_cw = list(range(sweep_base, sweep_base + 32))
        sweep_ccw = list(reversed(sweep_cw))
        bar_cw = [BAR_SCENE_BASE + ci * 4 + p for p in range(4)]
        bar_ccw = list(reversed(bar_cw))
        half_ids = [HALF_SCENE_BASE + ci * 2, HALF_SCENE_BASE + ci * 2 + 1]
        dual_ids = [DUAL_SCENE_BASE + ci * 16 + s for s in range(16)]

        blocks.append(chaser_xml(CH_SWEEP_CCW + ci,
                                 f"RING SWEEP CCW - {cname}", sweep_ccw, "Loop", 150))
        blocks.append(chaser_xml(CH_SWEEP_PP + ci,
                                 f"RING SWEEP PP - {cname}", sweep_cw, "PingPong", 150))
        blocks.append(chaser_xml(CH_DUAL + ci,
                                 f"RING DUAL CW - {cname}", dual_ids, "Loop", 150))
        blocks.append(chaser_xml(CH_BAR_CW + ci,
                                 f"RING BAR CW - {cname}", bar_cw, "Loop", 429))
        blocks.append(chaser_xml(CH_BAR_CCW + ci,
                                 f"RING BAR CCW - {cname}", bar_ccw, "Loop", 429))
        blocks.append(chaser_xml(CH_BAR_PP + ci,
                                 f"RING BAR PP - {cname}", bar_cw, "PingPong", 429))
        blocks.append(chaser_xml(CH_HALF + ci,
                                 f"RING HALF - {cname}", half_ids, "Loop", 429))

    return "\n".join(blocks)


ALL_SCENE_IDS = (
    list(range(BAR_SCENE_BASE, BAR_SCENE_BASE + 32))
    + list(range(HALF_SCENE_BASE, HALF_SCENE_BASE + 16))
    + list(range(DUAL_SCENE_BASE, DUAL_SCENE_BASE + 128))
)
ALL_CHASER_IDS = list(range(CH_SWEEP_CCW, CH_HALF + 8))


def main() -> None:
    text = strip_functions(load_qxw(), set(ALL_SCENE_IDS + ALL_CHASER_IDS))
    new_text = inject_before_monitor(text, build_all() + "\n")
    save_qxw(new_text)
    n_s = sum(1 for fid in ALL_SCENE_IDS if f'Function ID="{fid}"' in new_text)
    n_c = sum(1 for fid in ALL_CHASER_IDS if f'Function ID="{fid}"' in new_text)
    print(f"OK: {n_s} colored scenes + {n_c} colored chasers (matrix)")


if __name__ == "__main__":
    main()
