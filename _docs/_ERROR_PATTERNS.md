# Error patterns - Zero Hour GZ

Structured catalog of known bugs, symptoms, and fixes. Add new entries as you discover them.
Run `python _lint_showfile.py` first; it catches most structural issues automatically.

---

## Pattern 1: Rings do an in-out chase by default at startup

- **Symptom**: On opening QLC+, the outer+inner ring chase starts automatically.
- **Root cause**: A Playback slider's `<Level Value="255"/>` auto-starts function 71 (RING CHASE - OUTER+INNER CW) when the workspace loads.
- **Fix**: Find the slider in VirtualConsole, set its value to 0 (`<Level Value="0"/>`), or re-run `_rebuild_all.py` (which regenerates the VC from scratch with correct defaults).
- **Prevention**: `_lint_showfile.py` (with `--strict`) checks for Playback sliders with Value=255. The `_rebuild_all.py` sanity gate also warns on this pattern.

---

## Pattern 2: Speed buttons do not change chaser speed

- **Symptom**: Clicking 2x / 4x presets on a SpeedDial has no effect; all rates feel identical.
- **Root cause**: Child `<Function Duration="5"/>` uses SpeedMultiplier Half (0.5x) instead of One (1.0x = Duration="6"). With the wrong base multiplier, the global factor cannot apply correctly.
- **Fix**: Ensure each linked `<Function FadeIn="0" FadeOut="0" Duration="6">` in the SpeedDial XML. Re-run `_build_new_vc.py` or `_rebuild_all.py` to regenerate from the fixed template.
- **Prevention**: `_lint_showfile.py` checks speed dial Duration vs the linked function's Tempo type.

---

## Pattern 3: Sub-beat speeds are all identical

- **Symptom**: Setting a Beat-timed chaser to 1/2 beat or 1/4 beat step hold produces no audible or visible difference from 1 beat.
- **Root cause**: Architectural limit in QLC+ 5.2.1. `chaserrunner.cpp:774` advances `m_elapsedBeats += 1000` once per beat tick. Sub-beat duration is not resolvable; the chaser cannot fire mid-beat.
- **Fix**: Not fixable in QLC+ 5.2.1. Use bar-level multipliers instead (1x, 2x, 4x, 8x, 16x presets). For half-time feel, use a 2x multiplier rather than a 1/2-beat step.
- **Prevention**: This is a documented dead end in `.cursor/rules/qlc-project.md`. Do not attempt sub-beat timing with Tempo=Beats.

---

## Pattern 4: Widget content is clipped or buttons are unreadable

- **Symptom**: SpeedDial presets or multiplier buttons are cut off; only part of the dial is visible.
- **Root cause**: Widget Height too small for the combination of Visibility flags and preset count. The QML renderer clips at the widget boundary.
- **Fix**: Increase the widget Height in `_build_new_vc.py`. Use `_widget_sizer.speed_dial_recommend_height()` to compute the safe minimum. Beat-mode dials with 5 presets need at least 142px.
- **Prevention**: `_widget_sizer.py` is imported by `_build_new_vc.py` and `speed_dial_recommend_height()` enforces the minimum automatically.

---

## Pattern 5: XML parse error after build

- **Symptom**: QLC+ refuses to open the project; or `ET.parse()` raises `ParseError`.
- **Root cause**: A build script wrote malformed XML -- unescaped `&`, `<`, or `"` in a function name; or an unclosed tag; or a null byte from a UTF-16 write.
- **Fix**: Restore from `_Showfile_Backups/` (or use `python _rebuild_all.py --rollback`). Run `python _session_init.py` to confirm the file parses. Check the builder that last ran (`_build_report.json`) for the failing script.
- **Prevention**: `_qlc_helpers.py` uses `xml.sax.saxutils.escape()` on all text fields. `_rebuild_all.py` calls `validate_qxw()` after every script to catch breaks immediately.

---

## Pattern 6: Dropbox sync conflict corrupts the showfile

- **Symptom**: QLC+ shows a parse error or strange corrupted content; a "Conflicted copy" file appears in the folder.
- **Root cause**: Two machines saved the `.qxw` simultaneously while Dropbox was syncing.
- **Fix**: Identify the conflicted copies; compare with `python _preview_changes.py <older> <newer>`; restore the correct one. Use `_Showfile_Backups/` if the conflict is unresolvable.
- **Prevention**: Only one machine edits the showfile at a time. Prefer explicit copy-out / copy-in workflow when working on multiple machines. Dropbox pause before bulk rebuilds is recommended.

---

## Pattern 7: VC button or slider has no effect

- **Symptom**: Pressing a button or moving a slider in VC does nothing; no DMX output changes.
- **Root cause**: The widget's `<Function ID="..."/>` references a function ID that does not exist in the current Engine (deleted, not yet built, or wrong ID). Also possible: widget has `<Function ID="4294967295"/>` (no function assigned).
- **Fix**: Check the widget's function reference in the `.qxw`. Run `python _lint_showfile.py` to catch missing references. Re-run the builder that owns the target ID range, then re-run `_build_new_vc.py`.
- **Prevention**: `_lint_showfile.py` checks all VC function references against defined engine IDs after every build.

---

## Pattern 8: Duplicate Function IDs in Engine block

- **Symptom**: `_lint_showfile.py` warns about 1000+ duplicate engine Function IDs. QLC+ may use only the last definition.
- **Root cause**: Scripts that strip and reinsert functions sometimes leave an earlier copy in the file (e.g., if `strip_functions()` regex misses a block due to a non-standard format). Running a builder twice without stripping also doubles blocks.
- **Fix**: This is a persistent warning in this project because QLC+ appears to work correctly (using the last definition). To truly fix it: use `_preview_changes.py` to diff, identify the double blocks, and hand-edit or re-run all builders from scratch via `_rebuild_all.py`.
- **Prevention**: All idempotent builders call `strip_functions()` before inserting. If a new builder does not strip first, add `strip_functions(text, OWNED_IDS)` at the top of its `main()`.

---

## Diagnostic commands

```
python _session_init.py          # parse check + counts + build state
python _lint_showfile.py         # write _LD_AUDIT.md (use --strict for hard fail)
python _lint_showfile.py --strict  # treat dups/missing refs as errors
python _what_changed.py          # semantic diff vs latest backup
python _preview_changes.py       # raw text diff vs latest backup
python _preview_changes.py --dry-run  # rebuild on temp + semantic diff, no save
python _rebuild_all.py --rollback  # restore last backup
```
