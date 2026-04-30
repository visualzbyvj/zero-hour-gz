# -*- coding: utf-8 -*-
"""Energy state macros 3040-3045, speed-tier chasers 3050-3055,
PANIC 3060, STROBE KILL 3061, genre LOOK 1000-1002 + 1006-1008.

Energy states are designed around the DJ set energy curve:
  SIMMER → GROOVE → SURGE → DISSOLVE → TENSION → ERUPTION

Genre looks combine color splits + ring FX + motion for instant
recall of an entire sub-genre aesthetic.
"""
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
    collection_xml,
    fv_rgb_colored,
    fv_str,
    fv_white,
    inject_before_monitor,
    load_qxw,
    save_qxw,
    scene_xml,
    scene_xml_minimal,
    strip_functions,
    panel_led_matrix_rgb,
)

MACRO_IDS = set(range(3040, 3046))
SPEED_IDS = set(range(3050, 3056))
SAFETY_IDS = {3060, 3061}
LOOK_IDS = {1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008}
ALL_MACRO_STRIP = MACRO_IDS | SPEED_IDS | SAFETY_IDS | LOOK_IDS


def ring_bar_warm(rgb: tuple[int, int, int]) -> list[tuple[int, str]]:
    r, g, b = rgb
    all_rgb = set(range(RGB_SEGS))
    all_w = set(range(WHITE_SEGS))
    fvs: list[tuple[int, str]] = []
    for i in range(4):
        fvs.append((OUTER_CW[i], fv_rgb_colored(RGB_SEGS, all_rgb, rgb)))
        fvs.append((INNER_CW[i], fv_rgb_colored(RGB_SEGS, all_rgb, rgb)))
        fvs.append((WHITE_CW[i], fv_white(WHITE_SEGS, all_w)))
    return fvs


def panic_scene() -> str:
    rgb = (255, 200, 150)
    pairs: list[tuple[int, str]] = []
    pairs.extend(ring_bar_warm(rgb))
    bl = [(0, 255), (1, 0), (2, 0), (3, 0)] + [(c, 255) for c in range(4, 12)]
    for fx in FX_4CELL:
        pairs.append((fx, fv_str(bl)))
    cob = [(0, 255), (1, rgb[0]), (2, rgb[1]), (3, rgb[2]), (4, 0), (5, 0), (6, 0)]
    for fx in FX_COB:
        pairs.append((fx, fv_str(cob)))
    a55 = [(0, 255), (1, rgb[0]), (2, rgb[1]), (3, rgb[2])] + [(c, 0) for c in range(4, 10)]
    for fx in FX_A55:
        pairs.append((fx, fv_str(a55)))
    pv = panel_led_matrix_rgb((255, 200, 150), dim=255)
    for fx in FX_PANEL:
        pairs.append((fx, pv))
    return scene_xml(3060, "PANIC HOME - WARM SAFE", pairs)


def build_macros() -> list[str]:
    """Energy state macros — each represents a distinct point on the energy curve."""
    return [
        # SIMMER: ambient intro — slow blue, soft motion, no strobe
        collection_xml(3040, "ENERGY - SIMMER", [18, 121, 1200]),
        # GROOVE: dance floor — warm split, bar chase, bounce motion, gentle strobe
        collection_xml(3041, "ENERGY - GROOVE", [1402, 1753, 1300, 2918]),
        # SURGE: peak dance — aggressive split, dual ring, fast strobe
        collection_xml(3042, "ENERGY - SURGE", [1400, 1757, 2921]),
        # DISSOLVE: breakdown — cool colors, soft sweep
        collection_xml(3043, "ENERGY - DISSOLVE", [115, 121, 1201]),
        # TENSION: build-up — white/cyan split, half ring, med strobe
        collection_xml(3044, "ENERGY - TENSION", [1410, 1756, 2919]),
        # ERUPTION: climax — white blinder, bar chase, bounce, blitz strobe
        collection_xml(3045, "ENERGY - ERUPTION", [128, 1753, 1300, 2923]),
    ]


def build_speed_tiers() -> list[str]:
    sweep = list(range(1600, 1632))
    holds = [429, 214, 107, 54, 27, 13]
    parts: list[str] = []
    for i, h in enumerate(holds):
        parts.append(
            chaser_xml(
                3050 + i,
                f"RING SWEEP CW TIER {i + 1}",
                sweep,
                "Loop",
                h,
                step_hold=h,
            )
        )
    return parts


def build_looks() -> list[str]:
    """Genre-specific look presets — each combines a color world, ring FX, and motion
    style that captures the visual identity of that EDM sub-genre."""
    return [
        # TRAP: Purple/Gold aesthetic, bouncy motion, strobe accent
        collection_xml(1000, "LOOK - TRAP", [1403, 1757, 1300, 2918]),
        # BASS HOUSE: Cyan/Orange warmth, driving sweep, soft motion
        collection_xml(1001, "LOOK - BASS HOUSE", [1404, 1750, 1200]),
        # DUBSTEP: Red/Blue aggression, colored sweep, fast strobe
        collection_xml(1002, "LOOK - DUBSTEP", [1400, 1755, 1770, 2921]),
        # RIDDIM: Dark red/purple, relentless dual ring, fast strobe
        collection_xml(1006, "LOOK - RIDDIM", [1400, 1757, 2921]),
        # MELODIC: White/Cyan ethereal, gentle sweep, soft atmosphere
        collection_xml(1007, "LOOK - MELODIC", [1411, 1750, 1201]),
        # DnB: Cyan/Orange frantic energy, fast bounce
        collection_xml(1008, "LOOK - DnB", [1404, 1300, 1752]),
    ]


def main() -> None:
    text = strip_functions(load_qxw(), ALL_MACRO_STRIP)
    parts: list[str] = []
    parts.extend(build_macros())
    parts.extend(build_speed_tiers())
    parts.append(panic_scene())
    parts.append(scene_xml_minimal(3061, "STROBE KILL (no-op)"))
    parts.extend(build_looks())
    save_qxw(inject_before_monitor(text, "\n".join(parts) + "\n"))
    print("OK: energy3040-3045, speed3050-3055, 3060-3061, LOOK1000-1002+1006-1008")


if __name__ == "__main__":
    main()
