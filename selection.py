# CS 523 - Project 2
# T16
# Core warrior with GA: selection methods
from __future__ import division
import random 
import math
import numpy as np
from base import *


# copy file content from redcode_src to redcode_dest file and keep the header intact
def copy(redcode_src, redcode_dest, dest_warrior_name):

    dest_header = create_header(dest_warrior_name) #redcode_dest.replace('.red',''))
    src_file = open(redcode_src,'r')
    src_code = src_file.readlines()[4:]
    dest_file = open(redcode_dest, "w+")
    dest_file.write(dest_header + "\n")
    dest_file.writelines(src_code)
    src_file.close()
    dest_file.close()

# tournament selection method
def tournament_selection_one(population, pop_size, tournament_size):

	individuals = []
	# Shuffle the indices
	indices = range(pop_size)
	random.shuffle(indices)
	for i in xrange(tournament_size):
		individuals.append(population[indices[i]])
	# Sort individuals based on fitness with the best fitness
	# individual first
	individuals = sorted(individuals, key=lambda c: c.fitness, reverse=True)
	# Return the most fit individual
	return individuals[0]

# tournament selection method
def tournament_selection(population, pop_size):
    
    new_population = []
    os.system("mkdir -p ./tmp")
    for i in range(pop_size):
        tournament_size = np.random.rand(pop_size/2,pop_size)
        indv = tournament_selection_one(population, pop_size, tournament_size)
        warrior_name = "T16-" + str(i+1)
        file_name = "./tmp/" + warrior_name + ".red"
        copy(indv.genome, file_name, warrior_name)
        new_indv = GAIndividual("./warriors/" + warrior_name + ".red", indv.fitness)
        new_population.append(new_indv)

    os.system("rm ./warriors/*") ## remove old population
    os.system("mv ./tmp/* ./warriors/")  ## mv new population to the warriors directory
    return new_population


'''
Roulette selection method: The individuals are mapped to contiguous segments of a line, 
such that each individual's segment is equal in size to its 
fitness. A random number is generated and the individual whose 
segment spans the random number is selected.
'''
def roulette_selection_one(population, pop_size):
    total_fitness = sum(pop.fitness for pop in population)
    rand = np.random.randint(1, total_fitness)
    total_fitness_so_far = 0
    # iterate untill we find a genome
    for i in range(pop_size):
        total_fitness_so_far += population[i].fitness
        if rand <= total_fitness_so_far:
            return population[i]

# roulette selection method
def roulette_selection(population, pop_size):
    new_population = []
    os.system("mkdir -p ./tmp")
    
    for i in range(pop_size):
        indv = roulette_selection_one(population, pop_size)
        warrior_name = "T16-" + str(i+1)
        file_name = "./tmp/" + warrior_name + ".red"
        copy(indv.genome, file_name, warrior_name)
        new_indv = GAIndividual("./warriors/" + warrior_name + ".red", indv.fitness)
        new_population.append(new_indv)

    os.system("rm ./warriors/*") ## remove old population
    os.system("mv ./tmp/* ./warriors/")  ## mv new population to the warriors directory
    return new_population
    


''' Random selection method 
    Replace bottom half of population 
    with random individuals from the top % half '''
def random_selection(population, pop_size):
    # Sort population by fitness (in ascending order)
    population = np.sort(population)
    # flooring in case the population size is odd
    cutoff = int(math.floor(pop_size/2))
    for i in range(cutoff):
        index = np.random.randint(cutoff)
        wn_index = population[i].genome.find("T16") # get warrior name index
        copy(population[cutoff + index].genome, population[i].genome, population[i].genome[wn_index:].replace('.red',''))
        population[i].fitness = population[cutoff + index].fitness
    return population

