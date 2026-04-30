# -*- coding: utf-8 -*-
"""Validate Zero Hour GZ .qxw: IDs, references, VC pages. Writes _LD_AUDIT.md."""
from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import QXW
from _widget_sizer import speed_dial_min_height

ROOT = Path(__file__).resolve().parent.parent
WS_NS = "http://www.qlcplus.org/Workspace"
NONE_FN = 4294967295

EXPECTED_VC_PAGES = (
    "BUSK",
    "DUBSTEP",
    "TRAP",
    "BASS HOUSE",
    "HARD TECHNO",
    "COLOR",
    "FX",
    "IMPACT",
    "ATMOSPHERE",
    "DIRECTOR",
)


def tag(local: str) -> str:
    return f"{{{WS_NS}}}{local}"


# Elements under VirtualConsole that carry widget IDs (exclude Preset, Function, etc.)
VC_WIDGET_TAGS = frozenset(
    {
        tag("Frame"),
        tag("Button"),
        tag("Slider"),
        tag("SpeedDial"),
        tag("SoloFrame"),
        tag("Label"),
        tag("CueList"),
        tag("XYPad"),
        tag("Clock"),
        tag("AudioTriggers"),
    }
)


def engine_functions(engine: ET.Element) -> list[ET.Element]:
    return [el for el in engine if el.tag == tag("Function") and el.get("Type") is not None]


def defined_function_ids(fns: list[ET.Element]) -> set[int]:
    s: set[int] = set()
    for fn in fns:
        i = fn.get("ID")
        if i and i.isdigit():
            s.add(int(i))
    return s


def fixture_id_list(engine: ET.Element) -> tuple[list[int], set[int]]:
    lst: list[int] = []
    for el in engine:
        if el.tag != tag("Fixture"):
            continue
        cid = el.find(tag("ID"))
        if cid is not None and (cid.text or "").strip().isdigit():
            lst.append(int(cid.text.strip()))
    return lst, set(lst)


def fixture_group_ids(engine: ET.Element) -> set[int]:
    s: set[int] = set()
    for el in engine:
        if el.tag != tag("FixtureGroup"):
            continue
        i = el.get("ID")
        if i and i.isdigit():
            s.add(int(i))
    return s


def iter_vc_function_refs(vc: ET.Element) -> list[int]:
    refs: list[int] = []
    for fn in vc.iter(tag("Function")):
        aid = fn.get("ID")
        if aid is not None and aid.isdigit():
            refs.append(int(aid))
            continue
        txt = (fn.text or "").strip()
        if txt.isdigit():
            refs.append(int(txt))
    return refs


def vc_widget_ids(vc: ET.Element) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for el in vc.iter():
        if el.tag not in VC_WIDGET_TAGS:
            continue
        wid = el.get("ID")
        if wid is None:
            continue
        local = el.tag.split("}")[-1] if "}" in el.tag else el.tag
        rows.append((local, wid))
    return rows


def check_chaser_collection_steps(
    fns: list[ET.Element], defined: set[int], errors: list[str]
) -> None:
    for fn in fns:
        typ = fn.get("Type") or ""
        if typ not in ("Chaser", "Collection", "Sequence"):
            continue
        fid = fn.get("ID", "?")
        name = (fn.get("Name") or "")[:60]
        for step in fn.findall(tag("Step")):
            txt = (step.text or "").strip()
            if not txt.isdigit():
                continue
            ref = int(txt)
            if ref == NONE_FN:
                continue
            if ref not in defined:
                errors.append(
                    f"Function {fid} ({typ}) {name!r} Step references missing ID {ref}"
                )


def check_scene_fixturevals(
    fns: list[ET.Element], fixtures: set[int], errors: list[str]
) -> None:
    for fn in fns:
        if fn.get("Type") != "Scene":
            continue
        fid = fn.get("ID", "?")
        for fv in fn.findall(tag("FixtureVal")):
            i = fv.get("ID")
            if not i or not i.isdigit():
                continue
            fx = int(i)
            if fx not in fixtures:
                errors.append(f"Scene {fid} FixtureVal references missing fixture ID {fx}")


def check_rgb_matrix_groups(
    fns: list[ET.Element], groups: set[int], errors: list[str]
) -> None:
    for fn in fns:
        if fn.get("Type") != "RGBMatrix":
            continue
        fid = fn.get("ID", "?")
        gel = fn.find(tag("FixtureGroup"))
        if gel is None or not (gel.text or "").strip().isdigit():
            continue
        gid = int(gel.text.strip())
        if gid not in groups:
            errors.append(f"RGBMatrix {fid} FixtureGroup {gid} not found")


def check_playback_slider_255(vc: ET.Element, warnings: list[str]) -> None:
    """Warn if a Playback slider with a Function reference has Value=255 (auto-starts on load)."""
    slider_tag = tag("Slider")
    for sl in vc.iter(slider_tag):
        mode_el = sl.find(tag("SliderMode"))
        if mode_el is None or (mode_el.text or "").strip() != "Playback":
            continue
        level_el = sl.find(tag("Level"))
        if level_el is None:
            continue
        val = level_el.get("Value", "")
        if val != "255":
            continue
        fn_el = sl.find(tag("Function"))
        if fn_el is None:
            continue  # no function reference; just an intensity fader at full
        fn_id = fn_el.get("ID", "?")
        if fn_id == "4294967295":
            continue  # sentinel: no function assigned
        cap = sl.get("Caption", "?")
        wid = sl.get("ID", "?")
        warnings.append(
            f"Playback Slider [{wid}] {cap!r} Value=255 with fn {fn_id} -- will auto-start on load"
        )


def check_speed_dial_duration_tempo(
    vc: ET.Element, fns: list[ET.Element], warnings: list[str]
) -> None:
    """Warn if a SpeedDial's child Function Duration is not 6 (SpeedMultiplier One = 1.0x)."""
    fn_tempo: dict[int, str] = {}
    for fn in fns:
        fid_s = fn.get("ID", "")
        if not fid_s.isdigit():
            continue
        speed_el = fn.find(tag("Speed"))
        if speed_el is not None:
            fn_tempo[int(fid_s)] = speed_el.get("TempoType", "")

    sd_tag = tag("SpeedDial")
    for sd in vc.iter(sd_tag):
        cap = sd.get("Caption", "?")
        wid = sd.get("ID", "?")
        for fn_el in sd.findall(tag("Function")):
            fid_s = fn_el.get("ID", "")
            dur_s = fn_el.get("Duration", "")
            if not fid_s.isdigit():
                continue
            fid = int(fid_s)
            dur = int(dur_s) if dur_s.isdigit() else -1
            tempo = fn_tempo.get(fid, "")
            if tempo == "Beats" and dur != 6:
                warnings.append(
                    f"SpeedDial [{wid}] {cap!r} links Beat chaser {fid} "
                    f"with Duration={dur} (expected 6=One/1.0x)"
                )


def check_beat_dial_multipliers(vc: ET.Element, warnings: list[str]) -> None:
    """Warn if a beat-mode SpeedDial has Multipliers (bitmask 128) hidden in its Visibility."""
    sd_tag = tag("SpeedDial")
    BEATS_BIT = 512
    MULT_BIT = 128
    for sd in vc.iter(sd_tag):
        vis_s = sd.get("Visibility", "")
        if not vis_s.isdigit():
            continue
        vis = int(vis_s)
        if not (vis & BEATS_BIT):
            continue  # not a beat-mode dial
        if not (vis & MULT_BIT):
            cap = sd.get("Caption", "?")
            wid = sd.get("ID", "?")
            warnings.append(
                f"SpeedDial [{wid}] {cap!r} is beat-mode (Visibility={vis}) but Multipliers bit (128) is off"
            )


def check_dead_functions(
    fns: list[ET.Element], vc: ET.Element | None, warnings: list[str]
) -> None:
    """Warn about functions not referenced by any VC widget, collection, or chaser."""
    defined_ids: set[int] = set()
    for fn in fns:
        fid_s = fn.get("ID", "")
        if fid_s.isdigit():
            defined_ids.add(int(fid_s))

    referenced: set[int] = set()

    # References from other functions (steps, members)
    for fn in fns:
        for step in fn.findall(tag("Step")):
            ref = (step.text or "").strip()
            if ref.isdigit():
                referenced.add(int(ref))
        # Collection steps have FunctionID attr
        for step in fn.findall(tag("Step")):
            r2 = step.get("FunctionID", "")
            if r2.isdigit():
                referenced.add(int(r2))

    # References from VC
    if vc is not None:
        for fn_el in vc.iter(tag("Function")):
            aid = fn_el.get("ID", "")
            if aid.isdigit():
                referenced.add(int(aid))
            txt = (fn_el.text or "").strip()
            if txt.isdigit():
                referenced.add(int(txt))

    dead = sorted(defined_ids - referenced)
    if dead:
        sample = dead[:20]
        warnings.append(
            f"Dead/orphan functions (not in any VC, collection, or chaser) count={len(dead)}: "
            f"{sample}{'...' if len(dead) > 20 else ''}"
        )


def check_widget_heights(vc: ET.Element, warnings: list[str]) -> None:
    """Warn if a SpeedDial is too short for its Visibility flags (using _widget_sizer)."""
    sd_tag = tag("SpeedDial")
    BEATS_BIT = 512
    for sd in vc.iter(sd_tag):
        h_s = sd.get("Height", "")
        vis_s = sd.get("Visibility", "")
        if not h_s.isdigit() or not vis_s.isdigit():
            continue
        h = int(h_s)
        vis = int(vis_s)
        beat_mode = bool(vis & BEATS_BIT)
        min_h = speed_dial_min_height(beat_mode=beat_mode)
        if h < min_h:
            cap = sd.get("Caption", "?")
            wid = sd.get("ID", "?")
            warnings.append(
                f"SpeedDial [{wid}] {cap!r} Height={h} < min {min_h} "
                f"for beat_mode={beat_mode} (Visibility={vis})"
            )


def run_lint(*, strict: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    tree = ET.parse(QXW)
    root = tree.getroot()
    eng = root.find(f"./{tag('Engine')}")
    if eng is None:
        return ["No <Engine> in workspace"], []

    fns = engine_functions(eng)
    defined = defined_function_ids(fns)
    id_list = [int(fn.get("ID")) for fn in fns if fn.get("ID", "").isdigit()]
    dup_fn = sorted(k for k, v in Counter(id_list).items() if v > 1)
    if dup_fn:
        msg = (
            f"Duplicate engine Function IDs in <Engine> ({len(dup_fn)}); "
            f"QLC+ may use the last definition; sample: {dup_fn[:12]}"
        )
        (errors if strict else warnings).append(msg)

    fx_id_list, fixtures = fixture_id_list(eng)
    dup_fx = sorted(k for k, v in Counter(fx_id_list).items() if v > 1)
    if dup_fx:
        msg = f"Duplicate patched fixture IDs ({len(dup_fx)}): {dup_fx[:12]}"
        (errors if strict else warnings).append(msg)

    groups = fixture_group_ids(eng)

    check_chaser_collection_steps(fns, defined, errors)
    check_scene_fixturevals(fns, fixtures, errors)
    check_rgb_matrix_groups(fns, groups, errors)

    vc = root.find(f"./{tag('VirtualConsole')}")
    if vc is None:
        warnings.append("No <VirtualConsole> block")
    else:
        wids = vc_widget_ids(vc)
        id_only = [w for _, w in wids if w.isdigit()]
        dup_w = [k for k, v in Counter(id_only).items() if v > 1]
        for k in sorted(dup_w, key=int):
            owners = [f"{a}:{b}" for a, b in wids if b == k][:5]
            errors.append(f"Duplicate VC widget ID {k} ({', '.join(owners)})")

        missing_vc: list[int] = []
        for ref in iter_vc_function_refs(vc):
            if ref == NONE_FN:
                continue
            if ref not in defined:
                missing_vc.append(ref)
        if missing_vc:
            uniq = sorted(set(missing_vc))
            msg = (
                f"VC references missing Function IDs ({len(uniq)}): {uniq[:20]}"
                f"{'...' if len(uniq) > 20 else ''}"
            )
            (errors if strict else warnings).append(msg)

        vc_raw = ET.tostring(vc, encoding="unicode")
        for cap in EXPECTED_VC_PAGES:
            if cap not in vc_raw:
                errors.append(f"LD audit: expected VC page caption {cap!r} not found")

        # Additional LD checks
        check_playback_slider_255(vc, warnings)
        check_speed_dial_duration_tempo(vc, fns, warnings)
        check_beat_dial_multipliers(vc, warnings)
        check_widget_heights(vc, warnings)

    # Dead function check (needs both engine and VC)
    check_dead_functions(fns, vc if vc is not None else None, warnings)

    return errors, warnings


def run_fix() -> None:
    """Auto-fix: deduplicate engine functions."""
    from _dedup_engine import dedup
    from _qlc_helpers import auto_backup, load_qxw, save_qxw

    text = load_qxw()
    new_text, total, removed = dedup(text)
    if removed == 0:
        print("[fix] No duplicate functions to remove.")
        return
    backup = auto_backup()
    save_qxw(new_text)
    print(f"[fix] Removed {removed} duplicate Function blocks (backed up to {backup.name})")


def main() -> None:
    ap = argparse.ArgumentParser(description="Lint QLC+ workspace XML")
    ap.add_argument("--quiet", action="store_true", help="Only write _LD_AUDIT.md, minimal stdout")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Treat duplicate engine functions / missing VC refs as errors (default: warn)",
    )
    ap.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix issues (dedup engine functions) before linting",
    )
    args = ap.parse_args()

    if args.fix:
        run_fix()

    errors, warnings = run_lint(strict=args.strict)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# LD / showfile audit",
        "",
        f"_Generated: {stamp}_",
        "",
        "## Virtual Console pages (expected)",
        "",
        "\n".join(f"- {p}" for p in EXPECTED_VC_PAGES),
        "",
        "## Result",
        "",
    ]
    if errors:
        lines.append("**Status: FAIL**")
        lines.extend(["", "### Errors", ""] + [f"- {e}" for e in errors])
    else:
        lines.append("**Status: OK** (no blocking errors)")
    if warnings:
        lines.extend(["", "### Warnings", ""] + [f"- {w}" for w in warnings])

    (ROOT / "_docs" / "_LD_AUDIT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if not args.quiet:
        print("Wrote _LD_AUDIT.md")
        for w in warnings:
            print("WARN", w)
        for e in errors:
            print("ERR ", e)
        if errors:
            raise SystemExit(1)
        print("Lint OK.")
    elif errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
