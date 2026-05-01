# QLC+ Source Map For Fork Planning

## Source areas to inspect

This is the initial source map for planning the future QLC+ Zero Hour fork.

Upstream source:

```text
mcallegari/qlcplus
```

## Core source areas

### `engine`

Primary runtime layer.

Expected responsibilities:

1. Workspace document model
2. Fixtures
3. Fixture groups
4. Functions
5. Scenes
6. Chasers
7. RGB Matrix
8. Master timer
9. Universes
10. Faders
11. HTP / LTP behavior
12. XML load and save

Fork relevance:

This is where topology, playback, phasers, recipes, timing, and output arbitration eventually connect.

High risk area.

### `fixtureeditor`

Fixture definition editing application.

Expected responsibilities:

1. `.qxf` authoring
2. Modes
3. Channels
4. Heads
5. Capabilities
6. Fixture metadata

Fork relevance:

Important for future fixture profile validation, head / emitter preview, and custom pixel bar workflows.

### `qmlui`

QLC+ 5 QML UI layer.

Expected responsibilities:

1. Modern UI surfaces
2. QML based editors
3. Fixture manager UI
4. RGB Matrix editor UI
5. Virtual Console UI pieces

Fork relevance:

Likely target for future EDM Performance UI and topology debug overlay if targeting QLC+ 5.

### `ui`

Legacy Qt widget UI layer.

Expected responsibilities:

1. Older editor surfaces
2. Monitor views
3. Legacy Virtual Console or editor paths

Fork relevance:

Useful for understanding existing monitor and editor behavior. Avoid major investment here unless supporting QLC+ 4 style UI is required.

### `plugins`

Input/output plugin system.

Expected responsibilities:

1. MIDI
2. Art Net
3. E1.31 / sACN
4. OSC
5. HID
6. USB DMX
7. OLA and other outputs

Fork relevance:

Target for Art Net diagnostics, APC Mini MK2 behavior if plugin level changes are needed, and future safety output warnings.

### `resources`

Bundled resources.

Expected responsibilities:

1. Fixture definitions
2. RGB scripts
3. Input profiles
4. Icons
5. Docs
6. UI resources

Fork relevance:

Important because APC Mini MK2 already has an input profile and RGB scripts are a no source rebuild extension path.

### `webaccess`

Web or remote access layer.

Fork relevance:

Potential later target for remote busking dashboard or emergency blackout control, but not a first pass fork target.

## Verified source anchors from first inspection

### `engine/src/doc.cpp`

`Doc` is the workspace root and owns major systems such as fixture definitions, RGB scripts, input/output cache, master timer, IO map, fixtures, fixture groups, palettes, functions, startup function, and operating mode.

Fork relevance:

Any major engine feature eventually touches `Doc` or must register with systems owned by `Doc`.

### `engine/src/fixturegroup.h` and `engine/src/fixturegroup.cpp`

`FixtureGroup` stores fixture heads in a coordinate map:

```cpp
QMap<QLCPoint, GroupHead> m_heads;
```

Fork relevance:

This is the direct topology model for matrix and visualizer behavior.

### `engine/src/fixture.h`

`Fixture` exposes fixture definition, fixture mode, channel count, head count, head lookup, RGB channels, CMY channels, master intensity, and generic RGB panel helpers.

Fork relevance:

This is the bridge between `.qxf` fixture definitions and runtime patched fixture behavior.

### `engine/src/qlcfixturehead.h`

`QLCFixtureHead` stores head channel membership and cached channel maps such as RGB, CMY, color wheels, and shutter channels.

Fork relevance:

This is central for emitter and pixel section correctness.

### `engine/src/rgbmatrix.h` and `engine/src/rgbmatrix.cpp`

`RGBMatrix` targets a `FixtureGroup`, runs an `RGBAlgorithm`, and maps matrix pixels into fixture head channels.

Fork relevance:

This is the closest existing QLC+ engine path to an MA3 style phaser system for pixel fixtures.

### `engine/src/universe.h`

`Universe` owns DMX universe data, Grand Master behavior, HTP/LTP capabilities, faders, blend modes, and output patching.

Fork relevance:

This is where playback layers are ultimately composed into DMX output.

### `engine/src/chaser.cpp` and `engine/src/chaserrunner.cpp`

`Chaser` and `ChaserRunner` implement step based function playback.

Fork relevance:

Useful for existing timing model, but not a true MA3 phaser equivalent.

### `resources/inputprofiles/Akai-APCMini-mk2.qxi`

APC Mini MK2 has an existing QLC+ input profile with sliders, buttons, feedback values, color table, and MIDI channel table.

Fork relevance:

Native APC Mini MK2 behavior should build on this, not replace it blindly.

## Source map conclusion

The first fork should not start by rewriting playback.

The first fork should expose and debug the existing topology path:

```text
FixtureDefinition / FixtureMode
-> Fixture
-> FixtureHead
-> FixtureGroup / QLCPoint
-> RGBMatrix map
-> Universe / GenericFader
-> Output plugin
```

That gives the Zero Hour GZ project immediate value and provides a foundation for MAtricks, phasers, recipes, and performance UI later.
