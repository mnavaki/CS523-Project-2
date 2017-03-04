# CS 523 - Project 2
# T16
# Core warrior with GA: basic operations
import numpy as np
import os

class GAIndividual:
    def __init__(self, genome, fitness):
        self.genome = genome
        self.fitness = fitness

    def __lt__(self, other):
        return self.fitness < other.fitness


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
 
                           
''' opcodes = ['DAT', 'MOV', 'ADD', 'SUB','MOV', 'MUL',
           'DIV', 'MOD', 'JMP', 'JMZ', 'JMN', 'DJN', 
           'SPL', 'CMP', 'SEQ', 'SNE', 'SLT', 'LDP', 
           'STP', 'NOP', 
           'MOV', 'ADD','MOV', 'SUB', 'CMP', 'MOV', 
           'JMZ', 'DJN', 'ADD', 'SPL', 'ADD', 'SPL', 'CMP']
address_modes = ["#","$","@","<","*","{","}", "}", "}", "}", "}", "#", "#", "$", "$"]
'''

max_lines = 40 ## maximum numberlines of code for the initial population
benchmark_dir = "./WilkiesBench/"
pmars_dir = "."


def create_aLineOfCode():
    opcodes_size = len(opcodes)
    addrress_modes_size = len(address_modes)

    out = "\n"
    out += opcodes[np.random.randint(opcodes_size)] + " "
    out += address_modes[np.random.randint(1, addrress_modes_size)]
    out += str(np.random.randint(10)) + ","
    out += address_modes[np.random.randint(1, addrress_modes_size)]
    out += str(np.random.randint(10))

    return out


def create_header(warrior_name):
    header = "; redcode\n"
    header += "; name " + warrior_name + "\n"
    header += "; author T16\n"
    header += "; assert CORESIZE == 8000"
    return header


def is_viable(file_name):
    global pmars_dir
    
    command = pmars_dir + "/pmars -b -o ./WilkiesBench/CANNON.RED " + file_name + " > res.txt"
    os.system(command)
    res_file = open("res.txt", "r")
    result = res_file.read()
    result_index = result.find("T16 scores ")
    elem = result[result_index:].split(" ")
    score = elem[2].split("\n")[0]
    os.system("cd warriors")
    if score is "0":
        return False
    return True


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
            for j in range(max_lines):
                line = create_aLineOfCode() # TODO Make it efficient
                red_file.write(line)
            red_file.close()
            if is_viable(file_name) is True:
                break
        fitness = 0
        genome = file_name
        indv = GAIndividual(genome, fitness)
        population.append(indv)
        print "warrior:", warrior_name + ".red generated!"

    return population

