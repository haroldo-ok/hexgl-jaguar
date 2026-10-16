# Front end, real run replay and cartridge saves

This integration closes several major gaps, **not the entire remaining port**.
The agreed target and outstanding systems are in `STOCK-JAGUAR-SCOPE.md`.

## Original UI assets and native layout

`tools/frontend.py` converts original `css/bg.jpg`, `css/title.png`, and
`css/BebasNeue-webfont.ttf`; SHA-256 provenance and output hashes are in
`assets/frontend.json`. No replacement artwork or substitute title is generated.
Two 384×200 CrY backgrounds stream from cartridge offsets `0x590000` and
`0x5b5800`. A 96-character, 16×24-cell proportional ASCII atlas rasterizes the
actual font at 18 pixels, with monochrome coverage threshold 128. The original
font binary is retained; this is not every Unicode glyph or browser text rendering.

The menu uses a two-column native layout. Up/Down select; A confirms. Start enters
the existing seven-second countdown. Controls, Records and Credits do not start a
race when confirmed. Option returns to Start. The original browser quality/HUD
options, CSS motion and full-screen result transition are not reproduced. The
existing bitmap gauges and native text footer remain. Results add a source-font
panel without covering the whole track; save success/failure is indicated there.

GPU modules: `frontend.js` polls the controller once and manages menus/saves;
`recording.js` records or applies playback; existing `control.js` writes the real
mesh/camera pose; `frontdraw.js` renders presentation; `bitmap_hud.js` draws gauges.
All use the existing safe overlay region, not concurrent GPU-local code expansion.

## Real recording and playback

- RAM header at `0x1500`, sample storage `0x150000..0x1affff`.
- Capacity **6,144 × 64-byte samples**, before video starts at `0x1b4800`.
- Each committed sample contains native Q8 XYZ, heading, roll, pullback, camera Y,
  race ticks, speed/shield/lap/boost, collision count, source phase, lap start and
  best lap. Header retains completed splits.
- Sampling follows actual race updates; paused/duplicate timestamps are skipped.
  This data is not generated from the autopilot route and does not use the static
  upstream replay file. A manually driven run is recorded by the same code.
- Starting another countdown clears the prior recording. Option preserves the last
  run so it can be selected from the menu. A run can be replayed after an abort too.
- Playback phase 5 uses elapsed video fields, Q8 interpolation and shortest-path
  heading deltas. Step-valued telemetry/events come from the preceding sample.
- The real ship/booster/camera are updated through normal control/rendering paths.
  Replay is not a host-side video or animation. Pause freezes its clock, the end
  holds the final sample, and Option exits to Start.
- Replay never enters the score-saving finish phase. Manual/autopilot classification
  is latched during racing, not reconstructed from a replay.
- At capacity the recorder stops safely and sets the `full` flag; the retained prefix
  is playable. Recording duration therefore depends on update rate. Full races in
  the test suite fit. This is bounded RAM recording, not unlimited recording.
- Recordings do not survive power-off. A 128-byte stock EEPROM cannot store them.
- Camera orientation remains the existing native yaw/bank/chase adaptation, not
  THREE.js quaternion interpolation or the original replay orbit camera.

## EEPROM format and behavior

`FRONT` at `0x1300` holds menu state and two independent score categories. Normal
cartridge 93C46/NM93C14-compatible serial transactions use word accesses to JERRY
`0xf15000` (select), `0xf14800` (data/clock) and `0xf14000` (data-out).
No host RAM patches or save API are called by the ROM.

Manual journals occupy EEPROM word addresses 0..15; assisted/autopilot journals
16..31. Each category has two eight-word slots:

| Word | Meaning |
|---|---|
| 0 | Commit magic `0x4847` |
| 1 | 16-bit generation |
| 2..3 | Best race time, milliseconds |
| 4..5 | Best completed lap, milliseconds |
| 6 | Format version 1 |
| 7 | XOR of words 1..6 with `0xa5c3` |

Only an improved result is written: invalidate the other slot, write its seven
payload/check words, then commit magic last (**nine word writes**). The entire
slot is read back and validated before reporting success. Busy polling is bounded
by three video fields per word; absence/failure must not create an infinite wait.
Boot validates checksum/version/time bounds and chooses the newest valid generation
with modulo-65536 comparison. A damaged/incomplete newer slot falls back to the old
one. Boot does not silently rewrite or repair cartridge storage.

Times are normalized to milliseconds from the actual PAL/NTSC field clock using
split arithmetic, avoiding the GPU's 16-bit multiply operand limit. Values are
bounded below 100 minutes. A run that used autopilot cannot replace a manual record.
Replay and destroyed runs do not save. Results remaining only in RAM after failed
save are not evidence of persistence; the UI reports EEPROM unavailability.

An EEPROM-equipped cartridge or compatible flash cart is required. Emulator save
files must be writable. ROM CRC naming means a changed ROM may use a new emulator
save filename, even though the on-cartridge journal format is unchanged.

## Tests and evidence

- `tests/frontend_checks.py`: original-font pixel oracle, independent EEPROM decoder
  and interpolation oracle against recorded native state and actual mesh/camera.
- `tests/frontend_e2e.py`: menu navigation and actual font pixels in PAL/NTSC;
  record/play/pause/end/exit; full-race serial save and separate-process cold load;
  corrupt/incomplete journal recovery, generation wrap and blank storage.
- Recovery inputs are explicitly **EEPROM-format fault fixtures**, not fabricated
  race times offered as positive gameplay evidence. Persistence proof uses files
  written by the native ROM after real full races.
- The runner now performs cartridge CRC assignment and `EepromInit()` before reset,
  matching the stock GUI loader. Earlier tests did not need file-backed EEPROM.
- World brightness/heartbeat checks remain universal. Active playback now participates
  in the motion watchdog; a legitimately ended or paused replay is allowed to hold.
- The stock GUI test establishes a stationary track baseline after the legitimate
  menu-to-countdown transition, then still rejects premature/absent world motion.

Current exact-ROM verdicts are in `test-results/frontend-summary.json` and the
retained core/HUD/GUI summaries. No physical hardware, automated Windows 2.1.2 or
remote CI validation is claimed. Original notices remain in `NOTICE.md`.

## Evidence retention

Release packaging keeps complete compressed per-field traces and assertion
results, with representative screenshots for older core scenarios (countdown
glyphs, final frame, bank views and different gauge levels). New front-end/replay/
save screenshots are retained. The exact-ROM removal manifest is
`test-results/screenshot-retention.json`; desktop phase sampling is separately
listed in `test-results/gui/screenshot-retention.json`. Tests always run fresh
and do not consume these archived screenshots as success evidence.

## Dynamics update: auxiliary recorded angles

The newer native dynamics build keeps each 64-byte pose/telemetry sample and adds
a corresponding two-byte signed ship/camera pitch pair at `$1b0000..$1b2fff`.
These are 512-step angle units, time-interpolated during playback. They do not
overlap video, and capacity remains 6,144 samples. `recording-angles.bin` in test
evidence is exported from actual native RAM, not manufactured by the harness.
