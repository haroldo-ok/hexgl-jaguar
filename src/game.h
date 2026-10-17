; Native fixed-point gameplay state. Coordinates Q24.8, angles 512 steps * 4.
GAME equ $1000
VBL_TICKS equ $1080
MOTION equ $10a0 ; 17 words ending $10e3, separate from VBL/DSP counters
collision_map equ $a00000
height_map equ $a40000
replay_data equ $ac0000
replay_count equ 5625
; GAME: magic, updates, phase, countdown, x,y,z,heading,speed,shield,
; lap,checkpoint,boost,paused,replay,replay_index,race_ticks,collisions,
; last_vbl, input. Phase: 0 ready, 1 race, 2 destroyed, 3 finished, 4 countdown.
; +80 video Hz (50/60), +84 lap start ticks, +88/+92/+96 completed lap times,
; +100 best completed lap. All timings are video fields; pause excludes time.
; +104/+108 message/status DRAM pointers; +112..+124 reserved.
; Text formatting scratch at $1200..$126b, safely below program entry.
; Countdown matches Gameplay.js HUD timing: ready 2.5s, 3/2/1 1.5s each.

 include "../assets/route.inc"

; Standalone-stock front end and two independently journaled score categories.
FRONT equ $1300
; +0 magic,+4 selection,+8 panel,+12 block-start,+16 reserved,+20 reserved
; +24 manual total ms,+28 manual lap ms,+32 generation,+36 active EEPROM slot
; +40 autopilot total ms,+44 lap ms,+48 generation,+52 active slot
; +56 assisted latch,+60 save status (0 idle,1 pending,2 verified,3 error)
; +64 word writes,+68 loaded journals,+72 reserved,+76 previous phase
; +$80/$90/$a0/$b0 four formatted score strings, 10 bytes each.
EE_BUFFER equ $1400
EE_WORK equ $1440
; In-RAM last-run recording: 6144 complete 64-byte samples, never flash writes.
REPLAY equ $1500
REPLAY_BUFFER equ $150000
REPLAY_CAPACITY equ 6144
; words: magic,count,playing,index,clock,lastVBL,lastPhase,full,ended,lastTick,
; commit,alphaQ8,tick0,tick1,recordHz,expectedMotionCommit,sourcePhase,lap1/2/3
; samples: x/y/z Q8,heading,roll/pull/cameraY Q8,ticks,speed,shield,lap,boost,
; collisions,sourcePhase,lapStart,bestLap. Buffer ends $1b0000 before video.

PHYS equ $1600
REPLAY_ANGLES equ $1b0000 ; 6144 pairs of signed pitch steps, ends $1b3000

FX equ $1700
FX_POOL equ $1800 ; 16 * 32 bytes, ends $1a00 below code entry

AUDIO_STATE equ $1a00 ; 10 DSP words: seqlock,L,R,pan,centerL,spaceL,centerR,spaceR,bgPtr,boostPtr
ADPCM_STATE equ $1a80 ; five 24-byte native decoder states, end $1af8
MATERIAL_STATE equ $1a40 ; atlas pointer, bank, draw count, last texture pointer

FX_AUX equ $1b00 ; inherited velocity, projection and actual pixel blend proof
FX_DEPTH equ $1c00 ; read-only submitted-triangle depth query diagnostics
TRI_DEPTH equ $e0000 ; 8192 records x 3 actual vertex Z words, ends $f8000, plus 12-byte overflow guard for the first rejected face
