# QLC+ Zero Hour Fork Implementation Briefs

## Purpose

This file converts the fork roadmap into implementation ready briefs.

These are not generic ideas. They are the first source level fork modules to build after a real QLC+ fork exists.

Current planning repo:

```text
visualzbyvj/zero-hour-gz
```

Expected future QLC+ fork:

```text
visualzbyvj/zero-hour-qlcplus
```

Upstream source:

```text
mcallegari/qlcplus
```

## Implementation rule

Do not start by rewriting QLC+.

Build additive fork modules first.

Every fork module must be:

1. Readable
2. Reversible
3. Testable
4. Disabled by default when possible
5. Compatible with normal QLC+ behavior
6. Safe around live output
7. Useful for Zero Hour GZ

---

# Fork 1: GZ Topology Inspector

## Goal

Add a read only topology inspector that exposes how QLC+ maps fixture heads, fixture group X/Y positions, RGB Matrix cells, and output channels.

## Why first

This directly solves the recurring Zero Hour problem:

```text
Does QLC+ understand my physical rig layout the same way I do?
```

## Source areas

Inspect and likely touch:

```text
engine/src/fixturegroup.h
engine/src/fixturegroup.cpp
engine/src/fixture.h
engine/src/fixture.cpp
engine/src/qlcfixturehead.h
engine/src/qlcfixturehead.cpp
engine/src/rgbmatrix.h
engine/src/rgbmatrix.cpp
qmlui/rgbmatrixeditor.*
qmlui/fixturemanager.*
qmlui/fixturegroupeditor.*
```

## Additive source design

Create a small inspector module first.

Suggested files:

```text
engine/src/gztopologycell.h
engine/src/gztopologycell.cpp
engine/src/gztopologyinspector.h
engine/src/gztopologyinspector.cpp
```

Suggested data model:

```cpp
struct GZTopologyCell
{
    quint32 fixtureId;
    QString fixtureName;
    QString manufacturer;
    QString model;
    QString modeName;

    quint32 universe;
    quint32 address;
    quint32 channelStart;
    quint32 channelEnd;

    int headIndex;
    int matrixX;
    int matrixY;
    int groupOrder;

    QVector<quint32> rgbChannels;
    QVector<quint32> cmyChannels;
    QVector<quint32> shutterChannels;

    quint32 masterDimmerChannel;
    quint32 headDimmerChannel;

    bool hasRGB;
    bool hasDimmer;
    bool hasShutter;
    bool isValid;
    QStringList warnings;
};
```

Suggested inspector API:

```cpp
class GZTopologyInspector
{
public:
    static QList<GZTopologyCell> inspectFixtureGroup(const Doc* doc, quint32 groupId);
    static QList<GZTopologyCell> inspectRGBMatrix(const Doc* doc, quint32 matrixId);
    static QString toMarkdownTable(const QList<GZTopologyCell>& cells);
};
```

## First implementation behavior

Start with a non UI debug output.

Minimum useful command / panel output:

```text
Group: OPPSK Ring
X,Y | Fixture ID | Head | Universe | Address | RGB | Dimmer | Shutter | Warnings
```

## Validation tests

Create test cases for:

1. One fixture with one head
2. One fixture with 8 heads
3. One fixture with 16 heads
4. Fixture group width smaller than head count
5. Fixture group with skipped points
6. RGB Matrix targeting a group with missing RGB channels
7. Master dimmer only fixture
8. Per head RGB fixture

## Done when

The inspector can answer:

1. Which fixture head is at matrix X/Y?
2. Which DMX address does it write to?
3. Which channels are RGB?
4. Which channel is dimmer?
5. Why is a cell invalid or incomplete?
6. Is the layout wrapping because of fixture group size?

---

# Fork 2: GZ Fixture Profile Validator

## Goal

Add validation for `.qxf` fixture profiles and fixture modes, focused on multi head fixtures, pixel bars, lasers, strobes, and RGB Matrix compatibility.

## Source areas

Inspect and likely touch:

```text
engine/src/qlcfixturedef.*
engine/src/qlcfixturemode.*
engine/src/qlcfixturehead.*
engine/src/qlcchannel.*
fixtureeditor/*
qmlui/fixturemanager.*
```

## Suggested files

```text
engine/src/gzfixturevalidationreport.h
engine/src/gzfixturevalidationreport.cpp
engine/src/gzfixtureprofilevalidator.h
engine/src/gzfixtureprofilevalidator.cpp
```

## Validation report model

```cpp
enum class GZValidationSeverity
{
    Info,
    Warning,
    Error,
    SafetyWarning,
    MatrixWarning,
    VisualizerWarning
};

struct GZFixtureValidationMessage
{
    GZValidationSeverity severity;
    QString code;
    QString message;
    QString modeName;
    int channelIndex;
    int headIndex;
};
```

## Validator API

```cpp
class GZFixtureProfileValidator
{
public:
    static GZFixtureValidationReport validateDefinition(const QLCFixtureDef* def);
    static GZFixtureValidationReport validateMode(const QLCFixtureMode* mode);
};
```

## Required checks

### Generic checks

1. Missing manufacturer
2. Missing model
3. Missing fixture type
4. Mode has zero channels
5. Mode channel count mismatch
6. Duplicate channel names
7. Capability range gaps
8. Capability range overlaps

### Head checks

1. No heads defined for multi cell fixture
2. Head has no channels
3. Same channel assigned unexpectedly across multiple heads
4. Head has RGB but no dimmer path
5. Head has dimmer but no color path
6. Head order appears non sequential

### Matrix checks

1. RGB Matrix target mode has no RGB/CMY channels
2. Some heads have RGB and others do not
3. Master dimmer is present but per head dimmer is missing
4. Global channels are assigned to a single head when they should be global

### Safety checks

1. Channel name includes reset but is not safety flagged
2. Channel name includes laser but mode has no safety warning
3. Strobe channel exists but is not clearly labeled
4. Full output / blinder behavior is unclear

## Done when

The validator can explain why a fixture profile is likely to break:

1. RGB Matrix
2. Visualizer layout
3. Fixture group topology
4. Laser safety
5. Strobe safety
6. Multi emitter layout

---

# Fork 3: GZ APC Mini MK2 Feedback Layer

## Goal

Build smarter APC Mini MK2 feedback for live EDM busking.

QLC+ already has an APC Mini MK2 input profile. The fork should not replace it. It should add performance state logic.

## Source areas

Inspect and likely touch:

```text
resources/inputprofiles/Akai-APCMini-mk2.qxi
engine/src/qlcinputprofile.*
plugins/midi/*
qmlui/virtualconsole/*
engine/src/function.*
```

## Suggested files

```text
engine/src/gzfeedbackstate.h
engine/src/gzfeedbackstate.cpp
qmlui/virtualconsole/gzapcfeedbackcontroller.h
qmlui/virtualconsole/gzapcfeedbackcontroller.cpp
```

## Feedback concepts

```text
Off = inactive
Green = safe active layer
Yellow = effect or speed layer
Red = danger layer
Blinking red = high risk active or armed
White = selected utility or page
Blue = atmospheric or breakdown layer
Purple = laser / special FX layer
```

## Function safety classes

Add metadata or mapping for:

```text
Safe
Effect
Speed
HighIntensity
Strobe
Laser
Blinder
Blackout
Panic
Utility
```

## First implementation

Do not create a complete controller abstraction first.

Start by making Virtual Console feedback more informative for APC buttons:

1. Active function state
2. Button type
3. Safety class
4. Page state
5. Danger active state

## Done when

The APC Mini MK2 can visually show:

1. Active looks
2. Active effects
3. Dangerous armed states
4. Current page or bank
5. Blackout / panic visibility

---

# Fork 4: GZ Selection Engine

## Goal

Add MAtricks inspired fixture/head ordering transforms.

This should be a transform layer over FixtureGroup topology, not a replacement for FixtureGroup.

## Source areas

Inspect and likely touch:

```text
engine/src/fixturegroup.*
engine/src/rgbmatrix.*
engine/src/function.*
qmlui/fixturegroupeditor.*
qmlui/rgbmatrixeditor.*
```

## Suggested files

```text
engine/src/gzselectioncell.h
engine/src/gzselectioncell.cpp
engine/src/gzselectiontransform.h
engine/src/gzselectiontransform.cpp
engine/src/gzselectionengine.h
engine/src/gzselectionengine.cpp
```

## Selection cell

```cpp
struct GZSelectionCell
{
    quint32 fixtureId;
    int headIndex;
    int sourceX;
    int sourceY;
    int outputIndex;
    int phaseIndex;
    QString tag;
};
```

## First transforms

1. Natural order
2. Reverse
3. Odd only
4. Even only
5. Wings 2
6. Blocks
7. Groups
8. Mirror center
9. Rows
10. Columns
11. Ring clockwise
12. Ring counterclockwise

## Done when

A fixture group can be transformed and previewed without changing patching or addresses.

---

# Fork 5: GZ Phaser Engine

## Goal

Add an MA3 inspired phaser function type after topology and selection are stable.

## Source areas

Inspect and likely touch:

```text
engine/src/function.*
engine/src/rgbmatrix.*
engine/src/chaser.*
engine/src/scene.*
engine/src/universe.*
engine/src/genericfader.*
engine/src/mastertimer.*
```

## Suggested files

```text
engine/src/gzphaserfunction.h
engine/src/gzphaserfunction.cpp
engine/src/gzphaserlane.h
engine/src/gzphaserlane.cpp
engine/src/gzphaserstep.h
engine/src/gzphaserstep.cpp
```

## First phaser scope

1. Dimmer wave
2. RGB color wave
3. Fixture order phase
4. Wings
5. Blocks
6. Speed source
7. BPM source
8. Preview before output

## Do not include first

1. Full moving head position engine
2. Gobos
3. Prism
4. Complex 3D effects
5. Deep engine rewrite

## Done when

The phaser can target a FixtureGroup, use SelectionEngine ordering, calculate phased dimmer or RGB values, and write safely through Universe faders while respecting blackout and stop behavior.

---

# Fork 6: GZ Recipe Engine

## Goal

Create reusable busking looks from ingredients instead of manually building duplicate QLC+ functions.

## First implementation path

Build externally first in Zero Hour GZ builders.

Only integrate into QLC+ source after the recipe model is stable.

## Recipe model

```yaml
name: Drop Red Blast
target: Ring_All
layers:
  - type: dimmer
    value: 255
  - type: color
    value: red
  - type: phaser
    ref: bass_slam
playback: flash
safety: high_intensity
midi: apc.row1.col1
```

## Native fork target later

```text
engine/src/gzrecipe.*
engine/src/gzrecipeengine.*
qmlui/gzrecipeeditor.*
```

## Done when

A recipe can generate or instantiate:

1. Scene
2. Chaser
3. Phaser
4. Collection
5. Executor
6. VC control
7. MIDI mapping
8. Safety metadata

---

# Fork 7: GZ Performance UI

## Goal

Add a performance first QML panel for EDM busking.

## Source areas

Inspect and likely touch:

```text
qmlui/*
qmlui/virtualconsole/*
engine/src/function.*
engine/src/doc.*
plugins/midi/*
plugins/artnet/*
```

## First UI panels

1. Master / safety strip
2. Executor grid
3. Speed and BPM panel
4. APC state panel
5. Topology debug panel
6. Art Net output status

## Done when

The operator can see and control live state without digging through editor windows.

---

# Implementation order

Build in this order:

```text
1. GZ Topology Inspector
2. GZ Fixture Profile Validator
3. GZ APC Feedback Layer
4. GZ Selection Engine
5. GZ Phaser Engine
6. GZ Recipe Engine
7. GZ Performance UI
8. Engine rewrite only after all above are proven
```

## Absolute hard stop

Do not perform a full engine rewrite until:

1. Upstream QLC+ builds cleanly
2. Test workspaces exist
3. Topology inspector exists
4. Fixture validator exists
5. Selection engine exists
6. Phaser prototype exists
7. Existing `.qxw` files still load
8. Blackout and Grand Master behavior are verified
9. Art Net output behavior is verified
