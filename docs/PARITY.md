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
| Booster geometry | Runtime | All 72 triangles; follows ship pitch/bank; original stern glow sprite; coarse local scene illumination |
| Bonus base geometry | Runtime | All 168 triangles |
| Speed-pad geometry | Runtime | All 168 triangles |
| Scrapers 1 / 2 | Runtime | 176 triangles each |
| Start structure / banner | Runtime | 160 / 10 triangles; double-sided banner implemented; booster uses ordered-alpha zero-key transparency |
| Edge geometry | Converted only | Native indexed mesh; 6,416 triangles after quad triangulation; no second-track gameplay |
| Diffuse materials | Adapted | Nine material slots × eight normal/specular/environment lookup banks, 64² CrY; UV quantization and affine interpolation |
| Six-face skybox | Adapted | All six source faces baked into a 2048×512 panorama with pitch crop, fractional A1-source bank rotation and seam-split scanline blits |
| Collision/height maps | Adapted | Downsampled 2048² → 512²; native bilinear height sampling; classified nearest collision cells and neighbour contact gradients |
| ShipControls | Adapted | Q24.8 position, 512-step yaw, acceleration/braking, speed cap, damage, boost and height following |
| Visual steering/airbrake banking | Adapted | Original roll targets and reference response rates, fixed-point PAL/NTSC-normalized filtering; ship and booster share roll |
| Drift/repulsion, hover/fall/grade | Adapted | Actual lateral airbrake displacement, damped inward contact impulses, source-style hover, timed fall/destruction and rendered terrain pitch. Reduced-map contacts, map-derived cross-slope banking and bounded yaw inertia; not identical source angular/contact behavior; the source dummy quaternion is yaw-only |
| CameraChase | Adapted | Original speed-sensitive pullback maximum with normalized filtering; native height smoothing/safety bounds, retained trail framing and yaw follow. Vertical look-at pitch now rotates actual vertices/normals. Sky pitch crop implemented. Optional bank-follow roll rotates real geometry/normals/particles/light; actual CHASE/ORBIT/NEAR views implemented. Fractional-source rolled sky is implemented. Exact mesh-up contribution to chase position remains different; source CameraChase does not assign camera.up |
| Gameplay lap/checkpoint logic | Adapted | Ordered 0→1→2→0, three laps, native ready/racing/destroyed/finished states |
| Countdown and finish-time presentation | Adapted | Original HUD-mode timing: Get ready (2.5 s), 3/2/1 (1.5 s each), then GO. Native persistent finish results; original browser result-screen transition is still missing |
| Pause / restart | Runtime | Jaguar Pause / Option |
| Music and all four SFX | Adapted | Complete durations converted to original-channel stereo IMA4 at 7,990 Hz; DSP mixing/triggers and independent native music/effects mute |
| Spatial audio | Adapted | Centered music/destruction and movement-panned wind/boost/collision, real signed saturating stereo DSP/I2S output. Original L/R content is independently decoded; lossy native balance is not WebAudio HRTF. Source defines no audio filters |
| Original bitmap HUD layers | Adapted | All three original PNGs converted to 384×50 CrY, ordered alpha coverage, original speed/shield clipping; live native gauges. Moved to top to preserve ship framing; native numeric font and contrast backing |
| Front end and result presentation | Adapted | Original bg.jpg/title.png and Bebas Neue font, native Start/Controls/Records/Credits/Replay/Settings menus, original-font result panel. Two-column Jaguar layout; real camera/bank/HUD/particle/steering settings; AV page adds real bloom/shadow/blue-light/music/SFX consumers; browser resolution/layout and complete transitions are not reproduced |
| In-race typography/message animation | Adapted / incomplete | Original Bebas Neue race-event banners and native active-time slide-in now run; original CSS/canvas typography/layout/animation are not fully reproduced |
| Timer and lap splits | Adapted | PAL/NTSC-normalized elapsed time, current lap, three completed lap times and session best; MM:SS.mmm text HUD; pause and finish freeze the clock |
| Sparks / clouds / booster glow | Adapted | Original textures drive native collision emitters, 16-slot world-space pool, 15/event 10:5 emission mix, source color2 variations/lifetime brightness, pause and stern glow sprite. Perspective sizes, real RGB additive/alpha-over, approx .7 velocity inheritance and conservative center-only depth; not per-fragment shader parity ; native blue material-bank scene illumination is separate; source-default particles disable depth testing, unlike the conservative native policy |
| Normal/specular/environment maps | Adapted | Original maps drive eight camera-dependent material lookup banks; exponent-42 highlights, sky reflections. No per-face TBN or per-fragment shader equivalence |
| Shadows and local scene lighting | Adapted / incomplete | Static triangle-centroid sun occlusion baked into face luminance; native stern distance/intensity on actual faces now selects source-derived blue textures. Actual Feisar silhouette projects onto the moving ground footprint. Not a directional shadow map or per-fragment light |
| Bloom | Adapted | Actual post-scene 48×25 separable convolution and approx .8 signed-safe stock-blitter intensity addition; not full RGB/256²/25-tap browser fidelity. Quality switch defaults off |
| Touch, orientation, browser gamepad handlers | Adapted | Physical Jaguar controls replace browser inputs |
| Online ladder / score submission | Excluded by agreed stock target | Standalone stock Jaguar, no networking bridge. Local manual/assisted best records instead |
| Race recording / interpolated replay | Adapted | Actual native pose/camera/clock/telemetry samples; elapsed-field interpolation, shortest-path heading, pause/end/Option controls. Last run in RAM, 6,144-sample limit; recorded/interpolated ship/camera pitch pairs; no power-cycle persistence or original quaternion solver; actual native orbit/near XYZ/yaw/roll and composed bank now record/replay |
| Supplied replay file | Converted only | 5,625 records, **one unique position**; therefore not used as evidence of game animation |
| Autopilot | New feature | Generated from the actual collision-road centerline, for demos and test coverage |
| EEPROM best times / persistence | Adapted | Normal cartridge EEPROM serial I/O, two-slot journals per manual/autopilot category, generation/checksum validation, readback and bounded wait; no physical hardware verification |

## Important distinction

All Cityscape **mesh triangles** being converted does not mean all HexGL assets
and behavior are converted. The browser-equivalent layout/animation, in-race typography, shader system,
effects and several gameplay details remain unfinished. Browser services are
excluded from the agreed standalone-stock target.
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
- Program/static data load at `0x2000`, end `0xb6ca0` for the tested build.
- Submitted triangle vertex Z: `0x0e0000..0x0f7fff`; ADPCM states: `0x1a80..0x1af7`.
- Scratch begins `0x110000`; arena ends `0x14acc8`; video begins `0x1b4800`.
- Collision, height, routes, audio, material banks, sky and front-end backgrounds stream from cartridge ROM.
- Material/lighting/sky/audio source mappings: [MATERIALS-SKY-AND-STEREO.md](MATERIALS-SKY-AND-STEREO.md).
- Last-run samples occupy `0x150000..0x1affff`; pitch pairs use `0x1b0000..0x1b2fff`, before video at `0x1b4800`.
- GPU code overlays and DSP code are independently assembled with lyxass.

These choices retain real source content but sacrifice fidelity. The result
has visible texture, near-plane and quantization artifacts. Real-hardware
performance and compatibility are unverified.

Latest particle/audio details and limits: [PARTICLES-AND-ORIGINAL-STEREO.md](PARTICLES-AND-ORIGINAL-STEREO.md).

Latest handling/view/settings implementation: [GAMEPLAY-HANDLING-VIEWS.md](GAMEPLAY-HANDLING-VIEWS.md).

## Expanded source audit

See [REMAINING-NATIVE-SYSTEMS.md](REMAINING-NATIVE-SYSTEMS.md) and [source-inventory.json](source-inventory.json). Every one of 19 application JavaScript files has an explicit native/platform/network disposition; this is not line-level parity or a claim that outstanding fidelity work is complete. The stock target remains unchanged.
