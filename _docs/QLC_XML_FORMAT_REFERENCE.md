# QLC+ Workspace XML Format Reference (v4/5.x)

> **Extracted from**: `qlcplus-QLC-_5.2.1 Source Code`
> **Source files**: `ui/src/virtualconsole/*.cpp`, `engine/src/*.cpp`
> **Generated**: 2026-04-14

This document is the definitive reference for programmatically generating QLC+ workspace (`.qxw`) files.
All XML tag names, attribute names, and valid values are extracted directly from source code.

---

## Table of Contents

1. [Global Constants & Conventions](#1-global-constants--conventions)
2. [Function Common Elements](#2-function-common-elements)
3. [Scene Function](#3-scene-function)
4. [Chaser Function](#4-chaser-function)
5. [Collection Function](#5-collection-function)
6. [RGBMatrix Function](#6-rgbmatrix-function)
7. [EFX Function](#7-efx-function)
8. [Virtual Console Common (VCWidget)](#8-virtual-console-common-vcwidget)
9. [VCButton](#9-vcbutton)
10. [VCSlider](#10-vcslider)
11. [VCFrame](#11-vcframe)
12. [VCSoloFrame](#12-vcsoloframe)
13. [VCSpeedDial](#13-vcspeeddial)
14. [Complete Workspace File Structure](#14-complete-workspace-file-structure)

---

## 1. Global Constants & Conventions

### Boolean Values

| Constant | XML String |
|----------|-----------|
| `KXMLQLCTrue` | `"True"` |
| `KXMLQLCFalse` | `"False"` |

### Special Speed Values

| Constant | Value | Meaning |
|----------|-------|---------|
| `Function::infiniteSpeed()` | `4294967294` (0xFFFFFFFE / `(uint)-2`) | Infinite duration |
| `Function::defaultSpeed()` | `4294967295` (0xFFFFFFFF / `(uint)-1`) | Use default speed |
| `Function::invalidId()` | `4294967295` (0xFFFFFFFF / `UINT_MAX`) | No function assigned |

### Function Type Strings

Used in `<Function Type="...">` attribute:

| Enum | XML String |
|------|-----------|
| `SceneType` | `"Scene"` |
| `ChaserType` | `"Chaser"` |
| `EFXType` | `"EFX"` |
| `CollectionType` | `"Collection"` |
| `ScriptType` | `"Script"` |
| `RGBMatrixType` | `"RGBMatrix"` |
| `ShowType` | `"Show"` |
| `SequenceType` | `"Sequence"` |
| `AudioType` | `"Audio"` |
| `VideoType` | `"Video"` |

### Direction Strings

Used in `<Direction>` element text:

| Enum | XML String |
|------|-----------|
| `Forward` | `"Forward"` |
| `Backward` | `"Backward"` |

### Run Order Strings

Used in `<RunOrder>` element text:

| Enum | XML String |
|------|-----------|
| `Loop` | `"Loop"` |
| `PingPong` | `"PingPong"` |
| `SingleShot` | `"SingleShot"` |
| `Random` | `"Random"` |

### Tempo Type Strings

Used in `<Tempo>` element text:

| Enum | XML String |
|------|-----------|
| `Time` | `"Time"` |
| `Beats` | `"Beats"` |

### Frame Style Strings

Used in `<FrameStyle>` element text within `<Appearance>`:

| Constant | XML String |
|----------|-----------|
| `KVCFrameStyleSunken` | `"Sunken"` |
| `KVCFrameStyleRaised` | `"Raised"` |
| `KVCFrameStyleNone` | `"None"` |

---

## 2. Function Common Elements

All functions (`Scene`, `Chaser`, `Collection`, `EFX`, `RGBMatrix`, etc.) share this structure.

### Function Tag & Attributes (saveXMLCommon)

```xml
<Function ID="0" Type="Scene" Name="My Scene" Hidden="True" Path="Folder/Subfolder" BlendMode="...">
  ...
</Function>
```

| Attribute | XML Name | Required | Description |
|-----------|----------|----------|-------------|
| ID | `"ID"` | Yes | Unique function ID (quint32) |
| Type | `"Type"` | Yes | Function type string (see table above) |
| Name | `"Name"` | Yes | Human-readable name |
| Hidden | `"Hidden"` | No | `"True"` if function is hidden (used for Sequence bound scenes). Omitted if visible. |
| Path | `"Path"` | No | Folder path for organization. Omitted if empty. |
| BlendMode | `"BlendMode"` | No | Universe blend mode. Omitted if `NormalBlend`. |

### Speed Element

```xml
<Speed FadeIn="0" FadeOut="0" Duration="0" />
```

| Attribute | XML Name | Type | Description |
|-----------|----------|------|-------------|
| FadeIn | `"FadeIn"` | uint (ms) | Fade in time in milliseconds |
| FadeOut | `"FadeOut"` | uint (ms) | Fade out time in milliseconds |
| Duration | `"Duration"` | uint (ms) | Duration/hold time in milliseconds |

Self-closing element. All values are in **milliseconds**. Use `4294967294` for infinite, `4294967295` for default.

### Direction Element

```xml
<Direction>Forward</Direction>
```

Text content: `"Forward"` or `"Backward"`.

### Run Order Element

```xml
<RunOrder>Loop</RunOrder>
```

Text content: `"Loop"`, `"PingPong"`, `"SingleShot"`, or `"Random"`.

### Tempo Type Element

```xml
<Tempo>Time</Tempo>
```

Text content: `"Time"` or `"Beats"`. **Only written if `Beats`** (omitted for Time to save space).

---

## 3. Scene Function

**Source**: `engine/src/scene.cpp`, `engine/src/scene.h`

### XML Structure

```xml
<Function ID="0" Type="Scene" Name="My Scene">
  <Tempo>Time</Tempo>
  <Speed FadeIn="0" FadeOut="0" Duration="0" />
  <ChannelGroupsVal>id1,val1,id2,val2,...</ChannelGroupsVal>
  <FixtureVal ID="0">0,255,1,128,2,0</FixtureVal>
  <FixtureVal ID="1">0,255,3,200</FixtureVal>
  <FixtureGroup ID="0" />
  <Palette ID="0" />
</Function>
```

### Scene-Specific Elements

#### FixtureVal (new style - preferred)

```xml
<FixtureVal ID="0">channel,value,channel,value,...</FixtureVal>
```

| Attribute | XML Name | Description |
|-----------|----------|-------------|
| ID | `"ID"` | Fixture ID (quint32) |

**Text content**: Comma-separated pairs of `channel,value` where channel is the fixture channel number (0-based) and value is 0-255.

#### ChannelGroupsVal

```xml
<ChannelGroupsVal>groupId1,level1,groupId2,level2,...</ChannelGroupsVal>
```

**Text content**: Comma-separated pairs of `channelGroupId,level`.

#### FixtureGroup (reference)

```xml
<FixtureGroup ID="0" />
```

Self-closing element referencing a fixture group by ID.

#### Palette (reference)

```xml
<Palette ID="0" />
```

Self-closing element referencing a palette by ID.

#### Value (legacy style)

```xml
<Value Fixture="0" Channel="1">128</Value>
```

Legacy per-value format. The new `FixtureVal` style is preferred.

### Complete Scene Example

```xml
<Function ID="0" Type="Scene" Name="All Red">
  <Speed FadeIn="1000" FadeOut="500" Duration="0" />
  <FixtureVal ID="0">0,255,1,0,2,0</FixtureVal>
  <FixtureVal ID="1">0,255,1,0,2,0</FixtureVal>
</Function>
```

---

## 4. Chaser Function

**Source**: `engine/src/chaser.cpp`, `engine/src/chaser.h`

### XML Structure

```xml
<Function ID="1" Type="Chaser" Name="My Chaser">
  <Tempo>Time</Tempo>
  <Speed FadeIn="0" FadeOut="0" Duration="5000" />
  <Direction>Forward</Direction>
  <RunOrder>Loop</RunOrder>
  <SpeedModes FadeIn="Default" FadeOut="Default" Duration="Common" />
  <Step Number="0" FadeIn="0" Hold="1000" FadeOut="0" Note="">0</Step>
  <Step Number="1" FadeIn="500" Hold="2000" FadeOut="500" Note="Step note">1</Step>
</Function>
```

### Chaser-Specific Elements

#### SpeedModes

```xml
<SpeedModes FadeIn="Default" FadeOut="Default" Duration="Common" />
```

| Attribute | XML Name | Valid Values | Description |
|-----------|----------|-------------|-------------|
| FadeIn | `"FadeIn"` | `"Common"`, `"PerStep"`, `"Default"` | Fade-in speed mode |
| FadeOut | `"FadeOut"` | `"Common"`, `"PerStep"`, `"Default"` | Fade-out speed mode |
| Duration | `"Duration"` | `"Common"`, `"PerStep"`, `"Default"` | Duration speed mode |

**Speed Mode Values**:
- `"Common"` — Use the chaser's common speed settings
- `"PerStep"` — Each step has its own speed
- `"Default"` — Use the function's own speed settings

#### Step

```xml
<Step Number="0" FadeIn="0" Hold="1000" FadeOut="0" Note="">0</Step>
```

| Attribute | XML Name | Type | Description |
|-----------|----------|------|-------------|
| Number | `"Number"` | int | Step index (0-based) |
| FadeIn | `"FadeIn"` | uint (ms) | Per-step fade in |
| Hold | `"Hold"` | uint (ms) | Per-step hold |
| FadeOut | `"FadeOut"` | uint (ms) | Per-step fade out |
| Note | `"Note"` | string | Optional text note |

**Text content**: The function ID (quint32) to run for this step.

For Chaser steps, the text content may also include scene value overrides in the format:
`functionId:ch1,val1,ch2,val2,...` (for sequence-style steps).

### Complete Chaser Example

```xml
<Function ID="1" Type="Chaser" Name="Color Chase">
  <Speed FadeIn="500" FadeOut="500" Duration="2000" />
  <Direction>Forward</Direction>
  <RunOrder>Loop</RunOrder>
  <SpeedModes FadeIn="Common" FadeOut="Common" Duration="Common" />
  <Step Number="0" FadeIn="0" Hold="0" FadeOut="0" Note="">0</Step>
  <Step Number="1" FadeIn="0" Hold="0" FadeOut="0" Note="">2</Step>
  <Step Number="2" FadeIn="0" Hold="0" FadeOut="0" Note="">3</Step>
</Function>
```

---

## 5. Collection Function

**Source**: `engine/src/collection.cpp`

### XML Structure

```xml
<Function ID="2" Type="Collection" Name="My Collection">
  <Step Number="0">0</Step>
  <Step Number="1">1</Step>
  <Step Number="2">5</Step>
</Function>
```

### Collection-Specific Elements

#### Step

```xml
<Step Number="0">5</Step>
```

| Attribute | XML Name | Description |
|-----------|----------|-------------|
| Number | `"Number"` | Step index (0-based, sequential) |

**Text content**: Function ID (quint32) of the member function.

All functions in a collection run **simultaneously** when the collection is started.

### Complete Collection Example

```xml
<Function ID="10" Type="Collection" Name="Full Show">
  <Step Number="0">0</Step>
  <Step Number="1">1</Step>
  <Step Number="2">5</Step>
</Function>
```

---

## 6. RGBMatrix Function

**Source**: `engine/src/rgbmatrix.cpp`, `engine/src/rgbmatrix.h`

### XML Structure

```xml
<Function ID="3" Type="RGBMatrix" Name="My Matrix">
  <Tempo>Time</Tempo>
  <Speed FadeIn="0" FadeOut="0" Duration="500" />
  <Direction>Forward</Direction>
  <RunOrder>Loop</RunOrder>
  <Algorithm Type="Script">Stripes</Algorithm>
  <DimmerControl>1</DimmerControl>
  <Color Index="0">4294901760</Color>
  <Color Index="1">4278190335</Color>
  <ControlMode>RGB</ControlMode>
  <FixtureGroup>0</FixtureGroup>
  <Property Name="orientation" Value="Horizontal" />
</Function>
```

### RGBMatrix-Specific Elements

#### FixtureGroup

```xml
<FixtureGroup>0</FixtureGroup>
```

**Text content**: Fixture group ID (quint32).

#### Algorithm

```xml
<Algorithm Type="Script">Stripes</Algorithm>
```

The algorithm element is written by `RGBAlgorithm::saveXML()`. The `Type` attribute is one of:
- `"Script"` — RGBScript (text content is the script name)
- `"Plain"` — Plain color fill
- `"Text"` — Text display
- `"Image"` — Image display
- `"Audio"` — Audio spectrum

#### Color (new multi-color style)

```xml
<Color Index="0">4294901760</Color>
<Color Index="1">4278190335</Color>
```

| Attribute | XML Name | Description |
|-----------|----------|-------------|
| Index | `"Index"` | Color index (0 = start/mono, 1 = end, etc.) |

**Text content**: QRgb value as unsigned integer.

#### Legacy Color Elements

```xml
<MonoColor>4294901760</MonoColor>
<EndColor>4278190335</EndColor>
```

#### DimmerControl

```xml
<DimmerControl>1</DimmerControl>
```

**Text content**: `0` or `1`. Controls whether dimmer channels are managed.

#### ControlMode

```xml
<ControlMode>RGB</ControlMode>
```

**Text content** (valid values):
| String | Description |
|--------|-------------|
| `"RGB"` | Control RGB channels |
| `"Amber"` | Control amber channel |
| `"White"` | Control white channel |
| `"UV"` | Control UV channel |
| `"Dimmer"` | Control dimmer channel |
| `"Shutter"` | Control shutter channel |

#### Property

```xml
<Property Name="orientation" Value="Horizontal" />
```

| Attribute | XML Name | Description |
|-----------|----------|-------------|
| Name | `"Name"` | Property name |
| Value | `"Value"` | Property value |

### Complete RGBMatrix Example

```xml
<Function ID="3" Type="RGBMatrix" Name="Rainbow Stripes">
  <Speed FadeIn="0" FadeOut="0" Duration="50" />
  <Direction>Forward</Direction>
  <RunOrder>Loop</RunOrder>
  <Algorithm Type="Script">Stripes</Algorithm>
  <Color Index="0">4294901760</Color>
  <Color Index="1">4278255360</Color>
  <ControlMode>RGB</ControlMode>
  <FixtureGroup>0</FixtureGroup>
  <Property Name="orientation" Value="Horizontal" />
</Function>
```

---

## 7. EFX Function

**Source**: `engine/src/efx.cpp`, `engine/src/efx.h`, `engine/src/efxfixture.h`

### XML Structure

```xml
<Function ID="4" Type="EFX" Name="My EFX">
  <Fixture>
    <ID>0</ID>
    <Head>0</Head>
    <Mode>Position</Mode>
    <Direction>Forward</Direction>
    <StartOffset>0</StartOffset>
    <Intensity>255</Intensity>
  </Fixture>
  <PropagationMode>Parallel</PropagationMode>
  <Tempo>Time</Tempo>
  <Speed FadeIn="0" FadeOut="0" Duration="20000" />
  <Direction>Forward</Direction>
  <RunOrder>Loop</RunOrder>
  <Algorithm>Circle</Algorithm>
  <Width>127</Width>
  <Height>127</Height>
  <Rotation>0</Rotation>
  <StartOffset>0</StartOffset>
  <IsRelative>0</IsRelative>
  <Axis Name="X">
    <Offset>127</Offset>
    <Frequency>2</Frequency>
    <Phase>90</Phase>
  </Axis>
  <Axis Name="Y">
    <Offset>127</Offset>
    <Frequency>3</Frequency>
    <Phase>0</Phase>
  </Axis>
</Function>
```

### EFX-Specific Elements

#### Fixture (EFXFixture)

```xml
<Fixture>
  <ID>0</ID>
  <Head>0</Head>
  <Mode>Position</Mode>
  <Direction>Forward</Direction>
  <StartOffset>0</StartOffset>
  <Intensity>255</Intensity>
</Fixture>
```

| Child Tag | XML Name | Description |
|-----------|----------|-------------|
| ID | `"ID"` | Fixture ID |
| Head | `"Head"` | Fixture head index |
| Mode | `"Mode"` | Fixture mode (see below) |
| Direction | `"Direction"` | `"Forward"` or `"Backward"` |
| StartOffset | `"StartOffset"` | Phase offset in degrees (0-359) |
| Intensity | `"Intensity"` | Intensity value (0-255) |

**Fixture Mode values**:
| String | Description |
|--------|-------------|
| `"Position"` | Pan/Tilt movement mode |
| `"Dimmer"` | Dimmer control mode |
| `"RGB"` | RGB color control mode |

#### PropagationMode

```xml
<PropagationMode>Parallel</PropagationMode>
```

**Text content**:
| String | Description |
|--------|-------------|
| `"Parallel"` | All fixtures move together |
| `"Serial"` | Fixtures follow each other with delay |
| `"Asymmetric"` | Asymmetric movement |

#### Algorithm

```xml
<Algorithm>Circle</Algorithm>
```

**Text content** (valid values):
| String |
|--------|
| `"Circle"` |
| `"Eight"` |
| `"Line"` |
| `"Line2"` |
| `"Diamond"` |
| `"Square"` |
| `"SquareChoppy"` |
| `"SquareTrue"` |
| `"Leaf"` |
| `"Lissajous"` |

#### Width, Height, Rotation, StartOffset, IsRelative

```xml
<Width>127</Width>
<Height>127</Height>
<Rotation>0</Rotation>
<StartOffset>0</StartOffset>
<IsRelative>0</IsRelative>
```

| Element | Range | Description |
|---------|-------|-------------|
| `Width` | 0-127 | Pattern width |
| `Height` | 0-127 | Pattern height |
| `Rotation` | 0-359 | Pattern rotation in degrees |
| `StartOffset` | 0-359 | Start offset in degrees |
| `IsRelative` | 0 or 1 | Whether EFX is relative to fixture's current position |

#### Axis

```xml
<Axis Name="X">
  <Offset>127</Offset>
  <Frequency>2</Frequency>
  <Phase>90</Phase>
</Axis>
```

| Attribute | XML Name | Description |
|-----------|----------|-------------|
| Name | `"Name"` | `"X"` or `"Y"` |

| Child Tag | Description |
|-----------|-------------|
| `Offset` | Center offset (0-255, default 127) |
| `Frequency` | Frequency value (integer) |
| `Phase` | Phase value in degrees |

### Complete EFX Example

```xml
<Function ID="4" Type="EFX" Name="Circle Pan/Tilt">
  <Fixture>
    <ID>0</ID>
    <Head>0</Head>
    <Mode>Position</Mode>
    <Direction>Forward</Direction>
    <StartOffset>0</StartOffset>
    <Intensity>255</Intensity>
  </Fixture>
  <Fixture>
    <ID>1</ID>
    <Head>0</Head>
    <Mode>Position</Mode>
    <Direction>Forward</Direction>
    <StartOffset>90</StartOffset>
    <Intensity>255</Intensity>
  </Fixture>
  <PropagationMode>Parallel</PropagationMode>
  <Speed FadeIn="2000" FadeOut="2000" Duration="20000" />
  <Direction>Forward</Direction>
  <RunOrder>Loop</RunOrder>
  <Algorithm>Circle</Algorithm>
  <Width>127</Width>
  <Height>127</Height>
  <Rotation>0</Rotation>
  <StartOffset>0</StartOffset>
  <IsRelative>0</IsRelative>
  <Axis Name="X">
    <Offset>127</Offset>
    <Frequency>2</Frequency>
    <Phase>90</Phase>
  </Axis>
  <Axis Name="Y">
    <Offset>127</Offset>
    <Frequency>3</Frequency>
    <Phase>0</Phase>
  </Axis>
</Function>
```

---

## 8. Virtual Console Common (VCWidget)

**Source**: `ui/src/virtualconsole/vcwidget.cpp`, `vcwidget.h`

All VC widgets share common attributes and child elements.

### Widget Common Attributes (loadXMLCommon)

These attributes appear on the widget's top-level tag (e.g., `<Button>`, `<Slider>`, `<Frame>`):

| Attribute | XML Name | Required | Description |
|-----------|----------|----------|-------------|
| Caption | `"Caption"` | Yes | Widget display name |
| ID | `"ID"` | Yes | Unique widget ID (quint32). `UINT_MAX` = invalid. |
| Page | `"Page"` | No | Multipage frame page number (0-based). Only written if not 0. |

### WindowState Element

```xml
<WindowState Visible="True" X="10" Y="20" Width="100" Height="50" />
```

| Attribute | XML Name | Type | Description |
|-----------|----------|------|-------------|
| Visible | `"Visible"` | `"True"/"False"` | Widget visibility |
| X | `"X"` | int | X position |
| Y | `"Y"` | int | Y position |
| Width | `"Width"` | int | Width in pixels |
| Height | `"Height"` | int | Height in pixels |

Self-closing element.

### Appearance Element

```xml
<Appearance>
  <FrameStyle>None</FrameStyle>
  <ForegroundColor>Default</ForegroundColor>
  <BackgroundColor>Default</BackgroundColor>
  <BackgroundImage>None</BackgroundImage>
  <Font>Default</Font>
</Appearance>
```

| Child Tag | XML Name | Description |
|-----------|----------|-------------|
| FrameStyle | `"FrameStyle"` | `"None"`, `"Sunken"`, or `"Raised"` |
| ForegroundColor | `"ForegroundColor"` | `"Default"` or QRgb unsigned int |
| BackgroundColor | `"BackgroundColor"` | `"Default"` or QRgb unsigned int |
| BackgroundImage | `"BackgroundImage"` | `"None"` or file path |
| Font | `"Font"` | `"Default"` or Qt font description string |

### Input Element

```xml
<Input Universe="0" Channel="5" LowerValue="0" UpperValue="255" MonitorValue="255" LowerParams="1" UpperParams="1" MonitorParams="1" />
```

| Attribute | XML Name | Required | Description |
|-----------|----------|----------|-------------|
| Universe | `"Universe"` | Yes | Input universe number (0-based) |
| Channel | `"Channel"` | Yes | Input channel number |
| LowerValue | `"LowerValue"` | No | Feedback lower value (default 0) |
| UpperValue | `"UpperValue"` | No | Feedback upper value (default 255) |
| MonitorValue | `"MonitorValue"` | No | Feedback monitor value (default 255) |
| LowerParams | `"LowerParams"` | No | Extra feedback params for lower |
| UpperParams | `"UpperParams"` | No | Extra feedback params for upper |
| MonitorParams | `"MonitorParams"` | No | Extra feedback params for monitor |

Self-closing element.

### Key Element

```xml
<Key>A</Key>
```

**Text content**: Qt key sequence string (e.g., `"A"`, `"Shift+F1"`, etc.).

---

## 9. VCButton

**Source**: `ui/src/virtualconsole/vcbutton.cpp`, `vcbutton.h`

### Tag Name: `"Button"`

### XML Structure

```xml
<Button Caption="My Button" ID="0" Page="0" Icon="/path/to/icon.png">
  <WindowState Visible="True" X="10" Y="20" Width="50" Height="50" />
  <Appearance>
    <FrameStyle>None</FrameStyle>
    <ForegroundColor>Default</ForegroundColor>
    <BackgroundColor>Default</BackgroundColor>
    <BackgroundImage>None</BackgroundImage>
    <Font>Default</Font>
  </Appearance>
  <Function ID="0" />
  <Action FadeOut="1000" Override="0" ForceLTP="0">Toggle</Action>
  <Key>A</Key>
  <Intensity Adjust="True">100</Intensity>
  <Input Universe="0" Channel="5" />
</Button>
```

### Button-Specific Attributes

| Attribute | XML Name | On Tag | Description |
|-----------|----------|--------|-------------|
| Icon | `"Icon"` | `<Button>` | Path to icon image file. Empty string if none. |

### Button-Specific Child Elements

#### Function

```xml
<Function ID="0" />
```

| Attribute | Description |
|-----------|-------------|
| `ID` | The function ID attached to this button. `4294967295` = none. |

Self-closing element.

#### Action

```xml
<Action FadeOut="1000" Override="0" ForceLTP="0">Toggle</Action>
```

**Text content** (valid values):
| String | Description |
|--------|-------------|
| `"Toggle"` | Toggle function on/off (default) |
| `"Flash"` | Flash function while held |
| `"Blackout"` | Toggle blackout |
| `"StopAll"` | Stop all running functions |

**Optional attributes** (context-dependent):

| Attribute | XML Name | When | Description |
|-----------|----------|------|-------------|
| FadeOut | `"FadeOut"` | `StopAll` action | Fade-out time in ms for stop all |
| Override | `"Override"` | `Flash` action | `0`/`1` — flash overrides other faders |
| ForceLTP | `"ForceLTP"` | `Flash` action | `0`/`1` — force LTP behavior on flash |

#### Key

```xml
<Key>A</Key>
```

**Text content**: Key sequence string.

#### Intensity

```xml
<Intensity Adjust="True">100</Intensity>
```

| Attribute | XML Name | Description |
|-----------|----------|-------------|
| Adjust | `"Adjust"` | `"True"` or `"False"` — whether startup intensity is enabled |

**Text content**: Intensity percentage as integer (0-100). Stored internally as `value / 100.0` (so 100 = 1.0).

### Complete VCButton Example

```xml
<Button Caption="Scene 1" ID="0" Icon="">
  <WindowState Visible="True" X="10" Y="10" Width="50" Height="50" />
  <Appearance>
    <FrameStyle>None</FrameStyle>
    <ForegroundColor>Default</ForegroundColor>
    <BackgroundColor>Default</BackgroundColor>
    <BackgroundImage>None</BackgroundImage>
    <Font>Default</Font>
  </Appearance>
  <Function ID="0" />
  <Action>Toggle</Action>
  <Intensity Adjust="False">100</Intensity>
  <Input Universe="0" Channel="0" />
</Button>
```

---

## 10. VCSlider

**Source**: `ui/src/virtualconsole/vcslider.cpp`, `vcslider.h`

### Tag Name: `"Slider"`

### XML Structure

```xml
<Slider Caption="Dimmer" ID="1" WidgetStyle="Slider" InvertedAppearance="false" CatchValues="true">
  <WindowState Visible="True" X="70" Y="10" Width="60" Height="200" />
  <Appearance>...</Appearance>
  <Input Universe="0" Channel="1" />
  <SliderMode ValueDisplayStyle="Exact" ClickAndGoType="None" Monitor="false">Level</SliderMode>
  <Reset>
    <Key>R</Key>
    <Input Universe="0" Channel="10" />
  </Reset>
  <Level LowLimit="0" HighLimit="255" Value="0">
    <Channel Fixture="0">0</Channel>
    <Channel Fixture="0">1</Channel>
    <Channel Fixture="1">0</Channel>
  </Level>
  <Playback>
    <Function>0</Function>
    <Flash>
      <Key>F</Key>
      <Input Universe="0" Channel="11" />
    </Flash>
  </Playback>
</Slider>
```

### Slider-Specific Attributes (on `<Slider>` tag)

| Attribute | XML Name | Required | Description |
|-----------|----------|----------|-------------|
| WidgetStyle | `"WidgetStyle"` | No | `"Slider"` or `"Knob"` (default: `"Slider"`) |
| InvertedAppearance | `"InvertedAppearance"` | Yes | `"true"` or `"false"` |
| CatchValues | `"CatchValues"` | No | `"true"` if value catching is enabled. Omitted if false. |

### Slider-Specific Child Elements

#### SliderMode

```xml
<SliderMode ValueDisplayStyle="Exact" ClickAndGoType="None" Monitor="false">Level</SliderMode>
```

| Attribute | XML Name | Description |
|-----------|----------|-------------|
| ValueDisplayStyle | `"ValueDisplayStyle"` | `"Exact"` or `"Percentage"` |
| ClickAndGoType | `"ClickAndGoType"` | `"None"`, `"RGB"`, `"CMY"`, `"Preset"` |
| Monitor | `"Monitor"` | `"true"` or `"false"` (only for Level mode) |

**Text content** (slider mode):
| String | Description |
|--------|-------------|
| `"Level"` | Direct channel level control |
| `"Playback"` | Function playback intensity |
| `"Submaster"` | Submaster fader for parent frame |

#### Reset (Override Reset)

```xml
<Reset>
  <Key>R</Key>
  <Input Universe="0" Channel="10" />
</Reset>
```

Contains optional `<Key>` and/or `<Input>` for the override reset button. Only present when Level mode with Monitor enabled.

#### Level

```xml
<Level LowLimit="0" HighLimit="255" Value="0">
  <Channel Fixture="0">0</Channel>
  <Channel Fixture="0">1</Channel>
</Level>
```

| Attribute | XML Name | Description |
|-----------|----------|-------------|
| LowLimit | `"LowLimit"` | Minimum value (0-255, default 0) |
| HighLimit | `"HighLimit"` | Maximum value (0-255, default 255) |
| Value | `"Value"` | Current value (0-255) |

##### Channel (within Level)

```xml
<Channel Fixture="0">2</Channel>
```

| Attribute | XML Name | Description |
|-----------|----------|-------------|
| Fixture | `"Fixture"` | Fixture ID |

**Text content**: Channel number (0-based) within the fixture.

#### Playback

```xml
<Playback>
  <Function>5</Function>
  <Flash>
    <Key>F</Key>
    <Input Universe="0" Channel="11" />
  </Flash>
</Playback>
```

##### Function (within Playback)

```xml
<Function>5</Function>
```

**Text content**: Function ID. `4294967295` = none.

##### Flash (within Playback)

```xml
<Flash>
  <Key>F</Key>
  <Input Universe="0" Channel="11" />
</Flash>
```

Enables the flash button. Contains optional `<Key>` and/or `<Input>` elements. Presence of this element = flash is enabled.

### Complete VCSlider Examples

#### Level Mode Slider

```xml
<Slider Caption="Par Dimmer" ID="1" WidgetStyle="Slider" InvertedAppearance="false">
  <WindowState Visible="True" X="70" Y="10" Width="60" Height="200" />
  <Appearance>
    <FrameStyle>Sunken</FrameStyle>
    <ForegroundColor>Default</ForegroundColor>
    <BackgroundColor>Default</BackgroundColor>
    <BackgroundImage>None</BackgroundImage>
    <Font>Default</Font>
  </Appearance>
  <Input Universe="0" Channel="1" />
  <SliderMode ValueDisplayStyle="Exact" ClickAndGoType="None" Monitor="false">Level</SliderMode>
  <Level LowLimit="0" HighLimit="255" Value="0">
    <Channel Fixture="0">0</Channel>
  </Level>
  <Playback>
    <Function>4294967295</Function>
  </Playback>
</Slider>
```

#### Playback Mode Slider

```xml
<Slider Caption="Chase 1" ID="2" WidgetStyle="Slider" InvertedAppearance="false">
  <WindowState Visible="True" X="140" Y="10" Width="60" Height="200" />
  <Appearance>
    <FrameStyle>Sunken</FrameStyle>
    <ForegroundColor>Default</ForegroundColor>
    <BackgroundColor>Default</BackgroundColor>
    <BackgroundImage>None</BackgroundImage>
    <Font>Default</Font>
  </Appearance>
  <SliderMode ValueDisplayStyle="Exact" ClickAndGoType="None">Playback</SliderMode>
  <Level LowLimit="0" HighLimit="255" Value="0" />
  <Playback>
    <Function>1</Function>
  </Playback>
</Slider>
```

---

## 11. VCFrame

**Source**: `ui/src/virtualconsole/vcframe.cpp`, `vcframe.h`

### Tag Name: `"Frame"`

### XML Structure

```xml
<Frame Caption="Main Frame" ID="0">
  <Appearance>...</Appearance>
  <WindowState Visible="True" X="0" Y="0" Width="400" Height="300" />
  <AllowChildren>True</AllowChildren>
  <AllowResize>True</AllowResize>
  <ShowHeader>True</ShowHeader>
  <ShowEnableButton>True</ShowEnableButton>
  <Collapsed>False</Collapsed>
  <Disabled>False</Disabled>
  <Enable>
    <Key>E</Key>
    <Input Universe="0" Channel="20" />
  </Enable>
  <Multipage PagesNum="3" CurrentPage="0" />
  <Next>
    <Key>N</Key>
    <Input Universe="0" Channel="21" />
  </Next>
  <Previous>
    <Key>P</Key>
    <Input Universe="0" Channel="22" />
  </Previous>
  <Shortcut Page="0" Name="Page 1">
    <Key>1</Key>
    <Input Universe="0" Channel="30" />
  </Shortcut>
  <Shortcut Page="1" Name="Page 2">
    <Key>2</Key>
    <Input Universe="0" Channel="31" />
  </Shortcut>
  <PagesLoop>False</PagesLoop>
  <!-- Child widgets go here -->
  <Button Caption="Button 1" ID="1" Icon="">...</Button>
  <Slider Caption="Slider 1" ID="2" ...>...</Slider>
</Frame>
```

### Frame-Specific Child Elements

#### AllowChildren

```xml
<AllowChildren>True</AllowChildren>
```

**Text content**: `"True"` or `"False"`.

#### AllowResize

```xml
<AllowResize>True</AllowResize>
```

**Text content**: `"True"` or `"False"`.

#### ShowHeader

```xml
<ShowHeader>True</ShowHeader>
```

**Text content**: `"True"` or `"False"`. Controls visibility of the collapse/label header bar.

#### ShowEnableButton

```xml
<ShowEnableButton>True</ShowEnableButton>
```

**Text content**: `"True"` or `"False"`. Controls visibility of the enable/disable button in the header.

#### Collapsed

```xml
<Collapsed>False</Collapsed>
```

**Text content**: `"True"` or `"False"`.

#### Disabled

```xml
<Disabled>False</Disabled>
```

**Text content**: `"True"` or `"False"`.

#### Enable (enable source)

```xml
<Enable>
  <Key>E</Key>
  <Input Universe="0" Channel="20" />
</Enable>
```

Contains optional `<Key>` and/or `<Input>` for the enable/disable toggle.

#### Multipage

```xml
<Multipage PagesNum="3" CurrentPage="0" />
```

| Attribute | XML Name | Description |
|-----------|----------|-------------|
| PagesNum | `"PagesNum"` | Total number of pages |
| CurrentPage | `"CurrentPage"` | Currently active page (0-based) |

Self-closing element. Presence enables multipage mode.

#### Next (next page source)

```xml
<Next>
  <Key>N</Key>
  <Input Universe="0" Channel="21" />
</Next>
```

Contains optional `<Key>` and/or `<Input>` for next page.

#### Previous (previous page source)

```xml
<Previous>
  <Key>P</Key>
  <Input Universe="0" Channel="22" />
</Previous>
```

Contains optional `<Key>` and/or `<Input>` for previous page.

#### Shortcut (page shortcut)

```xml
<Shortcut Page="0" Name="Page 1">
  <Key>1</Key>
  <Input Universe="0" Channel="30" />
</Shortcut>
```

| Attribute | XML Name | Description |
|-----------|----------|-------------|
| Page | `"Page"` | Page index (0-based) |
| Name | `"Name"` | Display name for this page |

Contains optional `<Key>` and/or `<Input>` for direct page access.
One `<Shortcut>` per page. Number of shortcuts must equal `PagesNum`.

#### PagesLoop

```xml
<PagesLoop>False</PagesLoop>
```

**Text content**: `"True"` or `"False"`. Whether page navigation wraps around.

### Child Widget Types (loaded inside Frame)

The frame can contain these child widget tags:
- `<Frame>` — nested VCFrame
- `<Button>` — VCButton
- `<Slider>` — VCSlider
- `<SoloFrame>` — VCSoloFrame
- `<SpeedDial>` — VCSpeedDial
- `<CueList>` — VCCueList
- `<XYPad>` — VCXYPad
- `<Label>` — VCLabel
- `<AudioTriggers>` — VCAudioTriggers
- `<Clock>` — VCClock
- `<Matrix>` — VCMatrix

### Bottom Frame Note

The top-level frame (direct child of `<VirtualConsole>`) is the "bottom frame". It does **not** save:
- WindowState, AllowChildren, AllowResize, ShowHeader, ShowEnableButton
- Collapsed, Disabled, Enable, Multipage, Next, Previous, Shortcuts, PagesLoop

Only its Appearance and child widgets are saved.

### Complete VCFrame Example

```xml
<Frame Caption="Control" ID="5">
  <Appearance>
    <FrameStyle>Sunken</FrameStyle>
    <ForegroundColor>Default</ForegroundColor>
    <BackgroundColor>Default</BackgroundColor>
    <BackgroundImage>None</BackgroundImage>
    <Font>Default</Font>
  </Appearance>
  <WindowState Visible="True" X="10" Y="10" Width="300" Height="250" />
  <AllowChildren>True</AllowChildren>
  <AllowResize>True</AllowResize>
  <ShowHeader>True</ShowHeader>
  <ShowEnableButton>True</ShowEnableButton>
  <Collapsed>False</Collapsed>
  <Disabled>False</Disabled>
  <Button Caption="Scene 1" ID="6" Icon="">
    <WindowState Visible="True" X="10" Y="40" Width="50" Height="50" />
    <Appearance>
      <FrameStyle>None</FrameStyle>
      <ForegroundColor>Default</ForegroundColor>
      <BackgroundColor>Default</BackgroundColor>
      <BackgroundImage>None</BackgroundImage>
      <Font>Default</Font>
    </Appearance>
    <Function ID="0" />
    <Action>Toggle</Action>
    <Intensity Adjust="False">100</Intensity>
  </Button>
</Frame>
```

---

## 12. VCSoloFrame

**Source**: `ui/src/virtualconsole/vcsoloframe.cpp`, `vcsoloframe.h`

### Tag Name: `"SoloFrame"`

A SoloFrame inherits everything from VCFrame. It uses the **same `loadXML` method** as VCFrame (via `VCFrame::loadXML`) but with `xmlTagName()` returning `"SoloFrame"`.

### Additional SoloFrame Elements

These are parsed inside VCFrame's loadXML when the widget type is `SoloFrameWidget`:

#### Mixing

```xml
<Mixing>True</Mixing>
```

**Text content**: `"True"` or `"False"`. When enabled, functions fade out proportionally instead of hard-stopping.

#### ExcludeMonitored

```xml
<ExcludeMonitored>True</ExcludeMonitored>
```

**Text content**: `"True"` or `"False"`. When enabled, monitored (externally started) functions are excluded from solo behavior.

### Complete VCSoloFrame Example

```xml
<SoloFrame Caption="Solo Group" ID="10">
  <Appearance>
    <FrameStyle>Sunken</FrameStyle>
    <ForegroundColor>Default</ForegroundColor>
    <BackgroundColor>Default</BackgroundColor>
    <BackgroundImage>None</BackgroundImage>
    <Font>Default</Font>
  </Appearance>
  <WindowState Visible="True" X="320" Y="10" Width="200" Height="200" />
  <AllowChildren>True</AllowChildren>
  <AllowResize>True</AllowResize>
  <ShowHeader>True</ShowHeader>
  <ShowEnableButton>True</ShowEnableButton>
  <Mixing>False</Mixing>
  <Collapsed>False</Collapsed>
  <Disabled>False</Disabled>
  <Button Caption="Scene A" ID="11" Icon="">
    <WindowState Visible="True" X="10" Y="40" Width="50" Height="50" />
    <Appearance>
      <FrameStyle>None</FrameStyle>
      <ForegroundColor>Default</ForegroundColor>
      <BackgroundColor>Default</BackgroundColor>
      <BackgroundImage>None</BackgroundImage>
      <Font>Default</Font>
    </Appearance>
    <Function ID="0" />
    <Action>Toggle</Action>
    <Intensity Adjust="False">100</Intensity>
  </Button>
  <Button Caption="Scene B" ID="12" Icon="">
    <WindowState Visible="True" X="70" Y="40" Width="50" Height="50" />
    <Appearance>
      <FrameStyle>None</FrameStyle>
      <ForegroundColor>Default</ForegroundColor>
      <BackgroundColor>Default</BackgroundColor>
      <BackgroundImage>None</BackgroundImage>
      <Font>Default</Font>
    </Appearance>
    <Function ID="1" />
    <Action>Toggle</Action>
    <Intensity Adjust="False">100</Intensity>
  </Button>
</SoloFrame>
```

---

## 13. VCSpeedDial

**Source**: `ui/src/virtualconsole/vcspeeddial.cpp`, `vcspeeddial.h`, `vcspeeddialpreset.h`, `vcspeeddialfunction.h`

### Tag Name: `"SpeedDial"`

### XML Structure

```xml
<SpeedDial Caption="Duration" ID="20">
  <WindowState Visible="True" X="10" Y="220" Width="200" Height="175" />
  <Appearance>...</Appearance>
  <Visibility>62</Visibility>
  <AbsoluteValue Minimum="0" Maximum="10000">
    <Input Universe="0" Channel="50" />
  </AbsoluteValue>
  <Tap>
    <Input Universe="0" Channel="51" />
  </Tap>
  <ResetFactorOnDialChange>True</ResetFactorOnDialChange>
  <Mult>
    <Input Universe="0" Channel="52" />
  </Mult>
  <Div>
    <Input Universe="0" Channel="53" />
  </Div>
  <MultDivReset>
    <Input Universe="0" Channel="54" />
  </MultDivReset>
  <Apply>
    <Input Universe="0" Channel="55" />
  </Apply>
  <Time>5000</Time>
  <Key>T</Key>
  <MultKey>M</MultKey>
  <DivKey>D</DivKey>
  <MultDivResetKey>R</MultDivResetKey>
  <ApplyKey>Return</ApplyKey>
  <Function ID="1" FadeInMultiplier="0" FadeOutMultiplier="0" DurationMultiplier="1" />
  <Preset ID="16">
    <Name>∞</Name>
    <Value>4294967294</Value>
    <Key>I</Key>
    <Input Universe="0" Channel="60" />
  </Preset>
</SpeedDial>
```

### SpeedDial-Specific Attributes (on `<SpeedDial>` tag)

| Attribute | XML Name | Required | Description |
|-----------|----------|----------|-------------|
| SpeedTypes | `"SpeedTypes"` | No | Legacy bitfield (1=FadeIn, 2=FadeOut, 4=Duration) |

### SpeedDial-Specific Child Elements

#### Visibility (mask)

```xml
<Visibility>62</Visibility>
```

**Text content**: Bitmask (uint32) controlling visibility of SpeedDial UI elements.

Default visibility mask bits (from `SpeedDial` class):
- Bit 0 (1): Hours
- Bit 1 (2): Minutes
- Bit 2 (4): Seconds
- Bit 3 (8): Milliseconds
- Bit 4 (16): Infinite button (legacy, now handled by presets)
- Bit 5 (32): Tap button
- Bit 6 (64): MultDiv controls (on VCSpeedDial)
- Bit 7 (128): Apply button (on VCSpeedDial)

#### AbsoluteValue

```xml
<AbsoluteValue Minimum="0" Maximum="10000">
  <Input Universe="0" Channel="50" />
</AbsoluteValue>
```

| Attribute | XML Name | Description |
|-----------|----------|-------------|
| Minimum | `"Minimum"` | Min value in ms (default 0) |
| Maximum | `"Maximum"` | Max value in ms (default 10000) |

Contains optional `<Input>` element for absolute value control.

#### Tap

```xml
<Tap>
  <Input Universe="0" Channel="51" />
</Tap>
```

Contains `<Input>` for tap tempo input.

#### Mult, Div, MultDivReset, Apply

```xml
<Mult><Input ... /></Mult>
<Div><Input ... /></Div>
<MultDivReset><Input ... /></MultDivReset>
<Apply><Input ... /></Apply>
```

Each contains optional `<Input>` for the respective control.

#### ResetFactorOnDialChange

```xml
<ResetFactorOnDialChange>True</ResetFactorOnDialChange>
```

**Text content**: `"True"` or `"False"`. Only written if true.

#### Time

```xml
<Time>5000</Time>
```

**Text content**: Current time value in milliseconds (uint).

#### Key Sequences

```xml
<Key>T</Key>
<MultKey>M</MultKey>
<DivKey>D</DivKey>
<MultDivResetKey>R</MultDivResetKey>
<ApplyKey>Return</ApplyKey>
```

Each is optional and only written if the key sequence is non-empty.

#### Function (VCSpeedDialFunction)

```xml
<Function ID="1" FadeInMultiplier="0" FadeOutMultiplier="0" DurationMultiplier="1" />
```

| Attribute | XML Name | Description |
|-----------|----------|-------------|
| ID | `"ID"` | Function ID |
| FadeInMultiplier | `"FadeInMultiplier"` | Multiplier index for fade-in speed |
| FadeOutMultiplier | `"FadeOutMultiplier"` | Multiplier index for fade-out speed |
| DurationMultiplier | `"DurationMultiplier"` | Multiplier index for duration |

**Multiplier index values**:
| Index | Meaning |
|-------|---------|
| 0 | None (not controlled) |
| 1 | 1x (direct) |
| 2 | 0.5x |
| 3 | 1x (same as 1) |
| 4 | 2x |
| 5+ | Higher multipliers |

(See `VCSpeedDialFunction::speedMultiplierValuesTimes1000()` for the full table.)

#### Preset

```xml
<Preset ID="16">
  <Name>∞</Name>
  <Value>4294967294</Value>
  <Key>I</Key>
  <Input Universe="0" Channel="60" />
</Preset>
```

| Attribute | XML Name | Description |
|-----------|----------|-------------|
| ID | `"ID"` | Unique preset ID (quint8) |

| Child Tag | XML Name | Description |
|-----------|----------|-------------|
| Name | `"Name"` | Display name |
| Value | `"Value"` | Time value in ms (uint). Use `4294967294` for infinite. |

Optionally contains `<Key>` and `<Input>` elements.

### Complete VCSpeedDial Example

```xml
<SpeedDial Caption="Chase Speed" ID="20">
  <WindowState Visible="True" X="10" Y="250" Width="200" Height="175" />
  <Appearance>
    <FrameStyle>Sunken</FrameStyle>
    <ForegroundColor>Default</ForegroundColor>
    <BackgroundColor>Default</BackgroundColor>
    <BackgroundImage>None</BackgroundImage>
    <Font>Default</Font>
  </Appearance>
  <AbsoluteValue Minimum="0" Maximum="10000" />
  <Time>5000</Time>
  <Key>T</Key>
  <Function ID="1" FadeInMultiplier="0" FadeOutMultiplier="0" DurationMultiplier="1" />
  <Preset ID="16">
    <Name>∞</Name>
    <Value>4294967294</Value>
  </Preset>
  <Preset ID="17">
    <Name>0s</Name>
    <Value>0</Value>
  </Preset>
  <Preset ID="18">
    <Name>1s</Name>
    <Value>1000</Value>
  </Preset>
</SpeedDial>
```

---

## 14. Complete Workspace File Structure

A QLC+ workspace (`.qxw`) file has this top-level structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Workspace>
<Workspace xmlns="http://www.qlcplus.org/Workspace" CurrentWindow="VirtualConsole">
 <Creator>
   <Name>Q Light Controller Plus</Name>
   <Version>4.13.1</Version>
   <Author>Your Name</Author>
 </Creator>
 <Engine>
  <InputOutputMap>
   <Universe Name="Universe 1" ID="0">
    <Input Plugin="..." Line="..." />
    <Output Plugin="..." Line="..." />
    <Feedback Plugin="..." Line="..." />
   </Universe>
  </InputOutputMap>
  <Fixture>
   <Manufacturer>Generic</Manufacturer>
   <Model>Generic</Model>
   <Mode>1 Channel</Mode>
   <ID>0</ID>
   <Name>Fixture 1</Name>
   <Universe>0</Universe>
   <Address>0</Address>
   <Channels>1</Channels>
  </Fixture>
  <FixtureGroup ID="0">
   <Name>Group 1</Name>
   <Size X="4" Y="4" />
   <Head X="0" Y="0" Fixture="0">0</Head>
  </FixtureGroup>
  <Function ID="0" Type="Scene" Name="Scene 1">
   <Speed FadeIn="0" FadeOut="0" Duration="0" />
   <FixtureVal ID="0">0,255</FixtureVal>
  </Function>
  <Function ID="1" Type="Chaser" Name="Chaser 1">
   <Speed FadeIn="0" FadeOut="0" Duration="5000" />
   <Direction>Forward</Direction>
   <RunOrder>Loop</RunOrder>
   <SpeedModes FadeIn="Default" FadeOut="Default" Duration="Common" />
   <Step Number="0" FadeIn="0" Hold="0" FadeOut="0" Note="">0</Step>
  </Function>
  <Monitor DisplayMode="0" ShowLabels="0">
   <Font>Arial,12,-1,5,50,0,0,0,0,0</Font>
   <ChannelStyle>0</ChannelStyle>
   <ValueStyle>0</ValueStyle>
   <Grid Width="1" Height="1" Depth="1" Units="0" />
  </Monitor>
 </Engine>
 <VirtualConsole>
  <Frame Caption="">
   <Appearance>
    <FrameStyle>None</FrameStyle>
    <ForegroundColor>Default</ForegroundColor>
    <BackgroundColor>Default</BackgroundColor>
    <BackgroundImage>None</BackgroundImage>
    <Font>Default</Font>
   </Appearance>
   <!-- All VC widgets go here as children of the bottom frame -->
   <Button Caption="Scene 1" ID="0" Icon="">
    <WindowState Visible="True" X="10" Y="10" Width="50" Height="50" />
    <Appearance>
     <FrameStyle>None</FrameStyle>
     <ForegroundColor>Default</ForegroundColor>
     <BackgroundColor>Default</BackgroundColor>
     <BackgroundImage>None</BackgroundImage>
     <Font>Default</Font>
    </Appearance>
    <Function ID="0" />
    <Action>Toggle</Action>
    <Intensity Adjust="False">100</Intensity>
   </Button>
  </Frame>
  <Properties>
   <Size Width="1920" Height="1080" />
   <GrandMaster ChannelMode="Intensity" ValueMode="Reduce" SliderMode="Normal" />
  </Properties>
 </VirtualConsole>
 <SimpleDesk>
  <Engine />
 </SimpleDesk>
</Workspace>
```

### Key Workspace-Level Tags

| Tag | Description |
|-----|-------------|
| `<Workspace>` | Root element. `xmlns="http://www.qlcplus.org/Workspace"`. `CurrentWindow` attr. |
| `<Creator>` | Contains `<Name>`, `<Version>`, `<Author>` |
| `<Engine>` | Contains all fixtures, functions, and engine configuration |
| `<VirtualConsole>` | Contains the VC widget tree |
| `<SimpleDesk>` | Simple desk configuration |
| `<InputOutputMap>` | Input/output patching for universes |

### Properties (VirtualConsole)

```xml
<Properties>
  <Size Width="1920" Height="1080" />
  <GrandMaster ChannelMode="Intensity" ValueMode="Reduce" SliderMode="Normal" />
</Properties>
```

| Element | Description |
|---------|-------------|
| `Size` | Virtual console canvas size |
| `GrandMaster` | Grand master settings. `ChannelMode`: `"Intensity"` or `"AllChannels"`. `ValueMode`: `"Reduce"` or `"Limit"`. `SliderMode`: `"Normal"` or `"Inverted"`. |

---

## Appendix A: XML Tag Name Quick Reference

### Engine Tags

| Constant | String |
|----------|--------|
| `KXMLQLCFunction` | `"Function"` |
| `KXMLQLCFunctionID` | `"ID"` |
| `KXMLQLCFunctionType` | `"Type"` |
| `KXMLQLCFunctionName` | `"Name"` |
| `KXMLQLCFunctionHidden` | `"Hidden"` |
| `KXMLQLCFunctionPath` | `"Path"` |
| `KXMLQLCFunctionBlendMode` | `"BlendMode"` |
| `KXMLQLCFunctionSpeed` | `"Speed"` |
| `KXMLQLCFunctionSpeedFadeIn` | `"FadeIn"` |
| `KXMLQLCFunctionSpeedFadeOut` | `"FadeOut"` |
| `KXMLQLCFunctionSpeedDuration` | `"Duration"` |
| `KXMLQLCFunctionSpeedHold` | `"Hold"` |
| `KXMLQLCFunctionDirection` | `"Direction"` |
| `KXMLQLCFunctionRunOrder` | `"RunOrder"` |
| `KXMLQLCFunctionTempoType` | `"Tempo"` |
| `KXMLQLCFunctionStep` | `"Step"` |
| `KXMLQLCFunctionNumber` | `"Number"` |
| `KXMLQLCFunctionValue` | `"Value"` |
| `KXMLQLCFunctionChannel` | `"Channel"` |
| `KXMLQLCFunctionEnabled` | `"Enabled"` |
| `KXMLQLCFixtureValues` | `"FixtureVal"` |
| `KXMLQLCFixtureID` | `"ID"` |

### Chaser-Specific Tags

| Constant | String |
|----------|--------|
| `KXMLQLCChaserSpeedModes` | `"SpeedModes"` |

### Scene-Specific Tags

| Constant | String |
|----------|--------|
| `KXMLQLCSceneChannelGroupsValues` | `"ChannelGroupsVal"` |
| `KXMLQLCSceneChannelGroups` | `"ChannelGroups"` |

### RGBMatrix-Specific Tags

| Constant | String |
|----------|--------|
| `KXMLQLCRGBMatrixStartColor` | `"MonoColor"` |
| `KXMLQLCRGBMatrixEndColor` | `"EndColor"` |
| `KXMLQLCRGBMatrixColor` | `"Color"` |
| `KXMLQLCRGBMatrixColorIndex` | `"Index"` |
| `KXMLQLCRGBMatrixFixtureGroup` | `"FixtureGroup"` |
| `KXMLQLCRGBMatrixDimmerControl` | `"DimmerControl"` |
| `KXMLQLCRGBMatrixProperty` | `"Property"` |
| `KXMLQLCRGBMatrixPropertyName` | `"Name"` |
| `KXMLQLCRGBMatrixPropertyValue` | `"Value"` |
| `KXMLQLCRGBMatrixControlMode` | `"ControlMode"` |

### EFX-Specific Tags

| Constant | String |
|----------|--------|
| `KXMLQLCEFXPropagationMode` | `"PropagationMode"` |
| `KXMLQLCEFXAlgorithm` | `"Algorithm"` |
| `KXMLQLCEFXWidth` | `"Width"` |
| `KXMLQLCEFXHeight` | `"Height"` |
| `KXMLQLCEFXRotation` | `"Rotation"` |
| `KXMLQLCEFXStartOffset` | `"StartOffset"` |
| `KXMLQLCEFXIsRelative` | `"IsRelative"` |
| `KXMLQLCEFXAxis` | `"Axis"` |
| `KXMLQLCEFXOffset` | `"Offset"` |
| `KXMLQLCEFXFrequency` | `"Frequency"` |
| `KXMLQLCEFXPhase` | `"Phase"` |
| `KXMLQLCEFXX` | `"X"` |
| `KXMLQLCEFXY` | `"Y"` |
| `KXMLQLCEFXFixture` | `"Fixture"` |
| `KXMLQLCEFXFixtureID` | `"ID"` |
| `KXMLQLCEFXFixtureHead` | `"Head"` |
| `KXMLQLCEFXFixtureMode` | `"Mode"` |
| `KXMLQLCEFXFixtureDirection` | `"Direction"` |
| `KXMLQLCEFXFixtureStartOffset` | `"StartOffset"` |
| `KXMLQLCEFXFixtureIntensity` | `"Intensity"` |

### VCWidget Tags

| Constant | String |
|----------|--------|
| `KXMLQLCVCCaption` | `"Caption"` |
| `KXMLQLCVCWidgetID` | `"ID"` |
| `KXMLQLCVCWidgetPage` | `"Page"` |
| `KXMLQLCVCWidgetAppearance` | `"Appearance"` |
| `KXMLQLCVCFrameStyle` | `"FrameStyle"` |
| `KXMLQLCVCWidgetForegroundColor` | `"ForegroundColor"` |
| `KXMLQLCVCWidgetBackgroundColor` | `"BackgroundColor"` |
| `KXMLQLCVCWidgetFont` | `"Font"` |
| `KXMLQLCVCWidgetBackgroundImage` | `"BackgroundImage"` |
| `KXMLQLCVCWidgetKey` | `"Key"` |
| `KXMLQLCVCWidgetInput` | `"Input"` |
| `KXMLQLCVCWidgetInputUniverse` | `"Universe"` |
| `KXMLQLCVCWidgetInputChannel` | `"Channel"` |
| `KXMLQLCVCWidgetInputLowerValue` | `"LowerValue"` |
| `KXMLQLCVCWidgetInputUpperValue` | `"UpperValue"` |
| `KXMLQLCVCWidgetInputMonitorValue` | `"MonitorValue"` |
| `KXMLQLCVCWidgetInputLowerParams` | `"LowerParams"` |
| `KXMLQLCVCWidgetInputUpperParams` | `"UpperParams"` |
| `KXMLQLCVCWidgetInputMonitorParams` | `"MonitorParams"` |
| `KXMLQLCWindowState` | `"WindowState"` |
| `KXMLQLCWindowStateVisible` | `"Visible"` |
| `KXMLQLCWindowStateX` | `"X"` |
| `KXMLQLCWindowStateY` | `"Y"` |
| `KXMLQLCWindowStateWidth` | `"Width"` |
| `KXMLQLCWindowStateHeight` | `"Height"` |

### VCButton Tags

| Constant | String |
|----------|--------|
| `KXMLQLCVCButton` | `"Button"` |
| `KXMLQLCVCButtonIcon` | `"Icon"` |
| `KXMLQLCVCButtonFunction` | `"Function"` |
| `KXMLQLCVCButtonFunctionID` | `"ID"` |
| `KXMLQLCVCButtonAction` | `"Action"` |
| `KXMLQLCVCButtonActionFlash` | `"Flash"` |
| `KXMLQLCVCButtonActionToggle` | `"Toggle"` |
| `KXMLQLCVCButtonActionBlackout` | `"Blackout"` |
| `KXMLQLCVCButtonActionStopAll` | `"StopAll"` |
| `KXMLQLCVCButtonFlashOverride` | `"Override"` |
| `KXMLQLCVCButtonFlashForceLTP` | `"ForceLTP"` |
| `KXMLQLCVCButtonStopAllFadeTime` | `"FadeOut"` |
| `KXMLQLCVCButtonKey` | `"Key"` |
| `KXMLQLCVCButtonIntensity` | `"Intensity"` |
| `KXMLQLCVCButtonIntensityAdjust` | `"Adjust"` |

### VCSlider Tags

| Constant | String |
|----------|--------|
| `KXMLQLCVCSlider` | `"Slider"` |
| `KXMLQLCVCSliderMode` | `"SliderMode"` |
| `KXMLQLCVCSliderWidgetStyle` | `"WidgetStyle"` |
| `KXMLQLCVCSliderValueDisplayStyle` | `"ValueDisplayStyle"` |
| `KXMLQLCVCSliderValueDisplayStyleExact` | `"Exact"` |
| `KXMLQLCVCSliderValueDisplayStylePercentage` | `"Percentage"` |
| `KXMLQLCVCSliderCatchValues` | `"CatchValues"` |
| `KXMLQLCVCSliderClickAndGoType` | `"ClickAndGoType"` |
| `KXMLQLCVCSliderInvertedAppearance` | `"InvertedAppearance"` |
| `KXMLQLCVCSliderLevel` | `"Level"` |
| `KXMLQLCVCSliderLevelLowLimit` | `"LowLimit"` |
| `KXMLQLCVCSliderLevelHighLimit` | `"HighLimit"` |
| `KXMLQLCVCSliderLevelValue` | `"Value"` |
| `KXMLQLCVCSliderLevelMonitor` | `"Monitor"` |
| `KXMLQLCVCSliderOverrideReset` | `"Reset"` |
| `KXMLQLCVCSliderChannel` | `"Channel"` |
| `KXMLQLCVCSliderChannelFixture` | `"Fixture"` |
| `KXMLQLCVCSliderPlayback` | `"Playback"` |
| `KXMLQLCVCSliderPlaybackFunction` | `"Function"` |
| `KXMLQLCVCSliderPlaybackFlash` | `"Flash"` |

### VCFrame Tags

| Constant | String |
|----------|--------|
| `KXMLQLCVCFrame` | `"Frame"` |
| `KXMLQLCVCFrameAllowChildren` | `"AllowChildren"` |
| `KXMLQLCVCFrameAllowResize` | `"AllowResize"` |
| `KXMLQLCVCFrameShowHeader` | `"ShowHeader"` |
| `KXMLQLCVCFrameIsCollapsed` | `"Collapsed"` |
| `KXMLQLCVCFrameIsDisabled` | `"Disabled"` |
| `KXMLQLCVCFrameEnableSource` | `"Enable"` |
| `KXMLQLCVCFrameShowEnableButton` | `"ShowEnableButton"` |
| `KXMLQLCVCFrameMultipage` | `"Multipage"` |
| `KXMLQLCVCFramePagesNumber` | `"PagesNum"` |
| `KXMLQLCVCFrameCurrentPage` | `"CurrentPage"` |
| `KXMLQLCVCFrameNext` | `"Next"` |
| `KXMLQLCVCFramePrevious` | `"Previous"` |
| `KXMLQLCVCFramePagesLoop` | `"PagesLoop"` |
| `KXMLQLCVCFramePageShortcut` | `"Shortcut"` |
| `KXMLQLCVCFramePageShortcutPage` | `"Page"` |
| `KXMLQLCVCFramePageShortcutName` | `"Name"` |

### VCSoloFrame Tags

| Constant | String |
|----------|--------|
| `KXMLQLCVCSoloFrame` | `"SoloFrame"` |
| `KXMLQLCVCSoloFrameMixing` | `"Mixing"` |
| `KXMLQLCVCSoloFrameExclude` | `"ExcludeMonitored"` |

### VCSpeedDial Tags

| Constant | String |
|----------|--------|
| `KXMLQLCVCSpeedDial` | `"SpeedDial"` |
| `KXMLQLCVCSpeedDialSpeedTypes` | `"SpeedTypes"` |
| `KXMLQLCVCSpeedDialAbsoluteValue` | `"AbsoluteValue"` |
| `KXMLQLCVCSpeedDialAbsoluteValueMin` | `"Minimum"` |
| `KXMLQLCVCSpeedDialAbsoluteValueMax` | `"Maximum"` |
| `KXMLQLCVCSpeedDialTap` | `"Tap"` |
| `KXMLQLCVCSpeedDialMult` | `"Mult"` |
| `KXMLQLCVCSpeedDialDiv` | `"Div"` |
| `KXMLQLCVCSpeedDialMultDivReset` | `"MultDivReset"` |
| `KXMLQLCVCSpeedDialApply` | `"Apply"` |
| `KXMLQLCVCSpeedDialTapKey` | `"Key"` |
| `KXMLQLCVCSpeedDialMultKey` | `"MultKey"` |
| `KXMLQLCVCSpeedDialDivKey` | `"DivKey"` |
| `KXMLQLCVCSpeedDialMultDivResetKey` | `"MultDivResetKey"` |
| `KXMLQLCVCSpeedDialApplyKey` | `"ApplyKey"` |
| `KXMLQLCVCSpeedDialResetFactorOnDialChange` | `"ResetFactorOnDialChange"` |
| `KXMLQLCVCSpeedDialVisibilityMask` | `"Visibility"` |
| `KXMLQLCVCSpeedDialTime` | `"Time"` |
| `KXMLQLCVCSpeedDialPreset` | `"Preset"` |
| `KXMLQLCVCSpeedDialPresetID` | `"ID"` |
| `KXMLQLCVCSpeedDialPresetName` | `"Name"` |
| `KXMLQLCVCSpeedDialPresetValue` | `"Value"` |

---

## Appendix B: Parsing Rules & Defaults Summary

### VCButton Defaults
- Action: `Toggle`
- Intensity: `1.0` (100%), not enabled
- State: `Inactive`
- Function: `4294967295` (none)
- Icon: empty string

### VCSlider Defaults
- Mode: `Playback`
- InvertedAppearance: `false`
- ValueDisplayStyle: `Exact`
- WidgetStyle: `Slider`
- Level LowLimit: `0`
- Level HighLimit: `255`
- Playback Function: `4294967295` (none)
- CatchValues: `false`

### VCFrame Defaults
- AllowChildren: `true`
- AllowResize: `true`
- ShowHeader: `true`
- ShowEnableButton: `true`
- Collapsed: `false`
- Disabled: `false`
- MultipageMode: `false`
- TotalPagesNumber: `1`
- CurrentPage: `0`
- PagesLoop: `false`
- FrameStyle: `Sunken`

### VCSoloFrame Defaults
- Same as VCFrame
- Mixing: `false`
- ExcludeMonitored: `false`
- FrameStyle: `Sunken`

### VCSpeedDial Defaults
- AbsoluteValueMin: `0`
- AbsoluteValueMax: `10000` (10 seconds)
- ResetFactorOnDialChange: `false`
- FrameStyle: `Sunken`

### Function Defaults
- Direction: `Forward`
- RunOrder: `Loop`
- TempoType: `Time`
- FadeInSpeed: `0`
- FadeOutSpeed: `0`
- Duration: `0` (except EFX default = `20000`, RGBMatrix default = `500`)

### Chaser Speed Mode Defaults
- FadeInMode: `Default`
- FadeOutMode: `Default`
- HoldMode/DurationMode: `Common`

---

## Appendix C: Color Value Encoding

QLC+ stores colors as `QRgb` unsigned integers. To convert:

```python
# RGB to QRgb uint
def rgb_to_qrgb(r, g, b, a=255):
    return (a << 24) | (r << 16) | (g << 8) | b

# Examples:
# Red:   rgb_to_qrgb(255, 0, 0)     = 4294901760
# Green: rgb_to_qrgb(0, 255, 0)     = 4278255360
# Blue:  rgb_to_qrgb(0, 0, 255)     = 4278190335
# White: rgb_to_qrgb(255, 255, 255) = 4294967295

# QRgb uint to RGB
def qrgb_to_rgb(val):
    a = (val >> 24) & 0xFF
    r = (val >> 16) & 0xFF
    g = (val >> 8) & 0xFF
    b = val & 0xFF
    return (r, g, b, a)
```

For `<ForegroundColor>` and `<BackgroundColor>` in widget appearance, the value is stored the same way but **without alpha** (just the RGB portion as a plain unsigned integer from `QColor::rgb()`).

---

*End of QLC+ XML Format Reference*
