# QLC+ Zero Hour Fork Vision

## Purpose

This folder defines a planning package for a future QLC+ source fork focused on Zero Hour GZ and EDM busking workflows.

The goal is not to copy grandMA3 blindly.

The goal is to build MA3 inspired systems into or around QLC+ where they directly improve:

1. Fixture topology trust
2. Visualizer accuracy
3. Custom fixture authoring
4. APC Mini MK2 live control
5. EDM busking speed
6. Art Net output safety
7. Laser, strobe, and blinder safety
8. Future fixture expansion

## Active upstream target

Upstream source:

```text
https://github.com/mcallegari/qlcplus
```

Current project repository:

```text
https://github.com/visualzbyvj/zero-hour-gz
```

Future fork repository name recommendation:

```text
visualzbyvj/zero-hour-qlcplus
```

or

```text
visualzbyvj/qlcplus-zero-hour-fork
```

## Fork principle

Do not start with a full engine rewrite.

Start with visibility and safety.

The current project bottleneck is not only creative capability. The bottleneck is whether QLC+ accurately understands and exposes the physical fixture topology:

```text
fixture profile -> fixture mode -> heads / emitters -> fixture group X/Y -> RGB Matrix map -> Universe output
```

If that chain is wrong, then phasers, recipes, MAtricks style selection, executor pages, and MIDI control all inherit wrong behavior.

## Recommended fork order

1. Source map and build verification
2. Visualizer / fixture topology debug overlay
3. Fixture profile validator and editor improvements
4. APC Mini MK2 native feedback layer
5. MAtricks style selection engine
6. Phaser engine
7. Recipe system
8. EDM performance UI
9. Playback / engine rewrite

## Non goals for the first fork pass

Do not begin with:

1. Full MA3 clone
2. Full phaser clone
3. Full engine rewrite
4. Full UI replacement
5. Workspace format replacement
6. Breaking existing QLC+ showfile compatibility

## Success definition

The first successful fork feature should make it obvious how QLC+ is interpreting every controllable fixture part.

For any RGB Matrix or visualizer mapped group, the operator should be able to see:

1. Fixture ID
2. Fixture name
3. Fixture mode
4. Universe
5. Address
6. Head index
7. Matrix X/Y
8. Group order
9. RGB channels
10. Dimmer channel
11. Shutter or strobe channel
12. Output value when active

This directly supports the Zero Hour GZ workflow and future rig expansion.
