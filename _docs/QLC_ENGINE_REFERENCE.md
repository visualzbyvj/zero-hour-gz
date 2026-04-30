# QLC+ 5.2.1 Engine Reference (auto-generated)

Generated from `qlcplus-QLC-_5.2.1 Source Code/`.

## SpeedDial Visibility (project)
| Bit | Value | Element |
|-----|-------|---------|
| 0 | 1 | PlusMinus |
| 1 | 2 | Dial |
| 2 | 4 | Tap |
| 6 | 64 | Milliseconds |
| 7 | 128 | Multipliers |
| 8 | 256 | Apply |
| 9 | 512 | Beats |

## Beat chaser
- `m_elapsedBeats += 1000` per beat tick; sub-beat step holds unreliable for Tempo=Beats.

## Enums (sample)

### `engine/src/avolitesd4parser.h::Attributes`
SPECIAL, INTENSITY, PANTILT, COLOUR, GOBO, BEAM, EFFECT

### `engine/src/channelmodifier.h::Type`
SystemTemplate, UserTemplate

### `engine/src/chaser.h::FadeControlMode`
FromFunction, Blended, Crossfade, BlendedCrossfade

### `engine/src/chaseraction.h::ChaserActionType`
ChaserNoAction, ChaserStopStep, ChaserNextStep, ChaserPreviousStep, ChaserSetStepIndex, ChaserPauseRequest

### `engine/src/dmxdumpfactoryproperties.h::TargetType`
Chaser, VCButton, VCSlider

### `engine/src/doc.h::LoadStatus`
Cleared, Loading, Loaded

### `engine/src/efx.h::Algorithm`
Circle, Eight, Line, Line2, Diamond, Square, SquareChoppy, SquareTrue, Leaf, Lissajous

### `engine/src/efx.h::EFXAttr`
Intensity, Width, Height, Rotation, XOffset, YOffset, StartOffset

### `engine/src/efxfixture.h::Mode`
PanTilt, Dimmer, RGB

### `engine/src/fadechannel.h::ChannelFlag`
ForceLTP

### `engine/src/fixture.h::Components`
RGB, BGR, BRG, GBR, GRB, RGBW, RBG

### `engine/src/function.h::Attr`
Intensity

### `engine/src/function.h::FractionsType`
NoFractions, ByTwoFractions, AllFractions

### `engine/src/function.h::OverrideFlags`
Single

### `engine/src/function.h::TempoType`
Original, Time, Beats

### `engine/src/function.h::Type`
Undefined, SceneType, ChaserType, EFXType, CollectionType, ScriptType, RGBMatrixType, ShowType, SequenceType, AudioType, VideoType

### `engine/src/functionparent.h::Type`
Function, AutoVCWidget, ManualVCWidget, Master

### `engine/src/inputoutputmap.h::BlackoutRequest`
BlackoutRequestNone, BlackoutRequestOn, BlackoutRequestOff

### `engine/src/inputoutputmap.h::NetworkServerType`
NativeServer, WebServer

### `engine/src/keypadparser.h::KeyPadCommands`
CommandNone, CommandAT, CommandTHRU, CommandFULL, CommandZERO, CommandBY, CommandPlus, CommandPlusPercent, CommandMinus, CommandMinusPercent

### `engine/src/monitorproperties.h::ItemFlags`
HiddenFlag, InvertedPanFlag, InvertedTiltFlag, MeshZUpFlag

### `engine/src/qlccapability.h::PresetType`
None, SingleColor, DoubleColor, SingleValue, DoubleValue, Picture

### `engine/src/qlccapability.h::WarningType`
NoWarning, EmptyName, Overlapping

### `engine/src/qlcchannel.h::ControlByte`
MSB, LSB

### `engine/src/qlcchannel.h::Group`
Intensity, Colour, Gobo, Speed, Pan, Tilt, Shutter, Prism, Beam, Effect, Maintenance, Nothing, NoGroup

### `engine/src/qlcchannel.h::PrimaryColour`
NoColour, Red, Green, Blue, Cyan, Magenta, Yellow, Amber, White, UV, Lime, Indigo

### `engine/src/qlcfixturedef.h::FixtureType`
ColorChanger, Dimmer, Effect, Fan, Flower, Hazer, Laser, LEDBarBeams, LEDBarPixels, MovingHead, Other, Scanner, Smoke, Strobe

### `engine/src/qlcinputchannel.h::MovementType`
Absolute, Relative

### `engine/src/qlcinputchannel.h::Type`
Slider, Knob, Encoder, Button, NextPage, PrevPage, PageSet, NoType

### `engine/src/qlcinputfeedback.h::FeedbackType`
Undefinded, LowerValue, UpperValue, MonitorValue

### `engine/src/qlcinputprofile.h::Type`
MIDI, OS2L, OSC, HID, DMX, Enttec

### `engine/src/qlcinputsource.h::WorkingMode`
Absolute, Relative, Encoder

### `engine/src/qlcpalette.h::FanningLayout`
XAscending, XDescending, XCentered, YAscending, YDescending, YCentered, ZAscending, ZDescending, ZCentered

### `engine/src/qlcpalette.h::FanningType`
Flat, Linear, Sine, Square, Saw

### `engine/src/qlcpalette.h::PaletteType`
Undefined, Dimmer, Color, Pan, Tilt, PanTilt, Shutter, Gobo, Zoom

### `engine/src/rgbalgorithm.h::Type`
Text, Script, Image, Audio, Plain

### `engine/src/rgbmatrix.h::ControlMode`
ControlModeRgb, ControlModeWhite, ControlModeAmber, ControlModeUV, ControlModeDimmer, ControlModeShutter

### `engine/src/rgbscriptproperty.h::ValueType`
None, List, Range, Float, String

### `engine/src/scene.h::SceneAttr`
Intensity, ParentIntensity

### `engine/src/scriptrunner.h::FunctionOperation`
START, START_DONT_STOP, STOP, WAIT_START, WAIT_STOP

### `engine/src/show.h::TimeDivision`
Time, BPM_4_4, BPM_3_4, BPM_2_4, Invalid

### `engine/src/universe.h::BlendMode`
NormalBlend, MaskBlend, AdditiveBlend, SubtractiveBlend

### `engine/src/universe.h::ChannelType`
Undefined, LTP, HTP, Intensity

### `engine/src/universe.h::FaderPriority`
Auto, Override, SimpleDesk

### `engine/src/video.h::VideoAttr`
Intensity, Volume, XRotation, YRotation, ZRotation, XPosition, YPosition, WidthScale, HeightScale

### `plugins/dmxusb/src/dmxinterface.h::Type`
libFTDI, FTD2xx, QtSerial

### `plugins/dmxusb/src/dmxusbwidget.h::LineFlags`
None, DMX, MIDI, Input, Output, ArtNet_sACN_Forward

### `plugins/dmxusb/src/enttecdmxusbpro.h::ActionType`
OpenLine, CloseLine, RDMCommand

### `plugins/dmxusb/src/enttecdmxusbpro.h::PortType`
Output, Input, USB_DMX_Forward, ArtNet_sACN_Forward, ArtNet_sACN_Select

### `plugins/dmxusb/src/enttecdmxusbpro.h::RDMOperation`
None, Discovery, GetSetCommand

### `plugins/enttecwing/src/wing.h::Type`
Unknown, Playback, Shortcut, Program

### `plugins/gpio/gpioplugin.h::LineDirection`
NoDirection, OutputDirection, InputDirection

### `plugins/hid/hiddmxdevice.h::DMXmode`
DMX_MODE_NONE, DMX_MODE_OUTPUT, DMX_MODE_INPUT, DMX_MODE_MERGER

### `plugins/interfaces/qlcioplugin.h::Capability`
Output, Input, Feedback, Infinite, RDM, Beats

### `plugins/osc/oscpacketizer.h::TagType`
IntegerTag, FloatTag, DoubleTag, TimeTag, StringTag, BlobTag

### `plugins/peperoni/unix/peperonidevice.h::OperatingMode`
CloseMode, OutputMode, InputMode

### `plugins/uart/uartwidget.h::WidgetMode`
Closed, Output, Input

### `qmlui/app.h::AccessControl`
AC_FixtureEditing, AC_FunctionEditing, AC_VCControl, AC_VCEditing, AC_SimpleDesk, AC_ShowManager, AC_InputOutput

### `qmlui/app.h::ChannelColors`
Red, Green, Blue, Cyan, Magenta, Yellow, White, Amber, UV, Lime, Indigo

### `qmlui/app.h::ChannelType`
DimmerType, GoboType, SpeedType, PanType, TiltType, ShutterType, PrismType, BeamType, EffectType, MaintenanceType, ColorType

### `qmlui/app.h::DragItemType`
NoDragItem, GenericDragItem, FolderDragItem, FunctionDragItem, UniverseDragItem, FixtureGroupDragItem, FixtureDragItem, ChannelDragItem, PaletteDragItem, HeadDragItem, ShowDragItem, TrackDragItem, WidgetDragItem

### `qmlui/app.h::FileDialogOpModes`
OpenMode, SaveMode, SaveAsMode, ImportMode

### `qmlui/app.h::MouseEvents`
Pressed, Released, Clicked, DoubleClicked, DragStarted, DragFinished, Checked

### `qmlui/fixtureeditor/editorview.h::CompositeChannelTypes`
RGBChannel, RGBWChannel, RGBAWChannel

### `qmlui/fixturegroupeditor.h::TransformType`
Rotate90, Rotate180, Rotate270, HorizontalFlip, VerticalFlip

### `qmlui/fixturemanager.h::PanelDirection`
Horizontal, Vertical

### `qmlui/fixturemanager.h::PanelOrientation`
TopLeft, TopRight, BottomLeft, BottomRight

### `qmlui/fixturemanager.h::PanelType`
Snake, ZigZag

### `qmlui/fixturemanager.h::PrecedenceType`
AutoHTP, AutoLTP, ForcedHTP, ForcedLTP

### `qmlui/inputprofileeditor.h::MIDIMessageOffset`
ControlChangeOffset, NoteOffset, NoteAfterTouchOffset, ProgramChangeOffset, ChannelAfterTouchOffset, PitchWheelOffset, MBCPlaybackOffset, MBCBeatOffset, MBCStopOffset

### `qmlui/inputprofileeditor.h::MIDIMessageType`
ControlChange, NoteOnOff, NoteAftertouch, ProgramChange, ChannelAfterTouch, PitchWheel, MBCPlayback, MBCBeat, MBCStop

### `qmlui/mainview3d.h::FixtureMeshType`
NoMeshType, ParMeshType, MovingHeadMeshType, ScannerMeshType, StrobeMeshType, LEDBarMeshType, DefaultMeshType

### `qmlui/mainview3d.h::RenderQuality`
LowQuality, MediumQuality, HighQuality, UltraQuality

### `qmlui/showmanager.h::PreviewDrawType`
RepeatingDuration, FadeIn, StepDivider, FadeOut, AudioData

### `qmlui/simpledesk.h::SimpleDeskCommand`
ResetChannel, ResetUniverse

### `qmlui/tardis/networkmanager.h::ConnectionStatus`
Disconnected, WaitAuthentication, DownloadingProject, Connected

### `qmlui/tardis/networkmanager.h::HostType`
UnknownHostType, ServerHostType, ClientHostType

### `qmlui/tardis/networkmanager.h::ServerType`
NativeServer, WebServer

### `qmlui/tardis/simplecrypt.h::CryptoFlag`
CryptoFlagNone, CryptoFlagCompression, CryptoFlagChecksum, CryptoFlagHash

### `qmlui/treemodel.h::FixedRoles`
LabelRole, PathRole, IsExpandedRole, IsSelectedRole, IsCheckableRole, IsCheckedRole, IsDraggableRole, ItemsCountRole, HasChildrenRole, ChildrenModel, FixedRolesEnd

## loadXML (sample)
- `engine/audio/src/audio.cpp` -> `Audio`
- `engine/src/avolitesd4parser.cpp` -> `AvolitesD4Parser`
- `engine/src/bus.cpp` -> `Bus`
- `engine/src/channelsgroup.cpp` -> `ChannelsGroup`
- `engine/src/chaser.cpp` -> `Chaser`
- `engine/src/chaserstep.cpp` -> `ChaserStep`
- `engine/src/collection.cpp` -> `Collection`
- `engine/src/cue.cpp` -> `Cue`
- `engine/src/cuestack.cpp` -> `CueStack`
- `engine/src/doc.cpp` -> `Doc`
- `engine/src/efx.cpp` -> `EFX`
- `engine/src/efxfixture.cpp` -> `EFXFixture`
- `engine/src/fixture.cpp` -> `Fixture`
- `engine/src/fixturegroup.cpp` -> `FixtureGroup`
- `engine/src/function.cpp` -> `Function`
- `engine/src/inputoutputmap.cpp` -> `InputOutputMap`
- `engine/src/monitorproperties.cpp` -> `MonitorProperties`
- `engine/src/qlccapability.cpp` -> `QLCCapability`
- `engine/src/qlcchannel.cpp` -> `QLCChannel`
- `engine/src/qlcfixturedef.cpp` -> `QLCFixtureDef`
- `engine/src/qlcfixturehead.cpp` -> `QLCFixtureHead`
- `engine/src/qlcfixturemode.cpp` -> `QLCFixtureMode`
- `engine/src/qlcinputchannel.cpp` -> `QLCInputChannel`
- `engine/src/qlcinputprofile.cpp` -> `QLCInputProfile`
- `engine/src/qlcpalette.cpp` -> `QLCPalette`
- `engine/src/qlcphysical.cpp` -> `QLCPhysical`
- `engine/src/rgbaudio.cpp` -> `RGBAudio`
- `engine/src/rgbimage.cpp` -> `RGBImage`
- `engine/src/rgbmatrix.cpp` -> `RGBMatrix`
- `engine/src/rgbplain.cpp` -> `RGBPlain`
- `engine/src/rgbscript.cpp` -> `RGBScript`
- `engine/src/rgbscriptv4.cpp` -> `RGBScript`
- `engine/src/rgbtext.cpp` -> `RGBText`
- `engine/src/scene.cpp` -> `Scene`
- `engine/src/scenevalue.cpp` -> `SceneValue`
- `engine/src/script.cpp` -> `Script`
- `engine/src/scriptv4.cpp` -> `Script`
- `engine/src/sequence.cpp` -> `Sequence`
- `engine/src/show.cpp` -> `Show`
- `engine/src/showfunction.cpp` -> `ShowFunction`
- `engine/src/track.cpp` -> `Track`
- `engine/src/universe.cpp` -> `Universe`
- `engine/src/video.cpp` -> `Video`
- `plugins/midi/src/common/miditemplate.cpp` -> `MidiTemplate`
- `qmlui/app.cpp` -> `App`
- `qmlui/importmanager.cpp` -> `ImportManager`
- `qmlui/virtualconsole/vcanimation.cpp` -> `VCAnimation`
- `qmlui/virtualconsole/vcaudiotriggers.cpp` -> `VCAudioTriggers`
- `qmlui/virtualconsole/vcbutton.cpp` -> `VCButton`
- `qmlui/virtualconsole/vcclock.cpp` -> `VCClock`
- `qmlui/virtualconsole/vcclock.cpp` -> `VCClockSchedule`
- `qmlui/virtualconsole/vccuelist.cpp` -> `VCCueList`
- `qmlui/virtualconsole/vcframe.cpp` -> `VCFrame`
- `qmlui/virtualconsole/vclabel.cpp` -> `VCLabel`
- `qmlui/virtualconsole/vcslider.cpp` -> `VCSlider`
- `qmlui/virtualconsole/vcspeeddial.cpp` -> `VCSpeedDial`
- `qmlui/virtualconsole/vcspeeddialpreset.cpp` -> `VCSpeedDialPreset`
- `qmlui/virtualconsole/vcwidget.cpp` -> `VCWidget`
- `qmlui/virtualconsole/vcxypad.cpp` -> `VCXYPad`
- `qmlui/virtualconsole/vcxypadpreset.cpp` -> `VCXYPadPreset`
- `qmlui/virtualconsole/virtualconsole.cpp` -> `VirtualConsole`
- `ui/src/app.cpp` -> `App`
- `ui/src/audiobar.cpp` -> `AudioBar`
- `ui/src/simpledesk.cpp` -> `SimpleDesk`
- `ui/src/simpledeskengine.cpp` -> `SimpleDeskEngine`
- `ui/src/virtualconsole/vcaudiotriggers.cpp` -> `VCAudioTriggers`
- `ui/src/virtualconsole/vcbutton.cpp` -> `VCButton`
- `ui/src/virtualconsole/vcclock.cpp` -> `VCClock`
- `ui/src/virtualconsole/vcclock.cpp` -> `VCClockSchedule`
- `ui/src/virtualconsole/vccuelist.cpp` -> `VCCueList`
- `ui/src/virtualconsole/vcframe.cpp` -> `VCFrame`
- `ui/src/virtualconsole/vcframepageshortcut.cpp` -> `VCFramePageShortcut`
- `ui/src/virtualconsole/vclabel.cpp` -> `VCLabel`
- `ui/src/virtualconsole/vcmatrix.cpp` -> `VCMatrix`
- `ui/src/virtualconsole/vcmatrixcontrol.cpp` -> `VCMatrixControl`
- `ui/src/virtualconsole/vcproperties.cpp` -> `VCProperties`
- `ui/src/virtualconsole/vcslider.cpp` -> `VCSlider`
- `ui/src/virtualconsole/vcspeeddial.cpp` -> `VCSpeedDial`
- `ui/src/virtualconsole/vcspeeddialfunction.cpp` -> `VCSpeedDialFunction`
- `ui/src/virtualconsole/vcspeeddialpreset.cpp` -> `VCSpeedDialPreset`
- `ui/src/virtualconsole/vcwidgetproperties.cpp` -> `VCWidgetProperties`
- `ui/src/virtualconsole/vcxypad.cpp` -> `VCXYPad`
- `ui/src/virtualconsole/vcxypadfixture.cpp` -> `VCXYPadFixture`
- `ui/src/virtualconsole/vcxypadpreset.cpp` -> `VCXYPadPreset`
- `ui/src/virtualconsole/virtualconsole.cpp` -> `VirtualConsole`

## Pattern hits
### ChaserRunner beat tick +1000 millibeats
- `engine/src/chaserrunner.cpp:774`
- `engine/src/function.cpp:1126`
- `engine/src/showrunner.cpp:166`

### VCSpeedDial applyFunctionsTime
- `webaccess/src/webaccess-qml.cpp:847`
- `qmlui/virtualconsole/vcspeeddial.cpp:254`
- `qmlui/virtualconsole/vcspeeddial.cpp:291`
- `qmlui/virtualconsole/vcspeeddial.cpp:511`
- `qmlui/virtualconsole/vcspeeddial.cpp:671`

Regenerate: `python _generate_engine_ref.py`
