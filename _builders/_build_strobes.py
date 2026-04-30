# -*- coding: utf-8 -*-
"""Canonical strobe builder.

Builds:
- ring helper scenes 35-40
- hardware strobes 74-93
- ring strobe chasers 94-108
- ring-all collections 109-113
- global strobe collections 2918/2919/2921/2923
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import (
    collection_xml,
    fixture_ids_by_group_name,
    fv_str,
    inject_before_monitor,
    load_qxw,
    save_qxw,
    scene_xml,
    strobe_chaser_xml,
    strip_functions,
)

FX_4CELL = fixture_ids_by_group_name("4 CELL BLINDER - Full")
FX_COB = fixture_ids_by_group_name("SHEHDS COB - Full")
FX_A55 = fixture_ids_by_group_name("A55 SEGMENT - Full")
FX_PANEL = fixture_ids_by_group_name("LED PANEL - Full")
FX_RING_OUTER = fixture_ids_by_group_name("OUTER RING - Full")
FX_RING_INNER = fixture_ids_by_group_name("INNER RING - Full")
FX_RING_WHITE = fixture_ids_by_group_name("WHITE RING - Full")

STROBE_SPEEDS = [
    ("SLOW", 15),
    ("MED", 70),
    ("FAST", 140),
    ("XFAST", 210),
    ("BLITZ", 255),
]

STROBE_RATE_NAMES = ["SLOW", "MED", "FAST", "XFAST", "BLITZ"]
RING_CHASER_DUR = [500, 250, 125, 62, 31]


def fv_4cell(speed: int) -> str:
    return fv_str(
        [(0, 0), (1, speed), (2, 0), (3, 0)]
        + [(ch, 255) for ch in range(4, 12)]
    )


def fv_cob(speed: int) -> str:
    return fv_str([(0, 0), (4, speed)])


def fv_a55(speed: int) -> str:
    return fv_str([(0, 0), (4, speed)])


def fv_panel(speed: int) -> str:
    return fv_str([(0, 0), (1, speed)])


def build_ring_helpers() -> str:
    def all_ch(n: int, val: int) -> str:
        return fv_str([(i, val) for i in range(n)])

    ring_white_24 = all_ch(24, 255)
    ring_black_24 = all_ch(24, 0)
    wring_white_16 = all_ch(16, 255)
    wring_black_16 = all_ch(16, 0)

    parts = [
        scene_xml(35, "STB HELPER - Outer Ring White", [(f, ring_white_24) for f in FX_RING_OUTER]),
        scene_xml(36, "STB HELPER - Outer Ring Black", [(f, ring_black_24) for f in FX_RING_OUTER]),
        scene_xml(37, "STB HELPER - Inner Ring White", [(f, ring_white_24) for f in FX_RING_INNER]),
        scene_xml(38, "STB HELPER - Inner Ring Black", [(f, ring_black_24) for f in FX_RING_INNER]),
        scene_xml(39, "STB HELPER - White Ring Full", [(f, wring_white_16) for f in FX_RING_WHITE]),
        scene_xml(40, "STB HELPER - White Ring Black", [(f, wring_black_16) for f in FX_RING_WHITE]),
    ]
    return "\n".join(parts)


def build_hw_scenes() -> str:
    blocks: list[str] = []
    groups = [
        ("STROBE 4CELL", FX_4CELL, fv_4cell, 74),
        ("STROBE COB", FX_COB, fv_cob, 79),
        ("STROBE A55", FX_A55, fv_a55, 84),
        ("STROBE LED PANEL", FX_PANEL, fv_panel, 89),
    ]
    for prefix, fx_ids, fv_fn, base_id in groups:
        for i, (rate_name, speed) in enumerate(STROBE_SPEEDS):
            blocks.append(
                scene_xml(
                    base_id + i,
                    f"{prefix} - {rate_name}",
                    [(fx, fv_fn(speed)) for fx in fx_ids],
                )
            )
    return "\n".join(blocks)


def build_ring_strobe_chasers() -> str:
    parts: list[str] = []
    for i, (dur, rate_name) in enumerate(zip(RING_CHASER_DUR, STROBE_RATE_NAMES)):
        parts.append(strobe_chaser_xml(94 + i, f"STROBE OUTER RING - {rate_name}", [35, 36], dur))
        parts.append(strobe_chaser_xml(99 + i, f"STROBE INNER RING - {rate_name}", [37, 38], dur))
        parts.append(strobe_chaser_xml(104 + i, f"STROBE WHITE RING - {rate_name}", [39, 40], dur))
        parts.append(collection_xml(109 + i, f"STROBE RINGS ALL - {rate_name}", [94 + i, 99 + i, 104 + i]))
    return "\n".join(parts)


def build_master_strobe_collections() -> str:
    slow = [74, 79, 84, 89, 94, 99, 104, 109]
    med = [75, 80, 85, 90, 95, 100, 105, 110]
    fast = [76, 81, 86, 91, 96, 101, 106, 111]
    blitz = [78, 83, 88, 93, 98, 103, 108, 113]
    parts = [
        collection_xml(73, "MASTER STROBE ALL GROUPS", med),
        collection_xml(2918, "STROBE ALL - SLOW", slow),
        collection_xml(2919, "STROBE ALL - MED", med),
        collection_xml(2921, "STROBE ALL - FAST", fast),
        collection_xml(2923, "STROBE ALL - BLITZ", blitz),
    ]
    return "\n".join(parts)


def main() -> None:
    strip_ids = set(range(35, 41)) | set(range(74, 114)) | set(range(41, 49)) | {73, 2918, 2919, 2921, 2923}
    text = strip_functions(load_qxw(), strip_ids)
    blob = (
        build_ring_helpers()
        + "\n"
        + build_hw_scenes()
        + "\n"
        + build_ring_strobe_chasers()
        + "\n"
        + build_master_strobe_collections()
        + "\n"
    )
    save_qxw(inject_before_monitor(text, blob))
    print("OK: strobes 35-113 + master collections 2918/2919/2921/2923")


if __name__ == "__main__":
    main()
