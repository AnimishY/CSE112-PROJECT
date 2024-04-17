zero = 0
s5 = 0

def addi(reg1, reg2, imm):
    reg1 = reg2 + imm
    if reg1 > 65535:
        reg1 = reg1 % 65535
    return reg1

print(addi(s5, zero, 11))
