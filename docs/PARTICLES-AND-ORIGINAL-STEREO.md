> **Increment history:** This document describes its original implementation/test milestone. Current banked-sky, source-color/lifetime, blue-light/contact-shadow, bloom and AV changes supersede older missing-feature notes: see [REMAINING-NATIVE-SYSTEMS.md](REMAINING-NATIVE-SYSTEMS.md), [PARITY.md](PARITY.md) and the current hash-bound test reports.

# Perspective particles, RGB composition and original stereo

This is a native stock-Jaguar increment, **not completion of the full port**.
The cartridge remains 6 MiB. No host renderer, network/audio bridge, emulated
extra RAM, or widened cartridge mapping is required. Physical hardware is untested.

## Source mapping and native particle behavior

Sources: the pinned `bkcore/hexgl/ShipEffects.js`, `bkcore/threejs/Particles.js`,
`bkcore/hexgl/ShipControls.js`, and the three original effect images recorded in
`assets/effects.json`. File-specific licensing remains in NOTICE and vendor files.

- Original 16×16 converted spark/cloud/glow atlases are now resampled over a
  perspective-sized square. World sizes are 8/24/16 native units respectively;
  size is `clamp(2, 32, worldSize * floor(32768 / cameraZ) >> 7)` pixels.
- Sprites use the same camera yaw, pitch, reciprocal projection and video aspect
  as the scene. Every output texel is independently clipped to the 384×200 view,
  below the 50-row HUD, including sprites straddling an edge.
- Sparks and glow use RGB additive blending; clouds use RGB alpha-over, with
  the source cloud opacity multiplier approximated by 204/256.
- CrY chroma indices must **not** be added. Each source/destination is decoded
  using the actual DAC coefficients and intensity multiplication. RGB channels
  are blended with integer alpha, saturated for additive output, reduced to
  RGB555, then requantized to CrY using a 32,768-entry table. Tables occupy
  66,560 bytes in the loaded payload. Quantization is a hardware adaptation,
  not exact WebGL floating-point composition or gamma-equivalent output.
- Packed atlas words contain alpha in bits 16..23. The shader explicitly masks
  that field before indexing the 256-entry chroma decode table. An independent
  oracle catches accidentally using alpha as part of the chroma address.
- Newly emitted velocity includes the ship's actual world displacement divided
  by the capped reference timestep, bounded before 16-bit multiplication, then
  scaled by 179/256 (approximately the source's 0.7 inheritance).
- The 16-slot pool, six-particle contact bursts, deterministic randomness,
  one-second lifetime, native fade and fixed-point integration remain adaptations.
  This is not a claim of all source random colors/emitter/lifetime behavior.

### Conservative depth policy

`src/addobj.inc` retains the three true camera-space vertex Z values for every
submitted triangle in `0x0e0000..0x0f7fff`. A further 12-byte guard is reserved
for the first candidate rejected when the draw arena is full; it remains far
below transform scratch at `0x110000`. The query uses the actual draw-list
screen coordinates and those depths, not a second approximate terrain map.

The center point must lie inside a nondegenerate triangle; winding is normalized.
Barycentric weights are reduced to fit Jaguar's multiplier operands. Perspective
reciprocal depth is interpolated, then inverted; the sprite is rejected when its
center is more than eight native Z units behind the triangle. Near-plane,
extreme-projection, ship and transparent-booster polygons are skipped. Glow
bypasses the test. This is center-only, not per-pixel depth.

**This is a native policy, not literal source depth parity:** upstream Particles
has `depthTest=false` by default, and the glow uses `mergeWith3D=false`.

Driving traces exercise inside-triangle depth arithmetic but did not encounter
an occluded particle. A separate, clearly labeled diagnostic ROM calls the
**unchanged production query assembly** on 12 native fixtures: front/coplanar,
eight-unit bias boundary, behind, outside, reversed winding, near-plane exclusion,
ship/booster exclusion, degeneracy, and varying-vertex reciprocal depth.
It records three real GPU rejection results. This is native unit coverage,
not fabricated driving evidence or physical-hardware validation.

## Full-duration original-channel audio

`tools/audio.py` decodes all five original Ogg files to 7,990 Hz signed PCM16
stereo, without duration truncation or mono conversion, then encodes a native
IMA4 stream. Every stereo frame uses one byte (high nibble left, low nibble right).
Each 2,048-frame block starts with two big-endian signed-16 predictor/unsigned-16
index pairs. Files are eight-byte aligned; the final block is not duration-padded.

The complete bank is **1,045,933 bytes**, fitting the original one-MiB slot at
cartridge offset `0x300000` / bus address `0xb00000`, before the sky at `0xc00000`.
An initially attempted uncompressed stereo layout exceeded the stock cartridge
window and was discarded, not accommodated by relaxing the emulator loader.

The DSP decodes each channel independently, maintains separate centered left/right
and spatial left/right buses, applies native gain/balance and signed saturation,
and writes distinct JERRY I2S registers. Music and destruction are not movement-
panned; their original channel content is retained. The source music file's two
channels happen to be identical: preservation does not invent a stereo difference.
Boost is an edge/retrigger-controlled one-shot with an explicit stop, not a loop.
Wind/music loop; crash/destruction are one-shots.

The five 24-byte decoder states occupy `0x1a80..0x1af7`, separate from audio
telemetry, materials and particles. `tools/write_audio_mixer.py` deterministically
emits `src/audio.js`, which is assembled into real DSP code by `make rom`.

Quality remains adapted: 7,990 Hz bandwidth and lossy IMA4, coarse spatial
balance rather than WebAudio HRTF, simplified gains and some event semantics.
Independent full-stream tests measure >22 dB SNR for every converted source and
>0.95 correlation of stereo-difference content where the source has a difference.
Exact values, source hashes, frame counts and encoded hashes are in `audio.json`.
The source defines no Biquad/filter graph, and its listener-velocity call is
commented out; neither is invented as an omitted feature.

## Validation and reproducibility

- 99 unit tests cover conversion integrity, full-duration stereo quality,
  canonical signed IMA nibble vectors, saturation/index clamps, all RGB555
  quantizer entries against actual DAC coefficients, shader/source/pixel oracles,
  and corrupt/fixed-size/mono/reversed-channel rejection.
- NTSC/PAL driving runs check source atlas addressing, opacity, perspective size,
  RGB arithmetic, actual framebuffer destination and actual TOM screenshot pixels.
  The read-only shader proof is seqlocked and records a texel with meaningful alpha.
- Native triangle proofs independently reproduce barycentric weights and
  reciprocal depth from the actual submitted coordinates and vertex depths.
- The independently decoded source music is compared sample-for-sample with
  completed DSP mixer telemetry and its committed cartridge cursor. Separate
  assertions validate native left/right gain/saturation and actual emulator PCM.
- `python3 tests/native_fx_probe.py` rebuilds/runs the separate native depth
  fixtures. Its report records production source/ROM and diagnostic ROM hashes.
- Two further controller-only NTSC/PAL runs start the actual boost stream, clear
  it while active with Option, start a second race and verify the source restarts
  from its first block. Separate source L/R content is observed at zero native pan.
- Complete-race read-only checks verify monotonic one-shot cursors and an ended
  source cursor/stop behavior. The newer gameplay integration removes the assisted
  boost latch and normalizes duration; ended-under-an-indefinite-flag is no longer
  a gate. See [the current gameplay note](GAMEPLAY-HANDLING-VIEWS.md). These remain
  native timer adaptations, not source-equivalent boost kinetics.
- Original black-screen, freeze, game-flow, bitmap-HUD, replay, EEPROM and stock
  desktop gates remain required; none was relaxed to accept the new effects.
- `make assets rom` regenerates and compiles the assets/GPU/DSP/68000 code;
  `make test` includes the native probe; `make test-clean` independently regenerates
  all source assets and checks for a byte-identical ROM plus real NTSC/PAL boots.

## Explicitly still incomplete

Full angular/quaternion and cross-slope physics, camera up-vector/roll/orbit,
colored/high-fidelity moving lighting and shadows, bloom, full emitter/color
fidelity, WebAudio HRTF/gain/trigger parity, and presentation/settings remain
unfinished. Native effects, static lighting and stereo do not imply shader,
physics, browser UI, or physical-Jaguar equivalence. Online services remain
excluded by the user's standalone-stock target decision.

This milestone is retained; current release adds native yaw/cross-slope handling,
actual alternate/rolled views, race banners and settings. See
[GAMEPLAY-HANDLING-VIEWS.md](GAMEPLAY-HANDLING-VIEWS.md) for current evidence semantics.
