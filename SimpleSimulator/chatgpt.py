import sys


class Simulator:
    def __init__(self):
        # Initialize registers
        self.registers = {
            "zero": 0, "ra": 0, "sp": 0, "gp": 0, "tp": 0,
            "t0": 0, "t1": 0, "t2": 0, "s0": 0, "s1": 0,
            "a0": 0, "a1": 0, "a2": 0, "a3": 0, "a4": 0,
            "a5": 0, "a6": 0, "a7": 0, "s2": 0, "s3": 0,
            "s4": 0, "s5": 0, "s6": 0, "s7": 0, "s8": 0,
            "s9": 0, "s10": 0, "s11": 0, "t3": 0, "t4": 0,
            "t5": 0, "t6": 0
        }
        self.registers_by_number = {
            i: reg for i, reg in enumerate(self.registers)}
        self.pc = 0  # Program counter
        self.memory = [0] * 32  # Memory initialized with zeros

    def execute_instruction(self, instruction):
        opcode = instruction[:7]
        rs1 = int(instruction[7:12], 2)
        rs2 = int(instruction[12:17], 2)
        rd = int(instruction[20:25], 2)
        imm = int(instruction[17:], 2) if instruction[0] == '1' else int(
            instruction[17:], 2) - 2 ** 12

        if opcode == '0110011':  # R-Type Instructions
            funct3 = instruction[17:20]
            funct7 = instruction[:7]

            if funct7 == '0000000':
                if funct3 == '000':
                    self.registers[self.registers_by_number[rd]] = self.registers[self.registers_by_number[rs1]
                        ] + self.registers[self.registers_by_number[rs2]]
                elif funct3 == '001':
                    self.registers[self.registers_by_number[rd]] = self.registers[self.registers_by_number[rs1]
                        ] << self.registers[self.registers_by_number[rs2]]
                elif funct3 == '010':
                    self.registers[self.registers_by_number[rd]] = self.registers[self.registers_by_number[rs1]
                        ] < self.registers[self.registers_by_number[rs2]]
                elif funct3 == '011':
                    self.registers[self.registers_by_number[rd]] = self.registers[self.registers_by_number[rs1]
                        ] < self.registers[self.registers_by_number[rs2]]
                elif funct3 == '100':
                    self.registers[self.registers_by_number[rd]] = self.registers[self.registers_by_number[rs1]
                        ] ^ self.registers[self.registers_by_number[rs2]]
                elif funct3 == '101':
                    self.registers[self.registers_by_number[rd]] = self.registers[self.registers_by_number[rs1]
                        ] >> self.registers[self.registers_by_number[rs2]]
                elif funct3 == '110':
                    self.registers[self.registers_by_number[rd]] = self.registers[self.registers_by_number[rs1]
                        ] | self.registers[self.registers_by_number[rs2]]
                elif funct3 == '111':
                    self.registers[self.registers_by_number[rd]] = self.registers[self.registers_by_number[rs1]
                        ] & self.registers[self.registers_by_number[rs2]]
            elif funct7 == '0100000':
                self.registers[self.registers_by_number[rd]] = self.registers[self.registers_by_number[rs1]
                    ] - self.registers[self.registers_by_number[rs2]]

        elif opcode == '0000011':  # I-Type Instructions
            funct3 = instruction[17:20]

            if funct3 == '010':
                self.registers[self.registers_by_number[rd]
                    ] = self.memory[self.registers[self.registers_by_number[rs1]] + imm]
            elif funct3 == '000':
                self.registers[self.registers_by_number[rd]
                    ] = self.registers[self.registers_by_number[rs1]] + imm
            elif funct3 == '111':
                self.registers[self.registers_by_number[rd]
                    ] = self.registers[self.registers_by_number[rs1]] < imm

        elif opcode == '0100011':  # S-Type Instructions
            funct3 = instruction[17:20]
            imm = int(instruction[7:12] + instruction[20:25], 2)

            if funct3 == '010':
                self.memory[self.registers[self.registers_by_number[rs1]
                    ] + imm] = self.registers[self.registers_by_number[rs2]]

        elif opcode == '1100011':  # B-Type Instructions
            funct3 = instruction[17:20]
            imm = int(instruction[0] + instruction[24:25] +
                      instruction[1:7] + instruction[20:24], 2)

            if funct3 == '000':
                if self.registers[self.registers_by_number[rs1]] == self.registers[self.registers_by_number[rs2]]:
                    self.pc += imm
            elif funct3 == '001':
                if self.registers[self.registers_by_number[rs1]] != self.registers[self.registers_by_number[rs2]]:
                    self.pc += imm
            elif funct3 == '100':
                if self.registers[self.registers_by_number[rs1]] < self.registers[self.registers_by_number[rs2]]:
                    self.pc += imm
            elif funct3 == '101':
                if self.registers[self.registers_by_number[rs1]] >= self.registers[self.registers_by_number[rs2]]:
                    self.pc += imm
            elif funct3 == '110':
                if self.registers[self.registers_by_number[rs1]] < self.registers[self.registers_by_number[rs2]]:
                    self.pc += imm
            elif funct3 == '111':
                if self.registers[self.registers_by_number[rs1]] >= self.registers[self.registers_by_number[rs2]]:
                    self.pc += imm

        elif opcode == '0010111':  # U-Type Instructions
            self.registers[self.registers_by_number[rd]] = imm

        elif opcode == '0110111':  # U-Type Instructions
            self.registers[self.registers_by_number[rd]] = self.pc + imm

        # Increment Program Counter
        self.pc += 4


    def print_registers(self, output_file):
        # Print program counter in binary format
        pc_binary = format(self.pc, '032b')

        # Print register values in binary format
        register_values = [format(self.registers[reg], '032b')
                                  for reg in self.registers_by_number.values()]

        # Write program counter and register values to the output file
        output_file.write(f"{pc_binary} {' '.join(register_values)}\n")

    def print_memory(self, output_file):
        # Print memory contents to the output file
        for data in self.memory:
            output_file.write(f"{data}\n")

    def simulate(self, input_file, output_file):
        # Open input and output files
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                instruction = line.strip()
                self.execute_instruction(instruction)
                self.print_registers(outfile)

            # Print memory contents after virtual halt
            self.print_memory(outfile)
            print("Hello")


# Main function to run the simulator
def main():
    if len(sys.argv) != 3:
        print("Usage: python simulator.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Create and run the simulator
    simulator = Simulator()
    simulator.simulate(input_file, output_file)


if __name__ == "__main__":
    main()
