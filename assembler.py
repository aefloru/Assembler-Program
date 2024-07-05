import re

file = open('/Users/sasha/Desktop/School/csprojects/python/problem4/mycommands_example2', 'r')
read = file.readlines()

instruction_list = []

R_type_dict = {
    #op_name --> op_code, funct3, funct6/7
    'add': ('0110011', '000', '0000000'),
    'and': ('0110011', '111', '0000000'),
    'sll': ('0110011', '001', '0000000'),
    'srl': ('0110011', '101', '0000000'),
    'xor': ('0110011', '100', '0000000'),
    'mul': ('0110011', '000', '0000001')
}

I_type_dict = {
    #op_name --> op_code, funct3
    'slli': ('0010011', '001', '0000000'),
    'srli': ('0010011', '101', '0000000'),
    'addi': ('0010011', '000'),
    'ori': ('0010011', '110'),
    'andi': ('0010011', '111')
}

B_type_dict = {
    #op_name --> op_code, funct3
    'bne': ('1100011', '001'),
    'beq': ('1100011', '000')
}

register_mapping = {
    "a0": "x10",
    "a1": "x11",
    "a2": "x12",
    "a3": "x13",
    "a4": "x14",
    "a5": "x15",
    "a6": "x16",
    "a7": "x17",
    "t0": "x5",
    "t1": "x6",
    "t2": "x7",
    "t3": "x28",
    "t4": "x29",
    "t5": "x30",
    "t6": "x31",
    "s0": "x8",
    "s1": "x9",
    "s2": "x18",
    "s3": "x19",
    "s4": "x20",
    "s5": "x21",
    "s6": "x22",
    "s7": "x23",
    "s8": "x24",
    "s9": "x25",
    "s10": "x26",
    "s11": "x27",
}

def reverse_binary(number):

    # Reverse the binary string
    reversed_binary_string = number[::-1]
    # Convert the reversed string back to an integer (binary form)
    return reversed_binary_string


for line in read:

    string_to_split = line.strip()
    #print(string_to_split)
    tokens = re.split(' |, ', string_to_split)

    #print(tokens[0])
    op_name = tokens[0] #op_code 

    #tokens[1] rd
    #tokens[2] rs1
    #tokens[3] rs2

    if tokens[1] in ('a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 't0', 't1', 't2', 't3', 't4', 't5', 't6', 's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11'):   
        token_1 = register_mapping[tokens[1]]
    else:
        token_1 = tokens[1]

    if tokens[2] in ('a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 't0', 't1', 't2', 't3', 't4', 't5', 't6', 's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11'):
        token_2 = register_mapping[tokens[2]]
    else:
        token_2 = tokens[2]    

    if tokens[3] in ('a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 't0', 't1', 't2', 't3', 't4', 't5', 't6', 's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11'):
        token_3 = register_mapping[tokens[3]]
    else:
        token_3 = tokens[3]
            

    #print(token_1, token_2, token_3)

    #immediate(12), rs1(5), funct3(3), rd(5), opcode()
    if op_name in("and","mul","sll","srl","xor","add"):
        #    print("R Type")

      #  rd = bin(int(tokens[1].replace("x", "")))[2:] 
      #  rs1 = bin(int(tokens[2].replace("x", "")))[2:] 
      #  rs2 = bin(int(tokens[3].replace("x", "")))[2:] 

        rd = token_1.replace("x", "")
        rd = (f'{int(rd):05b}')

        rs1 = token_2.replace("x", "")
        rs1 = (f'{int(rs1):05b}')

        rs2 = token_3.replace("x", "")
        rs2 = (f'{int(rs2):05b}')

        R_op_code = R_type_dict[op_name][0] 
        R_funct3 = R_type_dict[op_name][1]
        R_funct7 = R_type_dict[op_name][2]

        machine_line = R_funct7 + rs2 + rs1 + R_funct3 + rd + R_op_code
        machine_line_binary = int(machine_line, 2)
        machine_line_hex = hex(machine_line_binary)

        #print('hexxxx')
        #print(machine_line_hex)
        instruction_list.append(machine_line_hex)
        
        
    elif op_name in ("beq","bne"):
        #instruction_list.append(machine_line_hex)

        if int(token_3) < 0 :
            #found this method of representing negative ints in binary on https://stackoverflow.com/questions/12946116/twos-complement-binary-in-python
            #token_3 = bin(int(token_3) & 0b11111111111)
            imm = str(bin(int(token_3) & 0b1111111111111))[2:15]
            #print(str(bin(int(token_3) & 0b111111111111111)))
            #print(imm)
            
        else:
            imm = token_3
            imm = f'{int(token_3):013b}'
            
        

        rs1 = token_1.replace("x", "")
        rs1 = (f'{int(rs1):05b}')

        rs2 = token_2.replace("x", "")
        rs2 = (f'{int(rs2):05b}')
        
        B_op_code = B_type_dict[op_name][0] 
        B_funct3 = B_type_dict[op_name][1]
        
                                     #[2:8]                                           #might be 8-12
        machine_line = str(imm[0]) + str(imm[2:8]) + str(rs2) + str(rs1) + B_funct3 + str(imm[8:12]) + str(imm[1]) + B_op_code
        

        machine_line_binary = int(machine_line, 2)
        machine_line_hex = hex(machine_line_binary)
       
        #print(machine_line_hex)
        instruction_list.append(machine_line_hex)

    elif op_name in ("slli" ,"srli"):

        rd = token_1.replace("x", "")
        rd = (f'{int(rd):05b}')

        rs1 = token_2.replace("x", "")
        rs1 = (f'{int(rs1):05b}')

        #rs2 = token_3.replace("x", "")
        #rs2 = (f'{int(rs2):05b}')
        token_3 = (f'{int(token_3):05b}')

        I_op_code = I_type_dict[op_name][0] 
        I_funct3 = I_type_dict[op_name][1]
        I_funct7 = I_type_dict[op_name][2]   

        #instruction_list.append(machine_line_hex)
        machine_line = I_funct7 + token_3 + rs1 + I_funct3 + rd + I_op_code 
        machine_line_binary = int(machine_line, 2)
        machine_line_hex = hex(machine_line_binary)
        instruction_list.append(machine_line_hex)

    elif op_name in ("addi","ori","andi"):

        if int(token_3) < 0 :
            #found this method of representing negative ints in binary on https://stackoverflow.com/questions/12946116/twos-complement-binary-in-python
            token_3 = str(bin(int(token_3) & 0b1111111111111))[3:15]

        else:
            token_3 = (f'{int(token_3):012b}')

        rd = token_1.replace("x", "")
        rd = (f'{int(rd):05b}')

        rs1 = token_2.replace("x", "")
        rs1 = (f'{int(rs1):05b}')

        I_op_code = I_type_dict[op_name][0] 
        I_funct3 = I_type_dict[op_name][1]


        machine_line = token_3 + rs1 + I_funct3 + rd + I_op_code    
        machine_line_binary = int(machine_line, 2)
        machine_line_hex = hex(machine_line_binary)
        instruction_list.append(machine_line_hex)

    else:

        print("default case")
       


#instructions are stored in instruction_list and can be viewed by printing
print(instruction_list)