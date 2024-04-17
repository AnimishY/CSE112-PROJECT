import sys

# Register file
x = [0] * 32

# PC and instruction memory
pc = 0
memory = [0] * 64

# Helper functions
def sign_extend(imm, n):
    return (imm & (1 << (n - 1)) ^ imm >> (n - 1)) << 32 - n

def get_register(reg):
    return x[reg]

def set_register(reg, value):
    x[reg] = value

# Instruction implementations
def add(rs1, rs2, rd):
    set_register(rd, get_register(rs1) + get_register(rs2))

def sub(rs1, rs2, rd):
    set_register(rd, get_register(rs1) - get_register(rs2))

def sll(rs1, rs2, rd):
    set_register(rd, get_register(rs1) << get_register(rs2) & 0xFFFFFFFF)

def slt(rs1, rs2, rd):
    set_register(rd, int(get_register(rs1) < get_register(rs2)))

def sltu(rs1, rs2, rd):
    set_register(rd, int(get_register(rs1) < get_register(rs2) or (get_register(rs1) == get_register(rs2) and get_register(rs1) & 0x80000000)))

def xor(rs1, rs2, rd):
    set_register(rd, get_register(rs1) ^ get_register(rs2))

def srl(rs1, rs2, rd):
    set_register(rd, get_register(rs1) >> get_register(rs2))

def or_(rs1, rs2, rd):
    set_register(rd, get_register(rs1) | get_register(rs2))

def and_(rs1, rs2, rd):
    set_register(rd, get_register(rs1) & get_register(rs2))

def lw(rs1, imm, rd):
    addr = get_register(rs1) + sign_extend(imm, 12)
    set_register(rd, memory[addr])

def addi(rs1, imm, rd):
    set_register(rd, get_register(rs1) + sign_extend(imm, 12))

def sltiu(rs1, imm, rd):
    set_register(rd, int(get_register(rs1) < sign_extend(imm, 12)))

def jalr(rs1, offset, rd):
    set_register(rd, pc + 4)
    pc = get_register(rs1) + sign_extend(offset, 12)

def sw(rs2, imm, rs1):
    addr = get_register(rs1) + sign_extend(imm, 12)
    memory[addr] = get_register(rs2)

def beq(rs1, rs2, offset):
    if get_register(rs1) == get_register(rs2):
        pc += sign_extend(offset, 13)

def bne(rs1, rs2, offset):
    if get_register(rs1) != get_register(rs2):
        pc += sign_extend(offset, 13)

def blt(rs1, rs2, offset):
    if get_register(rs1) < get_register(rs2):
        pc += sign_extend(offset, 13)

def bge(rs1, rs2, offset):
    if get_register(rs1) >= get_register(rs2):
        pc += sign_extend(offset, 13)

def bltu(rs1, rs2, offset):
    if int(get_register(rs1) < get_register(rs2) or (get_register(rs1) == get_register(rs2) and get_register(rs1) & 0x80000000)):
        pc += sign_extend(offset, 13)

def bgeu(rs1, rs2, offset):
    if int(get_register(rs1) >= get_register(rs2) or (get_register(rs1) == get_register(rs2) and get_register(rs1) & 0x80000000)):
        pc += sign_extend(offset, 13)

def lui(rd, imm):
    set_register(rd, imm << 12)

def auipc(rd, imm):
    set_register(rd, pc + (imm << 12))

def jal(rd, imm):
    set_register(rd, pc + 4)
    pc += sign_extend(imm, 21)

def mul(rs1, rs2, rd):
    set_register(rd, get_register(rs1) * get_register(rs2))

def rst():
    for i in range(1, 32):
        set_register(i, 0)

def halt():
    pass

def rvrs(rd, rs):
    set_register(rd, (get_register(rs) & 0x80000000) | (get_register(rs) >> 1))

# Main simulator loop
while True:
    instruction = memory[pc]
    opcode = instruction >> 7
    funct3 = instruction >> 12 & 0b111
    funct7 = instruction >> 25 & 0b1111111
    rs1 = instruction >> 15 & 0b11111
    rs2 = instruction >> 20 & 0b11111
    rd = instruction >> 7 & 0b11111
    imm12 = instruction & 0xFFF
    imm13 = (instruction & 0x1FFF) << 19
    imm20 = (instruction & 0xFFFFF) << 12
    imm21 = (instruction & 0x7FFFF) << 12

    if opcode == 0b000:
        if funct3 == 0b000:
            add(rs1, rs2, rd)
        elif funct3 == 0b001:
            sub(rs1, rs2, rd)
        elif funct3 == 0b010:
            sll(rs1, rs2, rd)
        elif funct3 == 0b011:
            slt(rs1, rs2, rd)
        elif funct3 == 0b100:
            sltu(rs1, rs2, rd)
        elif funct3 == 0b101:
            xor(rs1, rs2, rd)
        elif funct3 == 0b110:
            srl(rs1, rs2, rd)
        elif funct3 == 0b111:
            or_(rs1, rs2, rd)
    elif opcode == 0b001:
        if funct3 == 0b000:
            lw(rs1, imm12, rd)
        elif funct3 == 0b001:
            addi(rs1, imm12, rd)
        elif funct3 == 0b011:
            sltiu(rs1, imm12, rd)
        elif funct3 == 0b110:
            jalr(rs1, imm12, rd)
    elif opcode == 0b010:
        sw(rs2, imm12, rs1)
    elif opcode == 0b110:
        if funct3 == 0b000:
            beq(rs1, rs2, imm13)
        elif funct3 == 0b001:
            bne(rs1, rs2, imm13)
        elif funct3 == 0b100:
            blt(rs1, rs2, imm13)
        elif funct3 == 0b101:
            bge(rs1, rs2, imm13)
        elif funct3 == 0b110:
            bltu(rs1, rs2, imm13)
        elif funct3 == 0b111:
            bgeu(rs1, rs2, imm13)
    elif opcode == 0b011:
        if funct3 == 0b000:
            lui(rd, imm20)
        elif funct3 == 0b001:
            auipc(rd, imm20)
    elif opcode == 0b111:
        if funct3 == 0b000:
            jal(rd, imm21)
    elif opcode == 0b011 and funct3 == 0b111:
        if funct7 == 0b0000000:
            mul(rs1, rs2, rd)
        elif funct7 == 0b1111111:
            rst()
        elif funct7 == 0b0000001:
            halt()
        elif funct7 == 0b0100000:
            rvrs(rd, rs)
    elif opcode == 0b000 and funct3 == 0b000 and rs1 == 0 and rs2 == 0 and imm12 == 0:
        pass

    pc += 4