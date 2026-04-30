# -*- coding: utf-8 -*-
"""Semantic diff: compare main showfile to the newest backup.

Usage:
    python _what_changed.py                   # compare QXW vs latest backup
    python _what_changed.py <a.qxw> <b.qxw>  # compare two explicit files

Outputs a structured report:
  - Functions added / deleted / modified (name, type, step count)
  - VC widgets added / deleted / repositioned / resized / fn-ref changes
  - Speed dial config changes (preset count, visibility)
  - Collection membership changes
  - Warning if hash matches (no diff at all)
"""
from __future__ import annotations

import hashlib
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import BACKUP_DIR, QXW

WS_NS = "http://www.qlcplus.org/Workspace"
_VC_WIDGET_TAGS = {
    "Button", "Slider", "SpeedDial", "Frame", "SoloFrame", "Label",
    "XYPad", "AnimationWidget", "Knob", "AudioTriggerWidget", "VideoPlayer",
    "Clock", "VCMatrix",
}


def t(local: str) -> str:
    return f"{{{WS_NS}}}{local}"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()[:16]


# ---------------------------------------------------------------------------
# Extract structured maps from a QXW file
# ---------------------------------------------------------------------------
def _fn_map(eng: ET.Element) -> dict[int, dict[str, Any]]:
    """Return {fn_id: {type, name, step_count, member_ids}}."""
    result: dict[int, dict[str, Any]] = {}
    for el in eng:
        if el.tag != t("Function"):
            continue
        fid_s = el.get("ID", "")
        if not fid_s.isdigit():
            continue
        fid = int(fid_s)
        typ = el.get("Type", "?")
        name = el.get("Name", "")
        step_count = len(el.findall(f".//{t('Step')}"))
        members = [
            int(s.get("FunctionID") or s.text or "-1")
            for s in el.findall(t("Step"))
            if s.get("FunctionID") or s.text
        ]
        result[fid] = {
            "type": typ,
            "name": name,
            "step_count": step_count,
            "members": members,
        }
    return result


def _widget_map(vc: ET.Element | None) -> dict[int, dict[str, Any]]:
    """Return {widget_id: {type, caption, x, y, w, h, fn_refs, preset_count, visibility}}."""
    if vc is None:
        return {}
    result: dict[int, dict[str, Any]] = {}
    for el in vc.iter():
        local = el.tag.split("}")[-1] if "}" in el.tag else el.tag
        if local not in _VC_WIDGET_TAGS:
            continue
        wid_s = el.get("ID", "")
        if not wid_s.isdigit():
            continue
        wid = int(wid_s)

        fn_refs: list[int] = []
        for fn_el in el.findall(t("Function")):
            fid_s = fn_el.get("ID", "")
            if fid_s.isdigit():
                fn_refs.append(int(fid_s))

        result[wid] = {
            "type": local,
            "caption": el.get("Caption", ""),
            "x": el.get("X"),
            "y": el.get("Y"),
            "w": el.get("Width"),
            "h": el.get("Height"),
            "fn_refs": fn_refs,
            "preset_count": len(el.findall(t("Preset"))),
            "visibility": el.get("Visibility"),
        }
    return result


def _parse(path: Path) -> tuple[ET.Element, ET.Element | None]:
    r = ET.parse(path).getroot()
    eng = r.find(f"./{t('Engine')}")
    vc = r.find(f"./{t('VirtualConsole')}")
    return eng, vc


# ---------------------------------------------------------------------------
# Diff helpers
# ---------------------------------------------------------------------------
def _diff_functions(
    a_fns: dict[int, dict], b_fns: dict[int, dict]
) -> list[str]:
    lines: list[str] = []
    a_ids = set(a_fns)
    b_ids = set(b_fns)

    added = sorted(b_ids - a_ids)
    deleted = sorted(a_ids - b_ids)
    common = a_ids & b_ids

    if added:
        lines.append(f"  Functions ADDED ({len(added)}):")
        for fid in added[:20]:
            d = b_fns[fid]
            nm = d["name"]
            lines.append(f"    + [{fid}] {d['type']} {nm!r}  steps={d['step_count']}")
        if len(added) > 20:
            lines.append(f"    ... (+{len(added)-20} more)")

    if deleted:
        lines.append(f"  Functions DELETED ({len(deleted)}):")
        for fid in deleted[:20]:
            d = a_fns[fid]
            nm = d["name"]
            lines.append(f"    - [{fid}] {d['type']} {nm!r}  steps={d['step_count']}")
        if len(deleted) > 20:
            lines.append(f"    ... (+{len(deleted)-20} more)")

    modified: list[str] = []
    for fid in sorted(common):
        a = a_fns[fid]
        b = b_fns[fid]
        changes: list[str] = []
        if a["name"] != b["name"]:
            changes.append(f"name: {a['name']!r} -> {b['name']!r}")
        if a["type"] != b["type"]:
            changes.append(f"type: {a['type']} -> {b['type']}")
        if a["step_count"] != b["step_count"]:
            changes.append(f"steps: {a['step_count']} -> {b['step_count']}")
        if changes:
            bname = b["name"]
            modified.append(f"    ~ [{fid}] {b['type']} {bname!r}: {', '.join(changes)}")

    if modified:
        lines.append(f"  Functions MODIFIED ({len(modified)}):")
        lines.extend(modified[:20])
        if len(modified) > 20:
            lines.append(f"    ... (+{len(modified)-20} more)")

    if not (added or deleted or modified):
        lines.append("  Functions: no changes")

    return lines


def _diff_widgets(
    a_wgs: dict[int, dict], b_wgs: dict[int, dict]
) -> list[str]:
    lines: list[str] = []
    a_ids = set(a_wgs)
    b_ids = set(b_wgs)

    added = sorted(b_ids - a_ids)
    deleted = sorted(a_ids - b_ids)
    common = a_ids & b_ids

    if added:
        lines.append(f"  VC Widgets ADDED ({len(added)}):")
        for wid in added[:15]:
            d = b_wgs[wid]
            cap = d["caption"]
            lines.append(f"    + [{wid}] {d['type']} {cap!r}")
        if len(added) > 15:
            lines.append(f"    ... (+{len(added)-15} more)")

    if deleted:
        lines.append(f"  VC Widgets DELETED ({len(deleted)}):")
        for wid in deleted[:15]:
            d = a_wgs[wid]
            cap = d["caption"]
            lines.append(f"    - [{wid}] {d['type']} {cap!r}")
        if len(deleted) > 15:
            lines.append(f"    ... (+{len(deleted)-15} more)")

    modified: list[str] = []
    for wid in sorted(common):
        a = a_wgs[wid]
        b = b_wgs[wid]
        changes: list[str] = []
        if a["caption"] != b["caption"]:
            changes.append(f"caption: {a['caption']!r} -> {b['caption']!r}")
        if a["x"] != b["x"] or a["y"] != b["y"]:
            changes.append(f"pos: ({a['x']},{a['y']}) -> ({b['x']},{b['y']})")
        if a["w"] != b["w"] or a["h"] != b["h"]:
            changes.append(f"size: {a['w']}x{a['h']} -> {b['w']}x{b['h']}")
        if sorted(a["fn_refs"]) != sorted(b["fn_refs"]):
            changes.append(f"fn_refs: {sorted(a['fn_refs'])} -> {sorted(b['fn_refs'])}")
        if a["preset_count"] != b["preset_count"]:
            changes.append(f"presets: {a['preset_count']} -> {b['preset_count']}")
        if a["visibility"] != b["visibility"]:
            changes.append(f"visibility: {a['visibility']} -> {b['visibility']}")
        if changes:
            bcap = b["caption"]
            modified.append(f"    ~ [{wid}] {b['type']} {bcap!r}: {', '.join(changes)}")

    if modified:
        lines.append(f"  VC Widgets MODIFIED ({len(modified)}):")
        lines.extend(modified[:20])
        if len(modified) > 20:
            lines.append(f"    ... (+{len(modified)-20} more)")

    if not (added or deleted or modified):
        lines.append("  VC widgets: no changes")

    return lines


# ---------------------------------------------------------------------------
# Public API (used by _preview_changes.py --dry-run)
# ---------------------------------------------------------------------------
def semantic_diff(path_a: Path, path_b: Path, *, label_a: str = "A", label_b: str = "B") -> None:
    """Print structured semantic diff between two QXW files."""
    if sha256(path_a) == sha256(path_b):
        print(f"Files are IDENTICAL (hash match): {path_a.name} == {path_b.name}")
        return

    eng_a, vc_a = _parse(path_a)
    eng_b, vc_b = _parse(path_b)

    if eng_a is None or eng_b is None:
        print("Could not parse Engine from one or both files")
        return

    a_fns = _fn_map(eng_a)
    b_fns = _fn_map(eng_b)
    a_wgs = _widget_map(vc_a)
    b_wgs = _widget_map(vc_b)

    print(f"\n=== Semantic diff: {label_a}  ->  {label_b} ===")

    fn_lines = _diff_functions(a_fns, b_fns)
    print("\n[Functions]")
    for line in fn_lines:
        print(line)

    wg_lines = _diff_widgets(a_wgs, b_wgs)
    print("\n[VC Widgets]")
    for line in wg_lines:
        print(line)


def latest_backup() -> Path | None:
    if not BACKUP_DIR.is_dir():
        return None
    files = sorted(BACKUP_DIR.glob("*.qxw"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def main() -> None:
    if len(sys.argv) == 3:
        path_a = Path(sys.argv[1])
        path_b = Path(sys.argv[2])
        if not path_a.is_file():
            raise SystemExit(f"Not found: {path_a}")
        if not path_b.is_file():
            raise SystemExit(f"Not found: {path_b}")
        semantic_diff(path_a, path_b, label_a=path_a.name, label_b=path_b.name)
        return

    lb = latest_backup()
    if lb is None:
        raise SystemExit("No backups in _Showfile_Backups")
    if not QXW.is_file():
        raise SystemExit(f"Missing {QXW}")

    print("Main:  ", QXW)
    print("Backup:", lb)
    semantic_diff(lb, QXW, label_a=lb.name, label_b="current")


if __name__ == "__main__":
    main()
