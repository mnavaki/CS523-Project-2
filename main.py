# CS 523 - Project 2
# T16
# Core warrior with GA

#import numpy.matlib
#import matplotlib.pyplot as plt
import math
import operator
import sys
from selection import *


def battle_one_vs_one(red_filename1, red_filename2):
    global pmars_dir
    global number_of_rounds

    command = pmars_dir + "/pmars -r " + str(number_of_rounds) + " -b -o " + red_filename1 + " " + red_filename2 + " > res.txt"
    os.system(command)
    res_file = open("res.txt", "r")
    result = res_file.read()
    wn_index = red_filename1.find("T16")  ## get warrior name index
    warrior_name = red_filename1[wn_index:].replace('.red','') ## extract warrior name
    result_index = result.find(warrior_name)
    score_line = result[result_index:].split("\n")[0] ## extract score line
    my_score = int(score_line.split(" ")[4]) ## extract my score
    
    return my_score

# Returns number of wins over the benchmakrs
# fitness will be the score of running aganist benchmarks and other warriors
def fitness_func(red_filename):
    global benchmark_dir

    score_total = 0
    ## Running against benchmarks
    for file in os.listdir(benchmark_dir):
        bench_filename = benchmark_dir + file
        my_score = battle_one_vs_one(red_filename, bench_filename)
        score_total += my_score
        print "total score against bench:", my_score
    ## Running against other warriors
    warriors_dir = "./warriors/"
    for file in os.listdir(warriors_dir):
        if (warriors_dir + file) != red_filename:
            warrior_filename = warriors_dir + file
            my_score = battle_one_vs_one(red_filename, warrior_filename)
            score_total += my_score

    return score_total

'''
def run_competion(compet1_filename, compet2_filename):
    command = pmars_dir +  "/pmars -r 50 -b -o " + compet1_filename + " " + compet2_filename + " > res.txt"
    os.system(command)
    res_file = open("res.txt", "r")
    print res_file.read()
'''

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
    if len(new_code.split("\n")) <= 4: # avoid an empty code file
        new_code += create_aLineOfCode()
    red_file = open(individual.genome, "w")
    red_file.write(new_code)
    red_file.close()


## Simple GA that tries to find the maximum value
## of a 1D Function F. Example: GA(10, 0.5, 10, @(X) sin(X).*X.^2, 2.2)
def GA(pop_size, mutation_rate, num_generations, fitness_func):

    population = create_a_population(pop_size)
    print "> initial population generated!"
    for generation in range(num_generations):
        print "========================" 
        print "> Mutating population..."
        # Mutate population
        for i in range(pop_size):
            mutate(population[i])
        
        print "> Evaluating fitness..."
        # Evaluate fitness
        for i in range(pop_size):
            population[i].fitness = fitness_func(population[i].genome)
     
        # Replace bottom half of population 
        # with random individuals from the top % half
        #population = random_selection(population, pop_size)
        
        print "> Selecting genomes..."
        ## roulette selection
        max_score = 0
        population, pop_size = roulette_selection(population, pop_size)
        if pop_size != 0:
            max_score = max(pop.fitness for pop in population)

        # indv = tournament_selection(population, pop_size, 6)
        print "> Generation " + str(generation+1) + " created!"
        print "> Top fitness in this generation: " + str(max_score)



''' ******************* MAIN BODY ******************* '''
pop_size = 20
num_generations = 40
mutation_rate = 10 # out of 100
number_of_rounds = 100


## Run GA
GA(pop_size, mutation_rate, num_generations, fitness_func)



