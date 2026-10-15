# Executed regression results

ROM SHA-256: `4c8a579bd4676e5a7d6a1fb415aaa547ad13cfa459a452f779334654b5de0911`

Both full suites: **PASS**. All positive cases executed fresh.

## Stock Virtual Jaguar desktop

```json
{
  "status": "PASS",
  "rom_sha256": "4c8a579bd4676e5a7d6a1fb415aaa547ad13cfa459a452f779334654b5de0911",
  "emulator_binary_sha256": "9ce9b17eaf33382e3aafce8841f3dc44c5547a140733baf8499254ad21488f86",
  "emulator_version": "Virtual Jaguar v2.1.3 (Final)",
  "cases": {
    "default-ntsc": {
      "status": "PASS",
      "rom_sha256": "4c8a579bd4676e5a7d6a1fb415aaa547ad13cfa459a452f779334654b5de0911",
      "video": "ntsc",
      "boot": "default",
      "command": [
        "/usr/bin/virtualjaguar",
        "/home/user/hexgl-jaguar/rom/hexgl.j64",
        "--ntsc",
        "--gpu",
        "--dsp",
        "--no-blur"
      ],
      "window_bbox": [
        200,
        200,
        852,
        761
      ],
      "elapsed_seconds": 30.53
    },
    "no-bios-ntsc": {
      "status": "PASS",
      "rom_sha256": "4c8a579bd4676e5a7d6a1fb415aaa547ad13cfa459a452f779334654b5de0911",
      "video": "ntsc",
      "boot": "no-bios",
      "command": [
        "/usr/bin/virtualjaguar",
        "/home/user/hexgl-jaguar/rom/hexgl.j64",
        "--ntsc",
        "--gpu",
        "--dsp",
        "--no-blur",
        "--no-bios"
      ],
      "window_bbox": [
        200,
        200,
        852,
        761
      ],
      "elapsed_seconds": 30.33
    },
    "bios-ntsc": {
      "status": "PASS",
      "rom_sha256": "4c8a579bd4676e5a7d6a1fb415aaa547ad13cfa459a452f779334654b5de0911",
      "video": "ntsc",
      "boot": "bios",
      "command": [
        "/usr/bin/virtualjaguar",
        "/home/user/hexgl-jaguar/rom/hexgl.j64",
        "--ntsc",
        "--gpu",
        "--dsp",
        "--no-blur",
        "--bios"
      ],
      "window_bbox": [
        200,
        200,
        852,
        761
      ],
      "elapsed_seconds": 30.02
    },
    "no-bios-pal": {
      "status": "PASS",
      "rom_sha256": "4c8a579bd4676e5a7d6a1fb415aaa547ad13cfa459a452f779334654b5de0911",
      "video": "pal",
      "boot": "no-bios",
      "command": [
        "/usr/bin/virtualjaguar",
        "/home/user/hexgl-jaguar/rom/hexgl.j64",
        "--pal",
        "--gpu",
        "--dsp",
        "--no-blur",
        "--no-bios"
      ],
      "window_bbox": [
        200,
        200,
        852,
        793
      ],
      "elapsed_seconds": 30.16
    },
    "bios-pal": {
      "status": "PASS",
      "rom_sha256": "4c8a579bd4676e5a7d6a1fb415aaa547ad13cfa459a452f779334654b5de0911",
      "video": "pal",
      "boot": "bios",
      "command": [
        "/usr/bin/virtualjaguar",
        "/home/user/hexgl-jaguar/rom/hexgl.j64",
        "--pal",
        "--gpu",
        "--dsp",
        "--no-blur",
        "--bios"
      ],
      "window_bbox": [
        200,
        200,
        852,
        793
      ],
      "elapsed_seconds": 29.82
    },
    "negative-old-entry": {
      "status": "EXPECTED_FAILURE",
      "detected": "world black or untextured at startup deadline"
    },
    "negative-frozen-window": {
      "status": "EXPECTED_FAILURE",
      "detected": "world frozen for 3 seconds during throttle"
    }
  }
}
```

## Virtual Jaguar Rx core

```json
{
  "rom_sha256": "4c8a579bd4676e5a7d6a1fb415aaa547ad13cfa459a452f779334654b5de0911",
  "emulator": "Virtual Jaguar Rx 2.1.3 headless core harness",
  "cases": {
    "manual-ntsc": {
      "checks": [
        "BIOS boot",
        "native entry",
        "nonblack world",
        "GPU heartbeat",
        "DSP sample clock",
        "audible PCM",
        "throttle",
        "steering",
        "pause/resume",
        "collision damage",
        "destruction",
        "restart"
      ],
      "fields": 1200,
      "updates": 64,
      "audio_samples": 157937
    },
    "manual-ntsc-direct": {
      "checks": [
        "direct cartridge boot",
        "native entry",
        "nonblack world",
        "GPU heartbeat",
        "DSP sample clock",
        "audible PCM",
        "throttle",
        "steering",
        "pause/resume",
        "collision damage",
        "destruction",
        "restart"
      ],
      "fields": 1200,
      "updates": 64,
      "audio_samples": 156339
    },
    "race-ntsc": {
      "checks": [
        "BIOS boot",
        "native entry",
        "nonblack world",
        "GPU heartbeat",
        "DSP sample clock",
        "audible PCM",
        "continuous world animation",
        "all checkpoints",
        "boost pads",
        "three laps",
        "finish"
      ],
      "fields": 12393,
      "updates": 3892,
      "race_ticks": 12294,
      "audio_samples": 1648482
    },
    "manual-pal": {
      "checks": [
        "BIOS boot",
        "native entry",
        "nonblack world",
        "GPU heartbeat",
        "DSP sample clock",
        "audible PCM",
        "throttle",
        "steering",
        "pause/resume",
        "collision damage",
        "destruction",
        "restart"
      ],
      "fields": 1200,
      "updates": 65,
      "audio_samples": 189866
    },
    "manual-pal-direct": {
      "checks": [
        "direct cartridge boot",
        "native entry",
        "nonblack world",
        "GPU heartbeat",
        "DSP sample clock",
        "audible PCM",
        "throttle",
        "steering",
        "pause/resume",
        "collision damage",
        "destruction",
        "restart"
      ],
      "fields": 1200,
      "updates": 65,
      "audio_samples": 188427
    },
    "race-pal": {
      "checks": [
        "BIOS boot",
        "native entry",
        "nonblack world",
        "GPU heartbeat",
        "DSP sample clock",
        "audible PCM",
        "continuous world animation",
        "all checkpoints",
        "boost pads",
        "three laps",
        "finish"
      ],
      "fields": 10813,
      "updates": 3893,
      "race_ticks": 10713,
      "audio_samples": 1726207
    },
    "cold-boot-seed-7": {
      "checks": [
        "randomized power-on RAM",
        "direct entry",
        "nonblack world",
        "heartbeat",
        "world animation"
      ],
      "fields": 600
    },
    "cold-boot-seed-42": {
      "checks": [
        "randomized power-on RAM",
        "direct entry",
        "nonblack world",
        "heartbeat",
        "world animation"
      ],
      "fields": 600
    },
    "negative-frozen-gpu": {
      "expected_failure_detected": "World viewport black (includes final field)",
      "process_exit_code": 1,
      "native_heartbeat_stopped": true
    },
    "negative-black-video": {
      "expected_failure_detected": "Black-screen watchdog",
      "process_exit_code": 1,
      "native_heartbeat_stopped": false
    },
    "negative-frozen-video": {
      "expected_failure_detected": "World framebuffer frozen at 420",
      "process_exit_code": 0,
      "native_heartbeat_stopped": false
    }
  },
  "status": "PASS",
  "execution_note": "All cases executed fresh. Direct manual cases executed a second time after correcting their descriptive boot-mode labels; assertions and ROM unchanged."
}
```

Ten watchdog unit tests passed (test-results/unit-tests.log). Remote CI and physical hardware execution are not claimed.
