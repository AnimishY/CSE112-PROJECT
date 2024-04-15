import sys

# Memory sizes and addressing
PROGRAM_MEMORY_SIZE = 256  # 256 bytes
PROGRAM_MEMORY_START = 0x0000_0000
PROGRAM_MEMORY_END = 0x0000_00FF

STACK_MEMORY_SIZE = 128  # 128 bytes 
STACK_MEMORY_START = 0x0000_0100
STACK_MEMORY_END = 0x0000_017F

DATA_MEMORY_SIZE = 128  # 128 bytes
DATA_MEMORY_START = 0x0001_0000 
DATA_MEMORY_END = 0x0001_007F

# Register names and addresses
REGISTER_NAMES = ['zero', 'ra', 'sp', 'gp', 'tp', 't0', 't1', 't2', 's0', 's1', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 't3', 't4', 't5', 't6']
REGISTER_ADDRESSES = [0b00000, 0b00001, 0b00010, 0b00011, 0b00100, 0b00101, 0b00110, 0b00111, 0b01000, 0b01001, 0b01010, 0b01011, 0b01100, 0b01101, 0b01110, 0b01111, 0b10000, 0b10001, 0b10010, 0b10011, 0b10100, 0b10101, 0b10110, 0b10111, 0b11000, 0b11001, 0b11010, 0b11011, 0b11100, 0b11101, 0b11110, 0b11111]

class RISCVSimulator:
    def __init__(self, binary_file, output_file):
        self.binary_file = binary_file
        self.output_file = output_file
        self.program_counter = PROGRAM_MEMORY_START
        self.registers = [0] * 32
        self.program_memory = [0] * (PROGRAM_MEMORY_SIZE // 4)
        self.stack_memory = [0] * (STACK_MEMORY_SIZE // 4)
        self.data_memory = [0] * (DATA_MEMORY_SIZE // 4)

        self.load_program()

    def load_program(self):
        with open(self.binary_file, 'r') as f:
            for i, line in enumerate(f):
                self.program_memory[i] = int(line.strip(), 2)

    def print_register_values(self):
        with open(self.output_file, 'a') as f:
            f.write(f"{self.program_counter:08X} {' '.join(f'{reg:08X}' for reg in self.registers)}\n")

    def print_memory_contents(self):
        with open(self.output_file, 'a') as f:
            for addr in range(PROGRAM_MEMORY_START, PROGRAM_MEMORY_END + 1, 4):
                f.write(f"{self.program_memory[(addr - PROGRAM_MEMORY_START) // 4]:08b}\n")
            for addr in range(STACK_MEMORY_START, STACK_MEMORY_END + 1, 4):
                f.write(f"{self.stack_memory[(addr - STACK_MEMORY_START) // 4]:08b}\n")
            for addr in range(DATA_MEMORY_START, DATA_MEMORY_END + 1, 4):
                f.write(f"{self.data_memory[(addr - DATA_MEMORY_START) // 4]:08b}\n")

    def execute_instruction(self, instruction):
        opcode = instruction & 0b1111111
        funct3 = (instruction >> 12) & 0b111
        funct7 = (instruction >> 25) & 0b1111111

        # Decode and execute the instruction
        if opcode == 0b0110011:  # R-type instructions
            rs1 = (instruction >> 15) & 0b11111
            rs2 = (instruction >> 20) & 0b11111
            rd = (instruction >> 7) & 0b11111

            if funct3 == 0b000:
                if funct7 == 0b0000000:
                    self.registers[rd] = self.registers[rs1] + self.registers[rs2]  # add
                elif funct7 == 0b0100000:
                    self.registers[rd] = self.registers[rs1] - self.registers[rs2]  # sub
            elif funct3 == 0b001:
                self.registers[rd] = self.registers[rs1] << (self.registers[rs2] & 0b11111)  # sll
            elif funct3 == 0b010:
                self.registers[rd] = 1 if self.registers[rs1] < self.registers[rs2] else 0  # slt
            elif funct3 == 0b011:
                self.registers[rd] = 1 if self.registers[rs1] < self.registers[rs2] else 0  # sltu
            elif funct3 == 0b100:
                self.registers[rd] = self.registers[rs1] ^ self.registers[rs2]  # xor
            elif funct3 == 0b101:
                if funct7 == 0b0000000:
                    self.registers[rd] = self.registers[rs1] >> (self.registers[rs2] & 0b11111)  # srl
            elif funct3 == 0b110:
                self.registers[rd] = self.registers[rs1] | self.registers[rs2]  # or
            elif funct3 == 0b111:
                self.registers[rd] = self.registers[rs1] & self.registers[rs2]  # and
            elif funct3 == 0b000 and funct7 == 0b0000001:
                self.registers[rd] = self.registers[rs1] * self.registers[rs2]  # mul (bonus)

        elif opcode == 0b0000011:  # I-type instructions
            rs1 = (instruction >> 15) & 0b11111
            rd = (instruction >> 7) & 0b11111
            imm = (instruction >> 20) & 0b111111111111

            if funct3 == 0b010:
                self.registers[rd] = self.load_word(self.registers[rs1] + imm)  # lw
            elif funct3 == 0b000:
                self.registers[rd] = self.registers[rs1] + imm  # addi
            elif funct3 == 0b011:
                self.registers[rd] = 1 if self.registers[rs1] < imm else 0  # sltiu
            elif funct3 == 0b000:
                self.program_counter = (self.registers[rs1] + imm) & ~1  # jalr

        elif opcode == 0b0100011:  # S-type instructions
            rs1 = (instruction >> 15) & 0b11111
            rs2 = (instruction >> 20) & 0b11111
            imm = ((instruction >> 25) << 5) | ((instruction >> 7) & 0b11111)
            address = self.registers[rs1] + imm

            if funct3 == 0b010:
                self.store_word(address, self.registers[rs2])  # sw

        elif opcode == 0b1100011:  # B-type instructions
            rs1 = (instruction >> 15) & 0b11111
            rs2 = (instruction >> 20) & 0b11111
            imm = ((instruction >> 31) << 12) | ((instruction >> 25) << 5) | ((instruction >> 8) & 0b1110) | ((instruction >> 7) & 0b1)

            if funct3 == 0b000:
                if self.registers[rs1] == self.registers[rs2]:
                    self.program_counter = self.program_counter + imm  # beq
            elif funct3 == 0b001:
                if self.registers[rs1] != self.registers[rs2]:
                    self.program_counter = self.program_counter + imm  # bne
            elif funct3 == 0b100:
                if self.registers[rs1] < self.registers[rs2]:
                    self.program_counter = self.program_counter + imm  # blt
            elif funct3 == 0b101:
                if self.registers[rs1] >= self.registers[rs2]:
                    self.program_counter = self.program_counter + imm  # bge
            elif funct3 == 0b110:
                if self.registers[rs1] < self.registers[rs2]:
                    self.program_counter = self.program_counter + imm  # bltu
            elif funct3 == 0b111:
                if self.registers[rs1] >= self.registers[rs2]:
                    self.program_counter = self.program_counter + imm  # bgeu

        elif opcode == 0b0010111:  # U-type instructions
            rd = (instruction >> 7) & 0b11111
            imm = (instruction >> 12) << 12
            self.registers[rd] = self.program_counter + imm  # auipc

        elif opcode == 0b0110111:  # U-type instructions
            rd = (instruction >> 7) & 0b11111
            imm = (instruction >> 12) << 12
            self.registers[rd] = imm  # lui

        elif opcode == 0b1101111:  # J-type instructions
            rd = (instruction >> 7) & 0b11111
            imm = ((instruction >> 31) << 20) | ((instruction >> 21) << 1) | ((instruction >> 20) & 0b1) | ((instruction >> 12) << 12)
            self.registers[rd] = self.program_counter + 4
            self.program_counter = self.program_counter + imm

        elif opcode == 0b0001011:  # Bonus instructions
            rs1 = (instruction >> 15) & 0b11111
            rd = (instruction >> 7) & 0b11111
            if funct3 == 0b000:
                for i in range(32):
                    self.registers[i] = 0  # rst (bonus)
            elif funct3 == 0b001:
                value = self.registers[rs1]
                self.registers[rd] = 0
                for i in range(32):
                    if value & (1 << i):
                        self.registers[rd] |= (1 << (31 - i))  # rvrs (bonus)
            elif funct3 == 0b010:
                self.program_counter = self.program_counter  # halt (bonus)
        else:
            raise ValueError(f"Unsupported instruction: {instruction:08X}")

        self.program_counter += 4

    def load_word(self, address):
        if address >= PROGRAM_MEMORY_START and address <= PROGRAM_MEMORY_END:
            index = (address - PROGRAM_MEMORY_START) // 4
            return self.program_memory[index]
        elif address >= STACK_MEMORY_START and address <= STACK_MEMORY_END:
            index = (address - STACK_MEMORY_START) // 4
            return self.stack_memory[index]
        elif address >= DATA_MEMORY_START and address <= DATA_MEMORY_END:
            index = (address - DATA_MEMORY_START) // 4
            return self.data_memory[index]
        else:
            raise ValueError(f"Invalid memory address: {address:08X}")

    def store_word(self, address, value):
        if address >= STACK_MEMORY_START and address <= STACK_MEMORY_END:
            index = (address - STACK_MEMORY_START) // 4
            self.stack_memory[index] = value
        elif address >= DATA_MEMORY_START and address <= DATA_MEMORY_END:
            index = (address - DATA_MEMORY_START) // 4
            self.data_memory[index] = value
        else:
            raise ValueError(f"Invalid memory address: {address:08X}")

    def run(self):
        while True:
            instruction = self.program_memory[self.program_counter // 4]
            self.execute_instruction(instruction)
            self.print_register_values()

            if (self.program_counter == PROGRAM_MEMORY_END + 4) and (instruction & 0b1111111 == 0b1100011) and ((instruction >> 12) & 0b111 == 0b000) and ((instruction >> 15) & 0b11111 == 0) and ((instruction >> 20) & 0b11111 == 0):
                self.print_memory_contents()
                break

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python simulator.py <input_binary_file> <output_file>")
        sys.exit(1)

    binary_file = sys.argv[1]
    output_file = sys.argv[2]

    simulator = RISCVSimulator(binary_file, output_file)
    simulator.run()