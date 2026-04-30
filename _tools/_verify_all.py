"""Comprehensive verification of the showfile after rebuild."""
from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QXW = ROOT / "Zero Hour GZ Project File.qxw"
NS = {"qlc": "http://www.qlcplus.org/Workspace"}


def banner(msg: str) -> None:
    print("\n" + "=" * 72)
    print(f"  {msg}")
    print("=" * 72)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    banner("SHOWFILE INTEGRITY")
    size = QXW.stat().st_size
    print(f"Path   : {QXW}")
    print(f"Size   : {size:,} bytes ({size / 1024 / 1024:.2f} MB)")

    try:
        tree = ET.parse(QXW)
    except ET.ParseError as e:
        errors.append(f"XML parse failed: {e}")
        print(f"PARSE FAIL: {e}")
        return 1
    root = tree.getroot()
    print("XML parse: OK")

    engine = root.find("./qlc:Engine", NS)
    vc = root.find("./qlc:VirtualConsole", NS)

    # ── Functions ───────────────────────────────────────────────────────
    banner("FUNCTION LIBRARY")
    top_fns = engine.findall("./qlc:Function", NS)
    types = Counter(f.get("Type") for f in top_fns)
    print(f"Top-level functions: {len(top_fns)}")
    for t, c in types.most_common():
        print(f"  {t:15s} {c}")

    ids = [int(f.get("ID")) for f in top_fns]
    id_counts = Counter(ids)
    dups = {k: v for k, v in id_counts.items() if v > 1}
    if dups:
        errors.append(f"Duplicate function IDs: {dups}")
    print(f"Duplicate IDs: {len(dups)}")
    print(f"ID range: {min(ids)} to {max(ids)}")

    all_ids = set(ids)

    # ── Function cross-references ────────────────────────────────────────
    banner("FUNCTION CROSS-REFERENCES")
    missing_refs: dict[int, list[int]] = {}
    for fn in top_fns:
        fid = int(fn.get("ID"))
        ftype = fn.get("Type")
        refs: list[int] = []

        if ftype == "Chaser":
            for step in fn.findall("./qlc:Step", NS):
                fun_attr = step.get("FadeIn") and step.get("Hold") and step.get("FadeOut") and step.get("Number")
                val = step.text
                if val is not None:
                    try:
                        refs.append(int(val.strip()))
                    except ValueError:
                        pass
        elif ftype == "Collection":
            for step in fn.findall("./qlc:Step", NS):
                val = step.text
                if val is not None:
                    try:
                        refs.append(int(val.strip()))
                    except ValueError:
                        pass

        for r in refs:
            if r not in all_ids:
                missing_refs.setdefault(fid, []).append(r)

    if missing_refs:
        errors.append(f"{len(missing_refs)} functions reference missing IDs")
        for fid, refs in list(missing_refs.items())[:5]:
            print(f"  Function {fid} -> missing {refs}")
    else:
        print("All function step references resolve: OK")

    # ── Fixture groups ───────────────────────────────────────────────────
    banner("FIXTURE GROUPS & FIXTURES")
    fixtures = engine.findall("./qlc:Fixture", NS)
    groups = engine.findall("./qlc:FixtureGroup", NS)
    print(f"Fixtures: {len(fixtures)}")
    print(f"Fixture groups: {len(groups)}")
    for g in groups:
        name = g.find("./qlc:Name", NS)
        sz = g.find("./qlc:Size", NS)
        heads = g.findall("./qlc:Head", NS)
        n = name.text if name is not None else "?"
        s = (sz.get("X"), sz.get("Y")) if sz is not None else ("?", "?")
        print(f"  {n:45s} size={s[0]}x{s[1]} heads={len(heads)}")

    # ── Virtual Console ──────────────────────────────────────────────────
    banner("VIRTUAL CONSOLE")
    pages = vc.findall("./qlc:Frame", NS) if vc is not None else []
    print(f"Pages: {len(pages)}")

    all_vc_fn_refs: list[int] = []
    for i, p in enumerate(pages):
        caption = p.get("Caption", "?")
        buttons = p.findall(".//qlc:Button", NS)
        sliders = p.findall(".//qlc:Slider", NS)
        frames = p.findall(".//qlc:Frame", NS)
        solo = p.findall(".//qlc:SoloFrame", NS)
        matrix = p.findall(".//qlc:Matrix", NS)
        speed = p.findall(".//qlc:SpeedDial", NS)
        label = p.findall(".//qlc:Label", NS)

        for b in buttons + sliders + matrix:
            fn = b.find("./qlc:Function", NS)
            if fn is not None:
                try:
                    fid = int(fn.get("ID"))
                    all_vc_fn_refs.append(fid)
                except (ValueError, TypeError):
                    pass
        for sd in speed:
            for fn in sd.findall("./qlc:Function", NS):
                val = (fn.text or "").strip()
                if val:
                    try:
                        all_vc_fn_refs.append(int(val))
                    except ValueError:
                        pass

        print(
            f"  {i}: {caption:12s} "
            f"btns={len(buttons):3d} "
            f"sld={len(sliders):2d} "
            f"fr={len(frames):2d} "
            f"solo={len(solo):2d} "
            f"mat={len(matrix):2d} "
            f"spd={len(speed):2d} "
            f"lbl={len(label):2d}"
        )

    unique_refs = set(all_vc_fn_refs)
    UINT32_MAX = 4294967295
    missing_vc = [r for r in unique_refs if r not in all_ids and r != UINT32_MAX]
    if missing_vc:
        errors.append(f"VC references missing function IDs: {sorted(missing_vc)}")
        print(f"\nVC MISSING FN REFS: {sorted(missing_vc)}")
    else:
        print(f"\nAll VC widget function refs resolve: OK ({len(unique_refs)} unique IDs referenced)")

    # ── Dead/orphan functions ────────────────────────────────────────────
    banner("DEAD / ORPHAN FUNCTIONS")
    referenced = set(all_vc_fn_refs)
    for fn in top_fns:
        ftype = fn.get("Type")
        if ftype in ("Chaser", "Collection"):
            for step in fn.findall("./qlc:Step", NS):
                val = step.text
                if val is not None:
                    try:
                        referenced.add(int(val.strip()))
                    except ValueError:
                        pass
    orphans = sorted(all_ids - referenced)
    if orphans:
        warnings.append(f"{len(orphans)} orphan functions (kept as clone seeds): {orphans}")
        print(f"Orphans (kept as clone seeds): {len(orphans)}")
        print(f"  IDs: {orphans}")
    else:
        print("No orphan functions")

    # ── Builders / pipeline ──────────────────────────────────────────────
    banner("BUILDER PIPELINE")
    builders_dir = ROOT / "_builders"
    builders = sorted(p.name for p in builders_dir.glob("_build_*.py"))
    print(f"Builders present: {len(builders)}")
    for b in builders:
        print(f"  {b}")

    rebuild_all = (ROOT / "_rebuild_all.py").read_text(encoding="utf-8")
    import re as _re
    referenced_builders = _re.findall(r'"(_builders/[^"]+\.py)"', rebuild_all)
    print(f"\nScripts in _rebuild_all.py sequence: {len(referenced_builders)}")
    for b in referenced_builders:
        exists = (ROOT / b).exists()
        status = "OK " if exists else "MISSING"
        print(f"  [{status}] {b}")
        if not exists:
            errors.append(f"Rebuild references missing builder: {b}")

    # ── Docs / legacy folders ────────────────────────────────────────────
    banner("FOLDER HYGIENE")
    legacy = ["_debug", "_patches", "_frames", "_frames_tmp", "_PRE_RESTRUCTURE_BACKUP_20260413"]
    for f in legacy:
        p = ROOT / f
        if p.exists():
            items = list(p.iterdir()) if p.is_dir() else []
            print(f"  EXISTS: {f:45s} items={len(items)}")
        else:
            print(f"  CLEAN : {f}")

    # ── Summary ──────────────────────────────────────────────────────────
    banner("VERIFICATION SUMMARY")
    print(f"Errors   : {len(errors)}")
    for e in errors:
        print(f"  ERR  {e}")
    print(f"Warnings : {len(warnings)}")
    for w in warnings:
        print(f"  WARN {w}")

    status = "PASS" if not errors else "FAIL"
    print(f"\n>>> STATUS: {status} <<<")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
