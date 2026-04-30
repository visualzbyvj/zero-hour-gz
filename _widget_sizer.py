# -*- coding: utf-8 -*-
"""Heuristics for Virtual Console widget geometry (SpeedDial presets need vertical space)."""
from __future__ import annotations

__all__ = ("speed_dial_min_height", "speed_dial_recommend_height")


def speed_dial_min_height(
    beat_mode: bool,
    visibility: int,
    preset_count: int,
    fn_count: int,
) -> int:
    """Minimum practical height so dial UI + optional preset row fits."""
    del beat_mode, visibility  # reserved for future tuning vs Visibility flags
    h = 78
    if preset_count:
        h = max(h, 142)
    if fn_count > 12:
        h += 10
    return h


def speed_dial_recommend_height(
    beat_mode: bool,
    visibility: int,
    requested: int,
    preset_count: int,
    fn_count: int,
) -> int:
    """Clamp requested height up to a safe minimum."""
    return max(
        requested,
        speed_dial_min_height(beat_mode, visibility, preset_count, fn_count),
    )
