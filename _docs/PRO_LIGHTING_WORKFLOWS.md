# Professional Lighting Workflows — Busking Knowledge Cache

> Compiled from professional sources, community forums (QLC+, MA Lighting, ControlBooth),
> industry articles (CHAUVET Professional, Harman/Martin, Lighting & Sound America),
> and experienced operators. Optimized for QLC+ busking with LED rings, wash bars,
> and RGB matrix panels.

---

## Table of Contents

1. [Busking Fundamentals](#1-busking-fundamentals)
2. [Color Theory for Stage Lighting](#2-color-theory-for-stage-lighting)
3. [Beat-Sync and Timing](#3-beat-sync-and-timing)
4. [Effect Layering and Stacking](#4-effect-layering-and-stacking)
5. [Console Layout Philosophy](#5-console-layout-philosophy)
6. [Quick-Access Strategies](#6-quick-access-strategies)
7. [Creative Effect Ideas (LED Rings, Wash Bars, Matrices)](#7-creative-effect-ideas)
8. [Cue Structure and Organization](#8-cue-structure-and-organization)
9. [Community Tips (Reddit / Forum Wisdom)](#9-community-tips)
10. [BPM-to-Duration Conversion Tables](#10-bpm-to-duration-conversion-tables)

---

## 1. Busking Fundamentals

### What Is Busking?

Busking (also called "punting" or "winging it") is controlling live stage lighting in real-time response to a show, rather than relying on pre-recorded cues. The operator "plays" the lighting rig like a musical instrument, making decisions on the fly. Common in concerts, clubs, festivals, corporate events, and any situation where the exact performance cannot be predicted in advance.

*— Brad Schiller, "The Basics of Busking," Lighting & Sound America, Dec 2024*

### The Core Philosophy

> "You cannot simply start with an empty console. You will need playbacks and other tools at the ready, enabling you to create improvisational lighting looks as you respond to the action happening on stage."

Busking is **not** "winging it from scratch." It is **live remixing of well-prepared building blocks.** The preparation happens before the show; the creativity happens during it.

### The Seven Pillars of Busking

#### 1. Know Your Controller
Your console/software is your primary instrument. You must know your patch, your layout, where every button and fader lives, and how to navigate without looking. In QLC+, this means your Virtual Console layout, MIDI mappings, and frame pages.

#### 2. Know Your Rig
Understand every fixture's capabilities, color mixing method (RGB vs RGBW vs CMY), DMX channel layout, and physical position. Know which fixtures have white LEDs and which don't. Know where everything is patched.

#### 3. Know the Expectations
Ask the client/band/event organizer what they expect. Get a playlist if possible. Understand the audience demographic. Build your preset library to match.

#### 4. Remain Flexible and Relaxed
Tension kills creativity. If you've done the preparation, trust your instincts and flow with the show. Anticipate what's coming next rather than reacting after the fact.

#### 5. The "Punt Look" (Get-Out-of-Jail-Free Card)
**Always** have a safety cue on a dedicated, easy-to-find button. This look should:
- Keep the stage lit (never go black accidentally)
- Have no movement or effects
- Be as neutral as possible
- Reset chases, effects, and cue stacks
- Mark it with glow tape or a distinct color on your MIDI controller

*— Mike Graham, CHAUVET Professional*

#### 6. Repetition Is Your Friend
Audiences connect with recurring visual motifs. If you create a yellow audience ballyhoo with a cone gobo during the first chorus, repeat that same look when the chorus returns. This creates visual coherence and emotional payoff.

#### 7. Practice Constantly
Sit with your rig (or a visualizer) and play back to random music:
- 30 minutes on music you know (warm-up)
- 30 minutes on random music you've never heard (the real training)
- Practice builds muscle memory and develops your improvisational instincts

*— Brad Schiller, Lighting & Sound America*

### Busking vs Timecode: When to Use What

| Scenario | Approach | Why |
|----------|----------|-----|
| Headliner with fixed setlist | Timecode | Precision, repeatability, complex sync |
| Improvisational DJ set | Busk | Music changes on a whim |
| B2B DJ session | Busk | Two artists, zero predictability |
| Corporate with surprise band | Busk | No rehearsal time, no setlist |
| Mid-size/side festival stages | Busk | Budget/time constraints |
| Complex multi-element production | Timecode + Busk hybrid | Base on timecode, accents busked |

**Hybrid Approach (Best of Both Worlds):** Run the base show on timecode or pre-programmed sequences, but keep live control over certain fixtures or effects on top. If sync is lost, the operator can seamlessly take over.

### The Busking Mindset

- **Build** from intro to verse to chorus to bridge to finale (like a musician)
- **Don't** fire everything for every song — use restraint, save your big looks
- **Count beats** — most music is in 4/4, changes happen every 4 or 8 bars
- **Watch the performer** not the console — read their body language
- **Watch the crowd** — adjust intensity and energy to match their response
- **Own your mistakes** — hit the punt look, breathe, rebuild

﻿---

## 2. Color Theory for Stage Lighting

### The Additive Color Model (RGB)

Stage lighting uses **additive color mixing** (RGB), not subtractive (like paint). Overlapping red, green, and blue at full intensity produces white.

**Primary Colors:** Red, Green, Blue
**Secondary Colors:** Cyan (G+B), Magenta (R+B), Yellow (R+G)

### Color Temperature

| Range | Description | Feeling |
|-------|-------------|---------|
| 1800-2400K | Candlelight, deep amber | Extreme warmth, intimacy |
| 2700-3000K | Warm white, tungsten | Comfort, familiarity |
| 3500-4000K | Neutral warm | Natural, balanced |
| 4000-5000K | Neutral | Clean, professional |
| 5000-6500K | Daylight, cool white | Clarity, alertness |
| 7000K+ | Blue-white | Cold, sterile, moonlight |

### Color-Emotion Map

| Color | Emotion / Association | Best Use |
|-------|----------------------|----------|
| **Red** | Power, passion, urgency, danger | Climaxes, high-energy moments, rock. Use sparingly — visual fatigue |
| **Deep Red** | Weight, intensity | Heavy emotional scenes, dramatic tension |
| **Orange** | Energy, warmth, excitement | Upbeat moments, transitions to high energy |
| **Amber** | Comfort, nostalgia, soft warmth | Acoustic sets, ballads, golden hour feels |
| **Yellow** | Optimism, happiness, attention | Bright uplifting moments. Avoid on skin — unflattering |
| **Green** | Nature, renewal, unease | Environmental themes. Blend toward yellow/blue. Avoid heavy washes on performers |
| **Cyan** | Cool freshness, technology | EDM, futuristic vibes, transitions |
| **Blue** | Calm, mystery, sadness, isolation | Breakdowns, slow songs. Pairs with haze for dreamlike effects |
| **Deep Blue** | Depth, introspection | Slow ballads, ambient moments |
| **Purple/Violet** | Creativity, luxury, spirituality | Transitions, reveals, imaginative scenes |
| **Magenta/Pink** | Romance, playfulness, pop energy | Pop music, celebrations, dance segments |
| **White** | Clarity, focus, purity | Face lighting, visibility, neutral reset |

### Color Pairing Strategies

#### Complementary (Opposite on Color Wheel)
Maximum contrast and visual tension. High drama.
- Blue + Orange (the cinematic classic)
- Red + Cyan
- Green + Magenta
- Purple + Yellow

#### Analogous (Neighbors on Color Wheel)
Smooth, unified, harmonious looks.
- Blue, Cyan, Green
- Red, Orange, Yellow
- Purple, Magenta, Red

#### Triadic (Three Colors at 120 degree Intervals)
Balanced variety with dynamic tension: Red/Green/Blue or Cyan/Magenta/Yellow

### The 3-Layer Color Method

| Layer | Purpose | Example |
|-------|---------|---------|
| **Base** | Performer visibility, natural skin tones | Neutral or slightly warm white |
| **Middle** | Atmosphere and mood | Main color wash (blue for calm, red for intensity) |
| **Top** | Accents, highlights, drama | Sharp beam, rotating gobo, contrasting color splash |

### Temperature Mapping (The 60/40 Rule)

Layer **60% warm front light** with **40% cool backlight** to create three-dimensional depth and natural-looking separation between performers and background.

### Proven Color Recipes

| Recipe Name | Colors | Mood / Use |
|-------------|--------|------------|
| **Neo-Dream** | Teal + Purple | Futuristic, immersive — EDM, synth |
| **Royal Ember** | Red + Gold | Regal, dramatic — ceremonies, finales |
| **Solar Chill** | Ice Blue + White | Crisp, elegant — ambient, winter |
| **Sunset Punch** | Blue + Orange | Cinematic contrast — storytelling, dance |
| **Blossom Haze** | Pink + Lavender | Soft, whimsical — ballads, dreamy |
| **Neon Nights** | Magenta + Cyan | High energy — EDM drops, club vibes |
| **Deep Forest** | Green + Amber | Organic, earthy — acoustic, folk |
| **Midnight Fire** | Deep Blue + Red | Intense duality — rock, metal |
| **Ice Storm** | White + Cyan + Blue | Cold, aggressive — heavy bass drops |
| **Golden Hour** | Amber + Warm White | Intimate warmth — singer-songwriter |

### Genre-Specific Color Palettes

| Genre | Primary Colors | Approach |
|-------|---------------|----------|
| **Rock** | Deep reds, oranges, amber, white strobes | High contrast, aggressive, sharp transitions |
| **Pop** | Pink, teal, purple, magenta | Bright, saturated, playful transitions |
| **EDM/House** | Cyan, magenta, purple, UV | Beat-synced, saturated, rainbow chases |
| **Hardstyle/Techno** | Red, white, blue strobes | Aggressive, fast, high-contrast |
| **Trance** | Blue, purple, cyan, lavender | Sweeping, euphoric, gradual builds |
| **Hip-Hop/R&B** | Red, amber, gold, white | Warm, spotlight-focused, slow fades |
| **Jazz/Acoustic** | Amber, warm white, deep blue | Subtle, warm, minimal movement |
| **Metal** | Red, green, white, black (absence) | Harsh, fast strobes, aggressive movement |
| **Country** | Amber, gold, warm white | Natural warmth, minimal effects |
| **Corporate** | Cool blue, neutral white | Clean, professional, brand-consistent |

### Color Mistakes to Avoid

- **Over-saturation everywhere** — keep some neutral zones for contrast
- **Too many hues at once** — stick to 2-3 per scene, 5 max in palette
- **Heavy green wash on skin** — makes performers look sick
- **Abrupt color changes without motivation** — program smooth fades
- **Same color on backdrop AND performer** — lose separation, flatten the scene

﻿---

## 3. Beat-Sync and Timing

### The Master Formula

```
Milliseconds per Beat = 60,000 / BPM
```

This single formula is the foundation of all beat-synced lighting.

### Musical Structure for Lighting Operators

Most popular music follows predictable structures:

```
INTRO > VERSE > PRE-CHORUS > CHORUS > VERSE > CHORUS > BRIDGE > CHORUS > OUTRO
```

**Key principle:** Changes in lighting should align with changes in musical structure. Verses are calmer, choruses are bigger, bridges are different, drops are explosive.

### Beat Divisions

| Division | Name | Formula | Use |
|----------|------|---------|-----|
| 1/1 | Whole note (1 bar in 4/4) | (60000/BPM) x 4 | Slow sweeps, full color transitions |
| 1/2 | Half note | (60000/BPM) x 2 | Moderate movements, wash fades |
| 1/4 | Quarter note (1 beat) | 60000/BPM | Standard chase speed, beat-locked effects |
| 1/8 | Eighth note | 60000/BPM/2 | Faster chases, bumps |
| 1/16 | Sixteenth note | 60000/BPM/4 | Fast strobes, rapid chases |
| 1/32 | Thirty-second note | 60000/BPM/8 | Extreme strobes (DMX limit warning) |
| Dotted 1/4 | Dotted quarter | (60000/BPM) x 1.5 | Shuffled/swung timing |
| Triplet 1/8 | Eighth triplet | (60000/BPM) / 1.5 | Triplet feels, waltz timing |

### DMX Refresh Rate Constraints

- Standard DMX refresh rate: **~25-44 Hz** (one frame every 23-40ms)
- Many controllers throttle to **25 Hz** (40ms per frame) for compatibility
- **Practical minimum timing: ~40ms** — anything faster will drop frames
- For effects faster than ~50ms, use the fixture's **built-in strobe macros** instead of rapid DMX value changes

### Timing Rules of Thumb

1. **Chase speed = quarter note** as default, adjust from there
2. **Fade time for smooth crossfade:** half note to whole note (slow song) or quarter note (fast song)
3. **Strobe: sixteenth notes** at minimum; faster requires fixture internal strobe
4. **Color wash transitions:** whole note or half note for smooth; snap on beat
5. **Effect changes:** every 4 or 8 bars to match musical phrases
6. **Big moment (drop/chorus):** snap change on the downbeat of bar 1
7. **Build-up:** gradually increase chase speed or add fixtures over 4-8 bars before the drop

### BPM Ranges by Genre

| Genre | Typical BPM | Quarter Note (ms) |
|-------|------------|-------------------|
| Hip-Hop / Trap | 60-90 | 1000-667 |
| R&B / Soul | 70-90 | 857-667 |
| Pop | 100-130 | 600-462 |
| House | 120-130 | 500-462 |
| Techno | 125-150 | 480-400 |
| Trance | 130-150 | 462-400 |
| Drum & Bass | 160-180 | 375-333 |
| Hardstyle | 150-160 | 400-375 |
| Dubstep (half-time) | 140 (feels like 70) | 428 (effective 857) |

### Tap Tempo in QLC+

QLC+ Speed Dials support tap tempo input. During a live show:
1. Tap the beat button 4-8 times in rhythm
2. The Speed Dial calculates average BPM
3. All linked chases/effects sync to that tempo
4. Re-tap when the song changes or tempo drifts

For MIDI controllers, map a pad to the Speed Dial's tap input for hands-free beat matching.

﻿---

## 4. Effect Layering and Stacking

### The Building Block Philosophy

The most effective busking approach builds looks from independent parameter layers that combine freely:

```
FINAL LOOK
  Layer 4: Effects / FX         (chases, strobes, movement effects)
  Layer 3: Beam / Gobo          (gobo selection, prism, beam shape)
  Layer 2: Color                (color palette, color effects)
  Layer 1: Position / Focus     (where lights point)
  Layer 0: Intensity / Dimmer   (which fixtures are on, how bright)
```

Each layer is controlled independently. By changing any single layer, you create a new look without rebuilding from scratch.

### Cue Stack Layering (Brad Schiller Method)

Create **separate cue stacks** organized by parameter type:

| Stack | Contents | Example Cues |
|-------|----------|-------------|
| **Position Stack** | Multiple position presets | All center, fan out, audience, drummer spot, left/right split |
| **Color Stack** | Color combinations | Blue wash, red/orange split, purple/cyan, warm white |
| **Beam/Gobo Stack** | Beam parameters | Open, tight circle gobo, prism rotate, frost |
| **Effect/Chase Stack** | Dynamic effects | Dimmer chase, color chase, ballyhoo, rainbow |

**Combine any cue from each stack** to create hundreds of unique looks from a small number of programmed elements.

### Fixture Group Layering

Build faders and flash keys that control fixture groupings:

| Group | Purpose |
|-------|---------|
| All spots | Global spot control |
| All wash | Global wash control |
| Overhead fixtures | Truss-mounted only |
| Floor fixtures | Uplighting, floor effects |
| Audience lights | House/audience wash |
| Stage left / Stage right | Positional splits |
| Odd / Even | Alternate fixtures for chase effects |

Toggle groups on/off during a show to dramatically change the look while the same color/position cue plays.

### Effect Building Strategies

#### Additive Building
1. Begin with back wash only
2. Add side spots
3. Add front wash
4. Add overhead effects
5. Full rig for chorus/drop

#### Subtractive Reveal
1. Full rig for opening impact
2. Remove effects, leave color wash
3. Strip to single spot for intimate moment
4. Rebuild for the next section

#### The Contrast Principle
The power of any lighting look is defined by what came before it:
- A slow blue wash makes the following red strobe feel explosive
- A blackout makes ANY light feel dramatic
- A single spot after full rig makes the performer feel isolated

### QLC+ Specific Layering

- **LTP (Latest Takes Precedence):** Set 99% of fixtures to LTP mode for intuitive busking — the last triggered scene/function wins for that parameter
- **HTP (Highest Takes Precedence):** Use for dimmer/intensity channels where you want multiple sources to combine additively
- **Submasters:** Place a submaster fader inside a frame with the functions it should control — acts as a global intensity for that group
- **RGB Matrix Blend Modes:** Use Add, Subtract, and Mask modes to layer effects:
  - **Default (Add):** Colors combine additively
  - **Subtract:** Removes color/intensity from existing output
  - **Mask:** Uses the matrix as a transparency mask over existing looks

﻿---

## 5. Console Layout Philosophy

### The Universal Principle

> "Lay out any console you work on the same way every time. This way, you always know where to find your groups, colors and palettes."
> — Susan Rose, Touring LD (Ringo Starr, Dove Awards, Disney)

Consistency enables muscle memory. During a live show, you should never need to look down to find a control.

### Layout Architecture

**Zone 1: Always Visible (Master Controls)**
- Grand Master / Blackout
- Punt Look (safety cue)
- Fixture group intensity faders
- Currently active scene indicators

**Zone 2: Primary Busking Area**
- Color selection (most used)
- Position/focus presets
- Master preset buttons
- Chase/effect triggers

**Zone 3: Modification Area**
- Speed controls / Tap Tempo
- Effect parameters (size, spread, speed)
- Gobo/beam selection
- Strobe controls

**Zone 4: Extended / Less Used**
- Individual fixture control
- Setup/configuration
- Advanced effects
- Secondary fixture types

### Fixture Numbering System (Susan Rose Method)

| Number Range | Fixture Type |
|-------------|-------------|
| 1-99 | Conventional / PAR |
| 101-199 | LED wash fixtures |
| 201-299 | Large spot moving heads |
| 301-399 | Small/medium beam moving heads |
| 401-499 | LED bars / battens |
| 501-599 | LED rings / pixel fixtures |
| 601-699 | Moving wash fixtures |
| 701-799 | Matrix / panel fixtures |
| 801-899 | Audience / house lights |
| 901-999 | Specials / effects (strobe, UV, haze) |

### Group Organization

Organize groups in two dimensions:

**By Position (columns):** DS Left, DS Center, DS Right, US Left, US Center, US Right

**By Type (rows):** Spots, Washes, Bars, Rings, Matrix

This creates a grid where any intersection gives you a specific set of fixtures at a specific position.

### Pan/Tilt Initialization

Adjust pan and tilt offsets so ALL fixtures start facing the same direction (toward FOH). This enables uniform starting positions, predictable movement when busking, and muscle memory for directional adjustments.

### Palette Building Priority

Build palettes in this order (most reused first):

1. **Position palettes:** Center, left, right, audience, split, diagonal, drum riser
2. **Color palettes:** Every useful color at proper saturation
3. **Beam palettes:** Open, narrow, gobo selections, prism states
4. **Effect palettes:** Standard chases, movement patterns

If something changes (performer moves, fixture re-hung), update the palette once and every cue that references it updates automatically.

﻿---

## 6. Quick-Access Strategies

### The "Live vs Trigger" Memory Classification

| Type | Behavior | Examples | Fader Treatment |
|------|----------|---------|----------------|
| **Live memories** | Must stay faded up to remain active | PAR washes, dimmer levels, LED color holds | Keep on accessible faders |
| **Trigger memories** | Only need momentary activation | Color change, gobo select, strobe fire | Flash button or raise-and-lower |

**Rule:** Never stack Live and Trigger memories on the same fader/page position. You don't want to lose your blue wash just to fire a gobo change. — Rob Sayer, OnStageLighting.co.uk

### Page Management

- **Home Page:** Your safety net. Most-used looks, punt look, basic washes. Always return here when lost.
- **Page +1:** Additional color options, secondary effects
- **Page +2:** Extended effects, specialized looks
- **Maximum 3 pages** — more than that and you'll get lost during a show
- **Circular scrolling:** Enable in QLC+ Multi Page Frames so you cycle endlessly

### MIDI Controller Layout Strategy

For grid controllers (APC Mini, Launchpad, etc.):

```
ROW 1: Color presets (R, B, G, Purple, Cyan, etc.)
ROW 2: Position presets
ROW 3: Effects / Chases
ROW 4: Master presets (full looks)
ROW 5: Strobes / Momentary FX
ROW 6: Fixture group selects
ROW 7: Page navigation / Utilities
ROW 8: Intensity bumps / Blackout / Punt
FADERS: Group intensity (per fixture type)
```

**Color-code your MIDI pads:**
- Red = Color triggers
- Green = Position triggers
- Blue = Effects
- Yellow = Master presets
- White/bright = Safety / punt / blackout

### The Safety Net Macro

Program a single button that:
1. Kills all running chases and effects
2. Resets all cue stacks to their first cue
3. Releases all active scenes except the safety wash
4. Fades to a neutral stage wash over 1-2 seconds

Mark it clearly. Use it without shame.

### Speed Control Quick-Access

- **Dedicated tap tempo button** on your MIDI controller
- **Speed fader** for real-time BPM adjustment
- **Preset speed buttons:** Slow (60 BPM) / Medium (120 BPM) / Fast (140 BPM)
- In QLC+, use Speed Dials linked to chases
- A sequence with 2 different values is more stable than a scene for speed presets
- Use separate Speed Dials for Run Time and Fade Time — never let fade exceed run time

### Pre-Built Quick-Fire Looks

| Look | Description | When to Use |
|------|------------|------------|
| **Pre-Start** | Low amber/blue wash, minimal movement | Before show, between sets |
| **Between Songs** | Medium cool wash, gentle fade | Song transitions, talk cue |
| **Verse Low** | Subdued warm wash, spots on vocalist | Verses, quiet moments |
| **Chorus Full** | Full rig, saturated color, effects | Choruses, big moments |
| **Ballad** | Single warm spot + deep blue wash | Slow songs, intimate |
| **High Energy** | Rapid chases, strobes, full saturation | Drops, peaks, finales |
| **Audience Wash** | Outward-facing lights on crowd | Sing-alongs, crowd shots |
| **Blackout** | Everything off | Dramatic pauses, endings |

﻿---

## 7. Creative Effect Ideas

### LED Ring Effects

LED rings offer unique circular geometry that other fixtures can't replicate.

#### Chase Patterns
| Effect | Description | Speed |
|--------|------------|-------|
| **Clockwise Chase** | Single lit pixel rotates around the ring | 1/4 note to 1 bar |
| **Counter-Clockwise** | Reverse rotation | Match or offset from CW |
| **Bi-directional** | Two pixels chasing in opposite directions | 1/4 note |
| **Pendulum** | Pixel bounces back and forth across arc | 1/2 note |
| **Fill-Drain** | Ring fills pixel by pixel, then drains | 1 bar fill, 1 bar drain |
| **Split Chase** | Two halves chase independently | 1/4 note each |

#### Pulse and Fade Patterns
| Effect | Description | Speed |
|--------|------------|-------|
| **Breathe** | All pixels pulse together (0% to 100% to 0%) | 1-2 bars |
| **Heartbeat** | Double-pulse pattern (pulse-pulse-rest) | Synced to beat |
| **Cascading Pulse** | Pulse travels around the ring as a wave | 1/4 note offset per pixel |
| **Iris Pulse** | Inner pixels pulse first, radiating outward | 1/2 bar |

#### Color Effects
| Effect | Description | Speed |
|--------|------------|-------|
| **Rainbow Chase** | Full spectrum rotating around the ring | 1-4 bars/revolution |
| **Color Wipe** | New color sweeps around replacing old | 1/2 to 1 bar |
| **Split Complementary** | Opposite halves in complementary colors | Static or slow rotate |
| **Gradient Rotate** | Smooth gradient spins continuously | 2-4 bars |
| **Strobe Segments** | Alternating segments strobe in different colors | 1/8 to 1/16 note |
| **Fire Flicker** | Random warm pixels with varied intensity | Continuous, organic |

#### Advanced Multi-Ring Patterns

| Effect | Description |
|--------|------------|
| **Concentric Pulse** | Inner ring pulses first, then outer — ripple effect |
| **Counter-Rotate** | Inner CW, outer CCW — mesmerizing complexity |
| **Ring Cascade** | Same pattern offset by 1 beat between rings |
| **Converge/Diverge** | Rings pulse inward together then outward |
| **Crown Effect** | All rings pulse simultaneously on downbeat, chase on beats |

### Wash Bar Effects

| Effect | Description | Speed |
|--------|------------|-------|
| **Color Sweep** | Color travels across the bar end to end | 1/4 to 1 bar |
| **Center-Out** | Effect starts in center, spreads to edges | 1/4 to 1/2 bar |
| **Edge-In** | Effect starts at edges, converges to center | 1/4 to 1/2 bar |
| **Knight Rider** | Single pixel bounces back and forth | 1/4 note |
| **Rainbow Scroll** | Full spectrum scrolling across segments | 2-4 bars |
| **Alternating Blocks** | Even/odd segments alternate colors | Snap on beat |
| **Stagger Chase** | Segments light up one by one | 1/8 note per segment |
| **VU Meter** | Segments light from one end based on audio | Real-time |
| **Segment Strobe** | Individual segments strobe at different rates | 1/8 to 1/16 |
| **Pixel Rainfall** | Random segments light up and fade | Continuous |

### RGB Matrix Panel Effects

| Effect | Description |
|--------|------------|
| **Horizontal Scroll** | Pattern moves left to right or right to left |
| **Vertical Scroll** | Pattern moves top to bottom or bottom to top |
| **Diagonal Sweep** | Color/pattern moves at 45 degree angle |
| **Checkerboard** | Alternating on/off pixels in grid pattern |
| **Random Pixels** | TV static effect with adjustable density |
| **Starfield** | Pixels appear from center moving outward |
| **Audio Spectrum** | Vertical bars responding to audio input |
| **Text Scroll** | Scrolling text messages |
| **Plasma** | Organic, flowing color patterns using sine waves |
| **Square Fill** | Colored squares expand from corner or center |

### QLC+ RGB Matrix Scripts Available

**Built-in:** Full Row/Column, Gradient, Marquee, Opposite, Plasma (Color Bar, Plasma Colors, Phased), Random Fill Column/Row, Squares, Stripes, Waves

**Community:** Random Pixel Per Row, Random Pixel Per Row Multicolor, Static (TV snow), 3D Starfield

**Color slots (v4.14.1+):** Up to 5 simultaneous color points (Start, End, Midpoint 1-3) for smooth gradients. Colors editable during playback via MIDI/OSC or loopback sliders.

### Universal Creative Techniques

#### The Build
Gradually add layers over 8-16 bars:
1. Single color wash at low intensity
2. Add slow chase on the rings
3. Bring in wash bars with complementary color
4. Increase chase speed
5. Add matrix effects
6. Full intensity + strobe on the drop

#### The Strip
Reverse — peel away layers for intimacy:
1. Full rig
2. Kill matrix effects
3. Slow the chases
4. Fade wash bars
5. Reduce to single ring glow + spot

#### The Snap
Maximum contrast — instant transition between two completely different looks. Use on the downbeat of a chorus, drop, or key lyric.

#### The Blackout Punch
Brief blackout (250-500ms) immediately followed by full rig. Massive impact. Use sparingly — once or twice per set maximum.

﻿---

## 8. Cue Structure and Organization

### Cue Hierarchy

```
Parameter > Palette > Scene/Cue > Sequence/Chase > Cue List > Show File
```

| Level | What It Is | Example |
|-------|-----------|---------|
| **Parameter** | Single controllable attribute | Red = 255, Pan = 128 |
| **Palette/Preset** | Reusable parameter collection | "Deep Blue" color, "Center Stage" position |
| **Scene/Cue** | Complete lighting state | Full verse look with all fixtures |
| **Sequence/Chase** | Ordered series of scenes with timing | 4-step color chase at 500ms |
| **Cue List** | Collection of cues for a song/segment | Intro, Verse, Chorus, etc. |
| **Show File** | Everything combined | Complete workspace |

### The Talk Cue (Susan Rose Method)

The talk cue is your **first and last cue in every song.** It bridges between songs when the performer is talking to the audience.

Requirements:
- Wash fixtures in a neutral or cool color
- No movement or effects
- Comfortable visibility
- Smooth crossfade capability into any song look
- All intensity, color, and beam information baked in

**This is different from the punt look.** The punt look is an emergency reset. The talk cue is a deliberate, clean bridge between songs.

### Generic Song Cue Structure

When you have no rehearsal time, use this template for any song:

```
CUE 1:  Talk / Pre-Song      (neutral wash)
CUE 2:  Intro                 (build from dark or minimal)
CUE 3:  Verse 1               (moderate, warm, focused on vocalist)
CUE 4:  Pre-Chorus            (build intensity, add color)
CUE 5:  Chorus 1              (full rig, saturated, effects)
CUE 6:  Verse 2               (pull back, variation from V1)
CUE 7:  Chorus 2              (similar to C1, slight variation)
CUE 8:  Bridge / Breakdown    (something completely different)
CUE 9:  Final Chorus / Climax (biggest look of the song)
CUE 10: End / Tag             (dramatic ending)
CUE 11: Talk / Post-Song      (return to neutral)
```

Copy this template for each song, then customize with different palettes and presets. — Susan Rose, Harman Professional

### Tracking Mode

In tracking, parameters **persist through subsequent cues until explicitly changed.** If you set a light to blue in Cue 3, it stays blue through Cue 4, 5, 6... until a later cue changes it. Only program what changes, not every fixture in every cue.

### Cue Labeling Best Practices

Always label cues so **anyone** can operate the show:
```
CUE  1.0  "Talk"           Neutral wash
CUE  2.0  "Intro Slow"     Blue wash builds over 4 bars
CUE  3.0  "V1 Warm"        Amber spots + cool back
CUE  4.0  "Pre Build"      Add sides, intensity rising
CUE  5.0  "Chorus Full"    Full rig, magenta/cyan, chase on
CUE  5.5  "Chorus FX"      Add strobe accents
CUE  6.0  "V2 Cool"        Pulled back, blue tones
```
Use decimal numbering (5.0, 5.5) to insert cues without renumbering.

### QLC+ Cue Organization

Organize your Function Manager with folders:

```
Functions/
  Scenes/
    Colors/
    Positions/
    Beams/
    Off States/
  Chasers/
  RGB Matrices/
    Bar Effects/
    Ring Effects/
    Panel Effects/
  Sequences/
    Speed Presets/
    Loopback Controls/
  Master Presets/
  Utilities/
    Blackout
    Punt Look
    Reset All
```

### Naming Conventions

Pattern: `[FixtureGroup] [Parameter] [Description]`

Examples: `Pars Color Red`, `Spots Position Center`, `Bars Chase Rainbow`, `Rings Pulse Breathe`, `All Master Chorus Big`

﻿---

## 9. Community Tips (Reddit / Forum Wisdom)

### From the QLC+ Forum Community

#### File Management (MichelSliepenbeek, GGGss)
- **Always create backups** — even to the 3rd generation. "Thank me later."
- Store fixture definitions, input profiles, MIDI templates, custom RGB scripts, gobo images, and drivers in your QLC+ User Library folder
- Back up your User Lib alongside your .qxw workspace files
- When transferring between PCs, include the full User Library

#### Virtual Console Design
- **Use Multi Page Frames** with circular scrolling enabled — once you're used to it, you can't live without it
- **Be consistent:** Similar functions always in the same position. Color selectors on the left, intensity faders on the right (or whatever your convention is — just keep it the same everywhere)
- **Standardize button colors:** Light grey for effects, dark grey for gobos, colored backgrounds matching the actual color they trigger
- **Less is more:** A red background button doesn't need the label "Red" — the color is self-explanatory
- **Set resolution to 1860x1050** for max usage on Full HD in kiosk mode

#### LTP Mode for Busking
- Set **99% of fixtures to LTP mode** — this makes busking intuitive because the last thing you trigger wins
- Only dimmer/intensity should typically be HTP

#### RGB Matrix Power Moves
- Use **RGB Matrix Strobe** instead of individual fixture strobe channels — fixture strobes from different manufacturers have different ranges and sensitivities, making sync impossible. RGB Matrix strobe in Mask mode works with any color.
- **Add/Subtract/Mask modes** enable sophisticated layering:
  - Subtract mode creates dimming effects (-0.25, -0.50, -0.75 buttons)
  - Mask mode lets you use the matrix as a transparency layer
- Use **separate Speed Dials for Run Time and Fade Time** — never let fade time exceed run time
- **Loopback sliders** can dynamically control RGB Matrix speed in real-time

#### Submaster Tricks
- If a fixture has no master dimmer channel, use a **Submaster** inside a frame with the functions you want it to control
- **Loopback trick:** Create a loopback universe, use buttons/sliders to control other widgets via external control inputs — one slider can multiplex into controlling multiple submasters

#### MIDI Controller Tips
- Follow the **physical layout** of your MIDI controller for your VC layout — matching what you see on screen with what you feel under your fingers
- Use different button orientations (horizontal vs vertical) to visually distinguish MIDI controller modes without looking at the screen
- Consider setting up 2-3 "modes" on your MIDI controller using page switching

### From MA Lighting Forum (grandMA2/3 Users)

#### Busking Techniques (Transferable Concepts)
- **"Hiding Changes" technique:** Load cues without triggering them immediately. Load multiple cues across different executors, then fire them all simultaneously with a single GO press. Creates clean, coordinated transitions.
- **Ratemaster method:** Assign a ratemaster to executors. Set it to zero to freeze transitions while you set up multiple changes. Move the fader up to execute all changes with smooth transitions.
- **Separate speed masters:** One for dimmer/color effects, another for movement. Lets you independently control the pace of different effect types.

#### Philosophical Points
- There is **no single "correct" workflow** — what matters is comfort and efficiency with your preferred method
- **Show files are console-specific** — don't expect to port shows between platforms. Learn the concepts and rebuild in your tool
- **Every operator develops their own style** — learn the principles, then adapt to your tools and personality

### From Experienced Operators (Various Sources)

#### Show Preparation
- "There will be a band onstage" is the most common brief you'll receive. Prepare for the worst, hope for the best.
- Even for busked shows, **gather as much information as possible:** genre, set length, audience demographics, special moments
- If it's a wedding: they WILL play "Chicken Dance." Have a look ready.
- If it's a cover band: they WILL play "The Final Countdown." Have a look ready.

#### During the Show
- **Don't spot the drummer** unless they're doing a solo
- **Lay off caffeine** if you're busking AND calling spots simultaneously
- **Black stage = you blew it.** The punt look prevents this.
- Read the crowd: If you see "a lot of freaky tattoos and pierced faces, any kind of moving light show will do as long as it's fast and bright." If you see "walkers and blue hair, keep the lights on the stage." — Mike Graham, CHAUVET

#### Practice Methodology
- Practice with music you **don't know and don't like** — real shows rarely feature music you enjoy
- Put on a random Spotify playlist and busk for an hour
- Record yourself and watch back — you'll spot timing mistakes and missed opportunities
- The goal is **organized improvisation** — enough pre-programmed content arranged intuitively for real-time response

﻿---

## 10. BPM-to-Duration Conversion Tables

### Master Conversion Table

Formula: `ms = 60,000 / BPM` for a quarter note

| BPM | Whole (4 beats) | Half (2) | Quarter (1) | 8th | 16th | 32nd | Dotted 1/4 | Trip 1/8 |
|-----|-----------------|----------|-------------|-----|------|------|------------|----------|
| 60 | 4000 | 2000 | 1000 | 500 | 250 | 125 | 1500 | 333 |
| 65 | 3692 | 1846 | 923 | 462 | 231 | 115 | 1385 | 308 |
| 70 | 3429 | 1714 | 857 | 429 | 214 | 107 | 1286 | 286 |
| 75 | 3200 | 1600 | 800 | 400 | 200 | 100 | 1200 | 267 |
| 80 | 3000 | 1500 | 750 | 375 | 188 | 94 | 1125 | 250 |
| 85 | 2824 | 1412 | 706 | 353 | 176 | 88 | 1059 | 235 |
| 90 | 2667 | 1333 | 667 | 333 | 167 | 83 | 1000 | 222 |
| 95 | 2526 | 1263 | 632 | 316 | 158 | 79 | 947 | 211 |
| 100 | 2400 | 1200 | 600 | 300 | 150 | 75 | 900 | 200 |
| 105 | 2286 | 1143 | 571 | 286 | 143 | 71 | 857 | 190 |
| 110 | 2182 | 1091 | 545 | 273 | 136 | 68 | 818 | 182 |
| 115 | 2087 | 1043 | 522 | 261 | 130 | 65 | 783 | 174 |
| 120 | 2000 | 1000 | 500 | 250 | 125 | 63 | 750 | 167 |
| 125 | 1920 | 960 | 480 | 240 | 120 | 60 | 720 | 160 |
| 128 | 1875 | 938 | 469 | 234 | 117 | 59 | 703 | 156 |
| 130 | 1846 | 923 | 462 | 231 | 115 | 58 | 692 | 154 |
| 135 | 1778 | 889 | 444 | 222 | 111 | 56 | 667 | 148 |
| 140 | 1714 | 857 | 429 | 214 | 107 | 54 | 643 | 143 |
| 145 | 1655 | 828 | 414 | 207 | 103 | 52 | 621 | 138 |
| 150 | 1600 | 800 | 400 | 200 | 100 | 50 | 600 | 133 |
| 155 | 1548 | 774 | 387 | 194 | 97 | 48 | 581 | 129 |
| 160 | 1500 | 750 | 375 | 188 | 94 | 47 | 563 | 125 |
| 165 | 1455 | 727 | 364 | 182 | 91 | 45 | 545 | 121 |
| 170 | 1412 | 706 | 353 | 176 | 88 | 44 | 529 | 118 |
| 175 | 1371 | 686 | 343 | 171 | 86 | 43 | 514 | 114 |
| 180 | 1333 | 667 | 333 | 167 | 83 | 42 | 500 | 111 |

### Quick Reference: Common Electronic Music BPMs

| Genre | BPM | Quarter (ms) | 8th (ms) | 16th (ms) | 1 Bar (ms) |
|-------|-----|-------------|---------|----------|------------|
| Downtempo | 80 | 750 | 375 | 188 | 3000 |
| Deep House | 120 | 500 | 250 | 125 | 2000 |
| House | 125 | 480 | 240 | 120 | 1920 |
| Electro House | 128 | 469 | 234 | 117 | 1875 |
| Tech House | 126 | 476 | 238 | 119 | 1905 |
| Techno | 130 | 462 | 231 | 115 | 1846 |
| Prog Trance | 138 | 435 | 217 | 109 | 1739 |
| Trance | 140 | 429 | 214 | 107 | 1714 |
| Hard Trance | 145 | 414 | 207 | 103 | 1655 |
| Hardstyle | 150 | 400 | 200 | 100 | 1600 |
| Jungle/DnB | 170 | 353 | 176 | 88 | 1412 |
| Drum and Bass | 175 | 343 | 171 | 86 | 1371 |

### Useful Timing Relationships

```
1 Bar (4/4 time)  = 4 x quarter note
2 Bars            = 8 x quarter note     (typical effect loop length)
4 Bars            = 16 x quarter note    (typical phrase length)
8 Bars            = 32 x quarter note    (typical section: verse/chorus)
16 Bars           = 64 x quarter note    (typical build-up length)
```

### DMX Limitations at Speed

| At 128 BPM | Duration | DMX Frames at 40Hz | Reliable? |
|------------|----------|-------------------|-----------|
| Quarter note | 469ms | ~19 frames | Yes |
| Eighth note | 234ms | ~9 frames | Yes |
| Sixteenth note | 117ms | ~5 frames | Marginal |
| Thirty-second | 59ms | ~2 frames | Unreliable — use fixture strobe |

**Rule:** If your effect needs fewer than 5 DMX frames per step, use the fixture's built-in strobe/effect macros instead of rapid DMX value changes.

﻿---

## Appendix A: QLC+ Busking Checklist

Before every show:

- [ ] Fixture definitions loaded and verified
- [ ] All fixtures patched and DMX addresses confirmed
- [ ] Pan/tilt inverted/offset so all fixtures face FOH
- [ ] Fixture groups created (by type AND by position)
- [ ] Color palettes programmed
- [ ] Position palettes programmed
- [ ] Master presets created (Pre-Start, Between Songs, Verse, Chorus, etc.)
- [ ] Punt look / safety cue on dedicated button
- [ ] Blackout on dedicated button
- [ ] Speed Dial configured and linked to chases
- [ ] MIDI controller mapped and tested
- [ ] Tap tempo mapped to MIDI pad
- [ ] LTP mode set on all non-dimmer channels
- [ ] Virtual Console layout arranged and page-tested
- [ ] Backup of show file saved (3 generations)
- [ ] Test all looks and transitions in visualizer or on actual rig
- [ ] Practice busking to random music for 15-30 minutes

---

## Appendix B: Dimmer Curves and Intensity Techniques

### Dimmer Curve Types

| Curve | Behavior | Use |
|-------|----------|-----|
| **Linear** | Direct proportional: input = output | Simple, predictable, default for LED |
| **Square Law** | Slow start, rapid finish | Theatrical convention, natural for tungsten |
| **S-Curve** | Slow start AND finish, fast middle | Smooth visible transitions, good for fades |
| **Inverse Square** | Fast start, slow finish | Snappy on, gentle off |

### Key Principle: Human Perception Is Logarithmic

The human eye perceives brightness logarithmically, not linearly. A light at 50% DMX output does NOT look "half as bright" — it looks much brighter than half. The CIE 1931 lightness curve accounts for this and produces the most natural-looking fades.

### Practical Intensity Techniques

- **Use inhibitive faders** to subtract intensity from groups — stagger spots into odd/even and use negative inhibitors to create variety
- **Bump buttons** for momentary flash-to-full on specific fixture groups
- **Intensity masters per fixture type** — separate faders for wash, spot, bars, rings
- **Never go to true 0%** unless deliberate blackout — even 2-3% creates subtle ambient glow that prevents the "dead stage" look

---

## Appendix C: Sources and Further Reading

### Articles and Guides
- Brad Schiller, "The Basics of Busking," Lighting & Sound America, December 2024
- Mike Graham, "Tech Talk: How to Master the Art of Busking," CHAUVET Professional
- Susan Rose, "Top Tips for Programming Dynamic Light Shows on Any Console," Harman Professional
- Rob Sayer, "Using Submasters for Busking Band Lighting," OnStageLighting.co.uk
- "Lighting for BPM Festivals: Timecode vs Busking," TicketFairy.com
- XMLite, "Stage Lighting Color Theory: Rules, Emotions, and Real-World Applications"
- BeTopperDJ, "Stage Lighting Color Guide: How to Pick Palettes That Tell a Story"

### QLC+ Community Threads
- "How to efficiently make a busking showfile?" — qlcplus.org/forum
- "First go at a busking show file — thoughts?" — forum.qlcplus.org
- "Busking with generic RGB Fixtures" — qlcplus.org/forum
- "Turbo-charging RGB Matrix functions!" — qlcplus.org news

### Console Documentation
- ChamSys MagicQ: Live Programming (Busking) documentation
- Avolites: Organising the Console manual
- ETC Eos: Busking Workbook v3.0
- MA Lighting Forum: Busking Style discussions

---

*Last updated: April 2026*
*This document is a living reference — update it as you discover new techniques.*
