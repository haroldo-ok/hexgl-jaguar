# Ship banking and speed-sensitive camera milestone

## What changes at runtime

- Left/right steering banks the original ship mesh toward the turn. The booster
  mesh receives exactly the same yaw and roll; it stays attached during banking.
- Normal bank target is 49 of the renderer's 512 angular steps, approximately
  34.45 degrees (the upstream target is 0.6 radians). Holding B while steering
  selects 83 steps, approximately 58.36 degrees (upstream airbrake addition is
  0.7 times the normal bank). Opposing directions cancel the bank target.
- Releasing steering filters the bank back toward level rather than snapping.
- The camera pulls back smoothly from the existing 160-unit trail distance to
  200 native world units at full base speed. Braking brings it back toward 160.
  This uses the existing 0–28 base-speed state; boost does not add extra pullback.
- Camera height now filters toward ship Y + 64 instead of immediately adopting
  every height-map step. A safety envelope clamps it to ship Y + 24 through
  ship Y + 80, preventing the filter from lagging beneath the ship/road or too
  far above the visible ship. Large map jumps can still require a clamped jump.
- Pause freezes the filters and actual renderer pose. Countdown/READY do not
  drift. Finish/destruction freeze filter state; restart explicitly resets it.
- The existing native autopilot banks using the shortest wrapped heading delta.
  This is new native behavior, not a conversion of the upstream static replay.

No replacement ship, booster, road geometry or textures are introduced.

## Source relationship and intentional adaptations

References, already included in vendor/HexGL:

- `bkcore/hexgl/ShipControls.js`: rollAngle 0.6, rollLerp 0.08, opposite steering
  signs, and the 0.7 airbrake roll addition.
- `bkcore/hexgl/CameraChase.js`: speedOffsetMax 10 and speed offset response 0.30.

Preserve their CC BY-NC 3.0 notices and the project's licensing exceptions.

This is **not full ShipControls or CameraChase parity**. It keeps the previous
native framing (160 units behind) and adds the original maximum speed offset,
scaled from 10 original units to 40 native units. It retains the yaw-only camera;
no original look-at pitch, quaternion/up-vector tracking, orbit mode or camera
switch is claimed. The extra camera-height filter is a native adaptation, not
an exact translation of upstream CameraChase. The ship itself still uses the
existing height-map position; this is not a new hover/suspension model.

Heading acceleration, lateral drift/repulsion, falling, slope pitch/tilt and
complete airbrake physics remain unfinished. B still uses the port's existing
braking/doubled-steering rules. Banking adds the corresponding visual response,
not an unimplemented lateral-physics claim. Original menus/bitmap HUD, effects,
recording/replay, leaderboards and persistent times also remain unfinished.

## Stable fixed-point response

`tools/motion.py` derives Q0.8 coefficients for capped steps of 1–6 video fields:

`alpha = round(256 × (1 − (1 − rate)^(fields × 60 / video_hz)))`

Rates at the 60 Hz reference are 0.08 for bank, 0.30 for speed offset and 0.15 for
height (the last is a native choice). PAL uses 50 Hz, NTSC 60 Hz. This compounds
response across elapsed fields instead of applying the browser's per-rendered-
update interpolation unchanged. It is an explicit frame-rate adaptation.

The state values are Q24.8. Jaguar IMULT only multiplies signed 16-bit operands;
feeding a whole Q8 bank/height delta directly to it would truncate valid values.
`src/motion.inc` instead splits each delta into signed high bits and an unsigned
fractional byte. It rounds the resulting product and advances one least-
significant bit when rounding would otherwise leave a nonzero residual stuck.
The build verifier establishes the high-part range over every driveable height-
map pixel, not merely the tested route. Unit tests compare the split operation
with a wide-integer reference over 10,000 deterministic input triples.

## Rendering and state layout

`src/control.js` calls the motion filter after gameplay updates, writes roll to
`obj_angle_c` on both meshes, and writes the filtered camera to the renderer's
normal CAMERA_X/Y/Z fields. There is no host-side animation or frame overlay.
The original engine already supports the necessary local Z rotation before yaw.

New state occupies 17 words at `$10a0` through `$10e3`, clear of the game state,
VBL/DSP counters and text-format buffers:

| Word | Meaning |
|---|---|
| 0 | Current roll, Q8 renderer angle-index units |
| 1 | Current speed pullback, Q8 native world units |
| 2 | Current camera Y, Q8 native world units |
| 3 | Previous heading for autopilot bank estimation |
| 4–6 | Targets: roll, pullback, camera Y |
| 7 | Capped integration step, in video fields |
| 8–10 | Bank/pullback/height Q0.8 coefficients |
| 11 | Effective integer trail distance |
| 12–14 | Camera X/Y/Z written by the game |
| 15 | Applied ship and booster roll indices, packed as two words |
| 16 | Pose-commit sequence; updated after all renderer values are written |

These fields are observations, not test controls. The runner additionally reads
actual mesh angles and camera memory independently, using exported assembler
symbols (`--symbols src/hexgl.equ`). The tests require those renderer inputs to
match the filtered state, so changing only a telemetry counter cannot satisfy
this part of verification. Existing pixel/watchdog tests still inspect actual
TOM output, and the independent stock GUI test inspects real OpenGL presentation.

## Added tests

- Controller-only, stationary steering sequences in PAL and NTSC: left/right,
  release, both airbrake directions, pause and restart. Stationary testing avoids
  steering into a wall before the filter can settle.
- Bank is required to approach each target and return within about 1.5 degrees
  of level after the tested release interval. The filter's exact recurrence is
  separately checked on every committed update.
- Acceleration/braking sequences: proportional pullback, intermediate distances
  rather than a snap, return to baseline after braking, and actual camera output.
- Full races: both bank directions, more than 500 filtered-height updates,
  correct recurrence and height bounds, plus all existing lap/timer/result and
  nonblack/freeze assertions.
- Matched half-second PAL/NTSC bank responses must remain within 1.5 degrees.
- Eight new numerical/oracle unit tests, including deliberately wrong renderer
  angles, camera values and filter state. These are synthetic unit fixtures,
  not substitutes for real emulator runs.

See `test-results/summary.json`, `test-results/gui/summary.json`, and REPORT.html
for the executed verdicts tied to the distributed ROM's SHA-256. No physical
Jaguar or remote CI execution is claimed.
