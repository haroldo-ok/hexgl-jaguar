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
  native blue source-derived booster-lit face textures and projected Feisar contact shadow, zero-key booster alpha and double-sided banner.
- Camera pitch/yaw/bank panorama with fractional A1-source seam-wrap blits.
- Real scene convolution/bloom and native AV quality switches.
- Complete-duration source-channel stereo IMA4 decoding, independent L/R DSP/I2S buses and independent music/effects mute.
- Source particle color2 choices and half-life brightness, 10:5 bounded collision emission.
- Cartridge EEPROM persistence with separate manual/assisted best times and
  two-slot recovery journals.

## Still outstanding — the overall request is not complete

1. **Physics:** full source-equivalent angular/contact detail. Native bounded yaw
   inertia, signed fractional heading carry, map-derived cross-slope banking,
   drift/recoil, bilinear hover, grade pitch and timed falling now run. Manual
   and assisted paths share active-time normalized boost expiry. The assisted
   path remains a waypoint demo rather than the complete manual solver.
2. **Camera:** exact transformed mesh-up contribution to chase position. Native
   chase/orbit/near, pitch/bank transforms, rolled sky and actual-view replay run.
   Source dummy quaternion is yaw-only; CameraChase does not assign camera.up.
3. **Effects:** complete source emitter/force/distribution/capacity and stochastic
   booster behavior. Source color2 ranges, half-life brightness and bounded 10:5
   emission now run; center-depth differs from source default depthTest=false.
4. **Lighting/rendering fidelity:** full normal/specular/TBN and cubemap response,
   directional moving shadow maps, continuous per-fragment colored attenuation,
   and RGB/high-resolution bloom. Real projected source-ship contact shadow,
   blue scene-face texture selection and native convolution/additive bloom now
   run, but are documented hardware approximations, not full GLSL parity.
5. **Audio:** WebAudio-equivalent HRTF and complete source gain/trigger
   fidelity. Original L/R content is now decoded independently; IMA4 and movement-based
   balance remain hardware adaptations. The source has
   no audio filters; the earlier filter gap was an audit error.
6. **Presentation fidelity:** complete browser-equivalent layout/transitions.
   Original-font race-event banners and native slide-in feedback now run, as do
   real gameplay and AV settings pages and keypad shortcuts. Neither implies full
   original HTML/CSS/canvas animation or full browser resolution/quality settings.
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

Latest gameplay integration: [GAMEPLAY-HANDLING-VIEWS.md](GAMEPLAY-HANDLING-VIEWS.md).

Latest expanded integration and audit: [REMAINING-NATIVE-SYSTEMS.md](REMAINING-NATIVE-SYSTEMS.md), [source-inventory.json](source-inventory.json). The inventory covers 23 application files, not every generic browser-library function.
