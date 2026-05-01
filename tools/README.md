# Tools

## QLC+ Topology Inspector Prototype

File:

```text
tools/qlc_topology_inspector.py
```

Purpose:

```text
Read a QLC+ workspace and optional fixture profile directory, then generate a report showing fixture group X/Y mapping, fixture IDs, head indices, universes, addresses, and channel hints.
```

This is a safe prototype for the future QLC+ fork topology debug overlay.

It does not modify:

1. `.qxw` showfiles
2. `.qxf` fixture profiles
3. Builder scripts
4. MIDI mappings
5. Art Net settings
6. Live output behavior

## Basic usage

```bash
python tools/qlc_topology_inspector.py --workspace path/to/show.qxw --out reports/topology.md
```

## With fixture profiles

```bash
python tools/qlc_topology_inspector.py \
  --workspace path/to/show.qxw \
  --fixtures-dir path/to/qxf \
  --out reports/topology.md \
  --json reports/topology.json
```

## What the report checks

The report attempts to show:

1. Fixture IDs
2. Fixture names
3. Manufacturer / model / mode
4. Universe and address
5. Fixture group X/Y cells
6. Fixture head index
7. RGB channel hints
8. Dimmer channel hints
9. Shutter / strobe channel hints
10. Missing fixture references
11. Missing profile matches
12. Group topology mapping

## Why this matters

Zero Hour GZ depends on accurate visualizer and fixture topology behavior.

This tool helps answer:

1. Is every physical emitter represented?
2. Is the bar wrapping into rows?
3. Are heads ordered correctly?
4. Are RGB Matrix cells mapped to the expected fixture heads?
5. Are universe and address ranges readable before live output?

## Limitations

This is a prototype.

It is intentionally defensive and does not guess missing QLC+ behavior.

Current limitations:

1. It does not fully replicate QLC+ C++ fixture capability parsing.
2. It only uses lightweight channel name hints for RGB / dimmer / shutter grouping.
3. It does not send output.
4. It does not modify workspaces.
5. It may need updates once tested against the current Zero Hour GZ `.qxw` structure.

## Intended next step

Run it against the current Zero Hour GZ workspace and fixture profile folder, then compare the report against what QLC+ visualizer shows.
