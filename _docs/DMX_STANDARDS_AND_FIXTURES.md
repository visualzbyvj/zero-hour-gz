# DMX Standards And Fixtures

> Purpose: practical protocol and fixture-definition reference for building reliable QLC+ showfiles.
> Scope: DMX512 basics, addressing, merge behavior, fixture profile guidance, and ring/pixel mapping considerations.

---

## DMX512 Fundamentals

### What a universe is

One DMX universe contains up to `512` address slots.

- addresses are `1-512`
- each slot is usually `8-bit` (`0-255`)
- a fixture consumes one or more consecutive slots

### Common protocol facts

- transport: RS-485 differential serial
- nominal speed: `250000` bits/sec
- common maximum slots per packet: `512`
- start code for normal lighting data: `0`

### Practical refresh behavior

There is no single magical "DMX refresh rate." Real refresh depends on:

- number of active slots transmitted
- interface quality
- controller implementation
- any network bridge in the path

Rules of thumb:

- full universes commonly land around `30-44 Hz`
- shorter universes can refresh faster
- cheap USB interfaces often jitter more than professional nodes

For visible motion and strobe consistency, stability matters as much as raw rate.

---

## Addressing Strategy

### Best practice

Use predictable address blocks rather than packing fixtures as tightly as possible.

Example strategy:

- small fixtures: allocate in blocks of `8`
- mid fixtures: allocate in blocks of `16`
- larger fixtures: allocate in blocks of `32`

That leaves room for:

- future mode changes
- fixture swaps
- easier troubleshooting

### Good addressing rules

- never let fixtures overlap
- keep identical fixtures in identical modes
- label universes physically and logically
- reserve spare space between fixture families
- keep pixel fixtures grouped contiguously when possible

---

## HTP vs LTP

### HTP

`Highest Takes Precedence`

Use HTP for:

- master dimmer
- intensity channels
- individual RGB emitter intensity channels in additive color systems

Why:

- multiple sources can contribute intensity safely
- lowering one fader does not unexpectedly black out another source if a stronger one is active

### LTP

`Latest Takes Precedence`

Use LTP for:

- pan / tilt
- color wheel and macros
- gobo
- prism
- shutter modes
- beam attributes
- effects and maintenance channels

Why:

- the latest command should fully replace the previous instruction

### Practical QLC+ implication

If a fixture profile assigns the wrong channel type, the whole console behaves wrong:

- grand master may not affect the expected channels
- color pickers may disappear
- scenes may merge badly
- blackout behavior can fail

---

## Common Channel Layouts

### RGB

Typical order:

| Address offset | Channel |
|---|---|
| 1 | Red |
| 2 | Green |
| 3 | Blue |

### RGBW

Typical order:

| Address offset | Channel |
|---|---|
| 1 | Red |
| 2 | Green |
| 3 | Blue |
| 4 | White |

### Dimmer + RGBW

Very common for stage fixtures:

| Address offset | Channel |
|---|---|
| 1 | Master dimmer |
| 2 | Red |
| 3 | Green |
| 4 | Blue |
| 5 | White |

### Dimmer + RGBW + extras

Typical extended layout:

| Address offset | Channel |
|---|---|
| 1 | Master dimmer |
| 2 | Red |
| 3 | Green |
| 4 | Blue |
| 5 | White |
| 6 | Strobe / shutter |
| 7 | Macro / mode |
| 8 | Speed / program |

### RGBWAUV

Typical order:

| Address offset | Channel |
|---|---|
| 1 | Red |
| 2 | Green |
| 3 | Blue |
| 4 | White |
| 5 | Amber |
| 6 | UV |

Manufacturer order varies. Always follow the fixture manual, not assumptions.

---

## 16-Bit Channels

Some fixtures expose fine resolution as coarse/fine pairs:

- coarse = MSB
- fine = LSB

Typical examples:

- pan coarse / pan fine
- tilt coarse / tilt fine
- dimmer coarse / dimmer fine

Use 16-bit channels when:

- movement needs to look smooth on camera
- tiny pan/tilt jumps are visible
- dimmer response needs fine resolution

---

## Strobe And Shutter Conventions

Common patterns:

- low range = shutter open or no strobe
- middle range = slow to fast strobe
- upper range = pulse, random strobe, or special effects

Some fixtures invert this completely. Never assume shared values across brands.

Operational advice:

- keep strobe on dedicated impact controls
- avoid hiding strobe in broad scene libraries
- clearly label "open shutter" versus "strobe enabled"

---

## Color Mixing Guidance

### RGB only

Best for:

- saturated colors
- bold effects
- pixel work

Weakness:

- white often looks cool or uneven

### RGBW

Best for:

- better white rendering
- pastels
- cleaner open looks

### RGBWAUV

Best for:

- broader palette
- warmth control
- UV moments

### Warm white / cool white channels

When present:

- use warm white for audience warmth and tungsten feel
- use cool white for icy, modern, or daylight looks
- blend carefully to avoid flat gray-looking output

---

## Fixture Profile Best Practices

### Before building or editing a profile

Confirm:

- exact manufacturer
- exact model
- exact mode name
- exact channel count
- exact DMX chart from the manual

### Channel typing matters

In QLC+, classify channels accurately:

- intensity channels as intensity
- RGB emitters as primary color channels
- color wheel/macro as color, not RGB emitters
- strobe as shutter
- mode/reset/fan as maintenance or similar utility type

### Defaults matter

Set safe defaults:

- open shutter when appropriate
- full master dimmer only if that is the normal operating state
- centered pan/tilt when meaningful
- no macro selected unless intended

Bad defaults create fixtures that boot into broken looks or refuse to output cleanly.

---

## QLC+ Fixture Definition Notes

### `.qxf` structure at a glance

A QLC+ fixture definition generally contains:

- creator metadata
- manufacturer and model
- fixture type
- channel pool definitions
- one or more modes
- optional heads
- physical data

### Good profile workflow

1. define the reusable channel pool correctly
2. create modes by selecting from that pool
3. assign heads only when the fixture truly has independent pixel/head control
4. validate the profile
5. test it with real hardware

### Common profile mistakes

- wrong channel type
- missing open-shutter value
- overlapping capability ranges
- incorrect defaults
- ignoring fine channels
- mixing multiple fixture modes in one rig

---

## Pixel Mapping And Rings

### Ring addressing

Pixel rings often work best when their pixels are contiguous in DMX:

- pixel 1 channels together
- pixel 2 channels together
- and so on

This makes:

- troubleshooting easier
- chasers easier
- RGBMatrix mapping easier

### Mapping a ring into a grid

QLC+ RGBMatrix thinks in grids, but a ring is circular. Common practical mapping choices:

- `1 x N`
  easiest for linear clockwise/counterclockwise motion
- `2 x N` or segmented groups
  useful for inner/outer ring pairings

For your workflow, linear group ordering is usually the most predictable choice for fill and marquee-style looks.

### Direction gotcha

Visual clockwise direction does not always match fixture-group order. Always test:

- wave left/right
- global forward/backward
- fill in both directions

Do not trust naming alone.

---

## Network DMX

### Art-Net

Widely supported and easy to find in mixed ecosystems.

Good for:

- flexible routing
- multiple nodes
- mixed software and hardware environments

### sACN

Also common in professional installs and scalable setups.

Good for:

- larger structured networks
- multicast-capable environments
- priority-aware networked output

### Practical advice

- keep show networks isolated when possible
- use quality nodes and switches
- document universe routing clearly
- avoid mystery adapters in live paths

---

## Recommended Rules For This Project

- Keep ring and panel pixels in clean contiguous groups.
- Maintain consistent fixture modes across identical units.
- Preserve correct HTP/LTP semantics through accurate channel typing.
- Use dedicated utility actions for blackout and stop-all.
- Treat white-ring output as a separate effect layer, not just "more brightness."
- Test visual direction physically after any group reorder.

---

## Quick Reference Tables

### BPM to quarter-note timing

| BPM | Quarter note |
|---|---:|
| 80 | 750 ms |
| 90 | 667 ms |
| 100 | 600 ms |
| 110 | 545 ms |
| 120 | 500 ms |
| 128 | 469 ms |
| 140 | 429 ms |

### Safe fixture-profile checklist

- right manual
- right mode
- right channel count
- right channel types
- right defaults
- right capability ranges
- validated
- hardware tested

---

## Cross-References

- `QLC_XML_FORMAT_REFERENCE.md`
- `QLC_VCMATRIX_AND_EFX.md`
- `QLC_SCRIPTING_AND_TIPS.md`
- `QLC_SOURCE_INDEX.md`
- `PRO_LIGHTING_WORKFLOWS.md`
