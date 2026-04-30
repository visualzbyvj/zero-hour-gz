# -*- coding: utf-8 -*-
"""Color World themed palette collections 3000-3009.

Each Color World assigns DIFFERENT colors to different fixture groups
to create depth and visual interest — the pro lighting approach of
warm front / cool back, or themed palettes across the rig.
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import collection_xml, inject_before_monitor, load_qxw, save_qxw, strip_functions

IDS = list(range(3000, 3010))

# Fixture color scene ID lookup:
#   Outer: R=17 O=118 Y=117 Gd=119 G=116 Cy=115 B=18 Pu=114 W=1121
#   Inner: R=19 O=124 Y=123 Gd=125 G=122 Cy=121 B=20 Pu=120 W=1122
#   Full:  R=1100 O=1101 Y=1102 Gd=1103 G=1104 Cy=1105 B=1106 Pu=1107 W=1120
#   Panel: R=272 O=278 Y=277 Gd=279 G=276 Cy=275 B=273 Pu=274 W=280
#   COB:   R=379 O=385 Y=384 Gd=386 G=383 Cy=382 B=380 Pu=381 W=387
#   A55:   R=1110 O=1111 Y=1112 Gd=1113 G=1114 Cy=1115 B=1116 Pu=1117 W=1118

WORLDS = [
    # 0: INFERNO — hot fire (red/orange gradient across rig)
    ("COLOR WORLD - INFERNO", [17, 124, 272, 386, 1111]),
    # 1: EMBER — warm amber glow
    ("COLOR WORLD - EMBER", [118, 125, 278, 385, 1113]),
    # 2: SOLAR — bright golden energy
    ("COLOR WORLD - SOLAR", [117, 125, 277, 386, 1112]),
    # 3: VERDANT — nature palette (green/cyan depth)
    ("COLOR WORLD - VERDANT", [116, 121, 276, 383, 1114]),
    # 4: ARCTIC — ice cold (cyan/blue wash)
    ("COLOR WORLD - ARCTIC", [115, 20, 275, 382, 1115]),
    # 5: OCEAN — deep sea (blue/purple depth)
    ("COLOR WORLD - OCEAN", [18, 120, 273, 380, 1116]),
    # 6: ULTRAVIOLET — UV club vibes (purple/blue)
    ("COLOR WORLD - ULTRAVIOLET", [114, 20, 274, 381, 1117]),
    # 7: AURORA — northern lights (green/purple/gold)
    ("COLOR WORLD - AURORA", [116, 120, 279, 382, 1114]),
    # 8: PRISM — full white clarity
    ("COLOR WORLD - PRISM", [1120, 280, 387, 1118]),
    # 9: VOID — blackout
    ("COLOR WORLD - VOID", [126]),
]

NAMES = [w[0] for w in WORLDS]


def main() -> None:
    text = strip_functions(load_qxw(), set(IDS))
    parts: list[str] = []
    for i, (name, steps) in enumerate(WORLDS):
        parts.append(collection_xml(3000 + i, name, steps))
    save_qxw(inject_before_monitor(text, "\n".join(parts) + "\n"))
    print("OK: Color World collections 3000-3009")


if __name__ == "__main__":
    main()
