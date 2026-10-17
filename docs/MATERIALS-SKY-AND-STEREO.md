> **Increment history:** This document describes its original implementation/test milestone. Current banked-sky, source-color/lifetime, blue-light/contact-shadow, bloom and AV changes supersede older missing-feature notes: see [REMAINING-NATIVE-SYSTEMS.md](REMAINING-NATIVE-SYSTEMS.md), [PARITY.md](PARITY.md) and the current hash-bound test reports.

# Native material, lighting, sky and stereo integration

This is another implemented increment toward the standalone-stock port, **not a
claim that everything has been ported**. There is no host renderer or network
bridge. Jaguar GPU/DSP code consumes the converted source assets directly.

## What now runs

### Material lookup banks

`tools/materials.py` consumes the original six normal maps, six specular maps,
nine runtime diffuse/material slots and all six sky cubemap faces. It creates
**eight directional banks × nine materials × 64² CrY texels** (589,824 bytes).
`assets/materials.json` records each source and bank hash. The renderer selects a
bank from camera yaw, then its real texture address uses the original face UVs.

- Source normal maps modulate diffuse response; bonus-base normal scale is 3.
- Source specular maps control a power-42 highlight. Ship/track use metallic tint.
- Scraper materials sample the original sky cubemap with reflection directions,
  modulated by their original specular textures and source reflectivity 0.8.
- Speed pads use the source `0x0096ff` material color, not the bonus-base picture.
- Booster alpha becomes ordered coverage with a zero texel key. The Jaguar
  blitter's data comparator skips transparent texels; opaque black uses code 1.
- The original start banner is double-sided. The renderer still rejects invalid
  near-plane triangles; it bypasses only banner backface rejection.

**Adaptation, not shader equivalence:** the banks use tangent-hemisphere view
approximations, not a per-face tangent/bitangent/normal basis or interpolated
per-fragment WebGL light evaluation. Bank changes are discrete. Textures remain
64² and affine-mapped. These are used material maps, not unused archived files,
but full normal/specular/environment rendering fidelity remains unfinished.

### Static sunlight and local booster illumination

The converter ray-tests actual static scene triangles toward the original sun
position `(-4000,1200,1800)`. Each static receiver face is tested at its centroid;
self hits within one native unit are ignored. The result is baked into that
face's native luminance. The source speed material does not receive shadows.

For the pinned geometry, **7,435 of 10,290 receiver centroids** are occluded.
`assets/shadow-faces.json` records the per-object/per-face results and geometry
hashes. The conversion does not add a replacement shadow mesh or omit triangles.

The low-resolution renderer uses an ambient-preserving range: shadowed faces
start at luminance 128 (no subtractive CrY offset), unoccluded faces at 160, plus
bounded direct-sun response. This avoids crushing dark source textures into an
apparently black viewport. It is not the browser's 2048² shadow-map filter.

`pose_light` puts the stern light in the current camera frame. The face-visibility
stage applies a radius-240-native-unit Manhattan falloff to **real scene-face
luminance**. Thrust increases its strength; destruction disables it. Replay uses
the recorded source phase. This is monochrome face illumination, not the original
blue per-fragment point light. The existing glow sprite remains a separate effect.

**Still missing:** moving ship shadows, accurate per-pixel light/material response,
colored local illumination, and scene bloom. Static centroid shadows are coarse
and can change abruptly at triangle boundaries; no claim of WebGL parity is made.

### Camera-pitched sky

All six source sky faces are now baked into a **2048×512** panorama, without the
previous horizontal duplicate. The native blitter copies a 384×200 window:

- Horizontal offset follows real camera yaw.
- Vertical crop is `clamp(156 + trunc(176*tan(cameraPitch)), 0, 312)`.
- A second blit handles the panorama seam. No out-of-range texture read is needed.
- Recorded camera pitch drives the same code in replay.

This implements vertical sky tracking. It remains a cylindrical approximation,
not a fully rotated cubemap; sky roll and an orbit camera remain unfinished.

### Native spatial stereo

The DSP separates a centered bus (music/destruction) from a spatial bus
(wind/boost/collision), matching the source `usePanner` split. Native lateral drift
drives bounded stereo pan; the spatial bus has a 2/3 inverse-distance attenuation
adaptation for the source panner's 1.5-unit position scale. Signed saturating
left/right samples go to the real JERRY I2S registers. Music stays centered.

The source audio **does not construct a BiquadFilter or filter graph**. Earlier
scope text incorrectly listed original audio filters as missing; this audit
corrects that requirement rather than inventing a fake filter implementation.
`setListenerVelocity` is commented out upstream, too.

The latest integration preserves original left/right content in complete-duration
7,990 Hz stereo IMA4 streams, decoded independently by the DSP. This replaces the
previous mono conversion without enlarging the stock cartridge slot. Music and
destruction are not movement-panned; their original channel content is retained.
Remaining differences include lossy reduced-bandwidth encoding, coarse balance
instead of WebAudio HRTF and simplified gains/event semantics. Boost is now an
edge/retrigger-controlled one-shot with stop, not a looping sample.
See [PARTICLES-AND-ORIGINAL-STEREO.md](PARTICLES-AND-ORIGINAL-STEREO.md).

## Fixed-point fixes found by fresh tests

Two low-16-bit multiply constraints mattered in this integration:

1. At a four-field update, the old falling calculation formed `80*256*dt` before
   multiplying by 60. Jaguar MULT truncates operands to 16 bits, producing a
   slower fall. The new order multiplies `80*60*dt` first (at most 28,800), then
   shifts by eight and divides by video Hz. Units cover every dt 1..6 at 50/60 Hz.
2. A 73,728-byte material-bank stride cannot be passed directly as a MULT operand.
   The renderer multiplies the bank by 9, then shifts by 13. Runtime pointer
   assertions catch a truncated-stride implementation.

The existing black-viewport oracle also rejected overly subtractive initial
shadow lighting. The implementation changed to preserve ambient illumination;
**the black-screen threshold was not reduced**.

## Memory and build

| Area | Address / extent |
| --- | --- |
| Material banks | ROM offset `0x102000..0x191fff` |
| Main menu image | ROM offset `0x192000` |
| Secondary menu image | ROM offset `0x1b7800` |
| Sky | ROM offset `0x400000..0x5fffff` |
| DSP sample snapshot | RAM `0x1a00..0x1a27` |
| Five stereo ADPCM decoder states | RAM `0x1a80..0x1af7` |
| Material/light diagnostics | RAM `0x1a40..0x1a6f` |

The cartridge remains **6 MiB**. Collision/height/audio offsets and the replay
buffers remain unchanged. `make assets` now regenerates materials, shadows,
geometry, terrain, sky, audio and route/replay data in dependency order. `make rom`
then regenerates the UI/HUD/effects art and coefficient tables and assembles the
GPU/DSP/68000 programs. All GPU overlays are checked below the reserved stack.

## Validation design

`tests/material_e2e.py` executes fresh NTSC/PAL controller sequences. It checks:

- Actual interleaved emulator PCM contains unequal left/right samples during
  both left and right airbrake movement; countdown music is centered.
- Even DSP seqlock snapshots match the exact signed gain/saturation arithmetic.
  The diagnostic values are the operands actually written to JERRY, not a model
  substituted for emulation.
- Runtime texture pointers refer to the correct material banks in the verified
  ROM, not the old diffuse table or a truncated bank stride.
- Real face-light additions are nonzero and saturate correctly.
- Thousands of actual sky pixels match independent pitch/yaw projections of the
  original converted panorama, including wraparound views.

Unit checks verify all source-map hashes, bank contents, view dependence,
transparent keys, source-blue speed material, geometry-bound shadow coverage,
and rejection of mono/reversed/corrupt stereo samples. Existing race, desktop,
HUD, dynamics, replay and EEPROM gates are retained. Current hash-bound JSON
summaries report actual executed outcomes; architecture text alone is not a test.

Physical Jaguar timing, picture quality, audio output and cartridge compatibility
still need hardware verification. Finite emulator runs cannot establish them.

`tools/check_recorded_materials.py` separately rechecks current-ROM dynamics
observations. Both 3,000-field route runs must render **all eight material banks**;
all four route/drive traces must show changing sky crops and actual local face
illumination. This is post-run analysis, not extra emulation. Its hash-bound result
is `docs/materials-additional-checks.json` and is required for release packaging.

## Dedicated falling/pause gate

The larger rendering pipeline changes which video field each controller event
is sampled on. Existing fixed-time manual pause scripts no longer exercise
falling in every boot mode. `tests/fall_e2e.py` therefore runs a separate
controller-only probe, observes the first real unsupported fall, then starts a
**fresh emulator process** with the same input prefix and a pause pulse 12 fields
after that observed onset. Each asserted case must freeze an active, not already
destroyed, fall for more than 20 native updates, resume, and reach destruction
after 1.5 active seconds. Both BIOS/direct boot and PAL/NTSC are covered.

No probe or asserted run writes game RAM. Probe observations and invocations are
archived. A unit fault check explicitly rejects pausing an already destroyed
ship as evidence of pause during falling.
