# dictionary with assembly command : [opode, opcode type, func 3, func 7]
# if invalid then "inv"
opcode = {
    'add': ['0110011', 'R', '000', '0000000'],
    'sub': ['0110011', 'R', '000', '0100000'],
    'sll': ['0110011', 'R', '001', '0000000'],
    'slt': ['0110011', 'R', '010', '0000000'],
    'sltu': ['0110011', 'R', '011', '0000000'],
    'xor': ['0110011', 'R', '100', '0000000'],
    'srl': ['0110011', 'R', '101', '0000000'],
    'or': ['0110011', 'R', '110', '0000000'],
    'and': ['0110011', 'R', '111', '0000000'],
    'lw': ['0000011', 'I', '010', 'inv'],
    'addi': ['0010011', 'I', '000', 'inv'],
    'sltiu': ['0010011', 'I', '011', 'inv'],
    'jalr': ['1100111', 'I', '000', 'inv'],
    'sw': ['0100011', 'S', '010', 'inv'],
    'beq': ['1100011', 'B', '000', 'inv'],
    'bne': ['1100011', 'B', '001', 'inv'],
    'blt': ['1100011', 'B', '100', 'inv'],
    'bge': ['1100011', 'B', '101', 'inv'],
    'bltu': ['1100011', 'B', '110', 'inv'],
    'bgeu': ['1100011', 'B', '111', 'inv'],
    'lui': ['0110111', 'U', 'inv', 'inv'],
    'auipc': ['0010111', 'U', 'inv', 'inv'],
    'jal': ['1101111', 'J', 'inv', 'inv'],
    'hlt': ['1111111', 'C', 'inv', 'inv'],
    'mul': ['0000000', 'C', 'inv', 'inv'],
    'rst': ['0000001', 'C', 'inv', 'inv'],
    'rvrs': ['0000010', 'C', 'inv', 'inv']
}

#register adresses in format ABI : binary adress
registers = {
    'zero': '00000', # hard wired to 0
    'ra': '00001', # return address
    'sp': '00010', # stack pointer
    'gp': '00011', # global pointer
    'tp': '00100', # thread pointer
    't0': '00101', # temporary
    't1': '00110', # temporaries
    't2': '00111', # temporaries
    's0': '01000', # saved register / frame pointer
    'fp': '01000', # saved register / frame pointer
    's1': '01001', # saved register
    'a0': '01010', # return value
    'a1': '01011', # return value
    'a2': '01100', # argument
    'a3': '01101', # argument
    'a4': '01110', # argument
    'a5': '01111', # argument
    'a6': '10000', # argument
    'a7': '10001', # argument 
    's2': '10010', # saved register
    's3': '10011', # saved register
    's4': '10100', # saved register
    's5': '10101', # saved register
    's6': '10110', # saved register
    's7': '10111', # saved register
    's8': '11000', # saved register
    's9': '11001', # saved register
    's10': '11010', # saved register
    's11': '11011', # saved register
    't3': '11100', # temporaries
    't4': '11101', # temporaries
    't5': '11110', # temporaries
    't6': '11111', # temporaries
}

# function to find opcode
def find_opcode(asmcmd):
    opcude_list = {
    'add': ['0110011', 'R', '000', '0000000'],
    'sub': ['0110011', 'R', '000', '0100000'],
    'sll': ['0110011', 'R', '001', '0000000'],
    'slt': ['0110011', 'R', '010', '0000000'],
    'sltu': ['0110011', 'R', '011', '0000000'],
    'xor': ['0110011', 'R', '100', '0000000'],
    'srl': ['0110011', 'R', '101', '0000000'],
    'or': ['0110011', 'R', '110', '0000000'],
    'and': ['0110011', 'R', '111', '0000000'],
    'lw': ['0000011', 'I', '010', 'inv'],
    'addi': ['0010011', 'I', '000', 'inv'],
    'sltiu': ['0010011', 'I', '011', 'inv'],
    'jalr': ['1100111', 'I', '000', 'inv'],
    'sw': ['0100011', 'S', '010', 'inv'],
    'beq': ['1100011', 'B', '000', 'inv'],
    'bne': ['1100011', 'B', '001', 'inv'],
    'blt': ['1100011', 'B', '100', 'inv'],
    'bge': ['1100011', 'B', '101', 'inv'],
    'bltu': ['1100011', 'B', '110', 'inv'],
    'bgeu': ['1100011', 'B', '111', 'inv'],
    'lui': ['0110111', 'U', 'inv', 'inv'],
    'auipc': ['0010111', 'U', 'inv', 'inv'],
    'jal': ['1101111', 'J', 'inv', 'inv'],
    'hlt': ['1111111', 'C', 'inv', 'inv'],
    'mul': ['0000000', 'C', 'inv', 'inv'],
    'rst': ['0000001', 'C', 'inv', 'inv'],
    'rvrs': ['0000010', 'C', 'inv', 'inv']
}

    if asmcmd in opcude_list:
        return opcude_list[asmcmd[0]]
    
def find_reg(reg):
    registers = {
        'zero': '00000', # hard wired to 0
        'ra': '00001', # return address
        'sp': '00010', # stack pointer
        'gp': '00011', # global pointer
        'tp': '00100', # thread pointer
        't0': '00101', # temporary
        't1': '00110', # temporaries
        't2': '00111', # temporaries
        's0': '01000', # saved register / frame pointer
        'fp': '01000', # saved register / frame pointer
        's1': '01001', # saved register
        'a0': '01010', # return value
        'a1': '01011', # return value
        'a2': '01100', # argument
        'a3': '01101', # argument
        'a4': '01110', # argument
        'a5': '01111', # argument
        'a6': '10000', # argument
        'a7': '10001', # argument 
        's2': '10010', # saved register
        's3': '10011', # saved register
        's4': '10100', # saved register
        's5': '10101', # saved register
        's6': '10110', # saved register
        's7': '10111', # saved register
        's8': '11000', # saved register
        's9': '11001', # saved register
        's10': '11010', # saved register
        's11': '11011', # saved register
        't3': '11100', # temporaries
        't4': '11101', # temporaries
        't5': '11110', # temporaries
        't6': '11111', # temporaries
    }
    if reg in registers:
        return registers[reg]
    
def find_fn7(asmcmd):
    opcude_list = {
    'add': ['0110011', 'R', '000', '0000000'],
    'sub': ['0110011', 'R', '000', '0100000'],
    'sll': ['0110011', 'R', '001', '0000000'],
    'slt': ['0110011', 'R', '010', '0000000'],
    'sltu': ['0110011', 'R', '011', '0000000'],
    'xor': ['0110011', 'R', '100', '0000000'],
    'srl': ['0110011', 'R', '101', '0000000'],
    'or': ['0110011', 'R', '110', '0000000'],
    'and': ['0110011', 'R', '111', '0000000'],
}

    if asmcmd in opcude_list:
        return opcude_list[asmcmd[3]]
    
def find_fn3(asmcmd):
        opcude_list = {
        'add': ['0110011', 'R', '000', '0000000'],
        'sub': ['0110011', 'R', '000', '0100000'],
        'sll': ['0110011', 'R', '001', '0000000'],
        'slt': ['0110011', 'R', '010', '0000000'],
        'sltu': ['0110011', 'R', '011', '0000000'],
        'xor': ['0110011', 'R', '100', '0000000'],
        'srl': ['0110011', 'R', '101', '0000000'],
        'or': ['0110011', 'R', '110', '0000000'],
        'and': ['0110011', 'R', '111', '0000000'],
        'lw': ['0000011', 'I', '010', 'inv'],
        'addi': ['0010011', 'I', '000', 'inv'],
        'sltiu': ['0010011', 'I', '011', 'inv'],
        'jalr': ['1100111', 'I', '000', 'inv'],
        'sw': ['0100011', 'S', '010', 'inv'],
        'beq': ['1100011', 'B', '000', 'inv'],
        'bne': ['1100011', 'B', '001', 'inv'],
        'blt': ['1100011', 'B', '100', 'inv'],
        'bge': ['1100011', 'B', '101', 'inv'],
        'bltu': ['1100011', 'B', '110', 'inv'],
        'bgeu': ['1100011', 'B', '111', 'inv'],
        }
    
        if asmcmd in opcude_list:
            return opcude_list[asmcmd[2]]
        
def imm(n, num_bits):
    if n < 0:
       
        binary_repr = bin(n & ((1 << num_bits) - 1))[2:]
    else:
        
        binary_repr = bin(n)[2:].zfill(num_bits)

    return binary_repr

def halterror(halt, l1):
    count=0
    for i in range(len(1)):
        if l1[i]==halt:
            count+=1
        if count>1:
            file=open('binary.txt','w')
            file.write("error: More than one virtual halt")
            file.close()
            return True
        if count==1:
            if l1[len(l1)]!=halt:
                file=open('binary.txt','w')
                file.write("error: Halt not last instruction")
                file.close()
                return True
        if count==0:
            file=open('binary.txt','w')
            file.write("error: No virtual halt found")
            file.close()
            return True
    return False
        
    
def error_check(list):
    "incomplete"

def assemble(input_file, output_file):
    with open(input_file, 'r') as file:
        assembly_code = file.readlines()

    binary_code = []

    for line_number, line in enumerate(assembly_code, start=1):
        line = line.strip()
        
        #add r1,r2,r3
        command_list = []
        asmcmd, operands = line.split()
        operands = operands.split(',')
        command_list.append(asmcmd)
        command_list.extend(operands)
        error_check(command_list)
        
        asmcmd_info = find_opcode(asmcmd) # check for valid opcode
        if asmcmd_info is None:
            error_message = f"Invalid opcode '{asmcmd}' at line {line_number}"
            with open(output_file, 'w') as file:
                file.write(error_message)
                file.close()
            return


        opcode = asmcmd_info[0]
        asmcmd_type = asmcmd_info[1]

        #add r1, r2 ,r3
        if asmcmd_type == 'R':
            bin = find_fn7(asmcmd) + find_reg(command_list[3]) + find_reg(command_list[2]) + find_fn3(asmcmd) + find_reg(command_list[1]) + opcode
            binary_code.append(bin)
        
        elif asmcmd_type == 'I':
            bin = imm(command_list[1], 12) + find_reg(command_list[2]) + find_fn3(asmcmd) + find_reg(command_list[1]) + opcode
            binary_code.append(bin)

        elif asmcmd_type == 'S':
            b
        
# Test the assembler
assemble('assembly_code.txt', 'binary_code.txt')


