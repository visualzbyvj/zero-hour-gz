# -*- coding: utf-8 -*-
"""Front/back COB + A55 spatial scenes 3020-3039."""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import (
    COB_BACK,
    COB_FRONT,
    A55_BACK,
    A55_FRONT,
    COLORS,
    fv_str,
    inject_before_monitor,
    load_qxw,
    save_qxw,
    scene_xml,
    strip_functions,
)

IDS = list(range(3020, 3040))


def _rgb(key: str) -> tuple[int, int, int]:
    if key == "WHT":
        return (255, 255, 255)
    return COLORS[key]["rgb"]  # type: ignore[index]


COMBOS: list[tuple[str, str, str]] = [
    ("WARM FRONT / COLD BACK", "GOLD", "BLUE"),
    ("RED FRONT / BLUE BACK", "RED", "BLUE"),
    ("GOLD FRONT / PURPLE BACK", "GOLD", "PURPLE"),
    ("CYAN FRONT / ORANGE BACK", "CYAN", "ORANGE"),
    ("GREEN FRONT / RED BACK", "GREEN", "RED"),
    ("WHT FRONT / RED BACK", "WHT", "RED"),
    ("WHT FRONT / BLUE BACK", "WHT", "BLUE"),
    ("PURPLE FRONT / GOLD BACK", "PURPLE", "GOLD"),
    ("ORANGE FRONT / CYAN BACK", "ORANGE", "CYAN"),
    ("BLUE FRONT / GOLD BACK", "BLUE", "GOLD"),
]


def cob_fv(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return fv_str([(0, 0), (1, r), (2, g), (3, b), (4, 0), (5, 0), (6, 0)])


def a55_fv(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return fv_str([(0, 0), (1, r), (2, g), (3, b)] + [(ch, 0) for ch in range(4, 10)])


def scene_front_back(
    fid: int,
    name: str,
    front_key: str,
    back_key: str,
) -> str:
    rgb_f = _rgb(front_key)
    rgb_b = _rgb(back_key)
    pairs: list[tuple[int, str]] = []
    for fx in COB_FRONT:
        pairs.append((fx, cob_fv(rgb_f)))
    for fx in COB_BACK:
        pairs.append((fx, cob_fv(rgb_b)))
    for fx in A55_FRONT:
        pairs.append((fx, a55_fv(rgb_f)))
    for fx in A55_BACK:
        pairs.append((fx, a55_fv(rgb_b)))
    return scene_xml(fid, name, pairs)


def main() -> None:
    text = strip_functions(load_qxw(), set(IDS))
    parts: list[str] = []
    base = 3020
    for i, (label, fk, bk) in enumerate(COMBOS):
        safe = label.replace("/", "-")
        parts.append(scene_front_back(base + i, f"SPATIAL COB+A55 - {safe}", fk, bk))
    # Pad to 20 IDs with mirrored variants
    extra = [
        ("BLUE FRONT / RED BACK", "BLUE", "RED"),
        ("CYAN FRONT / PURPLE BACK", "CYAN", "PURPLE"),
        ("GOLD FRONT / GREEN BACK", "GOLD", "GREEN"),
        ("RED FRONT / GOLD BACK", "RED", "GOLD"),
        ("WHT FRONT / CYAN BACK", "WHT", "CYAN"),
        ("ORANGE FRONT / BLUE BACK", "ORANGE", "BLUE"),
        ("PURPLE FRONT / CYAN BACK", "PURPLE", "CYAN"),
        ("GREEN FRONT / GOLD BACK", "GREEN", "GOLD"),
        ("YELLOW FRONT / BLUE BACK", "YELLOW", "BLUE"),
        ("GOLD FRONT / RED BACK", "GOLD", "RED"),
    ]
    for j, (label, fk, bk) in enumerate(extra):
        safe = label.replace("/", "-")
        parts.append(scene_front_back(base + len(COMBOS) + j, f"SPATIAL COB+A55 - {safe}", fk, bk))
    save_qxw(inject_before_monitor(text, "\n".join(parts) + "\n"))
    print("OK: spatial split scenes 3020-3039")


if __name__ == "__main__":
    main()
