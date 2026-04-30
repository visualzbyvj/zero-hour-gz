# -*- coding: utf-8 -*-
"""Scan bundled QLC+ fixture definitions under QLC+/Fixtures into _fixture_cache.json.

Each entry includes:
  - manufacturer, model, modes (name -> channel count)
  - capability flags: has_rgb, has_white, has_strobe, has_pan_tilt
  - segment_count: number of independent RGB sub-segments
  - channels_detail: list of {name, group, colour, preset} per channel in first mode
"""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIX_DIR = ROOT / "QLC+" / "Fixtures"
FD_NS = "http://www.qlcplus.org/FixtureDefinition"

# Preset attribute -> (group, colour) equivalents
_PRESET_MAP: dict[str, tuple[str, str]] = {
    "IntensityRed":   ("Intensity", "Red"),
    "IntensityGreen": ("Intensity", "Green"),
    "IntensityBlue":  ("Intensity", "Blue"),
    "IntensityWhite": ("Intensity", "White"),
    "IntensityDimmer": ("Intensity", ""),
}


def t(local: str) -> str:
    return f"{{{FD_NS}}}{local}"


def _channel_info(ch_el: ET.Element) -> dict:
    """Extract group, colour, and preset from a <Channel> element."""
    name = ch_el.get("Name", "")
    preset = ch_el.get("Preset", "")

    if preset and preset in _PRESET_MAP:
        grp, colour = _PRESET_MAP[preset]
    else:
        grp_el = ch_el.find(t("Group"))
        colour_el = ch_el.find(t("Colour"))
        grp = grp_el.text.strip() if grp_el is not None and grp_el.text else ""
        colour = colour_el.text.strip() if colour_el is not None and colour_el.text else ""

        # Fallback: infer from name when both Group child and Preset are absent
        if not grp:
            name_lc = name.lower()
            if any(k in name_lc for k in ("strobe", "shutter")):
                grp = "Shutter"
            elif any(k in name_lc for k in ("pan",)):
                grp = "Pan"
            elif any(k in name_lc for k in ("tilt",)):
                grp = "Tilt"
            elif any(k in name_lc for k in ("red",)):
                grp, colour = "Intensity", "Red"
            elif any(k in name_lc for k in ("green",)):
                grp, colour = "Intensity", "Green"
            elif any(k in name_lc for k in ("blue",)):
                grp, colour = "Intensity", "Blue"
            elif any(k in name_lc for k in ("white",)):
                grp, colour = "Intensity", "White"
            elif any(k in name_lc for k in ("dimmer", "master", "intensity")):
                grp = "Intensity"

    return {"name": name, "group": grp, "colour": colour, "preset": preset}


def _capabilities(channel_defs: dict[str, dict]) -> dict:
    """Derive capability flags and segment count from the channel dict."""
    colours = {c["colour"] for c in channel_defs.values()}
    groups = {c["group"] for c in channel_defs.values()}
    names_lc = {c["name"].lower() for c in channel_defs.values()}

    has_rgb = {"Red", "Green", "Blue"}.issubset(colours)
    has_white = "White" in colours
    has_strobe = "Shutter" in groups or any("strobe" in n for n in names_lc)
    has_pan_tilt = "Pan" in groups or "Tilt" in groups

    # Estimate segment count: count distinct numeric suffixes on Red channels
    # e.g. "Red 1", "Red 2" -> 2 segments; "Red" alone -> 1 segment
    red_chs = [c["name"] for c in channel_defs.values() if c["colour"] == "Red"]
    if len(red_chs) > 1:
        segment_count = len(red_chs)
    elif has_rgb:
        segment_count = 1
    else:
        segment_count = 0

    return {
        "has_rgb": has_rgb,
        "has_white": has_white,
        "has_strobe": has_strobe,
        "has_pan_tilt": has_pan_tilt,
        "segment_count": segment_count,
    }


def parse_qxf(path: Path) -> dict:
    tree = ET.parse(path)
    r = tree.getroot()

    man_el = r.find(t("Manufacturer"))
    model_el = r.find(t("Model"))

    # Build a lookup: channel name -> info dict
    all_channels: dict[str, dict] = {}
    for ch_el in r.findall(t("Channel")):
        name = ch_el.get("Name", "")
        all_channels[name] = _channel_info(ch_el)

    modes: dict[str, int] = {}
    for mode in r.findall(t("Mode")):
        mode_name = mode.get("Name") or "default"
        refs = mode.findall(t("Channel"))
        modes[str(mode_name)] = len(refs)

    # channels_detail = ordered channels in the first mode
    channels_detail: list[dict] = []
    first_mode = r.find(t("Mode"))
    if first_mode is not None:
        for ref in first_mode.findall(t("Channel")):
            ch_name = ref.text or ""
            info = all_channels.get(ch_name, {"name": ch_name, "group": "", "colour": "", "preset": ""})
            channels_detail.append(info)

    caps = _capabilities(all_channels)

    return {
        "file": path.name,
        "manufacturer": (man_el.text or "").strip() if man_el is not None else "",
        "model": (model_el.text or "").strip() if model_el is not None else "",
        "modes": modes,
        **caps,
        "channels_detail": channels_detail,
    }


def main() -> None:
    if not FIX_DIR.is_dir():
        raise SystemExit(f"Missing fixture folder: {FIX_DIR}")

    entries: list[dict] = []
    for p in sorted(FIX_DIR.glob("*.qxf")):
        try:
            entries.append(parse_qxf(p))
        except ET.ParseError as exc:
            entries.append({"file": p.name, "error": str(exc)})

    out = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "source_dir": str(FIX_DIR),
        "count": len(entries),
        "fixtures": entries,
    }
    (ROOT / "_output" / "_fixture_cache.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote _fixture_cache.json ({len(entries)} fixtures)")
    for e in entries:
        if "error" not in e:
            caps = f"rgb={e['has_rgb']} white={e['has_white']} strobe={e['has_strobe']} segs={e['segment_count']}"
            print(f"  {e['manufacturer']} {e['model']}: {caps}")


if __name__ == "__main__":
    main()
