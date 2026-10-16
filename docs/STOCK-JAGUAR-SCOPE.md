# Agreed completion target: standalone stock Atari Jaguar

The user selected the standalone-stock target: no host networking bridge, with
hardware-appropriate rendering adaptations and local saved scores in place of
online services. This does **not** authorize calling unimplemented systems done.

## Implemented in the native integration

- Native front-end navigation, original background/title art and source-font atlas.
- Controls/credits, local-record view and a result panel.
- Genuine native run recording, time-interpolated replay and playback controls.
- Native drift/contact/hover/fall dynamics, grade pitch and vertical chase look-at.
- Original spark/cloud world-space emitters and booster glow sprite.
- Cartridge EEPROM persistence with separate manual/assisted best times and
  two-slot recovery journals.

## Still outstanding — the overall request is not complete

1. **Physics:** full angular/inertial behavior, cross-slope tilt and source-equivalent
   collision detail. Native drift, contact recoil, bilinear hover, grade pitch and
   timed falling are implemented; the reduced-map/field-based adaptations remain.
2. **Camera:** quaternion up-vector/roll, sky pitch and orbit modes. Vertical chase
   look-at is now implemented in actual mesh/normal transforms and replay.
3. **Effects:** depth-aware, perspective-sized/additive sprites, full velocity
   inheritance, booster scene lighting and material transparency/double-sided
   behavior. Actual original-sprite spark/cloud emitters and stern glow now run.
4. **Lighting:** hardware-appropriate normal/specular response, shadows and glow/bloom
   adaptations. A booster sprite does not implement those scene-lighting systems.
5. **Audio:** positional/stereo treatment and original filters; the native mixer
   still uses converted mono PCM rather than reproducing the WebAudio graph.
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
