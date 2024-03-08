opcode = {
    'add': ['0110011', 'R'],
    'sub': ['0110011', 'R'],
    'sll': ['0110011', 'R'],
    'slt': ['0110011', 'R'],
    'sltu': ['0110011', 'R'],
    'xor': ['0110011', 'R'],
    'srl': ['0110011', 'R'],
    'or': ['0110011', 'R'],
    'and': ['0110011', 'R'],
    'lw': ['0000011', 'I'],
    'addi': ['0010011', 'I'],
    'sltiu': ['0010011', 'I'],
    'jalr': ['1100111', 'I'],
    'sw': ['0100011', 'S'],
    'beq': ['1100011', 'B'],
    'bne': ['1100011', 'B'],
    'blt': ['1100011', 'B'],
    'bge': ['1100011', 'B'],
    'bltu': ['1100011', 'B'],
    'bgeu': ['1100011', 'B'],
    'lui': ['0110111', 'U'],
    'auipc': ['0010111', 'U'],
    'jal': ['1101111', 'J'],
    'hlt': ['1111111', 'H'],
}

opcodeType = {
    'R': ['add', 'sub', 'sll', 'slt', 'sltu', 'xor', 'srl', 'or', 'and'],
    'I': ['lw', 'addi', 'sltiu', 'jalr'],
    'S': ['sw'],
    'B': ['beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu'],
    'U': ['lui', 'auipc'],
    'J': ['jal'],
    'H': ['hlt'],
}

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

def find_opcode(opcode):
    opcude_list = {
        'add': ['0110011', 'R'],
        'sub': ['0110011', 'R'],
        'sll': ['0110011', 'R'],
        'slt': ['0110011', 'R'],
        'sltu': ['0110011', 'R'],
        'xor': ['0110011', 'R'],
        'srl': ['0110011', 'R'],
        'or': ['0110011', 'R'],
        'and': ['0110011', 'R'],
        'lw': ['0000011', 'I'],
        'addi': ['0010011', 'I'],
        'sltiu': ['0010011', 'I'],
        'jalr': ['1100111', 'I'],
        'sw': ['0100011', 'S'],
        'beq': ['1100011', 'B'],
        'bne': ['1100011', 'B'],
        'blt': ['1100011', 'B'],
        'bge': ['1100011', 'B'],
        'bltu': ['1100011', 'B'],
        'bgeu': ['1100011', 'B'],
        'lui': ['0110111', 'U'],
        'auipc': ['0010111', 'U'],
        'jal': ['1101111', 'J'],
        'hlt': ['1111111', 'H'],
    }
    
    if opcode in opcude_list:
        return opcude_list[opcode]

def assemble(input_file, output_file):
    with open(input_file, 'r') as file:
        assembly_code = file.readlines()

    binary_code = []

    for line_number, line in enumerate(assembly_code, start=1):
        line = line.strip()
        
        command_list = []
        opcode, operands = line.split()
        operands = operands.split(',')
        command_list.append(opcode)
        command_list.extend(operands)
        print(command_list)
        
        opcode_info = find_opcode(opcode) # check for valid opcode
        print(opcode_info)
        if opcode_info is None:
            error_message = f"Invalid opcode '{opcode}' at line {line_number}"
            with open(output_file, 'w') as file:
                file.write(error_message)
            return

        opcode_binary, opcode_type = opcode_info
        command_list.append(opcode_type)

        # Process each operand and convert it to binary code
        operand_binary = []
        for operand, operand_type in zip(operands, opcode_type):
            if operand_type == 'R':
                # Register operand
                if operand not in registers:
                    error_message = f"Invalid register '{operand}' at line {line_number}"
                    with open(output_file, 'w') as file:
                        file.write(error_message)
                    return
                operand_binary.append(registers[operand])
            elif operand_type == 'I':
                # Immediate operand
                try:
                    operand_binary.append(format(int(operand), '012b'))
                except ValueError:
                    error_message = f"Invalid immediate value '{operand}' at line {line_number}"
                    with open(output_file, 'w') as file:
                        file.write(error_message)
                    return
            elif operand_type == 'S':
                # Store operand
                if operand.count('(') != 1 or operand.count(')') != 1:
                    error_message = f"Invalid store operand '{operand}' at line {line_number}"
                    with open(output_file, 'w') as file:
                        file.write(error_message)
                    return
                offset, base_register = operand.strip(')').split('(')
                offset = int(offset)
                if base_register not in registers:
                    error_message = f"Invalid register '{base_register}' at line {line_number}"
                    with open(output_file, 'w') as file:
                        file.write(error_message)
                    return
                base_register_binary = registers[base_register]
                offset_binary = format(offset, '012b')
                operand_binary.append(offset_binary + base_register_binary)
            elif operand_type == 'B':
                # Branch operand
                if len(operands) != 3:
                    error_message = f"Invalid number of operands for opcode '{opcode}' at line {line_number}"
                    with open(output_file, 'w') as file:
                        file.write(error_message)
                    return
                rs1, rs2, label = operands
                labels = {}  # Add this line to initialize the 'labels' variable

                if rs1 not in registers:
                    error_message = f"Invalid register '{rs1}' at line {line_number}"
                    with open(output_file, 'w') as file:
                        file.write(error_message)
                    return
                if rs2 not in registers:
                    error_message = f"Invalid register '{rs2}' at line {line_number}"
                    with open(output_file, 'w') as file:
                        file.write(error_message)
                    return
                if label not in labels:
                    error_message = f"Invalid label '{label}' at line {line_number}"
                    with open(output_file, 'w') as file:
                        file.write(error_message)
                    return
                rs1_binary = registers[rs1]
                rs2_binary = registers[rs2]
                if labels:
                    label_binary = format(labels[label] - line_number, '013b')
                else:
                    label_binary = '0000000000000'  # Default value if labels is empty
                operand_binary.append(rs1_binary + rs2_binary + label_binary)
            elif operand_type == 'U':
                # Upper immediate operand
                if len(operands) != 2:
                    error_message = f"Invalid number of operands for opcode '{opcode}' at line {line_number}"
                    with open(output_file, 'w') as file:
                        file.write(error_message)
                    return
                rd, immediate = operands
                if rd not in registers:
                    error_message = f"Invalid register '{rd}' at line {line_number}"
                    with open(output_file, 'w') as file:
                        file.write(error_message)
                    return
                try:
                    immediate = int(immediate)
                except ValueError:
                    error_message = f"Invalid immediate value '{immediate}' at line {line_number}"
                    with open(output_file, 'w') as file:
                        file.write(error_message)
                    return
                rd_binary = registers[rd]
                immediate_binary = format(immediate, '020b')
                operand_binary.append(immediate_binary + rd_binary)
            elif operand_type == 'J':
                # Jump operand
                if len(operands) != 2:
                    error_message = f"Invalid number of operands for opcode '{opcode}' at line {line_number}"
                    with open(output_file, 'w') as file:
                        file.write(error_message)
                    return
                labels = {}  # Define the "labels" variable
                rd, label = operands
                if rd not in registers:
                    error_message = f"Invalid register '{rd}' at line {line_number}"
                    with open(output_file, 'w') as file:
                        file.write(error_message)
                    return
                if label not in labels:
                    error_message = f"Invalid label '{label}' at line {line_number}"
                    with open(output_file, 'w') as file:
                        file.write(error_message)
                    return
                rd_binary = registers[rd]
                label_binary = format(labels[label] - line_number, '020b')
                operand_binary.append(label_binary + rd_binary)
            elif operand_type == 'H':
                # Halt operand
                operand_binary.append('0' * 32)

        # Combine the opcode binary code and operand binary code
        print(opcode_binary, operand_binary)
        binary_code.append(opcode_binary + ''.join(operand_binary))
    
        

    # Write the binary code to output file
    with open(output_file, 'w') as file:
        file.write('\n'.join(binary_code))
        
# Test the assembler
assemble('assembly_code.txt', 'binary_code.txt')