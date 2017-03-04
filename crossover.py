# CS 523 - Project 2
# T16
# Core warrior with GA: crossover methods
import numpy as np
import os
import math


# uniform unification
# It returns a child
def uniform_crossover(population, parent1_index, parent2_index):
    par1_file = population[parent1_index].readlines()[4:]
    par2_file = population[parent2_index].readlines()[4:]
    par1_length = len(par1_file)
    par2_length = len(par2_file)
    short_length = min(par1_length, par2_length)
    child = []
    for i in range(short_length):
        if random.uniform(0, 1) > 0.5:
            child.append(par1_file[i])
        else
            child.append(par2_file[i])
    diff = math.abs(par1_length - par2_length)
    for i in range(diff):
         if par1_length > par2_length:
              child.append(par1_file[par1_length + i])
         else:
              child.append(par2_file[par2_length + i])
    return child

