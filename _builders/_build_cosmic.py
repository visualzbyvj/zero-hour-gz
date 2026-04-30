# -*- coding: utf-8 -*-
"""Cosmic-god toolkit: darkness, white-phaser overlays, surprise randoms, time-shape ramps.

Philosophy hooks:
  - Darkness is a primary color: 3740-3749
  - Phaser/LFO layer on White Ring (independent dimmer channels = safe HTP stacking): 3750-3769
  - Generative / surprise-me (Random + SingleShot, huge hold so the first random
    step latches and holds): 3770-3779
  - Time as material (ramp/ritardando, ms-based accel/decel chasers): 3800-3819

All IDs in ranges 3740-3819. See .cursor/rules/qlc-project.md for the authoritative
ID ranges table.
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
    WHITE_BARS,
    WHITE_SEGS,
    chaser_xml,
    fv_rgb_colored,
    fv_str,
    fv_white,
    inject_before_monitor,
    load_qxw,
    save_qxw,
    scene_xml,
    scene_xml_minimal,
    strip_functions,
    strobe_chaser_xml,
)

DARK_IDS = set(range(3740, 3750))
PHASER_SEED_IDS = set(range(3750, 3760))
PHASER_CHASER_IDS = set(range(3760, 3770))
SURPRISE_IDS = set(range(3770, 3780))
RAMP_IDS = set(range(3800, 3820))
OWNED = DARK_IDS | PHASER_SEED_IDS | PHASER_CHASER_IDS | SURPRISE_IDS | RAMP_IDS

HOLD_HUGE = 1_000_000  # "forever" hold for SingleShot latch behaviour


# ──────────────────────────────────────────────────────────────────
# Helpers local to this builder
# ──────────────────────────────────────────────────────────────────
def fv_white_lvl(num_segs: int, level: int) -> str:
    """White-channel fixture value: all segs at `level`."""
    pairs: list[int] = []
    for seg in range(num_segs):
        pairs.extend([seg, level])
    return ",".join(str(x) for x in pairs)


def white_ring_all_level(level: int) -> list[tuple[int, str]]:
    return [(fx, fv_white_lvl(WHITE_SEGS, level)) for fx in WHITE_BARS]


def cob_level(rgb: tuple[int, int, int], dim: int) -> str:
    r, g, b = rgb
    return fv_str([(0, dim), (1, r), (2, g), (3, b), (4, 0), (5, 0), (6, 0)])


def a55_level(rgb: tuple[int, int, int], dim: int) -> str:
    r, g, b = rgb
    return fv_str([(0, dim), (1, r), (2, g), (3, b)] + [(c, 0) for c in range(4, 10)])


# ──────────────────────────────────────────────────────────────────
# DARKNESS TOOLKIT (3740-3749)
#   The dark between heartbeats is where the audience comes alive.
# ──────────────────────────────────────────────────────────────────
def scene_whisper() -> str:
    """3740: WHT ring warm-ish glow at 20%, everything else dark."""
    pairs = white_ring_all_level(51)  # ~20%
    return scene_xml(3740, "DARK - WHISPER", pairs)


def scene_silhouette() -> str:
    """3741: back fixtures (COB BACK + A55 BACK) warm amber 40%, fronts off.
    Audience sees silhouettes against a warm wash."""
    amber = (255, 100, 20)
    pairs: list[tuple[int, str]] = []
    # COB BACK (28, 29) warm @ ~40%
    for fx in (28, 29):
        pairs.append((fx, cob_level(amber, 102)))
    # A55 BACK (26, 27) warm @ ~40%
    for fx in (26, 27):
        pairs.append((fx, a55_level(amber, 102)))
    return scene_xml(3741, "DARK - SILHOUETTE", pairs)


def scene_candle() -> str:
    """3742: single outer-ring-front bar flicker-amber at 25%. The one flame."""
    amber = (255, 80, 0)
    # Outer ring front fixture is OUTER_CW[0] = 3 in rules. Use just 2 middle segs.
    front_fx = 3
    dim = 64
    r, g, b = amber
    pairs_out: list[int] = []
    active = {3, 4}  # middle 2 of 8 segs
    for seg in range(RGB_SEGS):
        base = seg * 3
        if seg in active:
            pairs_out.extend([base, int(r * dim / 255), base + 1, int(g * dim / 255), base + 2, int(b * dim / 255)])
        else:
            pairs_out.extend([base, 0, base + 1, 0, base + 2, 0])
    fv = ",".join(str(x) for x in pairs_out)
    return scene_xml(3742, "DARK - CANDLE", [(front_fx, fv)])


def scene_half_rig_front() -> str:
    """3743: only FRONT half of the rig on a dim warm. Gives intimate forward wash."""
    amber = (255, 120, 40)
    pairs: list[tuple[int, str]] = []
    # Outer+Inner FRONT bars only
    all_rgb = set(range(RGB_SEGS))
    pairs.append((OUTER_CW[0], fv_rgb_colored(RGB_SEGS, all_rgb, amber)))
    pairs.append((INNER_CW[0], fv_rgb_colored(RGB_SEGS, all_rgb, amber)))
    # White ring front @ 30%
    pairs.append((WHITE_BARS[0], fv_white_lvl(WHITE_SEGS, 77)))
    # COB fronts + A55 fronts
    for fx in (2, 11):
        pairs.append((fx, cob_level(amber, 128)))
    for fx in (0, 7):
        pairs.append((fx, a55_level(amber, 128)))
    return scene_xml(3743, "DARK - HALF RIG FRONT", pairs)


def scene_half_rig_back() -> str:
    """3744: only BACK half. The reveal effect after a front-only intro."""
    amber = (255, 100, 30)
    pairs: list[tuple[int, str]] = []
    all_rgb = set(range(RGB_SEGS))
    pairs.append((OUTER_CW[2], fv_rgb_colored(RGB_SEGS, all_rgb, amber)))  # back
    pairs.append((INNER_CW[2], fv_rgb_colored(RGB_SEGS, all_rgb, amber)))
    pairs.append((WHITE_BARS[2], fv_white_lvl(WHITE_SEGS, 77)))
    for fx in (28, 29):
        pairs.append((fx, cob_level(amber, 128)))
    for fx in (26, 27):
        pairs.append((fx, a55_level(amber, 128)))
    return scene_xml(3744, "DARK - HALF RIG BACK", pairs)


def scene_neg_flash_on() -> str:
    """3745: FULL white wash (opposite state of FULL BO 126). Used inside NEG STROBE."""
    white = (255, 255, 255)
    pairs: list[tuple[int, str]] = []
    all_rgb = set(range(RGB_SEGS))
    all_w = set(range(WHITE_SEGS))
    for fx in OUTER_CW:
        pairs.append((fx, fv_rgb_colored(RGB_SEGS, all_rgb, white)))
    for fx in INNER_CW:
        pairs.append((fx, fv_rgb_colored(RGB_SEGS, all_rgb, white)))
    for fx in WHITE_BARS:
        pairs.append((fx, fv_white(WHITE_SEGS, all_w)))
    bl = [(0, 255), (1, 0), (2, 0), (3, 0)] + [(c, 255) for c in range(4, 12)]
    for fx in FX_4CELL:
        pairs.append((fx, fv_str(bl)))
    for fx in FX_COB:
        pairs.append((fx, cob_level(white, 255)))
    for fx in FX_A55:
        pairs.append((fx, a55_level(white, 255)))
    return scene_xml(3745, "DARK - NEG FLASH ON", pairs)


def chaser_8bar_black() -> str:
    """3746: 8-bar (32-beat) full blackout hold; releases to whatever is underneath.
    Press = instant silence. Perfect for the beat before an ERUPTION."""
    return chaser_xml(
        3746,
        "DARK - 8 BAR BLACK",
        [126],  # FULL BO scene
        "SingleShot",
        32,  # 32 beats = 8 bars of 4/4
        tempo="Beats",
        sm_fi="PerStep",
        sm_fo="Default",
        sm_dur="PerStep",
        step_hold=[32],
    )


def chaser_neg_strobe() -> str:
    """3747: negative strobe — alternate FULL-WHITE and FULL-BLACK at 150ms.
    Ping-pong of presence and absence. Use on top of a color look for ferocity."""
    return strobe_chaser_xml(
        3747,
        "DARK - NEG STROBE",
        [3745, 126, 3745, 126],
        150,
        run_order="Loop",
    )


def chaser_smolder_decay() -> str:
    """3748: warm-to-dark decay over 8 bars. Cinematic dissolve. SingleShot."""
    # Chain: HALF RIG FRONT → WHISPER → FULL BO. Each holds 4 beats with 4-beat fade.
    return chaser_xml(
        3748,
        "DARK - SMOLDER DECAY",
        [3743, 3740, 126],
        "SingleShot",
        4,
        tempo="Beats",
        sm_fi="PerStep",
        sm_fo="PerStep",
        sm_dur="PerStep",
        step_fade_in=[4, 4, 4],
        step_fade_out=0,
        step_hold=[4, 4, 32],
    )


def chaser_soft_vanish() -> str:
    """3749: slow invisible fade from held state into blackness over 16 beats.
    Operator fires this a bar before a drop for gravitas."""
    return chaser_xml(
        3749,
        "DARK - SOFT VANISH",
        [3743, 3741, 3740, 126],
        "SingleShot",
        4,
        tempo="Beats",
        sm_fi="PerStep",
        sm_fo="Default",
        sm_dur="PerStep",
        step_fade_in=[4, 4, 4, 4],
        step_hold=[4, 4, 4, HOLD_HUGE],
    )


def build_darkness() -> list[str]:
    return [
        scene_whisper(),
        scene_silhouette(),
        scene_candle(),
        scene_half_rig_front(),
        scene_half_rig_back(),
        scene_neg_flash_on(),
        chaser_8bar_black(),
        chaser_neg_strobe(),
        chaser_smolder_decay(),
        chaser_soft_vanish(),
    ]


# ──────────────────────────────────────────────────────────────────
# WHITE PHASER / LFO OVERLAYS (3750-3769)
#   White Ring has independent per-segment dimmer channels (16 x 1ch).
#   Stacks safely on top of any colored ring look via HTP.
# ──────────────────────────────────────────────────────────────────
def phaser_seed(fid: int, name: str, level: int) -> str:
    return scene_xml(fid, name, white_ring_all_level(level))


def phaser_seed_segset(fid: int, name: str, active: set[int], level: int = 255) -> str:
    pairs: list[tuple[int, str]] = []
    for fx in WHITE_BARS:
        segpairs: list[int] = []
        for seg in range(WHITE_SEGS):
            segpairs.extend([seg, level if seg in active else 0])
        pairs.append((fx, ",".join(str(x) for x in segpairs)))
    return scene_xml(fid, name, pairs)


def build_phaser_seeds() -> list[str]:
    """Seed scenes 3750-3759 used by phaser chasers 3760-3769."""
    return [
        phaser_seed(3750, "PHASER WHT - OFF", 0),
        phaser_seed(3751, "PHASER WHT - LOW", 51),     # 20%
        phaser_seed(3752, "PHASER WHT - MED", 128),    # 50%
        phaser_seed(3753, "PHASER WHT - HIGH", 230),   # 90%
        phaser_seed(3754, "PHASER WHT - FULL", 255),
        # Sparse patterns (for sparkle/drift)
        phaser_seed_segset(3755, "PHASER WHT - EVEN",
                           active={0, 2, 4, 6, 8, 10, 12, 14}),
        phaser_seed_segset(3756, "PHASER WHT - ODD",
                           active={1, 3, 5, 7, 9, 11, 13, 15}),
        phaser_seed_segset(3757, "PHASER WHT - QUARTERS",
                           active={0, 4, 8, 12}),
        phaser_seed_segset(3758, "PHASER WHT - HALVES",
                           active={0, 1, 2, 3, 4, 5, 6, 7}),
        phaser_seed_segset(3759, "PHASER WHT - OTHER HALVES",
                           active={8, 9, 10, 11, 12, 13, 14, 15}),
    ]


def phaser_breathe() -> str:
    """3760: 4-beat breathe — cosine-ish wave from LOW to HIGH and back.
    Fades at PerStep make it feel organic."""
    return chaser_xml(
        3760,
        "PHASER WHT - BREATHE",
        [3751, 3753, 3752, 3753, 3751, 3750],
        "Loop",
        1,
        tempo="Beats",
        sm_fi="PerStep",
        sm_fo="Default",
        sm_dur="PerStep",
        step_fade_in=[1, 1, 1, 1, 1, 1],
        step_hold=[1, 1, 1, 1, 1, 1],
    )


def phaser_heartbeat() -> str:
    """3761: lub-dub cardiac pulse. Two sharp peaks, then rest.
    Pattern: HIGH-OFF-HIGH-OFF-OFF-OFF across 6 beats."""
    return chaser_xml(
        3761,
        "PHASER WHT - HEARTBEAT",
        [3753, 3750, 3753, 3750, 3750, 3750],
        "Loop",
        1,
        tempo="Beats",
        sm_fi="PerStep",
        sm_fo="Default",
        sm_dur="PerStep",
        step_fade_in=0,
        step_hold=[1, 1, 1, 1, 1, 1],
    )


def phaser_swell() -> str:
    """3762: gradual 16-beat swell from dark to bright, then cut.
    Fires once and holds at FULL until released."""
    return chaser_xml(
        3762,
        "PHASER WHT - SWELL",
        [3750, 3751, 3752, 3753, 3754],
        "SingleShot",
        4,
        tempo="Beats",
        sm_fi="PerStep",
        sm_fo="Default",
        sm_dur="PerStep",
        step_fade_in=[4, 4, 4, 4, 4],
        step_hold=[4, 4, 4, 4, HOLD_HUGE],
    )


def phaser_sparkle() -> str:
    """3763: random single-seg flashes. Uses Random run order through sparse patterns."""
    return chaser_xml(
        3763,
        "PHASER WHT - SPARKLE",
        [3755, 3756, 3757, 3758, 3759, 3750, 3755, 3757],
        "Random",
        1,
        tempo="Beats",
        sm_fi="Default",
        sm_fo="Default",
        sm_dur="PerStep",
        step_hold=[1] * 8,
    )


def phaser_drift() -> str:
    """3764: slow 8-beat drift — segments travel across the ring slowly.
    Uses quarters → halves → other halves for a wave feel."""
    return chaser_xml(
        3764,
        "PHASER WHT - DRIFT",
        [3758, 3757, 3759, 3757],
        "Loop",
        2,
        tempo="Beats",
        sm_fi="PerStep",
        sm_fo="Default",
        sm_dur="PerStep",
        step_fade_in=[2, 2, 2, 2],
        step_hold=[2, 2, 2, 2],
    )


def phaser_ghost() -> str:
    """3765: ethereal ultra-slow fade up+down over 16 beats. The 'something is
    coming' tease right before an ERUPTION."""
    return chaser_xml(
        3765,
        "PHASER WHT - GHOST",
        [3750, 3751, 3752, 3751, 3750],
        "Loop",
        4,
        tempo="Beats",
        sm_fi="PerStep",
        sm_fo="Default",
        sm_dur="PerStep",
        step_fade_in=[4, 4, 4, 4, 4],
        step_hold=[4, 4, 4, 4, 4],
    )


def phaser_pulse_fast() -> str:
    """3766: fast ms-based pulse (Tempo=Time) for climax moments. 150ms on/off."""
    return strobe_chaser_xml(
        3766,
        "PHASER WHT - PULSE 150",
        [3754, 3750, 3754, 3750],
        150,
        run_order="Loop",
    )


def build_phaser_chasers() -> list[str]:
    return [
        phaser_breathe(),
        phaser_heartbeat(),
        phaser_swell(),
        phaser_sparkle(),
        phaser_drift(),
        phaser_ghost(),
        phaser_pulse_fast(),
    ]


# ──────────────────────────────────────────────────────────────────
# SURPRISE / GENERATIVE (3770-3779)
#   Random + SingleShot with huge hold: first random step latches and holds
#   until operator releases. Gives operator a "roulette" surface.
# ──────────────────────────────────────────────────────────────────
def surprise(fid: int, name: str, steps: list[int]) -> str:
    return chaser_xml(
        fid,
        name,
        steps,
        "Random",
        HOLD_HUGE,
        tempo="Beats",
        sm_fi="Default",
        sm_fo="Default",
        sm_dur="PerStep",
        step_hold=[HOLD_HUGE] * len(steps),
    )


def build_surprise() -> list[str]:
    return [
        # 3770: roulette through Color Worlds (INFERNO..PRISM)
        surprise(3770, "SURPRISE - COLOR WORLD", [3000, 3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008]),
        # 3771: roulette through Genre Looks
        surprise(3771, "SURPRISE - GENRE LOOK", [1000, 1001, 1002, 1006, 1007, 1008]),
        # 3772: roulette through Energy States
        surprise(3772, "SURPRISE - ENERGY STATE", [3040, 3041, 3042, 3043, 3044, 3045]),
        # 3773: roulette through favorite ring FX
        surprise(3773, "SURPRISE - RING FX",
                 [1750, 1751, 1752, 1753, 1757, 1770, 1773, 1775]),
        # 3774: roulette through Ring RGBMatrix effects
        surprise(3774, "SURPRISE - RING MATRIX",
                 [3700, 3701, 3703, 3704, 3706, 3707, 3708, 3712]),
        # 3775: roulette through motion chasers (CW/CCW/bounce/wave)
        surprise(3775, "SURPRISE - MOTION",
                 [1200, 1201, 1202, 1300, 1301, 1510, 71]),
        # 3776: roulette through darkness textures
        surprise(3776, "SURPRISE - DARKNESS",
                 [3740, 3741, 3742, 3743, 3744]),
        # 3777: roulette through phaser overlays
        surprise(3777, "SURPRISE - PHASER",
                 [3760, 3761, 3762, 3763, 3764, 3765, 3766]),
        # 3778: roulette through spatial splits (COB+A55 spatial scenes 3020-3039)
        surprise(3778, "SURPRISE - SPATIAL",
                 list(range(3020, 3040))),
        # 3779: TOTAL ROULETTE — the most chaotic. Pulls from anywhere.
        surprise(3779, "SURPRISE - TOTAL CHAOS",
                 [3000, 3003, 3005, 1000, 1002, 1007, 3040, 3042, 3045,
                  1750, 1757, 3700, 3708, 3712, 71]),
    ]


# ──────────────────────────────────────────────────────────────────
# RAMP / TIME-SHAPE PRIMITIVES (3800-3819)
#   Tempo=Time ms-based chasers with per-step holds that follow a curve.
#   Exponential accel 500ms → 30ms, or decel 30ms → 500ms.
# ──────────────────────────────────────────────────────────────────
def _expo_holds(n: int, start_ms: int, end_ms: int) -> list[int]:
    """n-step exponential interpolation from start_ms to end_ms."""
    if n < 2:
        return [start_ms]
    ratio = (end_ms / start_ms) ** (1 / (n - 1))
    return [max(20, int(round(start_ms * (ratio ** i)))) for i in range(n)]


def ramp_chaser(fid: int, name: str, step_ids: list[int], holds: list[int]) -> str:
    """Tempo=Time chaser with per-step Hold values."""
    assert len(step_ids) == len(holds), "step_ids and holds must match length"
    safe = name.replace("&", "&amp;")
    lines = [
        f'  <Function ID="{fid}" Type="Chaser" Name="{safe}">',
        "   <Tempo>Time</Tempo>",
        '   <Speed FadeIn="0" FadeOut="0" Duration="150"/>',
        "   <Direction>Forward</Direction>",
        "   <RunOrder>SingleShot</RunOrder>",
        '   <SpeedModes FadeIn="Default" FadeOut="Default" Duration="PerStep"/>',
    ]
    for i, (sid, h) in enumerate(zip(step_ids, holds)):
        lines.append(f'   <Step Number="{i}" FadeIn="0" Hold="{h}" FadeOut="0">{sid}</Step>')
    lines.append("  </Function>")
    return "\n".join(lines)


def build_ramp() -> list[str]:
    # Use first 16 sweep scenes (1600-1615) for the ring progression
    sweep = list(range(1600, 1616))
    accel_holds = _expo_holds(16, 500, 30)       # slow→fast (accelerando)
    decel_holds = list(reversed(accel_holds))    # fast→slow (ritardando)

    # Build-up chain using energy states — 32-beat cinematic build
    #   The slow ramp of visuals matching a DJ building energy over 4 bars
    build_ids = [3040, 3040, 3041, 3041, 3044, 3044, 3042, 3045]
    build_holds_ms = [4000, 4000, 3000, 3000, 2000, 2000, 1500, 1500]

    # Release chain — climax to calm
    release_ids = [3045, 3042, 3041, 3043, 3040]
    release_holds_ms = [1500, 2000, 3000, 3000, 8000]

    # Color World cinematic accel — walk through all worlds faster and faster
    world_ids = [3000, 3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008]
    world_holds = _expo_holds(9, 4000, 500)

    return [
        ramp_chaser(3800, "RAMP - ACCEL SWEEP", sweep, accel_holds),
        ramp_chaser(3801, "RAMP - DECEL SWEEP", sweep, decel_holds),
        ramp_chaser(3802, "RAMP - CINEMATIC BUILD", build_ids, build_holds_ms),
        ramp_chaser(3803, "RAMP - AFTERGLOW RELEASE", release_ids, release_holds_ms),
        ramp_chaser(3804, "RAMP - WORLDS CRESCENDO", world_ids, world_holds),
        ramp_chaser(3805, "RAMP - WORLDS DIMINUENDO",
                    list(reversed(world_ids)), list(reversed(world_holds))),
        # Accel on ring matrix RGBMatrix functions — tasting menu
        ramp_chaser(3806, "RAMP - MATRIX TOUR",
                    [3700, 3701, 3703, 3704, 3706, 3707, 3708, 3712],
                    _expo_holds(8, 4000, 500)),
        # Ritardando on ring FX — fades the dance-floor into a breathe
        ramp_chaser(3807, "RAMP - FX DECAY",
                    [1753, 1757, 1750, 1200, 3740, 3741, 126],
                    [2000, 2000, 3000, 4000, 4000, 4000, 8000]),
        # Exponential ring-pulse accel — used as a "build" element
        ramp_chaser(3808, "RAMP - PULSE ACCEL",
                    sweep[:8] + sweep[:8],
                    _expo_holds(16, 400, 50)),
    ]


# ──────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────
def main() -> None:
    text = strip_functions(load_qxw(), OWNED)
    parts: list[str] = []
    parts.extend(build_darkness())
    parts.extend(build_phaser_seeds())
    parts.extend(build_phaser_chasers())
    parts.extend(build_surprise())
    parts.extend(build_ramp())
    save_qxw(inject_before_monitor(text, "\n".join(parts) + "\n"))
    print("OK: cosmic toolkit "
          "(dark 3740-3749, phaser seeds 3750-3759, phaser chasers 3760-3766, "
          "surprise 3770-3779, ramp 3800-3808)")


if __name__ == "__main__":
    main()
