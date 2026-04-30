# Zero Hour GZ Knowledge Cache

> Master index for the local reference cache used to build and maintain `Zero Hour GZ Project File.qxw`.
> Status: local, offline-first, source-backed where possible.

---

## What This Cache Covers

This cache now holds four major knowledge areas:

1. `QLC+ source-backed references`
2. `QLC+ operational and scripting references`
3. `Professional lighting workflow references`
4. `UI / touchscreen / GrandMA-inspired design references`

Use this file as the starting point instead of searching the repo from scratch each time.

---

## Primary Source-Backed Docs

### `QLC_XML_FORMAT_REFERENCE.md`

Use for:

- workspace XML generation
- widget tags and attributes
- function XML structure
- required vs optional fields

Backed by:

- local QLC+ source code in `qlcplus-QLC-_5.2.1 Source Code`

### `QLC_RGBMATRIX_ALGORITHMS.md`

Use for:

- built-in RGBMatrix algorithms
- script API behavior
- algorithm properties
- direction handling
- custom RGB script planning

Backed by:

- `engine/src/rgb*`
- `resources/rgbscripts/*.js`

### `QLC_VCMATRIX_AND_EFX.md`

Use for:

- VCMatrix XML and behavior
- EFX structure and options
- runtime color and algorithm interaction

Backed by:

- `ui/src/virtualconsole/vcmatrix*`
- `engine/src/efx*`

### `QLC_SOURCE_INDEX.md`

Use for:

- fast file lookups
- where to inspect specific widget/function behavior
- quick XML constant references

### `QLC_ENGINE_REFERENCE.md`

Use for:

- enum lookups
- engine-level constants
- spot-checking internal behavior

---

## Secondary QLC+ Docs

### `QLC_SCRIPTING_AND_TIPS.md`

Use for:

- RGB script authoring
- advanced VC usage
- community-known pitfalls
- speed dial and solo frame patterns

### `_FUNCTION_REGISTRY.md`

Use for:

- project-specific function inventory
- ID mapping and project archaeology

### `PROJECT_DOCUMENTATION.md`

Use for:

- repo/project overview
- existing system documentation

---

## Lighting Workflow Docs

### `PRO_LIGHTING_WORKFLOWS.md`

Use for:

- busking logic
- layer-based show operation
- effect family organization
- BPM conversion rules
- practical live-play ergonomics

### `DMX_STANDARDS_AND_FIXTURES.md`

Use for:

- DMX addressing
- HTP/LTP reasoning
- fixture-profile best practices
- ring/pixel-mapping implications

### `CREATIVE_EFFECTS_LIBRARY.md`

Use for:

- ring effect ideas
- panel effect ideas
- white ring usage
- energy-level and musical-section look design

---

## UI / Console Design Docs

### `GRANDMA_CONCEPTS_FOR_QLC.md`

Use for:

- translating MA workflow into QLC+
- executor-grid thinking
- preset system concepts
- speed-master philosophy

### `TOUCHSCREEN_UI_DESIGN.md`

Use for:

- square-button sizing
- spacing and gutters
- dark-theme rules
- right-lane layout decisions
- page geometry constants

---

## Fast Usage Guide

### When editing `_build_new_vc.py`

Check in this order:

1. `TOUCHSCREEN_UI_DESIGN.md`
2. `GRANDMA_CONCEPTS_FOR_QLC.md`
3. `QLC_XML_FORMAT_REFERENCE.md`
4. `QLC_SOURCE_INDEX.md`

### When editing ring RGBMatrix builders

Check in this order:

1. `QLC_RGBMATRIX_ALGORITHMS.md`
2. `QLC_VCMATRIX_AND_EFX.md`
3. `QLC_SCRIPTING_AND_TIPS.md`
4. `CREATIVE_EFFECTS_LIBRARY.md`

### When debugging merge / blackout / playback behavior

Check in this order:

1. `QLC_XML_FORMAT_REFERENCE.md`
2. `QLC_SOURCE_INDEX.md`
3. `QLC_ENGINE_REFERENCE.md`
4. `DMX_STANDARDS_AND_FIXTURES.md`

### When redesigning show workflow

Check in this order:

1. `PRO_LIGHTING_WORKFLOWS.md`
2. `GRANDMA_CONCEPTS_FOR_QLC.md`
3. `TOUCHSCREEN_UI_DESIGN.md`
4. `CREATIVE_EFFECTS_LIBRARY.md`

---

## Local Source Root

Primary local QLC+ source tree:

`E:\Dropbox\04.11.26 Zero Hour GZ\qlcplus-QLC-_5.2.1 Source Code`

Most relevant folders:

- `ui/src/virtualconsole`
- `engine/src`
- `resources/rgbscripts`

For QLC+ XML-generation work, prefer `ui/src/virtualconsole` over `qmlui`.

---

## Cache Health

Current state:

- source-backed docs: healthy
- workflow/docs layer: healthy
- touchscreen/docs layer: healthy
- corrupted agent outputs: repaired and rewritten as UTF-8

---

## Recommended Next Additions

Useful future cache files if you want this even deeper:

- `FIXTURE_PERSONALITY_NOTES.md`
  Notes per real fixture in your rig.
- `SHOWFILE_DESIGN_RULES.md`
  Hard rules for future page additions.
- `MIDI_CONTROLLER_MAP.md`
  Exact controller-to-widget mapping.
- `LOOK_RECIPES.md`
  Reusable musical looks by genre and song section.

