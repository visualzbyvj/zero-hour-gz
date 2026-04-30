# -*- coding: utf-8 -*-
"""Snapshot the showfile and save VC widget fingerprints.

Default (no flags):
    Copy the main showfile into _snapshots/ with a timestamp, then write
    _vc_snapshot.json containing a per-widget fingerprint (type, caption,
    visibility, preset_count, fn_count, W, H, timestamp).

--check flag:
    Load _vc_snapshot.json and compare against the *current* showfile.
    Print any regressions (widgets that were present but are now missing or
    have changed type/caption/fn_count/size).

Usage:
    python _snapshot.py                   # checkpoint + write fingerprints
    python _snapshot.py --label pre-fx    # add a label to the snapshot filename
    python _snapshot.py --check           # compare current to last snapshot
"""
from __future__ import annotations

import argparse
import json
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import QXW

ROOT = Path(__file__).resolve().parent.parent
SNAP_DIR = ROOT / "_snapshots"
VC_SNAP = ROOT / "_output" / "_vc_snapshot.json"
WS_NS = "http://www.qlcplus.org/Workspace"
_VC_WIDGET_TAGS = {
    "Button", "Slider", "SpeedDial", "Frame", "SoloFrame", "Label",
    "XYPad", "AnimationWidget", "Knob", "AudioTriggerWidget", "VideoPlayer",
    "Clock", "VCMatrix",
}


def t(local: str) -> str:
    return f"{{{WS_NS}}}{local}"


def _fingerprint_widgets(qxw: Path) -> list[dict]:
    """Parse the showfile and return a fingerprint record for every VC widget."""
    r = ET.parse(qxw).getroot()
    vc = r.find(f"./{t('VirtualConsole')}")
    if vc is None:
        return []
    widgets: list[dict] = []
    for el in vc.iter():
        local = el.tag.split("}")[-1] if "}" in el.tag else el.tag
        if local not in _VC_WIDGET_TAGS:
            continue
        wid_s = el.get("ID", "")
        if not wid_s.isdigit():
            continue
        fn_refs = [
            fn_el.get("ID", "")
            for fn_el in el.findall(t("Function"))
            if fn_el.get("ID", "").isdigit()
        ]
        widgets.append({
            "id": int(wid_s),
            "type": local,
            "caption": el.get("Caption", ""),
            "visibility": el.get("Visibility"),
            "preset_count": len(el.findall(t("Preset"))),
            "fn_count": len(fn_refs),
            "fn_refs": [int(x) for x in fn_refs],
            "w": el.get("Width"),
            "h": el.get("Height"),
        })
    return widgets


def write_snapshot(label: str) -> None:
    if not QXW.is_file():
        raise SystemExit(f"Missing {QXW}")

    SNAP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    tag = f"_{label}" if label else ""
    dest = SNAP_DIR / f"{QXW.stem}{tag}_{ts}.qxw"
    shutil.copy2(QXW, dest)
    print(f"Snapshot saved: {dest}")

    widgets = _fingerprint_widgets(QXW)
    payload = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "snapshot_file": str(dest.name),
        "widget_count": len(widgets),
        "widgets": widgets,
    }
    VC_SNAP.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Fingerprints written: _vc_snapshot.json ({len(widgets)} widgets)")


def check_regression() -> None:
    if not VC_SNAP.is_file():
        raise SystemExit("_vc_snapshot.json not found -- run `python _snapshot.py` first")
    if not QXW.is_file():
        raise SystemExit(f"Missing {QXW}")

    saved = json.loads(VC_SNAP.read_text(encoding="utf-8"))
    saved_ts = saved.get("generated", "?")
    saved_widgets: list[dict] = saved.get("widgets", [])
    saved_by_id = {w["id"]: w for w in saved_widgets}

    current_widgets = _fingerprint_widgets(QXW)
    current_by_id = {w["id"]: w for w in current_widgets}

    print(f"Comparing current showfile to snapshot from {saved_ts}")
    print(f"Snapshot: {len(saved_widgets)} widgets | Current: {len(current_widgets)} widgets")

    regressions: list[str] = []
    additions: list[str] = []

    for wid, sw in sorted(saved_by_id.items()):
        cw = current_by_id.get(wid)
        if cw is None:
            regressions.append(f"  MISSING [{wid}] {sw['type']} {sw['caption']!r}")
            continue
        changes: list[str] = []
        for field in ("type", "caption", "fn_count", "preset_count", "visibility"):
            if sw.get(field) != cw.get(field):
                changes.append(f"{field}: {sw.get(field)!r} -> {cw.get(field)!r}")
        if sw.get("w") != cw.get("w") or sw.get("h") != cw.get("h"):
            changes.append(f"size: {sw.get('w')}x{sw.get('h')} -> {cw.get('w')}x{cw.get('h')}")
        if sorted(sw.get("fn_refs", [])) != sorted(cw.get("fn_refs", [])):
            changes.append(f"fn_refs changed: {len(sw.get('fn_refs',[]))} -> {len(cw.get('fn_refs',[]))}")
        if changes:
            regressions.append(f"  CHANGED [{wid}] {cw['type']} {cw['caption']!r}: {', '.join(changes)}")

    for wid, cw in sorted(current_by_id.items()):
        if wid not in saved_by_id:
            additions.append(f"  NEW [{wid}] {cw['type']} {cw['caption']!r}")

    if regressions:
        print(f"\nREGRESSIONS ({len(regressions)}):")
        for r in regressions:
            print(r)
    else:
        print("\nNo regressions detected.")

    if additions:
        print(f"\nNew widgets ({len(additions)}):")
        for a in additions[:20]:
            print(a)
        if len(additions) > 20:
            print(f"  ... (+{len(additions)-20} more)")

    if regressions:
        raise SystemExit(1)


def main() -> None:
    ap = argparse.ArgumentParser(description="Snapshot showfile and manage VC fingerprints")
    ap.add_argument("--label", default="", help="Optional tag in snapshot filename")
    ap.add_argument("--check", action="store_true",
                    help="Compare current showfile to last snapshot (regression check)")
    args = ap.parse_args()

    if args.check:
        check_regression()
    else:
        write_snapshot(args.label)


if __name__ == "__main__":
    main()
