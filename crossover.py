# CS 523 - Project 2
# T16
# Core warrior with GA: crossover methods
import numpy as np
import os
import random

## uniform crossover
## It returns children
def uniform_crossover(parent1, parent2):
    par1_file = open(parent1.genome, "r")
    par2_file = open(parent2.genome, "r")
    par1_code = par1_file.readlines()[4:]
    par2_code = par2_file.readlines()[4:]
    par1_length = len(par1_code)
    par2_length = len(par2_code)

    #par1_code[par1_length-1] += "\n"
    #par2_code[par2_length-1] += "\n"

    short_length = min(par1_length, par2_length)
    child1 = []
    child2 = []
    for i in range(short_length):
        if random.uniform(0, 1) > 0.5:
            child1.append(par1_code[i])
            child2.append(par2_code[i])
        else:
            child1.append(par2_code[i])
            child2.append(par1_code[i])

    diff = abs(par1_length - par2_length)
    for i in range(diff):
        if par1_length > par2_length:
            child1.append(par1_code[par2_length + i])
        elif par2_length > par1_length:
            child2.append(par2_code[par1_length + i])
    
    par1_file.close()
    par2_file.close()
    return child1, child2

## one point crossover method
## It returns children
def one_point_crossover(parent1, parent2):
    par1_file = open(parent1.genome, "r")
    par2_file = open(parent2.genome, "r")
    par1_code = par1_file.readlines()[4:]
    par2_code = par2_file.readlines()[4:]
    par1_length = len(par1_code)
    par2_length = len(par2_code)
    
    #par1_code[par1_length-1] += "\n"
    #par2_code[par2_length-1] += "\n"
    
    min_len = min(par1_length,par2_length)
    max_len = max(par1_length,par2_length)
    point = random.randint(1, min_len)

    child1 = []
    child2 = []
    for i in range(point):
        child1.append(par1_code[i])
        child2.append(par2_code[i])
    for i in range(point, max_len - 1):
        if i < par2_length:
            child1.append(par2_code[i])
        if i < par1_length:
            child2.append(par1_code[i])

    par1_file.close()
    par2_file.close()
    return child1, child2

