import os
from warrior import *

# Defining some values
num_rounds = 100
tournament_size = 2

# Defining some constants to help with readability
# Selection methods
ROULETTE = 0
TOURNAMENT = 1
RANDOM = 2

# Crossover methods
NONE = 0
UNIFORM = 1
ONEPOINT = 2

# Creates a new population of random Warriors of size population_size
def initPopulation(population_size):
    population = [None] * population_size
    for x in range(0, population_size):
        population[x] = Warrior()
    return population


# Runs a genetic algorithm on a given population
def runGA(population, selection, crossover, crossover_rate, mutation_rate, stopping_criteria):
    while (True):
        temp = nextGen(population, selection, crossover, crossover_rate, mutation_rate)
        if (stopping_criteria): # Still need to decide on a good stopping criteria
            return population
        population = temp


# Produces the next generation of a given population
def nextGen(population, selection, crossover, crossover_rate, mutation_rate):
    # Init next generation
    nextGen = []
    # Running selection
    if (selection == ROULETTE):
        # First calculate fitness of Warriors relative to each other
        calcFitness(population)
        # Get each Warrior's percentage fitness
        total_fitness = sum(warrior.fitness for warrior in population)
        distribution = []
        for warrior in population:
            distribution.append(warrior.fitness / total_fitness)
        while (len(nextGen) < len(population)):
            parent1_index = np.random.choice(len(population), 1, p = distribution)
            parent2_index = np.random.choice(len(population), 1, p = distribution)
            child1 = Warrior(population[parent1_index])
            child2 = Warrior(population[parent2_index])
            # If crossover occurs
            if (np.random.randint(1, 100) <= crossover_rate):
                if (crossover == UNIFORM):
                    child1.crossover_uniform(child2)
                if (crossover == ONEPOINT):
                    child1.crossover_one_point(child2)
                # Do nothing for NONE
            # Run mutations
            child1.mutate()
            child2.mutate()
            # Add children to next generation
            nextGen.append(child1)
            nextGen.append(child2)
            
    if (selection == TOURNAMENT):
        while (len(nextGen) < len(population)):
            # Tournament for parent1
            parent1_tournament = []
            while (len(parent1_tournament) < tournament_size):
                parent1_tournament.append(population[np.random.choice(len(population)])
            calcFitness(parent1_tournament)
            child1 = max(parent1_tournament, key=lambda warrior: warrior.fitness)
            # Tournament for parent2
            parent2_tournament = []
            while (len(parent2_tournament) < tournament_size):
                parent2_tournament.append(population[np.random.choice(len(population)])
            calcFitness(parent2_tournament)
            child2 = max(parent1_tournament, key=lambda warrior: warrior.fitness)
            # If crossover occurs
            if (np.random.randint(1, 100) <= crossover_rate):
                if (crossover == UNIFORM):
                    child1.crossover_uniform(child2)
                if (crossover == ONEPOINT):
                    child1.crossover_one_point(child2)
                # Do nothing for NONE
            # Run mutations
            child1.mutate()
            child2.mutate()
            # Add children to next generation
            nextGen.append(child1)
            nextGen.append(child2)
            
    if (selection == RANDOM):
        # First calculate fitness of Warriors relative to each other
        calcFitness(population)
        # Sort the population
        sorted_population = sorted(population, key=lambda warrior: warrior.fitness, reverse = True)
        # Copy the top half of Warriors based on fitness into next generation
        for x in range(0,len(sorted_population)):
            nextGen.append(sorted_population[x])
        # Randomly select from the top half to fill in the rest
        while (len(nextGen) < len(population)):
            np.random.choice(len(population)
            nextGen.append()
    
    return nextGen


# Calculates and assigns fitness of Warriors in a population relative to each other
def calcFitness(population):
    # Make a temporary directory for the run
    os.system("mkdir temp")
    # Create red code for our Warriors in temp directory
    index = 0
    for warrior in population:
        # Naming each Warrior as just their index for easy retrieval later
        warrior.writeFile(str(index),"./temp/MYWAR" + str(index) + ".RED")
    # Run pmars in temp directory
    os.system("./pmars -r " + str(num_rounds) + " -b -o ./temp/*.RED > ./temp/results.txt")
    # Parse the results and assign them to the Warriors
    for line in open("./temp/results.txt",'r'):
        info = line.split()
        if (info[0].isdigit()):
            population[int(info[0])].fitness = int(info[-1])
    # Cleanup
    os.system("rm -rf ./temp")


# Get the benchmark fitness score for a single Warrior
# Assumes the benchmark Warriors are contained in a directory called WilkiesBench
def getBenchmarkFitness(warrior):
    fitness_score = -1
    # Make a temporary directory for the run
    os.system("mkdir temp")
    # Copy benchmark Warriors into temp directory
    os.system("cp ./WilkiesBench/* ./temp")
    # Create red code for our Warrior in temp directory
    warrior.writeFile("myWarrior","./temp/MYWAR.RED")
    # Run pmars in temp directory
    os.system("./pmars -r " + str(num_rounds) + " -b -o ./temp/*.RED > ./temp/results.txt")
    # Parse the result
    for line in open("./temp/results.txt",'r'):
        info = line.split()
        if (info[0] == "myWarrior"):
            fitness_score = int(info[-1])
    # Cleanup
    os.system("rm -rf ./temp")
    # Return result
    return fitness_score
