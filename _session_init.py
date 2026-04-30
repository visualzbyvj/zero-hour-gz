# -*- coding: utf-8 -*-
"""Session dashboard: environment smoke check + build state + counts + free IDs.

Run at the start of every coding session:
    python _session_init.py
"""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

from _qlc_helpers import QXW

ROOT = Path(__file__).resolve().parent

DIVIDER = "-" * 60


def _banner(title: str) -> None:
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)


def _ok(label: str, value: str = "") -> None:
    print(f"  [OK]  {label}{(' -- ' + value) if value else ''}")


def _warn(label: str, value: str = "") -> None:
    print(f"  [!!]  {label}{(' -- ' + value) if value else ''}")


def _info(label: str, value: str) -> None:
    print(f"        {label}: {value}")


# ---------------------------------------------------------------------------
# Section 1: Environment
# ---------------------------------------------------------------------------
def check_environment() -> bool:
    _banner("Environment")
    ok = True

    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 9):
        _warn(f"Python {sys.version.split()[0]} -- requires 3.9+")
        ok = False
    else:
        _ok(f"Python {sys.version.split()[0]}")

    _info("Project root", str(ROOT))
    _info("Showfile", str(QXW.name) + (" (EXISTS)" if QXW.is_file() else " (MISSING)"))

    if not QXW.is_file():
        _warn("Showfile missing -- cannot proceed")
        return False

    try:
        ET.parse(QXW)
        _ok("XML parse")
    except ET.ParseError as exc:
        _warn(f"XML parse FAILED: {exc}")
        ok = False

    tools = [
        "_rebuild_all.py",
        "_tools/_qxw_index.py",
        "_tools/_lint_showfile.py",
        "_widget_sizer.py",
        "_tools/_snapshot.py",
        "_tools/_preview_changes.py",
        "_tools/_what_changed.py",
        "_tools/_fixture_cache.py",
        "_builders/_templates.py",
        "_qlc_helpers.py",
        "_builders/_build_new_vc.py",
    ]
    missing = [tool for tool in tools if not (ROOT / tool).is_file()]
    if missing:
        for m in missing:
            _warn(f"Missing tool: {m}")
        ok = False
    else:
        _ok(f"Core tooling ({len(tools)} scripts present)")

    return ok


# ---------------------------------------------------------------------------
# Section 2: Last build report
# ---------------------------------------------------------------------------
def show_build_report() -> None:
    _banner("Last Build")
    rpt = ROOT / "_output" / "_build_report.json"
    if not rpt.is_file():
        _warn("_build_report.json not found -- run `python _rebuild_all.py`")
        return
    try:
        data = json.loads(rpt.read_text(encoding="utf-8"))
    except Exception as exc:
        _warn(f"Could not read _build_report.json: {exc}")
        return

    ts = data.get("timestamp", "?")
    elapsed = data.get("elapsed_seconds", "?")
    scripts = data.get("scripts_run", [])
    failures = [s for s in scripts if s.get("returncode", 0) != 0] if isinstance(scripts, list) else []
    warnings = data.get("ld_sanity_warnings", [])

    _info("Timestamp", ts)
    _info("Elapsed", f"{elapsed}s" if elapsed != "?" else "?")
    scripts_count = len(scripts) if isinstance(scripts, list) else "?"
    _info("Scripts run", str(scripts_count))
    if failures:
        for f in failures:
            _warn(f"Script FAILED: {f.get('script', '?')}")
    else:
        _ok("All scripts passed")

    if warnings:
        _info("LD sanity warnings", str(len(warnings)))
        for w in warnings[:5]:
            print(f"    - {w}")
        if len(warnings) > 5:
            print(f"    ... (+{len(warnings)-5} more)")
    else:
        _ok("No LD sanity warnings")


# ---------------------------------------------------------------------------
# Section 3: QXW index summary
# ---------------------------------------------------------------------------
def show_index_summary() -> None:
    _banner("Showfile Index")
    idx = ROOT / "_output" / "_QXW_INDEX.json"
    if not idx.is_file():
        _warn("_QXW_INDEX.json not found -- run `python _qxw_index.py`")
        return
    try:
        data = json.loads(idx.read_text(encoding="utf-8"))
    except Exception as exc:
        _warn(f"Could not read _QXW_INDEX.json: {exc}")
        return

    gen = data.get("generated", "?")
    summ = data.get("summary", {})
    fn_ct = summ.get("function_count", "?")
    fx_ct = summ.get("fixture_count", "?")
    wg_ct = summ.get("vc_widget_count", "?")
    id_min = summ.get("id_min", "?")
    id_max = summ.get("id_max", "?")
    by_type = summ.get("by_type", {})

    _info("Index generated", gen)
    _info("Functions", f"{fn_ct}  (ID {id_min}..{id_max})")
    _info("Fixtures", str(fx_ct))
    _info("VC widgets", str(wg_ct))
    if by_type:
        for typ, cnt in sorted(by_type.items(), key=lambda x: -x[1]):
            print(f"    {typ:<22} {cnt}")

    free = data.get("free_id_ranges", [])
    if free:
        _info("First 5 free ID ranges", "")
        for rng in free[:5]:
            print(f"    [{rng['from']}..{rng['to']}]  ({rng['count']} IDs)")


# ---------------------------------------------------------------------------
# Section 4: Lint / LD audit
# ---------------------------------------------------------------------------
def show_lint_status() -> None:
    _banner("LD Audit (_LD_AUDIT.md)")
    audit = ROOT / "_docs" / "_LD_AUDIT.md"
    if not audit.is_file():
        _warn("_LD_AUDIT.md not found -- run `python _lint_showfile.py`")
        return

    text = audit.read_text(encoding="utf-8")
    # Count lines starting with WARN or ERROR
    warn_lines = [l for l in text.splitlines() if re.match(r".*(WARN|ERROR|WARNING)", l, re.I)]
    ok_lines = [l for l in text.splitlines() if re.match(r".*OK", l)]

    if warn_lines:
        _info("Warnings/errors in audit", str(len(warn_lines)))
        for w in warn_lines[:5]:
            print(f"    {w.strip()}")
        if len(warn_lines) > 5:
            print(f"    ... (+{len(warn_lines)-5} more)")
    else:
        _ok(f"LD audit clean ({len(ok_lines)} checks passed)")


# ---------------------------------------------------------------------------
# Section 5: Snapshot status
# ---------------------------------------------------------------------------
def show_snapshot_status() -> None:
    _banner("Snapshot Status")
    snap_dir = ROOT / "_snapshots"
    snaps = sorted(snap_dir.glob("*.qxw")) if snap_dir.is_dir() else []
    if snaps:
        latest = snaps[-1]
        _ok(f"Latest snapshot: {latest.name}")
        _info("Snapshot count", str(len(snaps)))
    else:
        _warn("No snapshots in _snapshots/ -- run `python _snapshot.py`")

    vc_snap = ROOT / "_output" / "_vc_snapshot.json"
    if vc_snap.is_file():
        try:
            data = json.loads(vc_snap.read_text(encoding="utf-8"))
            ts = data.get("generated", "?")
            widget_ct = len(data.get("widgets", []))
            _ok(f"_vc_snapshot.json: {widget_ct} widgets  (saved {ts})")
        except Exception:
            _warn("_vc_snapshot.json exists but could not be parsed")
    else:
        _warn("No _vc_snapshot.json -- run `python _snapshot.py` after rebuild")


# ---------------------------------------------------------------------------
# Quick reference
# ---------------------------------------------------------------------------
def show_quick_ref() -> None:
    _banner("Quick Reference")
    cmds = [
        ("python _rebuild_all.py", "full rebuild (20 scripts + lint + index)"),
        ("python _rebuild_all.py --rollback", "restore last backup"),
        ("python _tools/_lint_showfile.py", "write _docs/_LD_AUDIT.md"),
        ("python _tools/_lint_showfile.py --strict", "same but fail on warnings"),
        ("python _tools/_qxw_index.py", "refresh _output/_QXW_INDEX.json"),
        ("python _tools/_what_changed.py", "semantic diff vs latest backup"),
        ("python _tools/_preview_changes.py --dry-run", "rebuild on temp copy + diff"),
        ("python _tools/_snapshot.py", "checkpoint + write _output/_vc_snapshot.json"),
        ("python _tools/_snapshot.py --check", "regression check vs last snapshot"),
        ("python _tools/_fixture_cache.py", "refresh _output/_fixture_cache.json"),
    ]
    for cmd, desc in cmds:
        print(f"  {cmd:<48} {desc}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    env_ok = check_environment()
    show_build_report()
    show_index_summary()
    show_lint_status()
    show_snapshot_status()
    show_quick_ref()
    print()
    if not env_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
