# GZ Phaser Engine Plan

## Purpose

The phaser engine is a later fork feature, not the first source change.

Goal:

```text
Create an MA3 inspired attribute phaser system for QLC+ that can run musical EDM effects across fixture groups using fixture order, phase offsets, timing, and attribute lanes.
```

## Why not first

A phaser engine depends on these foundations:

1. Fixture profiles must be accurate
2. Fixture heads must be correctly defined
3. Fixture groups must match physical topology
4. Selection transforms must be previewable
5. Output safety must be understood

Without those, a phaser engine will create complex wrong output.

## Existing QLC+ systems to study

1. `RGBMatrix`
2. `Chaser`
3. `ChaserRunner`
4. `Function`
5. `Scene`
6. `Universe`
7. `GenericFader`
8. `MasterTimer`

## Initial phaser scope

Start with:

1. Dimmer phasers
2. RGB color phasers
3. Shutter / strobe phasers where safe
4. Fixture order phase
5. Wings
6. Blocks
7. Groups
8. Speed source
9. BPM synced step timing
10. Preview before output

Do not start with every moving light attribute.

Later attributes:

1. Pan
2. Tilt
3. Zoom
4. Focus
5. Iris
6. Gobo
7. Prism
8. Laser pattern
9. Laser animation
10. Custom DMX channel lanes

## Conceptual model

```cpp
class GZPhaserFunction : public Function
{
public:
    void preRun(MasterTimer* timer) override;
    void write(MasterTimer* timer, QList<Universe*> universes) override;
    void postRun(MasterTimer* timer, QList<Universe*> universes) override;
};
```

```cpp
struct GZPhaserLane
{
    QString attributeFamily;
    QVector<GZPhaserStep> steps;
    QString blendMode;
};
```

```cpp
struct GZPhaserStep
{
    double phase;
    double width;
    double value;
    QString curve;
};
```

## Key design rule

A phaser should use fixture group topology and selection transforms, not raw fixture IDs only.

Flow:

```text
FixtureGroup
-> SelectionEngine transform
-> Phase distribution
-> Attribute lane calculation
-> Universe fader output
```

## EDM use cases

1. Bass slam dimmer wave
2. Ring spin color phaser
3. Mirror wing red / white pulse
4. Build riser brightness wave
5. Drop hit strobe burst
6. Slow atmospheric breakdown pulse
7. Column chase across OPPSK bars
8. Center out explosion

## Safety rules

1. Strobe phasers must be safety classified
2. Laser phasers must default to visualizer safe assumptions
3. Full white / blinder phasers must not latch casually
4. Panic and blackout must override all phasers
5. Dry run / preview mode must exist before live output testing

## Success definition

The first useful phaser engine can:

1. Target a FixtureGroup
2. Use a SelectionEngine transform
3. Apply a dimmer or RGB wave
4. Phase across fixture order
5. Sync to a speed or BPM source
6. Preview output mapping
7. Save/load safely
8. Stop cleanly
9. Respect blackout/panic
