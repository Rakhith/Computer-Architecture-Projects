import fileinput

file = "Assembly.txt"
line_list = []


for i in fileinput.input(file):
    line_list.append(i.split())


optcode_dict = {
    'LOAD':'00000001',
    'LOADMQ':'00001010',
    'STOR':'00100001',
    'SUB':'00000110',
    'ADD':'00000101',
    'JUMPL+':'00001111',
    'JUMPL':'00001101',
    'DIV':'00001100',
    'SQR':'10000000',
    'INC':'11000000',
    'NOP':'11100000',
    'EXIT':'10101010'
}


for i in line_list:
    if ((len(i) == 1) and type(i[0][0]).isdecimal):
        if (int(i[0]) >= 0):
            i[0] = bin(int(i[0]))[2:].zfill(40)
        else:
            mod_val = abs(int(i[0]))
            bin_mod_val = bin(mod_val)[2:].zfill(40)
            inverted_bin_mod_val = ''.join('1' if bit == '0' else '0' for bit in bin_mod_val)
            i[0] = bin(int(inverted_bin_mod_val,2)+1)[2:].zfill(40)
    

    else:
        for j in range(len(i)):
            if (i[j].isdecimal()):
                i[j]=bin(int(i[j]))[2:].zfill(12)
            else:
                i[j] = optcode_dict[i[j]]


file = open('Machine.txt','w')
for item in line_list:
    file.write("".join(item))
    file.write("\n")
file.close()