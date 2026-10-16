# Native dynamics, effects and retained systems: executed results

ROM SHA-256: `bfe5591fa30c95baa290f2591253d1ff47e12639a92b37d7bc9980d8456f1faa`

Five suites: **PASS**. 53 unit tests: **PASS**.

## Core

```json
{
  "rom_sha256": "bfe5591fa30c95baa290f2591253d1ff47e12639a92b37d7bc9980d8456f1faa",
  "emulator": "Virtual Jaguar Rx 2.1.3 headless core harness",
  "cases": {
    "manual-ntsc": {
      "checks": [
        "BIOS boot",
        "seven-second countdown",
        "3/2/1/GO display",
        "throttle locked until GO",
        "wall-clock timing",
        "formatted timer",
        "nonblack world",
        "heartbeat",
        "audio",
        "throttle",
        "steering",
        "pause/resume",
        "collision",
        "destruction",
        "restart"
      ],
      "fields": 2040,
      "updates": 64,
      "audio_samples": 269798
    },
    "manual-ntsc-direct": {
      "checks": [
        "direct cartridge boot",
        "seven-second countdown",
        "3/2/1/GO display",
        "throttle locked until GO",
        "wall-clock timing",
        "formatted timer",
        "nonblack world",
        "heartbeat",
        "audio",
        "throttle",
        "steering",
        "pause/resume",
        "collision",
        "destruction",
        "restart"
      ],
      "fields": 2040,
      "updates": 63,
      "audio_samples": 268067
    },
    "race-ntsc": {
      "checks": [
        "BIOS boot",
        "countdown",
        "nonblack world",
        "heartbeat",
        "audio",
        "continuous world animation",
        "checkpoints",
        "boost",
        "three laps",
        "lap splits",
        "best lap",
        "frozen finish clock",
        "finish results",
        "bank filter",
        "speed camera",
        "terrain-height filtering",
        "renderer pose"
      ],
      "motion_checks": {
        "verified_updates": 3864,
        "height_filtered_updates": 2901,
        "left_bank_seen": true,
        "right_bank_seen": true
      },
      "fields": 14000,
      "updates": 4061,
      "race_ticks": 13298,
      "lap_ticks": [
        4465,
        4417,
        4416
      ],
      "audio_samples": 1862483
    },
    "manual-pal": {
      "checks": [
        "BIOS boot",
        "seven-second countdown",
        "3/2/1/GO display",
        "throttle locked until GO",
        "wall-clock timing",
        "formatted timer",
        "nonblack world",
        "heartbeat",
        "audio",
        "throttle",
        "steering",
        "pause/resume",
        "collision",
        "destruction",
        "restart"
      ],
      "fields": 1900,
      "updates": 66,
      "audio_samples": 301739
    },
    "manual-pal-direct": {
      "checks": [
        "direct cartridge boot",
        "seven-second countdown",
        "3/2/1/GO display",
        "throttle locked until GO",
        "wall-clock timing",
        "formatted timer",
        "nonblack world",
        "heartbeat",
        "audio",
        "throttle",
        "steering",
        "pause/resume",
        "collision",
        "destruction",
        "restart"
      ],
      "fields": 1900,
      "updates": 66,
      "audio_samples": 299981
    },
    "race-pal": {
      "checks": [
        "BIOS boot",
        "countdown",
        "nonblack world",
        "heartbeat",
        "audio",
        "continuous world animation",
        "checkpoints",
        "boost",
        "three laps",
        "lap splits",
        "best lap",
        "frozen finish clock",
        "finish results",
        "bank filter",
        "speed camera",
        "terrain-height filtering",
        "renderer pose"
      ],
      "motion_checks": {
        "verified_updates": 3864,
        "height_filtered_updates": 2907,
        "left_bank_seen": true,
        "right_bank_seen": true
      },
      "fields": 12237,
      "updates": 4055,
      "race_ticks": 11604,
      "lap_ticks": [
        3892,
        3856,
        3856
      ],
      "audio_samples": 1953789
    },
    "bank-ntsc": {
      "verified_updates": 153,
      "height_filtered_updates": 0,
      "left_bank_seen": true,
      "right_bank_seen": true,
      "half_second_left_roll_q8": -45390,
      "checks": [
        "left/right bank",
        "airbrake bank",
        "return to level",
        "pause freezes renderer pose",
        "restart clears filters",
        "actual ship and booster angles",
        "fixed-point recurrence",
        "PAL/NTSC coefficients"
      ],
      "fields": 1180,
      "capture_fields": {
        "left": 632,
        "right": 752,
        "airbrake": 872,
        "paused": 1052
      }
    },
    "camera-speed-ntsc": {
      "verified_updates": 76,
      "height_filtered_updates": 0,
      "left_bank_seen": false,
      "right_bank_seen": false,
      "checks": [
        "speed-dependent pullback",
        "smooth camera distance",
        "return after braking",
        "rendered camera position",
        "fixed-point recurrence"
      ],
      "fields": 820
    },
    "bank-pal": {
      "verified_updates": 149,
      "height_filtered_updates": 0,
      "left_bank_seen": true,
      "right_bank_seen": true,
      "half_second_left_roll_q8": -46748,
      "checks": [
        "left/right bank",
        "airbrake bank",
        "return to level",
        "pause freezes renderer pose",
        "restart clears filters",
        "actual ship and booster angles",
        "fixed-point recurrence",
        "PAL/NTSC coefficients"
      ],
      "fields": 1000,
      "capture_fields": {
        "left": 542,
        "right": 642,
        "airbrake": 742,
        "paused": 892
      }
    },
    "camera-speed-pal": {
      "verified_updates": 83,
      "height_filtered_updates": 0,
      "left_bank_seen": false,
      "right_bank_seen": false,
      "checks": [
        "speed-dependent pullback",
        "smooth camera distance",
        "return after braking",
        "rendered camera position",
        "fixed-point recurrence"
      ],
      "fields": 700
    },
    "countdown-pause-ntsc": {
      "checks": [
        "countdown pause/resume",
        "seven-second active countdown",
        "no premature movement",
        "correct GO",
        "timer formatting"
      ],
      "fields": 1200
    },
    "countdown-pause-pal": {
      "checks": [
        "countdown pause/resume",
        "seven-second active countdown",
        "no premature movement",
        "correct GO",
        "timer formatting"
      ],
      "fields": 1200
    },
    "cold-boot-seed-7": {
      "checks": [
        "randomized power-on RAM",
        "direct entry",
        "nonblack world",
        "heartbeat",
        "world animation"
      ],
      "fields": 1100
    },
    "cold-boot-seed-42": {
      "checks": [
        "randomized power-on RAM",
        "direct entry",
        "nonblack world",
        "heartbeat",
        "world animation"
      ],
      "fields": 1100
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
      "expected_failure_detected": "World framebuffer frozen at 810",
      "process_exit_code": 1,
      "native_heartbeat_stopped": false
    }
  },
  "bitmap_hud": {
    "manual-ntsc": {
      "checks": [
        "original three PNG layers in actual TOM output",
        "HUD.js speed trapezoid and shield rectangle",
        "native speed/shield digits",
        "recent live game state"
      ],
      "captures": [
        {
          "capture": "frame_00180.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00280.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00380.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00480.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00580.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_00800.png",
          "speed": 0,
          "shield": 88,
          "pixels": 1718
        },
        {
          "capture": "frame_01200.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "final.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        }
      ]
    },
    "manual-ntsc-direct": {
      "checks": [
        "original three PNG layers in actual TOM output",
        "HUD.js speed trapezoid and shield rectangle",
        "native speed/shield digits",
        "recent live game state"
      ],
      "captures": [
        {
          "capture": "frame_00180.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00280.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00380.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00480.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00580.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_00800.png",
          "speed": 0,
          "shield": 88,
          "pixels": 1718
        },
        {
          "capture": "frame_01200.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "final.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        }
      ]
    },
    "race-ntsc": {
      "checks": [
        "original three PNG layers in actual TOM output",
        "HUD.js speed trapezoid and shield rectangle",
        "native speed/shield digits",
        "recent live game state"
      ],
      "captures": [
        {
          "capture": "frame_00180.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00280.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00380.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00480.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00580.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_00800.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_01200.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_02400.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_04800.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_08000.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_12000.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "final.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        }
      ]
    },
    "manual-pal": {
      "checks": [
        "original three PNG layers in actual TOM output",
        "HUD.js speed trapezoid and shield rectangle",
        "native speed/shield digits",
        "recent live game state"
      ],
      "captures": [
        {
          "capture": "frame_00180.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00280.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00380.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00480.png",
          "speed": 21,
          "shield": 100,
          "pixels": 2527
        },
        {
          "capture": "frame_00580.png",
          "speed": 0,
          "shield": 97,
          "pixels": 1735
        },
        {
          "capture": "frame_00800.png",
          "speed": 0,
          "shield": 0,
          "pixels": 1538
        },
        {
          "capture": "frame_01200.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "final.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        }
      ]
    },
    "manual-pal-direct": {
      "checks": [
        "original three PNG layers in actual TOM output",
        "HUD.js speed trapezoid and shield rectangle",
        "native speed/shield digits",
        "recent live game state"
      ],
      "captures": [
        {
          "capture": "frame_00180.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00280.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00380.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00480.png",
          "speed": 24,
          "shield": 100,
          "pixels": 2652
        },
        {
          "capture": "frame_00580.png",
          "speed": 0,
          "shield": 97,
          "pixels": 1735
        },
        {
          "capture": "frame_00800.png",
          "speed": 0,
          "shield": 0,
          "pixels": 1538
        },
        {
          "capture": "frame_01200.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "final.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        }
      ]
    },
    "race-pal": {
      "checks": [
        "original three PNG layers in actual TOM output",
        "HUD.js speed trapezoid and shield rectangle",
        "native speed/shield digits",
        "recent live game state"
      ],
      "captures": [
        {
          "capture": "frame_00180.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00280.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00380.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00480.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_00580.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_00800.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_01200.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_02400.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_04800.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_08000.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_12000.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "final.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        }
      ]
    },
    "bank-ntsc": {
      "checks": [
        "original three PNG layers in actual TOM output",
        "HUD.js speed trapezoid and shield rectangle",
        "native speed/shield digits",
        "recent live game state"
      ],
      "captures": [
        {
          "capture": "frame_00180.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00280.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00380.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00480.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00580.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00632.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00752.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00800.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00872.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_01052.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "final.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        }
      ]
    },
    "camera-speed-ntsc": {
      "checks": [
        "original three PNG layers in actual TOM output",
        "HUD.js speed trapezoid and shield rectangle",
        "native speed/shield digits",
        "recent live game state"
      ],
      "captures": [
        {
          "capture": "frame_00180.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00280.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00380.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00480.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00580.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00582.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00584.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00586.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00588.png",
          "speed": 4,
          "shield": 100,
          "pixels": 1867
        },
        {
          "capture": "frame_00590.png",
          "speed": 4,
          "shield": 100,
          "pixels": 1867
        },
        {
          "capture": "frame_00592.png",
          "speed": 8,
          "shield": 100,
          "pixels": 2024
        },
        {
          "capture": "frame_00594.png",
          "speed": 8,
          "shield": 100,
          "pixels": 2024
        },
        {
          "capture": "frame_00596.png",
          "speed": 12,
          "shield": 100,
          "pixels": 2181
        },
        {
          "capture": "frame_00598.png",
          "speed": 12,
          "shield": 100,
          "pixels": 2181
        },
        {
          "capture": "frame_00600.png",
          "speed": 16,
          "shield": 100,
          "pixels": 2335
        },
        {
          "capture": "frame_00602.png",
          "speed": 16,
          "shield": 100,
          "pixels": 2335
        },
        {
          "capture": "frame_00604.png",
          "speed": 20,
          "shield": 100,
          "pixels": 2492
        },
        {
          "capture": "frame_00606.png",
          "speed": 20,
          "shield": 100,
          "pixels": 2492
        },
        {
          "capture": "frame_00608.png",
          "speed": 24,
          "shield": 100,
          "pixels": 2652
        },
        {
          "capture": "frame_00610.png",
          "speed": 24,
          "shield": 100,
          "pixels": 2652
        },
        {
          "capture": "frame_00636.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_00652.png",
          "speed": 10,
          "shield": 100,
          "pixels": 2105
        },
        {
          "capture": "frame_00720.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00800.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "final.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        }
      ]
    },
    "bank-pal": {
      "checks": [
        "original three PNG layers in actual TOM output",
        "HUD.js speed trapezoid and shield rectangle",
        "native speed/shield digits",
        "recent live game state"
      ],
      "captures": [
        {
          "capture": "frame_00180.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00280.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00380.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00480.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00542.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00580.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00642.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00742.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00800.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00892.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "final.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        }
      ]
    },
    "camera-speed-pal": {
      "checks": [
        "original three PNG layers in actual TOM output",
        "HUD.js speed trapezoid and shield rectangle",
        "native speed/shield digits",
        "recent live game state"
      ],
      "captures": [
        {
          "capture": "frame_00180.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00280.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00380.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00480.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00500.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00502.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00504.png",
          "speed": 3,
          "shield": 100,
          "pixels": 1832
        },
        {
          "capture": "frame_00506.png",
          "speed": 3,
          "shield": 100,
          "pixels": 1832
        },
        {
          "capture": "frame_00508.png",
          "speed": 6,
          "shield": 100,
          "pixels": 1949
        },
        {
          "capture": "frame_00510.png",
          "speed": 9,
          "shield": 100,
          "pixels": 2065
        },
        {
          "capture": "frame_00512.png",
          "speed": 9,
          "shield": 100,
          "pixels": 2065
        },
        {
          "capture": "frame_00514.png",
          "speed": 12,
          "shield": 100,
          "pixels": 2181
        },
        {
          "capture": "frame_00516.png",
          "speed": 15,
          "shield": 100,
          "pixels": 2294
        },
        {
          "capture": "frame_00518.png",
          "speed": 15,
          "shield": 100,
          "pixels": 2294
        },
        {
          "capture": "frame_00520.png",
          "speed": 18,
          "shield": 100,
          "pixels": 2411
        },
        {
          "capture": "frame_00522.png",
          "speed": 21,
          "shield": 100,
          "pixels": 2527
        },
        {
          "capture": "frame_00524.png",
          "speed": 21,
          "shield": 100,
          "pixels": 2527
        },
        {
          "capture": "frame_00526.png",
          "speed": 24,
          "shield": 100,
          "pixels": 2652
        },
        {
          "capture": "frame_00528.png",
          "speed": 27,
          "shield": 100,
          "pixels": 2765
        },
        {
          "capture": "frame_00530.png",
          "speed": 27,
          "shield": 100,
          "pixels": 2765
        },
        {
          "capture": "frame_00546.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_00562.png",
          "speed": 1,
          "shield": 100,
          "pixels": 1751
        },
        {
          "capture": "frame_00580.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00620.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "final.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        }
      ]
    },
    "countdown-pause-ntsc": {
      "checks": [
        "original three PNG layers in actual TOM output",
        "HUD.js speed trapezoid and shield rectangle",
        "native speed/shield digits",
        "recent live game state"
      ],
      "captures": [
        {
          "capture": "frame_00180.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00280.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00380.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00480.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00580.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00800.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "final.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        }
      ]
    },
    "countdown-pause-pal": {
      "checks": [
        "original three PNG layers in actual TOM output",
        "HUD.js speed trapezoid and shield rectangle",
        "native speed/shield digits",
        "recent live game state"
      ],
      "captures": [
        {
          "capture": "frame_00180.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00280.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00380.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00480.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00580.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00800.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "final.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        }
      ]
    },
    "cold-boot-seed-7": {
      "checks": [
        "original three PNG layers in actual TOM output",
        "HUD.js speed trapezoid and shield rectangle",
        "native speed/shield digits",
        "recent live game state"
      ],
      "captures": [
        {
          "capture": "frame_00180.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00280.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00380.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00480.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00580.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_00800.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "final.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        }
      ]
    },
    "cold-boot-seed-42": {
      "checks": [
        "original three PNG layers in actual TOM output",
        "HUD.js speed trapezoid and shield rectangle",
        "native speed/shield digits",
        "recent live game state"
      ],
      "captures": [
        {
          "capture": "frame_00180.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00280.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00380.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00480.png",
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00580.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_00800.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "final.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        }
      ]
    }
  },
  "status": "PASS"
}
```

## Desktop

```json
{
  "status": "PASS",
  "rom_sha256": "bfe5591fa30c95baa290f2591253d1ff47e12639a92b37d7bc9980d8456f1faa",
  "emulator_binary_sha256": "9ce9b17eaf33382e3aafce8841f3dc44c5547a140733baf8499254ad21488f86",
  "emulator_version": "Virtual Jaguar v2.1.3 (Final)",
  "cases": {
    "default-ntsc": {
      "status": "PASS",
      "rom_sha256": "bfe5591fa30c95baa290f2591253d1ff47e12639a92b37d7bc9980d8456f1faa",
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
      "emulator_exit_code": -9,
      "elapsed_seconds": 47.7
    },
    "no-bios-ntsc": {
      "status": "PASS",
      "rom_sha256": "bfe5591fa30c95baa290f2591253d1ff47e12639a92b37d7bc9980d8456f1faa",
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
      "emulator_exit_code": -9,
      "elapsed_seconds": 46.93
    },
    "bios-ntsc": {
      "status": "PASS",
      "rom_sha256": "bfe5591fa30c95baa290f2591253d1ff47e12639a92b37d7bc9980d8456f1faa",
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
      "emulator_exit_code": -9,
      "elapsed_seconds": 48.32
    },
    "no-bios-pal": {
      "status": "PASS",
      "rom_sha256": "bfe5591fa30c95baa290f2591253d1ff47e12639a92b37d7bc9980d8456f1faa",
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
      "emulator_exit_code": -9,
      "elapsed_seconds": 45.61
    },
    "bios-pal": {
      "status": "PASS",
      "rom_sha256": "bfe5591fa30c95baa290f2591253d1ff47e12639a92b37d7bc9980d8456f1faa",
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
      "emulator_exit_code": -9,
      "elapsed_seconds": 47.03
    },
    "negative-old-entry": {
      "status": "EXPECTED_FAILURE",
      "detected": "emulator exited before presenting video"
    },
    "negative-frozen-window": {
      "status": "EXPECTED_FAILURE",
      "detected": "world frozen for 3 seconds during throttle"
    }
  }
}
```

## HUD

```json
{
  "status": "PASS",
  "rom_sha256": "bfe5591fa30c95baa290f2591253d1ff47e12639a92b37d7bc9980d8456f1faa",
  "cases": {
    "ntsc": {
      "checks": [
        "throttle/collision speed levels",
        "collision shield loss",
        "empty shield on destruction",
        "full shield after reset",
        "actual source-art pixel equality"
      ],
      "speeds_seen": [
        0,
        4,
        8,
        16,
        28
      ],
      "shields_seen": [
        0,
        97,
        100
      ],
      "fields": 900,
      "bitmap_hud": {
        "checks": [
          "original three PNG layers in actual TOM output",
          "HUD.js speed trapezoid and shield rectangle",
          "native speed/shield digits",
          "recent live game state"
        ],
        "captures": [
          {
            "capture": "frame_00180.png",
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          },
          {
            "capture": "frame_00280.png",
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          },
          {
            "capture": "frame_00380.png",
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          },
          {
            "capture": "frame_00480.png",
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          },
          {
            "capture": "frame_00526.png",
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          },
          {
            "capture": "frame_00530.png",
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          },
          {
            "capture": "frame_00534.png",
            "speed": 4,
            "shield": 100,
            "pixels": 1867
          },
          {
            "capture": "frame_00538.png",
            "speed": 8,
            "shield": 100,
            "pixels": 2024
          },
          {
            "capture": "frame_00546.png",
            "speed": 16,
            "shield": 100,
            "pixels": 2335
          },
          {
            "capture": "frame_00580.png",
            "speed": 28,
            "shield": 100,
            "pixels": 2793
          },
          {
            "capture": "frame_00614.png",
            "speed": 28,
            "shield": 100,
            "pixels": 2793
          },
          {
            "capture": "frame_00632.png",
            "speed": 28,
            "shield": 100,
            "pixels": 2793
          },
          {
            "capture": "frame_00652.png",
            "speed": 0,
            "shield": 97,
            "pixels": 1735
          },
          {
            "capture": "frame_00672.png",
            "speed": 0,
            "shield": 97,
            "pixels": 1735
          },
          {
            "capture": "frame_00692.png",
            "speed": 0,
            "shield": 97,
            "pixels": 1735
          },
          {
            "capture": "frame_00712.png",
            "speed": 0,
            "shield": 97,
            "pixels": 1735
          },
          {
            "capture": "frame_00732.png",
            "speed": 0,
            "shield": 0,
            "pixels": 1538
          },
          {
            "capture": "frame_00752.png",
            "speed": 0,
            "shield": 0,
            "pixels": 1538
          },
          {
            "capture": "frame_00772.png",
            "speed": 0,
            "shield": 0,
            "pixels": 1538
          },
          {
            "capture": "frame_00800.png",
            "speed": 0,
            "shield": 0,
            "pixels": 1538
          },
          {
            "capture": "frame_00820.png",
            "speed": 0,
            "shield": 0,
            "pixels": 1538
          },
          {
            "capture": "frame_00850.png",
            "speed": 0,
            "shield": 0,
            "pixels": 1538
          },
          {
            "capture": "frame_00880.png",
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          },
          {
            "capture": "final.png",
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          }
        ]
      }
    },
    "pal": {
      "checks": [
        "throttle/collision speed levels",
        "collision shield loss",
        "empty shield on destruction",
        "full shield after reset",
        "actual source-art pixel equality"
      ],
      "speeds_seen": [
        0,
        3,
        6,
        12,
        18,
        24,
        28
      ],
      "shields_seen": [
        0,
        97,
        100
      ],
      "fields": 830,
      "bitmap_hud": {
        "checks": [
          "original three PNG layers in actual TOM output",
          "HUD.js speed trapezoid and shield rectangle",
          "native speed/shield digits",
          "recent live game state"
        ],
        "captures": [
          {
            "capture": "frame_00180.png",
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          },
          {
            "capture": "frame_00280.png",
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          },
          {
            "capture": "frame_00380.png",
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          },
          {
            "capture": "frame_00456.png",
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          },
          {
            "capture": "frame_00460.png",
            "speed": 3,
            "shield": 100,
            "pixels": 1832
          },
          {
            "capture": "frame_00464.png",
            "speed": 6,
            "shield": 100,
            "pixels": 1949
          },
          {
            "capture": "frame_00468.png",
            "speed": 12,
            "shield": 100,
            "pixels": 2181
          },
          {
            "capture": "frame_00476.png",
            "speed": 18,
            "shield": 100,
            "pixels": 2411
          },
          {
            "capture": "frame_00480.png",
            "speed": 24,
            "shield": 100,
            "pixels": 2652
          },
          {
            "capture": "frame_00510.png",
            "speed": 28,
            "shield": 100,
            "pixels": 2793
          },
          {
            "capture": "frame_00544.png",
            "speed": 28,
            "shield": 100,
            "pixels": 2793
          },
          {
            "capture": "frame_00562.png",
            "speed": 28,
            "shield": 100,
            "pixels": 2793
          },
          {
            "capture": "frame_00580.png",
            "speed": 0,
            "shield": 97,
            "pixels": 1735
          },
          {
            "capture": "frame_00582.png",
            "speed": 0,
            "shield": 97,
            "pixels": 1735
          },
          {
            "capture": "frame_00602.png",
            "speed": 0,
            "shield": 97,
            "pixels": 1735
          },
          {
            "capture": "frame_00622.png",
            "speed": 0,
            "shield": 97,
            "pixels": 1735
          },
          {
            "capture": "frame_00642.png",
            "speed": 0,
            "shield": 0,
            "pixels": 1538
          },
          {
            "capture": "frame_00662.png",
            "speed": 0,
            "shield": 0,
            "pixels": 1538
          },
          {
            "capture": "frame_00682.png",
            "speed": 0,
            "shield": 0,
            "pixels": 1538
          },
          {
            "capture": "frame_00702.png",
            "speed": 0,
            "shield": 0,
            "pixels": 1538
          },
          {
            "capture": "frame_00750.png",
            "speed": 0,
            "shield": 0,
            "pixels": 1538
          },
          {
            "capture": "frame_00780.png",
            "speed": 0,
            "shield": 0,
            "pixels": 1538
          },
          {
            "capture": "frame_00800.png",
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          },
          {
            "capture": "frame_00810.png",
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          },
          {
            "capture": "final.png",
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          }
        ]
      }
    }
  }
}
```

## Front end / replay / saves

```json
{
  "rom_sha256": "bfe5591fa30c95baa290f2591253d1ff47e12639a92b37d7bc9980d8456f1faa",
  "status": "PASS",
  "cases": {
    "menu-ntsc": {
      "checks": [
        "controller navigation",
        "controls/records/credits",
        "Option return",
        "real source font pixels",
        "Start enters countdown",
        "no unsolicited saves"
      ],
      "source_font_pixels": 1586
    },
    "replay-ntsc": {
      "samples": 88,
      "interpolated_commits": 137,
      "fractional_commits": 73,
      "record_ticks": 326,
      "checks": [
        "real run samples",
        "time interpolation",
        "mesh positions and camera",
        "wrapped heading",
        "pause/resume",
        "stable end",
        "Option exit",
        "no replay score writes"
      ],
      "recording_input": "manual throttle and steering",
      "recorded_pitch_pairs_verified": 88
    },
    "menu-pal": {
      "checks": [
        "controller navigation",
        "controls/records/credits",
        "Option return",
        "real source font pixels",
        "Start enters countdown",
        "no unsolicited saves"
      ],
      "source_font_pixels": 1586
    },
    "replay-pal": {
      "samples": 121,
      "interpolated_commits": 147,
      "fractional_commits": 92,
      "record_ticks": 396,
      "checks": [
        "real run samples",
        "time interpolation",
        "mesh positions and camera",
        "wrapped heading",
        "pause/resume",
        "stable end",
        "Option exit",
        "no replay score writes"
      ],
      "recording_input": "autopilot",
      "recorded_pitch_pairs_verified": 121
    },
    "save-ntsc": {
      "checks": [
        "real full-race serial EEPROM write",
        "nine writes only on improvement",
        "readback verified",
        "new process cold-load",
        "PAL/NTSC normalized milliseconds",
        "manual/assisted separation",
        "visible original-font saved time"
      ],
      "record": {
        "generation": 1,
        "total_ms": 221633,
        "lap_ms": 73600,
        "slot": 16
      },
      "eeprom_sha256": "fd84697b1a224a578ceceedf6262f4d6e6666b7c3d08eed53261c69b1cb28b20"
    },
    "save-pal": {
      "checks": [
        "real full-race serial EEPROM write",
        "nine writes only on improvement",
        "readback verified",
        "new process cold-load",
        "PAL/NTSC normalized milliseconds",
        "manual/assisted separation",
        "visible original-font saved time"
      ],
      "record": {
        "generation": 1,
        "total_ms": 232080,
        "lap_ms": 77120,
        "slot": 16
      },
      "eeprom_sha256": "02d23b6b60ed1cb3e4ebabd3cd60f25fc6e098679fcf5db81f1f8ab30b3405d9"
    },
    "journal-torn": {
      "checks": [
        "EEPROM boot recovery",
        "bounded boot/no freeze",
        "no repair writes"
      ],
      "fixture": "torn",
      "loaded_total_ms": 221633,
      "generation": 1
    },
    "journal-checksum": {
      "checks": [
        "EEPROM boot recovery",
        "bounded boot/no freeze",
        "no repair writes"
      ],
      "fixture": "checksum",
      "loaded_total_ms": 221633,
      "generation": 1
    },
    "journal-wrap": {
      "checks": [
        "EEPROM boot recovery",
        "bounded boot/no freeze",
        "no repair writes"
      ],
      "fixture": "wrap",
      "loaded_total_ms": 221633,
      "generation": 0
    },
    "journal-invalid": {
      "checks": [
        "EEPROM boot recovery",
        "bounded boot/no freeze",
        "no repair writes"
      ],
      "fixture": "invalid",
      "loaded_total_ms": 0,
      "generation": 0
    }
  }
}
```

## Dynamics / camera / effects

```json
{
  "status": "PASS",
  "rom_sha256": "bfe5591fa30c95baa290f2591253d1ff47e12639a92b37d7bc9980d8456f1faa",
  "cases": {
    "dynamics-drive-ntsc": {
      "actual_vertices": 475,
      "pitched_vertices": 350,
      "hover_updates": 73,
      "drifting_updates": 6,
      "repulsion_updates": 64,
      "fall_updates": 30,
      "particle_integrations": 1058,
      "observed_spawns": 90,
      "drawn_frames": 137,
      "maximum_pool": 16,
      "source_sprite_matching_pixels": [
        80,
        4863,
        9
      ],
      "exact_glow_pixels": 11,
      "checks": [
        "airbrake lateral force",
        "contact recoil",
        "bilinear hover",
        "active-time fall/destruction",
        "real ship/camera vertex and projection",
        "original sprite pixels",
        "bounded world-space spark/cloud emitters",
        "lifetime integration",
        "particle pause"
      ],
      "fall_integration_updates": 30,
      "paused_fall_updates": 0,
      "terminal_fall_fields": 90
    },
    "dynamics-route-ntsc": {
      "actual_vertices": 802,
      "pitched_vertices": 677,
      "hover_updates": 677,
      "drifting_updates": 0,
      "repulsion_updates": 0,
      "fall_updates": 0,
      "checks": [
        "source-map slopes",
        "actual pitched GPU mesh and look-at camera",
        "bilinear hover over varied track heights",
        "bounded PAL/NTSC response"
      ]
    },
    "dynamics-drive-pal": {
      "actual_vertices": 484,
      "pitched_vertices": 383,
      "hover_updates": 61,
      "drifting_updates": 6,
      "repulsion_updates": 40,
      "fall_updates": 25,
      "particle_integrations": 678,
      "observed_spawns": 42,
      "drawn_frames": 113,
      "maximum_pool": 16,
      "source_sprite_matching_pixels": [
        47,
        5041,
        9
      ],
      "exact_glow_pixels": 11,
      "checks": [
        "airbrake lateral force",
        "contact recoil",
        "bilinear hover",
        "active-time fall/destruction",
        "real ship/camera vertex and projection",
        "original sprite pixels",
        "bounded world-space spark/cloud emitters",
        "lifetime integration",
        "particle pause"
      ],
      "fall_integration_updates": 25,
      "paused_fall_updates": 0,
      "terminal_fall_fields": 75
    },
    "dynamics-route-pal": {
      "actual_vertices": 929,
      "pitched_vertices": 828,
      "hover_updates": 827,
      "drifting_updates": 0,
      "repulsion_updates": 0,
      "fall_updates": 0,
      "checks": [
        "source-map slopes",
        "actual pitched GPU mesh and look-at camera",
        "bilinear hover over varied track heights",
        "bounded PAL/NTSC response"
      ]
    }
  }
}
```

This does not complete every remaining port system. Physical hardware and remote CI remain untested.
