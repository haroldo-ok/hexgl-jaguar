# Race-flow milestone

## Scope

This increment implements the timing/flow part of HexGL's Gameplay.js on the
Jaguar. It does not complete the original bitmap HUD or browser menus. It retains
the playable Cityscape port, both cartridge entry paths, and the black-screen
tests from the preceding build.

Reference: `vendor/HexGL/bkcore/hexgl/Gameplay.js`, particularly `start`, `update`,
`modes.timeattack` and `end`. Preserve its CC BY-NC 3.0 notice and the existing
project notices. The implementation uses native GPU assembly, not JavaScript.

## Implemented behavior

- A/Up begins countdown from READY. The original HUD-enabled delays are used:
  Get ready for 2.5 seconds, 3 for 1.5 seconds, 2 for 1.5 seconds, 1 for 1.5 seconds.
  GO occurs after seven active seconds. Its message lasts half a second.
- Inputs cannot accelerate, steer, move the ship, or advance the race timer
  before GO. Autopilot can be armed during countdown but cannot move early.
- Pause freezes countdown or racing. Resume does not add paused time. Option
  resets state, lap results and best-lap value and returns to READY.
- Elapsed and current-lap times use the uncapped VBL delta; physics retains its
  capped integration step. PAL uses 50 ticks/second, NTSC 60. This prevents slow
  rendering or capped movement integration from silently shortening the timer.
- Ordered checkpoint crossings record each completed lap as total minus the
  previous lap-start time. Best lap is the minimum completed split this race.
- Lap 3 displays FINAL LAP. Finish freezes position and clock, retaining the
  total, three splits and best lap until reset. Destruction also freezes time.
- Display is `MM:SS.mmm`. Milliseconds are derived by integer division from
  video fields, not a claim of millisecond clock resolution: roughly 16.67 ms
  NTSC and 20 ms PAL. Display minutes wrap modulo 100; underlying field counters
  are not truncated. This is a time-attack course, not a 100-minute endurance UI.

## Intentional adaptations and remaining gaps

The original browser automatically enters its result/menu callback two seconds
after ending. Here the native results remain visible until Option. The original
animated message fades and bitmap HUD are not implemented. FINAL LAP remains
visible through the last lap, apart from pause/GO messages. Best lap is in RAM,
not EEPROM and not a cross-session record. No leaderboard, saved replay or new
sound sample is claimed. The world renderer and simplified physics are unchanged.

## Source layout

- `src/control.js`: READY/COUNTDOWN/RACING/DESTROYED/FINISHED transitions, raw
  VBL timing, lap capture, best lap and reset.
- `src/race_hud.inc`: native four-line text HUD, countdown/status selection,
  fixed-width numeric/time formatting with non-overlapping fields. Status messages
  occupy the first line; all four lines fit inside NTSC visible output.
- `src/game.h`: state layout.
- `tests/e2e.py`: gameplay and timing assertions on actual emulator runs.
- `tests/gui_e2e.py`: real desktop captures and keyboard input; waits for countdown
  completion without mistaking a valid still scene for a frozen renderer.

## Additional telemetry (read-only to tests)

The original first 20 words at `$1000` remain in the same positions.

| Word | Address | Meaning |
|---|---|---|
| 2 | `$1008` | Phase: 0 ready, 1 racing, 2 destroyed, 3 finished, **4 countdown** |
| 3 | `$100c` | Active countdown fields |
| 20 | `$1050` | Video frequency, 50 or 60 |
| 21 | `$1054` | Last completed lap boundary, in race fields |
| 22–24 | `$1058–$1060` | Completed lap 1, 2 and 3 fields |
| 25 | `$1064` | Best completed lap fields, zero before any completion |
| 26 | `$1068` | Backing DRAM address of selected HUD message |
| 27 | `$106c` | Backing DRAM address of selected status word |

The runner captures all 28 words. Six displayed time strings are copied from
native formatter buffers at `$1205`, `$1213`, `$1222`, `$1243`, `$1252`, `$1261`.
These are produced by the game and passed to its real text renderer. Screenshots
also capture the actual output; formatted text is not fabricated by the tests.

## Regression coverage

Each manual PAL/NTSC and BIOS-on/off scenario includes countdown before driving.
Checks cover all four countdown messages in order, original transition timing,
no movement/clock advance before GO, correctly selected 50/60 Hz rate, formatted
elapsed time within one rendering update, and race-clock deltas equal to VBL
deltas. Separate scenarios pause midway through countdown and resume it.

Two full three-lap races additionally require all splits positive, their sum
exactly equal to total race time, best lap equal to the minimum split, displayed
splits matching the native values, FINAL LAP notification, and a stable results
screen after finish. The runner continues for 180 video fields after finish so
these are checked, rather than ending at the instant the finish flag is set.

The previous whole-run animation-percentage heuristic was incompatible with
intentional static countdown/results screens. It is replaced by a continuous,
state-aware moving-world watchdog. Brightness and heartbeat checks remain active
in all phases. Deliberately frozen/black output still must fail; thresholds were
not lowered to hide a failing game. Unit cases cover valid static countdown and
finish scenes alongside invalid black output or stalled native code.

See `test-results/summary.json`, `test-results/gui/summary.json` and REPORT.html
for the actual verdicts for the distributed ROM, rather than assuming this
feature description itself constitutes test evidence.

Screenshot assertions match the original font glyphs against actual TOM pixels
for GET READY, 3, FINISH and all six result time fields. This catches text that
exists in telemetry but is clipped off the visible screen.

The corrupted-entry negative control now may crash the stock emulator rather
than leave it presenting black: moving the GPU payload changes the invalid
68000 instruction stream at the deliberately wrong entry. The GUI test accepts
this rejection as an expected failure for that negative ROM only; crashes of
any positive ROM case still fail the suite. The first run's classification
failure is preserved in docs/gui-negative-before-classification.json. All GUI
cases were rerun after correcting the expected-negative classification.

The upstream text object began two visible lines too low: the last ink row of
lap digits was clipped in NTSC output. prepare_engine.py now derives all four
object lists from upstream and moves only the text bitmap up four half-lines
(two visible lines). The text overlays the last two world lines; no RAM layout
or geometry is changed. Glyph-pixel tests exposed and now guard this defect.
