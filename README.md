# HexGL → Atari Jaguar

A playable, **incomplete native port** of BKcore's HexGL using 42Bastian's
`jag_3d_engine`. The target is a **standalone stock Jaguar ROM**: gameplay and
rendering run on the console, with no host bridge or enhanced-emulator dependency.
Online services are excluded; local cartridge records replace online scores.

The port uses original assets and native GPU/DSP assembly, but it is **not a
complete or visually equivalent conversion of HexGL**. Physical Jaguar hardware
has not been tested. See [remaining work](#remaining-work-and-limitations).

## Current release

**Release snapshot: 17 October 2026.** Standalone stock-Jaguar target; 6 MiB
cartridge ROM, native GPU/DSP/68000 code, and no host networking bridge.

| Release item | Recorded status |
| --- | --- |
| Build | Compiled ROM; structure and memory checks passed |
| Validation | 99 unit tests and 48 end-to-end scenarios passed |
| Native depth fixtures | 12 passed in a separately labeled diagnostic ROM |
| Reproducibility | Clean source/asset rebuild produced a byte-identical ROM; NTSC/PAL boot checks passed |
| Completion | Incomplete port; physical Jaguar hardware untested |

Quick links: [Build](#build-from-source) · [Controls](#quick-start) ·
[Validation](#validation) · [Visual report](REPORT.html) ·
[Remaining work](#remaining-work-and-limitations) · [Licensing](NOTICE.md).

The latest integration adds **perspective particles, real RGB composition and
original-channel stereo ADPCM**:

- Per-texel clipped perspective sizing, additive sparks/glow and alpha-over clouds.
- Approximately 0.7 ship-motion inheritance in newly emitted particle velocity.
- Conservative center-depth queries against actual submitted triangle vertex Z;
  separately executed native GPU fixtures validate rejection boundaries.
- Complete-duration original left/right channels, independently decoded on the
  DSP from a stereo IMA4 bank that fits the existing one-MiB cartridge slot.
- Stronger read-only source-texel, RGB, actual-framebuffer and DSP-source oracles.

See [particles and original stereo](docs/PARTICLES-AND-ORIGINAL-STEREO.md) for
algorithms, compromises, memory layout, evidence and remaining gaps.

Retained material/lighting, camera-sky and spatial-audio systems:

- **Original normal/specular/environment maps:** eight directional lookup banks
  consumed by the native renderer; source highlights and scraper sky reflections.
- **Static sun shadows:** actual scene-triangle ray tests baked into face luminance.
- **Booster scene light:** thrust-sensitive local illumination on rendered faces,
  separate from the existing glow sprite.
- **Material behavior:** ordered-alpha transparent booster texels, a double-sided
  start banner, and the source blue speed-pad material.
- **Pitched sky:** a taller six-face-source panorama follows real camera pitch/yaw
  with native seam-wrap blits, including during replay.
- **Spatial stereo:** the DSP sends distinct saturating left/right samples to
  JERRY for wind/boost/collisions while music/destruction remain centered.
- **Fall arithmetic fix:** correct displacement at every capped 1..6-field step.

These are documented hardware adaptations, not per-fragment shader or WebAudio
equivalence. See [materials, sky and stereo](docs/MATERIALS-SKY-AND-STEREO.md).

The previous integration added:

- **Airbrake drift:** B + Left/Right applies lateral movement as well as stronger
  steering and banking.
- **Contact response:** map-derived inward impulses persist and decay after an
  impact, rather than relying only on position rejection.
- **Hover and falling:** bilinear height-map following, smoothed descents, and
  unsupported falls ending in destruction after 1.5 seconds of active video time.
- **Ship pitch:** terrain grade drives the actual ship and booster transforms.
- **Chase-camera pitch:** vertical look-at rotation affects rendered vertices and
  normals, alongside speed-sensitive pullback and height filtering.
- **Native effects:** original spark/cloud textures drive a bounded world-space
  particle pool with lifetimes, fading and pause. The original booster glow sprite
  follows the ship's stern and responds to speed/boost.
- **Pitched replay:** actual-run recording now includes interpolated ship and
  camera pitch without reducing the 6,144-sample capacity.

These are hardware-adapted implementations, not claims of full source parity.
[Implementation details](docs/DYNAMICS-AND-EFFECTS.md) describe the algorithms,
source mapping, memory layout and explicit compromises.

### Other implemented systems

| System | Current implementation |
| --- | --- |
| Cityscape geometry | All 12,206 triangles from nine scene meshes, partitioned into 289 runtime objects |
| Artwork and terrain | Original diffuse textures converted to 64² CrY; six skybox faces baked into a pitch/yaw-following panorama; original collision/height maps reduced from 2048² to 512² |
| Racing | Acceleration, braking, steering, boost pads, shield damage, ordered checkpoints, three laps, destruction, finish and restart |
| Race flow | Seven-second Get Ready / 3 / 2 / 1 / GO countdown; input lock before GO; PAL/NTSC video-clock timers, lap splits and best lap |
| HUD | All three original speed/shield bitmap layers, live clipping and native numeric/timing readouts |
| Menus | Original background/title artwork and Bebas Neue typography; Start, Controls, Local Records, Credits, Replay and results |
| Replay | Actual native run samples with elapsed-field interpolation, pause, end hold and Option exit; not the supplied static upstream replay |
| Saved records | Real serial EEPROM I/O, separate manual/autopilot records, two-slot journals, checksums, readback and bounded waits |
| Audio | All five original Ogg tracks/effects converted without duration truncation to 7,990 Hz original-channel stereo IMA4; independent native left/right centered/spatial buses through JERRY I2S |
| Boot paths | Retail-BIOS GPU loader and a 68000 cartridge entry for BIOS-off loading |

## Quick start

Load [`rom/hexgl.j64`](rom/hexgl.j64) in Virtual Jaguar with **GPU and DSP enabled**.
Choose PAL or NTSC before power-on. Both BIOS-on and BIOS-off entry paths passed
in the tested emulator configurations.

```sh
virtualjaguar rom/hexgl.j64 --ntsc --gpu --dsp
# Explicit retail-BIOS entry:
virtualjaguar rom/hexgl.j64 --ntsc --bios --gpu --dsp
```

### Controls

| Jaguar control | Action | Stock Virtual Jaguar keyboard default |
| --- | --- | --- |
| A | Confirm menu / begin countdown / accelerate after GO | L |
| Up / Down | Navigate menus; thrust / brake during a race | S / X |
| Left / Right | Steer | Z / C |
| B | Brake; with a direction, stronger steering and lateral airbrake drift | K |
| C | Toggle optional track-following autopilot | J |
| Pause | Pause/resume gameplay and replay | P |
| Option | Return to Start / reset race and shield | O |

**S/X navigate the menu and L confirms.** Arrow keys are not the stock
player-one defaults; configured controller profiles may differ.

Autopilot follows a centerline extracted from the original collision image. It
is a native test/demo feature, **not** original HexGL replay. Its records are kept
separate from manual records. The assisted waypoint path does not run the full
manual integrator: its boost latch currently remains set between pads. It is
not evidence of source-equivalent boost kinetics.

### Replay and saves

- Replay Last Run becomes available after a run produces samples. Option retains
  that recording; starting a new countdown replaces it.
- Replay holds up to **6,144 samples**, plus recorded pitch pairs, in RAM. A full
  buffer retains a playable prefix. Power-off loses the recording.
- Best times require an EEPROM-equipped cartridge/compatible flash cart, or an
  emulator with writable EEPROM storage. EEPROM does not store the replay.
- Virtual Jaguar identifies EEPROM files by ROM CRC, so a changed ROM build may
  use a different emulator save file.

See [front end, replay and saves](docs/FRONTEND-REPLAY-SAVES.md).

## Build from source

The archive includes pinned upstream sources and converted assets. Revisions
are recorded in [`dependencies.lock.json`](dependencies.lock.json). The `.js`
files in `src/` follow the engine's **Jaguar assembly** naming convention: lyxass
assembles them; they are not browser JavaScript.

On Debian-like Linux, install the build and emulator-test prerequisites:

```sh
sudo apt-get install build-essential pkg-config libsdl2-dev qtbase5-dev \
    zlib1g-dev ffmpeg python3 python3-venv git binutils-m68k-linux-gnu \
    virtualjaguar xvfb xauth xdotool libgl1-mesa-dri
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Use a Python version supported by the pinned packages in `requirements.txt`.
From the extracted `hexgl-jaguar/` directory:

```sh
make rom       # build assembler; assemble GPU/DSP/68000 code; package and verify
make verify    # verify the assembled payload, ROM layout, assets and capacities
```

To regenerate the asset groups from the supplied originals:

```sh
make assets               # original material/shadow/geometry/terrain/sky/audio/route conversion
make rom                  # also regenerates UI/HUD/effects art and response tables
```

`make assets` now runs `tools/materials.py` before `tools/convert.py`, so the
regenerated geometry includes fresh source-bound static shadow results. Individual
converter tools remain available for focused development; keep that dependency
order when changing geometry. It requires FFmpeg for original audio conversion.

The encrypted GPU loader and object-list binaries come from the pinned engine
and SDK. They are boot/video metadata, not a substituted game executable. Game
integration and the DSP mixer are assembled from the delivered source. Generated
host executables and object libraries are excluded from the archive and rebuilt
locally. If using a checkout without `vendor/`, run
`python3 tools/fetch_dependencies.py` before building.

## Validation

### Recorded results for the bundled ROM

| Gate | Result |
| --- | --- |
| Unit tests | **99 passed** |
| Core gameplay / boot / fault scenarios | **17 passed**, including expected fault rejections |
| Stock desktop emulator scenarios | **7 passed**, including expected fault rejections |
| Focused HUD scenarios | **2 passed** |
| Front-end / replay / EEPROM scenarios | **10 passed** |
| Dynamics / camera / effects scenarios | **4 passed** |
| Materials / sky / stereo scenarios | **2 passed** |
| Dedicated falling / pause scenarios | **4 passed** |
| Original stereo / audio-event scenarios | **2 passed** |
| Separate native GPU depth fixtures | **12 passed**, including three actual rejection cases |
| Separate clean rebuild | **Byte-identical ROM**, plus NTSC/PAL smoke checks |

That is **48 end-to-end scenarios**, plus 12 separate native GPU depth fixtures,
unit tests and the separate clean-build checks. These are recorded results for the ROM identified below, not a claim
that documentation edits rerun the tests.

The tests cover full PAL/NTSC races, fresh-process EEPROM loading, journal
recovery, replay interpolation, original-art pixels, actual transformed/projected
ship vertices, bilinear hover and particle integration. New tests additionally verify source texel addressing, perspective sizes, RGB blends,
actual composed framebuffer pixels, native triangle reciprocal depth, source DSP
samples, actual stereo PCM, runtime material
bank addresses, scene-face light arithmetic and thousands of exact camera-pitched
sky pixels. Additional post-run
checks verify fall displacement/timing, pause during falling, and recorded pitch
pairs against observed gameplay.

The desktop gate launches the stock Qt/OpenGL emulator under Xvfb, supplies
normal keyboard input and measures actual window pixels without reading game
RAM. The headless harness links Virtual Jaguar Rx's real device cores and observes
native state, TOM output and DSP audio. Halted-GPU, black-video, frozen-video and
frozen-desktop controls must be rejected; a live heartbeat cannot excuse a
black or frozen picture.

- [Visual report](REPORT.html)
- [Detailed results](docs/TEST-RESULTS.md)
- [Clean-build proof](docs/dynamics-clean-rebuild.json)
- [Additional observed-state checks](docs/dynamics-additional-checks.json)
- [Native GPU depth-fixture results](test-results/native-fx-probe/summary.json)
- [Original stereo and audio-event results](test-results/original-audio-summary.json)
- [Recorded one-shot/stereo checks](docs/particles-audio-additional-checks.json)

### Run the gates

```sh
make test          # build, unit tests, all eight emulator suites and post-run checks
make test-core     # detailed core/HUD/dynamics/frontend tests; no desktop suite
make test-gui      # stock Qt/OpenGL desktop tests
make test-unit     # Python unit tests
make test-materials # focused NTSC/PAL material/sky/stereo gate
make test-fall     # dedicated fall/pause, both boot paths and video standards
make test-clean    # isolated source rebuild and two emulator smoke checks
make test-quick    # reduced core/manual/fault coverage; not a release gate
make release       # full tests + clean rebuild + report + source/ROM ZIP
```

`make test` executes fresh emulator runs. The explicit post-run checker reads
those observations; it does not replace emulator execution. Timeouts, crashes
and nonzero positive-run exit codes fail the suite. Release packaging requires
all eight suites, native depth fixtures, clean-build proof and additional checks to match the exact ROM
SHA-256. The supplied CI workflow is not evidence of an executed remote CI run.

Complete per-field traces are retained as lossless `.json.gz` files. Screenshots
are sampled after validation; retention manifests record removals. Finite tests
cannot guarantee every input sequence or emulator/driver configuration.

## Repository and archive contents

| Path | Purpose |
| --- | --- |
| `rom/hexgl.j64` | Compiled 6 MiB cartridge ROM |
| `rom/verification.json` | ROM identity, memory bounds and asset checks |
| `src/` | Native gameplay, renderer, effects, menus, recording, EEPROM and audio code |
| `assets/` | Converted original content, response tables and provenance manifests |
| `tools/` | Conversion, build preparation, verification, reporting and packaging |
| `tests/` | Unit tests, real-emulator harness, E2E runners and independent oracles |
| `test-results/` | Executed verdicts, logs, compressed traces and retained captures |
| `vendor/` | Pinned upstream code and original assets |
| `docs/` | Implementation notes, parity boundaries and validation details |
| `licenses/`, `NOTICE.md` | License texts, exceptions and attribution |

The release ZIP extracts into `hexgl-jaguar/` and contains source, dependencies,
converted assets, the compiled ROM and test evidence. Its companion `.sha256`
file verifies the ZIP itself. Extract it before building; generated host
executables and object libraries are intentionally omitted. The source archive
includes the original assets, license notices, conversion tools and native test
fixtures, not just the assembled game.

To check the downloaded archive on Linux:

```sh
sha256sum -c HexGL-Jaguar-source-and-ROM.sha256
```

**Bundled ROM:** 6,291,456 bytes (6 MiB).

```text
SHA-256
fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8
```

## Remaining work and limitations

- Fully source-equivalent angular/contact physics and cross-slope tilt.
- Quaternion/up-vector camera behavior, camera roll and orbit modes. Sky pitch
  is now implemented through a cylindrical panorama crop, not a rotated cubemap.
- Full source emitter/random-color/lifetime fidelity and per-pixel depth behavior.
  Native perspective sizing, RGB additive/alpha-over and 0.7 velocity inheritance
  now run; center-only depth is an adaptation, not source-default depth semantics.
- Full tangent-basis/per-fragment normal/specular response, moving ship shadows,
  colored local lighting and bloom. Source-map lookup banks, static centroid shadows
  and monochrome booster face lighting now run; they do not imply shader parity.
- WebAudio-equivalent spatial/HRTF audio and full gain/trigger fidelity.
  Original-channel stereo is now preserved via lossy IMA4; native balance is not
  HRTF. The original source defines no audio filters; the previous filter gap was an audit error, not an omitted source system.
- Remaining browser-equivalent presentation, typography, transitions and settings.
- Physical Jaguar timing and cartridge/EEPROM compatibility verification.

Rendering is affine textured and has visible quantization and clipping artifacts.
The unused Edge mesh is converted but is not a playable second track; the upstream
Cityscape launcher did not wire it in either. Online services are excluded by the
standalone-stock target, not represented by fake local networking functions.

See [PARITY.md](docs/PARITY.md) and
[STOCK-JAGUAR-SCOPE.md](docs/STOCK-JAGUAR-SCOPE.md) for the precise boundary between
conversion, runtime support, adaptations and missing systems.

## Credits and licensing

- **HexGL:** Thibaut “BKcore” Despoulain and contributors; original model, texture
  and audio credits remain in `vendor/HexGL`.
- **Jaguar renderer and SDK:** 42Bastian.
- **Emulator:** Virtual Jaguar / Virtual Jaguar Rx contributors.

**Do not assume the entire bundle is MIT.** HexGL's top-level license coexists
with file-specific CC BY-NC 3.0 notices. Audio has separate licenses and credits;
emulator/harness licensing is separate from the game. Preserve these exceptions
when redistributing. See [NOTICE.md](NOTICE.md) and [`licenses/`](licenses/).
