"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 0b00001000 # binary 8
        self.ram = [0] * 0b100000000 # binary 256

        # INTERNAL REGISTERS
        self.pc = 0 # keeps address of currently executing instruction

        self.halted = False
        # self.IR = self.reg[self.PC]  # Copy of currently executing instruction

        # self.MAR = self.PC # HOLDS memory address we're reading/writing

        # self.MDR = self.IR # value to write or value just read

        # self.FL  = [0] * 0b00001000 # 8 bits

        # Registers External
        # self.IM = self.reg[6] # interrupt mask
        # self.IS = self.reg[7] # interrupt status
        # self.SP = self.reg[8] # stack pointer
        



    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
        
        # loop through ram 
        # while not self.halted:
        #     instruction = self.ram[self.PC]
            
        #     if instruction == PRN:
        #         print("ram", self.ram)
        #         print("")
        #         print("")
        #         print("reg", self.ram)
        #         self.PC += 1
            
        #     elif instruction == LDI:
        #         r_position = self.ram[self.PC + 1]
        #         reg_num = self.ram[self.PC + 2]

        #         self.reg[r_position] = reg_num
        #         self.PC += 3
            
        #     elif instruction == HLT:
        #         self.halted == True


        #     else:
        #         print(f"unknown instruction {instruction} at address {self.PC}")
        #         exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        # accept a value to write, and the address to write to
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        # needs to read the memory address stored in pc

        # store results in IR

        # needs: PC, IR, ram_read
        LDI = 0b10000010 # LDI R0,8
        PRN = 0b01000111 # PRN R0
        HLT = 0b00000001 # HLT



        while not self.halted:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            if IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            
            elif IR == HLT:
                self.halted = True
        
            else:
                print(f"unknown instruction {IR} at address {self.pc}")
                exit(1)
