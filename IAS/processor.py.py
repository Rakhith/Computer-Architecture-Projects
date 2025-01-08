#This is a processor which will calaculate the variance of first 5 consecutive 
#natural numbers...

import fileinput

file = "Machine.txt"
memory = [0]

for line in fileinput.input(file):
    bits = line[:40]
    memory.append(bits)

memory.extend([0] * (510 - len(memory)))
memory[500] = 0 #i=0 (For the first loop part of code)
memory[501] = 0 #this location stores mean
memory[502] = 5 #5 is stored here
memory[503] = 1 #j=0 (For the second loop part of code)
memory[504] = 0 #This location stores Variance
memory[505] = 0 #This location is a temporary place to store variance calculation
memory[506] = 6 #6 is stored here


class IAS_Machine():

    def __init__(self):
        self.true=0
        self.pc = 1
        self.ac = 0
        self.mar = ""
        self.mbr = ""
        self.ibr = ""
        self.ir = ""
        self.mq = 0
        self.alu = 0
    
    def preg(self,a):
        if (a<0):
            calculate_twos_complement = lambda n, bits=39: bin((2**bits + n) % 2**bits)[2:].zfill(bits)
            return calculate_twos_complement(a)
        else:
            return bin(a)[2:].zfill(40)

    def print_ac(self):
        if (self.ac<0):
            calculate_twos_complement = lambda n, bits=39: bin((2**bits + n) % 2**bits)[2:].zfill(bits)
            return calculate_twos_complement(self.ac)
        else:
            return bin(self.ac)[2:].zfill(40)

    def decode_execute(self):
        if (self.ir == "00000001"): #LOAD
            print("LOAD :")
            self.mbr = memory[int(self.mar, 2)]
            print(F"MBR <-- M({int(self.mar, 2)} :)",self.preg(self.mbr))
            self.ac = int(self.mbr) 
            print("AC <-- MBR :   ",self.preg(self.ac))
            self.mbr = str(bin(self.mbr)[2:].zfill(40))

        elif (self.ir == "00001010"): #LOADMQ
            print("LOAD MQ :")
            self.ac = self.mq
            print("AC <-- MQ : ",self.preg(self.ac))
            self.mq = 0
        
        elif (self.ir == "00100001"): #STOR
            print("STOR :")
            self.mbr = self.ac
            print("MBR <-- AC : ",self.preg(self.ac))
            memory[int(self.mar,2)] = self.mbr
            self.mbr = str(bin(self.mbr)[2:].zfill(40))
            print(f'M({int(self.mar,2)}) <-- MBR : ',self.mbr)

            

        elif (self.ir == "00001101"): #JUMPL
            print("JUMP L:")
            self.pc = int(self.mar,2)
            print(f"PC <-- {int(self.mar,2)} ")

            return 1
        
        elif (self.ir == "00001111"): #JUMP+
            print("JUMPL + :")
            if (self.ac >= 0):
                print(f"PC <-- MAR ",int(self.mar,2))
                self.pc = int(self.mar,2)

                return 1
            else:
                print("Condition not satisfied, so will continue:")
            
        elif (self.ir == "00000101"): #ADD
            print("ADD :")
            self.alu = self.ac
            print("ALU <-- AC : ",self.preg(self.ac))
            self.mbr = memory[int(self.mar,2)]
            print(f"MBR <-- M({int(self.mar,2)}) : ",self.preg(memory[int(self.mar,2)]))
            self.ac = self.mbr
            print(f'AC <-- MBR : ',self.preg(self.mbr))
            self.alu += memory[int(self.mar,2)]
            print(f'ALU <-- ALU + AC : ',self.preg(self.alu))
            self.ac = self.alu
            print(f'AC <-- ALU : ',self.preg(self.ac))

        
        elif (self.ir == "00000110"): #SUB
            print("SUB :")
            self.alu = self.ac
            print("ALU <-- AC : ",self.preg(self.ac))
            self.mbr = memory[int(self.mar,2)]
            print(f"MBR <-- M({int(self.mar,2)}) : ",self.preg(memory[int(self.mar,2)]))
            self.ac = self.mbr
            print(f'AC <-- MBR : ',self.preg(self.mbr))
            self.alu -= memory[int(self.mar,2)]
            print(f'ALU <-- ALU - AC : ',self.preg(self.alu))
            self.ac = self.alu
            print(f'AC <-- ALU : ',self.preg(self.ac))


        elif (self.ir == "11000000"): #INC
            print("INC :")
            print(f'MBR <-- M({int(self.mar,2)}) : ',self.preg(memory[int(self.mar,2)]))
            self.ac = memory[int(self.mar,2)]
            print("AC <-- MBR : ",self.preg(self.ac))
            self.alu = self.ac
            print("ALU <-- AC : ",self.preg(self.ac))
            self.alu += 1
            print(f'ALU <-- ALU + 1 : ',self.preg(self.alu))
            self.ac = self.alu
            print(f'AC <-- ALU : ',self.preg(self.ac))

        
        elif (self.ir == "00001100"): #DIV
            print("DIV :")
            self.mbr = memory[int(self.mar,2)]
            print(f'MBR <-- M({int(self.mar,2)}) : ',self.preg(memory[int(self.mar,2)]))
            print(f'ALU <-- AC : {self.ac}')
            print("ALU <-- MBR : ",self.preg(self.mbr))
            self.alu =int(self.ac / self.mbr)
            print(f'MQ <-- AC / M(X)  : ',self.preg(self.alu))
            self.mq = self.alu

        
        elif (self.ir == "10000000" ): #SQR
            print("SQR :")
            print(f'MBR <-- M({int(self.mar,2)}) : ',self.preg(memory[int(self.mar,2)]))
            self.ac = memory[int(self.mar,2)]
            print("AC <-- MBR : ",self.preg(self.ac))
            self.alu = self.ac
            print("ALU <-- AC : ",self.preg(self.ac))
            self.alu = self.alu * self.alu
            print(f'ALU <-- ALU * ALU : ',self.preg(self.alu))
            self.ac = self.alu
            print(f'AC <-- ALU : ',self.preg(self.ac))

        elif (self.ir == "11100000"): #NOP
            print("NOP :")
            self.pc+=0

        elif (self.ir == "10101010"): #EXIT
            print("EXIT :")
            print("The program will now exit.")
            self.true=0
            return 1


    def fetch(self,memory):
        self.true = 1
        while (self.true):
            for i in range (2):
                if (i%2==0):
                    print("After fetching the instructions, the registers contain as follows:")
                    print("PC :",self.pc)
                    self.mar = self.pc
                    print("MAR <-- PC :",self.mar)
                    self.mbr = memory[self.mar]
                    print("MBR <-- M[MAR] :",self.mbr)
                    self.ibr = self.mbr[20:40]
                    print("IBR <-- MBR[20:39] : ",self.ibr)
                    self.ir = self.mbr[0:8]
                    print("IR <-- MBR[0:7] : ",self.ir)
                    self.mar = self.mbr[8:20]
                    print("MAR <-- MBR[8:19] : ",self.mar)

                    
                    print("-"*72)
                    

                elif (i%2==1):
                    print("After fetching the right instructions, the registers contain as follows:")
                    self.ir = self.ibr[0:8]
                    print("IR <-- IBR[0:7] : ",self.ir)
                    self.mar = self.ibr[8:20]
                    print("MAR <-- IBR[8:19] : ",self.mar)
                    self.pc = self.pc + 1
                    print("PC <-- PC + 1 :",self.pc)
                    self.ibr = ""
                    self.mbr=""
                    print("-"*72)

                if (self.decode_execute() == 1 ):
                    print("-"*72)
                    break   
                print("-"*72)
                
        print("The variance of the first 5 natural numbers is:",memory[504])
variance = IAS_Machine()

variance.fetch(memory)