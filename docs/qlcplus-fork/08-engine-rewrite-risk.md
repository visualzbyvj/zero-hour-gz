# Engine Rewrite Risk Plan

## Purpose

This file defines why a full QLC+ engine rewrite should be last, not first.

A full engine rewrite is technically possible, but it is the highest risk fork direction.

## Why this is dangerous

The QLC+ engine owns or coordinates:

1. Workspace document state
2. Fixture instances
3. Fixture groups
4. Function lifecycle
5. Scene values
6. Chaser playback
7. RGB Matrix playback
8. Master timer
9. Universes
10. Fader composition
11. Grand Master
12. HTP / LTP behavior
13. Output patching
14. XML load and save
15. Startup function
16. Design / operate mode behavior

Breaking any of these can break existing showfiles.

## Engine rewrite should wait until

1. Topology debug overlay exists
2. Fixture validator exists
3. APC feedback layer is stable
4. Selection engine is stable
5. Phaser engine has been tested
6. Recipe system can generate repeatable outputs
7. Performance UI has been tested
8. Existing QLC+ showfiles still load
9. Regression tests exist

## Required compatibility rule

Do not break `.qxw` compatibility.

Preferred strategy:

```text
Keep native .qxw compatibility.
Store advanced GZ fork metadata in sidecar files until serialization is fully understood.
```

Possible sidecar:

```text
show.qxw
show.gzshow
```

## High risk engine areas

1. Function start / stop lifecycle
2. Function parent behavior
3. Fader requests
4. Universe output composition
5. Grand Master and blackout behavior
6. HTP / LTP channel handling
7. Chaser and RGB Matrix timing
8. Input / output plugin timing
9. XML serialization
10. Fixture ID and function ID references

## Future engine goals

Only after earlier systems are stable, consider:

1. Executor priority engine
2. Attribute ownership
3. Flash / temp / toggle / latch behavior
4. Kill groups
5. Release fade behavior
6. Safety override layer
7. Phrase aware BPM clock
8. Speed masters
9. Rate masters
10. Native phaser runtime
11. Recipe runtime

## Rollback requirement

Every engine change must have:

1. Test workspace
2. Before / after output comparison
3. Known rollback commit
4. Clear affected source files
5. Clear compatibility note
6. Explicit safety review

## Success definition

A future engine rewrite is successful only when it improves live control without breaking:

1. Existing QLC+ showfiles
2. Fixture patching
3. Function references
4. MIDI mappings
5. Art Net output
6. Blackout
7. Grand Master
8. Panic recovery
9. Visualizer / monitor behavior
