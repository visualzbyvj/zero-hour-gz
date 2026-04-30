# Zero Hour GZ - QLC+ project rule

## Always

- Prefer `python _rebuild_all.py` for full engine + VC refresh unless you know script dependencies.
- After XML changes: close and reopen the `.qxw` in QLC+.
- Backup before bulk scripts: `_Showfile_Backups/` or project backup folder.

## Engine truths (QLC+ 5.2.1)

- Beat chaser: runner adds **1000** per beat tick; Tempo=Beats step duration is beat-quantized in practice.
  Source: `engine/src/chaserrunner.cpp:774` -- `m_elapsedBeats += 1000`
- SpeedDial formula (`vcspeeddial.cpp:511`): `currentTime * globalFactor * perFunctionFactor`.
  Child Function Duration="6" = SpeedMultiplier One (1.0x). Presets set **Time** only, not the factor.
- SpeedMultiplier enum: 0=None, 1=Zero, 2=1/16, 3=1/8, 4=1/4, 5=1/2, 6=One(1.0x), 7=Two, 8=Four, 9=Eight, 10=Sixteen.
- Visibility bitmask: PlusMinus=1, Dial=2, Tap=4, Ms=64, Multipliers=128, Apply=256, Beats=512.
- HTP: highest DMX wins on intensity-group channels.

## Known dead ends

- **Sub-beat step duration**: impossible. Beat clock quantum = 1 beat (1000 millibeats per tick). Cannot reliably hold for half a beat with Tempo=Beats chasers.
- **Beats grid "1" button**: not in QLC+ 5.2.1 QML (`VCSpeedDialItem.qml:168-305`). Use Multipliers X (reset to 1x) or Presets instead.
- **Presets as factor control**: presets only set base `currentTime`; the global factor applies on top. Cannot set the factor via a preset.

## Source index (bundled tree)

- `ui/src/virtualconsole/vcspeeddial.cpp:511-529` -- `applyFunctionsTime()` formula
- `ui/src/virtualconsole/vcspeeddial.cpp:174-187` -- multiplier cache (index 6 = 1000 = 1.0x)
- `engine/src/chaserrunner.cpp:774-780` -- beat advance + step fire condition
- `qmlui/qml/virtualconsole/VCSpeedDialItem.qml:168-305` -- hardcoded Beats grid (no "1" button)
- `qmlui/qml/virtualconsole/VCSpeedDialItem.qml:420-445` -- preset button rendering (Flow layout)
- `engine/src/function.cpp:551-573` -- `timeToBeats` / `beatsToTime` conversion
- `engine/src/function.cpp:651-658` -- `setDuration(ms)` implementation

## "What Would MA3 Do?" decision framework

For every design decision, check industry-standard patterns first:
- **Speed control**: MA3 Speed Masters use BPM tap + bar multiplier (1/4, 1/2, 1, 2, 4 bars). Our preset approach (1x-16x) mirrors this.
- **Intensity priority**: MA3 uses HTP for dimmer. QLC+ does this natively.
- **Effect layering**: MA3 Phasers with layer priority. Our SoloFrame approach is the QLC+ equivalent.
- **Busking layout**: MA3 Playback = executors in rows by function type. Our page layout matches this.
- **Panic/blackout**: MA3 has dedicated "Off All" + "Grand Master". We have PANIC (3060) + FULL BO + GRAND fader.
- **One-button philosophy**: One touch = one complete look. Collections bundle color + motion + FX + intensity.

## Systematic analysis checklist (mandatory before any implementation)

1. Read the QLC+ source for every component involved.
2. Map the full data flow: XML to load() to runtime to render.
3. List ALL possible approaches with trade-offs.
4. Identify hard architectural limits before writing code.
5. Check the MA3/industry framework for proven patterns.
6. Then implement the best option.

## 100-year LD perspective

- **Musical structure**: Everything maps to bars (4 beats at 4/4), phrases (4/8/16 bars), sections (intro/build/drop/break). Speed controls map to these, not raw ms.
- **Operator hand path**: Which controls need to be adjacent? What is the panic recovery flow? Design for muscle memory.
- **Layering hierarchy**: Intensity > Color > Motion > FX. VC layout reflects this top-to-bottom.
- **One-button philosophy**: The best cue is one button press. Collections are king.
- **Fail-safe**: PANIC always works. GRAND always dims. FULL BO always blacks out. No exceptions.

## Build pipeline

Order is in `_rebuild_all.py` (SCRIPTS). `_build_new_vc.py` is always last.
Serial execution only -- parallel stages are architecturally incompatible (all scripts share one .qxw via read-modify-write).

20-script sequence: `_build_advanced_fns` -> `_patch_ring_chase` -> `_build_ring_fx` -> `_build_ring_out_in_chase` -> `_build_colored_out_in` -> `_build_ring_fx_matrix` -> `_build_strobes` -> `_build_all_color` -> `_build_spatial_splits` -> `_build_macros` -> `_build_bump` -> `_build_ring_fx_soft` -> `_build_accel_chasers` -> `_build_tunnel` -> `_build_white_ring_layer` -> `_build_bass_hits` -> `_build_show_arc` -> `_build_intensity_faders` -> `_build_ring_rgbmatrix` -> `_build_new_vc`

## ID ranges (authoritative)

| Range | Type | Builder |
|-------|------|---------|
| 0-34 | Scenes (busk colors, blackout, misc) | hand-built / legacy |
| 35-40 | Ring strobe helpers | `_build_strobes.py` |
| 41-48 | Stripped (legacy) | -- |
| 71 | Chaser RING CHASE OUTER+INNER CW | `_build_ring_out_in_chase.py` |
| 73 | Collection MASTER STROBE ALL | `_build_strobes.py` |
| 74-93 | Scenes (hardware strobe) | `_build_strobes.py` |
| 94-113 | Chasers/collections (ring strobe tiers) | `_build_strobes.py` |
| 114-137 | Scenes/Collections (BUSK colors, LOOK, STATE) | hand-built |
| 200-523 | Scenes (LED panel colors, PINK, COB) | `_rebuild_scenes.py` |
| 448-474 | Chasers (LED panel chases) | pre-existing |
| 475-483 | RGBMatrix (LED panel FX) | pre-existing |
| 1000-1008 | Collections/Scenes (LOOK, STATE) | `_build_macros.py` |
| 1200-1212 | Chasers (soft) | `_build_advanced_fns.py` |
| 1300-1311 | Chasers (ping-pong) | `_build_advanced_fns.py` |
| 1400-1414 | Collections (split O+I) | `_build_advanced_fns.py` |
| 1500-1507, 1516-1517 | Scenes (intensity) | `_build_advanced_fns.py` |
| 1510-1515 | Chasers (ring wave) | `_patch_ring_chase.py` |
| 1550-1581 | Scenes (ring segments) | `_patch_ring_chase.py` |
| 1600-2055 | Scenes (ring FX sweep) | `_build_ring_fx.py` |
| 1750-1757 | Chasers (white patterns) | `_build_ring_fx.py` |
| 1770-1777 | Chasers (colored SWEEP CW) | `_build_ring_fx.py` |
| 2060-2084 | Chasers (colored O+I) | `_build_colored_out_in.py` |
| 2100-2539 | Scenes (colored O+I) | `_build_colored_out_in.py` |
| 2600-2827 | Scenes (ring FX matrix) | `_build_ring_fx_matrix.py` |
| 2850-2905 | Chasers (ring FX matrix) | `_build_ring_fx_matrix.py` |
| 2918-2923 | Collections (master strobe) | `_build_strobes.py` |
| 3000-3009 | Collections (Color Worlds) | `_build_all_color.py` |
| 3020-3039 | Scenes (spatial COB+A55) | `_build_spatial_splits.py` |
| 3040-3045 | Collections (macros) | `_build_macros.py` |
| 3050-3055 | Chasers (speed tiers) | `_build_macros.py` |
| 3060-3061 | Scene PANIC, Scene STROBE KILL | `_build_macros.py` |
| 3070-3074 | Scenes/Chasers (BUMP) | `_build_bump.py` |
| 3100-3155 | Chasers (soft ring/matrix) | `_build_ring_fx_soft.py` |
| 3200-3263 | Chasers (accel) | `_build_accel_chasers.py` |
| 3300-3329 | Scenes/Chasers (tunnel) | `_build_tunnel.py` |
| 3400-3419 | Scenes/Chasers (white ring layer) | `_build_white_ring_layer.py` |
| 3500-3509 | Scenes/Chasers (bass hits) | `_build_bass_hits.py` |
| 3600-3605 | Chasers (emotional arcs: Descent/Betrayal/Long Climb/Hunt/Grinder/Resurrection) | `_build_show_arc.py` |
| 3700-3734 | RGBMatrix (ring effects) | `_build_ring_rgbmatrix.py` |
| 3740-3749 | Darkness Toolkit (scenes + dark chasers) | `_build_cosmic.py` |
| 3750-3759 | White Phaser seed scenes | `_build_cosmic.py` |
| 3760-3766 | White Phaser chasers (breathe/heartbeat/swell/sparkle/drift/ghost/pulse) | `_build_cosmic.py` |
| 3770-3779 | Surprise Roulette (Random+SingleShot latches) | `_build_cosmic.py` |
| 3800-3808 | Ramp / Time-shape (accel/decel/cinematic build/afterglow) | `_build_cosmic.py` |

VC pages: 0=BUSK, 1=COLOR, 2=FX GRID, 3=MATRIX, 4=IMPACT, 5=LOOKS, 6=ATMOSPHERE, 7=TOUCH, 8=ACCEL, 9=COSMIC.
Widget bases: 10000 (BUSK), 11000 (COLOR), 12000 (FX GRID), 15000 (MATRIX), 15200 (IMPACT), 20000 (LOOKS), 25000 (TOUCH), 26000 (ATMOSPHERE), 27000 (ACCEL), 28000 (COSMIC).

## Fixture layouts

| ID | Name | Type | Ch |
|----|------|------|----|
| 0, 7, 26, 27 | A55 Flash (FL FR BL BR) | RGB segments | 10 |
| 1, 6, 14, 17 | 4-Cell COB Blinder | RGBW blinder | 12 |
| 2, 11, 28, 29 | 30W COB-RGB | RGB+strobe | 7 |
| 3, 4, 10, 19 | Outer Ring (F L B R) | 8-seg RGB | 24 |
| 5, 23, 25, 20 | Inner Ring (L B F R) | 8-seg RGB | 24 |
| 15, 16, 18, 21 | White Ring (F L B R) | 16-seg white | 16 |
| 8, 9, 22, 24 | LED Matrix Panels | 154ch | 48 RGB pixels + 8 white |

OUTER_BARS = (3, 4, 10, 19) physical order F/L/B/R.
INNER_BARS = (25, 5, 23, 20) physical order F/L/B/R.
RGB_SEGS = 8 per bar, WHITE_SEGS = 16 per bar.

## Tooling commands

- `python _session_init.py` -- full dashboard (counts, build state, warnings, free IDs)
- `python _rebuild_all.py` -- full serial rebuild + registry + post lint/index
- `python _rebuild_all.py --rollback` -- restore last backup
- `python _lint_showfile.py` -- write `_LD_AUDIT.md`
- `python _qxw_index.py` -- write `_QXW_INDEX.json`
- `python _what_changed.py` -- semantic diff vs latest backup
- `python _preview_changes.py --dry-run` -- rebuild on temp + diff (no save)
- `python _snapshot.py` -- checkpoint to `_snapshots/` + write `_vc_snapshot.json`
- `python _snapshot.py --check` -- compare current to last snapshot
- `python _fixture_cache.py` -- refresh `_fixture_cache.json`
- `python _generate_engine_ref.py` -- refresh `QLC_ENGINE_REFERENCE.md`

## Cosmic-god architecture (feasibility-audited)

These principles are embedded in the showfile and every builder must respect them.

### Pillar 1: Darkness is a primary color
- Blackout is not a kill switch; it is a rest note. `DARK - 8 BAR BLACK` (3746) exists
  as a *musical* blackout hold, not an emergency.
- Scenes 3740-3744 are intimacy tools (WHISPER, SILHOUETTE, CANDLE, HALF RIG F/B).
  Use them BEFORE climaxes, not only as releases.
- `DARK - NEG STROBE` (3747) inverts the presence/absence polarity — layer on a
  color look for ferocity.
- Always keep PANIC (3060), FULL BO flash (126, ForceLTP), and ALL OFF (StopAll)
  accessible. Failure to reach black in <1s is a cardinal sin.

### Pillar 2: Time is material (ramps, not rates)
- Ramp chasers 3800-3808 use **Tempo=Time** with exponential Hold curves
  (`_expo_holds(n, start, end)` helper in `_build_cosmic.py`). Accel/decel via
  ms-valued per-step holds, NOT beat-quantized stepping.
- **Dead end**: Tempo=Beats chasers cannot sub-divide a beat. For sub-beat motion,
  use Tempo=Time with hold values in ms.
- Build = escalation; Release = afterglow; Crescendo = exposition. Treat every
  chaser as a dramatic curve, not a metronome.

### Pillar 3: Phaser / LFO layer on White Ring only
- The White Ring has **independent per-segment dimmer channels** (16 fixtures × 16
  segs = 1-channel each). This is the ONLY surface where you can overlay breathing
  intensity on top of a colored look via HTP without conflicts.
- Phaser chasers 3760-3766 (breathe, heartbeat, swell, sparkle, drift, ghost, pulse)
  are intentionally scoped to White Ring. Do NOT attempt RGB ring phaser overlays
  with this pattern — RGB color IS brightness for those fixtures.
- If an RGB-ring overlay is needed: build the effect as a dedicated color-varying
  chaser (e.g. "RED BREATHING") rather than decomposing into color + intensity layers.

### Pillar 4: Surprise as a muse (Random + SingleShot latch)
- Chasers 3770-3779 use `RunOrder=Random` + `SingleShot` + `Hold=HOLD_HUGE` (1M beats).
  First random step latches and holds until operator stops it. Gives a "roulette"
  surface for busking out of muscle memory.
- **Do NOT** use Random+Loop for this — it keeps cycling chaotically. The
  latch-on-first-step pattern is the one that feels "generative but usable".

### Pillar 5: Emotional naming over genre filenames
- Show arcs are named for feelings (`THE DESCENT`, `THE BETRAYAL`, `THE LONG CLIMB`,
  `THE HUNT`, `THE GRINDER`, `THE RESURRECTION`). Genre is a subtitle in parentheses.
- Energy states use verbs/states of being (`SIMMER`, `GROOVE`, `SURGE`, `DISSOLVE`,
  `TENSION`, `ERUPTION`), not tempos or BPM numbers.
- Color Worlds use environment names (`INFERNO`, `EMBER`, `SOLAR`, `VERDANT`, `ARCTIC`,
  `OCEAN`, `ULTRAVIOLET`, `AURORA`, `PRISM`, `VOID`), not hex/RGB tuples.

### Pillar 6: SoloFrame = layer discipline
- Mutually-exclusive tools (one phaser at a time, one color world at a time, one
  darkness scene at a time) MUST be in SoloFrames. This is the QLC+ equivalent of
  MA3 layer priority.
- Compatible layers (intensity faders × color × FX × strobe) live in sibling
  non-solo frames — they can stack via HTP.

### Pillar 7: Three-tier surface philosophy
- **BUSK (page 0)**: fast operation surface. Everything that changes per-song.
- **Deep-dive pages (1-8)**: subsystem-focused surfaces (COLOR, FX GRID, MATRIX,
  IMPACT, LOOKS, ATMOSPHERE, TOUCH, ACCEL). Reached only when BUSK can't express
  the moment.
- **COSMIC (page 9)**: director tier. Darkness, phaser, surprise, ramps, emotional
  arcs. For the operator who has done the work to think like a storyteller, not a
  button-masher.

### Pillar 8: Fail-safes are sacred
- PANIC (3060) is ALWAYS a warm-white wash at 100%, on EVERY page.
- FULL BO (126 with ForceLTP="1") blacks out instantly even over LTP colors.
- ALL OFF (Action="StopAll") disengages every active function.
- GRAND fader always dims the full rig.
- No exceptions. Ever.

## Feasibility matrix — what QLC+ CAN and CANNOT do

### Fully supported (use freely)
- Darkness scenes, blackout-hold chasers with Tempo=Beats.
- White-ring phaser overlays (independent dimmer channels).
- Random+SingleShot latch pattern for surprise roulettes.
- Per-step Tempo=Time chasers for accelerando/ritardando.
- Tap-advance SingleShot chasers for narrative arcs.
- SoloFrame for mutual-exclusion ("one thing at a time").
- Chaser.Run order: Loop, SingleShot, PingPong, Random.
- Collection to fire N functions simultaneously (no speed master, duration=max child).
- RGBMatrix native algorithms (Waves/Fill/Marquee/etc.) + `<Tempo>Beats</Tempo>`.
- SpeedDial widgets binding multiple functions; Duration="6" = 1.0x multiplier.
- VCMatrix widget for live algorithm + color picking (loads by algorithm name).
- AudioTriggers widget (maps freq bands to function IDs) — underutilized today.
- CueList widget for Next/Previous narrative stepping — underutilized today.
- Show function (timeline auto-director) — underutilized today.

### Requires architectural workaround
- Phaser overlay on RGB rings: must pre-bake as color-varying chaser, not decomposed.
- grandMA3-style color palettes (reference-based recolor): requires Loopback Universe
  setup (OS-level input/output routing). Not achievable purely in builders.
- A/B toggle banks: approximate with two SoloFrames + a Flash button.
- Auto-director with live busking on top: use Show function + SoloFrame isolation.

### Hard dead ends — don't attempt
- Sub-beat step duration in Tempo=Beats chasers (beat quantum = 1 beat, 1000 millibeats).
- "1x" reset button on the beats-multiplier grid (not in QLC+ 5.2.1 QML).
- Presets that set the speed *factor* (presets set Time only; factor applies on top).
- Runtime state capture / memory slots / undo (no script access to current DMX state).
- Freeze-frame of a live running state (chasers advance; cannot pause and mutate).
- Nested submasters (a slider inside a slider).
- Context-aware color modifiers that introspect what's playing.

## Common mistakes (for humans and AI)

1. **Do not prune the BUSK page** without explicit user request — it is operator-tuned.
2. **Do not use `Random + Loop` chasers for surprise roulettes** — use `Random + SingleShot`
   with `Hold=1_000_000` so the first step latches.
3. **Do not put RGB phaser chasers on outer/inner rings** — they have no separate dimmer
   channel, so HTP layering of intensity on top of color is impossible.
4. **Do not rename `_build_new_vc.py` pages or widget bases** without updating both
   `_lint_showfile.py::EXPECTED_VC_PAGES` and `.cursor/rules/qlc-project.md`.
5. **Do not add builders without inserting them into `_rebuild_all.py::SCRIPTS` in the
   correct order** — builders are serial and write-after-read the same .qxw.
6. **Do not let functions lack a VC reference** — the prune pass will delete them.
   To keep a function as a clone seed, ensure a builder references it during build.

## Errors

See `_ERROR_PATTERNS.md`.
