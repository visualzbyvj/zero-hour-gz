# -*- coding: utf-8 -*-
"""Accelerating hold profile chasers3200-3263 (sweep + bar families)."""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import SWEEP_COLORS, chaser_xml, inject_before_monitor, load_qxw, save_qxw, strip_functions

OWNED = set(range(3200, 3264))
ACCEL_32 = [400] * 8 + [300] * 8 + [200] * 8 + [100] * 8
ACCEL_BAR = [400, 350, 250, 100]


def main() -> None:
    text = strip_functions(load_qxw(), OWNED)
    parts: list[str] = []
    fid = 3200
    sweep_w = list(range(1600, 1632))
    parts.append(
        chaser_xml(
            fid,
            "ACCEL SWEEP - WHITE CW",
            sweep_w,
            "Loop",
            max(ACCEL_32),
            step_hold=ACCEL_32,
        )
    )
    fid += 1
    for ci, (name, _rgb) in enumerate(SWEEP_COLORS):
        base = 1800 + ci * 32
        steps = list(range(base, base + 32))
        parts.append(
            chaser_xml(
                fid,
                f"ACCEL SWEEP - {name}",
                steps,
                "Loop",
                max(ACCEL_32),
                step_hold=ACCEL_32,
            )
        )
        fid += 1
    parts.append(
        chaser_xml(
            fid,
            "ACCEL SWEEP - WHITE PP",
            sweep_w,
            "PingPong",
            max(ACCEL_32),
            step_hold=ACCEL_32,
        )
    )
    fid += 1
    bar = [1640, 1641, 1642, 1643]
    for j in range(4):
        parts.append(
            chaser_xml(
                fid + j,
                f"ACCEL BAR CW - TIER {j + 1}",
                bar,
                "Loop",
                max(ACCEL_BAR),
                step_hold=ACCEL_BAR,
            )
        )
    fid += 4
    bar_pp = [1640, 1641, 1642, 1643]
    parts.append(
        chaser_xml(
            fid,
            "ACCEL BAR PP",
            bar_pp,
            "PingPong",
            max(ACCEL_BAR),
            step_hold=ACCEL_BAR,
        )
    )
    fid += 1
    dual = list(range(1650, 1666))
    dual_hold = ([400] * 4 + [300] * 4 + [200] * 4 + [100] * 4)[: len(dual)]
    while len(dual_hold) < len(dual):
        dual_hold.append(100)
    parts.append(
        chaser_xml(
            fid,
            "ACCEL DUAL CW",
            dual,
            "Loop",
            max(dual_hold),
            step_hold=dual_hold,
        )
    )
    fid += 1
    # Fill remaining IDs with colored bar accel (reuse bar pattern, different run labels)
    label_idx = 0
    extra_labels = ["HALF SPIN", "SWEEP CCW TIGHT", "BAR CCW ACCEL", "DUAL PP ACCEL"]
    while fid <= 3263:
        label = extra_labels[label_idx % len(extra_labels)]
        parts.append(
            chaser_xml(
                fid,
                f"ACCEL {label} {label_idx + 1}",
                bar,
                "Loop",
                max(ACCEL_BAR),
                step_hold=ACCEL_BAR,
            )
        )
        fid += 1
        label_idx += 1
    save_qxw(inject_before_monitor(text, "\n".join(parts) + "\n"))
    print("OK: accel chasers 3200-3263")


if __name__ == "__main__":
    main()
