# Native particles, original stereo and retained systems: executed results

ROM SHA-256: `fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8`

Eight suites: **PASS**. 99 unit tests: **PASS**.

## Core

```json
{
  "rom_sha256": "fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8",
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
      "updates": 49,
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
      "updates": 49,
      "audio_samples": 267667
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
        "height_filtered_updates": 2892,
        "left_bank_seen": true,
        "right_bank_seen": true
      },
      "fields": 15222,
      "updates": 4026,
      "race_ticks": 14520,
      "lap_ticks": [
        4872,
        4824,
        4824
      ],
      "audio_samples": 2025213
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
      "audio_samples": 299661
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
        "height_filtered_updates": 2880,
        "left_bank_seen": true,
        "right_bank_seen": true
      },
      "fields": 13162,
      "updates": 4054,
      "race_ticks": 12531,
      "lap_ticks": [
        4205,
        4163,
        4163
      ],
      "audio_samples": 2101622
    },
    "bank-ntsc": {
      "verified_updates": 135,
      "height_filtered_updates": 0,
      "left_bank_seen": true,
      "right_bank_seen": true,
      "half_second_left_roll_q8": -46755,
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
      "verified_updates": 75,
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
      "verified_updates": 144,
      "height_filtered_updates": 0,
      "left_bank_seen": true,
      "right_bank_seen": true,
      "half_second_left_roll_q8": -47074,
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
      "verified_updates": 68,
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
          "shield": 78,
          "pixels": 1706
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
          "shield": 78,
          "pixels": 1706
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
          "speed": 24,
          "shield": 100,
          "pixels": 2652
        },
        {
          "capture": "frame_00580.png",
          "speed": 0,
          "shield": 86,
          "pixels": 1718
        },
        {
          "capture": "frame_00800.png",
          "speed": 0,
          "shield": 56,
          "pixels": 1660
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
          "speed": 21,
          "shield": 100,
          "pixels": 2527
        },
        {
          "capture": "frame_00580.png",
          "speed": 0,
          "shield": 92,
          "pixels": 1733
        },
        {
          "capture": "frame_00800.png",
          "speed": 0,
          "shield": 56,
          "pixels": 1660
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
          "speed": 4,
          "shield": 100,
          "pixels": 1867
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
          "speed": 6,
          "shield": 100,
          "pixels": 1949
        },
        {
          "capture": "frame_00512.png",
          "speed": 10,
          "shield": 100,
          "pixels": 2105
        },
        {
          "capture": "frame_00514.png",
          "speed": 13,
          "shield": 100,
          "pixels": 2222
        },
        {
          "capture": "frame_00516.png",
          "speed": 13,
          "shield": 100,
          "pixels": 2222
        },
        {
          "capture": "frame_00518.png",
          "speed": 16,
          "shield": 100,
          "pixels": 2335
        },
        {
          "capture": "frame_00520.png",
          "speed": 16,
          "shield": 100,
          "pixels": 2335
        },
        {
          "capture": "frame_00522.png",
          "speed": 19,
          "shield": 100,
          "pixels": 2454
        },
        {
          "capture": "frame_00524.png",
          "speed": 19,
          "shield": 100,
          "pixels": 2454
        },
        {
          "capture": "frame_00526.png",
          "speed": 23,
          "shield": 100,
          "pixels": 2609
        },
        {
          "capture": "frame_00528.png",
          "speed": 23,
          "shield": 100,
          "pixels": 2609
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
          "speed": 10,
          "shield": 100,
          "pixels": 2105
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
  "rom_sha256": "fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8",
  "emulator_binary_sha256": "9ce9b17eaf33382e3aafce8841f3dc44c5547a140733baf8499254ad21488f86",
  "emulator_version": "Virtual Jaguar v2.1.3 (Final)",
  "cases": {
    "default-ntsc": {
      "status": "PASS",
      "rom_sha256": "fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8",
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
      "elapsed_seconds": 54.84
    },
    "no-bios-ntsc": {
      "status": "PASS",
      "rom_sha256": "fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8",
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
      "elapsed_seconds": 53.7
    },
    "bios-ntsc": {
      "status": "PASS",
      "rom_sha256": "fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8",
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
      "elapsed_seconds": 53.22
    },
    "no-bios-pal": {
      "status": "PASS",
      "rom_sha256": "fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8",
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
      "elapsed_seconds": 48.45
    },
    "bios-pal": {
      "status": "PASS",
      "rom_sha256": "fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8",
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
      "elapsed_seconds": 45.83
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
  "rom_sha256": "fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8",
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
        90,
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
            "shield": 90,
            "pixels": 1727
          },
          {
            "capture": "frame_00672.png",
            "speed": 0,
            "shield": 90,
            "pixels": 1727
          },
          {
            "capture": "frame_00692.png",
            "speed": 0,
            "shield": 90,
            "pixels": 1727
          },
          {
            "capture": "frame_00712.png",
            "speed": 0,
            "shield": 90,
            "pixels": 1727
          },
          {
            "capture": "frame_00732.png",
            "speed": 0,
            "shield": 90,
            "pixels": 1727
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
        21,
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
            "speed": 21,
            "shield": 100,
            "pixels": 2527
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
  "rom_sha256": "fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8",
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
      "recorded_pitch_pairs_verified": 64,
      "samples": 64,
      "interpolated_commits": 156,
      "fractional_commits": 19,
      "record_ticks": 231,
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
      "recording_input": "manual throttle and steering"
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
      "recorded_pitch_pairs_verified": 107,
      "samples": 107,
      "interpolated_commits": 140,
      "fractional_commits": 26,
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
      "recording_input": "autopilot"
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
        "total_ms": 242000,
        "lap_ms": 80400,
        "slot": 16
      },
      "eeprom_sha256": "e758a3b00ae6f4e61c351649e0a2eca72c72d028f1fa49f4f24ba2f339c705ae"
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
        "total_ms": 250620,
        "lap_ms": 83260,
        "slot": 16
      },
      "eeprom_sha256": "f66cd2cdfd6511bb561d4521d668274095a958d2b760d162ea379ad71a5cab94"
    },
    "journal-torn": {
      "checks": [
        "EEPROM boot recovery",
        "bounded boot/no freeze",
        "no repair writes"
      ],
      "fixture": "torn",
      "loaded_total_ms": 242000,
      "generation": 1
    },
    "journal-checksum": {
      "checks": [
        "EEPROM boot recovery",
        "bounded boot/no freeze",
        "no repair writes"
      ],
      "fixture": "checksum",
      "loaded_total_ms": 242000,
      "generation": 1
    },
    "journal-wrap": {
      "checks": [
        "EEPROM boot recovery",
        "bounded boot/no freeze",
        "no repair writes"
      ],
      "fixture": "wrap",
      "loaded_total_ms": 242000,
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
  "rom_sha256": "fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8",
  "cases": {
    "dynamics-drive-ntsc": {
      "actual_vertices": 335,
      "pitched_vertices": 242,
      "hover_updates": 38,
      "drifting_updates": 5,
      "repulsion_updates": 28,
      "fall_updates": 29,
      "fall_integration_updates": 29,
      "paused_fall_updates": 0,
      "terminal_fall_fields": 92,
      "particle_integrations": 544,
      "observed_spawns": 72,
      "drawn_frames": 85,
      "maximum_pool": 16,
      "rgb_composites_and_source_texels_checked": 1036,
      "source_sprite_kinds": [
        0,
        1,
        2
      ],
      "perspective_pixel_sizes": [
        8,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        32
      ],
      "actual_triangle_depth_checks": 987,
      "observed_depth_occlusions": 0,
      "exact_composed_framebuffer_captures": [
        "frame_00575.png",
        "frame_00580.png",
        "frame_00620.png",
        "frame_00650.png",
        "frame_00665.png",
        "frame_00770.png",
        "frame_00800.png",
        "frame_00830.png"
      ],
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
      ]
    },
    "dynamics-route-ntsc": {
      "actual_vertices": 703,
      "pitched_vertices": 610,
      "hover_updates": 609,
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
      "actual_vertices": 445,
      "pitched_vertices": 344,
      "hover_updates": 42,
      "drifting_updates": 6,
      "repulsion_updates": 25,
      "fall_updates": 24,
      "fall_integration_updates": 24,
      "paused_fall_updates": 0,
      "terminal_fall_fields": 75,
      "particle_integrations": 464,
      "observed_spawns": 54,
      "drawn_frames": 83,
      "maximum_pool": 16,
      "rgb_composites_and_source_texels_checked": 1112,
      "source_sprite_kinds": [
        0,
        1,
        2
      ],
      "perspective_pixel_sizes": [
        11,
        12,
        13,
        14,
        18,
        19,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        31,
        32
      ],
      "actual_triangle_depth_checks": 1057,
      "observed_depth_occlusions": 0,
      "exact_composed_framebuffer_captures": [
        "frame_00480.png",
        "frame_00550.png",
        "frame_00580.png",
        "frame_00595.png",
        "frame_00700.png",
        "frame_00730.png",
        "frame_00760.png",
        "frame_00800.png"
      ],
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
      ]
    },
    "dynamics-route-pal": {
      "actual_vertices": 866,
      "pitched_vertices": 765,
      "hover_updates": 765,
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

## Materials / sky / stereo

```json
{
  "status": "PASS",
  "rom_sha256": "fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8",
  "cases": {
    "ntsc": {
      "exact_original_music_adpcm_samples": 619,
      "music_stereo_content_samples": 0,
      "completed_dsp_samples_checked": 1146,
      "pan_range": [
        -52,
        52
      ],
      "actual_stereo_fields": 611,
      "material_banks": [
        0,
        7
      ],
      "sky_crop_rows": 12,
      "fields_with_scene_illumination": 622,
      "face_light_additions_checked": 296,
      "sky_pixel_captures": [
        {
          "capture": "frame_00180.png",
          "exact_pitch_and_yaw_sky_pixels": 5800
        },
        {
          "capture": "frame_00280.png",
          "exact_pitch_and_yaw_sky_pixels": 5800
        },
        {
          "capture": "frame_00380.png",
          "exact_pitch_and_yaw_sky_pixels": 5800
        },
        {
          "capture": "frame_00480.png",
          "exact_pitch_and_yaw_sky_pixels": 5800
        },
        {
          "capture": "frame_00550.png",
          "exact_pitch_and_yaw_sky_pixels": 4447
        },
        {
          "capture": "frame_00570.png",
          "exact_pitch_and_yaw_sky_pixels": 4921
        },
        {
          "capture": "frame_00580.png",
          "exact_pitch_and_yaw_sky_pixels": 6092
        },
        {
          "capture": "frame_00600.png",
          "exact_pitch_and_yaw_sky_pixels": 5854
        },
        {
          "capture": "frame_00620.png",
          "exact_pitch_and_yaw_sky_pixels": 1257
        },
        {
          "capture": "frame_00650.png",
          "exact_pitch_and_yaw_sky_pixels": 6158
        }
      ],
      "checks": [
        "actual interleaved stereo PCM",
        "left/right native spatial bus and centered music",
        "signed saturating DSP gain arithmetic",
        "runtime ROM atlas addresses",
        "real scene-face point-light addition",
        "exact camera-dependent sky framebuffer pixels including seam wrap"
      ]
    },
    "pal": {
      "exact_original_music_adpcm_samples": 610,
      "music_stereo_content_samples": 0,
      "completed_dsp_samples_checked": 1149,
      "pan_range": [
        -52,
        52
      ],
      "actual_stereo_fields": 645,
      "material_banks": [
        0,
        7
      ],
      "sky_crop_rows": 8,
      "fields_with_scene_illumination": 612,
      "face_light_additions_checked": 280,
      "sky_pixel_captures": [
        {
          "capture": "frame_00180.png",
          "exact_pitch_and_yaw_sky_pixels": 5800
        },
        {
          "capture": "frame_00280.png",
          "exact_pitch_and_yaw_sky_pixels": 5800
        },
        {
          "capture": "frame_00380.png",
          "exact_pitch_and_yaw_sky_pixels": 5800
        },
        {
          "capture": "frame_00480.png",
          "exact_pitch_and_yaw_sky_pixels": 4281
        },
        {
          "capture": "frame_00500.png",
          "exact_pitch_and_yaw_sky_pixels": 5266
        },
        {
          "capture": "frame_00510.png",
          "exact_pitch_and_yaw_sky_pixels": 5964
        },
        {
          "capture": "frame_00530.png",
          "exact_pitch_and_yaw_sky_pixels": 4620
        },
        {
          "capture": "frame_00550.png",
          "exact_pitch_and_yaw_sky_pixels": 4691
        },
        {
          "capture": "frame_00580.png",
          "exact_pitch_and_yaw_sky_pixels": 5822
        }
      ],
      "checks": [
        "actual interleaved stereo PCM",
        "left/right native spatial bus and centered music",
        "signed saturating DSP gain arithmetic",
        "runtime ROM atlas addresses",
        "real scene-face point-light addition",
        "exact camera-dependent sky framebuffer pixels including seam wrap"
      ]
    }
  }
}
```

## Dedicated fall / pause

```json
{
  "status": "PASS",
  "rom_sha256": "fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8",
  "cases": {
    "fall-pause-ntsc-direct": {
      "fall_integration_updates": 29,
      "paused_fall_updates": 37,
      "terminal_fall_fields": 92,
      "probe_first_fall_field": 885,
      "controller_pause_field": 897,
      "checks": [
        "controller-triggered unsupported fall",
        "exact PAL/NTSC displacement at capped dt",
        "pause freezes falling for >20 native updates",
        "1.5 active seconds to destruction"
      ]
    },
    "fall-pause-ntsc-bios": {
      "fall_integration_updates": 29,
      "paused_fall_updates": 37,
      "terminal_fall_fields": 92,
      "probe_first_fall_field": 885,
      "controller_pause_field": 897,
      "checks": [
        "controller-triggered unsupported fall",
        "exact PAL/NTSC displacement at capped dt",
        "pause freezes falling for >20 native updates",
        "1.5 active seconds to destruction"
      ]
    },
    "fall-pause-pal-direct": {
      "fall_integration_updates": 24,
      "paused_fall_updates": 49,
      "terminal_fall_fields": 75,
      "probe_first_fall_field": 746,
      "controller_pause_field": 758,
      "checks": [
        "controller-triggered unsupported fall",
        "exact PAL/NTSC displacement at capped dt",
        "pause freezes falling for >20 native updates",
        "1.5 active seconds to destruction"
      ]
    },
    "fall-pause-pal-bios": {
      "fall_integration_updates": 24,
      "paused_fall_updates": 49,
      "terminal_fall_fields": 76,
      "probe_first_fall_field": 623,
      "controller_pause_field": 635,
      "checks": [
        "controller-triggered unsupported fall",
        "exact PAL/NTSC displacement at capped dt",
        "pause freezes falling for >20 native updates",
        "1.5 active seconds to destruction"
      ]
    }
  }
}
```

## Original stereo / audio events

```json
{
  "status": "PASS",
  "rom_sha256": "fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8",
  "cases": {
    "ntsc": {
      "boost_episodes": [
        {
          "first_active_field": 730,
          "observed_active_fields": 20,
          "first_cartridge_cursor": "0xbea37d"
        },
        {
          "first_active_field": 1558,
          "observed_active_fields": 23,
          "first_cartridge_cursor": "0xbea37d"
        }
      ],
      "completed_zero_timer_stop_samples": [
        55,
        55
      ],
      "source_stereo_at_zero_pan_fields": 38,
      "native_stereo_gain_checks": 43,
      "checks": [
        "actual original-channel boost content at zero pan",
        "real DSP one-shot cursor progression",
        "Option timer-clear stops while stream active",
        "second controller race restarts source at first block",
        "unchanged black/frozen-video and source-HUD gates"
      ]
    },
    "pal": {
      "boost_episodes": [
        {
          "first_active_field": 632,
          "observed_active_fields": 20,
          "first_cartridge_cursor": "0xbea398"
        },
        {
          "first_active_field": 1363,
          "observed_active_fields": 20,
          "first_cartridge_cursor": "0xbea398"
        }
      ],
      "completed_zero_timer_stop_samples": [
        55,
        55
      ],
      "source_stereo_at_zero_pan_fields": 38,
      "native_stereo_gain_checks": 40,
      "checks": [
        "actual original-channel boost content at zero pan",
        "real DSP one-shot cursor progression",
        "Option timer-clear stops while stream active",
        "second controller race restarts source at first block",
        "unchanged black/frozen-video and source-HUD gates"
      ]
    }
  }
}
```

## Separate native GPU depth fixtures

```json
{
  "status": "PASS",
  "rom_sha256": "fc99ae03d093ec1483cf814d18f484bfa5adf154d42081d37a9350710c93e1a8",
  "diagnostic_rom_sha256": "5af0b5e735e53293c8a08da918758ba069771f87854cc1860a1b53c234093a34",
  "method": "Separate native-GPU fixture ROM, unchanged production fx_occluded assembly, read-only host observations. Not a gameplay trace.",
  "production_depth_source_sha256": "a6aa6b4514b6fb95fb9741efad1d64e4b2ed77bc5bdb25f783396437442a8ed6",
  "cases": [
    {
      "name": "front",
      "expected": 0,
      "actual": 0
    },
    {
      "name": "coplanar",
      "expected": 0,
      "actual": 0
    },
    {
      "name": "bias_boundary",
      "expected": 0,
      "actual": 0
    },
    {
      "name": "behind",
      "expected": 1,
      "actual": 1
    },
    {
      "name": "outside",
      "expected": 0,
      "actual": 0
    },
    {
      "name": "reverse_winding_behind",
      "expected": 1,
      "actual": 1
    },
    {
      "name": "near_plane_skipped",
      "expected": 0,
      "actual": 0
    },
    {
      "name": "ship_excluded",
      "expected": 0,
      "actual": 0
    },
    {
      "name": "booster_excluded",
      "expected": 0,
      "actual": 0
    },
    {
      "name": "degenerate_skipped",
      "expected": 0,
      "actual": 0
    },
    {
      "name": "varying_reciprocal_front",
      "expected": 0,
      "actual": 0
    },
    {
      "name": "varying_reciprocal_behind",
      "expected": 1,
      "actual": 1
    }
  ],
  "actual_occlusion_rejections": 3,
  "varying_vertex_triangle_z": 160,
  "gpu_overlay_end": "0xf03ce8"
}
```

This does not complete every remaining port system. Physical hardware and remote CI remain untested.
