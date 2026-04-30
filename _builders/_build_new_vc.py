# -*- coding: utf-8 -*-
"""
Zero Hour GZ Virtual Console — ground-up rebuild for dubstep/trap/bass-house/hard-techno.

10-page layout (grandMA3-style square executor grid, touchscreen-first):
  0 BUSK       universal DJ surface (faders, colors, O/I, motion, FX quick, drops, impact)
  1 DUBSTEP    genre page - growls, wobbles, neuro chops, riddim, drops
  2 TRAP       genre page - lean, triplets, 808 pulse, flex, entrance, drops
  3 BASS HOUSE genre page - groove, pump, filter sweep, tear drops, drops
  4 TECHNO     genre page - industrial, berghain, kick hammer, machine, drops
  5 COLOR      O/I splits, spatial splits, color worlds, per-ring color rows
  6 FX         ring FX pattern x color grid, ring RGBMatrix bank, motion bank
  7 IMPACT     strobe tiers, color strobes, bumps, bass hits, blinder flash
  8 ATMOSPHERE tunnel, white ring layers, soft FX grid, darkness, phaser
  9 DIRECTOR   emotional arcs, energy states, surprise, ramps, cosmic doctrine

All pages use CELL=120, SQ=114 square buttons. Page height 1080, width 1920.
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _widget_sizer import speed_dial_recommend_height

QXW = Path(__file__).resolve().parent.parent / "Zero Hour GZ Project File.qxw"
U0 = 'Universe="0"'
U3 = 'Universe="3"'
FONT = "Roboto Condensed,16,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"
THEME_BG = "4281545523"
BLACK_FG = "4278190080"

PAGE_W = 1920
PAGE_H = 1080
CELL = 120
GAP = 6
SQ = CELL - GAP  # 114


# ─────────────────────────────────── Color constants (ARGB) ───────────────────────────────────
ARGB_RED = "4294901760"
ARGB_ORANGE = "4294944000"
ARGB_YELLOW = "4294967040"
ARGB_GOLD = "4294954700"
ARGB_GREEN = "4278255360"
ARGB_CYAN = "4289374890"
ARGB_BLUE = "4278190335"
ARGB_PURPLE = "4286578816"
ARGB_WHITE = "4294967295"
ARGB_BLACK = "4278190080"
ARGB_DGRAY = "4281545523"
ARGB_CHARCOAL = "4282664004"
ARGB_WARM = "4289890816"
ARGB_AMBER = "4291611852"
ARGB_DEEPRED = "4286578816"  # also purple, reuse
ARGB_DARKPURP = "4283573504"
ARGB_CYAN_DEEP = "4278233600"
ARGB_WHITE_SOFT = "4284506208"
ARGB_GOLD_SOFT = "4291611852"
ARGB_MINT = "4288256409"

COLORS = [
    ("RED", ARGB_RED),
    ("ORA", ARGB_ORANGE),
    ("YEL", ARGB_YELLOW),
    ("GLD", ARGB_GOLD),
    ("GRN", ARGB_GREEN),
    ("CYN", ARGB_CYAN),
    ("BLU", ARGB_BLUE),
    ("PUR", ARGB_PURPLE),
]


# ─────────────────────────────────── Widget ID allocator ───────────────────────────────────
class WidgetAlloc:
    def __init__(self, base: int, limit: int) -> None:
        self._n = base
        self._limit = limit

    def take(self, n: int = 1) -> int:
        w = self._n
        self._n += n
        if self._n > self._limit + 1:
            raise OverflowError(f"Widget overflow: {self._n} > {self._limit}")
        return w

    @property
    def current(self) -> int:
        return self._n


# ─────────────────────────────────── Widget helpers ───────────────────────────────────
def _is_bright(argb: str) -> bool:
    v = int(argb)
    r, g, b = (v >> 16) & 0xFF, (v >> 8) & 0xFF, v & 0xFF
    return (r * 299 + g * 587 + b * 114) / 1000 > 150


def btn(caption: str, wid: int, x: int, y: int, w: int, h: int, fid: int,
        *, flash: bool = False, force_ltp: bool = False, stop_all: bool = False,
        bg: str | None = None) -> str:
    if stop_all:
        act = "<Action>StopAll</Action>"
    elif flash:
        ltp = "1" if force_ltp else "0"
        act = f'<Action Override="0" ForceLTP="{ltp}">Flash</Action>'
    else:
        act = "<Action>Toggle</Action>"
    app = ""
    if bg is not None:
        fg = f"\n      <ForegroundColor>{BLACK_FG}</ForegroundColor>" if _is_bright(bg) else ""
        app = (f"\n     <Appearance>\n      <BackgroundColor>{bg}</BackgroundColor>{fg}"
               "\n     </Appearance>")
    fn_attr = 4294967295 if stop_all else fid
    return (f'    <Button Caption="{escape(caption)}" ID="{wid}">\n'
            f'     <WindowState Visible="True" X="{x}" Y="{y}" Width="{w}" Height="{h}"/>{app}\n'
            f'     <Function ID="{fn_attr}"/>\n'
            f'     {act}\n'
            f'    </Button>')


def slider_pb(caption: str, wid: int, x: int, y: int, w: int, h: int,
              fn: int, *, initial: int = 0) -> str:
    return (f'    <Slider Caption="{escape(caption)}" ID="{wid}" '
            f'WidgetStyle="Slider" InvertedAppearance="false">\n'
            f'     <WindowState Visible="True" X="{x}" Y="{y}" Width="{w}" Height="{h}"/>\n'
            f'     <SliderMode ValueDisplayStyle="Percentage">Playback</SliderMode>\n'
            f'     <Level LowLimit="0" HighLimit="255" Value="{initial}"/>\n'
            f'     <Playback><Function>{fn}</Function></Playback>\n'
            f'    </Slider>')


def slider_gm(caption: str, wid: int, x: int, y: int, w: int, h: int) -> str:
    return (f'    <Slider Caption="{escape(caption)}" ID="{wid}" '
            f'WidgetStyle="Slider" InvertedAppearance="false">\n'
            f'     <WindowState Visible="True" X="{x}" Y="{y}" Width="{w}" Height="{h}"/>\n'
            f'     <SliderMode ValueDisplayStyle="Percentage">Submaster</SliderMode>\n'
            f'     <Level LowLimit="0" HighLimit="255" Value="255"/>\n'
            f'     <Playback><Function>4294967295</Function></Playback>\n'
            f'    </Slider>')


def vc_matrix(caption: str, wid: int, x: int, y: int, w: int, h: int, fn_id: int) -> str:
    return (f'    <Matrix Caption="{escape(caption)}" ID="{wid}">\n'
            f'     <WindowState Visible="True" X="{x}" Y="{y}" Width="{w}" Height="{h}"/>\n'
            f'     <Appearance>\n      <BackgroundColor>{THEME_BG}</BackgroundColor>\n     </Appearance>\n'
            f'     <Function ID="{fn_id}"/>\n'
            f'    </Matrix>')


def speed_dial(caption: str, wid: int, x: int, y: int, w: int, h: int,
               fn_ids: list[int], *, beat_mode: bool = False) -> str:
    assert fn_ids, "speed_dial: fn_ids must not be empty"
    req_h = h
    if beat_mode:
        visibility, t_min, t_max, t_default = 128, 50, 16000, 1000
    else:
        visibility, t_min, t_max, t_default = 65, 20, 2000, 150
    preset_count = 5 if (beat_mode and req_h >= 140) else 0
    h = speed_dial_recommend_height(beat_mode, visibility, req_h, preset_count, len(fn_ids))
    fn_tags = "\n".join(
        f'     <Function FadeIn="0" FadeOut="0" Duration="6">{fid}</Function>'
        for fid in fn_ids)
    preset_tags = ""
    if beat_mode and req_h >= 140:
        presets = [("1x", 1000, 16), ("2x", 2000, 17), ("4x", 4000, 18),
                   ("8x", 8000, 19), ("16x", 16000, 20)]
        preset_tags = "\n" + "\n".join(
            f'     <Preset ID="{pid}">\n      <Name>{n}</Name>\n      <Value>{v}</Value>\n     </Preset>'
            for n, v, pid in presets)
    return (f'    <SpeedDial Caption="{escape(caption)}" ID="{wid}">\n'
            f'     <WindowState Visible="True" X="{x}" Y="{y}" Width="{w}" Height="{h}"/>\n'
            f'     <Visibility>{visibility}</Visibility>\n'
            f'     <AbsoluteValue Minimum="{t_min}" Maximum="{t_max}"/>\n'
            f'     <Time>{t_default}</Time>\n'
            f'{fn_tags}{preset_tags}\n'
            f'    </SpeedDial>')


def label(caption: str, wid: int, x: int, y: int, w: int, h: int, bg: str = ARGB_DGRAY) -> str:
    fg = f"\n      <ForegroundColor>{BLACK_FG}</ForegroundColor>" if _is_bright(bg) else ""
    return (f'    <Button Caption="{escape(caption)}" ID="{wid}">\n'
            f'     <WindowState Visible="True" X="{x}" Y="{y}" Width="{w}" Height="{h}"/>\n'
            f'     <Appearance>\n      <BackgroundColor>{bg}</BackgroundColor>{fg}\n     </Appearance>\n'
            f'     <Function ID="4294967295"/>\n'
            f'     <Action>Toggle</Action>\n'
            f'    </Button>')


def solo_open(caption: str, wid: int, x: int, y: int, w: int, h: int) -> str:
    return (f'    <SoloFrame Caption="{escape(caption)}" ID="{wid}">\n'
            f'     <WindowState Visible="True" X="{x}" Y="{y}" Width="{w}" Height="{h}"/>\n'
            f'     <AllowResize>False</AllowResize>\n'
            f'     <ShowHeader>True</ShowHeader>\n'
            f'     <ShowEnableButton>False</ShowEnableButton>\n'
            f'     <Collapsed>False</Collapsed>\n'
            f'     <Disabled>False</Disabled>')


def solo_close() -> str:
    return "    </SoloFrame>"


def page_header(page_id: int, caption: str) -> str:
    return (f'  <Frame Caption="{escape(caption)}" ID="{page_id}">\n'
            f'   <Appearance>\n    <Font>{FONT}</Font>\n'
            f'    <BackgroundColor>{THEME_BG}</BackgroundColor>\n   </Appearance>\n'
            f'   <WindowState Visible="True" X="0" Y="0" Width="{PAGE_W}" Height="{PAGE_H}"/>\n'
            f'   <AllowResize>False</AllowResize>\n   <ShowHeader>False</ShowHeader>\n'
            f'   <ShowEnableButton>True</ShowEnableButton>\n   <Collapsed>False</Collapsed>\n'
            f'   <Disabled>False</Disabled>\n'
            f'   <Frame Caption="{escape(caption)} - content" ID="{9000 + page_id}">\n'
            f'    <WindowState Visible="True" X="0" Y="0" Width="{PAGE_W}" Height="{PAGE_H}"/>\n'
            f'    <AllowResize>False</AllowResize>\n    <ShowHeader>False</ShowHeader>\n'
            f'    <ShowEnableButton>False</ShowEnableButton>\n    <Collapsed>False</Collapsed>\n'
            f'    <Disabled>False</Disabled>')


def page_footer() -> str:
    return "   </Frame>\n  </Frame>"


# ─────────────────────────────────── Common function pools ───────────────────────────────────
RING_FX_ALL = (list(range(1750, 1758)) + list(range(1770, 1778))
               + list(range(2850, 2906)) + list(range(3100, 3156)))
RING_MATRIX_ALL = list(range(3700, 3730))
MOTION_ALL = list(range(1200, 1213)) + list(range(1300, 1312)) + list(range(1510, 1516)) + [71]
STROBE_RATE_CHASERS = list(range(94, 114))
STROBE_COLLECTIONS = [2918, 2919, 2921, 2923]
PANEL_MATRIX_FN_IDS = list(range(475, 484))
ACCEL_ALL = list(range(3200, 3264))

# Genre drops (5 each)
DUB_DROPS = [3835, 3836, 3837, 3838, 3839]
TRAP_DROPS = [3865, 3866, 3867, 3868, 3869]
BH_DROPS = [3895, 3896, 3897, 3898, 3899]
TECHNO_DROPS = [3926, 3927, 3928, 3929]  # only 4 for techno

# Genre chasers
DUB_CHASERS = [3830, 3831, 3832, 3833, 3834]
TRAP_CHASERS = [3860, 3861, 3862, 3863, 3864]
BH_CHASERS = [3890, 3891, 3892, 3893, 3894]
TECHNO_CHASERS = [3920, 3921, 3922, 3923, 3924]

# Genre scene palettes (for one-tap looks without FX)
DUB_SCENES = [3820, 3821, 3822, 3823, 3824, 3825, 3826, 3827, 3828, 3829]
TRAP_SCENES = [3850, 3851, 3852, 3853, 3854, 3855, 3856, 3857, 3858, 3859]
BH_SCENES = [3880, 3881, 3882, 3883, 3884, 3885, 3886, 3887, 3888, 3889]
TECHNO_SCENES = [3910, 3911, 3912, 3913, 3914, 3915, 3916, 3917, 3918, 3919]


# ─────────────────────────────────── Layout helpers ───────────────────────────────────
def grid_row_square(alloc: WidgetAlloc, items: list[tuple[str, int, str]],
                    x0: int, y: int, cell: int = CELL, sq: int = SQ) -> list[str]:
    """Place items as a square row of buttons with given bg colors."""
    out = []
    for i, (cap, fid, bg) in enumerate(items):
        out.append(btn(cap, alloc.take(), x0 + i * cell, y, sq, sq, fid, bg=bg))
    return out


def grid_row_flash(alloc: WidgetAlloc, items: list[tuple[str, int, str]],
                   x0: int, y: int, *, force_ltp: bool = False,
                   cell: int = CELL, sq: int = SQ) -> list[str]:
    out = []
    for cap, fid, bg in items:
        out.append(btn(cap, alloc.take(), x0, y, sq, sq, fid,
                       flash=True, force_ltp=force_ltp, bg=bg))
        x0 += cell
    return out


# ───────────────── PAGE 0: BUSK ─────────────────
def page_busk() -> str:
    PID = 0
    a = WidgetAlloc(10000, 10999)
    out = [page_header(PID, "BUSK")]

    # Top row: faders + 3 speed dials
    # Faders (9) at x=0..1080 y=0 h=200
    fader_defs = [
        ("GRAND", 4294967295, "sub"),
        ("RING", 1120, "sub"),
        ("OUTER", 1121, "sub"),
        ("INNER", 1122, "sub"),
        ("WHT RG", 67, "pb"),
        ("BLIND", 43, "pb"),
        ("COB", 47, "pb"),
        ("A55", 51, "pb"),
        ("PANEL", 55, "pb"),
    ]
    for i, (cap, fn, mode) in enumerate(fader_defs):
        x = i * 120
        if mode == "sub":
            out.append(slider_gm(cap, a.take(), x, 0, 114, 200))
        else:
            out.append(slider_pb(cap, a.take(), x, 0, 114, 200, fn))

    # Speed dials at x=1090.. y=0 h=200
    out.append(speed_dial("FX SPD", a.take(), 1090, 0, 260, 200,
                          RING_FX_ALL, beat_mode=True))
    out.append(speed_dial("MX SPD", a.take(), 1360, 0, 260, 200,
                          RING_MATRIX_ALL + PANEL_MATRIX_FN_IDS, beat_mode=True))
    out.append(speed_dial("MOT SPD", a.take(), 1630, 0, 260, 200,
                          MOTION_ALL, beat_mode=True))

    # Row 1 (y=210): RING COLORS (full ring bars) — solo'd color scenes
    out.append(solo_open("COLORS", a.take(), 0, 210, 1200, 114))
    color_row = [
        ("RED", 1100, ARGB_RED),
        ("ORG", 1101, ARGB_ORANGE),
        ("YEL", 1102, ARGB_YELLOW),
        ("GLD", 1103, ARGB_GOLD),
        ("GRN", 1104, ARGB_GREEN),
        ("CYN", 1105, ARGB_CYAN),
        ("BLU", 1106, ARGB_BLUE),
        ("PUR", 1107, ARGB_PURPLE),
        ("WHT", 1120, ARGB_WHITE),
        ("BO", 1108, ARGB_BLACK),
    ]
    for i, (cap, fn, bg) in enumerate(color_row):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row 2 (y=330): O/I SPLITS
    out.append(solo_open("O/I SPLITS", a.take(), 0, 330, 1200, 114))
    split_row = [
        ("R/BL", 1400, ARGB_RED), ("BL/R", 1401, ARGB_BLUE),
        ("GLD/PUR", 1402, ARGB_GOLD), ("PUR/GLD", 1403, ARGB_PURPLE),
        ("CYN/ORG", 1404, ARGB_CYAN), ("ORG/CYN", 1405, ARGB_ORANGE),
        ("W/R", 1408, ARGB_WHITE), ("W/BL", 1409, ARGB_WHITE),
        ("W/PUR", 1410, ARGB_WHITE), ("GRN/PUR", 1414, ARGB_GREEN),
    ]
    for i, (cap, fn, bg) in enumerate(split_row):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row 3 (y=450): SPATIAL splits (COB+A55 front/back)
    out.append(solo_open("SPATIAL", a.take(), 0, 450, 1200, 114))
    spatial_row = [
        ("WRM/COLD", 3020, ARGB_WARM),
        ("R/BL", 3021, ARGB_RED),
        ("GLD/PUR", 3022, ARGB_GOLD),
        ("CYN/ORG", 3023, ARGB_CYAN),
        ("GRN/R", 3024, ARGB_GREEN),
        ("W/R", 3025, ARGB_WHITE),
        ("W/BL", 3026, ARGB_WHITE),
        ("PUR/GLD", 3027, ARGB_PURPLE),
        ("ORG/CYN", 3028, ARGB_ORANGE),
        ("BL/GLD", 3029, ARGB_BLUE),
    ]
    for i, (cap, fn, bg) in enumerate(spatial_row):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row 4 (y=570): MOTION (panel+cob chases)
    out.append(solo_open("MOTION", a.take(), 0, 570, 1200, 114))
    motion_row = [
        ("CW SOFT", 1200, ARGB_DGRAY),
        ("F/B SOFT", 1201, ARGB_DGRAY),
        ("L/R SOFT", 1202, ARGB_DGRAY),
        ("DIAG SFT", 1203, ARGB_DGRAY),
        ("CW PP", 1300, ARGB_CHARCOAL),
        ("F/B PP", 1301, ARGB_CHARCOAL),
        ("L/R PP", 1302, ARGB_CHARCOAL),
        ("R WAVE", 1510, ARGB_DGRAY),
        ("I WAVE", 1512, ARGB_DGRAY),
        ("R PULSE", 1514, ARGB_DGRAY),
    ]
    for i, (cap, fn, bg) in enumerate(motion_row):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row 5 (y=690): RING FX QUICK
    out.append(solo_open("RING FX", a.take(), 0, 690, 1200, 114))
    fx_row = [
        ("SWP CW", 1750, ARGB_DGRAY),
        ("SWP CCW", 1751, ARGB_DGRAY),
        ("SWP PP", 1752, ARGB_DGRAY),
        ("BAR CW", 1753, ARGB_DGRAY),
        ("BAR CCW", 1754, ARGB_DGRAY),
        ("BAR PP", 1755, ARGB_DGRAY),
        ("HALF", 1756, ARGB_DGRAY),
        ("DUAL CW", 1757, ARGB_DGRAY),
        ("MX WAVE", 3700, ARGB_DGRAY),
        ("MX FILL", 3703, ARGB_DGRAY),
    ]
    for i, (cap, fn, bg) in enumerate(fx_row):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row 6 (y=810): DUBSTEP 5 + TRAP 5 drops
    out.append(solo_open("DUBSTEP & TRAP DROPS", a.take(), 0, 810, 1200, 114))
    drop1 = [
        ("DUB CLS", 3835, ARGB_RED),
        ("DUB NRO", 3836, ARGB_RED),
        ("DUB RDM", 3837, ARGB_RED),
        ("DUB MTL", 3838, ARGB_RED),
        ("DUB PUR", 3839, ARGB_PURPLE),
        ("TRP GTA", 3865, ARGB_GOLD),
        ("TRP FLX", 3866, ARGB_GOLD),
        ("TRP NL", 3867, ARGB_GOLD),
        ("TRP SWG", 3868, ARGB_GOLD),
        ("TRP MAF", 3869, ARGB_GOLD),
    ]
    for i, (cap, fn, bg) in enumerate(drop1):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row 7 (y=930): BH 5 + TECHNO 4 drops + BO+HIT
    out.append(solo_open("BASS HOUSE & TECHNO DROPS", a.take(), 0, 930, 1200, 114))
    drop2 = [
        ("BH CLS", 3895, ARGB_CYAN),
        ("BH FST", 3896, ARGB_CYAN),
        ("BH UK", 3897, ARGB_CYAN),
        ("BH DUT", 3898, ARGB_CYAN),
        ("BH DEP", 3899, ARGB_CYAN),
        ("TEC HMR", 3926, ARGB_WHITE),
        ("TEC UND", 3927, ARGB_WHITE),
        ("TEC WHS", 3928, ARGB_WHITE),
        ("TEC PK", 3929, ARGB_WHITE),
        ("BO+HIT", 3073, ARGB_YELLOW),
    ]
    for i, (cap, fn, bg) in enumerate(drop2):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Right column: Safety stack (x=1210..1910)
    out.append(solo_open("SAFETY", a.take(), 1210, 210, 700, 834))
    safety_y = 3
    out.append(btn("FULL BO", a.take(), 3, safety_y, 340, 160, 126, flash=True, force_ltp=True, bg=ARGB_BLACK))
    out.append(btn("ALL OFF", a.take(), 350, safety_y, 340, 160, 0, stop_all=True, bg=ARGB_ORANGE))
    out.append(btn("PANIC", a.take(), 3, safety_y + 170, 340, 160, 3060, bg=ARGB_RED))
    out.append(btn("BUMP W", a.take(), 350, safety_y + 170, 340, 160, 3070, flash=True, bg=ARGB_WHITE))
    out.append(btn("BUMP WR", a.take(), 3, safety_y + 340, 340, 160, 3071, flash=True, bg=ARGB_AMBER))
    out.append(btn("DECAY", a.take(), 350, safety_y + 340, 340, 160, 3072, bg=ARGB_GOLD))
    out.append(btn("STR MED", a.take(), 3, safety_y + 510, 340, 150, 2919, flash=True, bg=ARGB_YELLOW))
    out.append(btn("STR FST", a.take(), 350, safety_y + 510, 340, 150, 2921, flash=True, bg=ARGB_ORANGE))
    out.append(btn("STR BLZ", a.take(), 3, safety_y + 665, 340, 150, 2923, flash=True, bg=ARGB_RED))
    out.append(btn("BASS HIT", a.take(), 350, safety_y + 665, 340, 150, 3509, flash=True, bg=ARGB_PURPLE))
    out.append(solo_close())

    out.append(page_footer())
    return "\n".join(out)


def _genre_page(page_id: int, title: str, base: int, theme_bg: str,
                scenes: list[tuple[str, int]],
                chasers: list[tuple[str, int]],
                drops: list[tuple[str, int]],
                dial_caption: str, dial_fns: list[int],
                extra_support: list[tuple[str, int, str]],
                palette_scenes: list[tuple[str, int, str]],
                motion_row: list[tuple[str, int, str]]) -> str:
    """Shared layout for the 4 genre pages.
    
    Grid (1200w main, 710w right column):
      y=0-114  Row A: 10 scenes (8 main scenes + 2 palette accents) [SoloFrame]
      y=120-234 Row B: 5 chasers (genre rhythm patterns) + 5 matching ring FX
      y=240-354 Row C: 5 drops (DROP collections) + 5 supporting looks
      y=360-474 Row D: impact row (strobes, bumps, bass hit, BO+HIT, BO FLASH)
      y=480-594 Row E: palette scenes (10 color options, tuned to genre)
      y=600-714 Row F: motion/chase support (10 ring chases)
      y=720-834 Row G: genre chasers tier 2 (remaining 5 scenes/chasers + 5 extras)
      y=840-1044 Row H: quick safety + speed dial + BPM footer
    
    Right column (x=1210-1910, y=0-834): big DROP + SAFETY stack
    """
    a = WidgetAlloc(base, base + 999)
    out = [page_header(page_id, title)]

    # ── ROW A: scenes (10 slots) ──
    out.append(solo_open(f"{title} - PALETTE", a.take(), 0, 0, 1200, 114))
    for i, (cap, fn) in enumerate(scenes[:10]):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=theme_bg))
    out.append(solo_close())

    # ── ROW B: chasers (5) + 5 ring FX ──
    out.append(solo_open(f"{title} - RHYTHM", a.take(), 0, 120, 1200, 114))
    row_b_items = chasers[:5] + [
        ("BAR CW", 1753), ("DUAL CW", 1757), ("HALF", 1756),
        ("MX FILL", 3703), ("MX WAVE", 3700),
    ]
    for i, (cap, fn) in enumerate(row_b_items):
        bg = ARGB_CHARCOAL if i < 5 else ARGB_DGRAY
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # ── ROW C: drops (up to 5) + support (up to 5) ──
    out.append(solo_open(f"{title} - DROPS", a.take(), 0, 240, 1200, 114))
    row_c_drops = [(c, f, theme_bg) for c, f in drops[:5]]
    row_c_full = row_c_drops + list(extra_support[:5])
    # Pad to exactly 10 if needed
    while len(row_c_full) < 10:
        row_c_full.append(("", 4294967295, ARGB_DGRAY))
    for i, (cap, fn, bg) in enumerate(row_c_full[:10]):
        if cap:
            out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # ── ROW D: IMPACT (strobes, bumps, BO+HIT, BUMP, BASS HIT) ──
    out.append(solo_open(f"{title} - IMPACT", a.take(), 0, 360, 1200, 114))
    impact_row = [
        ("STR SLW", 2918, ARGB_ORANGE),
        ("STR MED", 2919, ARGB_YELLOW),
        ("STR FST", 2921, ARGB_ORANGE),
        ("STR BLZ", 2923, ARGB_RED),
        ("BUMP W", 3070, ARGB_WHITE),
        ("BUMP WR", 3071, ARGB_AMBER),
        ("BO+HIT", 3073, ARGB_YELLOW),
        ("BASS FB", 3502, ARGB_PURPLE),
        ("BASS A55", 3505, ARGB_CYAN),
        ("BASS QD", 3509, ARGB_GOLD),
    ]
    flash_idx = {0, 1, 2, 3, 4, 5, 8, 9}  # indexes that should flash
    for i, (cap, fn, bg) in enumerate(impact_row):
        flash = i in flash_idx
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn,
                       flash=flash, force_ltp=flash, bg=bg))
    out.append(solo_close())

    # ── ROW E: palette (genre-tuned color row) ──
    out.append(solo_open(f"{title} - COLORS", a.take(), 0, 480, 1200, 114))
    for i, (cap, fn, bg) in enumerate(palette_scenes[:10]):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # ── ROW F: motion / chase support (10 slots) ──
    out.append(solo_open(f"{title} - MOTION", a.take(), 0, 600, 1200, 114))
    for i, (cap, fn, bg) in enumerate(motion_row[:10]):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # ── ROW G: genre tier-2 (remaining scenes) ──
    out.append(solo_open(f"{title} - TIER 2", a.take(), 0, 720, 1200, 114))
    extra_scenes = scenes[10:] if len(scenes) > 10 else []
    tier2 = extra_scenes + chasers[5:]  # chasers 5 extras if any
    # Pad to 10 with empty
    for i, (cap, fn) in enumerate(tier2[:10]):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=theme_bg))
    out.append(solo_close())

    # ── Right column: BIG DROPS + SAFETY ──
    out.append(solo_open(f"{title} - MASTER", a.take(), 1210, 0, 700, 834))
    out.append(btn(drops[0][0], a.take(), 3, 3, 690, 180, drops[0][1], bg=theme_bg))
    if len(drops) > 1:
        out.append(btn(drops[1][0], a.take(), 3, 190, 340, 120, drops[1][1], bg=theme_bg))
    if len(drops) > 2:
        out.append(btn(drops[2][0], a.take(), 350, 190, 340, 120, drops[2][1], bg=theme_bg))
    if len(drops) > 3:
        out.append(btn(drops[3][0], a.take(), 3, 316, 340, 120, drops[3][1], bg=theme_bg))
    if len(drops) > 4:
        out.append(btn(drops[4][0], a.take(), 350, 316, 340, 120, drops[4][1], bg=theme_bg))
    out.append(btn("FULL BO", a.take(), 3, 445, 340, 115, 126,
                   flash=True, force_ltp=True, bg=ARGB_BLACK))
    out.append(btn("ALL OFF", a.take(), 350, 445, 340, 115, 0,
                   stop_all=True, bg=ARGB_ORANGE))
    out.append(btn("PANIC", a.take(), 3, 566, 340, 115, 3060, bg=ARGB_RED))
    out.append(btn("BUMP W", a.take(), 350, 566, 340, 115, 3070,
                   flash=True, bg=ARGB_WHITE))
    out.append(speed_dial(dial_caption, a.take(), 3, 690, 687, 140,
                          dial_fns, beat_mode=True))
    out.append(solo_close())

    # ── ROW H: footer quick-safety (x=0-1200 y=840) ──
    out.append(solo_open(f"{title} - QUICK", a.take(), 0, 840, 1200, 204))
    quick_row = [
        ("FULL BO", 126, ARGB_BLACK, True, True),
        ("BUMP W", 3070, ARGB_WHITE, True, False),
        ("BUMP WR", 3071, ARGB_AMBER, True, False),
        ("BO+HIT", 3073, ARGB_YELLOW, False, False),
        ("PANIC", 3060, ARGB_RED, False, False),
    ]
    for i, (cap, fn, bg, flash, ltp) in enumerate(quick_row):
        out.append(btn(cap, a.take(), 3 + i * 240, 3, 234, 200, fn,
                       flash=flash, force_ltp=ltp, bg=bg))
    out.append(solo_close())

    out.append(page_footer())
    return "\n".join(out)


# ───────────────── PAGE 1: DUBSTEP ─────────────────
def page_dubstep() -> str:
    scenes = [
        ("GROWL", 3820), ("WOB HI", 3821), ("WOB LO", 3822),
        ("DROP F", 3823), ("METAL", 3824), ("N BLK", 3825),
        ("N WHT", 3826), ("PUR SW", 3827), ("CANNON", 3828),
        ("RIDDIM", 3829),
    ]
    chasers = [
        ("WOB 1/8", 3830), ("WOB 1/16", 3831), ("N CHOP", 3832),
        ("STRIKE", 3833), ("RDM PAT", 3834),
    ]
    drops = [
        ("CLASSIC", 3835), ("NEURO", 3836), ("RIDDIM", 3837),
        ("METAL", 3838), ("PUR SWELL", 3839),
    ]
    support = [
        ("SWP CW", 1750, ARGB_RED),
        ("SWP CCW", 1751, ARGB_RED),
        ("OI R>BL", 2070, ARGB_RED),
        ("OI BL>R", 2071, ARGB_BLUE),
        ("DUAL CW", 1757, ARGB_PURPLE),
    ]
    palette = [
        ("RED", 1100, ARGB_RED),
        ("PUR", 1107, ARGB_PURPLE),
        ("WHT", 1120, ARGB_WHITE),
        ("BL", 1106, ARGB_BLUE),
        ("BO", 1108, ARGB_BLACK),
        ("R/BL", 1400, ARGB_RED),
        ("BL/R", 1401, ARGB_BLUE),
        ("PUR/GLD", 1403, ARGB_PURPLE),
        ("W/R", 1408, ARGB_WHITE),
        ("WLD VOID", 3009, ARGB_BLACK),
    ]
    motion = [
        ("CW SOFT", 1200, ARGB_DGRAY),
        ("F/B SOFT", 1201, ARGB_DGRAY),
        ("CW PP", 1300, ARGB_CHARCOAL),
        ("F/B PP", 1301, ARGB_CHARCOAL),
        ("DIAG PP", 1303, ARGB_CHARCOAL),
        ("BAR CCW", 1754, ARGB_DGRAY),
        ("SWP R", 1770, ARGB_RED),
        ("BAR R", 2874, ARGB_RED),
        ("BAR PUR", 2880, ARGB_PURPLE),
        ("MX NOISE", 3711, ARGB_DGRAY),
    ]
    return _genre_page(1, "DUBSTEP", 11000, ARGB_RED,
                       scenes, chasers, drops,
                       "DUB FX SPEED",
                       list(range(3830, 3835)) + list(range(3700, 3731)) + [2921, 2923],
                       support, palette, motion)


# ───────────────── PAGE 2: TRAP ─────────────────
def page_trap() -> str:
    scenes = [
        ("LEAN", 3850), ("MAFIA", 3851), ("808 DRK", 3852),
        ("TRIP FL", 3853), ("GRITTY", 3854), ("ACE", 3855),
        ("FLEX", 3856), ("808 ON", 3857), ("808 OFF", 3858),
        ("SWAGGER", 3859),
    ]
    chasers = [
        ("TRIPLET", 3860), ("LEAN DR", 3861), ("808 PLS", 3862),
        ("GRT STB", 3863), ("ENTRAN", 3864),
    ]
    drops = [
        ("GUTTA", 3865), ("FLEX", 3866), ("NO LIMIT", 3867),
        ("SWAGGER", 3868), ("MAFIA", 3869),
    ]
    support = [
        ("OI G>P", 2072, ARGB_GOLD),
        ("OI P>G", 2073, ARGB_PURPLE),
        ("DUAL G", 2873, ARGB_GOLD),
        ("DUAL P", 2872, ARGB_PURPLE),
        ("BAR P", 2880, ARGB_PURPLE),
    ]
    palette = [
        ("GOLD", 1103, ARGB_GOLD),
        ("PUR", 1107, ARGB_PURPLE),
        ("ORG", 1101, ARGB_ORANGE),
        ("RED", 1100, ARGB_RED),
        ("WHT", 1120, ARGB_WHITE),
        ("G/P", 1402, ARGB_GOLD),
        ("P/G", 1403, ARGB_PURPLE),
        ("W/PUR", 1410, ARGB_WHITE),
        ("WLD UV", 3006, ARGB_PURPLE),
        ("BO", 1108, ARGB_BLACK),
    ]
    motion = [
        ("CW SOFT", 1200, ARGB_DGRAY),
        ("F/B SFT", 1201, ARGB_DGRAY),
        ("L/R SFT", 1202, ARGB_DGRAY),
        ("DIAG SFT", 1203, ARGB_DGRAY),
        ("TRAP GP", 1204, ARGB_GOLD),
        ("CW PP", 1300, ARGB_CHARCOAL),
        ("F/B PP", 1301, ARGB_CHARCOAL),
        ("SWP G", 1777, ARGB_GOLD),
        ("SWP P", 1776, ARGB_PURPLE),
        ("MX GRAD", 3708, ARGB_GOLD),
    ]
    return _genre_page(2, "TRAP", 12000, ARGB_GOLD,
                       scenes, chasers, drops,
                       "TRAP FX SPEED",
                       list(range(3860, 3865)) + list(range(3700, 3731)) + [2919, 2921],
                       support, palette, motion)


# ───────────────── PAGE 3: BASS HOUSE ─────────────────
def page_bass_house() -> str:
    scenes = [
        ("GROOVE", 3880), ("PUMP UP", 3881), ("PMP DN", 3882),
        ("FLT HI", 3883), ("FLT LO", 3884), ("DROP HT", 3885),
        ("TEARDRP", 3886), ("HOUSE L", 3887), ("UK GRG", 3888),
        ("DUTCH", 3889),
    ]
    chasers = [
        ("GRV PLS", 3890), ("PUMP COMP", 3891), ("FLT SWP", 3892),
        ("TEAR PLS", 3893), ("HOUSE GV", 3894),
    ]
    drops = [
        ("CLASSIC", 3895), ("FESTIVAL", 3896), ("UK GARAGE", 3897),
        ("DUTCH", 3898), ("DEEP", 3899),
    ]
    support = [
        ("OI C>O", 2074, ARGB_CYAN),
        ("OI O>C", 2075, ARGB_ORANGE),
        ("DUAL C", 2870, ARGB_CYAN),
        ("DUAL O", 2867, ARGB_ORANGE),
        ("BAR C", 2878, ARGB_CYAN),
    ]
    palette = [
        ("CYN", 1105, ARGB_CYAN),
        ("ORG", 1101, ARGB_ORANGE),
        ("GLD", 1103, ARGB_GOLD),
        ("YEL", 1102, ARGB_YELLOW),
        ("WHT", 1120, ARGB_WHITE),
        ("C/O", 1404, ARGB_CYAN),
        ("O/C", 1405, ARGB_ORANGE),
        ("W/C", 1411, ARGB_WHITE),
        ("WLD AUR", 3007, ARGB_GREEN),
        ("BO", 1108, ARGB_BLACK),
    ]
    motion = [
        ("CW SOFT", 1200, ARGB_DGRAY),
        ("F/B SFT", 1201, ARGB_DGRAY),
        ("L/R SFT", 1202, ARGB_DGRAY),
        ("BH COI", 1205, ARGB_CYAN),
        ("CW PP", 1300, ARGB_CHARCOAL),
        ("F/B PP", 1301, ARGB_CHARCOAL),
        ("SWP C", 1774, ARGB_CYAN),
        ("SWP O", 1771, ARGB_ORANGE),
        ("SWP GLD", 1777, ARGB_GOLD),
        ("MX SINE", 3710, ARGB_CYAN),
    ]
    return _genre_page(3, "BASS HOUSE", 13000, ARGB_CYAN,
                       scenes, chasers, drops,
                       "BH FX SPEED",
                       list(range(3890, 3895)) + list(range(3700, 3731)) + [2919, 2921],
                       support, palette, motion)


# ───────────────── PAGE 4: HARD TECHNO ─────────────────
def page_techno() -> str:
    scenes = [
        ("INDUST", 3910), ("BRGHN", 3911), ("KICK FL", 3912),
        ("RED MIN", 3913), ("MCH ON", 3914), ("MCH OFF", 3915),
        ("BLOOD", 3916), ("VOID R", 3917), ("WRHOUSE", 3918),
        ("PEAK T", 3919),
    ]
    chasers = [
        ("HAMMER", 3920), ("IND STB", 3921), ("BRG PLS", 3922),
        ("MACHINE", 3923), ("VOID BR", 3924),
    ]
    drops = [
        ("HAMMER", 3926), ("UNDRGR", 3927), ("WRHOUSE", 3928),
        ("PEAK TM", 3929),
    ]
    support = [
        ("WHT RNG", 67, ARGB_WHITE),
        ("SWP W", 71, ARGB_WHITE),
        ("SWP R", 1770, ARGB_RED),
        ("BAR R", 2874, ARGB_RED),
        ("HALF R", 2898, ARGB_RED),
    ]
    palette = [
        ("WHT", 1120, ARGB_WHITE),
        ("RED", 1100, ARGB_RED),
        ("BO", 1108, ARGB_BLACK),
        ("BL", 1106, ARGB_BLUE),
        ("PUR", 1107, ARGB_PURPLE),
        ("W/R", 1408, ARGB_WHITE),
        ("W/BL", 1409, ARGB_WHITE),
        ("WLD INF", 3000, ARGB_RED),
        ("WLD VD", 3009, ARGB_BLACK),
        ("WLD UV", 3006, ARGB_PURPLE),
    ]
    motion = [
        ("CW SOFT", 1200, ARGB_DGRAY),
        ("F/B SFT", 1201, ARGB_DGRAY),
        ("DUAL W", 71, ARGB_WHITE),
        ("SWP CW", 1750, ARGB_WHITE),
        ("SWP CCW", 1751, ARGB_WHITE),
        ("BAR CW", 1753, ARGB_WHITE),
        ("BAR CCW", 1754, ARGB_WHITE),
        ("HALF", 1756, ARGB_WHITE),
        ("MX FILL", 3703, ARGB_WHITE),
        ("MX NOIS", 3711, ARGB_RED),
    ]
    return _genre_page(4, "HARD TECHNO", 14000, ARGB_WHITE,
                       scenes, chasers, drops,
                       "TECHNO FX SPEED",
                       list(range(3920, 3925)) + list(range(3700, 3731)) + [2921, 2923],
                       support, palette, motion)


# ───────────────── PAGE 5: COLOR ─────────────────
def page_color() -> str:
    a = WidgetAlloc(15000, 15999)
    out = [page_header(5, "COLOR")]

    # Row A y=0-114: COLOR WORLDS
    out.append(solo_open("COLOR WORLDS", a.take(), 0, 0, 1200, 114))
    worlds = [
        ("INFERNO", 3000, ARGB_RED),
        ("EMBER", 3001, ARGB_ORANGE),
        ("SOLAR", 3002, ARGB_YELLOW),
        ("VERDANT", 3003, ARGB_GREEN),
        ("ARCTIC", 3004, ARGB_CYAN),
        ("OCEAN", 3005, ARGB_BLUE),
        ("UV", 3006, ARGB_PURPLE),
        ("AURORA", 3007, ARGB_MINT),
        ("PRISM", 3008, ARGB_WHITE),
        ("VOID", 3009, ARGB_BLACK),
    ]
    for i, (cap, fn, bg) in enumerate(worlds):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row B y=120: RING FULL COLORS
    out.append(solo_open("RING FULL", a.take(), 0, 120, 1200, 114))
    full_row = [
        ("RED", 1100, ARGB_RED), ("ORG", 1101, ARGB_ORANGE),
        ("YEL", 1102, ARGB_YELLOW), ("GLD", 1103, ARGB_GOLD),
        ("GRN", 1104, ARGB_GREEN), ("CYN", 1105, ARGB_CYAN),
        ("BLU", 1106, ARGB_BLUE), ("PUR", 1107, ARGB_PURPLE),
        ("WHT", 1120, ARGB_WHITE), ("BO", 1108, ARGB_BLACK),
    ]
    for i, (cap, fn, bg) in enumerate(full_row):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row C y=240: O/I SPLITS
    out.append(solo_open("O/I SPLITS", a.take(), 0, 240, 1200, 114))
    oi_splits = [
        ("R/BL", 1400, ARGB_RED), ("BL/R", 1401, ARGB_BLUE),
        ("G/P", 1402, ARGB_GOLD), ("P/G", 1403, ARGB_PURPLE),
        ("C/O", 1404, ARGB_CYAN), ("O/C", 1405, ARGB_ORANGE),
        ("GRN/R", 1406, ARGB_GREEN), ("YEL/BL", 1407, ARGB_YELLOW),
        ("W/R", 1408, ARGB_WHITE), ("W/BL", 1409, ARGB_WHITE),
    ]
    for i, (cap, fn, bg) in enumerate(oi_splits):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row D y=360: O/I CHASES (colored)
    out.append(solo_open("O/I CHASES", a.take(), 0, 360, 1200, 114))
    oi_chases = [
        ("R", 2060, ARGB_RED), ("ORG", 2061, ARGB_ORANGE),
        ("YEL", 2062, ARGB_YELLOW), ("GRN", 2063, ARGB_GREEN),
        ("CYN", 2064, ARGB_CYAN), ("BLU", 2065, ARGB_BLUE),
        ("PUR", 2066, ARGB_PURPLE), ("GLD", 2067, ARGB_GOLD),
        ("R>BL", 2070, ARGB_RED), ("G>P", 2072, ARGB_GOLD),
    ]
    for i, (cap, fn, bg) in enumerate(oi_chases):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row E y=480: SPATIAL (row 1)
    out.append(solo_open("SPATIAL - F/B (1)", a.take(), 0, 480, 1200, 114))
    sp1 = [
        ("W/C", 3020, ARGB_WARM), ("R/BL", 3021, ARGB_RED),
        ("G/P", 3022, ARGB_GOLD), ("C/O", 3023, ARGB_CYAN),
        ("GRN/R", 3024, ARGB_GREEN), ("W/R", 3025, ARGB_WHITE),
        ("W/BL", 3026, ARGB_WHITE), ("P/G", 3027, ARGB_PURPLE),
        ("O/C", 3028, ARGB_ORANGE), ("BL/G", 3029, ARGB_BLUE),
    ]
    for i, (cap, fn, bg) in enumerate(sp1):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row F y=600: SPATIAL (row 2)
    out.append(solo_open("SPATIAL - F/B (2)", a.take(), 0, 600, 1200, 114))
    sp2 = [
        ("BL/R", 3030, ARGB_BLUE), ("C/P", 3031, ARGB_CYAN),
        ("G/GRN", 3032, ARGB_GOLD), ("R/G", 3033, ARGB_RED),
        ("W/C", 3034, ARGB_WHITE), ("O/BL", 3035, ARGB_ORANGE),
        ("P/C", 3036, ARGB_PURPLE), ("GRN/G", 3037, ARGB_GREEN),
        ("Y/BL", 3038, ARGB_YELLOW), ("G/R", 3039, ARGB_GOLD),
    ]
    for i, (cap, fn, bg) in enumerate(sp2):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row G y=720: OUTER + INNER per-color
    out.append(solo_open("OUTER RING", a.take(), 0, 720, 600, 114))
    outer_row = [
        ("R", 17, ARGB_RED), ("PUR", 114, ARGB_PURPLE),
        ("CYN", 115, ARGB_CYAN), ("GRN", 116, ARGB_GREEN),
        ("YEL", 117, ARGB_YELLOW),
    ]
    for i, (cap, fn, bg) in enumerate(outer_row):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    out.append(solo_open("INNER RING", a.take(), 610, 720, 590, 114))
    inner_row = [
        ("R", 19, ARGB_RED), ("PUR", 120, ARGB_PURPLE),
        ("CYN", 121, ARGB_CYAN), ("GRN", 122, ARGB_GREEN),
        ("YEL", 123, ARGB_YELLOW),
    ]
    for i, (cap, fn, bg) in enumerate(inner_row):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Right column: Quick color sub-tools (x=1210..1910)
    out.append(solo_open("COLOR TOOLS", a.take(), 1210, 0, 700, 834))
    out.append(btn("OUTER BO", a.take(), 3, 3, 340, 114, 30, bg=ARGB_BLACK))
    out.append(btn("INNER BO", a.take(), 350, 3, 340, 114, 30, bg=ARGB_BLACK))
    out.append(btn("WHT FULL", a.take(), 3, 123, 340, 114, 1120, bg=ARGB_WHITE))
    out.append(btn("WHT OFF", a.take(), 350, 123, 340, 114, 22, bg=ARGB_BLACK))
    out.append(btn("PANEL R", a.take(), 3, 243, 340, 114, 272, bg=ARGB_RED))
    out.append(btn("PANEL W", a.take(), 350, 243, 340, 114, 280, bg=ARGB_WHITE))
    out.append(btn("COB W", a.take(), 3, 363, 340, 114, 387, bg=ARGB_WHITE))
    out.append(btn("A55 W", a.take(), 350, 363, 340, 114, 1118, bg=ARGB_WHITE))
    out.append(btn("FULL BO", a.take(), 3, 483, 340, 114, 126,
                   flash=True, force_ltp=True, bg=ARGB_BLACK))
    out.append(btn("ALL OFF", a.take(), 350, 483, 340, 114, 0,
                   stop_all=True, bg=ARGB_ORANGE))
    out.append(btn("STR MED", a.take(), 3, 603, 340, 114, 2919,
                   flash=True, bg=ARGB_YELLOW))
    out.append(btn("STR FST", a.take(), 350, 603, 340, 114, 2921,
                   flash=True, bg=ARGB_ORANGE))
    out.append(btn("BUMP W", a.take(), 3, 723, 340, 108, 3070, flash=True, bg=ARGB_WHITE))
    out.append(btn("BUMP WR", a.take(), 350, 723, 340, 108, 3071, flash=True, bg=ARGB_AMBER))
    out.append(solo_close())

    # Row H y=840: safety footer
    out.append(solo_open("QUICK", a.take(), 0, 840, 1200, 204))
    quick = [
        ("FULL BO", 126, ARGB_BLACK, True, True),
        ("BUMP W", 3070, ARGB_WHITE, True, False),
        ("BUMP WR", 3071, ARGB_AMBER, True, False),
        ("BO+HIT", 3073, ARGB_YELLOW, False, False),
        ("PANIC", 3060, ARGB_RED, False, False),
    ]
    for i, (cap, fn, bg, fl, ltp) in enumerate(quick):
        out.append(btn(cap, a.take(), 3 + i * 240, 3, 234, 200, fn,
                       flash=fl, force_ltp=ltp, bg=bg))
    out.append(solo_close())

    out.append(page_footer())
    return "\n".join(out)


# ───────────────── PAGE 6: FX ─────────────────
def page_fx() -> str:
    a = WidgetAlloc(16000, 16999)
    out = [page_header(6, "FX")]

    # Row A y=0: Ring RGBMatrix OUTER
    out.append(solo_open("RING MX - OUTER", a.take(), 0, 0, 1200, 114))
    mx_outer = [
        ("WAVE CW", 3700), ("WAVE CCW", 3701), ("BOUNCE", 3702),
        ("FILL", 3703), ("F+DRAIN", 3704), ("CENTER", 3705),
        ("EVEN/OD", 3706), ("MARQUEE", 3707), ("GRADNT", 3708),
        ("PLASMA", 3709),
    ]
    for i, (cap, fn) in enumerate(mx_outer):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=ARGB_DGRAY))
    out.append(solo_close())

    # Row B y=120: Ring RGBMatrix INNER
    out.append(solo_open("RING MX - INNER", a.take(), 0, 120, 1200, 114))
    mx_inner = [
        ("WAVE CW", 3715), ("WAVE CCW", 3716), ("BOUNCE", 3717),
        ("FILL", 3718), ("F+DRAIN", 3719), ("CENTER", 3720),
        ("EVEN/OD", 3721), ("MARQUEE", 3722), ("GRADNT", 3723),
        ("PLASMA", 3724),
    ]
    for i, (cap, fn) in enumerate(mx_inner):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=ARGB_CHARCOAL))
    out.append(solo_close())

    # Row C y=240: More Outer matrix + white ring matrix + panel
    out.append(solo_open("EXTRA MX", a.take(), 0, 240, 1200, 114))
    mx_extra = [
        ("SINE", 3710), ("NOISE", 3711), ("SPARKLE", 3712),
        ("RAND FL", 3713), ("FIREWRK", 3714), ("WHT W", 3730),
        ("PNL SWH", 475), ("PNL SWV", 476), ("PNL GRD", 477),
        ("PNL STB", 478),
    ]
    for i, (cap, fn) in enumerate(mx_extra):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=ARGB_DGRAY))
    out.append(solo_close())

    # Row D y=360: Standard Ring FX
    out.append(solo_open("RING FX", a.take(), 0, 360, 1200, 114))
    fx_std = [
        ("SWP CW", 1750), ("SWP CCW", 1751), ("SWP PP", 1752),
        ("BAR CW", 1753), ("BAR CCW", 1754), ("BAR PP", 1755),
        ("HALF", 1756), ("DUAL CW", 1757), ("OUT CW", 71),
        ("PULSE", 1514),
    ]
    for i, (cap, fn) in enumerate(fx_std):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=ARGB_DGRAY))
    out.append(solo_close())

    # Row E y=480: LED PANEL CHASES
    out.append(solo_open("LED PANEL CHASES", a.take(), 0, 480, 1200, 114))
    pnl = [
        ("CW", 448), ("F/B", 449), ("L/R", 450),
        ("DIAG A", 451), ("DIAG B", 452), ("TRAP GP", 453),
        ("BH CO", 454), ("DUB RB", 455), ("TRAP SLW", 457),
        ("CW SOFT", 1200),
    ]
    for i, (cap, fn) in enumerate(pnl):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=ARGB_DGRAY))
    out.append(solo_close())

    # Row F y=600: COB chases + bass hits
    out.append(solo_open("COB + BLINDER", a.take(), 0, 600, 1200, 114))
    cob = [
        ("COB CW", 458), ("COB F/B", 459), ("COB L/R", 460),
        ("COB DIAG", 461), ("COB TRAP", 463), ("COB BH", 464),
        ("COB DUB", 465), ("BLIND CW", 467), ("BLIND FL", 468),
        ("COB SOFT", 1207),
    ]
    for i, (cap, fn) in enumerate(cob):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=ARGB_DGRAY))
    out.append(solo_close())

    # Row G y=720: Colored ring FX samplers
    out.append(solo_open("RING FX - COLORED", a.take(), 0, 720, 1200, 114))
    clr = [
        ("SWP R", 1770, ARGB_RED), ("SWP O", 1771, ARGB_ORANGE),
        ("SWP Y", 1772, ARGB_YELLOW), ("SWP GR", 1773, ARGB_GREEN),
        ("SWP C", 1774, ARGB_CYAN), ("SWP B", 1775, ARGB_BLUE),
        ("SWP PR", 1776, ARGB_PURPLE), ("SWP GLD", 1777, ARGB_GOLD),
        ("BAR R", 2874, ARGB_RED), ("BAR B", 2879, ARGB_BLUE),
    ]
    for i, (cap, fn, bg) in enumerate(clr):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Right column y=0-834: SPEED DIALS + COLOR PICKER
    out.append(solo_open("FX CONTROL", a.take(), 1210, 0, 700, 834))
    out.append(speed_dial("RING FX SPD", a.take(), 3, 3, 690, 170,
                          RING_FX_ALL, beat_mode=True))
    out.append(speed_dial("MATRIX SPD", a.take(), 3, 180, 690, 170,
                          RING_MATRIX_ALL + PANEL_MATRIX_FN_IDS, beat_mode=True))
    out.append(speed_dial("MOTION SPD", a.take(), 3, 357, 690, 170,
                          MOTION_ALL + [448, 449, 450, 451, 452, 453, 454, 455,
                                         457, 458, 459, 460, 461, 463, 464, 465,
                                         467, 468],
                          beat_mode=True))
    out.append(speed_dial("STROBE SPD", a.take(), 3, 534, 690, 140,
                          STROBE_COLLECTIONS + list(range(94, 114)),
                          beat_mode=False))
    out.append(btn("FULL BO", a.take(), 3, 683, 340, 145, 126,
                   flash=True, force_ltp=True, bg=ARGB_BLACK))
    out.append(btn("ALL OFF", a.take(), 350, 683, 340, 145, 0,
                   stop_all=True, bg=ARGB_ORANGE))
    out.append(solo_close())

    # Row H footer
    out.append(solo_open("QUICK", a.take(), 0, 840, 1200, 204))
    quick = [
        ("FULL BO", 126, ARGB_BLACK, True, True),
        ("BUMP W", 3070, ARGB_WHITE, True, False),
        ("BO+HIT", 3073, ARGB_YELLOW, False, False),
        ("STR FST", 2921, ARGB_ORANGE, True, False),
        ("PANIC", 3060, ARGB_RED, False, False),
    ]
    for i, (cap, fn, bg, fl, ltp) in enumerate(quick):
        out.append(btn(cap, a.take(), 3 + i * 240, 3, 234, 200, fn,
                       flash=fl, force_ltp=ltp, bg=bg))
    out.append(solo_close())

    out.append(page_footer())
    return "\n".join(out)


# ───────────────── PAGE 7: IMPACT ─────────────────
def page_impact() -> str:
    a = WidgetAlloc(17000, 17999)
    out = [page_header(7, "IMPACT")]

    # Row A y=0: STROBE TIERS (all-group)
    out.append(solo_open("STROBE TIERS", a.take(), 0, 0, 1200, 114))
    tiers = [
        ("SLOW", 2918, ARGB_YELLOW),
        ("MED", 2919, ARGB_ORANGE),
        ("FAST", 2921, ARGB_RED),
        ("BLITZ", 2923, ARGB_PURPLE),
        ("RINGS M", 110, ARGB_AMBER),
        ("RINGS X", 112, ARGB_AMBER),
        ("MASTER", 73, ARGB_WHITE),
        ("BLINDER", 43, ARGB_WHITE),
        ("KILL", 3061, ARGB_BLACK),
        ("ALL OFF", 0, ARGB_ORANGE),
    ]
    for i, (cap, fn, bg) in enumerate(tiers):
        flash = i < 8 and cap != "BLINDER"
        stopall = cap == "ALL OFF"
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn,
                       flash=flash, force_ltp=flash, stop_all=stopall, bg=bg))
    out.append(solo_close())

    # Row B y=120: BLINDER/COB/A55/PANEL strobes (slow-med-fast per group)
    out.append(solo_open("GROUP STROBES", a.take(), 0, 120, 1200, 114))
    group = [
        ("BL SLW", 74), ("BL MED", 75), ("BL FST", 76),
        ("BL BLZ", 78), ("CB MED", 80), ("CB FST", 81),
        ("A55 MED", 85), ("A55 FST", 86), ("PNL MED", 90),
        ("PNL FST", 91),
    ]
    for i, (cap, fn) in enumerate(group):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn,
                       flash=True, bg=ARGB_YELLOW))
    out.append(solo_close())

    # Row C y=240: RING strobes (outer, inner, white)
    out.append(solo_open("RING STROBES", a.take(), 0, 240, 1200, 114))
    rs = [
        ("O SLW", 94), ("O MED", 95), ("O FST", 96),
        ("O BLZ", 98), ("I MED", 100), ("I FST", 101),
        ("W MED", 105), ("W FST", 106), ("ALL MED", 110),
        ("ALL FST", 111),
    ]
    for i, (cap, fn) in enumerate(rs):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=ARGB_WHITE))
    out.append(solo_close())

    # Row D y=360: BUMPS
    out.append(solo_open("BUMPS", a.take(), 0, 360, 1200, 114))
    bumps = [
        ("BUMP W", 3070, ARGB_WHITE, True),
        ("BUMP WR", 3071, ARGB_AMBER, True),
        ("DECAY", 3072, ARGB_GOLD, False),
        ("DIM WRM", 3074, ARGB_AMBER, False),
        ("BO+HIT", 3073, ARGB_YELLOW, False),
        ("ALL WHT", 128, ARGB_WHITE, True),
        ("BLNDR", 127, ARGB_WHITE, True),
        ("COB W HIT", 33, ARGB_WHITE, True),
        ("A55 W", 1118, ARGB_WHITE, True),
        ("PNL W", 280, ARGB_WHITE, True),
    ]
    for i, (cap, fn, bg, fl) in enumerate(bumps):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn,
                       flash=fl, bg=bg))
    out.append(solo_close())

    # Row E y=480: BASS HITS
    out.append(solo_open("BASS HITS", a.take(), 0, 480, 1200, 114))
    bass = [
        ("F COB+B", 3500, ARGB_PURPLE, True),
        ("B COB+B", 3501, ARGB_PURPLE, True),
        ("ALT F/B", 3502, ARGB_PURPLE, False),
        ("F A55", 3503, ARGB_CYAN, True),
        ("B A55", 3504, ARGB_CYAN, True),
        ("ALT A55", 3505, ARGB_CYAN, False),
        ("F COB", 3506, ARGB_RED, True),
        ("B COB", 3507, ARGB_RED, True),
        ("ALT COB", 3508, ARGB_RED, False),
        ("QUAD", 3509, ARGB_GOLD, False),
    ]
    for i, (cap, fn, bg, fl) in enumerate(bass):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn,
                       flash=fl, bg=bg))
    out.append(solo_close())

    # Row F y=600: Color strobes (fast OI chases by color)
    out.append(solo_open("COLOR PULSES", a.take(), 0, 600, 1200, 114))
    cp = [
        ("R PULSE", 2060, ARGB_RED),
        ("ORG PLS", 2061, ARGB_ORANGE),
        ("GLD PLS", 2067, ARGB_GOLD),
        ("GRN PLS", 2063, ARGB_GREEN),
        ("CYN PLS", 2064, ARGB_CYAN),
        ("BLU PLS", 2065, ARGB_BLUE),
        ("PUR PLS", 2066, ARGB_PURPLE),
        ("W>R", 2078, ARGB_WHITE),
        ("W>BL", 2079, ARGB_WHITE),
        ("W>PUR", 2080, ARGB_WHITE),
    ]
    for i, (cap, fn, bg) in enumerate(cp):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row G y=720: Accel chasers — tension-builders
    out.append(solo_open("ACCEL SWEEPS", a.take(), 0, 720, 1200, 114))
    ac = [
        ("WHT CW", 3200, ARGB_WHITE),
        ("RED", 3201, ARGB_RED),
        ("ORG", 3202, ARGB_ORANGE),
        ("YEL", 3203, ARGB_YELLOW),
        ("GRN", 3204, ARGB_GREEN),
        ("CYN", 3205, ARGB_CYAN),
        ("BLU", 3206, ARGB_BLUE),
        ("PUR", 3207, ARGB_PURPLE),
        ("GLD", 3208, ARGB_GOLD),
        ("WHT PP", 3209, ARGB_WHITE),
    ]
    for i, (cap, fn, bg) in enumerate(ac):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Right column
    out.append(solo_open("IMPACT CTRL", a.take(), 1210, 0, 700, 834))
    out.append(speed_dial("STROBE RATE", a.take(), 3, 3, 690, 170,
                          STROBE_COLLECTIONS + list(range(94, 114)),
                          beat_mode=False))
    out.append(speed_dial("BUMP DECAY", a.take(), 3, 180, 690, 140, [3072],
                          beat_mode=False))
    out.append(btn("FULL BO", a.take(), 3, 330, 340, 120, 126,
                   flash=True, force_ltp=True, bg=ARGB_BLACK))
    out.append(btn("ALL OFF", a.take(), 350, 330, 340, 120, 0,
                   stop_all=True, bg=ARGB_ORANGE))
    out.append(btn("PANIC", a.take(), 3, 456, 340, 120, 3060, bg=ARGB_RED))
    out.append(btn("STR KILL", a.take(), 350, 456, 340, 120, 3061,
                   flash=True, force_ltp=True, bg=ARGB_BLACK))
    out.append(btn("BO+HIT", a.take(), 3, 582, 690, 120, 3073, bg=ARGB_YELLOW))
    out.append(btn("BUMP W", a.take(), 3, 708, 340, 120, 3070,
                   flash=True, bg=ARGB_WHITE))
    out.append(btn("BUMP WR", a.take(), 350, 708, 340, 120, 3071,
                   flash=True, bg=ARGB_AMBER))
    out.append(solo_close())

    # Footer
    out.append(solo_open("QUICK", a.take(), 0, 840, 1200, 204))
    quick = [
        ("FULL BO", 126, ARGB_BLACK, True, True),
        ("STR MED", 2919, ARGB_YELLOW, True, False),
        ("STR FST", 2921, ARGB_ORANGE, True, False),
        ("STR BLZ", 2923, ARGB_RED, True, False),
        ("PANIC", 3060, ARGB_RED, False, False),
    ]
    for i, (cap, fn, bg, fl, ltp) in enumerate(quick):
        out.append(btn(cap, a.take(), 3 + i * 240, 3, 234, 200, fn,
                       flash=fl, force_ltp=ltp, bg=bg))
    out.append(solo_close())

    out.append(page_footer())
    return "\n".join(out)


# ───────────────── PAGE 8: ATMOSPHERE ─────────────────
def page_atmosphere() -> str:
    a = WidgetAlloc(18000, 18999)
    out = [page_header(8, "ATMOSPHERE")]

    # Row A y=0: Tunnel scenes + chasers
    out.append(solo_open("TUNNEL", a.take(), 0, 0, 1200, 114))
    tn = [
        ("T-S1", 3300), ("T-S2", 3301), ("T-S3", 3302),
        ("T-S4", 3303), ("T-S5", 3304), ("T-S6", 3305),
        ("T-S7", 3306), ("T-S8", 3307), ("CONVERGE", 3320),
        ("BREATHE", 3321),
    ]
    for i, (cap, fn) in enumerate(tn):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=ARGB_DGRAY))
    out.append(solo_close())

    # Row B y=120: Tunnel rings (colored)
    out.append(solo_open("TUNNEL RINGS", a.take(), 0, 120, 1200, 114))
    tr = [
        ("T-R", 3322, ARGB_RED), ("T-O", 3323, ARGB_ORANGE),
        ("T-Y", 3324, ARGB_YELLOW), ("T-GRN", 3325, ARGB_GREEN),
        ("T-C", 3326, ARGB_CYAN), ("T-B", 3327, ARGB_BLUE),
        ("T-PUR", 3328, ARGB_PURPLE), ("T-GLD", 3329, ARGB_GOLD),
        ("INT O F/B", 1516, ARGB_DGRAY), ("INT I F/B", 1517, ARGB_DGRAY),
    ]
    for i, (cap, fn, bg) in enumerate(tr):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row C y=240: White ring layers
    out.append(solo_open("WHITE RING LAYERS", a.take(), 0, 240, 1200, 114))
    wrl = [
        ("S1", 3400), ("S2", 3401), ("S3", 3402), ("S4", 3403),
        ("S5", 3404), ("S6", 3405), ("S7", 3406), ("S8", 3407),
        ("SEG CH", 3416), ("ALT BRS", 3417),
    ]
    for i, (cap, fn) in enumerate(wrl):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=ARGB_WHITE))
    out.append(solo_close())

    # Row D y=360: White ring chasers + fills
    out.append(solo_open("WHITE RING FX", a.take(), 0, 360, 1200, 114))
    wrf = [
        ("SHIMMER", 3418), ("DBL TIM", 3419), ("SPARKLE", 3436),
        ("BREATHE", 3437), ("FILL CH", 3438), ("FILL 4", 3423),
        ("FILL 8", 3427), ("FILL 12", 3431), ("FILL 16", 3435),
        ("WHT FULL", 67),
    ]
    for i, (cap, fn) in enumerate(wrf):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=ARGB_WHITE))
    out.append(solo_close())

    # Row E y=480: DARKNESS
    out.append(solo_open("DARKNESS", a.take(), 0, 480, 1200, 114))
    dk = [
        ("WHISPER", 3740), ("SLHOUET", 3741), ("CANDLE", 3742),
        ("HALF F", 3743), ("HALF B", 3744), ("NEG FL", 3745),
        ("8B BLK", 3746), ("N STROBE", 3747), ("SMOLDER", 3748),
        ("VANISH", 3749),
    ]
    for i, (cap, fn) in enumerate(dk):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=ARGB_BLACK))
    out.append(solo_close())

    # Row F y=600: PHASER seeds
    out.append(solo_open("PHASER SEEDS", a.take(), 0, 600, 1200, 114))
    phs = [
        ("OFF", 3750), ("LOW", 3751), ("MED", 3752),
        ("HIGH", 3753), ("FULL", 3754), ("EVEN", 3755),
        ("ODD", 3756), ("QTRS", 3757), ("HALVES", 3758),
        ("OTHER", 3759),
    ]
    for i, (cap, fn) in enumerate(phs):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=ARGB_WHITE_SOFT))
    out.append(solo_close())

    # Row G y=720: PHASER chasers + soft FX quick picks
    out.append(solo_open("PHASER + SOFT", a.take(), 0, 720, 1200, 114))
    psc = [
        ("BREATHE", 3760, ARGB_WHITE_SOFT),
        ("HEART", 3761, ARGB_WHITE_SOFT),
        ("SWELL", 3762, ARGB_WHITE_SOFT),
        ("SPARKLE", 3763, ARGB_WHITE_SOFT),
        ("DRIFT", 3764, ARGB_WHITE_SOFT),
        ("GHOST", 3765, ARGB_WHITE_SOFT),
        ("PULSE 150", 3766, ARGB_WHITE_SOFT),
        ("SOFT SWP", 3100, ARGB_DGRAY),
        ("SOFT BAR", 3140, ARGB_DGRAY),
        ("SOFT DUAL", 3132, ARGB_DGRAY),
    ]
    for i, (cap, fn, bg) in enumerate(psc):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Right column
    out.append(solo_open("ATM CTRL", a.take(), 1210, 0, 700, 834))
    out.append(speed_dial("TUNNEL SPD", a.take(), 3, 3, 690, 170,
                          [3320, 3321] + list(range(3322, 3330)),
                          beat_mode=True))
    out.append(speed_dial("WHT RNG SPD", a.take(), 3, 180, 690, 170,
                          [3416, 3417, 3418, 3419, 3436, 3437, 3438],
                          beat_mode=True))
    out.append(speed_dial("DARK SPD", a.take(), 3, 357, 690, 170,
                          list(range(3746, 3750)), beat_mode=True))
    out.append(speed_dial("PHASER SPD", a.take(), 3, 534, 690, 140,
                          list(range(3760, 3767)), beat_mode=False))
    out.append(btn("FULL BO", a.take(), 3, 683, 340, 145, 126,
                   flash=True, force_ltp=True, bg=ARGB_BLACK))
    out.append(btn("ALL OFF", a.take(), 350, 683, 340, 145, 0,
                   stop_all=True, bg=ARGB_ORANGE))
    out.append(solo_close())

    # Footer
    out.append(solo_open("QUICK", a.take(), 0, 840, 1200, 204))
    quick = [
        ("FULL BO", 126, ARGB_BLACK, True, True),
        ("8B BLK", 3746, ARGB_BLACK, False, False),
        ("BREATHE", 3760, ARGB_WHITE_SOFT, False, False),
        ("BUMP W", 3070, ARGB_WHITE, True, False),
        ("PANIC", 3060, ARGB_RED, False, False),
    ]
    for i, (cap, fn, bg, fl, ltp) in enumerate(quick):
        out.append(btn(cap, a.take(), 3 + i * 240, 3, 234, 200, fn,
                       flash=fl, force_ltp=ltp, bg=bg))
    out.append(solo_close())

    out.append(page_footer())
    return "\n".join(out)


# ───────────────── PAGE 9: DIRECTOR ─────────────────
def page_director() -> str:
    a = WidgetAlloc(19000, 19999)
    out = [page_header(9, "DIRECTOR")]

    # Row A y=0: ENERGY STATES
    out.append(solo_open("ENERGY STATES", a.take(), 0, 0, 1200, 114))
    es = [
        ("SIMMER", 3040, ARGB_DARKPURP),
        ("GROOVE", 3041, ARGB_CYAN_DEEP),
        ("SURGE", 3042, ARGB_ORANGE),
        ("DISSOLVE", 3043, ARGB_BLUE),
        ("TENSION", 3044, ARGB_RED),
        ("ERUPTION", 3045, ARGB_YELLOW),
        ("PANIC", 3060, ARGB_RED),
        ("KILL", 3061, ARGB_BLACK),
        ("FULL BO", 126, ARGB_BLACK),
        ("ALL OFF", 0, ARGB_ORANGE),
    ]
    for i, (cap, fn, bg) in enumerate(es):
        flash = cap in ("FULL BO",)
        stopall = cap == "ALL OFF"
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn,
                       flash=flash, force_ltp=flash, stop_all=stopall, bg=bg))
    out.append(solo_close())

    # Row B y=120: EMOTIONAL ARCS (show chasers)
    out.append(solo_open("EMOTIONAL ARCS", a.take(), 0, 120, 1200, 114))
    arcs = [
        ("DESCENT", 3600, ARGB_RED),
        ("BETRAYAL", 3601, ARGB_GOLD),
        ("CLIMB", 3602, ARGB_CYAN),
        ("HUNT", 3603, ARGB_GREEN),
        ("GRINDER", 3604, ARGB_PURPLE),
        ("RESURRECT", 3605, ARGB_WHITE),
        ("LOOK DUB", 1002, ARGB_RED),
        ("LOOK TRP", 1000, ARGB_GOLD),
        ("LOOK BH", 1001, ARGB_CYAN),
        ("LOOK RDM", 1006, ARGB_ORANGE),
    ]
    for i, (cap, fn, bg) in enumerate(arcs):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row C y=240: SURPRISE ROULETTE
    out.append(solo_open("SURPRISE", a.take(), 0, 240, 1200, 114))
    sur = [
        ("COLOR W", 3770, ARGB_ORANGE),
        ("GENRE", 3771, ARGB_GOLD),
        ("ENERGY", 3772, ARGB_YELLOW),
        ("RING FX", 3773, ARGB_CYAN),
        ("MATRIX", 3774, ARGB_CYAN),
        ("MOTION", 3775, ARGB_GREEN),
        ("DARK", 3776, ARGB_BLACK),
        ("PHASER", 3777, ARGB_WHITE),
        ("SPATIAL", 3778, ARGB_PURPLE),
        ("CHAOS", 3779, ARGB_RED),
    ]
    for i, (cap, fn, bg) in enumerate(sur):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row D y=360: RAMPS (time-shape primitives)
    out.append(solo_open("RAMPS", a.take(), 0, 360, 1200, 114))
    rmp = [
        ("ACCEL", 3800), ("DECEL", 3801), ("CINEMA", 3802),
        ("AFTERGLW", 3803), ("WRLDS UP", 3804), ("WRLDS DN", 3805),
        ("MX TOUR", 3806), ("FX DECAY", 3807), ("PLS ACC", 3808),
        ("STRIKE", 3833),
    ]
    for i, (cap, fn) in enumerate(rmp):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=ARGB_AMBER))
    out.append(solo_close())

    # Row E y=480: ACCEL SWEEPS (tension-builders)
    out.append(solo_open("ACCEL TENSION", a.take(), 0, 480, 1200, 114))
    ac = [
        ("T1", 3210), ("T2", 3211), ("T3", 3212),
        ("T4", 3213), ("PP", 3214), ("DUAL", 3215),
        ("HALF", 3216), ("TIGHT2", 3217), ("ACC3", 3218),
        ("DUAL4", 3219),
    ]
    for i, (cap, fn) in enumerate(ac):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=ARGB_ORANGE))
    out.append(solo_close())

    # Row F y=600: COLOR WORLDS
    out.append(solo_open("COLOR WORLDS", a.take(), 0, 600, 1200, 114))
    worlds = [
        ("INFRN", 3000, ARGB_RED),
        ("EMBER", 3001, ARGB_ORANGE),
        ("SOLAR", 3002, ARGB_YELLOW),
        ("VRDNT", 3003, ARGB_GREEN),
        ("ARCTIC", 3004, ARGB_CYAN),
        ("OCEAN", 3005, ARGB_BLUE),
        ("UV", 3006, ARGB_PURPLE),
        ("AURORA", 3007, ARGB_MINT),
        ("PRISM", 3008, ARGB_WHITE),
        ("VOID", 3009, ARGB_BLACK),
    ]
    for i, (cap, fn, bg) in enumerate(worlds):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Row G y=720: GENRE LOOKS + MELODIC/DnB
    out.append(solo_open("GENRE LOOKS", a.take(), 0, 720, 1200, 114))
    gl = [
        ("TRAP", 1000, ARGB_GOLD),
        ("BASSHSE", 1001, ARGB_CYAN),
        ("DUBSTEP", 1002, ARGB_RED),
        ("RIDDIM", 1006, ARGB_ORANGE),
        ("MELODIC", 1007, ARGB_PURPLE),
        ("DnB", 1008, ARGB_GREEN),
        ("ENERGY S", 3040, ARGB_DARKPURP),
        ("ENERGY G", 3041, ARGB_CYAN_DEEP),
        ("ENERGY R", 3042, ARGB_ORANGE),
        ("ENERGY E", 3045, ARGB_YELLOW),
    ]
    for i, (cap, fn, bg) in enumerate(gl):
        out.append(btn(cap, a.take(), 3 + i * 120, 3, SQ, SQ, fn, bg=bg))
    out.append(solo_close())

    # Right column
    out.append(solo_open("DIRECTOR CTRL", a.take(), 1210, 0, 700, 834))
    out.append(speed_dial("ARC SPD", a.take(), 3, 3, 690, 170,
                          list(range(3600, 3606)), beat_mode=True))
    out.append(speed_dial("SURPRISE", a.take(), 3, 180, 690, 170,
                          list(range(3770, 3780)), beat_mode=True))
    out.append(speed_dial("RAMP SPD", a.take(), 3, 357, 690, 170,
                          list(range(3800, 3809)), beat_mode=True))
    out.append(btn("TOTAL CHAOS", a.take(), 3, 534, 690, 120, 3779,
                   bg=ARGB_RED))
    out.append(btn("FULL BO", a.take(), 3, 660, 340, 170, 126,
                   flash=True, force_ltp=True, bg=ARGB_BLACK))
    out.append(btn("ALL OFF", a.take(), 350, 660, 340, 170, 0,
                   stop_all=True, bg=ARGB_ORANGE))
    out.append(solo_close())

    # Footer
    out.append(solo_open("QUICK", a.take(), 0, 840, 1200, 204))
    quick = [
        ("FULL BO", 126, ARGB_BLACK, True, True),
        ("TENSION", 3044, ARGB_RED, False, False),
        ("ERUPT", 3045, ARGB_YELLOW, False, False),
        ("DISSOLVE", 3043, ARGB_BLUE, False, False),
        ("PANIC", 3060, ARGB_RED, False, False),
    ]
    for i, (cap, fn, bg, fl, ltp) in enumerate(quick):
        out.append(btn(cap, a.take(), 3 + i * 240, 3, 234, 200, fn,
                       flash=fl, force_ltp=ltp, bg=bg))
    out.append(solo_close())

    out.append(page_footer())
    return "\n".join(out)


# ─────────────────────────────────── Assemble + main ───────────────────────────────────
def build_virtual_console() -> str:
    parts = [
        "<VirtualConsole>",
        " <Frame Caption=\"\">",
        "  <Appearance>",
        f"   <Font>{FONT}</Font>",
        f"   <BackgroundColor>{THEME_BG}</BackgroundColor>",
        "  </Appearance>",
        f"  <WindowState Visible=\"True\" X=\"0\" Y=\"0\" Width=\"{PAGE_W}\" Height=\"{PAGE_H}\"/>",
        "  <AllowResize>False</AllowResize>",
        "  <ShowHeader>True</ShowHeader>",
        "  <ShowEnableButton>False</ShowEnableButton>",
        "  <Collapsed>False</Collapsed>",
        "  <Disabled>False</Disabled>",
        "  <Multipage>True</Multipage>",
        "  <PagesCount>10</PagesCount>",
        "  <CurrentPage>0</CurrentPage>",
        page_busk(),
        page_dubstep(),
        page_trap(),
        page_bass_house(),
        page_techno(),
        page_color(),
        page_fx(),
        page_impact(),
        page_atmosphere(),
        page_director(),
        " </Frame>",
        " <Properties>",
        "  <Size Width=\"1920\" Height=\"1080\"/>",
        "  <GrandMaster ChannelMode=\"Intensity\" ValueMode=\"Reduce\" SliderMode=\"Normal\"/>",
        " </Properties>",
        "</VirtualConsole>",
    ]
    return "\n".join(parts)


def main() -> None:
    text = QXW.read_text(encoding="utf-8")
    new_vc = build_virtual_console()
    import re
    new_text = re.sub(
        r"<VirtualConsole>.*?</VirtualConsole>",
        new_vc, text, count=1, flags=re.DOTALL,
    )
    QXW.write_text(new_text, encoding="utf-8")
    print("OK: Virtual Console rebuilt (10 pages)")


if __name__ == "__main__":
    main()
