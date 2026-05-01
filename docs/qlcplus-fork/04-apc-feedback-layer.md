# APC Mini MK2 Native Feedback Layer

## Purpose

The third recommended QLC+ fork feature is an APC Mini MK2 performance feedback layer.

Zero Hour GZ uses APC Mini MK2 as a live EDM busking control surface. QLC+ already includes an APC Mini MK2 input profile, so the first source fork should not be basic controller recognition.

The fork target is smarter live feedback and operator state.

## Existing foundation

QLC+ has an APC Mini MK2 input profile:

```text
resources/inputprofiles/Akai-APCMini-mk2.qxi
```

It includes:

1. Sliders
2. Button channels
3. Feedback values
4. Color table
5. MIDI channel table
6. Brightness / pulse / blink labels

## Problem this solves

A generic MIDI mapping tells QLC+ what button was pressed.

A performance feedback layer tells the operator what the rig is doing.

For live EDM busking, the controller should show:

1. Active base looks
2. Active color worlds
3. Active chasers
4. Active strobes
5. Active lasers
6. Active blinders
7. Current page or bank
8. Danger states
9. Armed states
10. Shift states
11. Speed layer state
12. Panic / blackout state

## Recommended feedback language

Default meaning:

```text
Off = inactive
Green = safe active layer
Yellow = effect / speed / movement layer
Red = danger layer
Blinking red = high risk active or armed
White = selected page or utility
Blue = atmospheric / breakdown layer
Purple = laser visualizer or special FX layer
```

Exact APC values must be verified against the `.qxi` color table and hardware behavior.

## Fork feature ideas

### Page aware LED feedback

When Virtual Console page changes, APC LEDs should reflect that page.

### Function type feedback

LED color should be based on what a button controls:

1. Base look
2. Drop hit
3. Build
4. Strobe
5. Laser
6. Blinder
7. Speed
8. Utility
9. Safety

### Active state feedback

If a function is running, the LED should indicate it.

### Danger feedback

High risk controls should have stronger feedback:

1. Strobes
2. Lasers
3. Blinders
4. Full white hits
5. Output arm states

### Shift layers

Support a held shift button to access secondary controls without losing state feedback.

### Soft takeover

For faders, prevent sudden jumps when physical fader position does not match internal value.

## Implementation sketch

Potential class:

```cpp
class GZApcMiniMk2FeedbackController
{
public:
    void bindToVirtualConsole();
    void updateButtonState(int channel, GZFeedbackState state);
    void updatePageState(int pageIndex);
    void updateDangerState(GZDangerClass dangerClass, bool active);
};
```

Potential state object:

```cpp
struct GZFeedbackState
{
    bool active;
    bool armed;
    bool flashing;
    QString functionType;
    QString safetyClass;
    int colorValue;
    int midiChannelValue;
};
```

## Integration points to inspect

1. MIDI plugin
2. Input profiles
3. Virtual Console widgets
4. Function running state
5. Feedback patch logic
6. APC Mini MK2 `.qxi` color table

## What not to do first

1. Do not remove the existing APC Mini MK2 profile
2. Do not remap all controls automatically
3. Do not break generic MIDI support
4. Do not require APC Mini MK2 for normal QLC+ operation
5. Do not encode Zero Hour specific page names directly into generic QLC+ core

## Success definition

The layer is useful when a user can glance at the APC Mini MK2 and know:

1. Which looks are active
2. Which effects are armed
3. Which controls are dangerous
4. Which page or bank is selected
5. Whether blackout or panic state is active
6. Whether a strobe, laser, or blinder layer is currently live
