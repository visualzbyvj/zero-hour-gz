# -*- coding: utf-8 -*-
"""
Insert advanced show functions into Zero Hour GZ Project File.qxw:
  - Soft-fade chasers 1200-1212 (from sources 448-451,453-455,458-460,463-465)
  - PingPong chasers 1300-1311 (from 448-452,457-461,467-468)
  - Colour split Collections 1400-1414
  - Intensity pulse scenes 1500-1507, pair scenes 1516-1517
  - Chasers 1510-1515: run _patch_ring_chase.py after this script
  - BeatGenerator: normalized to configured mode (default Internal)
Idempotent: strips owned IDs then reinserts.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import (
    extract_function_block,
    inject_before_monitor,
    load_qxw,
    make_pp_chaser,
    make_soft_chaser,
    save_qxw,
    strip_functions,
)

SOFT_CHASERS = [
    (1200, 448),
    (1201, 449),
    (1202, 450),
    (1203, 451),
    (1204, 453),
    (1205, 454),
    (1206, 455),
    (1207, 458),
    (1208, 459),
    (1209, 460),
    (1210, 463),
    (1211, 464),
    (1212, 465),
]

PP_CHASERS = [
    (1300, 448),
    (1301, 449),
    (1302, 450),
    (1303, 451),
    (1304, 452),
    (1305, 457),
    (1306, 458),
    (1307, 459),
    (1308, 460),
    (1309, 461),
    (1310, 467),
    (1311, 468),
]

SPLIT_COLLECTIONS = [
    (1400, "SPLIT - RED/BLUE", 17, 20),
    (1401, "SPLIT - BLUE/RED", 18, 19),
    (1402, "SPLIT - GOLD/PURPLE", 119, 120),
    (1403, "SPLIT - PURPLE/GOLD", 114, 125),
    (1404, "SPLIT - CYAN/ORANGE", 115, 124),
    (1405, "SPLIT - ORANGE/CYAN", 118, 121),
    (1406, "SPLIT - GREEN/RED", 116, 19),
    (1407, "SPLIT - YELLOW/BLUE", 117, 20),
    (1408, "SPLIT - WHITE/RED", 1121, 19),
    (1409, "SPLIT - WHITE/BLUE", 1121, 20),
    (1410, "SPLIT - WHITE/PURPLE", 1121, 120),
    (1411, "SPLIT - WHITE/CYAN", 1121, 121),
    (1412, "SPLIT - GOLD/CYAN", 119, 121),
    (1413, "SPLIT - PURPLE/ORANGE", 114, 124),
    (1414, "SPLIT - GREEN/PURPLE", 116, 120),
]

INT_PULSE_SCENES = [
    (1500, "INT PULSE - Outer Front", 3),
    (1501, "INT PULSE - Outer Left", 4),
    (1502, "INT PULSE - Outer Back", 10),
    (1503, "INT PULSE - Outer Right", 19),
    (1504, "INT PULSE - Inner Front", 25),
    (1505, "INT PULSE - Inner Left", 5),
    (1506, "INT PULSE - Inner Back", 23),
    (1507, "INT PULSE - Inner Right", 20),
]


def ring_dimmer_only_fv() -> str:
    parts: list[int] = []
    for ch in range(24):
        parts.extend([ch, 255 if ch == 0 else 0])
    return ",".join(map(str, parts))


def build_split_collections() -> str:
    lines: list[str] = []
    for fid, name, a, b in SPLIT_COLLECTIONS:
        lines.append(f'  <Function ID="{fid}" Type="Collection" Name="{name}">')
        lines.append(f'   <Step Number="0">{a}</Step>')
        lines.append(f'   <Step Number="1">{b}</Step>')
        lines.append("  </Function>")
    return "\n".join(lines)


def build_intensity_scenes() -> str:
    fv = ring_dimmer_only_fv()
    blocks: list[str] = []
    for fid, name, fix in INT_PULSE_SCENES:
        blocks.append(f'  <Function ID="{fid}" Type="Scene" Name="{name}">')
        blocks.append('   <Speed FadeIn="0" FadeOut="0" Duration="0"/>')
        blocks.append(f'   <FixtureVal ID="{fix}">{fv}</FixtureVal>')
        blocks.append("  </Function>")
    blocks.append('  <Function ID="1516" Type="Scene" Name="INT PULSE - Outer Front+Back">')
    blocks.append('   <Speed FadeIn="0" FadeOut="0" Duration="0"/>')
    blocks.append(f'   <FixtureVal ID="3">{fv}</FixtureVal>')
    blocks.append(f'   <FixtureVal ID="10">{fv}</FixtureVal>')
    blocks.append("  </Function>")
    blocks.append('  <Function ID="1517" Type="Scene" Name="INT PULSE - Inner Front+Back">')
    blocks.append('   <Speed FadeIn="0" FadeOut="0" Duration="0"/>')
    blocks.append(f'   <FixtureVal ID="25">{fv}</FixtureVal>')
    blocks.append(f'   <FixtureVal ID="23">{fv}</FixtureVal>')
    blocks.append("  </Function>")
    return "\n".join(blocks)


DEFAULT_BEAT_TYPE = "Internal"


def patch_beat_generator(text: str, beat_type: str = DEFAULT_BEAT_TYPE) -> str:
    """Patch BeatGenerator mode while preserving current BPM value."""
    return re.sub(
        r'<BeatGenerator BeatType="[^"]+" BPM="(\d+)"/>',
        lambda m: f'<BeatGenerator BeatType="{beat_type}" BPM="{m.group(1)}"/>',
        text,
        count=1,
    )


def advanced_function_ids() -> set[int]:
    return set(
        list(range(1200, 1213))
        + list(range(1300, 1312))
        + list(range(1400, 1415))
        + list(range(1500, 1508))
        + [1516, 1517]
    )


def main() -> None:
    text = strip_functions(load_qxw(), advanced_function_ids())
    blocks: list[str] = []
    for new_id, src_id in SOFT_CHASERS:
        raw = extract_function_block(text, src_id)
        if "Type=\"Chaser\"" not in raw:
            raise SystemExit(f"Source {src_id} is not a Chaser (needed for SOFT).")
        blocks.append(make_soft_chaser(raw, new_id))

    for new_id, src_id in PP_CHASERS:
        raw = extract_function_block(text, src_id)
        if "Type=\"Chaser\"" not in raw:
            raise SystemExit(f"Source {src_id} is not a Chaser (needed for PP).")
        blocks.append(make_pp_chaser(raw, new_id))

    blocks.append(build_split_collections())
    blocks.append(build_intensity_scenes())

    text = inject_before_monitor(text, "\n" + "\n".join(blocks) + "\n")
    text = patch_beat_generator(text)
    save_qxw(text)
    print("OK: Advanced 1200-1414, scenes 1500-1507,1516-1517 + BeatGenerator patch (run _patch_ring_chase for 1510-1515)")


if __name__ == "__main__":
    main()
