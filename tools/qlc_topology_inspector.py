#!/usr/bin/env python3
"""
QLC+ Topology Inspector Prototype

Purpose:
    Read a QLC+ workspace (.qxw) and optional fixture profile directory (.qxf)
    and generate a topology report showing how fixtures, fixture groups, heads,
    matrix X/Y positions, universes, and DMX addresses relate.

Why this exists:
    This is the safe prototype for the future QLC+ fork topology debug overlay.
    It does not modify showfiles, fixture profiles, MIDI mappings, Art-Net settings,
    or live output behavior.

Usage:
    python tools/qlc_topology_inspector.py --workspace path/to/show.qxw --out reports/topology.md
    python tools/qlc_topology_inspector.py --workspace path/to/show.qxw --fixtures-dir fixtures/qxf --out reports/topology.md --json reports/topology.json

Notes:
    QLC+ XML can vary by version and file source. This parser is intentionally
    namespace tolerant and defensive. Unknown structures are reported instead of guessed.
"""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass
class FixtureModeInfo:
    manufacturer: str = ""
    model: str = ""
    mode: str = ""
    channel_count: Optional[int] = None
    head_count: Optional[int] = None
    heads: Dict[int, List[int]] = field(default_factory=dict)
    rgb_channels_by_head: Dict[int, List[int]] = field(default_factory=dict)
    dimmer_channels_by_head: Dict[int, List[int]] = field(default_factory=dict)
    shutter_channels_by_head: Dict[int, List[int]] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)


@dataclass
class FixtureInstance:
    fixture_id: str
    name: str = ""
    manufacturer: str = ""
    model: str = ""
    mode: str = ""
    universe: Optional[int] = None
    address: Optional[int] = None
    channels: Optional[int] = None
    raw: Dict[str, str] = field(default_factory=dict)


@dataclass
class FixtureGroupHead:
    group_name: str
    group_id: str
    x: Optional[int]
    y: Optional[int]
    fixture_id: str
    head_index: Optional[int]


@dataclass
class MatrixFunction:
    function_id: str
    name: str
    fixture_group: str = ""
    algorithm: str = ""
    width: Optional[int] = None
    height: Optional[int] = None
    raw: Dict[str, str] = field(default_factory=dict)


@dataclass
class TopologyCell:
    group_name: str
    group_id: str
    x: Optional[int]
    y: Optional[int]
    fixture_id: str
    fixture_name: str
    manufacturer: str
    model: str
    mode: str
    universe: Optional[int]
    address_zero_based: Optional[int]
    address_one_based: Optional[int]
    channel_range_one_based: str
    head_index: Optional[int]
    head_channels: List[int]
    rgb_channels: List[int]
    dimmer_channels: List[int]
    shutter_channels: List[int]
    warnings: List[str] = field(default_factory=list)


@dataclass
class TopologyReport:
    workspace: str
    fixtures_dir: Optional[str]
    fixtures: List[FixtureInstance]
    fixture_groups: List[FixtureGroupHead]
    matrices: List[MatrixFunction]
    cells: List[TopologyCell]
    warnings: List[str]


# -----------------------------
# XML helpers
# -----------------------------


def local_name(tag: str) -> str:
    """Strip XML namespace from a tag name."""
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def children_named(node: ET.Element, name: str) -> List[ET.Element]:
    return [child for child in list(node) if local_name(child.tag) == name]


def first_child_text(node: ET.Element, names: Iterable[str], default: str = "") -> str:
    wanted = set(names)
    for child in list(node):
        if local_name(child.tag) in wanted:
            return (child.text or "").strip()
    return default


def attr_any(node: ET.Element, names: Iterable[str], default: str = "") -> str:
    wanted = set(names)
    for key, value in node.attrib.items():
        if local_name(key) in wanted:
            return value
    return default


def safe_int(value: object) -> Optional[int]:
    if value is None:
        return None
    text = str(value).strip()
    if text == "":
        return None
    try:
        return int(text)
    except ValueError:
        return None


def iter_nodes(root: ET.Element, name: str) -> Iterable[ET.Element]:
    for node in root.iter():
        if local_name(node.tag) == name:
            yield node


def parse_xml(path: Path) -> ET.Element:
    try:
        return ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise SystemExit(f"XML parse error in {path}: {exc}") from exc


# -----------------------------
# Workspace parsing
# -----------------------------


def parse_fixtures(root: ET.Element) -> Dict[str, FixtureInstance]:
    fixtures: Dict[str, FixtureInstance] = {}

    for node in iter_nodes(root, "Fixture"):
        fixture_id = attr_any(node, ["ID", "Id", "id"])
        if not fixture_id:
            continue

        name = attr_any(node, ["Name"]) or first_child_text(node, ["Name"])
        universe = safe_int(attr_any(node, ["Universe"]) or first_child_text(node, ["Universe"]))
        address = safe_int(attr_any(node, ["Address"]) or first_child_text(node, ["Address"]))
        channels = safe_int(attr_any(node, ["Channels"]) or first_child_text(node, ["Channels"]))

        manufacturer = first_child_text(node, ["Manufacturer", "Creator"], "")
        model = first_child_text(node, ["Model"], "")
        mode = first_child_text(node, ["Mode"], "")

        # QLC+ workspaces commonly store manufacturer/model/mode as child tags,
        # but keep all simple child text so unusual versions are still visible.
        raw: Dict[str, str] = {}
        for child in list(node):
            text = (child.text or "").strip()
            if text:
                raw[local_name(child.tag)] = text

        fixtures[fixture_id] = FixtureInstance(
            fixture_id=fixture_id,
            name=name,
            manufacturer=manufacturer,
            model=model,
            mode=mode,
            universe=universe,
            address=address,
            channels=channels,
            raw=raw,
        )

    return fixtures


def parse_fixture_groups(root: ET.Element) -> List[FixtureGroupHead]:
    groups: List[FixtureGroupHead] = []

    for group in iter_nodes(root, "FixtureGroup"):
        group_id = attr_any(group, ["ID", "Id", "id"])
        group_name = attr_any(group, ["Name"]) or first_child_text(group, ["Name"])

        # QLC+ stores group head placement as Head tags with X/Y attributes and Fixture attr.
        for head in children_named(group, "Head"):
            fixture_id = attr_any(head, ["Fixture", "FixtureID", "fixture"])
            head_index = safe_int((head.text or "").strip())
            x = safe_int(attr_any(head, ["X", "x"]))
            y = safe_int(attr_any(head, ["Y", "y"]))

            if fixture_id:
                groups.append(
                    FixtureGroupHead(
                        group_name=group_name,
                        group_id=group_id,
                        x=x,
                        y=y,
                        fixture_id=fixture_id,
                        head_index=head_index,
                    )
                )

    return groups


def parse_rgb_matrices(root: ET.Element) -> List[MatrixFunction]:
    matrices: List[MatrixFunction] = []

    for fn in iter_nodes(root, "Function"):
        fn_type = attr_any(fn, ["Type", "type"])
        if "RGB" not in fn_type and "Matrix" not in fn_type:
            continue

        function_id = attr_any(fn, ["ID", "Id", "id"])
        name = attr_any(fn, ["Name"]) or first_child_text(fn, ["Name"])
        raw: Dict[str, str] = {}
        for child in list(fn):
            text = (child.text or "").strip()
            if text:
                raw[local_name(child.tag)] = text

        matrices.append(
            MatrixFunction(
                function_id=function_id,
                name=name,
                fixture_group=raw.get("FixtureGroup", raw.get("FixtureGroupID", "")),
                algorithm=raw.get("Algorithm", ""),
                width=safe_int(raw.get("Width")),
                height=safe_int(raw.get("Height")),
                raw=raw,
            )
        )

    return matrices


# -----------------------------
# Fixture profile parsing
# -----------------------------


def parse_fixture_profiles(fixtures_dir: Optional[Path]) -> Dict[Tuple[str, str, str], FixtureModeInfo]:
    if fixtures_dir is None or not fixtures_dir.exists():
        return {}

    profiles: Dict[Tuple[str, str, str], FixtureModeInfo] = {}

    for path in fixtures_dir.rglob("*.qxf"):
        root = parse_xml(path)
        manufacturer = first_child_text(root, ["Manufacturer"], path.parent.name)
        model = first_child_text(root, ["Model"], path.stem)

        for mode_node in iter_nodes(root, "Mode"):
            mode_name = attr_any(mode_node, ["Name", "name"]) or first_child_text(mode_node, ["Name"], "")
            channels = children_named(mode_node, "Channel")
            heads = children_named(mode_node, "Head")

            info = FixtureModeInfo(
                manufacturer=manufacturer,
                model=model,
                mode=mode_name,
                channel_count=len(channels) if channels else None,
                head_count=len(heads) if heads else None,
            )

            for head_index, head_node in enumerate(heads):
                channel_nums: List[int] = []
                for ch in children_named(head_node, "Channel"):
                    # QXF heads typically store channel number as text.
                    ch_num = safe_int((ch.text or "").strip())
                    if ch_num is not None:
                        channel_nums.append(ch_num)
                info.heads[head_index] = channel_nums

            # Lightweight channel grouping by channel name/group hints.
            # This is not a full QLC capability parser, but it is useful for reports.
            channel_names: Dict[int, str] = {}
            for idx, ch in enumerate(channels):
                channel_names[idx] = attr_any(ch, ["Name", "name"]) or first_child_text(ch, ["Name"], "")

            for head_index, ch_list in info.heads.items():
                for ch_num in ch_list:
                    label = channel_names.get(ch_num, "").lower()
                    if any(token in label for token in ["red", "green", "blue", "white", "rgb", "color", "colour"]):
                        info.rgb_channels_by_head.setdefault(head_index, []).append(ch_num)
                    if any(token in label for token in ["dimmer", "intensity", "master"]):
                        info.dimmer_channels_by_head.setdefault(head_index, []).append(ch_num)
                    if any(token in label for token in ["shutter", "strobe"]):
                        info.shutter_channels_by_head.setdefault(head_index, []).append(ch_num)

            if not heads:
                info.warnings.append("Mode has no explicit Head definitions.")
            if channels and heads:
                assigned = sorted({ch for values in info.heads.values() for ch in values})
                if not assigned:
                    info.warnings.append("Mode defines heads, but no channels are assigned to heads.")

            profiles[(manufacturer, model, mode_name)] = info

    return profiles


# -----------------------------
# Report construction
# -----------------------------


def profile_lookup(
    fixture: FixtureInstance, profiles: Dict[Tuple[str, str, str], FixtureModeInfo]
) -> Optional[FixtureModeInfo]:
    direct = profiles.get((fixture.manufacturer, fixture.model, fixture.mode))
    if direct:
        return direct

    # Be forgiving about missing manufacturer/mode casing.
    for (manufacturer, model, mode), info in profiles.items():
        if model.lower() == fixture.model.lower() and mode.lower() == fixture.mode.lower():
            return info
        if model.lower() == fixture.model.lower() and not fixture.mode:
            return info

    return None


def build_cells(
    groups: List[FixtureGroupHead],
    fixtures: Dict[str, FixtureInstance],
    profiles: Dict[Tuple[str, str, str], FixtureModeInfo],
) -> Tuple[List[TopologyCell], List[str]]:
    cells: List[TopologyCell] = []
    warnings: List[str] = []

    for group_head in groups:
        fixture = fixtures.get(group_head.fixture_id)
        if fixture is None:
            warnings.append(
                f"FixtureGroup '{group_head.group_name}' references missing fixture ID {group_head.fixture_id}."
            )
            continue

        info = profile_lookup(fixture, profiles)
        cell_warnings: List[str] = []

        head_channels: List[int] = []
        rgb_channels: List[int] = []
        dimmer_channels: List[int] = []
        shutter_channels: List[int] = []

        if info and group_head.head_index is not None:
            head_channels = info.heads.get(group_head.head_index, [])
            rgb_channels = info.rgb_channels_by_head.get(group_head.head_index, [])
            dimmer_channels = info.dimmer_channels_by_head.get(group_head.head_index, [])
            shutter_channels = info.shutter_channels_by_head.get(group_head.head_index, [])
            cell_warnings.extend(info.warnings)
            if info.head_count is not None and group_head.head_index >= info.head_count:
                cell_warnings.append(
                    f"Head index {group_head.head_index} exceeds profile head count {info.head_count}."
                )
        elif profiles:
            cell_warnings.append("No matching .qxf profile/mode found for this fixture.")

        address_one_based = fixture.address + 1 if fixture.address is not None else None
        if fixture.address is not None and fixture.channels is not None:
            start = fixture.address + 1
            end = fixture.address + fixture.channels
            channel_range = f"{start}-{end}"
        else:
            channel_range = "unknown"

        cells.append(
            TopologyCell(
                group_name=group_head.group_name,
                group_id=group_head.group_id,
                x=group_head.x,
                y=group_head.y,
                fixture_id=fixture.fixture_id,
                fixture_name=fixture.name,
                manufacturer=fixture.manufacturer,
                model=fixture.model,
                mode=fixture.mode,
                universe=fixture.universe,
                address_zero_based=fixture.address,
                address_one_based=address_one_based,
                channel_range_one_based=channel_range,
                head_index=group_head.head_index,
                head_channels=head_channels,
                rgb_channels=rgb_channels,
                dimmer_channels=dimmer_channels,
                shutter_channels=shutter_channels,
                warnings=cell_warnings,
            )
        )

    return cells, warnings


def make_report(workspace: Path, fixtures_dir: Optional[Path]) -> TopologyReport:
    root = parse_xml(workspace)
    fixtures = parse_fixtures(root)
    groups = parse_fixture_groups(root)
    matrices = parse_rgb_matrices(root)
    profiles = parse_fixture_profiles(fixtures_dir)
    cells, warnings = build_cells(groups, fixtures, profiles)

    if not fixtures:
        warnings.append("No Fixture nodes were found. Confirm this is a QLC+ workspace file.")
    if not groups:
        warnings.append("No FixtureGroup head mappings were found.")
    if fixtures_dir and not profiles:
        warnings.append(f"No .qxf profiles were parsed from {fixtures_dir}.")

    return TopologyReport(
        workspace=str(workspace),
        fixtures_dir=str(fixtures_dir) if fixtures_dir else None,
        fixtures=list(fixtures.values()),
        fixture_groups=groups,
        matrices=matrices,
        cells=cells,
        warnings=warnings,
    )


# -----------------------------
# Output formatting
# -----------------------------


def fmt_list(values: List[int]) -> str:
    if not values:
        return ""
    return ", ".join(str(v) for v in values)


def render_markdown(report: TopologyReport) -> str:
    lines: List[str] = []
    lines.append("# QLC+ Topology Inspector Report")
    lines.append("")
    lines.append(f"Workspace: `{report.workspace}`")
    lines.append(f"Fixture profiles: `{report.fixtures_dir or 'not provided'}`")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Fixtures found: {len(report.fixtures)}")
    lines.append(f"- Fixture group head mappings found: {len(report.fixture_groups)}")
    lines.append(f"- RGB Matrix functions found: {len(report.matrices)}")
    lines.append(f"- Topology cells built: {len(report.cells)}")
    lines.append("")

    if report.warnings:
        lines.append("## Global Warnings")
        lines.append("")
        for warning in report.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    lines.append("## Fixtures")
    lines.append("")
    lines.append("| ID | Name | Manufacturer | Model | Mode | Universe | Address | Channels |")
    lines.append("|---|---|---|---|---|---:|---:|---:|")
    for fixture in sorted(report.fixtures, key=lambda f: safe_int(f.fixture_id) if safe_int(f.fixture_id) is not None else 10**9):
        addr = fixture.address + 1 if fixture.address is not None else ""
        lines.append(
            f"| {fixture.fixture_id} | {fixture.name} | {fixture.manufacturer} | {fixture.model} | {fixture.mode} | "
            f"{fixture.universe if fixture.universe is not None else ''} | {addr} | {fixture.channels if fixture.channels is not None else ''} |"
        )
    lines.append("")

    lines.append("## Fixture Group Topology Cells")
    lines.append("")
    lines.append(
        "| Group | X | Y | Fixture ID | Fixture | Head | Universe | Address Range | RGB Ch | Dimmer Ch | Shutter Ch | Warnings |"
    )
    lines.append("|---|---:|---:|---:|---|---:|---:|---|---|---|---|---|")
    for cell in sorted(report.cells, key=lambda c: (c.group_name, c.y if c.y is not None else -1, c.x if c.x is not None else -1)):
        lines.append(
            f"| {cell.group_name} | {cell.x if cell.x is not None else ''} | {cell.y if cell.y is not None else ''} | "
            f"{cell.fixture_id} | {cell.fixture_name} | {cell.head_index if cell.head_index is not None else ''} | "
            f"{cell.universe if cell.universe is not None else ''} | {cell.channel_range_one_based} | "
            f"{fmt_list(cell.rgb_channels)} | {fmt_list(cell.dimmer_channels)} | {fmt_list(cell.shutter_channels)} | "
            f"{' ; '.join(cell.warnings)} |"
        )
    lines.append("")

    if report.matrices:
        lines.append("## RGB Matrix Functions")
        lines.append("")
        lines.append("| ID | Name | Fixture Group | Algorithm | Width | Height |")
        lines.append("|---:|---|---|---|---:|---:|")
        for matrix in report.matrices:
            lines.append(
                f"| {matrix.function_id} | {matrix.name} | {matrix.fixture_group} | {matrix.algorithm} | "
                f"{matrix.width if matrix.width is not None else ''} | {matrix.height if matrix.height is not None else ''} |"
            )
        lines.append("")

    lines.append("## Next Checks")
    lines.append("")
    lines.append("- Confirm every expected physical section appears exactly once.")
    lines.append("- Confirm X/Y order matches the intended physical bar or ring layout.")
    lines.append("- Confirm head index order matches the actual fixture manual.")
    lines.append("- Confirm RGB, dimmer, and shutter channels are present for every intended emitter.")
    lines.append("- Confirm universe/address ranges match the Art-Net patch plan.")
    lines.append("")

    return "\n".join(lines)


def write_outputs(report: TopologyReport, markdown_path: Path, json_path: Optional[Path]) -> None:
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(render_markdown(report), encoding="utf-8")

    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")


# -----------------------------
# CLI
# -----------------------------


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect QLC+ workspace fixture topology.")
    parser.add_argument("--workspace", required=True, type=Path, help="Path to QLC+ .qxw workspace.")
    parser.add_argument("--fixtures-dir", type=Path, default=None, help="Optional directory containing .qxf profiles.")
    parser.add_argument("--out", required=True, type=Path, help="Markdown report output path.")
    parser.add_argument("--json", type=Path, default=None, help="Optional JSON report output path.")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)

    if not args.workspace.exists():
        print(f"Workspace does not exist: {args.workspace}", file=sys.stderr)
        return 2

    if args.fixtures_dir and not args.fixtures_dir.exists():
        print(f"Fixture profile directory does not exist: {args.fixtures_dir}", file=sys.stderr)
        return 2

    report = make_report(args.workspace, args.fixtures_dir)
    write_outputs(report, args.out, args.json)

    print(f"Wrote topology report: {args.out}")
    if args.json:
        print(f"Wrote JSON report: {args.json}")
    if report.warnings:
        print(f"Warnings: {len(report.warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
