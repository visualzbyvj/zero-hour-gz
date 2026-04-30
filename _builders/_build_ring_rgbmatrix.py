# -*- coding: utf-8 -*-
from pathlib import Path
import sys
from xml.sax.saxutils import escape as xml_escape
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _qlc_helpers import (
    fixture_group_id_by_name,
    inject_before_monitor,
    load_qxw,
    save_qxw,
    strip_functions,
)
OUTER_BASE, INNER_BASE, WHITE_BASE = 3700, 3715, 3730
WHITE = "4294967295"
def _props_xml(props):
    return "".join(f'\n   <Property Name="{xml_escape(k)}" Value="{xml_escape(v)}"/>' for k, v in props)
def rgb_matrix_fn(fid, name, group_id, algo, duration, run_order, direction="Forward", extra_props=None):
    safe = xml_escape(name, {"'": "&apos;", '"': "&quot;"})
    props = extra_props or []
    return (f'  <Function ID="{fid}" Type="RGBMatrix" Name="{safe}">\n'
        f"   <Tempo>Beats</Tempo>\n"
        f'   <Speed FadeIn="0" FadeOut="0" Duration="{duration}"/>\n'
        f"   <Direction>{direction}</Direction>\n"
        f"   <RunOrder>{run_order}</RunOrder>\n"
        f'   <Algorithm Type="Script">{xml_escape(algo)}</Algorithm>\n'
        f'   <Color Index="0">{WHITE}</Color>\n'
        f"   <ControlMode>RGB</ControlMode>\n"
        f"   <FixtureGroup>{group_id}</FixtureGroup>"
        f"{_props_xml(props)}\n"
        f"  </Function>")
RING_SPECS = [
    ("WAVE CW", "Waves", 400, "Loop", "Forward", [("direction", "Right"), ("orientation", "Horizontal"), ("tailfade", "Yes")]),
    ("WAVE CCW", "Waves", 400, "Loop", "Forward", [("direction", "Left"), ("orientation", "Horizontal"), ("tailfade", "Yes")]),
    ("WAVE BNCE", "Waves", 400, "PingPong", "Forward", [("direction", "Right"), ("orientation", "Horizontal"), ("tailfade", "Yes")]),
    ("FILL", "Fill", 200, "Loop", "Backward", [("orientation", "Horizontal")]),
    ("FILL+DRAIN", "Fill Unfill", 200, "Loop", "Backward", [("orientation", "Horizontal")]),
    ("FILL CENTER", "Fill From Center", 400, "PingPong", "Backward", [("orientation", "Horizontal")]),
    ("EVEN/ODD", "Even/Odd", 200, "Loop", "Forward", []),
    ("MARQUEE", "Marquee", 300, "Loop", "Backward", []),
    ("GRADIENT", "Gradient", 800, "PingPong", "Forward", [("orientation", "Horizontal"), ("presetIndex", "Rainbow")]),
    ("PLASMA", "Plasma", 400, "Loop", "Forward", [("presetIndex", "Rainbow")]),
    ("SINE WAVE", "Sine Wave", 600, "Loop", "Backward", []),
    ("NOISE", "Noise", 200, "Loop", "Forward", []),
    ("SPARKLE", "Random Single", 80, "Loop", "Forward", []),
    ("RAND FILL", "Random Fill Single", 100, "Loop", "Forward", []),
    ("FIREWORKS", "Fireworks", 200, "Loop", "Forward", []),
]
WHITE_SPECS = [
    ("W WAVE", "Waves", 400, "Loop", "Forward", [("direction", "Right"), ("orientation", "Horizontal"), ("tailfade", "Yes")]),
    ("W FILL", "Fill Unfill", 200, "Loop", "Backward", [("orientation", "Horizontal")]),
    ("W MARQUEE", "Marquee", 300, "Loop", "Backward", []),
    ("W SPARKLE", "Random Single", 80, "Loop", "Forward", []),
    ("W EVEN/ODD", "Even/Odd", 200, "Loop", "Forward", []),
]
def build_all():
    outer_g = fixture_group_id_by_name("OUTER RING - FULL")
    inner_g = fixture_group_id_by_name("INNER RING - FULL")
    white_g = fixture_group_id_by_name("WHITE RING - FULL")
    parts = []
    for i, spec in enumerate(RING_SPECS):
        suffix, algo, dur, ro, direction, props = spec
        parts.append(rgb_matrix_fn(OUTER_BASE + i, f"RING MX OUT - {suffix}", outer_g, algo, dur, ro, direction=direction, extra_props=props))
        parts.append(rgb_matrix_fn(INNER_BASE + i, f"RING MX IN - {suffix}", inner_g, algo, dur, ro, direction=direction, extra_props=props))
    for i, spec in enumerate(WHITE_SPECS):
        suffix, algo, dur, ro, direction, props = spec
        parts.append(rgb_matrix_fn(WHITE_BASE + i, f"RING MX WHT - {suffix}", white_g, algo, dur, ro, direction=direction, extra_props=props))
    return "\n".join(parts) + "\n"
OWNED_IDS = set(range(OUTER_BASE, OUTER_BASE + 15)) | set(range(INNER_BASE, INNER_BASE + 15)) | set(range(WHITE_BASE, WHITE_BASE + 5))
def main():
    text = load_qxw()
    text = strip_functions(text, OWNED_IDS)
    text = inject_before_monitor(text, build_all())
    save_qxw(text)
    print("OK: Ring RGBMatrix", len(OWNED_IDS), "functions injected")
if __name__ == "__main__":
    main()