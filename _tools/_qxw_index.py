# -*- coding: utf-8 -*-
"""Build a detailed JSON index of the workspace (_QXW_INDEX.json).

Emits:
  functions_detail  - ID/Type/Name/Tempo/Speed/StepCount/StepIDs per function
  vc_widgets_detail - ID/Type/Caption/X/Y/W/H/FunctionRefs/Visibility/Presets per widget
  collections_detail - ID/Name/member function IDs
  cross_refs        - function ID -> list of widget IDs that reference it
  free_id_ranges    - gaps in allocated function IDs
  summary           - counts, id min/max, fixture list
"""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import QXW

ROOT = Path(__file__).resolve().parent.parent
WS_NS = "http://www.qlcplus.org/Workspace"

_VC_WIDGET_TAGS = {
    "Button", "Slider", "SpeedDial", "Frame", "SoloFrame", "Label",
    "XYPad", "AnimationWidget", "Knob", "AudioTriggerWidget", "VideoPlayer",
    "Clock", "VCMatrix",
}


def t(local: str) -> str:
    return f"{{{WS_NS}}}{local}"


def _text(el: ET.Element, tag: str) -> str:
    c = el.find(tag)
    return (c.text or "").strip() if c is not None else ""


def _int(s: str | None) -> int | None:
    if s and s.isdigit():
        return int(s)
    return None


# ---------------------------------------------------------------------------
# Function detail extraction
# ---------------------------------------------------------------------------
def _fn_detail(el: ET.Element) -> dict:
    fid = int(el.get("ID", -1))
    typ = el.get("Type", "?")
    name = el.get("Name", "")
    speed = el.get("Speed", "")
    tempo = ""
    step_ids: list[int] = []
    step_count = 0
    member_ids: list[int] = []

    if typ == "Chaser":
        tempo_el = el.find(t("Speed"))
        tempo = tempo_el.get("TempoType", "") if tempo_el is not None else ""
        for step in el.findall(f".//{t('Step')}"):
            sid = _int(step.get("FunctionID") or step.get("Number"))
            if sid is not None:
                step_ids.append(sid)
        step_count = len(step_ids)
    elif typ == "Collection":
        for step in el.findall(t("Step")):
            sid = _int(step.get("FunctionID") or step.text)
            if sid is not None:
                member_ids.append(sid)

    d: dict = {
        "id": fid,
        "type": typ,
        "name": name,
    }
    if speed:
        d["speed"] = speed
    if tempo:
        d["tempo"] = tempo
    if step_count:
        d["step_count"] = step_count
        d["step_ids"] = step_ids
    if member_ids:
        d["member_ids"] = member_ids
    return d


# ---------------------------------------------------------------------------
# VC widget detail extraction
# ---------------------------------------------------------------------------
def _widget_detail(el: ET.Element) -> dict | None:
    local = el.tag.split("}")[-1] if "}" in el.tag else el.tag
    if local not in _VC_WIDGET_TAGS:
        return None

    wid_str = el.get("ID", "")
    wid = _int(wid_str)
    caption = el.get("Caption", "")
    x = _int(el.get("X"))
    y = _int(el.get("Y"))
    w = _int(el.get("Width"))
    h = _int(el.get("Height"))
    visibility = _int(el.get("Visibility"))

    fn_refs: list[int] = []
    for fn_el in el.findall(t("Function")):
        fid = _int(fn_el.get("ID"))
        if fid is not None:
            fn_refs.append(fid)
    # also single Function element (Button / Slider)
    direct_fn = el.find(t("Function"))
    if direct_fn is not None:
        fid = _int(direct_fn.get("ID"))
        if fid is not None and fid not in fn_refs:
            fn_refs.append(fid)

    preset_count = len(el.findall(t("Preset")))

    return {
        "id": wid,
        "type": local,
        "caption": caption,
        "x": x,
        "y": y,
        "w": w,
        "h": h,
        "fn_refs": fn_refs,
        "visibility": visibility,
        "preset_count": preset_count,
    }


# ---------------------------------------------------------------------------
# Free ID range computation
# ---------------------------------------------------------------------------
def _free_id_ranges(fn_ids: list[int], padding: int = 100) -> list[dict]:
    if not fn_ids:
        return []
    id_set = set(fn_ids)
    max_id = max(fn_ids) + padding
    ranges: list[dict] = []
    start = None
    for i in range(0, max_id + 2):
        if i not in id_set:
            if start is None:
                start = i
        else:
            if start is not None and i - start >= 2:
                ranges.append({"from": start, "to": i - 1, "count": i - start})
                start = None
            else:
                start = None
        if len(ranges) >= 20:
            break
    return ranges


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    tree = ET.parse(QXW)
    r = tree.getroot()
    eng = r.find(f"./{t('Engine')}")
    if eng is None:
        raise SystemExit("No <Engine> in workspace")

    # --- Engine functions ---
    fn_by_type: Counter[str] = Counter()
    fn_ids: list[int] = []
    functions_detail: list[dict] = []
    collections_detail: list[dict] = []

    for el in eng:
        if el.tag != t("Function"):
            continue
        d = _fn_detail(el)
        functions_detail.append(d)
        fn_by_type[d["type"]] += 1
        fn_ids.append(d["id"])
        if d["type"] == "Collection":
            collections_detail.append({
                "id": d["id"],
                "name": d["name"],
                "member_ids": d.get("member_ids", []),
            })

    # --- Fixtures ---
    fixtures: list[dict] = []
    fx_ids: list[int] = []
    for el in eng:
        if el.tag != t("Fixture"):
            continue
        i = _text(el, t("ID"))
        fixtures.append({
            "id": int(i) if i.isdigit() else i,
            "name": _text(el, t("Name")),
            "manufacturer": _text(el, t("Manufacturer")),
            "model": _text(el, t("Model")),
            "mode": _text(el, t("Mode")),
            "universe": _text(el, t("Universe")),
            "address": _text(el, t("Address")),
            "channels": _text(el, t("Channels")),
        })
        if i.isdigit():
            fx_ids.append(int(i))

    # --- VC widgets ---
    vc = r.find(f"./{t('VirtualConsole')}")
    vc_widgets_detail: list[dict] = []
    cross_refs: dict[int, list[int]] = {}  # fn_id -> [widget_id, ...]

    if vc is not None:
        for el in vc.iter():
            if el is vc:
                continue
            d = _widget_detail(el)
            if d is None:
                continue
            vc_widgets_detail.append(d)
            if d["id"] is not None:
                for fid in d["fn_refs"]:
                    cross_refs.setdefault(fid, []).append(d["id"])

    free_ranges = _free_id_ranges(fn_ids)

    out = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "showfile": str(QXW.name),
        "summary": {
            "function_count": sum(fn_by_type.values()),
            "by_type": dict(sorted(fn_by_type.items())),
            "id_min": min(fn_ids) if fn_ids else None,
            "id_max": max(fn_ids) if fn_ids else None,
            "fixture_count": len(fixtures),
            "fixture_ids": sorted(set(fx_ids)),
            "vc_widget_count": len(vc_widgets_detail),
        },
        "functions_detail": functions_detail,
        "collections_detail": collections_detail,
        "vc_widgets_detail": vc_widgets_detail,
        "cross_refs": {str(k): v for k, v in sorted(cross_refs.items())},
        "free_id_ranges": free_ranges,
        "fixtures": fixtures,
    }

    out_path = ROOT / "_output" / "_QXW_INDEX.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    fn_ct = out["summary"]["function_count"]
    widget_ct = out["summary"]["vc_widget_count"]
    print(f"Wrote _QXW_INDEX.json ({fn_ct} functions, {len(fixtures)} fixtures, {widget_ct} VC widgets)")
    if free_ranges:
        top = free_ranges[:3]
        print(f"  First free ranges: {[(r['from'], r['to']) for r in top]}")


if __name__ == "__main__":
    main()
