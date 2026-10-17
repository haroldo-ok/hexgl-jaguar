# Agreed completion target: standalone stock Atari Jaguar

The user selected the standalone-stock target: no host networking bridge, with
hardware-appropriate rendering adaptations and local saved scores in place of
online services. This does **not** authorize calling unimplemented systems done.

## Implemented in the native integration

- Native front-end navigation, original background/title art and source-font atlas.
- Controls/credits, local-record view and a result panel.
- Genuine native run recording, time-interpolated replay and playback controls.
- Native drift/contact/hover/fall dynamics, grade pitch and vertical chase look-at.
- Original spark/cloud emitters and glow: perspective sizing, clipped RGB additive/alpha-over,
  approximately .7 ship-velocity inheritance and conservative center-depth queries.
- Source normal/specular/environment material lookup banks, coarse static sun shadows,
  native monochrome booster face lighting, zero-key booster alpha and double-sided banner.
- Camera-pitched panorama with native seam-wrap blits.
- Complete-duration source-channel stereo IMA4 decoding and independent L/R DSP/I2S buses.
- Cartridge EEPROM persistence with separate manual/assisted best times and
  two-slot recovery journals.

## Still outstanding — the overall request is not complete

1. **Physics:** full angular/inertial behavior, cross-slope tilt and source-equivalent
   collision detail. The extra assisted waypoint demo also retains a boost latch
   between pads rather than running the entire manual integrator. Native drift, contact recoil, bilinear hover, grade pitch and
   timed falling are implemented; the reduced-map/field-based adaptations remain.
2. **Camera:** quaternion up-vector/roll and orbit modes. Panorama sky pitch and vertical chase
   look-at is now implemented in actual mesh/normal transforms and replay.
3. **Effects:** full source emitter/random-color/lifetime fidelity, per-pixel depth,
   high-fidelity booster lighting and scene bloom. Native perspective RGB sprites
   and .7 velocity inheritance now run; center-depth is a deliberate native policy
   (source Particles defaults depthTest=false), not literal source semantics.
4. **Lighting:** full normal/specular/TBN response, moving shadows, colored point lighting and
   scene bloom. Eight source-map material banks, static centroid sun shadows and
   monochrome scene-face lighting now run, but do not imply shader equivalence.
5. **Audio:** WebAudio-equivalent HRTF and complete source gain/trigger
   fidelity. Original L/R content is now decoded independently; IMA4 and movement-based
   balance remain hardware adaptations. The source has
   no audio filters; the earlier filter gap was an audit error.
6. **Presentation fidelity:** original in-race typography/message animation, browser-
   equivalent layout/transitions and applicable settings. Native menus do not imply
   complete original HTML/CSS/canvas parity.
7. **Validation:** physical Jaguar timing, cartridge/EEPROM variants and hardware
   compatibility remain unverified. Finite emulator testing cannot establish them.

The original unused Edge mesh is converted but was not a supported track in the
upstream Cityscape launcher; no second playable track is being invented as parity.
Browser touch/orientation handlers are replaced by physical controls. Online
leaderboards and score submission are excluded by the explicit target decision.

No placeholder emitters, fake replay animations, unused shader maps or empty
service functions count as implementation. Each subsequent native system needs
source mapping, runtime integration, a compiled ROM and fresh emulator coverage.

See [MATERIALS-SKY-AND-STEREO.md](MATERIALS-SKY-AND-STEREO.md) for the latest
implemented systems, source provenance, hardware compromises and test design.

Latest particle/audio implementation: [PARTICLES-AND-ORIGINAL-STEREO.md](PARTICLES-AND-ORIGINAL-STEREO.md).
