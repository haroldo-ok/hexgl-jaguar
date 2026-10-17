> **Increment history:** This document describes its original implementation/test milestone. Current banked-sky, source-color/lifetime, blue-light/contact-shadow, bloom and AV changes supersede older missing-feature notes: see [REMAINING-NATIVE-SYSTEMS.md](REMAINING-NATIVE-SYSTEMS.md), [PARITY.md](PARITY.md) and the current hash-bound test reports.

# Native dynamics, camera pitch and original-asset effects

This integration is a substantial playable-system update, **not full HexGL parity**.
Everything below is in the GPU program, not a host bridge or a pre-rendered movie.

## Runtime changes

- **Airbrake drift:** B + a direction now changes lateral displacement, not only
  bank and turn rate. Signed Q8 drift approaches ±0.1 and decays back to zero.
- **Contact response:** the source collision map's adjacent supporting cells
  select an inward impulse. It persists and decays between impacts. Penetrating
  positions are rejected while the following updates actually move away from the
  boundary; left/right/front contacts are identified for effect spawning.
- **Hover:** four samples of the converted original height map are bilinearly
  interpolated. Upward terrain penetration is corrected immediately; descents
  use the source `heightLerp = .4`, compounded for capped elapsed video fields.
  Invalid neighbour heights are replaced by the valid center height.
- **Falling:** an attempted unsupported position with no supporting neighbouring
  collision cells starts a non-recoverable fall. The ship drops at 20 original
  units per 60-Hz field and is destroyed after 1.5 seconds of *active* video time.
  Pause stops the fall. This follows the source's fixed fall vector, **not a newly
  claimed gravity/suspension solver**.
- **Ship pitch:** an ahead-height probe supplies a filtered terrain grade. Both
  original ship and booster meshes receive the pitch in their real Euler transform.
- **Chase camera:** a filtered vertical look-at angle aims 40 native units ahead
  of the ship. The renderer rotates both camera-space vertices and normals, not
  merely camera telemetry. Existing bank, pullback and height filters remain.
- **Replay:** every existing 64-byte sample now has a two-byte auxiliary pair of
  signed ship/camera pitch steps. Playback interpolates those recorded angles;
  it does not run physics against the track again. Quantization is one of 512
  angular steps. The 6,144-sample capacity remains unchanged.
- **Particles:** genuine collision events emit the original `spark.png` and
  `cloud.png`, at the contacted side of the ship. Six particles per observed
  event enter a 16-slot bounded pool with deterministic random velocities,
  world-space integration, a one-second lifetime and fading coverage. Their
  world positions are projected with the actual chase camera. Pause freezes them.
- **Booster glow:** the original `boostersprite.jpg` follows the ship's stern;
  native speed/boost controls its visible intensity. It disappears on destruction.

## Source mapping and hardware adaptations

`ShipControls.js`, `ShipEffects.js`, and `CameraChase.js` are the pinned source
references. Their CC BY-NC 3.0 notices remain applicable; see `NOTICE.md`.
`tools/dynamics.py` generates response and arctangent tables.
`tools/effects.py` converts **original** sprites and records source/output hashes.

The 512² collision/height conversion is retained. The pitch probe spans 96 native
units because the reduced map has coarse cells; grade is bounded to ±atan(.5),
without the browser's 4× exaggerated gradient. This is an explicit adaptation.
Drift/height/pitch/contact response rates and fall timing account for PAL/NTSC;
existing base acceleration, yaw increments and forward motion remain the prior
field-based approximation, not a complete replacement of the source integrator.

Particle art is 16² CrY, now resampled with perspective sizing and clipped
per-texel RGB additive/alpha-over composition. New velocity includes approximately
.7 of the ship's measured motion. Actual submitted triangle depths support a
conservative center query; glow bypasses it. These are documented native policies,
not literal WebGL shader/default-depth behavior. The 16-slot pool, source-yellow
spark tint, emission rate, lifetime/fade and deterministic randomness remain
hardware adaptations. Glow is **not bloom**. Particle trajectories regenerate
from collision events in replay rather than being individually recorded.
See [PARTICLES-AND-ORIGINAL-STEREO.md](PARTICLES-AND-ORIGINAL-STEREO.md) for exact
formulas, RGB requantization, depth fixtures and compromises.

Camera pitch is implemented; quaternion up-vector tracking, camera roll, cross-
slope ship tilt and orbit modes remain outstanding. A later integration adds panorama sky pitch, source-map material banks, static
centroid shadows, coarse booster face lighting, material sidedness/zero-key alpha
and native spatial stereo. These remain hardware adaptations, not shader/audio
equivalence; remaining presentation and physics/camera gaps are still explicit.

## Native layout

- `control.js` + `dynamics.inc`: state, steering, drift/contact/fall/height/grade.
- `pose.js` + `motion.inc` + `race_hud.inc`: separate pose/presentation GPU overlay.
- `rotate.inc`: actual camera-space pitch rotation of vertices and normals.
- `effects.js`: bounded emitters, integrator, camera projection and sprite drawing.
- `$1600`: physics telemetry; `$1700`: effects counters; `$1800..$19ff`: pool.
- `$1b0000..$1b2fff`: auxiliary replay angles, before video at `$1b4800`.
- All overlays are bounded below the GPU stack; source assets remain cartridge data.

## Executed-test design

`tests/dynamics_e2e.py` drives PAL and NTSC via normal controller events. Its
independent Python oracle recomputes bilinear source heights, the hover recurrence,
full Euler/yaw/pitch transforms of an actual original ship vertex, reciprocal
projection/aspect, and native particle lifetime/position updates. Renderer evidence
is copied from the **actual** transformed/projected scratch vertex before reuse.
Additional captured-pixel checks look for converted original effect colors.

The tests do not patch game RAM. Unit fault checks reject removed camera/ship
pitch and corrupted projected coordinates. Existing core/desktop black-screen and
frozen-video fault tests, menus, real replay, HUD pixels and EEPROM tests remain
release gates. See current hash-bound JSON summaries for executed outcomes; this
file is architecture documentation, not an assertion that a pending run passed.

Physical Jaguar performance and cartridge/EEPROM compatibility remain untested.

## Delivered evidence retention

Release packaging losslessly compresses complete field traces. Desktop captures
retain the last saved idle/countdown/throttle/pause/restart-moving view; all
metrics and all negative-control screenshots remain. Calibration probes and static
EEPROM fixture/reboot cases retain final imagery and all field observations. Older core captures are sampled
by countdown, gauge state and bank pose. This integration's focused dynamics
and front-end captures remain. The screenshot-retention manifests
record exactly which generated images were removed, after validation.

`tools/check_recorded_dynamics.py` independently rechecks current-ROM archived
observations: falling displacement, exactly 1.5 active seconds and pause during
falling in all four dedicated fall/pause boot/video runs, plus recorded pitch pairs against
observed gameplay before verifying replay interpolation. Its hash-bound output
is `docs/dynamics-additional-checks.json`; it is explicitly post-run analysis,
not another emulator execution or a synthetic gameplay input.

### Historical camera-oracle correction

The longer rendering pipeline produced ten distinct *integer-rounded* camera
distances but thirteen distinct Q8 filter values during the acceleration test.
The anti-snap assertion now counts the actual Q8 values; the independent exact
filter recurrence, maximum pullback and brake-return assertions are unchanged.
The release gates always execute all emulator cases fresh; no archived trace is
used as a substitute for execution. `tools/check_recorded_dynamics.py` is a separate,
explicitly post-run analysis of those current-ROM observations.
