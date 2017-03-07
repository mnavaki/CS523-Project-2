# CS 523 - Project 2
# T16
# Core warrior with GA: basic operations
import numpy as np
import os
import random


class GAIndividual:
    def __init__(self, genome, fitness):
        self.genome = genome
        self.fitness = fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

      
'''
opcodes = ["dat","mov","add","sub",
           "mul","div","mod","jmp",
           "jmz","jmn","djn","spl",
           "slt","cmp","seq","sne",
           "nop",
           "mov","mov","mov","mov",
           "mov","mov","mov","mov",
           "spl","spl","spl","spl",
           "add","add","add","add",
           "jmz","jmz","jmz","jmz",
           "add","add","sub","sub",
           "spl","spl","mov","mov",
           "djn","djn","djn","djn",
           "cmp","cmp","cmp","cmp",
           "add","add","add","add"]


address_modes = ["#","$","@","<",">","*","{","}",
                 "#","#","#","$","$","$","$",
                 "#","#","#","$","$","$","$",
                 "}","}","}","}","}","}","}",
                 "}","}","}","}","}","}","}",
                 "}","}","}","}","}","}","}"]
'''



opcodes = ["dat","mov","add","sub",
           "mul","div","mod","jmp",
           "jmz","jmn","djn","spl",
           "slt","cmp","seq","sne",
           "nop",
           "mov","mov","mov","mov",
           "mov","mov","mov","mov",
           "spl","spl","spl","spl",
           "add","add","add","add",
           "jmz","jmz","jmz","jmz",
           "add","add","sub","sub",
           "spl","spl","dat","dat",
           "djn","djn","djn","djn",
           "spl","spl","spl","dat",
           "mov","mov","spl","dat","jmp","jmp","jmp"]

address_modes = ["#","$","@","<",">","*","{","}",
                 "#","#","#","@","@","@","@",
                 "#","#","#","<","<","@","$",
                 "#","#","#","<","<","@","$",
                 "}","}","}","}","}","}","}",
                 "}","}","}","}","}","}","}"]
                

mod_list = [ ".a ",".b ",".ab",".ba",".f ",".x ",".i ",
                 ".i ",".i ",".i ",".i ",".i ",".i ",".i "  ]

'''                           
opcodes = ['DAT', 'MOV', 'ADD', 'SUB','MOV', 'MUL',
           'DIV', 'MOD', 'JMP', 'JMZ', 'JMN', 'DJN', 
           'SPL', 'CMP', 'SEQ', 'SNE', 'SLT', 'LDP', 
           'STP', 'NOP']
address_modes = ["#","$","@","<","*","{","}"]

mod_list = [ ".a ",".b ",".ab",".ba",".f ",".x ",".i "]
'''

            
max_lines = 10 ## maximum numberlines of code for the initial population
benchmark_dir = "./WilkiesBench/"
pmars_dir = "."

core_size = 8000

def get_a_random_number():
    return np.random.randint(-20,20)#core_size)

'''
    if random.uniform(0, 1) > 0.6:
        return np.random.randint(1, 10)
    elif random.uniform(0, 1) > 0.8:
        return np.random.randint(-10, 0)
    else:
        return np.random.randint(1, core_size)
'''
    
known_instructions = ['mov 0, ', 'spl.x  #0,#0']


def create_aLineOfCode():
    known_instructions_size = len(known_instructions)
    if np.random.randint(0,100) < 5:
        return "\n" + known_instructions[0] + str(np.random.randint(core_size))
    if np.random.randint(0,100) < 5:
        return "\n" + known_instructions[1]
    opcodes_size = len(opcodes)
    addrress_modes_size = len(address_modes)
    mod_list_size = len(mod_list)

    out = "\n"
    out += opcodes[np.random.randint(opcodes_size)]
    out += mod_list[np.random.randint(mod_list_size)] + " "
    out += address_modes[np.random.randint(1, addrress_modes_size)]
    out += str(get_a_random_number()) + ","
    out += address_modes[np.random.randint(1, addrress_modes_size)]
    out += str(get_a_random_number())

    return out


def create_header(warrior_name):
    header = "; redcode\n"
    header += "; name " + warrior_name + "\n"
    header += "; author T16\n"
    header += "; assert CORESIZE == " + str(core_size)
    return header


def is_viable(file_name):
    global pmars_dir

    command = pmars_dir + "/pmars -r 100 -b -o test.red " + file_name + " > res.txt"
    os.system(command)
    res_file = open("res.txt", "r")
    result = res_file.read()
    
    wn_index = file_name.find("T16")  ## get warrior name index
    warrior_name = file_name[wn_index:].replace('.red','') ## extract warrior name
    result_index = result.find(warrior_name)
    score_line = result[result_index:].split("\n")[0] ## extract score line
    score = int(score_line.split(" ")[4]) ## extract my score
    
    
    #result_index = result.find("T16")
    #elem = result[result_index:].split(" ")
    #score = elem[2].split("\n")[0]
    #os.system("cd warriors")
    if score > 250:
        return True
    return False


def create_a_population(pop_size):
    global max_lines
    os.system("mkdir -p warriors")  # create warriors directory
    os.system("rm ./warriors/*")  # clean the directory
    warrior_dir = "./warriors/"
    population = []
    for i in range(pop_size):
        warrior_name = "T16-" + str(i+1)
        file_name = warrior_dir + warrior_name + ".red"
        header = create_header(warrior_name)
        while True:
            red_file = open(file_name, "w+")  # open the warrior file
            red_file.write(header)
            line_number = max_lines  # np.random.randint(5, max_lines)
            for j in range(line_number):
                line = create_aLineOfCode() # TODO Make it efficient
                red_file.write(line)
            red_file.write("\n")
            red_file.close()
            if is_viable(file_name) is True:
                break
        fitness = 0
        genome = file_name
        indv = GAIndividual(genome, fitness)
        population.append(indv)
        print "warrior:", warrior_name + ".red generated!"

    return population

