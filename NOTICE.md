# Notices and attribution

This bundle contains multiple works with different licenses. Preserve the
upstream notices, source headers and attribution when redistributing it.

## HexGL

Source: BKcore/HexGL, revision in dependencies.lock.json.
Copyright/credit: Thibaut “BKcore” Despoulain and contributors.
The top-level LICENSE is copied to licenses/HexGL.txt. The README says MIT
**unless specified in the file**. Many gameplay JS files contain Creative
Commons Attribution-NonCommercial 3.0 Unported notices. Do not erase these
exceptions or describe all derived content as unconditionally MIT.

Original credits identify Charnel for the HexMKI base model and Nobiax for
the track texture. Original filenames and source hashes are recorded in
assets/manifest.json (meshes) and assets/hud.json (HUD) and preserved in vendor/HexGL.

## Audio

The original audio/LICENSE is copied to licenses/audio.txt. It credits:

- bg: mu6k, public domain, adjusted by Licson.
- crash: qubodup, public domain.
- boost: IFartInUrGeneralDirection, CC Attribution 3.0.
- wind: kangaroovindaloo, CC Attribution 3.0, adjusted by Licson.
- destroyed: beman87, CC Attribution 3.0, adjusted by Licson.
- Ogg conversion: baleboy.

Native conversion here changes sample rate, channel count and quantization,
not duration. There are no newly generated replacement sound effects.

## Jaguar rendering and SDK

42Bastian/jag_3d_engine: MIT, license copied to licenses/engine-MIT.txt.
The adapted GPU engine retains its source lineage. new_bjl and lyxass carry
separate upstream LICENSE files in their vendor directories. The encrypted
GPU boot loader, font, and original object-list binaries remain upstream data.

## Virtual Jaguar

The host-side test harness links Virtual Jaguar Rx core code. The emulator's
GPL license is preserved in vendor/virtualjaguar/LICENSE. The test harness and
its instrumentation are supplied under GPL-3.0-or-later as part of that host
program. No emulator code is linked into the Jaguar game ROM.

The CrY conversion lookup data in tools/cry.py is read from Virtual Jaguar's
cry2rgb.h; the corresponding source remains in the supplied vendor tree.
The offline converter tools are supplied under GPL-3.0-or-later.

The native port/game integration is supplied subject to the applicable HexGL
and 42Bastian upstream licenses/notices. This document is not a relicensing of
any upstream material. Commercial redistribution requires checking the
file-specific noncommercial notices and other upstream rights.

HUD conversion: the three textures/hud PNGs and clipping in bkcore/hexgl/HUD.js
are from the pinned BKcore source. HUD.js carries Thibaut Despoulain’s
CC BY-NC 3.0 notice. Native adaptation does not remove that notice.

Front-end assets use the original css/bg.jpg, css/title.png and
css/BebasNeue-webfont.ttf. The font binary and embedded naming/copyright metadata
remain supplied unchanged; rasterization is not relicensing. Native replay is an
adaptation of the original RaceData/Gameplay purpose, using native fixed-point
pose samples rather than THREE.js quaternions. The original file-specific notices
remain applicable. EEPROM code and recovery tests are native port additions.

Dynamics/effects source mapping: native hover/drift/grade/contact and falling
are adaptations of `ShipControls.js`; the pitch look-at and speed camera refer
to `CameraChase.js`; spark/cloud emitters and booster sprite refer to
`ShipEffects.js`. These source files carry the original CC BY-NC 3.0 notice.
Effect texture provenance is in `assets/effects.json`; the source sprites are
retained unchanged under `vendor/HexGL/textures/`.
