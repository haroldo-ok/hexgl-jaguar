# HexGL → Atari Jaguar — native, incomplete port

**This is a playable native port-in-progress, not a complete conversion of HexGL.**
It does not meet the request to convert *everything*. The implemented systems
run on Jaguar GPU/DSP assembly and use original assets; omitted systems are
listed below, not represented by empty functions or fake assets.

## Deliverables

- `rom/hexgl.j64` — assembled **6 MiB** cartridge ROM, with retail-BIOS and BIOS-off entry paths.
- `src/` — GPU renderer integration, fixed-point game control, DSP PCM mixer.
  The `.js` extension follows the engine’s Jaguar-assembly convention; these
  files are assembled by lyxass, not executed as JavaScript.
- `tools/` — real-asset conversion, ROM packaging and memory-layout checks.
- `tests/gui_e2e.py` — stock Virtual Jaguar desktop / OpenGL / keyboard E2E test.
- `tests/e2e.py` — Virtual Jaguar Rx core end-to-end test orchestrator.
- `test-results/gui/summary.json` — independent desktop-test verdicts and ROM hash.
- `tests/vjrunner/` — headless front end linking the actual Virtual Jaguar cores.
- `test-results/summary.json` — executed test verdicts, tied to the ROM SHA-256.
- `test-results/*/run_report.json` — field-by-field pixels, native state and audio evidence.
- `vendor/` — pinned upstream source; revisions in `dependencies.lock.json`.
- `docs/PARITY.md` — implemented, changed and missing features.

## Playing

Load `rom/hexgl.j64` in Virtual Jaguar with GPU and DSP enabled. **Both BIOS-on
and BIOS-off now work in the tested Virtual Jaguar versions.** The old build
had no working BIOS-off entry; Virtual Jaguar defaults to BIOS-off, exposing a
startup defect missed by the original BIOS-only harness. This build adds a
68000 cartridge bootstrap at `$900000` while retaining the retail GPU loader.
Select PAL or NTSC before power-on. Physical Jaguar hardware is untested.

```sh
virtualjaguar rom/hexgl.j64 --ntsc --gpu --dsp
# Explicit retail-BIOS path, also tested:
virtualjaguar rom/hexgl.j64 --ntsc --bios --gpu --dsp
```

Stock Virtual Jaguar's default keyboard map: **L = A/thrust, J = C/autopilot,
Z/C = left/right, K = brake, P = pause, O = restart**. Arrow keys are not its
player-one defaults. See `docs/BLACK-SCREEN-FIX.md` for regression coverage.

| Jaguar control | Action |
|---|---|
| A or Up | Start / accelerate |
| Left / Right | Steer |
| B | Brake; increases steering rate |
| Down | Brake |
| Pause | Pause/resume movement and race clock |
| Option | Reset race and shield |
| C | Toggle optional track-following autopilot |

C can be enabled before pressing A. The autopilot follows a centerline extracted
from the original collision image. It is a new test/demo feature, **not** the
original replay. Normal manual driving has no autopilot assistance.

The race uses ordered checkpoints 0 → 1 → 2 → 0 and ends after three laps.
Off-road movement is rejected, speed drops, and shield damage can end the race.
The display uses a native text HUD rather than HexGL's original bitmap HUD.

## What actually runs

- All **12,206 triangles** from the nine Cityscape scene meshes are converted;
  no replacement track or ship geometry is generated. World geometry is
  partitioned into 289 objects, culled and rendered by the adapted engine.
- Original diffuse textures are downsampled to 64×64 Jaguar CrY textures.
- All six original skybox faces are converted to a rotating CrY panorama.
- The original 2048² collision/height images become 512² native maps; height
  decoding retains HexGL's unusual base-255 encoding.
- Native fixed-point acceleration, braking, yaw steering, height following,
  collision damage, boost pads, checkpoints, laps, pause, finish and restart.
- All five original Ogg files are resampled **without duration truncation** to
  7,990 Hz signed PCM8 mono. A DSP mixer streams music, wind, boost, crash and
  destruction sounds from cartridge ROM, paced by JERRY's I2S latch.

## Build

On Debian-like Linux, install system prerequisites:

```sh
sudo apt-get install build-essential pkg-config libsdl2-dev qtbase5-dev \
    zlib1g-dev ffmpeg python3 python3-venv git binutils-m68k-linux-gnu \
    virtualjaguar xvfb xauth xdotool libgl1-mesa-dri
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

With the supplied sources and converted assets:

```sh
make rom                   # builds lyxass, assembles GPU/DSP source, packages ROM
make verify                # checks payload, sources, layout, capacity and hash
```

To regenerate the assets from the pinned originals:

```sh
make assets
make rom
```

The platform's unchanged object-list binaries and encrypted GPU loader are
supplied by the pinned `jag_3d_engine` / `new_bjl` repositories. They are boot and
video metadata, not a substituted game executable. GPU game code and the DSP
mixer are assembled from the delivered source. The assembler is built locally.

The source archive includes dependencies. If using a source-only checkout
without `vendor/`, run `python3 tools/fetch_dependencies.py` first.

## End-to-end validation

```sh
make test                  # compile ROM + unit tests + core E2E + stock desktop E2E
make test-gui              # compile ROM + real Qt/OpenGL GUI test only
make test-core             # compile ROM + detailed PAL/NTSC core tests
make test-quick            # core startup/manual/fault checks; not a release gate
make release               # full test gate, report, then source+ROM ZIP
```

The **desktop test** launches the unmodified installed `virtualjaguar` executable
under Xvfb, with a clean HOME/config on every run. It uses the normal file loader,
Qt input handling, asynchronous SDL audio and OpenGL presentation. It captures
actual window pixels, excludes menus/HUD/status bar, and checks world brightness,
contrast, color diversity and motion. It checks default settings, explicit
BIOS-off/on, PAL/NTSC, start, pause/resume and restart. A recreated broken entry
and an intentionally frozen emulator process must be rejected. The GUI test
never reads or writes Jaguar RAM. `test-results/gui/` contains screenshots,
metrics, commands, executable hash and verdicts.

The **core test** independently links Virtual Jaguar Rx's real CPU/device cores,
boots the production cartridge through both entry paths, supplies joystick input,
and observes native telemetry, actual TOM output and DSP audio. Detailed tests
cover throttle, steering, collision, destruction, restart, boost pads, ordered
checkpoints, two complete three-lap races and randomized power-on RAM. Video
checks include the final field; native heartbeat cannot excuse black or frozen
output. Deliberately halted GPU, blank video with live gameplay, and frozen video
with live gameplay must all fail the assertions. The core harness uses VJ's sound
callback synchronously; the desktop test covers its normal asynchronous path.

All positive runs are fresh. No saved trace reuse is permitted. Timeouts, emulator
crashes and nonzero positive exit codes fail the suite. `tools/bundle.py` refuses
to package a ROM unless BOTH full suites passed for its exact SHA-256.
`.github/workflows/virtual-jaguar.yml` runs the same gate in CI (workflow supplied;
remote CI execution is not claimed).

Tests detect and block the covered regressions; they cannot guarantee that every
possible input sequence or emulator/driver configuration will never freeze.
Physical hardware remains unverified. The GUI needs X11/Xvfb, Mesa OpenGL and the
stock Virtual Jaguar package, not just the headless runner.

## Main limitations

Physics/camera behavior is not a line-for-line translation. No original bitmap
HUD/menu flow, race-recording system, online ladder, particles, bloom, real-time
shadows, normal/specular lighting, or full fall/repulsion behavior. Rendering is
affine textured, with visible quantization and clipping artifacts. The unused
Edge mesh is converted separately but is not a playable second track (nor is
it wired into the upstream Cityscape launcher).

See `docs/PARITY.md` for the precise boundary between asset conversion and
runtime support. Do not advertise this build as the requested complete port.

## Credits and licensing

HexGL: Thibaut “BKcore” Despoulain and contributors; original model/texture and
sound credits remain in `vendor/HexGL`. Renderer/SDK: 42Bastian. Emulator:
Virtual Jaguar / Virtual Jaguar Rx contributors.

**Do not assume the entire bundle is MIT.** HexGL's top-level license and
per-file CC BY-NC notices coexist; its README explicitly makes file-specific
notices exceptions. Audio has separate credits/licenses. Emulator/harness
licensing is separate from the game. See `NOTICE.md` and `licenses/`.
