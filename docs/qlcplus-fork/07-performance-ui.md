# GZ Performance UI Plan

## Purpose

The performance UI is a later QLC+ fork feature focused on live EDM busking.

It should not replace the entire QLC+ UI in the first pass.

It should add a focused performance mode that makes QLC+ easier to operate under live pressure.

## Primary goals

1. Fast live triggering
2. Clear active state visibility
3. APC Mini MK2 feedback alignment
4. Safety state visibility
5. Speed / BPM visibility
6. Fixture group visibility
7. Visualizer topology debug access
8. No accidental live output mistakes

## Recommended UI sections

### Master and safety strip

Always visible:

1. Grand Master
2. Blackout
3. Panic
4. Output arm state
5. Laser arm state
6. Strobe arm state
7. Blinder arm state
8. Art Net output status

### Executor grid

MA3 inspired but QLC+ realistic.

Controls:

1. Flash
2. Toggle
3. Temp
4. Latch
5. Group exclusive
6. Kill group
7. Release fade

### Page / bank view

Pages:

1. Masters and safety
2. Base looks
3. Colors
4. Drops
5. Builds
6. Strobes / blinders
7. Pixel FX
8. Lasers
9. Speed
10. Utilities

### Speed and timing panel

Controls:

1. BPM
2. Tap tempo
3. Half time
4. Double time
5. Freeze
6. Speed master 1
7. Speed master 2
8. Effect family rate

### Topology debug panel

Quick access to:

1. FixtureGroup map
2. Head index overlay
3. Matrix X/Y overlay
4. Universe / address overlay
5. RGB / dimmer / shutter channels

### APC state panel

Show:

1. Connected status
2. Current bank
3. Shift state
4. LED feedback mode
5. Dangerous active controls
6. Fader pickup state if implemented

## UI architecture direction

If targeting QLC+ 5, prefer QML UI integration.

Additive first:

```text
New GZ Performance Mode panel
```

Do not delete existing QLC+ views.

## What not to do first

1. Do not replace the entire UI
2. Do not hide existing QLC+ editors
3. Do not require Zero Hour GZ hardware for normal QLC+ operation
4. Do not make live output easier to trigger accidentally
5. Do not remove current Virtual Console behavior before replacement is proven

## Success definition

The UI is successful when the operator can see and control:

1. What is active
2. What is armed
3. What is dangerous
4. What page is selected
5. What BPM/speed is active
6. What fixtures are being affected
7. How to panic or blackout instantly

without digging through editor windows during a live set.
