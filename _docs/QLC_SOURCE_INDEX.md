# QLC+ 5.2.1 Source Code -- Local Quick-Reference Index

Root: E:\Dropbox\04.11.26 Zero Hour GZ\qlcplus-QLC-_5.2.1 Source Code\

> Which folder? Use ui/src/ for the desktop Qt4 widgets (what our .qxw targets).
> qmlui/ is QLC+ 5's new QML UI -- ignore for XML generation purposes.
> engine/src/ holds shared logic (functions, algorithms, DMX engine).

---

## Virtual Console Widgets (ui/src/virtualconsole/)

| Widget           | Header                    | Impl                      | XML tag        |
|------------------|---------------------------|---------------------------|----------------|
| VCButton         | vcbutton.h                | vcbutton.cpp              | Button         |
| VCSlider         | vcslider.h                | vcslider.cpp              | Slider         |
| VCFrame          | vcframe.h                 | vcframe.cpp               | Frame          |
| VCSoloFrame      | vcsoloframe.h             | vcsoloframe.cpp           | SoloFrame      |
| VCMatrix         | vcmatrix.h                | vcmatrix.cpp              | Matrix         |
| VCSpeedDial      | vcspeeddial.h             | vcspeeddial.cpp           | SpeedDial      |
| VCSpeedDialFn    | vcspeeddialfunction.h     | vcspeeddialfunction.cpp   | Function child |
| VCSpeedDialPreset| vcspeeddialpreset.h       | vcspeeddialpreset.cpp     | Preset         |
| VCWidget (base)  | vcwidget.h                | vcwidget.cpp              | --             |

---

## Engine / Functions (engine/src/)

| Class           | Header             | Impl               | XML tag                        |
|-----------------|--------------------|---------------------|--------------------------------|
| Function (base) | function.h         | function.cpp        | Function                       |
| RGBMatrix       | rgbmatrix.h        | rgbmatrix.cpp       | Function Type="RGBMatrix"      |
| RGBAlgorithm    | rgbalgorithm.h     | rgbalgorithm.cpp    | Algorithm                      |
| MasterTimer     | mastertimer.h      | mastertimer.cpp     | --                             |
| Scene           | scene.h            | scene.cpp           | Function Type="Scene"          |
| Chaser          | chaser.h           | chaser.cpp          | Function Type="Chaser"         |
| Collection      | collection.h       | collection.cpp      | Function Type="Collection"     |

---

## Key XML Constants (from headers)

### VCButton (vcbutton.h)

    KXMLQLCVCButton             = "Button"
    KXMLQLCVCButtonIcon         = "Icon"
    KXMLQLCVCButtonFunction     = "Function"
    KXMLQLCVCButtonFunctionID   = "ID"
    KXMLQLCVCButtonAction       = "Action"
    KXMLQLCVCButtonActionFlash  = "Flash"
    KXMLQLCVCButtonActionToggle = "Toggle"
    KXMLQLCVCButtonActionBlackout = "Blackout"
    KXMLQLCVCButtonActionStopAll  = "StopAll"
    KXMLQLCVCButtonFlashOverride  = "Override"
    KXMLQLCVCButtonFlashForceLTP  = "ForceLTP"
    KXMLQLCVCButtonStopAllFadeTime = "FadeOut"
    KXMLQLCVCButtonKey             = "Key"
    KXMLQLCVCButtonIntensity       = "Intensity"
    KXMLQLCVCButtonIntensityAdjust = "Adjust"

### VCButton Actions -- XML Examples

    <!-- Toggle (default) -->
    <Action>Toggle</Action>

    <!-- Flash with LTP override (blackout-style) -->
    <Action Override="0" ForceLTP="1">Flash</Action>

    <!-- Flash without LTP override (normal bump) -->
    <Action Override="0" ForceLTP="0">Flash</Action>

    <!-- StopAll -- instant kill -->
    <Action>StopAll</Action>

    <!-- StopAll -- with 2-second fade-out -->
    <Action FadeOut="2000">StopAll</Action>

    <!-- Hardware blackout toggle (IOMap blackout, not a function) -->
    <Action>Blackout</Action>

### VCButton pressFunction() behavior

    Toggle   -> start/stop the attached function
    Flash    -> f->flash(masterTimer, flashOverrides, flashForceLTP)
                held = on, released = off
    StopAll  -> stopAllFadeTime()==0 ? masterTimer->stopAllFunctions()
                                     : masterTimer->fadeAndStopAll(ms)
    Blackout -> inputOutputMap->toggleBlackout()

---

### VCSpeedDialFunction (vcspeeddialfunction.h)

    enum SpeedMultiplier {
        None           = 0,   // "(Not Sent)"
        Zero           = 1,   // "0"
        OneSixteenth   = 2,   // "1/16"
        OneEighth      = 3,   // "1/8"
        OneFourth      = 4,   // "1/4"
        Half           = 5,   // "1/2"
        One            = 6,   // "1x"     <-- default Duration
        Two            = 7,   // "2x"
        Four           = 8,   // "4x"
        Eight          = 9,   // "8x"
        Sixteen        = 10,  // "16x"
    };

XML example:  <Function FadeIn="0" FadeOut="0" Duration="6">3700</Function>
  - Duration="6" = 1x multiplier
  - FadeIn="0"   = Not Sent (speed dial doesn't control fade-in)
  - Element text  = function ID

---

### VCSlider (vcslider.h)

    KXMLQLCVCSlider            = "Slider"
    KXMLQLCVCSliderMode        = "SliderMode"
      values: "Playback" | "Submaster" | "Level"
    KXMLQLCVCSliderPlayback    = "Playback"
      child: <Function>fid</Function>
    KXMLQLCVCSliderLevel       = "Level"
      attrs: LowLimit, HighLimit, Value
      children: <Channel Fixture="fid">ch</Channel>

### VCFrame (vcframe.h)

    KXMLQLCVCFrame             = "Frame"
    KXMLQLCVCFrameMultipage    = "Multipage"  (attr on Frame)
    KXMLQLCVCFramePagesNum     = "PagesNum"
    KXMLQLCVCFrameCurrentPage  = "CurrentPage"
    KXMLQLCVCFramePageCaption  = "PageCaption"

### VCMatrix (vcmatrix.h)

    KXMLQLCVCMatrix             = "Matrix"
    KXMLQLCVCMatrixFunction     = "Function"   (child element)
      attr: ID (function id)
    KXMLQLCVCMatrixInstantApply = "InstantApply"
    KXMLQLCVCMatrixCustomColor  = "CustomColor"

---

## Frequently-Used Paths (absolute, from source root)

    ui/src/virtualconsole/vcbutton.cpp        -- Button load/save/press/release
    ui/src/virtualconsole/vcbutton.h          -- Button XML constants and Action enum
    ui/src/virtualconsole/vcslider.cpp        -- Slider load/save (Playback/Submaster/Level)
    ui/src/virtualconsole/vcslider.h          -- Slider XML constants and mode enum
    ui/src/virtualconsole/vcframe.cpp         -- Frame/Multipage load/save
    ui/src/virtualconsole/vcmatrix.cpp        -- Matrix widget load/save
    ui/src/virtualconsole/vcmatrix.h          -- Matrix XML constants
    ui/src/virtualconsole/vcspeeddial.cpp     -- SpeedDial widget load/save
    ui/src/virtualconsole/vcspeeddialfunction.cpp  -- SpeedDial per-function multiplier
    ui/src/virtualconsole/vcspeeddialfunction.h    -- SpeedMultiplier enum
    ui/src/virtualconsole/vcspeeddialpreset.cpp    -- SpeedDial preset buttons
    engine/src/function.cpp                   -- Base Function load/save, flash()
    engine/src/function.h                     -- Function type enum, XML constants
    engine/src/rgbmatrix.cpp                  -- RGBMatrix load/save/run
    engine/src/rgbmatrix.h                    -- RGBMatrix XML constants
    engine/src/rgbalgorithm.cpp              -- Algorithm base class
    engine/src/mastertimer.cpp               -- stopAllFunctions(), fadeAndStopAll()

---

## RGBMatrix Algorithm Built-in Names (engine/src/rgbalgorithm.cpp)

These are the exact algorithm names QLC+ recognizes for built-in RGBMatrix effects:

    Full Columns
    Full Rows
    Alternate
    Even/Odd
    Gradient
    Waves
    Fill
    Fill Unfill
    Fill From Center
    Marquee
    Plasma
    Random Single
    Random Column
    Random Row
    Spiral
    Noise
    Sine Wave
    Fireworks
    Balls
    Balls (Colors)
    Text
    Image
    Audio

Direction property (for algorithms that support it, e.g. Waves):
  Values: "Left", "Right", "Up", "Down"
  Set via algorithm property, NOT the global Direction element.

Global Direction element (for algorithms like Fill, Marquee, Sine Wave):
  Values: "Forward", "Backward"
  Set via <Direction>Forward</Direction> or <Direction>Backward</Direction>
