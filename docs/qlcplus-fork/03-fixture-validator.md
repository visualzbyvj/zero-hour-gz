# Fixture Profile Validator And Editor Upgrade

## Purpose

The second recommended QLC+ fork feature is a fixture profile validator and editor upgrade.

Zero Hour GZ depends on custom fixtures. If `.qxf` profiles are wrong, every later system is wrong:

1. Visualizer
2. Fixture groups
3. RGB Matrix
4. MIDI control
5. Chasers
6. Lasers
7. Strobes
8. Future phasers
9. Future recipes

## Core problem

QLC+ can load a fixture profile that is technically valid XML but still bad for live programming.

Examples:

1. Wrong channel count
2. Wrong mode name
3. Missing heads
4. Head order does not match physical order
5. RGB channels not assigned per head
6. Master dimmer assigned to one head incorrectly
7. Per head dimmer missing
8. Strobe channel not labeled clearly
9. Laser reset or safety channel not labeled clearly
10. Fixture appears in patch list but behaves wrong in RGB Matrix

## Validator targets

Validate `.qxf` profiles for:

1. Manufacturer
2. Model
3. Fixture type
4. Mode names
5. Mode channel counts
6. Channel order
7. Channel capabilities
8. Capability ranges
9. Head count
10. Head channel assignments
11. RGB / RGBW / CMY channel mapping
12. Dimmer mapping
13. Master dimmer mapping
14. Shutter / strobe mapping
15. Pan / tilt mapping when present
16. Laser critical channels
17. Reset channels
18. Unsupported or unknown channel groups
19. Matrix compatibility
20. Visualizer compatibility

## Zero Hour GZ priority checks

### Pixel bars

1. Expected section count matches head count
2. Expected emitter count matches controllable cells
3. Physical order matches head index order
4. RGBW channel grouping is consistent
5. Global dimmer is separate from per section color when applicable

### Lasers

1. Laser channels are labeled clearly
2. Reset and motor channels are not hidden under generic names
3. Safety critical channels are flagged
4. RGB channels are not treated as normal wash emitters unless intended
5. Visualizer only behavior is separated from live output assumptions

### Strobes and blinders

1. Intensity and shutter channels are clear
2. Full output channels are flagged as high risk
3. Strobe rate and strobe enable are not ambiguous
4. Master intensity is easy to identify

## Fork implementation idea

Add a validator service in the fixture editor or engine resource loading path.

Potential class:

```cpp
class GZFixtureProfileValidator
{
public:
    GZFixtureValidationReport validateDefinition(const QLCFixtureDef* def);
    GZFixtureValidationReport validateMode(const QLCFixtureMode* mode);
};
```

Potential warning classes:

```text
Error
Warning
Info
SafetyWarning
MatrixWarning
VisualizerWarning
```

## Editor improvements

Add an inspection panel showing:

1. Mode channel count
2. Head count
3. Per head channels
4. Global channels
5. RGB channels per head
6. Dimmer channels per head
7. Shutter/strobe channels per head
8. Matrix compatibility status
9. Safety warnings
10. Suggested fixes

## Non source fallback

Before source implementation, a validator can exist in `zero-hour-gz` as a Python script that reads `.qxf` XML.

Recommended script:

```text
validation/validate_qxf.py
```

Outputs:

```text
reports/qxf-validation-report.md
```

## What not to do first

1. Do not auto rewrite profiles without user approval
2. Do not change fixture modes silently
3. Do not guess channel maps
4. Do not treat lasers as normal RGB fixtures
5. Do not remove existing modes unless explicitly approved

## Success definition

The validator is successful when it can catch the exact class of problems that cause:

1. Bars to split or skip sections
2. RGB Matrix to write to the wrong channels
3. Visualizer to mismatch physical layout
4. Fixture profiles to disappear or behave inconsistently
5. Dangerous channels to be unlabeled
