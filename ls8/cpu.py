"""CPU functionality."""

import sys


LDI = 0b10000010 # LDI R0,8
PRN = 0b01000111 # PRN R0
HLT = 0b00000001 # HLT
MUL = 0b10100010 # MUL

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 0b00001000 # binary 8
        self.ram = [0] * 256 # binary 256
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        # INTERNAL REGISTERS
        self.pc = 0 # keeps address of currently executing instruction
        self.halted = False

        # self.FL  = [0] * 0b00001000 # 8 bits

        # Registers External
        # self.IM = self.reg[6] # interrupt mask
        # self.IS = self.reg[7] # interrupt status
        # self.SP = self.reg[8] # stack pointer

    def handle_HLT(self):
        self.halted = True
    
    def handle_LDI(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_PRN(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])
        self.pc += 2

    def handle_MUL(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3

    def load(self):
        """Load a program into memory."""

        address = 0
        # For now, we've just hardcoded a program:
        if len(sys.argv) <= 1:
            print("Please be more specific with your command line")
            exit(1)
        elif sys.argv[1].split("/")[1].strip() == '':
            print("Please be more specific with your command line")
            exit(1)
        with open(sys.argv[1]) as f:
            for line in f:
                # split defines where you want to "split" the line
                # strip eliminates white space
                string_val = line.split("#")[0].strip()
                if string_val == '': 
                    continue
                # value must be integer and binary
                value = int(string_val, 2)
                # index = address, value = binary integer
                self.ram[address] = value
                address += 1
        

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # used to handle all math equations
        # reg_a == first num
        # reg_b == second num
        # op    == operation

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
        # LDI = 0b10000010 # LDI R0,8
        # PRN = 0b01000111 # PRN R0
        # HLT = 0b00000001 # HLT
        # MUL = 0b10100010 # MUL
        
        while not self.halted:
            IR = self.ram_read(self.pc)

            if IR in self.branchtable:
                self.branchtable[IR]()
            else:
                print(f"unknown instruction {IR} at address {self.pc}")
                exit(1)

        
        
        
        
        # while not self.halted:
        #     IR = self.ram_read(self.pc)
        #     # memory 1 spot after current
        #     operand_a = self.ram_read(self.pc + 1)
        #     # memory 2 spots after current 
        #     operand_b = self.ram_read(self.pc + 2)
            

        #     if IR == LDI:
                # self.reg[operand_a] = operand_b
                # self.pc += 3
            
        #     elif IR == PRN:
        #         print(self.reg[operand_a])
        #         self.pc += 2
            
        #     elif IR == MUL:
                # self.alu("MUL", operand_a, operand_b)
                # self.pc += 3

        #     elif IR == HLT:
        #         self.halted = True
            # else:
            #     print(f"unknown instruction {IR} at address {self.pc}")
            #     exit(1)`

