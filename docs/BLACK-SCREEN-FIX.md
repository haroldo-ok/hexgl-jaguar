# Black-screen regression: diagnosis and correction

## Confirmed defect, not a claim about every user configuration

The previous cartridge (`935f4d18e90da997d52329fa063dfe7ca485d3926ab4b6f78ed5836bb1fffe76`)
contained the encrypted GPU bootstrap used by 42Bastian's engine. Its cartridge
header advertised a 68000 entry at `$802000`, but that location was part of the
GPU payload, not a valid 68000 bootstrap. With the retail BIOS enabled, the BIOS
decrypted and ran the GPU loader and the game displayed. With BIOS disabled,
Virtual Jaguar executed the wrong instruction stream. The stock executable was
unable even to present the game window during the observed startup deadline.

Virtual Jaguar defaults `useJaguarBIOS` to false. The previous harness forced it
to true. Its passing results therefore did not cover the default startup path.
The earlier assurance was too broad. `docs/black-screen-before/` holds captures
of the old ROM with BIOS off and on. The user's exact emulator/version/settings
were not supplied, so other causes on that machine have not been ruled out.

## ROM correction

`src/cart_boot.S`, assembled with GNU m68k binutils, supplies an actual 68000
entry at `$900000`, inside previously unused cartridge space. It disables
interrupts during setup, stops GPU/DSP/OP, installs the same 68000 interrupt
acknowledgement loop expected by the GPU engine, copies the existing BS94 payload
from ROM to its declared RAM destination, starts the GPU, and enters the CPU
interrupt-acknowledgement loop. The cartridge entry field at offset `$404` now
points to this stub. The encrypted retail loader bytes remain unchanged; only
its external entry-address field is updated. Meshes, gameplay and DSP payload
are unchanged by this fix.

`tools/verify.py` verifies both paths' payload placement, exact bytes, entry
address and non-overlap. No emulator RAM patch or test-only positive ROM is used.

## Two independent end-to-end layers

### Stock GUI (tests/gui_e2e.py)

- Debian stock Virtual Jaguar 2.1.3 executable, normal cartridge file loading.
- Fresh configuration for every process; real Qt input, OpenGL presentation,
  and asynchronous SDL audio (dummy host audio device in CI).
- Actual X11 window captures via Pillow, not an image from our core harness.
- Cropped lower-middle world viewport excludes desktop, menus, HUD and status.
- Visible world requires lit fraction >15%, luma standard deviation >3, and
  at least 8 quantized colors. A bright solid screen cannot pass.
- During throttle, requires >2% changing world pixels and fails a 3-second
  world stall. A 1.5-second dark/untextured interval after boot fails.
- Boot deadline 15 seconds; missing window is a failure, not a skip.
- Default NTSC, explicit BIOS-off NTSC/PAL, BIOS-on NTSC/PAL.
- Start with real A/C keyboard events; pause/resume and restart with real keys.
- Negative controls recreate the old bad entry and freeze the whole emulator
  process after movement has been observed. Both must be rejected.

These wall-clock checks are intentionally stricter than a final screenshot, but
sample at roughly 2 Hz; they are supplemented by per-field core observations.

### Actual VJ Rx cores (tests/e2e.py + tests/vjrunner)

- Native entry deadline, continuous native-state signature, heartbeat watchdog.
- Visible world checked through the final field, closing the old unchecked tail.
- Moving gameplay must also change world pixels; telemetry alone is insufficient.
- Four manual runs across BIOS-on/off and NTSC/PAL; two full three-lap races.
- Additional cold boots with two randomized power-on RAM seeds.
- Audible PCM and advancing native DSP sample counter.
- Three injected faults: disabled GPU, black observed video with live game code,
  frozen observed video with live game code. The last two prove that advancing
  counters cannot mask broken presentation. Fault injections are only in the
  test harness, not in the game ROM or stock GUI emulator.
- Fresh subprocess executions, no trace reuse. Crashes, timeouts, truncated
  reports and nonzero positive exits fail.

Ten small unit tests exercise the watchdog assertions separately, including
black-at-final-field, HUD-only output, live telemetry with frozen video,
animated video with dead heartbeat, valid paused output, and solid-color output.
Synthetic unit fixtures are not presented as game execution evidence.

## Release guard

`make test` rebuilds the ROM before running all layers. `make release` then
creates the report and bundle. Packaging requires current-ROM SHA-256 matches
and PASS from both full E2E suites. CI configuration is included; local execution
results are in `test-results/`, not claimed as remotely executed CI.

This prevents the reproduced startup defect from passing the supplied release
gate. It does not prevent every conceivable future freeze, guarantee physical
Jaguar compatibility, or complete the remaining HexGL porting work.
