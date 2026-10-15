; Native fixed-point gameplay state. Coordinates Q24.8, angles 512 steps * 4.
GAME equ $1000
VBL_TICKS equ $1080
collision_map equ $a00000
height_map equ $a40000
replay_data equ $ac0000
replay_count equ 5625
; GAME: magic, updates, phase, countdown, x,y,z,heading,speed,shield,
; lap,checkpoint,boost,paused,replay,replay_index,race_ticks,collisions,
; last_vbl, input. Phase: 0 ready, 1 race, 2 destroyed, 3 finished.

 include "../assets/route.inc"
