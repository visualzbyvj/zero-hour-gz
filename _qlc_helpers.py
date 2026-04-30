# -*- coding: utf-8 -*-
"""Shared QLC+ .qxw XML helpers for Zero Hour GZ build scripts."""
from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape as xml_escape

QXW = Path(__file__).resolve().parent / "Zero Hour GZ Project File.qxw"
BACKUP_DIR = Path(__file__).resolve().parent / "_Showfile_Backups"
WS_NS = "http://www.qlcplus.org/Workspace"

# Physical order: Front, Left, Back, Right
OUTER_BARS = (3, 4, 10, 19)
INNER_BARS = (25, 5, 23, 20)
WHITE_BARS = (15, 16, 18, 21)
# CW sweep order: Front, Right, Back, Left
OUTER_CW = (3, 19, 10, 4)
INNER_CW = (25, 20, 23, 5)
WHITE_CW = (15, 21, 18, 16)

FX_4CELL = (1, 6, 14, 17)
FX_COB = (2, 11, 28, 29)
FX_A55 = (0, 7, 26, 27)
FX_PANEL = (8, 9, 22, 24)
COB_FRONT = (2, 11)
COB_BACK = (28, 29)
A55_FRONT = (0, 7)
A55_BACK = (26, 27)
BLINDER_FRONT = (1, 6)
BLINDER_BACK = (14, 17)

RGB_SEGS = 8
WHITE_SEGS = 16
SEG_REVERSED = (False, False, True, True)

COLORS: dict[str, dict[str, object]] = {
    "RED": {"rgb": (255, 0, 0), "argb": "4294901760"},
    "ORANGE": {"rgb": (255, 70, 0), "argb": "4294944000"},
    "YELLOW": {"rgb": (255, 255, 0), "argb": "4294967040"},
    "GREEN": {"rgb": (0, 255, 0), "argb": "4278255360"},
    "CYAN": {"rgb": (0, 220, 255), "argb": "4289374890"},
    "BLUE": {"rgb": (0, 0, 255), "argb": "4278190335"},
    "PURPLE": {"rgb": (130, 0, 220), "argb": "4286578816"},
    "GOLD": {"rgb": (255, 170, 0), "argb": "4294954700"},
}

SWEEP_COLORS: list[tuple[str, tuple[int, int, int]]] = [
    (k, COLORS[k]["rgb"])  # type: ignore[index]
    for k in ("RED", "ORANGE", "YELLOW", "GREEN", "CYAN", "BLUE", "PURPLE", "GOLD")
]


def fv_str(ch_vals: list[tuple[int, int]]) -> str:
    pairs: list[int] = []
    for ch, val in ch_vals:
        pairs.extend([ch, val])
    return ",".join(str(x) for x in pairs)


def fv_rgb_colored(num_segs: int, active_segs: set[int], rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    pairs: list[int] = []
    for seg in range(num_segs):
        base = seg * 3
        if seg in active_segs:
            pairs.extend([base, r, base + 1, g, base + 2, b])
        else:
            pairs.extend([base, 0, base + 1, 0, base + 2, 0])
    return ",".join(str(x) for x in pairs)


def fv_rgb(num_segs: int, active_segs: set[int]) -> str:
    return fv_rgb_colored(num_segs, active_segs, (255, 255, 255))


def fv_rgb_black(num_segs: int) -> str:
    return fv_rgb_colored(num_segs, set(), (0, 0, 0))


def fv_white(num_segs: int, active_segs: set[int]) -> str:
    pairs: list[int] = []
    for seg in range(num_segs):
        pairs.extend([seg, 255 if seg in active_segs else 0])
    return ",".join(str(x) for x in pairs)


def fv_white_black(num_segs: int) -> str:
    return fv_white(num_segs, set())


def panel_led_matrix_rgb(rgb: tuple[int, int, int], *, dim: int = 0) -> str:
    """154ch LED panel: dim+strobe +48 RGB pixels + 8 white (zeroed).

    dim defaults to 0 so intensity faders have sole control of Master Dimmer.
    Pass dim=255 only for safety overrides (PANIC).
    """
    r, g, b = rgb
    pairs: list[tuple[int, int]] = [(0, dim), (1, 0)]
    ch = 2
    for _ in range(48):
        pairs.extend([(ch, r), (ch + 1, g), (ch + 2, b)])
        ch += 3
    for c in range(146, 154):
        pairs.append((c, 0))
    return fv_str(pairs)


def scene_xml(fid: int, name: str, fixture_vals: list[tuple[int, str]]) -> str:
    safe = xml_escape(name, {"'": "&apos;", '"': "&quot;"})
    lines = [f'  <Function ID="{fid}" Type="Scene" Name="{safe}">']
    lines.append('   <Speed FadeIn="0" FadeOut="0" Duration="0"/>')
    for fx_id, fv in fixture_vals:
        lines.append(f'   <FixtureVal ID="{fx_id}">{fv}</FixtureVal>')
    lines.append("  </Function>")
    return "\n".join(lines)


def scene_xml_minimal(fid: int, name: str) -> str:
    """Scene with no FixtureVal (for STROBE KILL no-op)."""
    safe = xml_escape(name, {"'": "&apos;", '"': "&quot;"})
    return (
        f'  <Function ID="{fid}" Type="Scene" Name="{safe}">\n'
        '   <Speed FadeIn="0" FadeOut="0" Duration="0"/>\n'
        "  </Function>"
    )


def chaser_xml(
    fid: int,
    name: str,
    step_ids: list[int],
    run_order: str = "Loop",
    dur: int = 150,
    *,
    tempo: str = "Beats",
    sm_fi: str = "PerStep",
    sm_fo: str = "Default",
    sm_dur: str = "Common",
    step_fade_in: int | list[int] = 0,
    step_fade_out: int | list[int] = 0,
    step_hold: int | list[int] | None = None,
) -> str:
    n = len(step_ids)
    if isinstance(step_fade_in, list) and len(step_fade_in) != n:
        raise ValueError(f"chaser_xml: step_fade_in length {len(step_fade_in)} != {n} steps")
    if isinstance(step_fade_out, list) and len(step_fade_out) != n:
        raise ValueError(f"chaser_xml: step_fade_out length {len(step_fade_out)} != {n} steps")
    if isinstance(step_hold, list) and len(step_hold) != n:
        raise ValueError(f"chaser_xml: step_hold length {len(step_hold)} != {n} steps")
    safe = xml_escape(name, {"'": "&apos;", '"': "&quot;"})
    lines = [
        f'  <Function ID="{fid}" Type="Chaser" Name="{safe}">',
        f"   <Tempo>{tempo}</Tempo>",
        f'   <Speed FadeIn="0" FadeOut="0" Duration="{dur}"/>',
        "   <Direction>Forward</Direction>",
        f"   <RunOrder>{run_order}</RunOrder>",
        f'   <SpeedModes FadeIn="{sm_fi}" FadeOut="{sm_fo}" Duration="{sm_dur}"/>',
    ]
    holds = step_hold if step_hold is not None else dur
    for i, sid in enumerate(step_ids):
        fi = step_fade_in[i] if isinstance(step_fade_in, list) else step_fade_in
        fo = step_fade_out[i] if isinstance(step_fade_out, list) else step_fade_out
        h = holds[i] if isinstance(holds, list) else holds
        lines.append(
            f'   <Step Number="{i}" FadeIn="{fi}" Hold="{h}" FadeOut="{fo}">{sid}</Step>'
        )
    lines.append("  </Function>")
    return "\n".join(lines)


def collection_xml(fid: int, name: str, steps: list[int]) -> str:
    safe = xml_escape(name, {"'": "&apos;", '"': "&quot;"})
    lines = [f'  <Function ID="{fid}" Type="Collection" Name="{safe}">']
    for i, sid in enumerate(steps):
        lines.append(f'   <Step Number="{i}">{sid}</Step>')
    lines.append("  </Function>")
    return "\n".join(lines)


def strip_functions(text: str, ids: set[int]) -> str:
    if not ids:
        return text
    alt = "|".join(str(i) for i in sorted(ids))
    pat = rf'\s*<Function ID="({alt})" Type="[^"]*"[^>]*>.*?</Function>\s*'
    return re.sub(pat, "", text, flags=re.DOTALL)


def inject_before_monitor(text: str, xml_block: str) -> str:
    marker = "<Monitor "
    try:
        idx = text.index(marker)
    except ValueError as e:
        raise ValueError(
            f"inject_before_monitor: marker {marker!r} not found — is this a valid .qxw?"
        ) from e
    block = xml_block if xml_block.endswith("\n") else xml_block + "\n"
    return text[:idx] + block + "  " + text[idx:]


def _clone_chaser_block(
    block: str,
    new_id: int,
    suffix: str,
    *,
    soft_fades: bool,
    pingpong: bool,
) -> str:
    b = re.sub(
        r'^\s*<Function ID="\d+"',
        f'  <Function ID="{new_id}"',
        block,
        count=1,
        flags=re.MULTILINE,
    )

    def name_repl(m: re.Match[str]) -> str:
        return f'Name="{m.group(1)}{suffix}"'

    b = re.sub(r'Name="([^"]*)"', name_repl, b, count=1)
    if soft_fades:

        def speed_repl(m: re.Match[str]) -> str:
            dur = int(m.group(1))
            fi = min(dur // 2, 429)
            return f'<Speed FadeIn="{fi}" FadeOut="{fi}" Duration="{dur}"/>'

        b = re.sub(r'<Speed FadeIn="\d+" FadeOut="\d+" Duration="(\d+)"/>', speed_repl, b)

        def step_repl(m: re.Match[str]) -> str:
            n, hold, fn = m.groups()
            hold_i = int(hold)
            fade = min(max(hold_i // 2, 1), 429)
            return f'<Step Number="{n}" FadeIn="{fade}" Hold="{hold}" FadeOut="{fade}">{fn}</Step>'

        b = re.sub(
            r'<Step Number="(\d+)" FadeIn="\d+" Hold="(\d+)" FadeOut="\d+">(\d+)</Step>',
            step_repl,
            b,
        )
    if pingpong:
        b = re.sub(r"<RunOrder>Loop</RunOrder>", "<RunOrder>PingPong</RunOrder>", b)
    return b


def make_soft_chaser(block: str, new_id: int, suffix: str = " - SOFT") -> str:
    """Clone a Chaser XML block with per-step fades ~ half of hold (ring FX soft variants)."""
    return _clone_chaser_block(block, new_id, suffix, soft_fades=True, pingpong=False)


def make_pp_chaser(block: str, new_id: int, suffix: str = " - PP") -> str:
    """Clone a Chaser as PingPong (from advanced busk tooling)."""
    return _clone_chaser_block(block, new_id, suffix, soft_fades=False, pingpong=True)


def strobe_chaser_xml(
    fid: int,
    name: str,
    steps: list[int],
    dur: int,
    run_order: str = "Loop",
) -> str:
    """Hardware-style strobe chaser (Tempo=Time, common step timing)."""
    safe = xml_escape(name, {"'": "&apos;", '"': "&quot;"})
    lines = [
        f'  <Function ID="{fid}" Type="Chaser" Name="{safe}">',
        "   <Tempo>Time</Tempo>",
        f'   <Speed FadeIn="0" FadeOut="0" Duration="{dur}"/>',
        "   <Direction>Forward</Direction>",
        f"   <RunOrder>{run_order}</RunOrder>",
        '   <SpeedModes FadeIn="Default" FadeOut="Default" Duration="Common"/>',
    ]
    for i, step_fn in enumerate(steps):
        lines.append(
            f'   <Step Number="{i}" FadeIn="0" Hold="{dur}" FadeOut="0">{step_fn}</Step>'
        )
    lines.append("  </Function>")
    return "\n".join(lines)


def extract_function_block(text: str, fid: int) -> str:
    pat = rf'\s*<Function ID="{fid}" Type="[^"]*"[^>]*>.*?</Function>\s*'
    m = re.search(pat, text, re.DOTALL)
    if not m:
        raise ValueError(f"Function {fid} not found in .qxw")
    return m.group(0)


def load_qxw(path: Path = QXW) -> str:
    return path.read_text(encoding="utf-8")


def save_qxw(text: str, path: Path = QXW) -> None:
    path.write_text(text, encoding="utf-8")


def auto_backup(path: Path = QXW) -> Path:
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = BACKUP_DIR / f"{path.stem}.{ts}.qxw"
    shutil.copy2(path, dest)
    return dest


def fixture_group_id_by_name(group_name: str, *, path: Path = QXW) -> int:
    """Resolve a FixtureGroup ID by exact Name in the current showfile."""
    tree = ET.parse(path)
    root = tree.getroot()
    grp_tag = f"{{{WS_NS}}}FixtureGroup"
    name_tag = f"{{{WS_NS}}}Name"
    target = group_name.strip().casefold()
    for grp in root.findall(f".//{grp_tag}"):
        name_attr = (grp.get("Name") or "").strip()
        name_el = grp.find(name_tag)
        name_text = ((name_el.text if name_el is not None else "") or "").strip()
        if name_attr.casefold() == target or name_text.casefold() == target:
            gid = grp.get("ID")
            if gid and gid.isdigit():
                return int(gid)
    raise ValueError(f"FixtureGroup named {group_name!r} not found in {path.name}")


def fixture_ids_by_group_name(group_name: str, *, path: Path = QXW) -> tuple[int, ...]:
    """Resolve unique fixture IDs (Head X) contained in a FixtureGroup by Name."""
    tree = ET.parse(path)
    root = tree.getroot()
    grp_tag = f"{{{WS_NS}}}FixtureGroup"
    name_tag = f"{{{WS_NS}}}Name"
    head_tag = f"{{{WS_NS}}}Head"
    target = group_name.strip().casefold()

    for grp in root.findall(f".//{grp_tag}"):
        name_attr = (grp.get("Name") or "").strip()
        name_el = grp.find(name_tag)
        name_text = ((name_el.text if name_el is not None else "") or "").strip()
        if name_attr.casefold() != target and name_text.casefold() != target:
            continue

        seen: set[int] = set()
        ordered: list[int] = []
        for head in grp.findall(head_tag):
            fixture_attr = head.get("Fixture", "")
            if not fixture_attr.isdigit():
                continue
            fx_id = int(fixture_attr)
            if fx_id in seen:
                continue
            seen.add(fx_id)
            ordered.append(fx_id)
        if ordered:
            return tuple(ordered)
        raise ValueError(f"FixtureGroup {group_name!r} found but has no valid heads in {path.name}")

    raise ValueError(f"FixtureGroup named {group_name!r} not found in {path.name}")
