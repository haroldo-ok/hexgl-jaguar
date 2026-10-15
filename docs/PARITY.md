# Conversion and feature parity

## Status key

- **Runtime**: implemented and referenced by the shipped ROM.
- **Adapted**: functional native counterpart, not behaviorally identical.
- **Converted only**: data exists, but it is not a supported gameplay feature.
- **Missing**: not implemented. No stub is claimed as support.

| Upstream component | Status | Details |
|---|---|---|
| Cityscape track geometry | Runtime | All 9,600 triangles retained before runtime culling; spatially partitioned |
| Feisar ship geometry | Runtime | All 1,676 triangles; fixed-point quantization |
| Booster geometry | Runtime | All 72 triangles; follows ship, no additive glow |
| Bonus base geometry | Runtime | All 168 triangles |
| Speed-pad geometry | Runtime | All 168 triangles |
| Scrapers 1 / 2 | Runtime | 176 triangles each |
| Start structure / banner | Runtime | 160 / 10 triangles; transparency and double-sided material behavior are not fully preserved |
| Edge geometry | Converted only | Native indexed mesh; 6,416 triangles after quad triangulation; no second-track gameplay |
| Diffuse materials | Adapted | Nine texture slots, 64² CrY; UV quantization and affine interpolation |
| Six-face skybox | Adapted | All six source faces baked into a 2048×200 panorama, duplicated for blitter wrap |
| Collision/height maps | Adapted | Downsampled 2048² → 512²; nearest sampling rather than original bilinear behavior |
| ShipControls | Adapted | Q24.8 position, 512-step yaw, acceleration/braking, speed cap, damage, boost and height following |
| Drift/repulsion, banking, hover/fall | Missing | Boundary rejection is used instead of the complete original response |
| CameraChase | Adapted | Fixed chase distance and height, yaw follow; no original smoothing, pitch or camera switching |
| Gameplay lap/checkpoint logic | Adapted | Ordered 0→1→2→0, three laps, native ready/racing/destroyed/finished states |
| Countdown and finish-time presentation | Missing | A starts immediately; finish is a native HUD state, not original result-screen flow |
| Pause / restart | Runtime | Jaguar Pause / Option |
| Music and all four SFX | Adapted | Complete durations converted to signed PCM8 mono at 7,990 Hz; DSP mixing and triggers |
| Original spatial/audio filtering | Missing | No panning, WebAudio graph or original filter behavior |
| Original bitmap HUD and menu artwork | Missing | Native text display is a replacement UI, not a conversion of those images |
| Timer | Adapted | Native elapsed video-tick state; not the original browser timer or presentation |
| Particles / booster light / sparks | Missing | No fake particle substitute is counted as converted |
| Bloom, shadows, normal/specular maps | Missing | Renderer is not a shader-equivalent translation |
| Touch, orientation, browser gamepad handlers | Adapted | Physical Jaguar controls replace browser inputs |
| Online ladder / score submission | Missing | No network or local replacement leaderboard |
| Race recording / interpolated replay | Missing | Provided replay data is converted, but there is no full recording/playback subsystem |
| Supplied replay file | Converted only | 5,625 records, **one unique position**; therefore not used as evidence of game animation |
| Autopilot | New feature | Generated from the actual collision-road centerline, for demos and test coverage |
| EEPROM best times / persistence | Missing | No save-game implementation |

## Important distinction

All Cityscape **mesh triangles** being converted does not mean all HexGL assets
and behavior are converted. The original HTML/CSS menus, HUD art, shader system,
effects, browser services and several gameplay details remain unported.
This is why the build is explicitly labeled incomplete.

## Rendering and memory

- 384×200 interleaved double buffer, with separate 384×40 text surface.
- 16-bit CrY, 64×64 diffuse textures, affine UV mapping.
- One shared per-object transform scratch allocation, followed immediately by
  insertion into the global depth buckets. This replaces the upstream demo's
  simultaneous per-object scratch allocations to fit all original geometry.
- Triangle arena: capacity 8,192; bounded insertion prevents overwriting other
  RAM if a view exceeds capacity. Overflow drops additional triangles rather
  than writing outside the arena.
- Program/static data load at `0x2000`, end `0x999e0` for the tested build.
- Scratch begins `0x110000`; arena ends `0x14acc8`; video begins `0x1b4800`.
- Collision, height, routes, audio and sky stream from cartridge ROM.
- GPU code overlays and DSP code are independently assembled with lyxass.

These choices retain real source content but sacrifice fidelity. The result
has visible texture, near-plane and quantization artifacts. Real-hardware
performance and compatibility are unverified.
