"""CPU functionality."""

import sys


LDI = 0b10000010 # LDI R0,8
PRN = 0b01000111 # PRN R0
HLT = 0b00000001 # HLT
MUL = 0b10100010 # MUL
PUSH = 0b01000101
POP = 0b01000110
ADD = 0b10100000
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JEQ = 0b01010101
JMP = 0b01010100
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 0b00001000 # binary 8
        self.ram = [0] * 256 # binary 256
        self.pc = 0 # keeps address of currently executing instruction
        self.halted = False # controls run
        # Branch Table
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[JMP] = self.handle_JMP
        # Stack Work
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET
        # ALU
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JNE] = self.handle_JNE

        # Stack Information
        self.sp = 7 # stack pointer, only for the stack
        self.reg[self.sp] = 0xF4 # Start at f4 aka 244
        # Flags
        self.FL  = 5 # flag pointer in reg
        self.reg[self.FL] = 0 # Starts at 0 in reg, will adjust binary depending on CMP
        # Registers External
        # self.IM = self.reg[6] # interrupt mask
        # self.IS = self.reg[7] # interrupt status

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        # accept a value to write, and the address to write to
        self.ram[MAR] = MDR
       
    def handle_HLT(self):
        self.halted = True

    def handle_CALL(self):
        # make copy of address to return to
        operand_a = self.ram_read(self.pc + 1) # 00000000
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.pc + 2
        self.pc = self.reg[operand_a]


    def handle_RET(self):
        pop_stack = self.ram[self.reg[self.sp]]
        self.pc = pop_stack
        self.reg[self.sp] += 1

    def handle_LDI(self):
        operand_a = self.ram_read(self.pc + 1) # 00000000
        operand_b = self.ram_read(self.pc + 2) # 00000001
        self.reg[operand_a] = operand_b
        # self.pc += 3

    def handle_PRN(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])
        # self.pc += 2
        
    def handle_CMP(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("CMP", operand_a, operand_b)
 
    def handle_MUL(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("MUL", operand_a, operand_b)
        # self.pc += 3

    def handle_ADD(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("ADD", operand_a, operand_b)
        # self.pc += 3
    
    def handle_JEQ(self):
        operand_a = self.ram_read(self.pc + 1)
        if self.reg[self.FL] == 0b00000001:
            self.pc = self.reg[operand_a]
        else:
            # print("REG", self.reg)
            # print("ram", self.ram)
            # print("PC ", self.pc)
            # print("op_a", operand_a)
            self.pc += 2

    def handle_JNE(self):
        operand_a = self.ram_read(self.pc + 1)
        # print("operand", operand)
        # print("OP A", operand_a)
        # print("REG", self.reg)
        # print(self.pc)
        if self.reg[self.FL] != 0b00000001:
            # print(self.reg[self.pc])
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def handle_JMP(self):
        operand_a = self.ram_read(self.pc + 1)
        self.pc = self.reg[operand_a]


    def handle_push(self):
        # operand_a is the next available spot
        operand_a = self.ram_read(self.pc + 1)
        # Decrement Value of the Stack Pointer
            # REG[7] == 0, After == -1 
        self.reg[self.sp] -= 1
        # stores value of reg @ sp into the ram, stores the next spot AT BACK OF RAM 
            # reg [0, 1, 2, 3, 4, 5, 6, 7]
            # ram [0, 0, 0, 0, 0, 0...]
            # PUSH --- num after ---> 28
            # ram[-1] == value after push is called
            # ram [0, 0, 0, 0, 0, 0... 28] --> stack starts at 28
        """
        Process
            # print("TOP OF STACK ADDRESS", self.reg[self.sp])
            # print("Ram Current Value", self.ram[self.reg[self.sp]])
            # print("Replacement Value", operand_a)
        """
        copy_reg = self.reg[operand_a]
        self.ram[self.reg[self.sp]] = copy_reg
        # moves address 2 spots
        # self.pc += 2
        

    def handle_pop(self):
        # Retrieve value from RAM @ SP
        operand_a = self.ram_read(self.pc + 1)

        copy = self.ram[self.reg[self.sp]]

        self.reg[operand_a] = copy
       
        self.reg[self.sp] += 1

        

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
        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] > self.reg[reg_b]:
                self.reg[self.FL] = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.reg[self.FL] = 0b00000100
            else:
                self.reg[self.FL] = 0b00000001
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b] 
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


    def run(self):
        """Run the CPU."""
        # needs to read the memory address stored in pc

        # store results in IR

        # needs: PC, IR, ram_read
        while not self.halted:
            IR = self.ram_read(self.pc)
            # print('IR', IR)

            if IR in self.branchtable:
                self.branchtable[IR]()
                if (IR & 0b00010000) >> 4 == 0:
                    self.pc += (IR >> 6) + 1
            else:
                print(f"unknown instruction {IR} at address {self.pc}")
                exit(1)

        """

        IF/ELSE STATEMENTS BELOW

        """
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

