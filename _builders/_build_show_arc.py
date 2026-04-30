# -*- coding: utf-8 -*-
"""Show arc tap-advance cue chasers 3600-3605.

Each arc is a tap-advance chaser referencing energy state macros (3040-3045).
The operator taps Go+ to advance through the arc, following the musical
structure of a typical track in each genre.

Energy state IDs:
  3040 = SIMMER (ambient/intro)
  3041 = GROOVE (dance/verse)
  3042 = SURGE  (peak/drop)
  3043 = DISSOLVE (breakdown)
  3044 = TENSION (build-up)
  3045 = ERUPTION (climax)
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import chaser_xml, inject_before_monitor, load_qxw, save_qxw, strip_functions

OWNED = {3600, 3601, 3602, 3603, 3604, 3605}
HOLD = 1_000_000

# DUBSTEP: Intro → Build → Massive Drop → Breakdown → Build Again → Drop → Calm → Build → Build → Climax → Dissolve → End
DUBSTEP = [3040, 3044, 3042, 3043, 3044, 3042, 3043, 3044, 3044, 3045, 3043, 3040]

# TRAP: Moody intro → Groove → Build → Drop → Bridge → Drop → Climax → Cool Down → Build → Climax → Dissolve → End
TRAP = [3040, 3041, 3044, 3042, 3043, 3042, 3045, 3043, 3044, 3045, 3043, 3040]

# HOUSE: Long intro → Groove → Groove → Build → Peak → Groove → Bridge → Build → Climax → Groove → Dissolve → Dissolve → Dissolve → End
HOUSE = [3040, 3041, 3041, 3044, 3042, 3041, 3043, 3044, 3045, 3041, 3043, 3043, 3043, 3040]

# DnB: Intro → Tension → Drop → Groove → Build → Eruption → Dissolve → Build → Drop → Eruption → Dissolve → End
DNB = [3040, 3044, 3042, 3041, 3044, 3045, 3043, 3044, 3042, 3045, 3043, 3040]

# RIDDIM: Minimal intro → Surge → Surge → Dissolve → Surge → Eruption → Surge → Eruption → Dissolve → Surge → Eruption → End
RIDDIM = [3040, 3042, 3042, 3043, 3042, 3045, 3042, 3045, 3043, 3042, 3045, 3040]

# MELODIC: Ambient → Simmer → Groove → Tension → Surge → Dissolve → Tension → Eruption → Dissolve → Simmer → Dissolve → End
MELODIC = [3040, 3040, 3041, 3044, 3042, 3043, 3044, 3045, 3043, 3040, 3043, 3040]


def cue_chaser(fid: int, name: str, steps: list[int]) -> str:
    return chaser_xml(
        fid,
        name,
        steps,
        "SingleShot",
        HOLD,
        tempo="Beats",
        sm_fi="PerStep",
        sm_fo="Default",
        sm_dur="PerStep",
        step_hold=[HOLD] * len(steps),
    )


def main() -> None:
    # Emotional names: operators reach for a *feeling*, not a genre filename.
    # Subtitle preserves the genre hint so they still know the musical grammar.
    text = strip_functions(load_qxw(), OWNED)
    parts = [
        cue_chaser(3600, "ARC - THE DESCENT (DUBSTEP)", DUBSTEP),
        cue_chaser(3601, "ARC - THE BETRAYAL (TRAP)", TRAP),
        cue_chaser(3602, "ARC - THE LONG CLIMB (HOUSE)", HOUSE),
        cue_chaser(3603, "ARC - THE HUNT (DnB)", DNB),
        cue_chaser(3604, "ARC - THE GRINDER (RIDDIM)", RIDDIM),
        cue_chaser(3605, "ARC - THE RESURRECTION (MELODIC)", MELODIC),
    ]
    save_qxw(inject_before_monitor(text, "\n".join(parts) + "\n"))
    print("OK: show arc chasers 3600-3605 (emotional names)")


if __name__ == "__main__":
    main()
