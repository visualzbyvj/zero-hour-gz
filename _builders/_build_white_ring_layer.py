# -*- coding: utf-8 -*-
"""Independent white ring layer3400-3419 (shimmer / chase on fixtures15,16,18,21)."""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import WHITE_CW, WHITE_SEGS, chaser_xml, fv_white, inject_before_monitor, load_qxw, save_qxw, scene_xml, strip_functions

OWNED = set(range(3400, 3439))


def main() -> None:
    text = strip_functions(load_qxw(), OWNED)
    parts: list[str] = []
    fid = 3400
    for seg in range(16):
        pairs: list[tuple[int, str]] = []
        fv = fv_white(WHITE_SEGS, {seg})
        for bar in WHITE_CW:
            pairs.append((bar, fv))
        parts.append(scene_xml(fid, f"WHITE RING LAYER - Seg {seg + 1}", pairs))
        fid += 1
    chase_steps = list(range(3400, 3416))
    parts.append(chaser_xml(3416, "WHITE RING - SEG CHASE", chase_steps, "Loop", 120))
    alt_a = [3400, 3402, 3404, 3406, 3408, 3410, 3412, 3414]
    alt_b = [3401, 3403, 3405, 3407, 3409, 3411, 3413, 3415]
    parts.append(
        chaser_xml(
            3417,
            "WHITE RING - ALT BARS",
            alt_a + alt_b,
            "PingPong",
            200,
        )
    )
    shimmer = [3400, 3415, 3403, 3412, 3407, 3408, 3401, 3414, 3405, 3410]
    parts.append(chaser_xml(3418, "WHITE RING - SHIMMER", shimmer, "Loop", 90))
    parts.append(
        chaser_xml(3419, "WHITE RING - DOUBLE TIME", chase_steps, "Loop", 60)
    )

    # Progressive fill: light up segments 1..16 cumulatively
    fill_steps: list[int] = []
    fid = 3420
    for n in range(1, 17):
        active = set(range(n))
        fv = fv_white(WHITE_SEGS, active)
        pairs_fill = [(bar, fv) for bar in WHITE_CW]
        parts.append(scene_xml(fid, f"WHITE RING FILL - {n}/16", pairs_fill))
        fill_steps.append(fid)
        fid += 1
    # fid is now 3436; but we only have up to 3427 in OWNED, so use chaser IDs carefully
    # Actually fill scenes are 3420-3435 (16 scenes) -- extend OWNED check

    # Sparkle: pseudo-random segment pattern
    sparkle_order = [0, 7, 3, 12, 1, 9, 5, 14, 2, 11, 6, 13, 4, 8, 10, 15]
    sparkle_steps = [3400 + s for s in sparkle_order]
    parts.append(chaser_xml(3436, "WHITE RING - SPARKLE", sparkle_steps, "Loop", 60))

    # Breathe: fill up then empty down (SingleShot for one cycle, or Loop for continuous)
    breathe_steps = fill_steps + list(reversed(fill_steps[:-1]))
    parts.append(chaser_xml(3437, "WHITE RING - BREATHE", breathe_steps, "Loop", 80))

    # Progressive fill chaser (builds up then resets)
    parts.append(chaser_xml(3438, "WHITE RING - FILL CHASE", fill_steps, "Loop", 100))

    save_qxw(inject_before_monitor(text, "\n".join(parts) + "\n"))
    print("OK: white ring layer 3400-3438")


if __name__ == "__main__":
    main()
