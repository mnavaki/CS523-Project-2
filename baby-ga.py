 # Genetic algorithm
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import math
import random
import operator


class GAIndividual:
    def __init__(self, genome, fitness):
        self.genome = genome
        self.fitness = fitness

    def __lt__(self, other):
        return self.fitness < other.fitness


def F(X):
    return np.sin(X)*np.power(X, 2)
    #return np.power(-X, 2)



## Simple GA that tries to find the maximum value
## of a 1D Function F. Example: GA(10, 0.5, 10, @(X) sin(X).*X.^2, 2.2)
def GA(pop_size, mutation_rate, num_generations, F, animation_delay):
    genome_min = -15
    genome_max = 30
    genome_space = np.arange(genome_min, genome_max)
    # Keep some statistics about the evolution
    mean_fitness_over_time = []
    max_fitness_over_time = []
    min_fitness_over_time = []

    population = []
    print population
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('Genome', fontsize=20)
    ax.set_ylabel('Fitness', fontsize=20)

    plt.plot(genome_space, F(genome_space))
    p = []
    for i in range(pop_size):
        fitness = 0
        genome = random.uniform(0, 1)*(genome_max - genome_min) + genome_min
        indv = GAIndividual(fitness, genome)
        population.append(indv)
        lines, = plt.plot(genome, fitness, 'o', linewidth=10, markersize=20)
        p.append(lines)

    for generation in range(num_generations):
        # Mutate population
        for i in range(pop_size):
            candidate = population[i].genome + random.uniform(0, mutation_rate)
            if (candidate < genome_max) and (candidate > genome_min):
                population[i].genome = candidate
        plt.pause(animation_delay)

        # Animation
        for i in range(pop_size):
            p[i].set_xdata(population[i].genome)
            p[i].set_ydata(population[i].fitness)
            plt.draw()

        # Evaluate fitness
        for i in range(pop_size):
            population[i].fitness = F(population[i].genome)

        # Sort population by fitness (lowest to highest)
        population = np.sort(population)

        # Replace bottom half of population 
        # with random individuals from the top % half
        cutoff = pop_size/2
        # ceiling in case the population size is odd
        for i in range(cutoff):
            index = np.random.randint(cutoff)
            population[cutoff + i].genome = population[index].genome
            population[cutoff + i].fitness = population[index].fitness


#GA(50, 5, 30, F, 0.5)
GA(30, 1, 100, F, 0.1)

