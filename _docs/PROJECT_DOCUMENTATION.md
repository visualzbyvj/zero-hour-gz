# Zero Hour GZ — Project guide (Windows / power user)

QLC+ (**Q Light Controller Plus**) **5.2.1** workspace for this rig. This doc assumes you’re comfortable with **paths**, **backups**, **Python on Windows**, and basic **XML**—but you don’t need to live inside the file format for normal show operation.

---

## Terminology (quick)

| Term | What it is |
|------|------------|
| **`.qxw`** | Single-file workspace (UTF-8 XML). Fixtures, functions, Virtual Console, I/O map, monitor layout. |
| **Fixture** | One patched device in the **Fixture Manager** tree. |
| **Function** | Anything in the **Functions** tab: Scene, Chaser, Collection, RGB Matrix, etc. Each has a numeric **ID** in the file. |
| **Scene** | Static DMX snapshot: `<FixtureVal>` channel/value pairs per fixture. |
| **Chaser / RGB Matrix** | References other functions or fixture groups by ID. |
| **Collection** | Ordered list of function IDs; **all members fire simultaneously**. For sequential timing, use a **Chaser**. |
| **Virtual Console (VC)** | `<VirtualConsole>` in the `.qxw`: pages (`Frame`), buttons, sliders, SoloFrames. |
| **Universe** | Up to 512 DMX channels per pipe. **XML uses 0-based `ID`** (`ID="0"` = first universe); the UI often labels **Universe 1, 2, …** = XML `ID` + 1. |

---

## Files and folders (this repo)

| Path | Notes |
|------|--------|
| `Zero Hour GZ Project File.qxw` | **Primary show file.** Double-open in Explorer or **File → Open** in QLC+. |
| `Zero Hour GZ Project File.autosave.qxw` | If present: QLC+ autosave alongside the main file—don’t confuse with intentional backups. |
| `_Showfile_Backups\` | Timestamped manual / pre-change copies. Use when you need to diff or roll back. |
| `QLC+\Fixtures\*.qxf` | Fixture definitions (XML). Referenced by manufacturer/model in the workspace. |
| `_build_full_vc.py` | Legacy **VC** generator (superseded by **`_build_new_vc.py`**). Kept for reference; do not use unless you know you need the old layout. |
| `_build_new_vc.py` | **Current** Virtual Console: replaces **entire** `<VirtualConsole>` with the **5-page** layout (PUNT, EXTENDED BUSK, **FX LIBRARY**, **TOUCH BUSK**, **SOFT / ACCEL**). Run **last** after engine scripts. |
| `_build_vc.py` | Older **VC XML generator** (snippets / string builders). Superseded by **`_build_new_vc.py`**. |
| `_build_advanced_fns.py` | Engine: soft chasers **1200–1212**, ping-pong **1300–1311**, split Collections **1400–1414**, intensity scenes **1500–1507** + **1516–1517**, BeatGenerator mode normalization (preserves BPM). Chasers **1510–1515** are built by **`_patch_ring_chase.py`**. **Idempotent** (strip + reinsert). |
| `_build_strobes.py` | Canonical strobe engine builder: ring strobe helpers **35–40**, hardware strobe scenes **74–93**, ring strobe tiers **94–113**, MASTER STROBE **73**, and global strobe collections **2918/2919/2921/2923**. **Idempotent** (strip + reinsert). |
| `_build_ring_fx.py` | Engine: around-the-ring white + colored sweep scenes (**1600–1665**, **1800–2055**) and chasers **1750–1757**, **1770–1777**. **Idempotent**. |
| `_build_ring_fx_matrix.py` | Engine: extended colored matrix (**2600–2827** scenes, **2850–2905** chasers). **Idempotent**. |
| `_patch_ring_chase.py` | Engine: segment-level ring wave scenes **1550–1581** and chasers **1510–1515**; required before chaser **71**. **Idempotent**. |
| `_build_ring_out_in_chase.py` | Engine: chaser **71** (white outer+inner segment chase). **Idempotent**. |
| `_build_colored_out_in.py` | Engine: colored O+I scenes **2100–2227**, **2300–2539**; chasers **2060–2067**, **2070–2084**. **Idempotent**. |
| `_qlc_helpers.py` | Shared XML + fixture/color helpers for builders (`strip_functions`, `inject_before_monitor`, etc.). |
| `_rebuild_all.py` | Runs the full engine + VC script list in order; validates XML; one backup per run; writes `_build_report.json`, `_FUNCTION_REGISTRY.md`; post-steps **`_qxw_index.py`** + **`_lint_showfile.py`** (parallel). Flags: `--rollback`, `--no-post`. |
| `_qxw_index.py` | Summarizes functions/fixtures/VC widget counts → **`_QXW_INDEX.json`**. |
| `_lint_showfile.py` | Structural checks + **LD audit** (five VC page captions) → **`_LD_AUDIT.md`**. Default: warns on duplicate engine functions / stale VC links; **`--strict`** treats those as errors. |
| `_widget_sizer.py` | SpeedDial height heuristics (used by **`_build_new_vc.py`**). |
| `_snapshot.py` | Copies the live `.qxw` into **`_snapshots/`** with a timestamp. |
| `_preview_changes.py` | Unified diff (default: newest `_Showfile_Backups` vs main showfile). |
| `_what_changed.py` | Quick SHA256 compare: main vs latest backup. |
| `_fixture_cache.py` | Scans **`QLC+/Fixtures/*.qxf`** → **`_fixture_cache.json`**. |
| `_templates.py` | Shared constants (`WORKSPACE_NS`, `NO_FUNCTION_ID`, etc.). |
| `_session_init.py` | Smoke test: Python version, XML parse, core scripts on disk. |
| `_ERROR_PATTERNS.md` | Troubleshooting index for common `.qxw` / tooling failures. |
| `_build_all_color.py` | Engine: ALL-row Collections **3000–3009**. |
| `_build_spatial_splits.py` | Engine: COB+A55 spatial scenes **3020–3039**. |
| `_build_macros.py` | Engine: macros **3040–3045**, sweep speed tiers **3050–3055**, **3060/3061**, LOOK **1000–1002** + **1006–1008**. |
| `_build_bump.py` | Engine: BUMP / decay / BO+HIT **3070–3074**. |
| `_build_ring_fx_soft.py` | Engine: soft ring/matrix chasers **3100–3155**. |
| `_build_accel_chasers.py` | Engine: accel chasers **3200–3263**. |
| `_build_tunnel.py` | Engine: tunnel scenes/chasers **3300+**, **3320–3329**. |
| `_build_white_ring_layer.py` | Engine: white ring layer **3400–3419**. |
| `_build_bass_hits.py` | Engine: bass hits **3500–3509**. |
| `_build_show_arc.py` | Engine: emotional arc cue chasers **3600–3605** (Descent/Betrayal/Long Climb/Hunt/Grinder/Resurrection). |
| `_build_cosmic.py` | Engine: cosmic-god toolkit — Darkness **3740–3749**, White Phaser seeds **3750–3759** + chasers **3760–3766**, Surprise Roulette **3770–3779**, Ramp/Time-shape **3800–3808**. |
| `_patch_midi_vc.py` | **In-place** patch of the live `.qxw`: Page 4 MIDI note map (80–89), Page 2 chase/strobe + slider inputs, touch sizing, and **MIDI feedback** `<Output Universe="3" …/>` on buttons (requires a **MIDI output** universe in I/O Manager). **Idempotent risks:** re-running may duplicate inputs/outputs—work from a backup copy. |
| `_add_solo_frames_p3.py` | **One-time-style** patch: inserts **Page 3** SoloFrame strobe-division banks and renames **duplicate** SpeedDial widget IDs on Page 3 (**800–807** → **1800–1807**). Do not run twice on the same file without checking for doubled blocks. |
| `_gen_qlc_engine.py` | Generates engine **function** XML fragments → `_engine_insert.xml` (not a full show). |
| `_gen_scenes.py` | Builds **`FixtureVal`-style** channel strings (rings, panels, blackouts) for copy into scenes—does not write the `.qxw` by itself. **Note:** running/importing this file also writes `_scenes_block.xml` (legacy generator side effect)—prefer copying `panel_rgb()` into a small helper instead of importing the whole module. |
| `_build_monitor.py` | **In-place** replacement of **`<Monitor>…</Monitor>`** with a **GROUNDZERO-style layout**: totems FL/BL/BR/FR + ring (Outer/Inner/White) positions for the 2D/3D monitor. Safe to re-run (replaces one block). |
| `_rebuild_scenes.py` | **One-time / idempotent:** inserts **PINK** LED panel + COB scenes (**IDs 506–523**) before `<Monitor>` if `SCENE - LED PANEL - Full - PINK` is missing. |
| `_rebuild_collections.py` | **Idempotent:** inserts **Collection** functions **1000–1005** (`LOOK - *`, `STATE - *`) before `<Monitor>` if ID **1000** is missing. |
| `_rebuild_chasers.py` | **Read-only check:** verifies core **Chaser** IDs **448–474** exist (no XML write). |
| `_rebuild_rgbmatrix.py` | **Read-only check:** verifies **RGBMatrix** IDs **475–483** exist (no XML write). |
| `_patch_engine.py` | Example **string-splice** merge; brittle—prefer QLC+ UI or a proper XML merge. |
| `_generate_engine_ref.py` | Scans bundled QLC+ **5.2.1** source → **`QLC_ENGINE_REFERENCE.md`** (enums, loadXML samples, pattern hits). |
| `QLC_ENGINE_REFERENCE.md` | Auto-generated engine cheat sheet (re-run after QLC+ source updates). |
| `PROJECT_DOCUMENTATION.md` | This file (includes former **`RESUME_CONTEXT.md`** content below). |

**Full rebuild:** run `python _rebuild_all.py` from this folder (`_build_new_vc.py` last). After any script run, **close and reopen** the project in QLC+ so changes load. **Authoritative IDs / handshake:** see **Authoritative project context** below.

**Dropbox:** Sync conflicts can corrupt `.qxw` files if two PCs edit the same show. Prefer **one editor at a time** or explicit **copy-out / copy-in** workflow.

---

## I/O: what to touch in QLC+ vs raw XML

Routing lives under **`<Engine><InputOutputMap>`**.

- **Art-Net:** Output lines point at node **IP** and **universe** parameters in `<PluginParameters>` / plugin settings. Match your nodes’ web UI (subnet, Art-Net universe index).
- **MIDI input:** Patched to an input universe; VC widgets use **`<Input Universe="0" Channel="…"/>`** when external control is saved—**`0`** here is the **first input universe’s XML index**, not necessarily “Universe 1” in every labeling scheme. If MIDI mapping breaks after hand-editing, compare to **Input/Output Manager** in the GUI.
- **MIDI feedback / output-only universe:** Optional separate universe for host → controller LEDs; no DMX fixtures required on that universe. The **`_patch_midi_vc.py`** workflow adds `<Output Universe="3" …/>` on VC buttons—**`3`** is the **fourth** universe’s **0-based XML `ID`** (often shown as **Universe 4** in the UI); align that universe with your APC **MIDI output** line in **Input/Output Manager**.

**Rule of thumb:** Prefer **Input/Output Manager** and **input profiles** in QLC+ for anything you’ll repeat across gigs. Reserve Notepad/VS Code edits for bulk changes you understand and can diff.

---

## Engine (`<Engine>`): functions

- **Scenes:** `<Function Type="Scene">` + `<FixtureVal ID="fixtureId">…</FixtureVal>`.
- **Collections:** `<Function Type="Collection">` + `<Step Number="n">functionId</Step>`.
- Renumbering or copy-pasting `<Function ID="…">` without fixing references breaks chasers/collections/VC **`<Function ID="…"/>`** links.

Browse and edit safely via **Functions** in QLC+; use the workspace search for `Function ID=` only when you know what you’re merging.

---

## Virtual Console

- Section: **`<VirtualConsole>`** … **`</VirtualConsole>`** (sibling to closing `</Engine>` in a normal save).
- **Widget IDs** (`Button` / `Slider` / `SoloFrame` / inner `Frame`) must be **globally unique** across **all** VC pages. Duplicating a block without renumbering = undefined behavior.
- The `_build_full_vc.py` workflow **offsets** duplicated “grid” blocks (e.g. +5000 / +6000 on widget IDs) so the same layout can appear on multiple pages without colliding **widget** IDs; **`<Function ID="…"/>`** still points at engine functions, not VC widgets.
- Layout is **`WindowState` X/Y/Width/Height**—no separate “touch API”; large controls are a UX choice.

---

## Python helpers (Windows)

### Prerequisites

- **Python 3.x** on `PATH` (installer option “Add python.exe to PATH”, or use **py launcher**: `py -3 script.py`).
- Run from the **project directory** so relative paths behave if you change the scripts to use them:

```powershell
cd "E:\Dropbox\04.11.26 Zero Hour GZ"
python .\_build_new_vc.py
```

If `python` isn’t found, try `py .\_build_new_vc.py`.

### `_build_new_vc.py` (preferred for VC)

- **Overwrites** the whole `<VirtualConsole>` in `Zero Hour GZ Project File.qxw`.
- **Before running:** copy the `.qxw` to `_Showfile_Backups\` (or elsewhere) with a timestamp.

### `_build_full_vc.py` (legacy)

- Older full VC replace; superseded by **`_build_new_vc.py`** unless you are reviving the old layout.

### `_gen_qlc_engine.py`

- Writes `_engine_insert.xml`. **Does not** patch the live show unless you merge manually or with a tool you trust.
- Useful when you change repeated color math / blackout coverage and want generated `FixtureVal` strings.

### `_patch_midi_vc.py`

- Patches **`Zero Hour GZ Project File.qxw`** in place (backup first).
- See the **Files and folders** table for scope. After running, open the show in QLC+ and confirm **Input/Output** and **widget external I/O** match your controller profile.

### `_add_solo_frames_p3.py`

- Patches the same **`.qxw`** (backup first). Intended when Page 3 needs SoloFrame banks + unique SpeedDial IDs; see table notes on **not** double-running blindly.

### `_gen_scenes.py`

- Prints or writes scene-related **channel/value** text for rings/panels—merge into `<Engine>` by hand or with your own tooling.

### Quick XML sanity check (optional)

```powershell
python -c "import xml.etree.ElementTree as ET; ET.parse(r'Zero Hour GZ Project File.qxw'); print('parse ok')"
```

A passing parse does **not** guarantee QLC+ semantics (valid IDs, sane references)—only well-formed XML.

---

## Editing your own automation

1. Work on a **copy** of the `.qxw` (e.g. `Zero Hour GZ Project File.dev.qxw`).
2. Parameterize **one** `Path` at the top of new scripts; use `Path(__file__).resolve().parent` when possible so the tree is relocatable.
3. Keep **engine**, **VC**, and **I/O** changes in separate commits / separate script runs so you can bisect mistakes.
4. Avoid blind **find-replace** on values like `Y="40"` across the whole file—VC XML repeats numbers for unrelated widgets.

---

## Fixture definitions (`.qxf`)

Channel order and **mode** names come from the fixture file. After changing a fixture’s **mode** in the patch, re-check every scene/RGB matrix that touches it—indices may no longer match the old programming.

---

## One-page checklist

| Task | Where |
|------|--------|
| Open / run show | QLC+ → open `Zero Hour GZ Project File.qxw` |
| Patch DMX / Art-Net | **Input/Output Manager** |
| Edit cues | **Functions** |
| Edit on-screen layout | **Virtual Console** (design mode) |
| MIDI learn | Widget properties + input profile |
| Regenerate VC from script | Backup `.qxw` → `python .\_build_new_vc.py` → reopen in QLC+ |
| Full engine + VC (canonical) | `python .\_rebuild_all.py` |
| Colored OUT+IN + **5-page** VC | Prefer **`_rebuild_all.py`**; or `python .\_build_colored_out_in.py` then `python .\_build_new_vc.py` — colored O+I on **EXTENDED BUSK** |
| Bulk MIDI inputs + LED feedback on VC | Backup `.qxw` → `python .\_patch_midi_vc.py` → verify I/O universe **3** / APC output |
| Insert Page 3 SoloFrames + fix SpeedDial IDs | Backup `.qxw` → `python .\_add_solo_frames_p3.py` (do not double-run blindly) |
| Reset 2D/3D **Monitor** to GROUNDZERO layout | Backup `.qxw` → `python .\_build_monitor.py` |
| Add **PINK** panel/COB scenes + **LOOK/STATE** collections 1000–1005 | Backup `.qxw` → `python .\_rebuild_scenes.py` then `python .\_rebuild_collections.py` (idempotent) |
| Verify chasers / RGB matrix IDs | `python .\_rebuild_chasers.py` ; `python .\_rebuild_rgbmatrix.py` |
| Roll back | Restore a file from `_Showfile_Backups\` |

---

## Authoritative project context (handoff)

**QLC+ 5.2.1** (QML/Qt Quick). **Project file:** `Zero Hour GZ Project File.qxw`.

### Colored OUT+IN segment chasers (handshake)

| Item | Value |
|------|--------|
| **Generator** | `_build_colored_out_in.py` (uses `_build_ring_fx` helpers) |
| **White chaser** | **71** — `RING CHASE - OUTER+INNER CW`, scenes **1550–1565** |
| **Solid color chasers** | **2060–2067** |
| **Split chasers** | **2070–2084** (15), order matches split collections **1400–1414** |
| **Solid scenes** | **2100–2227** |
| **Split scenes** | **2300–2539** |
| **VC** | **STROBE + O/I** (page 3): O+I block + dial targets **71** + **2060–2084** |

### Strobe IDs **74–93** (after `_build_strobes.py`)

These are **Scenes** (hardware dimmer+strobe channel only on FX fixtures), not chasers. **94–113** are now generated by the same canonical builder as ring strobe chasers/collections. **`_build_strobes.py`** also strips helper scenes **41–48** (legacy) for compatibility.

### Collection **73** (`MASTER STROBE ALL`)

References **multiple chasers** (per fixture group / rate tier). Membership is **mixed function types** (chasers + possibly scenes depending on build order)—always verify in the live `.qxw`.

### SpeedDial `<Visibility>` (QLC+ 5.2.1 QML)

| Bit | Value | Element |
|-----|-------|---------|
| 0 | 1 | PlusMinus |
| 1 | 2 | Dial |
| 2 | 4 | Tap |
| 6 | 64 | Milliseconds |
| 7 | 128 | Multipliers |
| 8 | 256 | Apply |
| 9 | 512 | Beats |

Per linked function, child `<Function … Duration="N">` uses **SpeedMultiplier** enum (**6** = One / 1.0×). **Presets** set dial **Time** only, not the global multiplier index. **Beat-timed chasers:** runner advances **1000** “millibeats” per beat tick—sub-beat step holds are not reliable; use **1× / 2× /4×** style multipliers.

### `_rebuild_all.py` script order (21 steps)

`_build_advanced_fns.py`, `_patch_ring_chase.py`, `_build_ring_fx.py`, `_build_ring_out_in_chase.py`, `_build_colored_out_in.py`, `_build_ring_fx_matrix.py`, `_build_strobes.py`, `_build_all_color.py`, `_build_spatial_splits.py`, `_build_macros.py`, `_build_bump.py`, `_build_ring_fx_soft.py`, `_build_accel_chasers.py`, `_build_tunnel.py`, `_build_white_ring_layer.py`, `_build_bass_hits.py`, `_build_show_arc.py`, `_build_intensity_faders.py`, `_build_ring_rgbmatrix.py`, **`_build_cosmic.py`**, `_build_new_vc.py`.

### Virtual Console (10 pages)

| Page | Name | Widget base | Role |
|------|------|-------------|------|
| 0 | **BUSK** | 10000 | Primary busk surface (colors, FX quick, impact, faders, dials) |
| 1 | **COLOR** | 11000 | Deep color: O/I chases, spatial splits, Color Worlds |
| 2 | **FX GRID** | 12000 | Full ring FX pattern × color grid + ring matrix picks |
| 3 | **MATRIX** | 15000 | VCMatrix live control for rings + panel |
| 4 | **IMPACT** | 15200 | Strobes rate grid + bass hits + bumps |
| 5 | **LOOKS** | 20000 | Genre looks, energy states, show arcs, Color Worlds |
| 6 | **ATMOSPHERE** | 26000 | Soft ring grid + white ring layers + tunnel FX |
| 7 | **TOUCH** | 25000 | Large-square touch-optimized favorites |
| 8 | **ACCEL** | 27000 | Accelerating chasers grid |
| 9 | **COSMIC** | 28000 | Darkness, white phaser, surprise roulette, ramps, emotional arcs |

Fixture IDs, universes, ring geometry, split table **1400–1414**, and HTP notes match the former **`RESUME_CONTEXT.md`** (archived in `_PRE_RESTRUCTURE_BACKUP_20260413/` if needed).

### Session / tooling commands

- `python _session_init.py` — dashboard (counts, last build, warnings).
- `python _qxw_index.py` — refresh `_qxw_index.json`.
- `python _lint_showfile.py` — validate references / VC sanity.
- `python _what_changed.py` — compare two `.qxw` paths.
- `python _generate_engine_ref.py` — refresh **`QLC_ENGINE_REFERENCE.md`**.

---

## Version

Documentation written for **QLC+ 5.2.1** and this folder layout. **`RESUME_CONTEXT.md`** was merged here **2026-04-13**. If you upgrade QLC+, re-test saves and any custom XML assumptions after the first load/save cycle.
