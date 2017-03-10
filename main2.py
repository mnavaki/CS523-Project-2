from genetic_algorithm import *

# Doing island genetic algorithm
# Initializing some values
num_islands = 20
population_size = 20

# Initialize top Warriors list
top_warriors = []

# For each island
for x in range(0,num_islands):
    # Create an intial population
    myPopulation = initPopulation(population_size)
    # Run GA on it
    endPopulation = runGA(myPopulation, TOURNAMENT, UNIFORM, 100, 1, stopping_criteria):
    # Pick the top individual to compete in inter-island competition
    top_warriors.append(max(endPopulation, key=lambda warrior: warrior.fitness))
    
# Do a final competition with top Warriors from each island
finalPopulation = runGA(top_warriors, TOURNAMENT, UNIFORM, 100, 1, stopping_criteria):