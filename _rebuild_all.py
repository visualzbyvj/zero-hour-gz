# -*- coding: utf-8 -*-
"""Run all Zero Hour GZ engine + VC build scripts; validate; report; post-tools.

Architecture note: WHY THE BUILD IS SERIAL
-------------------------------------------
Each builder (e.g. _build_ring_fx.py, _build_strobes.py, ...) follows the
pattern:

    text = QXW.read_text(encoding="utf-8")   # read whole file
    text = modify(text)                       # strip + reinsert XML blocks
    QXW.write_text(text, encoding="utf-8")   # write whole file

Because every script reads and writes the *same* shared .qxw file, running
two scripts concurrently would produce a race condition where one script
overwrites another's changes.

True parallel stages would require each script to:
  (a) operate on separate in-memory XML fragment, then
  (b) merge all fragments into the workspace in a single atomic write.

This is a significant architectural change that risks introducing merge bugs
in a production showfile. The current 10-20 s serial build is acceptable
and safe. The post-build tools (_qxw_index.py, _lint_showfile.py) run in
parallel because they are read-only.

Do NOT add subprocess parallelism to the SCRIPTS list without first
refactoring all builders to operate on XML fragment objects instead of
full-file text replacement.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from _qlc_helpers import QXW, auto_backup

ROOT = Path(__file__).resolve().parent
WS_NS = "http://www.qlcplus.org/Workspace"


def tag(local: str) -> str:
    return f"{{{WS_NS}}}{local}"


OPTIONAL_SCRIPTS: set[str] = set()

SCRIPTS = [
    "_builders/_build_advanced_fns.py",
    "_builders/_patch_ring_chase.py",
    "_builders/_build_ring_fx.py",
    "_builders/_build_ring_out_in_chase.py",
    "_builders/_build_colored_out_in.py",
    "_builders/_build_ring_fx_matrix.py",
    "_builders/_build_strobes.py",
    "_builders/_build_all_color.py",
    "_builders/_build_spatial_splits.py",
    "_builders/_build_macros.py",
    "_builders/_build_bump.py",
    "_builders/_build_ring_fx_soft.py",
    "_builders/_build_accel_chasers.py",
    "_builders/_build_tunnel.py",
    "_builders/_build_white_ring_layer.py",
    "_builders/_build_bass_hits.py",
    "_builders/_build_show_arc.py",
    "_builders/_build_intensity_faders.py",
    "_builders/_build_ring_rgbmatrix.py",
    "_builders/_build_cosmic.py",
    "_builders/_build_genres.py",
    "_builders/_build_new_vc.py",
]


def validate_qxw(path: Path) -> None:
    ET.parse(path)


def rollback_latest_backup() -> Path | None:
    bdir = ROOT / "_Showfile_Backups"
    if not bdir.is_dir():
        return None
    files = sorted(bdir.glob("Zero Hour GZ Project File*.qxw"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        return None
    src = files[0]
    import shutil
    shutil.copy2(src, QXW)
    return src


def write_function_registry(path: Path = ROOT / "_docs" / "_FUNCTION_REGISTRY.md") -> None:
    tree = ET.parse(QXW)
    root = tree.getroot()
    eng = root.find(f".//{tag('Engine')}")
    if eng is None:
        path.write_text("# Function registry\n\n(No Engine)\n", encoding="utf-8")
        return
    rows: list[str] = ["# Function registry", "", "| ID | Type | Name | Tempo |", "|----|------|------|-------|"]
    for fn in eng:
        if fn.tag != tag("Function"):
            continue
        fid = fn.get("ID", "?")
        typ = fn.get("Type", "?")
        name = (fn.get("Name") or "").replace("|", "\\|")[:80]
        tempo_el = fn.find(tag("Tempo"))
        tempo = tempo_el.text if tempo_el is not None and tempo_el.text else "-"
        rows.append(f"| {fid} | {typ} | {name} | {tempo} |")
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def ld_sanity_warnings(vc_xml: str) -> list[str]:
    import re

    w: list[str] = []
    if "3060" not in vc_xml:
        w.append("LD sanity: PANIC scene ID 3060 not found in VirtualConsole block")
    if re.search(r"<SliderMode[^>]*>Playback</SliderMode>[\s\S]*?<Level[^>]*Value=\"255\"", vc_xml):
        w.append("LD sanity: Playback slider Value=255 may auto-start a cue (verify)")
    return w


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rollback", action="store_true", help="Restore latest _Showfile_Backups copy to main qxw")
    ap.add_argument("--no-post", action="store_true", help="Skip parallel post tools (_qxw_index, _lint_showfile)")
    ap.add_argument("--no-prune", action="store_true", help="Skip dead-function pruning pass")
    args = ap.parse_args()
    if args.rollback:
        src = rollback_latest_backup()
        if not src:
            raise SystemExit("No backup found.")
        print(f"Restored from {src}")
        return

    if not QXW.is_file():
        raise SystemExit(f"Missing showfile: {QXW}")

    t0 = time.perf_counter()
    validate_qxw(QXW)
    backup = auto_backup(QXW)
    print(f"Backup: {backup}")

    report: dict = {"started": datetime.now().isoformat(), "steps": [], "failed": []}
    failed: list[str] = []

    for script in SCRIPTS:
        sp = ROOT / script
        if not sp.is_file():
            if script in OPTIONAL_SCRIPTS:
                print(f"SKIP (optional missing): {script}")
                report["steps"].append({"script": script, "status": "skipped_optional"})
                continue
            print(f"FAIL (missing required): {script}")
            failed.append(script)
            report["steps"].append({"script": script, "status": "missing"})
            break
        print(f"--- {script} ---")
        t1 = time.perf_counter()
        r = subprocess.run(
            [sys.executable, str(sp)],
            cwd=str(ROOT),
            check=False,
            timeout=120,
        )
        ms = int((time.perf_counter() - t1) * 1000)
        if r.returncode != 0:
            print(f"FAIL: {script} exit {r.returncode}")
            failed.append(script)
            report["steps"].append({"script": script, "status": "fail", "exit": r.returncode, "ms": ms})
            break
        try:
            validate_qxw(QXW)
        except ET.ParseError as e:
            print(f"FAIL XML after {script}: {e}")
            failed.append(script)
            report["steps"].append({"script": script, "status": "xml_fail", "ms": ms})
            break
        print(f"OK: {script}")
        report["steps"].append({"script": script, "status": "ok", "ms": ms})

    report["elapsed_ms"] = int((time.perf_counter() - t0) * 1000)
    report["failed"] = failed

    (ROOT / "_output" / "_build_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    if failed:
        raise SystemExit(f"Rebuild finished with errors: {failed}")

    print("All steps completed; XML valid.")

    # Dedup engine functions (builders may reintroduce duplicates)
    from _dedup_engine import dedup
    raw = QXW.read_text(encoding="utf-8")
    deduped, total, removed = dedup(raw)
    if removed:
        QXW.write_text(deduped, encoding="utf-8")
        print(f"Dedup: removed {removed} duplicate Function blocks ({total} -> {total - removed})")
    else:
        print("Dedup: no duplicates found")

    if not args.no_prune:
        from _tools._prune_dead_functions import prune_dead_functions
        before_total, pruned = prune_dead_functions(dry_run=False, backup=False)
        if pruned:
            print(f"Prune: removed {pruned} dead functions")
        else:
            print(f"Prune: no dead functions found ({before_total} total)")

    write_function_registry()
    print("Wrote _FUNCTION_REGISTRY.md")

    if not args.no_post:

        def run_tool(name: str) -> tuple[str, int]:
            p = ROOT / name
            if not p.is_file():
                return name, -1
            r = subprocess.run([sys.executable, str(p)], cwd=str(ROOT), timeout=300)
            return name, r.returncode

        post = ["_tools/_qxw_index.py", "_tools/_lint_showfile.py"]
        with ThreadPoolExecutor(max_workers=2) as ex:
            futs = [ex.submit(run_tool, n) for n in post]
            for f in as_completed(futs):
                name, code = f.result()
                if code == -1:
                    print(f"POST skip (missing): {name}")
                elif code != 0:
                    print(f"POST FAIL: {name} exit {code}")
                else:
                    print(f"POST OK: {name}")

    vc_text = QXW.read_text(encoding="utf-8")
    try:
        a, b = vc_text.index("<VirtualConsole>"), vc_text.index("</VirtualConsole>") + len("</VirtualConsole>")
        for line in ld_sanity_warnings(vc_text[a:b]):
            print("WARN", line)
    except ValueError:
        pass


if __name__ == "__main__":
    main()