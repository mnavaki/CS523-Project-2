# CS 523 - Project 2
# T16
# Core warrior with GA

import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import math
import random
import operator
import sys
import os


class GAIndividual:
    def __init__(self, genome, fitness):
        self.genome = genome
        self.fitness = fitness

    def __lt__(self, other):
        return self.fitness < other.fitness


def create_header(warrior_name):
    header = "; redcode\n"
    header += "; name " + warrior_name + "\n"
    header += "; author T16\n"
    header += "; assert    CORESIZE == 8000"
    return header

def create_aLineOfCode():
    opcodes_size = len(opcodes)
    addrress_modes_size = len(address_modes)

    out = "\n"
    out += opcodes[np.random.randint(opcodes_size)] + " "
    out += address_modes[np.random.randint(1, addrress_modes_size)]
    out += str(np.random.randint(10)) + ","
    out += address_modes[np.random.randint(1, addrress_modes_size)]
    out += str(np.random.randint(10))

    #print out
    return out

def is_viable(file_name):
    command = "./pmars -b -o ./WilkiesBench/CANNON.RED " + file_name + " > res.txt"
    os.system(command)
    res_file = open("res.txt", "r")
    result = res_file.read()
    result_index = result.find("T16 scores ")
    elem = result[result_index:].split(" ")
    score = elem[2].split("\n")[0]
    if score is "0":
        return False
    return True

def create_a_population(pop_size):

    max_lines = 50
    population = []
    for i in range(pop_size):
        # open a file
        warrior_name = "T16-" + str(i+1)
        file_name = warrior_name + ".red"
        header = create_header(warrior_name)
        while True:
            red_file = open(file_name, "w+")
            red_file.write(header)
            for j in range(max_lines):
                line = create_aLineOfCode()
                red_file.write(line)
            red_file.close()
            if is_viable(file_name) is True:
                break
        fitness = 0
        genome = file_name
        indv = GAIndividual(genome, fitness)
        population.append(indv)

    return population


#Returns number of wins over the benchmakrs
def fitness_func(red_filename):
    global benchmark_dir
    score_total = 0
    for file in os.listdir(benchmark_dir):
        file_dir = benchmark_dir + file
        command = "./pmars -r 50 -b -o " + red_filename + " " + file_dir + " > res.txt"
        os.system(command)
        res_file = open("res.txt", "r")
        result = res_file.read()
        result_index = result.find("Results")
        res_line = result[result_index:].split(" ")
        oponent_score = int(res_line[1])
        my_score = int(res_line[3])
        score_total += my_score
        #if my_score > oponent_score:
        #    win_count += 1
        #print result[result_index:]
        #print oponent_score, my_score
    #print score_total
    return score_total


def run_competion(compet1_filename, compet2_filename):
    command = "./pmars -r 50 -b -o " + compet1_filename + " " + compet2_filename + " > res.txt"
    os.system(command)
    res_file = open("res.txt", "r")
    print res_file.read()


def should_mutate():
    return np.random.randint(1, 100) <= mutation_rate

# insert, delete, replace
def mutation_type():
    return np.random.randint(1, 4)
    

# mutate: remove, modify, add
def mutate(individual):

    red_file = open(individual.genome, "r")
    red_code_lines = red_file.read().split("\n")
    new_code = ""
    for line_index in range(len(red_code_lines)):
        if line_index == 0: # copy the header
            new_code += red_code_lines[line_index]
            continue
        if line_index < 4: # copy the header
            new_code += "\n" + red_code_lines[line_index]
            continue
        if should_mutate(): # mutate
            mut_type = mutation_type()
            if mut_type == 1: ## insert a new line
                new_code += "\n" + red_code_lines[line_index]
                new_code += create_aLineOfCode()
            elif mut_type == 2: ## delete the line
                continue
            else: ## replace
                new_code += create_aLineOfCode()
        else:
            new_code += "\n" + red_code_lines[line_index]

    red_file.close()
    if len(new_code.split("\n")) <= 4:
        return False
    else:
        red_file = open(individual.genome, "w")
        red_file.write(new_code)
        red_file.close()
    return True

## Simple GA that tries to find the maximum value
## of a 1D Function F. Example: GA(10, 0.5, 10, @(X) sin(X).*X.^2, 2.2)
def GA(pop_size, mutation_rate, num_generations, fitness_func):

    population = create_a_population(pop_size)
    for generation in range(num_generations):
        # Mutate population
        for i in range(pop_size):
            if mutate(population[i]) is False:
                np.delete(population, i)

        # Evaluate fitness
        for i in range(pop_size):
            population[i].fitness = fitness_func(population[i].genome)

        # Sort population by fitness (in descending order)
        population = np.sort(population)
        total_score = 0
        for i in range(pop_size):
            total_score += population[i].fitness
        print "total score: ", total_score
        # Replace bottom half of population 
        # with random individuals from the top % half
        cutoff = pop_size/2
        # ceiling in case the population size is odd
        for i in range(cutoff):
            index = np.random.randint(cutoff)
            os.system("cp " + population[cutoff + index].genome + " " + population[i].genome)
            population[i].fitness = population[cutoff + index].fitness

opcodes = ['DAT', 'MOV', 'ADD', 'SUB',
           'MUL', 'DIV', 'MOD', 'JMP',
           'JMZ', 'JMN', 'DJN', 'SPL', 
           'CMP', 'SEQ', 'SNE', 'SLT', 
           'LDP', 'STP', 'NOP']
address_modes = ["#","$","@","<","*","{","}"]

pop_size = 20
mutation_rate = 20
num_generations = 50

benchmark_dir = "./WilkiesBench/"
GA(pop_size, mutation_rate, num_generations, fitness_func)


