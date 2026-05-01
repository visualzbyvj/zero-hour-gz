# QLC+ Zero Hour Fork Roadmap

## Current planning branch

```text
fork-planning/qlcplus-gz
```

## Fork roadmap summary

### Phase 0: Build and source verification

Goal:

```text
Prove the upstream QLC+ source can be built before changing behavior.
```

Tasks:

1. Fork upstream QLC+
2. Build unmodified source
3. Document build environment
4. Confirm Qt version and CMake flags
5. Create a small test workspace
6. Identify QLC+ 5 QML UI entry points
7. Identify fixture group and RGB Matrix editor entry points

### Phase 1: Topology debug layer

Goal:

```text
Expose how QLC+ maps fixture heads, group positions, matrix cells, and output channels.
```

Deliverables:

1. Read only topology inspector
2. FixtureGroup table output
3. RGB Matrix mapping table
4. Head / emitter overlay plan
5. No engine behavior changes

### Phase 2: Fixture profile validator

Goal:

```text
Catch custom fixture profile problems before they break visualizer, matrix, or live output behavior.
```

Deliverables:

1. Mode channel count validation
2. Head assignment validation
3. RGB / dimmer / shutter validation
4. Laser and strobe safety warnings
5. Matrix compatibility warnings

### Phase 3: APC Mini MK2 feedback layer

Goal:

```text
Make APC Mini MK2 show live state, not just send MIDI input.
```

Deliverables:

1. Page aware LED feedback
2. Function type colors
3. Danger blinking states
4. Active layer feedback
5. Shift / bank state feedback

### Phase 4: MAtricks style selection engine

Goal:

```text
Create reusable fixture order transforms for rings, bars, wings, blocks, rows, columns, and odd/even logic.
```

Deliverables:

1. Natural order
2. Reverse
3. Odd / even
4. Wings
5. Blocks
6. Rows / columns
7. Ring clockwise / counterclockwise
8. Preview before output

### Phase 5: Phaser engine

Goal:

```text
Create MA3 inspired attribute phasers using QLC+ fixture groups, selection transforms, timing, and fader output.
```

Deliverables:

1. Dimmer phaser
2. RGB phaser
3. Fixture order phase
4. Wings / blocks support
5. BPM or speed source
6. Preview mode
7. Safety classification

### Phase 6: Recipe system

Goal:

```text
Build repeatable looks from target, attributes, effects, timing, playback behavior, MIDI mapping, and safety class.
```

Deliverables:

1. Recipe schema
2. Recipe to QLC+ function generation
3. Recipe to executor generation
4. Recipe validation
5. Fixture expansion support

### Phase 7: EDM Performance UI

Goal:

```text
Add a live performance UI optimized for EDM busking.
```

Deliverables:

1. Master / safety strip
2. Executor grid
3. Speed panel
4. APC state panel
5. Topology debug panel
6. Art Net status panel

### Phase 8: Playback / engine rewrite

Goal:

```text
Only after earlier systems are proven, add deeper playback ownership and priority behavior.
```

Deliverables:

1. Attribute ownership
2. Executor priorities
3. Flash / temp / toggle / latch
4. Kill groups
5. Release fade
6. Safety override
7. Backward compatibility

## Recommended first issue after real fork exists

```text
Build upstream QLC+ unchanged and document source entry points for FixtureGroup, RGBMatrix, Universe, Chaser, Virtual Console, MIDI, and Art Net.
```

## Recommended first implementation issue

```text
Add read only FixtureGroup topology inspector that prints Fixture ID, Head index, X/Y, universe, address, RGB channels, dimmer channel, and shutter channel.
```

## Hard rules

1. Do not rewrite engine first
2. Do not break `.qxw` compatibility
3. Do not remove existing QLC+ behavior before replacement exists
4. Do not change live output behavior without tests
5. Do not make lasers or strobes easier to trigger accidentally
6. Do not assume fixture topology is correct without inspection

## Practical first milestone

Milestone name:

```text
M1: Topology Trust
```

Milestone goal:

```text
QLC+ can clearly show how every fixture head maps to physical layout, matrix X/Y, and DMX output.
```

M1 files likely touched in future QLC+ fork:

```text
engine/src/fixturegroup.*
engine/src/fixture.*
engine/src/qlcfixturehead.*
engine/src/rgbmatrix.*
qmlui/fixturemanager.*
qmlui/rgbmatrixeditor.*
qmlui/fixturegroupeditor.*
```
