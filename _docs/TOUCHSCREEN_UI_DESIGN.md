# Touchscreen UI Design

> Purpose: practical touchscreen design rules for your QLC+ virtual console.
> Goal: a fast, low-error, GrandMA-style square-button layout that works in dark show conditions.

---

## Touch Target Standards

### Practical minimums

Common guidance across touch UI systems:

- absolute minimum: about `44 px`
- safer general target: `48 px`
- comfortable show-control target: `72-96 px`
- high-priority live controls: `96-120 px`

For a lighting console, you should bias larger than normal app UI because:

- the operator is moving fast
- the environment is dark
- the user may be standing
- accuracy drops under show pressure

### Recommended target sizes for your project

At `1920x1080` or larger:

- primary square buttons: `90-110 px`
- compact secondary squares: `72-88 px`
- safety buttons: `100-120 px`
- small status-only buttons: `56-72 px`

---

## Spacing And Margins

### Recommended spacing

- gap between related buttons: `4-8 px`
- gap between groups: `12-20 px`
- outer page margin: `12-24 px`
- padding inside button: `6-10 px`

### Why it matters

Tight spacing gives the "console" look, but zero spacing causes mis-taps. The sweet spot is:

- dense within a function block
- clearly separated between blocks

That is how you get the GrandMA-style visual density without sacrificing touch use.

---

## Layout Pattern

### Best pattern: modular square grid

Use a consistent square grid for:

- fixture selections
- colors
- FX families
- one-shot impacts
- page navigation

Then keep a right-side vertical utility lane for:

- speed dials
- master faders
- global overrides

### Good page structure

1. `Top row`
   page nav and high-level categories.
2. `Main grid`
   square button blocks by function.
3. `Right lane`
   sliders, speed controls, utility.
4. `Bottom lane`
   playback summary, bump row, or critical status.

This matches the console mental model better than scattering controls.

---

## Color Coding

### Suggested semantic colors

- `Intensity`: warm white / amber
- `Color`: actual chosen color
- `Position / motion`: cyan
- `Beam / gobo`: magenta
- `FX`: orange
- `Groups / selections`: blue-violet
- `Macros / utility`: teal or gray
- `Blackout / panic / all off`: red
- `Active`: brighter border or brighter fill
- `Selected`: yellow or white focus border

### Rule

Do not use color as the only state signal. Pair it with:

- border change
- caption change
- pressed state
- label/icon cue

This keeps the UI usable under stress and for color-deficient vision.

---

## Dark Theme Rules

### Base palette

Recommended dark neutrals:

- page background: `#121212`
- surface panel: `#1E1E1E`
- raised button rest state: `#252525`
- hover/armed state: `#333333`
- subtle divider: `#404040`
- primary text: `#E8E8E8`
- secondary text: `#A8A8A8`

### Avoid pure black everywhere

Pure black often feels dead and makes edges harder to read. A slightly lifted dark gray gives:

- clearer separation
- better border readability
- less harsh contrast

---

## Typography

### Recommended sizes

- main button label: `14-16 px`
- sublabel/value: `10-12 px`
- section heading: `16-18 px`
- compact button label: `12-14 px`

### Font rule

Prefer short labels over small fonts.

Bad:

- tiny text trying to fit long labels

Better:

- short labels like `ALL OFF`, `FULL BO`, `RING MX`, `PANEL FX`

---

## Feedback Rules

### Every touch should confirm quickly

A button tap should show visible feedback in under `100 ms`.

Suggested feedback:

- pressed scale or darker/lighter fill
- active border highlight
- latched state color change
- optional label or value update

### Distinguish states clearly

Each button should visually separate:

- rest
- pressed
- active/latched
- disabled
- selected/edit target

---

## GrandMA-Style Design Principles

What makes MA-style pages feel "right":

- square buttons
- repeated geometry
- tight gutters
- strong grouping
- consistent caption placement
- obvious active states
- separate utility strip
- minimal random alignment changes

What breaks that feel:

- mixed button shapes in the same block
- random button widths without purpose
- speed controls floating in the middle of content
- too many unique visual treatments on one page

---

## Recommended Layout Constants

These are practical constants for your current project direction:

```text
PAGE_MARGIN = 16
GROUP_GAP = 16
CELL_GAP = 6

SQ_LG = 100
SQ_MD = 88
SQ_SM = 76

RIGHT_LANE_W = 260 to 320
SLIDER_W = 56 to 72
SPEED_DIAL_W = 220 to 280

HEADER_H = 72
SECTION_LABEL_H = 24 to 32
BOTTOM_UTILITY_H = 110 to 140
```

### Suggested default

For your touchscreen-first pages, a good default is:

```text
SQ = 96
GAP = 6
GROUP_GAP = 16
MARGIN = 16
RIGHT_LANE_W = 280
```

That gives a dense but still finger-safe square grid on a `1920x1080` screen, and scales even better when page height is allowed to grow beyond `1080`.

---

## Page-Specific Guidance For Your Rig

### `PUNT`

Should prioritize:

- fixture selections
- core colors
- core ring / panel motion families
- right-lane masters and speed
- bottom-row safety and bumps

### `QUICK`

Good place for:

- secondary FX favorites
- combos
- specialty macros
- less-used panel variants

### `RING FX MATRIX`

Best kept as a large-control editor page:

- large VCMatrix widgets
- color picking
- algorithm selection
- one obvious speed dial

This page should feel like an editor, not a cluttered launchpad.

---

## Design Rules To Keep

- Keep all high-frequency buttons square.
- Keep the speed/master lane on the right.
- Use repeated group dimensions across pages.
- Keep safety actions visually isolated.
- Use a dark neutral base and colored functions.
- Avoid center-floating controls that break alignment.
- Favor fewer, larger controls over many tiny controls.

---

## Cross-References

- `GRANDMA_CONCEPTS_FOR_QLC.md`
- `PRO_LIGHTING_WORKFLOWS.md`
- `QLC_XML_FORMAT_REFERENCE.md`
- `QLC_SOURCE_INDEX.md`
