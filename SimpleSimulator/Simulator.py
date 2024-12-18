import sys
import shutil

registersbinary = {
    '00000': 'zero', '00001': 'ra', '00010': 'sp', '00011': 'gp', '00100': 'tp',
    '00101': 't0', '00110': 't1', '00111': 't2', '01000': 's0', '01001': 's1',
    '01010': 'a0', '01011': 'a1', '01100': 'a2', '01101': 'a3', '01110': 'a4',
    '01111': 'a5', '10000': 'a6', '10001': 'a7', '10010': 's2', '10011': 's3',
    '10100': 's4', '10101': 's5', '10110': 's6', '10111': 's7', '11000': 's8',
    '11001': 's9', '11010': 's10', '11011': 's11', '11100': 't3', '11101': 't4',
    '11110': 't5', '11111': 't6'
}

registers = {
    "zero": 0b00, "ra": 0b00, "sp": 0b0100000000, "gp": 0b00, "tp": 0b00,
    "t0": 0b00, "t1": 0b00, "t2": 0b00, "s0": 0b00, "s1": 0b00,
    "a0": 0b00, "a1": 0b00, "a2": 0b00, "a3": 0b00, "a4": 0b00,
    "a5": 0b00, "a6": 0b00, "a7": 0b00, "s2": 0b00, "s3": 0b00,
    "s4": 0b00, "s5": 0b00, "s6": 0b00, "s7": 0b00, "s8": 0b00,
    "s9": 0b00, "s10": 0b00, "s11": 0b00, "t3": 0b00, "t4": 0b00,
    "t5": 0b00, "t6": 0b00
}

PC = 0b00000000000000000000000000000100 #error

memory = {0x00010000: 0, 0x00010004: 0, 0x00010008: 0, 0x0001000C: 0, 0x00010010: 0, 0x00010014: 0, 0x00010018: 0, 0x0001001C: 0,
          0x00010020: 0, 0x00010024: 0, 0x00010028: 0, 0x0001002C: 0, 0x00010030: 0, 0x00010034: 0, 0x00010038: 0, 0x0001003C: 0,
          0x00010040: 0, 0x00010044: 0, 0x00010048: 0, 0x0001004C: 0, 0x00010050: 0, 0x00010054: 0, 0x00010058: 0, 0x0001005C: 0,
          0x00010060: 0, 0x00010064: 0, 0x00010068: 0, 0x0001006C: 0, 0x00010070: 0, 0x00010074: 0, 0x00010078: 0, 0x0001007C: 0}

MAIN_CODE = {}
input_file = sys.argv[1]
output_file = sys.argv[2]

infile = open(input_file, "r")
data = infile.read()
infile.close()


def signed_magnitude_to_int(binary):
    if binary[3] == '0':
        return int(binary, 2)
    else:
        return -int(binary[2:], 2)

def int_to_signed_magnitude(number):
    if number >= 0:
        return '0' + bin(number)[2:]
    else:
        return '1' + bin(-number)[2:]

def ADD(rs1, rs2, rd):
    rs1 = signed_magnitude_to_int(rs1[2:])
    rs2 = signed_magnitude_to_int(rs2[2:])
    rd = rs1 + rs2
    return int_to_signed_magnitude(rd)


def SUB(rs1, rs2, rd):
    rs1 = signed_magnitude_to_int(rs1[2:])
    rs2 = signed_magnitude_to_int(rs2[2:])
    rd = rs1 - rs2
    return int_to_signed_magnitude(rd)

def SLL(rd, rs1, rs2):
    rd = rs1 << rs2
    return rd

def XOR(bin1, bin2, rd):
    max_len = max(len(bin1), len(bin2))
    bin1 = bin1.zfill(max_len)
    bin2 = bin2.zfill(max_len)

    result = ''
    for i in range(3,max_len):
        result += '1' if bin1[i] != bin2[i] else '0'

    rd = result
    return int_to_signed_magnitude(int(rd)) #ERRORRRRRR


def SLT(rs1, rs2, rd):
    if rs1 < rs2:
        rd = 1
    else:
        rd = 0
    return rd


def SLTU(rs1, rs2, rd):
    if rs1 < 0:
        rs1 = -1 * rs1
    if rs2 < 0:
        rs2 = -1 * rs2

    if rs1 < rs2:
        rd = 1
    else:
        rd = 0
    return rd


def SRL(rs1, rs2, rd):
    rd = rs1 >> rs2
    return rd


def OR(rs1, rs2, rd):
    rd = rs1 | rs2
    return rd


def AND(rs1, rs2, rd):
    rd = rs1 & rs2
    return rd


def LW(rs1, rd, imm):
    address = rs1 + (imm & 0xFFF) #to mask off the upper 20 bits and keeps only the lower 12 bits of imm
    if address in memory: #memory dictionary jo tumne banayi
        rd = memory[address]
    else:
        rd = 0
    return rd


def ADDI(rs1, imm, rd):
    rd = rs1 + imm
    return rd


def SLTIU(rs1, imm, rd):
    if rs1 < imm:
        rd = 1
    else:
        rd = 0
    return rd

def JALR(rs1, imm, rd):
    global PC
    rd = PC + 4
    PC = rs1 + imm
    return rd


def SW(reg1, reg2, imm):
    address = reg2 + (imm & 0xFFF)  # Calculate the effective address
    memory[address] = reg1 

def LUI(reg1, imm):
    reg1 = imm << 12  # Shift the immediate value left by 12 bits
    return reg1

def AUIPC(reg1, imm):
    global i
    reg1 = i + (imm << 12)  # Add the immediate value (shifted left by 12 bits) to the current PC
    return reg1

def bin32(x):
    return '0b' + bin(x)[2:].zfill(32)

def hex8(x):
    return '0x' + hex(x)[2:].zfill(8)

for i in data.split("\n"):
    if i != "":
        temp = i.split(" ")
        MAIN_CODE[PC] = temp
        PC += 0b00000000000000000000000000000100


for i in MAIN_CODE:
    print(bin(i), MAIN_CODE[i])

# access the key of the last element in the dictionary
last_key = list(MAIN_CODE.keys())[-1]

first_key = list(MAIN_CODE.keys())[0]

output_file = open(output_file, "w")

i = 0b00000000000000000000000000000100
while i <= last_key:
    print("PC: ", i, end=" ")
    if MAIN_CODE[i][0][25:32] == '0110011':
        print("R", end=" ")
        if MAIN_CODE[i][0][17:20] == '000':
            if MAIN_CODE[i][0][0:7] == '0000000':
                print("ADD")
                rs1 = MAIN_CODE[i][0][12:17]
                rs2 = MAIN_CODE[i][0][7:12]
                rd = MAIN_CODE[i][0][20:25]
                registers[registersbinary[rd]] = ADD(
                    registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
            elif MAIN_CODE[i][0][0:7] == '0100000':
                print("SUB")
                registers[registersbinary[rd]] = SUB(
                    registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '001':
            print("SLL")
            rs1 = MAIN_CODE[i][0][12:17]
            rs2 = MAIN_CODE[i][0][7:12]
            rd = MAIN_CODE[i][0][20:25]
            registers[registersbinary[rd]] = SLL(
                registers[registersbinary[rd]], registers[registersbinary[rs1]], registers[registersbinary[rs2]])
        elif MAIN_CODE[i][0][17:20] == '010':
            print("SLT")
            registers[registersbinary[rd]] = SLT(
                registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '011':
            print("SLTU")
            registers[registersbinary[rd]] = SLTU(
                registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '100':
            print("XOR")
            registers[registersbinary[rd]] = XOR(
                registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '101':
            print("SRL")
            registers[registersbinary[rd]] = SRL(
                registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '110':
            print("OR")
            registers[registersbinary[rd]] = OR(
                registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '111':
            print("AND")
            registers[registersbinary[rd]] = AND(
                registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
    elif MAIN_CODE[i][0][25:32] in ['0000011', '0010011', '0010011', '1100111']:
        print("I", end=" ")
        if MAIN_CODE[i][0][17:20] == '010' and MAIN_CODE[i][0][25:32] == '0000011':
            print("LW")
            rs1 = MAIN_CODE[i][0][12:17]
            imm = MAIN_CODE[i][0][0:12]
            rd = MAIN_CODE[i][0][20:25]
            registers[registersbinary[rd]] = LW(registers[registersbinary[rs1]], registers[registersbinary[rd]], signed_magnitude_to_int(imm))
        elif MAIN_CODE[i][0][17:20] == '000' and MAIN_CODE[i][0][25:32] == '0010011':
            print("ADDI")
            rs1 = MAIN_CODE[i][0][12:17]
            imm = MAIN_CODE[i][0][0:12]
            rd = MAIN_CODE[i][0][20:25]
            registers[registersbinary[rd]] = ADDI(
                registers[registersbinary[rs1]], signed_magnitude_to_int(imm), registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '011' and MAIN_CODE[i][0][25:32] == '0010011':
            print("SLTIU")
            registers[registersbinary[rd]] = SLTIU(
                registers[registersbinary[rs1]], signed_magnitude_to_int(imm), registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '000' and MAIN_CODE[i][0][25:32] == '1100111':
            print("JALR")
            rs1 = MAIN_CODE[i][0][12:17]
            imm = MAIN_CODE[i][0][0:12]
            rd = MAIN_CODE[i][0][20:25]
            registers[registersbinary[rd]] = JALR(registers[registersbinary[rs1]], signed_magnitude_to_int(imm), registers[registersbinary[rd]])
            registers[registersbinary[rd]] = i + 4  # Save the current PC + 4 to the destination register
            i = registers[registersbinary[rs1]] + signed_magnitude_to_int(imm)  # Update PC with the effective jump address

    elif MAIN_CODE[i][0][25:32] == '0100011':
        print("S", end=" ")
        print("SW")

    elif MAIN_CODE[i][0][25:32] == '1100011':
        print("B", end=" ")
        if MAIN_CODE[i][0][17:20] == '000':
            print("BEQ")
            rs1 = MAIN_CODE[i][0][12:17]
            rs2 = MAIN_CODE[i][0][7:12]
            imm = MAIN_CODE[i][0][0:7]
            if registers[registersbinary[rs1]] == registers[registersbinary[rs2]]:
                i = i + signed_magnitude_to_int(imm)
        elif MAIN_CODE[i][0][17:20] == '001':
            print("BNE")
            rs1 = MAIN_CODE[i][0][12:17]
            rs2 = MAIN_CODE[i][0][7:12]
            imm = MAIN_CODE[i][0][0:7]
            if registers[registersbinary[rs1]] != registers[registersbinary[rs2]]:
                i = i + signed_magnitude_to_int(imm)
        elif MAIN_CODE[i][0][17:20] == '100':
            print("BLT")
            rs1 = MAIN_CODE[i][0][12:17]
            rs2 = MAIN_CODE[i][0][7:12]
            imm = MAIN_CODE[i][0][0:7]
            if registers[registersbinary[rs1]] < registers[registersbinary[rs2]]:
                i = i + signed_magnitude_to_int(imm)
        elif MAIN_CODE[i][0][17:20] == '101':
            print("BGE")
            rs1 = MAIN_CODE[i][0][12:17]
            rs2 = MAIN_CODE[i][0][7:12]
            imm = MAIN_CODE[i][0][0:7]
            if registers[registersbinary[rs1]] >= registers[registersbinary[rs2]]:
                i = i + signed_magnitude_to_int(imm)
        elif MAIN_CODE[i][0][17:20] == '110':
            print("BLTU")
            rs1 = MAIN_CODE[i][0][12:17]
            rs2 = MAIN_CODE[i][0][7:12]
            imm = MAIN_CODE[i][0][0:7]
            if registers[registersbinary[rs1]] < registers[registersbinary[rs2]]:
                i = i + signed_magnitude_to_int(imm)
        elif MAIN_CODE[i][0][17:20] == '111':
            print("BGEU")
            rs1 = MAIN_CODE[i][0][12:17]
            rs2 = MAIN_CODE[i][0][7:12]
            imm = MAIN_CODE[i][0][0:7]
            if registers[registersbinary[rs1]] >= registers[registersbinary[rs2]]:
                i = i + signed_magnitude_to_int(imm)
    elif MAIN_CODE[i][0][25:32] in ['0110111', '0010111']:
        print("U")
    elif MAIN_CODE[i][0][25:32] == '1101111':
        print("J")
    else:
        print("Unknown")
    print("Registers: ", registers)
    print("Memory: ", memory)
    string1 = f"{bin32(i)} {bin32(registers['zero'])} {bin32(registers['ra'])} {bin32(registers['sp'])} {bin32(registers['gp'])} {bin32(registers['tp'])} {bin32(registers['t0'])} {bin32(registers['t1'])} {bin32(registers['t2'])} {bin32(registers['s0'])} {bin32(registers['s1'])} {bin32(registers['a0'])} {bin32(registers['a1'])} {bin32(registers['a2'])} {bin32(registers['a3'])} {bin32(registers['a4'])} {bin32(registers['a5'])} {bin32(registers['a6'])} {bin32(registers['a7'])} {bin32(registers['s2'])} {bin32(registers['s3'])} {bin32(registers['s4'])} {bin32(registers['s5'])} {bin32(registers['s6'])} {bin32(registers['s7'])} {bin32(registers['s8'])} {bin32(registers['s9'])} {bin32(registers['s10'])} {bin32(registers['s11'])} {bin32(registers['t3'])} {bin32(registers['t4'])} {bin32(registers['t5'])} {bin32(registers['t6'])}\n"
    output_file.write(string1)

    i += 0b00000000000000000000000000000100


for i in memory:
    string2 = f"{hex8(i)}:{bin32(memory[i])}\n"
    output_file.write(string2)

output_file.close()
print("Registers: ", registers)
print("Memory: ", memory)
