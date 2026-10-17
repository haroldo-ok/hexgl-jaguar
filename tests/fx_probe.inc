; Native GPU unit fixture, compiled ONLY into the separately labeled probe ROM.
; Calls the unchanged production fx_occluded routine. No host game-RAM writes.
fx_selftest:
 PUSHLR
 movei #FX_AUX,r15
 load (r15+124),r0
 movei #$46585054,r1
 cmp r1,r0
 movei #fx_selftest_finished,r0
 jump eq,(r0)
 nop
 movei #tri_ptrs_ram,r0
 movei #1024,r1
 moveq #0,r2
.clear
 store r2,(r0)
 addq #4,r0
 subq #1,r1
 jr ne,.clear
 nop
 movei #tri_array_ram+4,r16
 movei #tri_ptrs_ram,r0
 store r16,(r0)
 store r2,(r16)
 movei #100<<16|100,r0
 move r16,r1
 addq #8,r1
 store r0,(r1)
 addq #4,r1
 movei #200<<16|100,r0
 store r0,(r1)
 addq #4,r1
 movei #150<<16|180,r0
 store r0,(r1)
 addq #4,r1
 movei #FX_AUX+120,r0
 store r0,(r1)
 movei #2<<16,r1
 store r1,(r0)
 movei #TRI_DEPTH,r0
 movei #100,r1
 store r1,(r0)
 addq #4,r0
 store r1,(r0)
 addq #4,r0
 store r1,(r0)
 include "../tests/fx_probe_cases.inc"
 movei #FX_AUX+124,r0
 movei #$46585054,r1
 store r1,(r0)
fx_selftest_finished:
 POPLR
