# Expanded native visual/AV systems and retained gameplay: executed results

ROM SHA-256: `c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a`

Ten suites / 64 scenarios: **PASS**. 148 unit tests: **PASS**.

## Core

```json
{
  "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
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
      "audio_samples": 267534
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
        "height_filtered_updates": 2889,
        "left_bank_seen": true,
        "right_bank_seen": true
      },
      "fields": 15942,
      "updates": 4026,
      "race_ticks": 15240,
      "lap_ticks": [
        5115,
        5063,
        5062
      ],
      "audio_samples": 2121094
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
      "updates": 64,
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
      "updates": 64,
      "audio_samples": 299501
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
        "height_filtered_updates": 2865,
        "left_bank_seen": true,
        "right_bank_seen": true
      },
      "fields": 13801,
      "updates": 4047,
      "race_ticks": 13170,
      "lap_ticks": [
        4420,
        4375,
        4375
      ],
      "audio_samples": 2203746
    },
    "bank-ntsc": {
      "verified_updates": 135,
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
      "verified_updates": 74,
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
      "verified_updates": 129,
      "height_filtered_updates": 0,
      "left_bank_seen": true,
      "right_bank_seen": true,
      "half_second_left_roll_q8": -47075,
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
      "verified_updates": 62,
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
          "speed": 12,
          "shield": 90,
          "pixels": 2173
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
      ],
      "hud_off_captures": []
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
          "speed": 12,
          "shield": 90,
          "pixels": 2173
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
      ],
      "hud_off_captures": []
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
      ],
      "hud_off_captures": []
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
          "shield": 91,
          "pixels": 1727
        },
        {
          "capture": "frame_00800.png",
          "speed": 0,
          "shield": 61,
          "pixels": 1669
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
      ],
      "hud_off_captures": []
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
          "speed": 20,
          "shield": 100,
          "pixels": 2492
        },
        {
          "capture": "frame_00580.png",
          "speed": 0,
          "shield": 91,
          "pixels": 1727
        },
        {
          "capture": "frame_00800.png",
          "speed": 12,
          "shield": 73,
          "pixels": 2135
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
      ],
      "hud_off_captures": []
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
      ],
      "hud_off_captures": []
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
      ],
      "hud_off_captures": []
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
      ],
      "hud_off_captures": []
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
      ],
      "hud_off_captures": []
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
          "speed": 0,
          "shield": 100,
          "pixels": 1735
        },
        {
          "capture": "frame_00506.png",
          "speed": 4,
          "shield": 100,
          "pixels": 1867
        },
        {
          "capture": "frame_00508.png",
          "speed": 4,
          "shield": 100,
          "pixels": 1867
        },
        {
          "capture": "frame_00510.png",
          "speed": 8,
          "shield": 100,
          "pixels": 2024
        },
        {
          "capture": "frame_00512.png",
          "speed": 8,
          "shield": 100,
          "pixels": 2024
        },
        {
          "capture": "frame_00514.png",
          "speed": 12,
          "shield": 100,
          "pixels": 2181
        },
        {
          "capture": "frame_00516.png",
          "speed": 12,
          "shield": 100,
          "pixels": 2181
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
          "speed": 20,
          "shield": 100,
          "pixels": 2492
        },
        {
          "capture": "frame_00524.png",
          "speed": 20,
          "shield": 100,
          "pixels": 2492
        },
        {
          "capture": "frame_00526.png",
          "speed": 24,
          "shield": 100,
          "pixels": 2652
        },
        {
          "capture": "frame_00528.png",
          "speed": 24,
          "shield": 100,
          "pixels": 2652
        },
        {
          "capture": "frame_00530.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_00546.png",
          "speed": 28,
          "shield": 100,
          "pixels": 2793
        },
        {
          "capture": "frame_00562.png",
          "speed": 4,
          "shield": 100,
          "pixels": 1867
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
      ],
      "hud_off_captures": []
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
      ],
      "hud_off_captures": []
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
      ],
      "hud_off_captures": []
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
      ],
      "hud_off_captures": []
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
      ],
      "hud_off_captures": []
    }
  },
  "status": "PASS"
}
```

## Desktop

```json
{
  "status": "PASS",
  "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
  "emulator_binary_sha256": "9ce9b17eaf33382e3aafce8841f3dc44c5547a140733baf8499254ad21488f86",
  "emulator_version": "Virtual Jaguar v2.1.3 (Final)",
  "cases": {
    "default-ntsc": {
      "status": "PASS",
      "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
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
      "elapsed_seconds": 49.27
    },
    "no-bios-ntsc": {
      "status": "PASS",
      "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
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
      "elapsed_seconds": 45.99
    },
    "bios-ntsc": {
      "status": "PASS",
      "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
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
      "elapsed_seconds": 46.43
    },
    "no-bios-pal": {
      "status": "PASS",
      "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
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
      "elapsed_seconds": 45.76
    },
    "bios-pal": {
      "status": "PASS",
      "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
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
      "elapsed_seconds": 46.39
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
  "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
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
        96,
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
            "shield": 96,
            "pixels": 1735
          },
          {
            "capture": "frame_00672.png",
            "speed": 0,
            "shield": 96,
            "pixels": 1735
          },
          {
            "capture": "frame_00692.png",
            "speed": 0,
            "shield": 96,
            "pixels": 1735
          },
          {
            "capture": "frame_00712.png",
            "speed": 0,
            "shield": 96,
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
        ],
        "hud_off_captures": []
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
        4,
        8,
        16,
        20,
        28
      ],
      "shields_seen": [
        0,
        91,
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
            "speed": 0,
            "shield": 100,
            "pixels": 1735
          },
          {
            "capture": "frame_00464.png",
            "speed": 4,
            "shield": 100,
            "pixels": 1867
          },
          {
            "capture": "frame_00468.png",
            "speed": 8,
            "shield": 100,
            "pixels": 2024
          },
          {
            "capture": "frame_00476.png",
            "speed": 16,
            "shield": 100,
            "pixels": 2335
          },
          {
            "capture": "frame_00480.png",
            "speed": 20,
            "shield": 100,
            "pixels": 2492
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
            "shield": 91,
            "pixels": 1727
          },
          {
            "capture": "frame_00582.png",
            "speed": 0,
            "shield": 91,
            "pixels": 1727
          },
          {
            "capture": "frame_00602.png",
            "speed": 0,
            "shield": 91,
            "pixels": 1727
          },
          {
            "capture": "frame_00622.png",
            "speed": 0,
            "shield": 91,
            "pixels": 1727
          },
          {
            "capture": "frame_00642.png",
            "speed": 0,
            "shield": 91,
            "pixels": 1727
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
        ],
        "hud_off_captures": []
      }
    }
  }
}
```

## Front end / replay / saves

```json
{
  "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
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
      "recorded_pitch_pairs_verified": 59,
      "samples": 59,
      "interpolated_commits": 149,
      "fractional_commits": 68,
      "record_ticks": 256,
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
      "recorded_pitch_pairs_verified": 103,
      "samples": 103,
      "interpolated_commits": 137,
      "fractional_commits": 21,
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
        "total_ms": 254000,
        "lap_ms": 84366,
        "slot": 16
      },
      "eeprom_sha256": "c8aec4cb58ba28b37d6dd15a29dbe83126d9f635471b8221899387fb191a667a"
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
        "total_ms": 263400,
        "lap_ms": 87500,
        "slot": 16
      },
      "eeprom_sha256": "3412c3b9ff5b6541b410352e9fdb801814a55b4110dc9cb2fa056db717cf35c7"
    },
    "journal-torn": {
      "checks": [
        "EEPROM boot recovery",
        "bounded boot/no freeze",
        "no repair writes"
      ],
      "fixture": "torn",
      "loaded_total_ms": 254000,
      "generation": 1
    },
    "journal-checksum": {
      "checks": [
        "EEPROM boot recovery",
        "bounded boot/no freeze",
        "no repair writes"
      ],
      "fixture": "checksum",
      "loaded_total_ms": 254000,
      "generation": 1
    },
    "journal-wrap": {
      "checks": [
        "EEPROM boot recovery",
        "bounded boot/no freeze",
        "no repair writes"
      ],
      "fixture": "wrap",
      "loaded_total_ms": 254000,
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
  "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
  "cases": {
    "dynamics-drive-ntsc": {
      "actual_vertices": 355,
      "pitched_vertices": 261,
      "hover_updates": 27,
      "drifting_updates": 8,
      "repulsion_updates": 3,
      "fall_updates": 22,
      "fall_integration_updates": 22,
      "paused_fall_updates": 11,
      "terminal_fall_fields": 92,
      "particle_integrations": 219,
      "observed_spawns": 30,
      "drawn_frames": 62,
      "maximum_pool": 16,
      "rgb_composites_and_source_texels_checked": 1073,
      "source_sprite_kinds": [
        0,
        1,
        2
      ],
      "perspective_pixel_sizes": [
        8,
        11,
        12,
        14,
        15,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        32
      ],
      "actual_triangle_depth_checks": 966,
      "observed_depth_occlusions": 0,
      "exact_composed_framebuffer_captures": [
        "frame_00575.png",
        "frame_00580.png",
        "frame_00620.png",
        "frame_00650.png",
        "frame_00665.png",
        "frame_00770.png",
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
    "dynamics-route-ntsc": {
      "actual_vertices": 684,
      "pitched_vertices": 590,
      "hover_updates": 589,
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
      "actual_vertices": 407,
      "pitched_vertices": 306,
      "hover_updates": 54,
      "drifting_updates": 5,
      "repulsion_updates": 42,
      "fall_updates": 23,
      "fall_integration_updates": 23,
      "paused_fall_updates": 0,
      "terminal_fall_fields": 75,
      "particle_integrations": 686,
      "observed_spawns": 195,
      "drawn_frames": 96,
      "maximum_pool": 16,
      "rgb_composites_and_source_texels_checked": 1101,
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
        17,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        30,
        31,
        32
      ],
      "actual_triangle_depth_checks": 1039,
      "observed_depth_occlusions": 1,
      "exact_composed_framebuffer_captures": [
        "frame_00480.png",
        "frame_00505.png",
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
      "actual_vertices": 813,
      "pitched_vertices": 712,
      "hover_updates": 711,
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
  "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
  "cases": {
    "ntsc": {
      "exact_original_music_adpcm_samples": 718,
      "music_stereo_content_samples": 0,
      "completed_dsp_samples_checked": 1148,
      "pan_range": [
        -52,
        52
      ],
      "actual_stereo_fields": 622,
      "material_banks": [
        0,
        7
      ],
      "sky_crop_rows": 11,
      "fields_with_scene_illumination": 721,
      "face_light_additions_checked": 380,
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
          "exact_pitch_and_yaw_sky_pixels": 4699
        },
        {
          "capture": "frame_00580.png",
          "exact_pitch_and_yaw_sky_pixels": 6179
        },
        {
          "capture": "frame_00600.png",
          "exact_pitch_and_yaw_sky_pixels": 5583
        },
        {
          "capture": "frame_00620.png",
          "exact_pitch_and_yaw_sky_pixels": 5330
        },
        {
          "capture": "frame_00650.png",
          "exact_pitch_and_yaw_sky_pixels": 6278
        },
        {
          "capture": "frame_00800.png",
          "exact_pitch_and_yaw_sky_pixels": 7680
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
      "exact_original_music_adpcm_samples": 567,
      "music_stereo_content_samples": 0,
      "completed_dsp_samples_checked": 1148,
      "pan_range": [
        -52,
        52
      ],
      "actual_stereo_fields": 597,
      "material_banks": [
        0,
        7
      ],
      "sky_crop_rows": 7,
      "fields_with_scene_illumination": 569,
      "face_light_additions_checked": 256,
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
          "exact_pitch_and_yaw_sky_pixels": 5201
        },
        {
          "capture": "frame_00510.png",
          "exact_pitch_and_yaw_sky_pixels": 5811
        },
        {
          "capture": "frame_00530.png",
          "exact_pitch_and_yaw_sky_pixels": 5959
        },
        {
          "capture": "frame_00550.png",
          "exact_pitch_and_yaw_sky_pixels": 4321
        },
        {
          "capture": "frame_00580.png",
          "exact_pitch_and_yaw_sky_pixels": 5661
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
  "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
  "cases": {
    "fall-pause-ntsc-direct": {
      "fall_integration_updates": 22,
      "paused_fall_updates": 29,
      "terminal_fall_fields": 93,
      "probe_controller_path": "left40",
      "probe_first_fall_field": 680,
      "controller_pause_field": 692,
      "checks": [
        "controller-triggered unsupported fall",
        "exact PAL/NTSC displacement at capped dt",
        "pause freezes falling for >20 native updates",
        "1.5 active seconds to destruction"
      ]
    },
    "fall-pause-ntsc-bios": {
      "fall_integration_updates": 21,
      "paused_fall_updates": 29,
      "terminal_fall_fields": 90,
      "probe_controller_path": "rightb25",
      "probe_first_fall_field": 657,
      "controller_pause_field": 669,
      "checks": [
        "controller-triggered unsupported fall",
        "exact PAL/NTSC displacement at capped dt",
        "pause freezes falling for >20 native updates",
        "1.5 active seconds to destruction"
      ]
    },
    "fall-pause-pal-direct": {
      "fall_integration_updates": 24,
      "paused_fall_updates": 36,
      "terminal_fall_fields": 77,
      "probe_controller_path": "left40",
      "probe_first_fall_field": 565,
      "controller_pause_field": 577,
      "checks": [
        "controller-triggered unsupported fall",
        "exact PAL/NTSC displacement at capped dt",
        "pause freezes falling for >20 native updates",
        "1.5 active seconds to destruction"
      ]
    },
    "fall-pause-pal-bios": {
      "fall_integration_updates": 24,
      "paused_fall_updates": 36,
      "terminal_fall_fields": 77,
      "probe_controller_path": "left40",
      "probe_first_fall_field": 563,
      "controller_pause_field": 575,
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
  "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
  "cases": {
    "ntsc": {
      "probe_first_pad_field": 740,
      "boost_episodes": [
        {
          "first_active_field": 740,
          "observed_active_fields": 20,
          "first_cartridge_cursor": "0xbea37d"
        },
        {
          "first_active_field": 1577,
          "observed_active_fields": 24,
          "first_cartridge_cursor": "0xbea37d"
        }
      ],
      "completed_zero_timer_stop_samples": [
        55,
        55
      ],
      "source_stereo_at_zero_pan_fields": 42,
      "native_stereo_gain_checks": 44,
      "checks": [
        "actual original-channel boost content at zero pan",
        "real DSP one-shot cursor progression",
        "Option timer-clear stops while stream active",
        "second controller race restarts source at first block",
        "unchanged black/frozen-video and source-HUD gates"
      ]
    },
    "pal": {
      "probe_first_pad_field": 649,
      "boost_episodes": [
        {
          "first_active_field": 649,
          "observed_active_fields": 20,
          "first_cartridge_cursor": "0xbea397"
        },
        {
          "first_active_field": 1396,
          "observed_active_fields": 23,
          "first_cartridge_cursor": "0xbea398"
        }
      ],
      "completed_zero_timer_stop_samples": [
        55,
        55
      ],
      "source_stereo_at_zero_pan_fields": 41,
      "native_stereo_gain_checks": 43,
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

## Handling / views / boost / settings

```json
{
  "status": "PASS",
  "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
  "cases": {
    "handling-ntsc": {
      "exact_yaw_updates": 118,
      "release_inertia_updates": 11,
      "direct_steering_updates": 43,
      "paused_yaw_updates": 9,
      "checks": [
        "actual angular velocity response",
        "fractional heading integration",
        "PAL/NTSC normalization",
        "release inertia settles",
        "direct/inertial setting",
        "pause freezes handling"
      ]
    },
    "views-ntsc": {
      "actual_vertices": 321,
      "pitched_vertices": 227,
      "actual_view_vertices_by_mode": {
        "0": 287,
        "1": 165,
        "2": 91
      },
      "bank_follow_vertices": 401,
      "paused_orbit_samples": 13,
      "independent_source_side_probes": 746,
      "cross_slope_filter_updates": 218,
      "source_font_banner_captures": [
        {
          "capture": "frame_00180.png",
          "code": 8,
          "source_font_pixels": 367
        },
        {
          "capture": "frame_00280.png",
          "code": 9,
          "source_font_pixels": 39
        },
        {
          "capture": "frame_00380.png",
          "code": 10,
          "source_font_pixels": 43
        },
        {
          "capture": "frame_00480.png",
          "code": 11,
          "source_font_pixels": 27
        },
        {
          "capture": "frame_00525.png",
          "code": 11,
          "source_font_pixels": 27
        },
        {
          "capture": "frame_00560.png",
          "code": 1,
          "source_font_pixels": 120
        },
        {
          "capture": "frame_00580.png",
          "code": 1,
          "source_font_pixels": 120
        },
        {
          "capture": "frame_00735.png",
          "code": 7,
          "source_font_pixels": 291
        },
        {
          "capture": "frame_00800.png",
          "code": 4,
          "source_font_pixels": 240
        }
      ],
      "exact_message_updates": 319,
      "triggered_event_codes": [
        1,
        4
      ],
      "drawn_message_codes": [
        1,
        4,
        7,
        8,
        9,
        10,
        11
      ],
      "paused_message_updates": 7,
      "exact_boost_decay_updates": 19,
      "manual_decay_updates": 0,
      "assisted_decay_updates": 19,
      "source_pad_refreshes": 3,
      "natural_expiries": 1,
      "paused_positive_boost_updates": 0,
      "duration_fields": 90,
      "checks": [
        "original-map cross-slope probes/filter",
        "mesh/normal camera-bank rotation",
        "real CHASE/ORBIT/NEAR placement",
        "paused orbit",
        "source-font animated banners in TOM output",
        "exact event priority/active-clock/slide",
        "source-pad boost expiry"
      ]
    },
    "boost-ntsc": {
      "exact_boost_decay_updates": 13,
      "manual_decay_updates": 7,
      "assisted_decay_updates": 6,
      "source_pad_refreshes": 3,
      "natural_expiries": 0,
      "paused_positive_boost_updates": 7,
      "duration_fields": 90,
      "probe_first_pad_field": 740,
      "checks": [
        "source-map pad refresh",
        "1.5 seconds at either video standard",
        "exact active-clock timer recurrence",
        "manual and assisted decay",
        "positive timer pause"
      ]
    },
    "settings-ntsc": {
      "checks": [
        "sixth native settings menu",
        "real camera/bank/HUD/particle/steering settings",
        "source-font setting labels",
        "Option retention",
        "keypad shortcuts",
        "actual bitmap/footer suppression",
        "disabled particle overlay during moving unpaused play",
        "particle overlay resumes"
      ],
      "source_font_pixels": 895,
      "absent_hud_pixels": 1730,
      "moving_fields_with_fx_disabled": 90
    },
    "view-replay-ntsc": {
      "recorded_pitch_pairs_verified": 76,
      "samples": 76,
      "interpolated_commits": 121,
      "fractional_commits": 84,
      "record_ticks": 324,
      "checks": [
        "real run samples",
        "time interpolation",
        "mesh positions and camera",
        "wrapped heading",
        "pause/resume",
        "stable end",
        "Option exit",
        "no replay score writes",
        "actual orbit camera XYZ/yaw/roll and composed cross-slope bank replay"
      ]
    },
    "handling-pal": {
      "exact_yaw_updates": 127,
      "release_inertia_updates": 11,
      "direct_steering_updates": 44,
      "paused_yaw_updates": 9,
      "checks": [
        "actual angular velocity response",
        "fractional heading integration",
        "PAL/NTSC normalization",
        "release inertia settles",
        "direct/inertial setting",
        "pause freezes handling"
      ]
    },
    "views-pal": {
      "actual_vertices": 362,
      "pitched_vertices": 261,
      "actual_view_vertices_by_mode": {
        "0": 396,
        "1": 224,
        "2": 116
      },
      "bank_follow_vertices": 536,
      "paused_orbit_samples": 20,
      "independent_source_side_probes": 712,
      "cross_slope_filter_updates": 252,
      "source_font_banner_captures": [
        {
          "capture": "frame_00180.png",
          "code": 8,
          "source_font_pixels": 367
        },
        {
          "capture": "frame_00280.png",
          "code": 9,
          "source_font_pixels": 39
        },
        {
          "capture": "frame_00380.png",
          "code": 10,
          "source_font_pixels": 43
        },
        {
          "capture": "frame_00455.png",
          "code": 11,
          "source_font_pixels": 27
        },
        {
          "capture": "frame_00480.png",
          "code": 1,
          "source_font_pixels": 120
        },
        {
          "capture": "frame_00490.png",
          "code": 1,
          "source_font_pixels": 120
        },
        {
          "capture": "frame_00665.png",
          "code": 7,
          "source_font_pixels": 291
        }
      ],
      "exact_message_updates": 360,
      "triggered_event_codes": [
        1,
        4
      ],
      "drawn_message_codes": [
        1,
        4,
        7,
        8,
        9,
        10,
        11
      ],
      "paused_message_updates": 7,
      "exact_boost_decay_updates": 19,
      "manual_decay_updates": 0,
      "assisted_decay_updates": 19,
      "source_pad_refreshes": 2,
      "natural_expiries": 1,
      "paused_positive_boost_updates": 6,
      "duration_fields": 75,
      "checks": [
        "original-map cross-slope probes/filter",
        "mesh/normal camera-bank rotation",
        "real CHASE/ORBIT/NEAR placement",
        "paused orbit",
        "source-font animated banners in TOM output",
        "exact event priority/active-clock/slide",
        "source-pad boost expiry"
      ]
    },
    "boost-pal": {
      "exact_boost_decay_updates": 15,
      "manual_decay_updates": 9,
      "assisted_decay_updates": 6,
      "source_pad_refreshes": 3,
      "natural_expiries": 0,
      "paused_positive_boost_updates": 10,
      "duration_fields": 75,
      "probe_first_pad_field": 649,
      "checks": [
        "source-map pad refresh",
        "1.5 seconds at either video standard",
        "exact active-clock timer recurrence",
        "manual and assisted decay",
        "positive timer pause"
      ]
    },
    "settings-pal": {
      "checks": [
        "sixth native settings menu",
        "real camera/bank/HUD/particle/steering settings",
        "source-font setting labels",
        "Option retention",
        "keypad shortcuts",
        "actual bitmap/footer suppression",
        "disabled particle overlay during moving unpaused play",
        "particle overlay resumes"
      ],
      "source_font_pixels": 895,
      "absent_hud_pixels": 1735,
      "moving_fields_with_fx_disabled": 90
    },
    "view-replay-pal": {
      "recorded_pitch_pairs_verified": 106,
      "samples": 106,
      "interpolated_commits": 131,
      "fractional_commits": 73,
      "record_ticks": 394,
      "checks": [
        "real run samples",
        "time interpolation",
        "mesh positions and camera",
        "wrapped heading",
        "pause/resume",
        "stable end",
        "Option exit",
        "no replay score writes",
        "actual orbit camera XYZ/yaw/roll and composed cross-slope bank replay"
      ]
    }
  }
}
```

## Expanded native sky / shadow / bloom / AV

```json
{
  "status": "PASS",
  "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
  "cases": {
    "bank-ntsc": {
      "rolled_sky_pixel_captures": [
        {
          "capture": "frame_00680.png",
          "exact_native_affine_sky_pixels": 4582,
          "pixels_distinguishing_unrolled_crop": 4496
        },
        {
          "capture": "frame_00800.png",
          "exact_native_affine_sky_pixels": 3440,
          "pixels_distinguishing_unrolled_crop": 3392
        },
        {
          "capture": "frame_00980.png",
          "exact_native_affine_sky_pixels": 2619,
          "pixels_distinguishing_unrolled_crop": 2577
        },
        {
          "capture": "frame_01200.png",
          "exact_native_affine_sky_pixels": 6522,
          "pixels_distinguishing_unrolled_crop": 6374
        },
        {
          "capture": "frame_01440.png",
          "exact_native_affine_sky_pixels": 1301,
          "pixels_distinguishing_unrolled_crop": 654
        },
        {
          "capture": "frame_01680.png",
          "exact_native_affine_sky_pixels": 6702,
          "pixels_distinguishing_unrolled_crop": 6468
        },
        {
          "capture": "frame_01900.png",
          "exact_native_affine_sky_pixels": 4838,
          "pixels_distinguishing_unrolled_crop": 4758
        },
        {
          "capture": "frame_02100.png",
          "exact_native_affine_sky_pixels": 5241,
          "pixels_distinguishing_unrolled_crop": 5125
        }
      ],
      "max_actual_source_segments": 400
    },
    "av-ntsc": {
      "native_bloom_operand_samples": 446,
      "native_shadow_operand_samples": 712,
      "actual_bloom_pixels": [
        {
          "capture": "frame_00900.png",
          "screen": [
            68,
            84
          ],
          "native_code": 30932
        },
        {
          "capture": "frame_01040.png",
          "screen": [
            68,
            84
          ],
          "native_code": 35065
        },
        {
          "capture": "frame_01180.png",
          "screen": [
            68,
            84
          ],
          "native_code": 34815
        },
        {
          "capture": "frame_01200.png",
          "screen": [
            68,
            84
          ],
          "native_code": 35069
        },
        {
          "capture": "frame_01300.png",
          "screen": [
            68,
            84
          ],
          "native_code": 38891
        }
      ],
      "actual_shadow_pixels": [
        {
          "capture": "frame_00680.png",
          "screen": [
            196,
            129
          ],
          "native_code": 22922
        },
        {
          "capture": "frame_00740.png",
          "screen": [
            196,
            128
          ],
          "native_code": 47256
        },
        {
          "capture": "frame_00800.png",
          "screen": [
            196,
            127
          ],
          "native_code": 30808
        }
      ],
      "blue_lit_face_texture_fields": 471,
      "independent_music_mute_fields": 39,
      "both_muted_actual_silent_i2s_fields": 50,
      "checks": [
        "original mesh silhouette ground projection/alpha",
        "separable native convolution",
        "signed-safe saturated hardware intensity addition",
        "actual TOM pixel equality",
        "source-blue lit scene texture consumption",
        "independent DSP music/effects mute",
        "controller-only live restore"
      ]
    },
    "menu-ntsc": {
      "source_font_pixels": 1300,
      "checks": [
        "real AV settings page with STAR",
        "all five settings changed through native menu",
        "original-font labels and values in actual TOM output",
        "Option RAM retention",
        "real keypad independent music/effects restore"
      ]
    },
    "bank-pal": {
      "rolled_sky_pixel_captures": [
        {
          "capture": "frame_00680.png",
          "exact_native_affine_sky_pixels": 3698,
          "pixels_distinguishing_unrolled_crop": 3618
        },
        {
          "capture": "frame_00800.png",
          "exact_native_affine_sky_pixels": 4472,
          "pixels_distinguishing_unrolled_crop": 4451
        },
        {
          "capture": "frame_00980.png",
          "exact_native_affine_sky_pixels": 3584,
          "pixels_distinguishing_unrolled_crop": 3415
        },
        {
          "capture": "frame_01200.png",
          "exact_native_affine_sky_pixels": 1316,
          "pixels_distinguishing_unrolled_crop": 664
        },
        {
          "capture": "frame_01440.png",
          "exact_native_affine_sky_pixels": 5263,
          "pixels_distinguishing_unrolled_crop": 5088
        },
        {
          "capture": "frame_01680.png",
          "exact_native_affine_sky_pixels": 4702,
          "pixels_distinguishing_unrolled_crop": 4601
        },
        {
          "capture": "frame_01900.png",
          "exact_native_affine_sky_pixels": 5750,
          "pixels_distinguishing_unrolled_crop": 5673
        },
        {
          "capture": "frame_02100.png",
          "exact_native_affine_sky_pixels": 3872,
          "pixels_distinguishing_unrolled_crop": 3804
        }
      ],
      "max_actual_source_segments": 400
    },
    "av-pal": {
      "native_bloom_operand_samples": 428,
      "native_shadow_operand_samples": 719,
      "actual_bloom_pixels": [
        {
          "capture": "frame_00900.png",
          "screen": [
            68,
            84
          ],
          "native_code": 35011
        },
        {
          "capture": "frame_01040.png",
          "screen": [
            68,
            84
          ],
          "native_code": 39163
        },
        {
          "capture": "frame_01180.png",
          "screen": [
            68,
            84
          ],
          "native_code": 30930
        },
        {
          "capture": "frame_01200.png",
          "screen": [
            68,
            84
          ],
          "native_code": 35053
        },
        {
          "capture": "frame_01300.png",
          "screen": [
            68,
            84
          ],
          "native_code": 34795
        }
      ],
      "actual_shadow_pixels": [
        {
          "capture": "frame_00680.png",
          "screen": [
            196,
            128
          ],
          "native_code": 30807
        },
        {
          "capture": "frame_00740.png",
          "screen": [
            190,
            130
          ],
          "native_code": 10402
        },
        {
          "capture": "frame_00800.png",
          "screen": [
            194,
            134
          ],
          "native_code": 46934
        }
      ],
      "blue_lit_face_texture_fields": 327,
      "independent_music_mute_fields": 40,
      "both_muted_actual_silent_i2s_fields": 50,
      "checks": [
        "original mesh silhouette ground projection/alpha",
        "separable native convolution",
        "signed-safe saturated hardware intensity addition",
        "actual TOM pixel equality",
        "source-blue lit scene texture consumption",
        "independent DSP music/effects mute",
        "controller-only live restore"
      ]
    },
    "menu-pal": {
      "source_font_pixels": 1300,
      "checks": [
        "real AV settings page with STAR",
        "all five settings changed through native menu",
        "original-font labels and values in actual TOM output",
        "Option RAM retention",
        "real keypad independent music/effects restore"
      ]
    }
  }
}
```

## Separate native GPU depth fixtures

```json
{
  "status": "PASS",
  "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
  "diagnostic_rom_sha256": "d6e9a762ee6371514e2d13705a83e96db03e03e1413a2264d502c47ab8dcae89",
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
  "gpu_overlay_end": "0xf03df0"
}
```

## Additional observed gameplay checks

```json
{
  "status": "PASS",
  "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
  "method": "Independent current-ROM observed-game/presentation-commit binding and exact message clock/priority/slide verification; source-map boost recurrence; no native memory writes.",
  "cases": {
    "race-ntsc": {
      "exact_message_updates": 3991,
      "triggered_event_codes": [
        1,
        2,
        3,
        4
      ],
      "drawn_message_codes": [
        1,
        2,
        3,
        4,
        8,
        9,
        10,
        11
      ],
      "paused_message_updates": 0,
      "exact_boost_decay_updates": 618,
      "manual_decay_updates": 0,
      "assisted_decay_updates": 618,
      "source_pad_refreshes": 54,
      "natural_expiries": 27,
      "paused_positive_boost_updates": 0,
      "duration_fields": 90
    },
    "race-pal": {
      "exact_message_updates": 4008,
      "triggered_event_codes": [
        1,
        2,
        3,
        4
      ],
      "drawn_message_codes": [
        1,
        2,
        3,
        4,
        8,
        9,
        10,
        11
      ],
      "paused_message_updates": 0,
      "exact_boost_decay_updates": 582,
      "manual_decay_updates": 0,
      "assisted_decay_updates": 582,
      "source_pad_refreshes": 54,
      "natural_expiries": 27,
      "paused_positive_boost_updates": 0,
      "duration_fields": 75
    },
    "manual-ntsc": {
      "exact_message_updates": 401,
      "triggered_event_codes": [
        1,
        5,
        6
      ],
      "drawn_message_codes": [
        1,
        5,
        6,
        7,
        8,
        9,
        10,
        11
      ],
      "paused_message_updates": 17
    },
    "manual-pal": {
      "exact_message_updates": 459,
      "triggered_event_codes": [
        1,
        5,
        6
      ],
      "drawn_message_codes": [
        1,
        5,
        6,
        7,
        8,
        9,
        10,
        11
      ],
      "paused_message_updates": 21
    },
    "dynamics-drive-ntsc": {
      "exact_message_updates": 353,
      "triggered_event_codes": [
        1,
        5
      ],
      "drawn_message_codes": [
        1,
        5,
        7,
        8,
        9,
        10,
        11
      ],
      "paused_message_updates": 12
    },
    "dynamics-drive-pal": {
      "exact_message_updates": 405,
      "triggered_event_codes": [
        1,
        5,
        6
      ],
      "drawn_message_codes": [
        1,
        5,
        6,
        7,
        8,
        9,
        10,
        11
      ],
      "paused_message_updates": 7
    },
    "views-ntsc": {
      "exact_message_updates": 319,
      "triggered_event_codes": [
        1,
        4
      ],
      "drawn_message_codes": [
        1,
        4,
        7,
        8,
        9,
        10,
        11
      ],
      "paused_message_updates": 7,
      "exact_boost_decay_updates": 19,
      "manual_decay_updates": 0,
      "assisted_decay_updates": 19,
      "source_pad_refreshes": 3,
      "natural_expiries": 1,
      "paused_positive_boost_updates": 0,
      "duration_fields": 90
    },
    "views-pal": {
      "exact_message_updates": 360,
      "triggered_event_codes": [
        1,
        4
      ],
      "drawn_message_codes": [
        1,
        4,
        7,
        8,
        9,
        10,
        11
      ],
      "paused_message_updates": 7,
      "exact_boost_decay_updates": 19,
      "manual_decay_updates": 0,
      "assisted_decay_updates": 19,
      "source_pad_refreshes": 2,
      "natural_expiries": 1,
      "paused_positive_boost_updates": 6,
      "duration_fields": 75
    },
    "boost-ntsc": {
      "exact_message_updates": 227,
      "triggered_event_codes": [
        1,
        4,
        5
      ],
      "drawn_message_codes": [
        1,
        4,
        5,
        7,
        8,
        9,
        10,
        11
      ],
      "paused_message_updates": 8,
      "exact_boost_decay_updates": 13,
      "manual_decay_updates": 7,
      "assisted_decay_updates": 6,
      "source_pad_refreshes": 3,
      "natural_expiries": 0,
      "paused_positive_boost_updates": 7,
      "duration_fields": 90
    },
    "boost-pal": {
      "exact_message_updates": 255,
      "triggered_event_codes": [
        1,
        4,
        5
      ],
      "drawn_message_codes": [
        1,
        4,
        5,
        7,
        8,
        9,
        10,
        11
      ],
      "paused_message_updates": 11,
      "exact_boost_decay_updates": 15,
      "manual_decay_updates": 9,
      "assisted_decay_updates": 6,
      "source_pad_refreshes": 3,
      "natural_expiries": 0,
      "paused_positive_boost_updates": 10,
      "duration_fields": 75
    }
  },
  "observed_event_codes": [
    1,
    2,
    3,
    4,
    5,
    6
  ],
  "observed_draw_codes": [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11
  ]
}
```

## Expanded native-system additional checks

```json
{
  "status": "PASS",
  "rom_sha256": "c7414e11b4edddc5274ae7d03742a31ee2f3e2bc9dcf815b331c9cfcc764572a",
  "method": "Independent post-run checks of current-ROM real-pad traces and original source assets. File inventory is not line/function parity. No game RAM writes.",
  "cases": {
    "bank-ntsc": {
      "rolled_sky_pixel_captures": [
        {
          "capture": "frame_00680.png",
          "exact_native_affine_sky_pixels": 4582,
          "pixels_distinguishing_unrolled_crop": 4496
        },
        {
          "capture": "frame_00800.png",
          "exact_native_affine_sky_pixels": 3440,
          "pixels_distinguishing_unrolled_crop": 3392
        },
        {
          "capture": "frame_00980.png",
          "exact_native_affine_sky_pixels": 2619,
          "pixels_distinguishing_unrolled_crop": 2577
        },
        {
          "capture": "frame_01200.png",
          "exact_native_affine_sky_pixels": 6522,
          "pixels_distinguishing_unrolled_crop": 6374
        },
        {
          "capture": "frame_01440.png",
          "exact_native_affine_sky_pixels": 1301,
          "pixels_distinguishing_unrolled_crop": 654
        },
        {
          "capture": "frame_01680.png",
          "exact_native_affine_sky_pixels": 6702,
          "pixels_distinguishing_unrolled_crop": 6468
        },
        {
          "capture": "frame_01900.png",
          "exact_native_affine_sky_pixels": 4838,
          "pixels_distinguishing_unrolled_crop": 4758
        },
        {
          "capture": "frame_02100.png",
          "exact_native_affine_sky_pixels": 5241,
          "pixels_distinguishing_unrolled_crop": 5125
        }
      ],
      "max_actual_source_segments": 400
    },
    "av-ntsc": {
      "convolution_and_actual_blitter_operand_samples": 446,
      "source_mesh_ground_shadow_samples": 712,
      "native_bg_decoder_pointers_while_muted": 40,
      "actual_bloom_pixels": [
        {
          "capture": "frame_00900.png",
          "screen": [
            68,
            84
          ],
          "native_code": 30932
        },
        {
          "capture": "frame_01040.png",
          "screen": [
            68,
            84
          ],
          "native_code": 35065
        },
        {
          "capture": "frame_01180.png",
          "screen": [
            68,
            84
          ],
          "native_code": 34815
        },
        {
          "capture": "frame_01200.png",
          "screen": [
            68,
            84
          ],
          "native_code": 35069
        },
        {
          "capture": "frame_01300.png",
          "screen": [
            68,
            84
          ],
          "native_code": 38891
        }
      ],
      "actual_source_mesh_shadow_pixels": [
        {
          "capture": "frame_00680.png",
          "screen": [
            196,
            129
          ],
          "native_code": 22922
        },
        {
          "capture": "frame_00740.png",
          "screen": [
            196,
            128
          ],
          "native_code": 47256
        },
        {
          "capture": "frame_00800.png",
          "screen": [
            196,
            127
          ],
          "native_code": 30808
        }
      ]
    },
    "particle-colors-ntsc": {
      "actual_source_color_composite_samples": 332,
      "current_rom_real_input_datasets": {
        "dynamics-drive-ntsc": 18,
        "manual-ntsc": 157,
        "manual-ntsc-direct": 157
      },
      "color_indices_per_kind": {
        "1": [
          0,
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          9,
          10,
          11,
          12,
          13,
          14,
          15
        ],
        "0": [
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11,
          12,
          13,
          14,
          15
        ]
      }
    },
    "bank-pal": {
      "rolled_sky_pixel_captures": [
        {
          "capture": "frame_00680.png",
          "exact_native_affine_sky_pixels": 3698,
          "pixels_distinguishing_unrolled_crop": 3618
        },
        {
          "capture": "frame_00800.png",
          "exact_native_affine_sky_pixels": 4472,
          "pixels_distinguishing_unrolled_crop": 4451
        },
        {
          "capture": "frame_00980.png",
          "exact_native_affine_sky_pixels": 3584,
          "pixels_distinguishing_unrolled_crop": 3415
        },
        {
          "capture": "frame_01200.png",
          "exact_native_affine_sky_pixels": 1316,
          "pixels_distinguishing_unrolled_crop": 664
        },
        {
          "capture": "frame_01440.png",
          "exact_native_affine_sky_pixels": 5263,
          "pixels_distinguishing_unrolled_crop": 5088
        },
        {
          "capture": "frame_01680.png",
          "exact_native_affine_sky_pixels": 4702,
          "pixels_distinguishing_unrolled_crop": 4601
        },
        {
          "capture": "frame_01900.png",
          "exact_native_affine_sky_pixels": 5750,
          "pixels_distinguishing_unrolled_crop": 5673
        },
        {
          "capture": "frame_02100.png",
          "exact_native_affine_sky_pixels": 3872,
          "pixels_distinguishing_unrolled_crop": 3804
        }
      ],
      "max_actual_source_segments": 400
    },
    "av-pal": {
      "convolution_and_actual_blitter_operand_samples": 428,
      "source_mesh_ground_shadow_samples": 719,
      "native_bg_decoder_pointers_while_muted": 40,
      "actual_bloom_pixels": [
        {
          "capture": "frame_00900.png",
          "screen": [
            68,
            84
          ],
          "native_code": 35011
        },
        {
          "capture": "frame_01040.png",
          "screen": [
            68,
            84
          ],
          "native_code": 39163
        },
        {
          "capture": "frame_01180.png",
          "screen": [
            68,
            84
          ],
          "native_code": 30930
        },
        {
          "capture": "frame_01200.png",
          "screen": [
            68,
            84
          ],
          "native_code": 35053
        },
        {
          "capture": "frame_01300.png",
          "screen": [
            68,
            84
          ],
          "native_code": 34795
        }
      ],
      "actual_source_mesh_shadow_pixels": [
        {
          "capture": "frame_00680.png",
          "screen": [
            196,
            128
          ],
          "native_code": 30807
        },
        {
          "capture": "frame_00740.png",
          "screen": [
            190,
            130
          ],
          "native_code": 10402
        },
        {
          "capture": "frame_00800.png",
          "screen": [
            194,
            134
          ],
          "native_code": 46934
        }
      ]
    },
    "particle-colors-pal": {
      "actual_source_color_composite_samples": 568,
      "current_rom_real_input_datasets": {
        "dynamics-drive-pal": 137,
        "manual-pal": 205,
        "manual-pal-direct": 226
      },
      "color_indices_per_kind": {
        "0": [
          0,
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11,
          12,
          13,
          14,
          15
        ],
        "1": [
          0,
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11,
          12,
          13,
          14,
          15
        ]
      }
    }
  }
}
```

This does not complete every remaining port system. Physical hardware and remote CI remain untested.
