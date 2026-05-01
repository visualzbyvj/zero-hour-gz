# MAtricks Style Selection Engine

## Purpose

The fourth recommended QLC+ fork feature is a MAtricks style selection engine.

The goal is not to copy grandMA3 syntax.

The goal is to give QLC+ a reusable way to transform fixture and head order for EDM effects, RGB Matrix behavior, phasers, recipes, and visualizer layout checks.

## Why this matters for Zero Hour GZ

The rig uses physical patterns where order matters:

1. Pixel bars
2. 16 section fixtures
3. Emitter columns
4. Ring layouts
5. Clockwise and counterclockwise sweeps
6. Left / right symmetry
7. Top / bottom symmetry
8. Center out effects
9. Odd / even hits
10. Build and drop patterns

QLC+ already has Fixture Groups with X/Y positions. A selection engine should build on that instead of replacing it.

## Core concepts

A selection engine should transform fixture heads by:

1. Order
2. Reverse order
3. Wings
4. Blocks
5. Groups
6. Odd / even
7. Mirror
8. Rows
9. Columns
10. Ring clockwise
11. Ring counterclockwise
12. Inside out
13. Outside in
14. Physical quadrant
15. Custom topology tag

## Data model sketch

```cpp
class GZSelectionEngine
{
public:
    GZSelectionResult apply(const FixtureGroup* group, const GZSelectionTransform& transform);
};
```

```cpp
struct GZSelectionTransform
{
    int wings;
    int blocks;
    int groups;
    bool reverse;
    bool mirror;
    bool oddOnly;
    bool evenOnly;
    QString orderMode;
};
```

```cpp
struct GZSelectionCell
{
    quint32 fixtureId;
    int headIndex;
    int sourceX;
    int sourceY;
    int outputIndex;
    int phaseIndex;
    QString groupTag;
};
```

## First supported transforms

Start small:

1. Natural order
2. Reverse
3. Odd
4. Even
5. Wings 2
6. Blocks
7. Mirror center
8. Rows
9. Columns
10. Ring clockwise
11. Ring counterclockwise

Do not implement every grandMA3 MAtricks feature in the first pass.

## Integration targets

The selection engine should eventually feed:

1. Topology debug overlay
2. RGB Matrix preview
3. Future phaser engine
4. Future recipe engine
5. Fixture group editor
6. Visualizer debug tools
7. Showfile builders

## Zero Hour GZ examples

### Ring clockwise

Take ring fixture heads and output them in physical clockwise order.

### Ring split wings

Top and bottom, or left and right, mirror from center.

### Column slam

Treat each vertical emitter column as one ordered selection unit.

### Odd / even strobe split

Alternate sections for high energy but controlled strobe effects.

## Safety and scope

This engine should not change fixture patching.

This engine should not renumber fixtures.

This engine should not change DMX addresses.

This engine should be a transform layer over existing fixture group topology.

## Success definition

The selection engine is successful when the user can preview:

1. Original fixture group order
2. Transformed order
3. Phase index per fixture head
4. Physical X/Y mapping
5. Whether the transform matches the intended rig layout

This must be visible before it drives live output.
