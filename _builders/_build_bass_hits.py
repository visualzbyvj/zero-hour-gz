# -*- coding: utf-8 -*-
"""Bass hit flashes3500-3509."""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import (
    BLINDER_BACK,
    BLINDER_FRONT,
    COB_BACK,
    COB_FRONT,
    A55_BACK,
    A55_FRONT,
    fv_str,
    chaser_xml,
    inject_before_monitor,
    load_qxw,
    save_qxw,
    scene_xml,
    strip_functions,
)

OWNED = set(range(3500, 3510))

COB_W = fv_str([(0, 0), (1, 255), (2, 255), (3, 255), (4, 0), (5, 0), (6, 0)])
A55_W = fv_str([(0, 0), (1, 255), (2, 255), (3, 255)] + [(c, 0) for c in range(4, 10)])
BL_W = fv_str([(0, 0), (1, 0), (2, 0), (3, 0)] + [(c, 255) for c in range(4, 12)])


def scene_hit(fid: int, name: str, cobs: tuple[int, ...], blinds: tuple[int, ...]) -> str:
    pairs: list[tuple[int, str]] = [(fx, COB_W) for fx in cobs] + [(fx, BL_W) for fx in blinds]
    return scene_xml(fid, name, pairs)


def scene_a55_hit(fid: int, name: str, a55: tuple[int, ...]) -> str:
    pairs = [(fx, A55_W) for fx in a55]
    return scene_xml(fid, name, pairs)


def main() -> None:
    text = strip_functions(load_qxw(), OWNED)
    parts = [
        scene_hit(
            3500,
            "BASS HIT - FRONT COB+BLIND",
            COB_FRONT,
            BLINDER_FRONT,
        ),
        scene_hit(
            3501,
            "BASS HIT - BACK COB+BLIND",
            COB_BACK,
            BLINDER_BACK,
        ),
        chaser_xml(3502, "BASS HIT - ALT F/B", [3500, 3501], "Loop", 107),
        scene_a55_hit(3503, "BASS HIT - FRONT A55", A55_FRONT),
        scene_a55_hit(3504, "BASS HIT - BACK A55", A55_BACK),
        chaser_xml(3505, "BASS HIT - ALT A55", [3503, 3504], "Loop", 107),
        scene_hit(3506, "BASS HIT - FRONT COB ONLY", COB_FRONT, tuple()),
        scene_hit(3507, "BASS HIT - BACK COB ONLY", COB_BACK, tuple()),
        chaser_xml(3508, "BASS HIT - ALT COB", [3506, 3507], "Loop", 107),
        chaser_xml(
            3509,
            "BASS HIT - QUAD PULSE",
            [3500, 3501, 3503, 3504],
            "Loop",
            214,
        ),
    ]
    save_qxw(inject_before_monitor(text, "\n".join(parts) + "\n"))
    print("OK: bass hits3500-3509")


if __name__ == "__main__":
    main()
