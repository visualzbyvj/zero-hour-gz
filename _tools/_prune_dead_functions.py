# -*- coding: utf-8 -*-
"""Remove unreferenced Engine functions from the showfile.

Reachability roots:
- Functions referenced by Virtual Console widgets

Reachability propagation:
- Chaser / Collection / Sequence Step references

This keeps all functions needed by VC-triggerable stacks while removing
legacy debris that is never reachable in live operation.
"""
from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import QXW, auto_backup, load_qxw, save_qxw, strip_functions

WS_NS = "http://www.qlcplus.org/Workspace"
NONE_FN = 4294967295
KEEP_FUNCTION_IDS = {
    208, 217, 226, 235,
    428, 429, 430,
    448, 449, 450, 451, 452, 453, 454, 455,
    457, 458, 459, 460, 461, 463, 464, 465,
    467, 468,
}


def tag(local: str) -> str:
    return f"{{{WS_NS}}}{local}"


def _extract_step_refs(fn_el: ET.Element) -> set[int]:
    refs: set[int] = set()
    for step in fn_el.findall(tag("Step")):
        txt = (step.text or "").strip()
        if txt.isdigit():
            refs.add(int(txt))
        fn_id_attr = step.get("FunctionID", "")
        if fn_id_attr.isdigit():
            refs.add(int(fn_id_attr))
    return refs


def _extract_vc_roots(vc: ET.Element) -> set[int]:
    roots: set[int] = set()
    for fn_el in vc.iter(tag("Function")):
        aid = fn_el.get("ID", "")
        if aid.isdigit():
            roots.add(int(aid))
        txt = (fn_el.text or "").strip()
        if txt.isdigit():
            roots.add(int(txt))
    roots.discard(NONE_FN)
    return roots


def compute_reachable(functions: dict[int, ET.Element], vc_roots: set[int]) -> set[int]:
    reachable: set[int] = set()
    stack = [fid for fid in vc_roots if fid in functions]
    while stack:
        fid = stack.pop()
        if fid in reachable:
            continue
        reachable.add(fid)
        fn_el = functions.get(fid)
        if fn_el is None:
            continue
        fn_type = fn_el.get("Type", "")
        if fn_type in {"Chaser", "Collection", "Sequence"}:
            for child_id in _extract_step_refs(fn_el):
                if child_id in functions and child_id not in reachable:
                    stack.append(child_id)
    return reachable


def prune_dead_functions(*, dry_run: bool = False, backup: bool = True) -> tuple[int, int]:
    tree = ET.parse(QXW)
    root = tree.getroot()
    engine = root.find(f"./{tag('Engine')}")
    if engine is None:
        raise SystemExit("No <Engine> found in workspace.")
    vc = root.find(f"./{tag('VirtualConsole')}")
    if vc is None:
        raise SystemExit("No <VirtualConsole> found in workspace.")

    fn_elements = [el for el in engine if el.tag == tag("Function") and (el.get("ID") or "").isdigit()]
    functions = {int(el.get("ID")): el for el in fn_elements}
    total = len(functions)

    roots = _extract_vc_roots(vc)
    reachable = compute_reachable(functions, roots)
    dead_ids = sorted(set(functions) - reachable - KEEP_FUNCTION_IDS)

    if dry_run:
        print(f"Functions total: {total}")
        print(f"Reachable:       {len(reachable)}")
        print(f"Dead:            {len(dead_ids)}")
        if dead_ids:
            print(f"Dead sample:     {dead_ids[:30]}")
        return total, len(dead_ids)

    if not dead_ids:
        print("No dead functions found.")
        return total, 0

    if backup:
        b = auto_backup(QXW)
        print(f"Backup: {b}")

    text = load_qxw(QXW)
    text = strip_functions(text, set(dead_ids))
    save_qxw(text, QXW)
    print(f"Removed dead functions: {len(dead_ids)} ({total} -> {total - len(dead_ids)})")
    return total, len(dead_ids)


def main() -> None:
    ap = argparse.ArgumentParser(description="Prune unreferenced QLC+ engine functions")
    ap.add_argument("--dry-run", action="store_true", help="Report only; do not modify showfile")
    ap.add_argument("--no-backup", action="store_true", help="Skip backup creation")
    args = ap.parse_args()
    prune_dead_functions(dry_run=args.dry_run, backup=not args.no_backup)


if __name__ == "__main__":
    main()
