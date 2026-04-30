# -*- coding: utf-8 -*-
"""Create intensity scenes for PUNT sidebar faders (IDs 43, 47, 51, 55, 67).

Dimmer-only scenes: these set ONLY the Master Dimmer channel so the Playback
sliders can control brightness without injecting white RGB values that would
override active color scenes via HTP.

Blinder and White Ring are white-only fixtures (no RGB), so they set all
intensity channels directly.

Also creates combo collections for one-button looks (IDs 44-46, 48-50, 52-54, 56-58).
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import (
    WHITE_SEGS,
    collection_xml,
    fixture_ids_by_group_name,
    fv_str,
    fv_white,
    inject_before_monitor,
    load_qxw,
    save_qxw,
    scene_xml,
    strip_functions,
)

OWNED = {43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 67, 68, 69, 70}

FX_4CELL = fixture_ids_by_group_name("4 CELL BLINDER - Full")
FX_COB = fixture_ids_by_group_name("SHEHDS COB - Full")
FX_A55 = fixture_ids_by_group_name("A55 SEGMENT - Full")
FX_PANEL = fixture_ids_by_group_name("LED PANEL - Full")
WHITE_RING_FULL = fixture_ids_by_group_name("WHITE RING - Full")


def blinder_full_white() -> str:
    """4-Cell COB Blinders at full white (dim+white channels).

    White-only fixture: no RGB conflict possible.
    """
    bl_fv = fv_str([(0, 255), (1, 0), (2, 0), (3, 0)] + [(c, 255) for c in range(4, 12)])
    pairs = [(fx, bl_fv) for fx in FX_4CELL]
    return scene_xml(43, "INTENSITY - BLINDER FULL WHITE", pairs)


def cob_dimmer() -> str:
    """30W COB-RGB: Master Dimmer only (ch0). No RGB channels."""
    cob_fv = fv_str([(0, 255)])
    pairs = [(fx, cob_fv) for fx in FX_COB]
    return scene_xml(47, "INTENSITY - COB DIMMER", pairs)


def a55_dimmer() -> str:
    """A55 Segment Flash: Master Dimmer only (ch0). No RGB channels."""
    a55_fv = fv_str([(0, 255)])
    pairs = [(fx, a55_fv) for fx in FX_A55]
    return scene_xml(51, "INTENSITY - A55 DIMMER", pairs)


def panel_dimmer() -> str:
    """LED Matrix Panels: Master Dimmer only (ch0), strobe off (ch1). No pixel channels."""
    pv = fv_str([(0, 255), (1, 0)])
    pairs = [(fx, pv) for fx in FX_PANEL]
    return scene_xml(55, "INTENSITY - PANEL DIMMER", pairs)


def white_ring_full() -> str:
    """White ring bars at full brightness (all 16 segs per bar).

    White-only fixture: no RGB conflict possible.
    """
    all_segs = set(range(WHITE_SEGS))
    fv = fv_white(WHITE_SEGS, all_segs)
    pairs = [(bar, fv) for bar in WHITE_RING_FULL]
    return scene_xml(67, "INTENSITY - WHITE RING FULL", pairs)


def combo_collections() -> list[str]:
    """One-button combo looks: ring FX + color split + motion.

    IDs 44-46: ring FX combos
    IDs 48-50: color + motion combos
    IDs 52-54: FX + split combos
    IDs 56-58: full scene combos
    """
    return [
        # Ring FX combos (FX + strobe tier)
        collection_xml(44, "COMBO - RED SWEEP + SLOW STROBE", [1770, 2918, 1200]),
        collection_xml(45, "COMBO - GOLD BOUNCE + MED STROBE", [2865, 2919, 1300]),
        collection_xml(46, "COMBO - BLUE BAR + FAST STROBE", [2879, 2921, 1510]),

        # Color + motion combos
        collection_xml(48, "COMBO - WARM SOFT CW", [114, 1750, 1200]),
        collection_xml(49, "COMBO - COOL BOUNCE CW", [115, 1775, 1300]),
        collection_xml(50, "COMBO - FIRE DUAL CHASE", [118, 1757, 1770]),

        # FX + split combos
        collection_xml(52, "COMBO - R/BL SPLIT + SWEEP", [1400, 1770, 1200]),
        collection_xml(53, "COMBO - G/P SPLIT + BAR", [1402, 2880, 1300]),
        collection_xml(54, "COMBO - W/BL SPLIT + BOUNCE", [1409, 1775, 1301]),

        # Full scene combos (ring FX + color + motion + strobe tier)
        collection_xml(56, "COMBO - ENERGY DROP", [1400, 1755, 2923, 1300]),
        collection_xml(57, "COMBO - CHILL WAVE", [1411, 1750, 1201, 2918]),
        collection_xml(58, "COMBO - RAGE MODE", [128, 1753, 1770, 2921]),

        # Extra ring utility
        collection_xml(68, "COMBO - ALL RING WHITE", [1121, 1122, 67]),
        collection_xml(69, "COMBO - OUTER + INNER RED", [17, 19]),
        collection_xml(70, "COMBO - FULL COLOR CYCLE", [1750, 1200]),
    ]


def main() -> None:
    text = strip_functions(load_qxw(), OWNED)
    parts = [
        blinder_full_white(),
        cob_dimmer(),
        a55_dimmer(),
        panel_dimmer(),
        white_ring_full(),
    ]
    parts.extend(combo_collections())
    save_qxw(inject_before_monitor(text, "\n".join(parts) + "\n"))
    print("OK: intensity faders (43,47,51,55,67) + combo collections (44-46,48-50,52-54,56-58,68-70)")


if __name__ == "__main__":
    main()
