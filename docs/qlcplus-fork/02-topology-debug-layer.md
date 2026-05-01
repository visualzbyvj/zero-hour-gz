# Visualizer And Fixture Topology Debug Layer

## Recommended first fork feature

The first QLC+ source fork feature should be a topology debug layer.

Purpose:

```text
Make QLC+ show exactly how it understands fixture heads, emitters, matrix positions, patch order, and output channels.
```

This directly supports Zero Hour GZ because the current workflow depends heavily on visualizer trust and custom fixtures.

## Problem this solves

For pixel bars, ring layouts, lasers, strobes, and expanding fixture systems, QLC+ may output DMX correctly while still representing the fixture topology incorrectly.

Common failure modes:

1. Bar appears as two rows instead of one continuous physical line
2. Heads are assigned in the wrong order
3. Matrix effects skip sections
4. Fixture group X/Y does not match physical layout
5. Emitter order does not match the real fixture
6. Global dimmer gets confused with per head dimmer
7. RGB Matrix writes to the wrong head channels
8. Visualizer cannot explain what it is displaying

## Source path to expose

The debug layer should expose this path:

```text
FixtureDefinition
FixtureMode
Fixture
QLCFixtureHead
FixtureGroup
QLCPoint
GroupHead
RGBMatrix
Universe
OutputPatch
```

## Data to display

For every displayed head or matrix cell, show:

1. Fixture ID
2. Fixture name
3. Manufacturer
4. Model
5. Mode name
6. Universe
7. DMX address
8. Fixture channel range
9. Head index
10. Matrix X
11. Matrix Y
12. Group name
13. Group order
14. RGB channels
15. CMY channels
16. Dimmer channel
17. Master dimmer channel
18. Shutter or strobe channel
19. Current output value
20. Whether this head is inside or outside group bounds

## UI idea

Add a toggle called:

```text
Topology Debug Overlay
```

Possible locations:

1. Visualizer view
2. RGB Matrix preview
3. Fixture Group editor
4. Fixture Manager detail panel
5. New GZ Debug panel

## Overlay modes

### Minimal mode

Display only:

```text
Fixture ID / Head / X,Y
```

### Patch mode

Display:

```text
Universe / Address / Channel range
```

### Matrix mode

Display:

```text
Group X/Y / RGB Matrix pixel / Head index
```

### Channel mode

Display:

```text
R,G,B / Dimmer / Shutter channel numbers
```

### Output mode

Display:

```text
Current DMX values being written
```

## Zero Hour GZ use case

For OPPSK style bars:

1. Confirm whether each section is one head
2. Confirm whether the bar is one row or multiple rows
3. Confirm whether QLC+ wraps heads because group width is too small
4. Confirm if the visualizer is following fixture profile head order
5. Confirm if RGB Matrix is mapping X/Y correctly

For ring layouts:

1. Confirm clockwise order
2. Confirm counterclockwise order
3. Confirm top/right/bottom/left mapping
4. Confirm physical rotation per side
5. Confirm center out and mirror behavior

For lasers:

1. Confirm control channels are visible but not treated as RGB emitters unless intended
2. Clearly label safety critical channels
3. Separate visualizer behavior from live output assumptions

## Implementation sketch

Create a read only inspector first.

Do not change engine behavior in the first pass.

Potential internal helper:

```cpp
class GZTopologyInspector
{
public:
    QList<GZTopologyCell> inspectFixtureGroup(Doc* doc, quint32 groupId);
    QList<GZTopologyCell> inspectRGBMatrix(Doc* doc, quint32 matrixId);
};
```

Potential data object:

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
    int headIndex;
    int x;
    int y;
    QVector<quint32> rgbChannels;
    QVector<quint32> cmyChannels;
    quint32 masterDimmer;
    quint32 headDimmer;
    QVector<quint32> shutterChannels;
};
```

## Validation checklist

The feature is useful when it can answer:

1. Why is this bar wrapping into two rows?
2. Which head is section 1?
3. Which DMX channels are written when matrix cell X/Y lights up?
4. Which fixture group point maps to which real physical section?
5. Are any heads missing from the group?
6. Are any group points outside the matrix size?
7. Are RGB channels missing from any head?
8. Is a global dimmer being treated correctly?

## First implementation target

Start with a non invasive debug panel that reads current topology and prints a table.

Only after that works, add visual overlay labels.

## Do not do yet

1. Do not rewrite visualizer geometry
2. Do not change fixture group behavior
3. Do not change RGB Matrix output behavior
4. Do not change fixture profile loading
5. Do not change workspace XML format

Read first. Display first. Modify later.
