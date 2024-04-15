start: lui t0,100
    addi t1,t0,-50
    bge t1,zero,end
    bltu t2,t1,start
    addi t2,t1,20
    add t3,t1,t2
    jal gp,-512
    jalr t4,t0,0
end: beq zero,zero,0