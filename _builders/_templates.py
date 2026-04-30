# -*- coding: utf-8 -*-
"""
Shared XML template helpers for Zero Hour GZ builders.

Re-exports the canonical generators from _qlc_helpers and _build_new_vc so
callers can do::

    from _templates import scene, chaser, collection, speed_dial, button, soloframe, slider

All re-exported wrappers add lightweight guard rails:
    - ID must be a non-negative int (not the sentinel 4294967295)
    - Coordinate/size args must be >= 0
    - List args must be non-empty where the underlying generator requires at least 1 item
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
WORKSPACE_NS = "http://www.qlcplus.org/Workspace"
FIXTURE_DEF_NS = "http://www.qlcplus.org/FixtureDefinition"

NO_FUNCTION_ID: int = 4294967295  # QLC+ sentinel: "no function assigned"

_VALID_RUN_ORDERS = {"Loop", "SingleShot", "PingPong"}
_VALID_TEMPO = {"Beats", "Time"}


# ---------------------------------------------------------------------------
# Guard helpers
# ---------------------------------------------------------------------------
def _check_fid(fid: int) -> None:
    if not isinstance(fid, int) or fid < 0 or fid == NO_FUNCTION_ID:
        raise ValueError(f"Invalid function ID: {fid!r} (must be 0 <= int < {NO_FUNCTION_ID})")


def _check_wid(wid: int) -> None:
    if not isinstance(wid, int) or wid < 0:
        raise ValueError(f"Invalid widget ID: {wid!r} (must be non-negative int)")


def _check_coords(x: int, y: int, w: int, h: int) -> None:
    for name, val in (("x", x), ("y", y), ("w", w), ("h", h)):
        if not isinstance(val, int) or val < 0:
            raise ValueError(f"Widget coord/size {name}={val!r} must be a non-negative int")


def _check_nonempty(lst: list, name: str = "list") -> None:
    if not lst:
        raise ValueError(f"{name} must be non-empty")


# ---------------------------------------------------------------------------
# Engine-function generators (wrappers around _qlc_helpers)
# ---------------------------------------------------------------------------
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import (  # noqa: E402  (module-level import after guards defined)
    scene_xml as _scene_xml,
    chaser_xml as _chaser_xml,
    collection_xml as _collection_xml,
)


def scene(
    fid: int,
    name: str,
    fixture_vals: "list[tuple[int, str]]",
) -> str:
    """Return XML string for a Scene function.

    Args:
        fid: Function ID (0 <= int, not NO_FUNCTION_ID)
        name: Human-readable name (will be XML-escaped by _qlc_helpers)
        fixture_vals: Non-empty list of (fixture_id, channel_values_str) tuples
    """
    _check_fid(fid)
    _check_nonempty(fixture_vals, "fixture_vals")
    return _scene_xml(fid, name, fixture_vals)


def chaser(
    fid: int,
    name: str,
    step_ids: "list[int]",
    run_order: str = "Loop",
    dur: int = 150,
    *,
    tempo: str = "Beats",
    sm_fi: str = "PerStep",
    sm_fo: str = "Default",
    sm_dur: str = "Common",
    step_fade_in: "int | list[int]" = 0,
    step_fade_out: "int | list[int]" = 0,
    step_hold: "int | list[int] | None" = None,
) -> str:
    """Return XML string for a Chaser function.

    Args:
        fid: Function ID
        name: Human-readable name
        step_ids: Non-empty list of scene/collection IDs for steps
        run_order: One of Loop/SingleShot/PingPong
        dur: Default step duration (ms or millibeats)
        tempo: 'Beats' or 'Time'
    """
    _check_fid(fid)
    _check_nonempty(step_ids, "step_ids")
    if run_order not in _VALID_RUN_ORDERS:
        raise ValueError(f"run_order must be one of {_VALID_RUN_ORDERS}, got {run_order!r}")
    if tempo not in _VALID_TEMPO:
        raise ValueError(f"tempo must be one of {_VALID_TEMPO}, got {tempo!r}")
    return _chaser_xml(
        fid, name, step_ids, run_order, dur,
        tempo=tempo, sm_fi=sm_fi, sm_fo=sm_fo, sm_dur=sm_dur,
        step_fade_in=step_fade_in, step_fade_out=step_fade_out, step_hold=step_hold,
    )


def collection(fid: int, name: str, steps: "list[int]") -> str:
    """Return XML string for a Collection function.

    Args:
        fid: Function ID
        name: Human-readable name
        steps: Non-empty list of function IDs to include
    """
    _check_fid(fid)
    _check_nonempty(steps, "steps")
    return _collection_xml(fid, name, steps)


# ---------------------------------------------------------------------------
# VC widget generators (wrappers around _build_new_vc)
# ---------------------------------------------------------------------------
from _build_new_vc import (  # noqa: E402
    speed_dial_multi as _speed_dial_multi,
    soloframe_open as _soloframe_open,
    slider_pb as _slider_pb,
    btn as _btn,
)
from _widget_sizer import speed_dial_min_height  # noqa: E402


def speed_dial(
    caption: str,
    wid: int,
    x: int,
    y: int,
    w: int,
    h: int,
    fn_ids: "list[int]",
    beat_mode: bool = False,
) -> str:
    """Return XML string for a SpeedDial widget.

    Enforces minimum height from _widget_sizer and validates all IDs.
    """
    _check_wid(wid)
    _check_coords(x, y, w, h)
    _check_nonempty(fn_ids, "fn_ids")
    for fid in fn_ids:
        _check_fid(fid)
    min_h = speed_dial_min_height(beat_mode=beat_mode)
    if h < min_h:
        raise ValueError(
            f"SpeedDial height {h} is below minimum {min_h} for beat_mode={beat_mode}. "
            "Use _widget_sizer.speed_dial_recommend_height() to compute a safe value."
        )
    return _speed_dial_multi(caption, wid, x, y, w, h, fn_ids, beat_mode)


def soloframe(
    caption: str,
    wid: int,
    x: int,
    y: int,
    w: int,
    h: int,
) -> str:
    """Return XML open-tag string for a SoloFrame widget."""
    _check_wid(wid)
    _check_coords(x, y, w, h)
    return _soloframe_open(caption, wid, x, y, w, h)


def slider(
    caption: str,
    wid: int,
    x: int,
    y: int,
    w: int,
    h: int,
    fn: int,
    cc: int = 0,
) -> str:
    """Return XML string for a Playback Slider widget."""
    _check_wid(wid)
    _check_coords(x, y, w, h)
    _check_fid(fn)
    return _slider_pb(caption, wid, x, y, w, h, fn, cc)


def button(
    caption: str,
    wid: int,
    x: int,
    y: int,
    w: int,
    h: int,
    fn: int,
    rgb: str = "#FFAA00",
    action: str = "Toggle",
) -> str:
    """Return XML string for a Button widget."""
    _check_wid(wid)
    _check_coords(x, y, w, h)
    _check_fid(fn)
    return _btn(caption, wid, x, y, w, h, fn, rgb, action)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
__all__ = (
    # Constants
    "WORKSPACE_NS",
    "FIXTURE_DEF_NS",
    "NO_FUNCTION_ID",
    # Guard helpers (usable by custom builders)
    "_check_fid",
    "_check_wid",
    "_check_coords",
    "_check_nonempty",
    # Engine generators
    "scene",
    "chaser",
    "collection",
    # VC widget generators
    "speed_dial",
    "soloframe",
    "slider",
    "button",
)
