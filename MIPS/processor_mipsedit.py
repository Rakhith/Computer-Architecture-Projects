reg_file = [0]*32
'''data_mean = {  # Initialize data memory with key-value pairs representing addresses and values
    0 : 1000,
    4 : 2400,
    8 : 2600,
    12 : 5,
    16 : 2000,
    20 : 2000
}'''
instr_mem_actual_1=[]
instr_mem_actual_2=[]
instr_mem_actual_3=[]

'''instruction_mem = {  # Initialize instruction memory with key-value pairs representing addresses and binary instructions
4000384 : '10001100000010000000000000000000',
4000388 : '10001100000010010000000000000100',
4000392 : '10001100000010100000000000001000',
4000396 : '10001100000010110000000000010000',    #mean
4000400 : '10001100000011010000000000010100',
4000404 : '00000001000010010100000000100000',
4000408 : '00000001000010100100000000100000',
4000412 : '00000001000010110100000000100000',
4000416 : '00000001000011010100000000100000',
4000420 : '10001100000011000000000000001100',
4000424 : '00000001000011000100000000011010'
}
for key in instruction_mem:
    instr_mem_actual_1.append(str(instruction_mem[key][0:8]))
    instr_mem_actual_1.append(str(instruction_mem[key][8:16]))
    instr_mem_actual_1.append(str(instruction_mem[key][16:24]))
    instr_mem_actual_1.append(str(instruction_mem[key][24:32]))
print("Instruction Memory:", instr_mem_actual_1)'''
    

instruction_mem =   {4000320:'00000001001010100110000000100000',   #fib
                     4000324:'00000000000010100100100000100000',
                     4000328:'00000000000011000101000000100000',
                     4000332:'00100001011010110000000000000001',
                     4000336:'00010101011010001111111111111011'}
for key in instruction_mem:
    instr_mem_actual_2.append(str(instruction_mem[key][0:8]))
    instr_mem_actual_2.append(str(instruction_mem[key][8:16]))
    instr_mem_actual_2.append(str(instruction_mem[key][16:24]))
    instr_mem_actual_2.append(str(instruction_mem[key][24:32]))
print("Instruction Memory:", instr_mem_actual_2)


'''instruction_mem = {
4000340 : '00000001000010010100100000000010',   #power
4000344 : '00100001011010110000000000000001',
4000348 : '00010101010010111111111111111101'
                }
for key in instruction_mem:
    instr_mem_actual_3.append(str(instruction_mem[key][0:8]))
    instr_mem_actual_3.append(str(instruction_mem[key][8:16]))
    instr_mem_actual_3.append(str(instruction_mem[key][16:24]))
    instr_mem_actual_3.append(str(instruction_mem[key][24:32]))
print("Instruction Memory:", instr_mem_actual_3)'''

class Instruction:  
    def __init__(self):
        self.opcode = ""  # Defining type of inst and initialising the control lines
        self.rd = ""
        self.rs = ""
        self.rt = ""
        self.imm = ""
        self.funct = ""
        self.shamt = ""
        self.regDst = 0
        self.regWr = 0
        self.AluSrc = 0
        self.MemWr = 0
        self.MemRd = 0
        self.MemToReg = 0
        self.jump = 0
        self.branch = 0
        self.rs_val = 0
        self.rt_val = 0


def twos_complement(bin_str):
    if bin_str[0] == '1':
        complement = ''.join('1' if bit == '0' else '0' for bit in bin_str[1:])
        return -int(complement, 2) - 1
    else:
        return int(bin_str, 2)
    
def Inst_Fetch(pc): 
    return instruction_mem[pc]

def Inst_Decode(inst): # setting the control lines for ALU here
    i = Instruction()
    i.opcode = inst[0:6]
    i.rd = int(inst[16:21],2)
    i.rs = int(inst[6:11],2)
    i.rt = int(inst[11:16], 2)
    i.rs_val = reg_file[int(inst[6:11],2)]
    i.rt_val = reg_file[int(inst[11:16],2)]
    if i.opcode == '000000': 
        i.funct = inst[26:32]
        i.shamt = int(inst[21:26],2)
        i.regWr = 1
    elif i.opcode == "000010" or i.opcode == "000011": #jump
        i.jump = 1
        i.imm = int("0000" + inst[6:32] + "00", 2)
    else:
        i.rd = int(inst[11:16], 2)
        i.imm = twos_complement(inst[16:32])
        i.regDst = 1
        if i.opcode == "100011": #load word
            i.MemRd = 1
            i.MemToReg = 1
            i.AluSrc = 1
            i.regWr = 1
        elif i.opcode == "101011": #store word
            i.AluSrc = 1
            i.MemWr = 1
        elif i.opcode == "000100" or i.opcode == "000101": #branch
            if i.opcode == "000100" and i.rs_val == i.rt_val: #beq
                i.branch = 1
            elif i.opcode == "000101" and i.rs_val != i.rt_val: #bne
                i.branch = 1
        else:
            i.regWr = 1
            i.AluSrc = 1
    return i

def execute(i,inst):
    source1 = i.rs_val
    source2 = i.rt_val
    if i.AluSrc:
        source2 = i.imm
    ALU_op = 0 #add, addi, li
    if i.opcode == "000000" and i.funct == "101010": #slt
        ALU_op = 1
    if i.opcode == "000000" and i.funct == "011010": #div
        ALU_op = 2
    if i.opcode == "000000" and i.funct == "000000": #shift
        ALU_op = 3
    if i.opcode == "000000" and i.funct == "000010": #mul
        ALU_op = 4
    if ALU_op == 0:    #ALU working
        return int(source1 + source2)
    elif ALU_op == 1:
        return int(source1 < source2)
    elif ALU_op == 2:
        return int(source1/source2)
    elif ALU_op == 3:
        return i.rs << i.shamt
    elif ALU_op == 4:
        return source1 * source2
def mem_access(i, address):
    if i.MemWr == 1:
        data_mean[address] = instruction.rt_val
    elif i.MemRd == 1:
        return data_mean[address]
    
def write_back(i, mem_val, alu_out): 
    if i.regWr :
        if i.MemToReg:
            reg_file[i.rd] = mem_val
        else :
            reg_file[i.rd] = alu_out


def execute_processor(): 
    pc = min(instruction_mem.keys())   #pc becomes min of keys defined ie start of instruction

    while pc in instruction_mem:
        inst = Inst_Fetch(pc)
        ID = Inst_Decode(inst)
        alu_out = execute(ID,inst)
        mem_val = mem_access(ID, alu_out)
        write_back(ID, mem_val, alu_out)
        pc += 4  
        if ID.branch:
            pc += (4 * ID.imm)
        elif ID.jump:
            pc = ID.imm
        
'''print('For code 1 - Finding power:')
reg_file[8] = 2 #base
reg_file[10] = 10 #expo
reg_file[9] = 1  # result
reg_file[11] = 0
execute_processor()
print("Base:", reg_file[8])
print("Exponent:", reg_file[10])
print("Reg file:", reg_file)
print("Result:", reg_file[9])'''

print('For code 2 - Fibonacci Series:')
reg_file[8] = 10
reg_file[9] = 0
reg_file[10] = 1
reg_file[11] = 0
execute_processor()
print("Input:", reg_file[8])
print("Reg file:", reg_file)
print("Result:", reg_file[9])

'''print('For code 3 - Finding mean:')
execute_processor()
print("Input:", data_mean.values())
print("Reg file:", reg_file)
print("Result:", reg_file[8])'''

