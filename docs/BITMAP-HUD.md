# Original bitmap gauges: native HUD milestone

This milestone converts **three specific original images**, not every remaining
HexGL interface or asset. It does not complete the port.

## Original sources → native output

Pinned `BKcore/HexGL` revision remains in `dependencies.lock.json`.

| Source, under `vendor/HexGL/` | Native output | Runtime use |
|---|---|---|
| `textures/hud/hud-bg.png` | `assets/hud-bg.bin` | background/outline |
| `textures/hud/hud-fg-speed.png` | `assets/hud-speed.bin` | symmetric speed fill |
| `textures/hud/hud-fg-shield.png` | `assets/hud-shield.bin` | shield fill |
| `bkcore/hexgl/HUD.js` | clipping thresholds in each record | original trapezoid and vertical rectangle |

`assets/hud.json` records source and native SHA-256 values, dimensions, placement,
coverage method and record counts. No substitute artwork is generated. The
original 1920×250 PNGs are downsampled to 384×50 using Lanczos; transparent
pixels are represented by absence of writes. CrY conversion uses the same
actual chroma DAC tables as the existing textures. Its implementation is now
shared in `tools/cry.py`, without importing/re-running mesh conversion.

Alpha becomes **deterministic 8×8 ordered coverage**, not full RGBA blending.
This makes edge/transparent regions visibly stippled at native resolution.
Color and fine honeycomb detail are quantized; this is not lossless image fidelity.
The runtime record streams total 23,656 bytes (2,957 eight-byte records).

## Clipping and live values

For native width W=384, height H=50, pixel centers (x,y):

- Speed: include pixels where `abs(x-W/2) <= (W/2.91)*speedRatio + H-y`.
- Shield: horizontal half-width `W/18.3`, full-height `W/14.3`, lower edge
  `W/34 + W/14.3`; the upper edge moves upward with shieldRatio.
- Native speedRatio = base speed / 28; shieldRatio = shield / 100.
- Digits show base speed × 10 and shield percent, matching the native footer.
  These are the existing native units, not a claim of browser-physics speed
  calibration. Extra movement from a boost pad does not raise base speed or
  expand this gauge beyond full, consistent with the current native telemetry.

Thresholds are precomputed at pixel centers; runtime compares the actual game
state, not an animation timer. The shield gauge drains with collision damage,
reaches empty on destruction and refills on Option reset. Speed responds to
throttle/braking. Paused/finished state retains its corresponding values.

## Screen and scheduling adaptations

- The artwork sits at the **top**, instead of HexGL's bottom, to avoid covering
  the ship at 384×200. Camera framing, projection, sky and physics are unchanged.
- Original bitmap proportions remain 384×50. The leading transparent rows mean
  all drawn pixels also fit the tested PAL output, whose world begins at y=-4.
- Center digits use the existing native 8×8 font, with black cell backgrounds
  for legibility against bright sky. This is **not** original font conversion.
- Original browser HUD visibility/message-only transitions, original menus,
  typography and full result-screen composition are still not implemented.
- The existing text timing/results footer remains readable and unchanged.
- `src/bitmap_hud.js` is a separate GPU overlay at the same safe overlay base
  used by control/engine. It waits for the final blit, draws only into the back
  buffer, and returns before the main loop permits the next VBL publication.
- PITCH2 address calculation respects interleaved four-pixel phrases. No writes
  are made into the other framebuffer's phrases. The next scene clear removes
  old gauge pixels, so shrinking fills do not accumulate stale fragments.

## Validation

`tests/hud_checks.py` builds expected RGB pixels from the original PNGs,
independently expressed clipping inequalities and DAC conversion. It does not
use the compiled record streams as its visual oracle. Every positive full-core
scenario compares actual TOM screenshots (including the final frame) against
live states from at most the preceding 12 video fields, allowing back-buffer
presentation latency. It checks every expected art pixel plus both complete
24×8 digit cells, normally 1,500–2,800 exact RGB pixels per capture.

Acceleration/braking scenarios must show zero, intermediate and full speed.
Manual driving also exercises shield loss, destruction and reset. Existing
countdown, timer glyphs, full races, bank/camera recurrence and independent
renderer-pose tests are retained. The lower-world watchdog ROI is y=111..189,
excluding both the top bitmap overlay and the PAL/NTSC text footer; a moving
HUD cannot rescue a black or frozen track.

Ten new unit tests cover source provenance, PITCH2 bounds, source alpha coverage,
all 29 speed and 101 shield levels, valid reference pixels, and intentionally
wrong/black/stuck gauge images. These synthetic negative fixtures are unit
checks, **not** emulator screenshots. All positive E2E evidence is freshly
captured from actual emulator execution. Stock GUI tests remain independent
black-box startup/input/rendering regressions, not the exact HUD pixel oracle.

Desktop screenshot retention keeps the endpoints of each static countdown
segment; moving/fault images and all per-sample metrics remain. See
`test-results/gui/screenshot-retention.json`. The newer front-end release also samples older core screenshots; complete
traces and assertion results remain. See `test-results/screenshot-retention.json`.

Current executed results are in `docs/TEST-RESULTS.md`, `test-results/summary.json`
and `test-results/gui/summary.json`. Historical motion/race-flow records retain
their old ROM hashes and must not be mistaken for current evidence.

Physical hardware, automated Windows Virtual Jaguar 2.1.2 and remote CI remain
unverified. Full physics, original menu/fonts/effects, replay and persistence
remain unfinished. See `docs/PARITY.md` and `NOTICE.md`.
