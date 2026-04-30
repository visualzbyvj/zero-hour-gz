# -*- coding: utf-8 -*-
"""Genre toolkits - DUBSTEP, TRAP, BASS HOUSE, HARD TECHNO.

ID map:
  DUBSTEP      3820-3839
  TRAP         3850-3869
  BASS HOUSE   3880-3899
  HARD TECHNO  3910-3929
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from xml.sax.saxutils import escape as xml_escape

from _qlc_helpers import (
    FX_4CELL, FX_A55, FX_COB, FX_PANEL,
    INNER_CW, OUTER_CW, WHITE_CW,
    RGB_SEGS, WHITE_SEGS,
    chaser_xml, collection_xml,
    fv_rgb_black, fv_rgb_colored, fv_str, fv_white, fv_white_black,
    inject_before_monitor, load_qxw, panel_led_matrix_rgb,
    save_qxw, scene_xml, strip_functions,
)

DUB_IDS = set(range(3820, 3840))
TRAP_IDS = set(range(3850, 3870))
BH_IDS = set(range(3880, 3900))
TECHNO_IDS = set(range(3910, 3930))
OWNED = DUB_IDS | TRAP_IDS | BH_IDS | TECHNO_IDS

RED = (255, 0, 0)
DEEP_RED = (150, 0, 0)
BLOOD_RED = (100, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (130, 0, 220)
DEEP_PURPLE = (60, 0, 120)
GOLD = (255, 170, 0)
CYAN = (0, 220, 255)
ORANGE = (255, 70, 0)
WARM_ORANGE = (255, 150, 50)

HOLD_LATCH = 1_000_000


def cob_pairs(rgb, dim):
    r, g, b = rgb
    return fv_str([(0, dim), (1, r), (2, g), (3, b), (4, 0), (5, 0), (6, 0)])


def a55_pairs(rgb, dim):
    r, g, b = rgb
    return fv_str([(0, dim), (1, r), (2, g), (3, b)] + [(c, 0) for c in range(4, 10)])


def blinder_white_pairs(intensity=255):
    return fv_str([(0, 0), (1, 0), (2, 0), (3, 0)] + [(c, intensity) for c in range(4, 12)])


def blinder_rgb_pairs(rgb):
    r, g, b = rgb
    return fv_str([(0, 255), (1, r), (2, g), (3, b)] + [(c, 0) for c in range(4, 12)])


def full_ring_color(rgb, *, outer=True, inner=True, white_segs=False):
    all_rgb = set(range(RGB_SEGS))
    all_w = set(range(WHITE_SEGS))
    pairs = []
    if outer:
        for fx in OUTER_CW:
            pairs.append((fx, fv_rgb_colored(RGB_SEGS, all_rgb, rgb)))
    if inner:
        for fx in INNER_CW:
            pairs.append((fx, fv_rgb_colored(RGB_SEGS, all_rgb, rgb)))
    if white_segs:
        for fx in WHITE_CW:
            pairs.append((fx, fv_white(WHITE_SEGS, all_w)))
    return pairs


def full_rig_color(rgb, *, include_panel=True, include_blinder_white=True,
                   include_white_ring=True, fx_rgb=None, cob_dim=255, a55_dim=255):
    all_rgb = set(range(RGB_SEGS))
    all_w = set(range(WHITE_SEGS))
    pairs = []
    for fx in OUTER_CW:
        pairs.append((fx, fv_rgb_colored(RGB_SEGS, all_rgb, rgb)))
    for fx in INNER_CW:
        pairs.append((fx, fv_rgb_colored(RGB_SEGS, all_rgb, rgb)))
    if include_white_ring:
        for fx in WHITE_CW:
            pairs.append((fx, fv_white(WHITE_SEGS, all_w)))
    fxc = fx_rgb if fx_rgb is not None else rgb
    if include_blinder_white:
        for fx in FX_4CELL:
            pairs.append((fx, blinder_white_pairs(255)))
    else:
        for fx in FX_4CELL:
            pairs.append((fx, blinder_rgb_pairs(fxc)))
    for fx in FX_COB:
        pairs.append((fx, cob_pairs(fxc, cob_dim)))
    for fx in FX_A55:
        pairs.append((fx, a55_pairs(fxc, a55_dim)))
    if include_panel:
        pv = panel_led_matrix_rgb(fxc)
        for fx in FX_PANEL:
            pairs.append((fx, pv))
    return pairs


def dim_everything():
    pairs = []
    for fx in OUTER_CW:
        pairs.append((fx, fv_rgb_black(RGB_SEGS)))
    for fx in INNER_CW:
        pairs.append((fx, fv_rgb_black(RGB_SEGS)))
    for fx in WHITE_CW:
        pairs.append((fx, fv_white_black(WHITE_SEGS)))
    for fx in FX_4CELL:
        pairs.append((fx, fv_str([(c, 0) for c in range(12)])))
    for fx in FX_COB:
        pairs.append((fx, fv_str([(c, 0) for c in range(7)])))
    for fx in FX_A55:
        pairs.append((fx, fv_str([(c, 0) for c in range(10)])))
    for fx in FX_PANEL:
        pairs.append((fx, panel_led_matrix_rgb((0, 0, 0))))
    return pairs


def time_chaser_xml(fid, name, step_ids, holds_ms, run_order="Loop"):
    assert len(step_ids) == len(holds_ms)
    safe = xml_escape(name, {"'": "&apos;", '"': "&quot;"})
    lines = [
        f'  <Function ID="{fid}" Type="Chaser" Name="{safe}">',
        "   <Tempo>Time</Tempo>",
        f'   <Speed FadeIn="0" FadeOut="0" Duration="{holds_ms[0]}"/>',
        "   <Direction>Forward</Direction>",
        f"   <RunOrder>{run_order}</RunOrder>",
        '   <SpeedModes FadeIn="Default" FadeOut="Default" Duration="PerStep"/>',
    ]
    for i, (sid, h) in enumerate(zip(step_ids, holds_ms)):
        lines.append(f'   <Step Number="{i}" FadeIn="0" Hold="{h}" FadeOut="0">{sid}</Step>')
    lines.append("  </Function>")
    return "\n".join(lines)


def rgb_fv(rgb):
    return fv_rgb_colored(RGB_SEGS, set(range(RGB_SEGS)), rgb)


def white_ring_on():
    return fv_white(WHITE_SEGS, set(range(WHITE_SEGS)))


# ═════════════════════════ DUBSTEP (3820-3839) ═════════════════════════
def build_dubstep():
    p = []
    # Scenes 3820-3829
    p.append(scene_xml(3820, "DUB - GROWL DARK",
        [(fx, rgb_fv(BLOOD_RED)) for fx in OUTER_CW] +
        [(fx, rgb_fv(DEEP_PURPLE)) for fx in INNER_CW] +
        [(28, cob_pairs(BLOOD_RED, 100)), (29, cob_pairs(BLOOD_RED, 100))] +
        [(26, a55_pairs(DEEP_PURPLE, 100)), (27, a55_pairs(DEEP_PURPLE, 100))]))
    p.append(scene_xml(3821, "DUB - WOBBLE HIGH",
        full_rig_color(RED, fx_rgb=RED, include_blinder_white=True)))
    p.append(scene_xml(3822, "DUB - WOBBLE LOW",
        full_ring_color(RED) +
        [(fx, blinder_rgb_pairs(BLACK)) for fx in FX_4CELL] +
        [(fx, cob_pairs(DEEP_RED, 60)) for fx in FX_COB] +
        [(fx, a55_pairs(DEEP_RED, 60)) for fx in FX_A55] +
        [(fx, panel_led_matrix_rgb(DEEP_RED)) for fx in FX_PANEL]))
    p.append(scene_xml(3823, "DUB - DROP FULL",
        full_rig_color(RED, fx_rgb=WHITE, include_blinder_white=True)))
    # Striped metalhead outer
    metal = []
    for fx in OUTER_CW:
        pr = []
        for seg in range(RGB_SEGS):
            if seg % 2 == 0:
                pr.extend([seg*3, 255, seg*3+1, 0, seg*3+2, 0])
            else:
                pr.extend([seg*3, 255, seg*3+1, 255, seg*3+2, 255])
        metal.append((fx, ",".join(str(x) for x in pr)))
    p.append(scene_xml(3824, "DUB - METALHEAD",
        metal + [(fx, rgb_fv(RED)) for fx in INNER_CW] +
        [(fx, blinder_white_pairs(255)) for fx in FX_4CELL]))
    p.append(scene_xml(3825, "DUB - NEURO BLACK", dim_everything()))
    p.append(scene_xml(3826, "DUB - NEURO WHITE",
        full_rig_color(WHITE, fx_rgb=WHITE, include_blinder_white=True)))
    p.append(scene_xml(3827, "DUB - PURPLE SWELL",
        full_rig_color(PURPLE, fx_rgb=PURPLE, include_blinder_white=False,
                       include_white_ring=False, cob_dim=180, a55_dim=180)))
    p.append(scene_xml(3828, "DUB - BASS CANNON",
        full_rig_color(DEEP_RED, fx_rgb=DEEP_RED, include_blinder_white=False,
                       include_white_ring=False)))
    p.append(scene_xml(3829, "DUB - RIDDIM ACCENTS",
        [(OUTER_CW[0], rgb_fv(RED)), (OUTER_CW[2], rgb_fv(RED)),
         (OUTER_CW[1], fv_rgb_black(RGB_SEGS)), (OUTER_CW[3], fv_rgb_black(RGB_SEGS)),
         (INNER_CW[1], rgb_fv(RED)), (INNER_CW[3], rgb_fv(RED)),
         (INNER_CW[0], fv_rgb_black(RGB_SEGS)), (INNER_CW[2], fv_rgb_black(RGB_SEGS))]))
    # Chasers 3830-3834
    p.append(time_chaser_xml(3830, "DUB - WOBBLE 1/8", [3821, 3822], [214, 214]))
    p.append(time_chaser_xml(3831, "DUB - WOBBLE 1/16", [3821, 3822], [107, 107]))
    p.append(time_chaser_xml(3832, "DUB - NEURO CHOP",
        [3826, 3825, 3826, 3825, 3826, 3825, 3826, 3825], [62]*8))
    p.append(chaser_xml(3833, "DUB - DROP STRIKE", [3825, 3823], "SingleShot", 1,
        tempo="Beats", sm_fi="PerStep", sm_fo="Default", sm_dur="PerStep",
        step_hold=[1, HOLD_LATCH]))
    p.append(time_chaser_xml(3834, "DUB - RIDDIM PATTERN",
        [3829, 3825, 3829, 3825], [428]*4))
    # Collections 3835-3839
    p.append(collection_xml(3835, "DROP DUB - CLASSIC", [3821, 3830, 2921, 1757]))
    p.append(collection_xml(3836, "DROP DUB - NEURO", [3832, 1770, 2923]))
    p.append(collection_xml(3837, "DROP DUB - RIDDIM", [3834, 1757, 2921]))
    p.append(collection_xml(3838, "DROP DUB - METALHEAD", [3824, 2921, 1753]))
    p.append(collection_xml(3839, "DROP DUB - PURPLE SWELL", [3827, 3762, 1201]))
    return p


# ═════════════════════════ TRAP (3850-3869) ═════════════════════════
def build_trap():
    p = []
    p.append(scene_xml(3850, "TRAP - LEAN",
        full_ring_color(DEEP_PURPLE) +
        [(26, a55_pairs(GOLD, 140)), (27, a55_pairs(GOLD, 140))] +
        [(0, a55_pairs(GOLD, 0)), (7, a55_pairs(GOLD, 0))] +
        [(fx, cob_pairs(DEEP_PURPLE, 100)) for fx in FX_COB] +
        [(fx, panel_led_matrix_rgb(DEEP_PURPLE)) for fx in FX_PANEL]))
    p.append(scene_xml(3851, "TRAP - MAFIA",
        [(OUTER_CW[2], rgb_fv(GOLD)), (INNER_CW[2], rgb_fv(GOLD))] +
        [(28, cob_pairs(GOLD, 200)), (29, cob_pairs(GOLD, 200))] +
        [(26, a55_pairs(GOLD, 200)), (27, a55_pairs(GOLD, 200))]))
    p.append(scene_xml(3852, "TRAP - 808 DARK",
        full_rig_color(DEEP_PURPLE, fx_rgb=DEEP_PURPLE, include_blinder_white=False,
                       include_white_ring=False, cob_dim=90, a55_dim=90)))
    p.append(scene_xml(3853, "TRAP - TRIPLET FLASH",
        [(fx, blinder_white_pairs(255)) for fx in FX_4CELL]))
    p.append(scene_xml(3854, "TRAP - GRITTY",
        [(fx, rgb_fv(PURPLE)) for fx in OUTER_CW] +
        [(fx, rgb_fv(GOLD)) for fx in INNER_CW] +
        [(fx, cob_pairs(GOLD, 200)) for fx in FX_COB] +
        [(fx, a55_pairs(PURPLE, 200)) for fx in FX_A55]))
    p.append(scene_xml(3855, "TRAP - ACE",
        full_rig_color(GOLD, fx_rgb=GOLD, include_blinder_white=True)))
    p.append(scene_xml(3856, "TRAP - FLEX",
        full_ring_color(PURPLE) +
        [(fx, blinder_white_pairs(255)) for fx in FX_4CELL] +
        [(fx, cob_pairs(PURPLE, 255)) for fx in FX_COB] +
        [(fx, a55_pairs(PURPLE, 255)) for fx in FX_A55] +
        [(fx, panel_led_matrix_rgb(PURPLE)) for fx in FX_PANEL]))
    p.append(scene_xml(3857, "TRAP - 808 PULSE ON",
        full_rig_color(PURPLE, fx_rgb=PURPLE, include_blinder_white=False,
                       include_white_ring=False)))
    p.append(scene_xml(3858, "TRAP - 808 PULSE OFF",
        full_rig_color(DEEP_PURPLE, fx_rgb=DEEP_PURPLE, include_blinder_white=False,
                       include_white_ring=False, cob_dim=40, a55_dim=40)))
    p.append(scene_xml(3859, "TRAP - SWAGGER",
        [(fx, rgb_fv(GOLD)) for fx in OUTER_CW] +
        [(fx, rgb_fv(PURPLE)) for fx in INNER_CW] +
        [(fx, cob_pairs(PURPLE, 200)) for fx in FX_COB] +
        [(fx, a55_pairs(GOLD, 200)) for fx in FX_A55]))
    # Chasers 3860-3864
    p.append(time_chaser_xml(3860, "TRAP - TRIPLET HIHATS",
        [3853, 3825, 3853, 3825, 3853, 3825], [133]*6))
    p.append(chaser_xml(3861, "TRAP - LEAN DRIFT",
        [3850, 3854, 3859, 3854], "Loop", 4,
        tempo="Beats", sm_fi="PerStep", sm_fo="Default", sm_dur="PerStep",
        step_fade_in=[4, 4, 4, 4], step_hold=[4, 4, 4, 4]))
    p.append(time_chaser_xml(3862, "TRAP - 808 PULSE", [3857, 3858], [200, 200]))
    p.append(time_chaser_xml(3863, "TRAP - GRITTY STROBE",
        [3854, 3859, 3854, 3859], [125]*4))
    p.append(chaser_xml(3864, "TRAP - ENTRANCE",
        [3825, 3851, 3855], "SingleShot", 2,
        tempo="Beats", sm_fi="PerStep", sm_fo="Default", sm_dur="PerStep",
        step_fade_in=[1, 2, 1], step_hold=[2, 2, HOLD_LATCH]))
    # Collections 3865-3869
    p.append(collection_xml(3865, "DROP TRAP - GUTTA", [3856, 3862, 2921]))
    p.append(collection_xml(3866, "DROP TRAP - FLEX", [3855, 3860, 2923]))
    p.append(collection_xml(3867, "DROP TRAP - NO LIMIT", [3856, 3860, 2921, 1757]))
    p.append(collection_xml(3868, "DROP TRAP - SWAGGER", [3859, 3863, 1302]))
    p.append(collection_xml(3869, "DROP TRAP - MAFIA", [3851, 3864]))
    return p


# ═════════════════════════ BASS HOUSE (3880-3899) ═════════════════════════
def build_bass_house():
    p = []
    p.append(scene_xml(3880, "BH - GROOVE CYAN",
        full_ring_color(CYAN) +
        [(fx, cob_pairs(ORANGE, 180)) for fx in FX_COB] +
        [(fx, a55_pairs(CYAN, 180)) for fx in FX_A55] +
        [(fx, panel_led_matrix_rgb(CYAN)) for fx in FX_PANEL]))
    p.append(scene_xml(3881, "BH - PUMP UP",
        full_rig_color(WHITE, fx_rgb=WHITE, include_blinder_white=True)))
    p.append(scene_xml(3882, "BH - PUMP DOWN",
        full_rig_color(WARM_ORANGE, fx_rgb=WARM_ORANGE, include_blinder_white=False,
                       include_white_ring=False, cob_dim=80, a55_dim=80)))
    p.append(scene_xml(3883, "BH - FILTER HIGH",
        full_ring_color(CYAN, white_segs=True) +
        [(fx, blinder_white_pairs(255)) for fx in FX_4CELL]))
    p.append(scene_xml(3884, "BH - FILTER LOW",
        full_ring_color(WARM_ORANGE) +
        [(fx, a55_pairs(WARM_ORANGE, 140)) for fx in FX_A55]))
    p.append(scene_xml(3885, "BH - DROP HIT",
        full_rig_color(CYAN, fx_rgb=CYAN, include_blinder_white=True)))
    p.append(scene_xml(3886, "BH - TEAR DROP",
        [(fx, rgb_fv(ORANGE)) for fx in INNER_CW] +
        [(fx, rgb_fv(CYAN)) for fx in OUTER_CW]))
    p.append(scene_xml(3887, "BH - HOUSE LIGHT",
        full_ring_color(WARM_ORANGE) +
        [(fx, cob_pairs(WARM_ORANGE, 200)) for fx in FX_COB]))
    p.append(scene_xml(3888, "BH - UK GARAGE",
        [(fx, rgb_fv(WARM_ORANGE)) for fx in OUTER_CW] +
        [(fx, rgb_fv(CYAN)) for fx in INNER_CW]))
    p.append(scene_xml(3889, "BH - DUTCH",
        full_rig_color(CYAN, fx_rgb=CYAN, include_blinder_white=True)))
    # Chasers 3890-3894
    p.append(time_chaser_xml(3890, "BH - GROOVE PULSE",
        [3880, 3884, 3880, 3884], [480]*4))
    p.append(time_chaser_xml(3891, "BH - PUMP COMPRESSION",
        [3881, 3882, 3881, 3882], [480]*4))
    p.append(chaser_xml(3892, "BH - FILTER SWEEP",
        [3883, 3884, 3883, 3884, 3883, 3884], "Loop", 2,
        tempo="Beats", sm_fi="PerStep", sm_fo="Default", sm_dur="PerStep",
        step_fade_in=[2]*6, step_hold=[2]*6))
    p.append(time_chaser_xml(3893, "BH - TEAR DROP PULSE",
        [3886, 3884, 3886, 3884], [240]*4))
    p.append(time_chaser_xml(3894, "BH - HOUSE GROOVE",
        [3880, 3884, 3888, 3884, 3880, 3884, 3888, 3884], [240]*8))
    # Collections 3895-3899
    p.append(collection_xml(3895, "DROP BH - CLASSIC", [3880, 3892, 2918, 1200]))
    p.append(collection_xml(3896, "DROP BH - FESTIVAL", [3889, 3891, 2921]))
    p.append(collection_xml(3897, "DROP BH - UK GARAGE", [3888, 3894, 2919]))
    p.append(collection_xml(3898, "DROP BH - DUTCH", [3889, 3890, 2921]))
    p.append(collection_xml(3899, "DROP BH - DEEP", [3887, 3893, 1200]))
    return p


# ═════════════════════════ HARD TECHNO (3910-3929) ═════════════════════════
def build_hard_techno():
    p = []
    p.append(scene_xml(3910, "TECHNO - INDUSTRIAL",
        [(fx, rgb_fv((200, 200, 200))) for fx in OUTER_CW] +
        [(fx, rgb_fv((200, 200, 200))) for fx in INNER_CW] +
        [(fx, white_ring_on()) for fx in WHITE_CW] +
        [(fx, cob_pairs(WHITE, 120)) for fx in FX_COB] +
        [(fx, a55_pairs(WHITE, 120)) for fx in FX_A55] +
        [(fx, panel_led_matrix_rgb((150, 150, 150))) for fx in FX_PANEL]))
    p.append(scene_xml(3911, "TECHNO - BERGHAIN DARK",
        dim_everything() + [(2, cob_pairs(RED, 200))]))
    p.append(scene_xml(3912, "TECHNO - KICK FLASH",
        full_rig_color(WHITE, fx_rgb=WHITE, include_blinder_white=True)))
    p.append(scene_xml(3913, "TECHNO - RED MINIMAL",
        dim_everything() + [(OUTER_CW[0], rgb_fv(RED))]))
    p.append(scene_xml(3914, "TECHNO - MACHINE ON",
        full_rig_color(WHITE, fx_rgb=WHITE, include_blinder_white=False)))
    p.append(scene_xml(3915, "TECHNO - MACHINE OFF",
        [(fx, rgb_fv((40, 40, 40))) for fx in OUTER_CW] +
        [(fx, rgb_fv((40, 40, 40))) for fx in INNER_CW]))
    p.append(scene_xml(3916, "TECHNO - BLOOD",
        full_rig_color(DEEP_RED, fx_rgb=DEEP_RED, include_blinder_white=False,
                       include_white_ring=False)))
    p.append(scene_xml(3917, "TECHNO - VOID RED",
        full_rig_color(RED, fx_rgb=RED, include_blinder_white=False,
                       include_white_ring=False)))
    p.append(scene_xml(3918, "TECHNO - WAREHOUSE",
        dim_everything() +
        [(OUTER_CW[0], rgb_fv(WHITE)), (OUTER_CW[2], rgb_fv(WHITE)),
         (INNER_CW[1], rgb_fv(RED)), (INNER_CW[3], rgb_fv(RED))]))
    p.append(scene_xml(3919, "TECHNO - PEAK TIME",
        [(fx, rgb_fv(WHITE)) for fx in OUTER_CW] +
        [(fx, rgb_fv(RED)) for fx in INNER_CW] +
        [(fx, white_ring_on()) for fx in WHITE_CW] +
        [(fx, blinder_white_pairs(255)) for fx in FX_4CELL]))
    # Chasers 3920-3924
    p.append(time_chaser_xml(3920, "TECHNO - KICK HAMMER",
        [3912, 3915, 3912, 3915], [444]*4))
    # Industrial strobe uses 3925 (declared below as extra scene)
    p.append(time_chaser_xml(3921, "TECHNO - INDUSTRIAL STROBE",
        [3912, 3925, 3912, 3925, 3912, 3925, 3912, 3925], [62]*8))
    p.append(time_chaser_xml(3922, "TECHNO - BERGHAIN PULSE",
        [3917, 3911], [1000, 1000]))
    gr = [3914, 3914, 3915, 3914, 3915, 3915, 3914, 3914] * 2
    p.append(time_chaser_xml(3923, "TECHNO - MACHINE GROOVE", gr, [111]*16))
    p.append(chaser_xml(3924, "TECHNO - VOID BREATH",
        [3917, 3916, 3911, 3916, 3917], "Loop", 2,
        tempo="Beats", sm_fi="PerStep", sm_fo="Default", sm_dur="PerStep",
        step_fade_in=[2]*5, step_hold=[2]*5))
    # Extra scene 3925: dim off for industrial strobe alternation
    p.append(scene_xml(3925, "TECHNO - FLASH OFF", dim_everything()))
    # Collections 3926-3929
    p.append(collection_xml(3926, "DROP TECHNO - HAMMER", [3914, 3920, 2921]))
    p.append(collection_xml(3927, "DROP TECHNO - UNDERGROUND", [3911, 3922, 1200]))
    p.append(collection_xml(3928, "DROP TECHNO - WAREHOUSE", [3918, 3923, 2919]))
    p.append(collection_xml(3929, "DROP TECHNO - PEAK TIME", [3919, 3921, 2923]))
    return p


def main():
    text = strip_functions(load_qxw(), OWNED)
    parts = []
    parts.extend(build_dubstep())
    parts.extend(build_trap())
    parts.extend(build_bass_house())
    parts.extend(build_hard_techno())
    save_qxw(inject_before_monitor(text, "\n".join(parts) + "\n"))
    print("OK: genres - DUB 3820-3839, TRAP 3850-3869, BH 3880-3899, TECHNO 3910-3929")


if __name__ == "__main__":
    main()
