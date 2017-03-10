# CS 523 - Project 2
# T16
# Core warrior with GA

#import numpy.matlib
#import matplotlib.pyplot as plt
import math
import operator
import sys
from selection import *
from crossover import *

def battle_one_vs_one(red_filename1, red_filename2, bench_flag):
    global pmars_dir
    global number_of_rounds

    command = pmars_dir + "/pmars -r " + str(number_of_rounds) + " -b -o " + red_filename1 + " " + red_filename2 + " > res.txt"
    os.system(command)
    res_file = open("res.txt", "r")
    result = res_file.read()
    ## Get score for the first contestant
    wn_index1 = red_filename1.find("T16")  ## get warrior name index
    warrior_name1 = red_filename1[wn_index1:].replace('.red','') ## extract warrior name  
    result_index1 = result.find(warrior_name1)
    score_line1 = result[result_index1:].split("\n")[0] ## extract score line
    score1 = int(score_line1.split(" ")[4]) ## extract the score
    if bench_flag:
        return score1
    ## Get score for the second contestant
    wn_index2 = red_filename2.find("T16")  ## get warrior name index
    warrior_name2 = red_filename2[wn_index2:].replace('.red','') ## extract warrior name
    result_index2 = result.find(warrior_name2)
    score_line2 = result[result_index2:].split("\n")[0] ## extract score line
    score2 = int(score_line2.split(" ")[4]) ## extract the score    
    
    res_file.close()
    return score1, score2

# Returns number of wins over the benchmakrs
# fitness will be the score of running aganist benchmarks and other warriors
def fitness_func(red_filename):
    global benchmark_dir

    score_total = 0
    ## Running against benchmarks
    for file in os.listdir(benchmark_dir):
        bench_filename = benchmark_dir + file
        my_score = battle_one_vs_one(red_filename, bench_filename, True)
        score_total += my_score

    bench_avg_score = score_total/benchmarks_number
    return bench_avg_score


def should_crossover():
    return np.random.randint(1, 100) <= crossover_rate

def should_mutate():
    return np.random.randint(1, 100) <= mutation_rate

def should_insert():
    return np.random.randint(1, 100) <= insert_rate

def should_replace():
    return np.random.randint(1, 100) <= replace_rate
    
def should_delete():
    return np.random.randint(1, 100) <= delete_rate

def mutation_type():
    return np.random.randint(1, 4)

def avg_score(population, pop_size):
    return sum(pop.fitness for pop in population)/pop_size


# mutate: remove, modify, add
def mutate(individual, population,_pop_size):
    tries_number = 100
    for i in range(tries_number):
    #while True:
        red_file = open(individual.genome, "r")
        red_code_lines = red_file.readlines()

        new_code = []
        for line_index in range(len(red_code_lines)):
            if line_index < 4: # copy the header
                new_code.append(red_code_lines[line_index])
                continue
            mut_type = mutation_type()
            if mut_type == 1 and len(new_code) < 98: ## insert
                if should_insert():  ## insert a new line
                    new_code.append(create_aLineOfCode().replace('\n','') + "\n")
                    new_code.append(red_code_lines[line_index])
                else:
                    new_code.append(red_code_lines[line_index])
            elif mut_type == 2 and len(new_code) < 98: ## replace
                if should_replace():  ## replace
                    new_code.append(create_aLineOfCode().replace('\n','') + "\n")
                else:
                    new_code.append(red_code_lines[line_index])
            else: ## delete
                if should_delete() and len(new_code) > 6:  ## delete the line
                    continue
                elif len(new_code) < 98:
                    new_code.append(red_code_lines[line_index])

        red_file.close()
        os.system("cp " + individual.genome + " temp.red")
        red_file = open(individual.genome, "w")
        red_file.writelines(new_code)
        red_file.close()
        if fitness_func(individual.genome) > avg_score(population,_pop_size):
            break
        os.system("cp temp.red " + individual.genome)


def find_the_weakest(population, pop_size):
    min_fitness = population[0].fitness
    min_fitness_index = 0
    for i in range(pop_size):
        if (population[i].fitness < min_fitness):
            min_fitness = population[i].fitness
            min_fitness_index = i
    return min_fitness_index

def find_the_strongest(population, pop_size):
    max_fitness = population[0].fitness
    max_fitness_index = 0
    for i in range(pop_size):
        if (population[i].fitness > max_fitness):
            max_fitness = population[i].fitness
            max_fitness_index = i
    return population[max_fitness_index]

def extract_warrior_name(filename):
    index = filename.find("T16")
    return filename[index:].replace('.red','')
    
def replace_weakest_warrior(population, pop_size, child):

    weakest_indv_index = find_the_weakest(population, pop_size)
    warrior_name = extract_warrior_name(population[weakest_indv_index].genome)
    header = create_header(warrior_name)
    os.system("mv " + population[weakest_indv_index].genome + " .")
    file = open(population[weakest_indv_index].genome, "w+")
    file.write(header + "\n")
    file.writelines(child)
    file.close()
    new_fitness = fitness_func(population[weakest_indv_index].genome)
    
    if new_fitness > avg_score(population, pop_size):
    #if is_viable(population[weakest_indv_index].genome):
        os.system("rm " + warrior_name + ".red ")
        population[weakest_indv_index].fitness = new_fitness
        return population
        
    os.system("mv " + warrior_name + ".red " + population[weakest_indv_index].genome)
    return population


def replace_warrior(warrior_src, warrior_dest):
    wn_index = warrior_dest.find("T16") # get warrior name index
    copy(warrior_src, warrior_dest, warrior_dest[wn_index:].replace('.red',''))

def run_battles(population, pop_size, elite_list):
    global number_of_rounds
    total_score = number_of_rounds*3
    for i in range(5):
        contestant1 = np.random.randint(0,pop_size)
        contestant2 = np.random.randint(0,pop_size)
        score1, score2 = battle_one_vs_one(population[contestant1].genome, population[contestant2].genome, False)
        if score1 > score2: ## contestant1 wins
            replace_warrior(population[contestant1].genome, population[contestant2].genome)
        elif score1 < score2: ## contestant2 wins
            replace_warrior(population[contestant2].genome, population[contestant1].genome)
        else:
            if contestant1 not in elite_list: ## tie
                mutate(population[contestant1], population, pop_size)
            if contestant2 not in elite_list: ## tie
                mutate(population[contestant2], population, pop_size)
    return population

def get_top_two(population, pop_size):
  
    max_fitness = population[0].fitness
    max_fitness_index = 0
    for i in range(pop_size):
        if (population[i].fitness > max_fitness):
            max_fitness = population[i].fitness
            max_fitness_index = i
    
    index1 = max_fitness_index
    
    max_fitness = 0
    max_fitness_index = 0
    for i in range(pop_size):
        if i == index1:
            continue
        if (population[i].fitness > max_fitness):
            max_fitness = population[i].fitness
            max_fitness_index = i
    index2 = max_fitness_index
    return index1, index2 
    
def save_top_two(population, pop_size):
    os.system("mkdir -p ./top-warriors/")
    os.system("rm ./top-warriors/*")
    index1, index2 = get_top_two(population, pop_size)   
    os.system("cp " + population[index1].genome + " ./top-warriors/")
    os.system("cp " + population[index2].genome + " ./top-warriors/")


## Simple GA that tries to find the maximum value
## of a 1D Function F. Example: GA(10, 0.5, 10, @(X) sin(X).*X.^2, 2.2)
def GA(pop_size, mutation_rate, num_generations, fitness_func):
    top_warriors = []
    population = create_a_population(pop_size)
    elite_list = []
    print "> initial population generated!"
    print "convergence threshold score: ", convergance_score_threshold
    for generation in range(num_generations):
        print "========================"
        population = run_battles(population, pop_size, elite_list)
        print "> Mutating population..."
        # Mutate population
        for i in range(pop_size):
            if i in elite_list:
                continue
            if should_mutate(): # mutate
                mutate(population[i], population, pop_size)

        print "> Evaluating fitness..."
        # Evaluate fitness
        for i in range(pop_size):
            population[i].fitness = fitness_func(population[i].genome)
            #print "fitness: ", population[i].fitness

        if selection_method is 'random': ## random selection
            # Replace bottom half of population
            # with random individuals from the top % half
            population = random_selection(population, pop_size)
        elif selection_method is 'roulette': ## roulette selection
            population = roulette_selection(population, pop_size)

        print "> Generating the next generation..."
        ## Generate a new individual and replace the weakest individual
        ## and iterate this for pop_size
        for i in range(pop_size):
            if should_crossover():
                if selection_method is 'roulette':
                    ## roulette selection
                    parent1 = roulette_selection_one(population, pop_size)
                    parent2 = roulette_selection_one(population, pop_size)
                elif selection_method is 'tournament':
                    ## tournament selection
                    tournament_size = np.random.randint(4, pop_size)
                    parent1 = tournament_selection_one(population, pop_size, tournament_size)
                    parent2 = tournament_selection_one(population, pop_size, tournament_size)
                elif selection_method is 'random': # select two parents from the bottom half
                    parent1 = population[np.random.randint(pop_size/2, pop_size)]
                    parent2 = population[np.random.randint(pop_size/2, pop_size)]
                ## generate offspring
                if(np.random.randint(1, 100) > 20):
                    child1, child2 = one_point_crossover(parent1, parent2)
                else:
                    child1, child2 = uniform_crossover(parent1, parent2)

                ## replace the weakest individuals with the children
                population = replace_weakest_warrior(population, pop_size, child1)
                population = replace_weakest_warrior(population, pop_size, child2)


        ## update elite list. We consider top two as elite
        if elite_enabled:
            index1, index2 = get_top_two(population, pop_size)
            elite_list = [index1, index2]
        
        top_score = max(pop.fitness for pop in population)
        avg_score = sum(pop.fitness for pop in population)/pop_size
        print "> Generation " + str(generation+1) + " created!"
        print "> Avg fitness in this generation: " + str(avg_score)
        print "> Top fitness in this generation: " + str(top_score)
        top_indv = find_the_strongest(population, pop_size)
        print "> Top in this generation: ", top_indv.genome 
        if top_score >= convergance_score_threshold:
            top_indv = find_the_strongest(population, pop_size)
            print "> the winner is: ", top_indv.genome 
            print "> converged :-)"
            break
        save_top_two(population, pop_size)



''' ******************* MAIN BODY ******************* '''
pop_size = 20
num_generations = 2000
mutation_rate = 25 # out of 100
crossover_rate = 25 # out of 100
number_of_rounds = 100

elite_enabled = False

insert_rate = 20
replace_rate = 20
delete_rate = 20

selection_methods = ['roulette', 'tournament', 'random']
selection_method = selection_methods[2]

benchmarks_number = 12
#total_possible_score = 3*number_of_rounds
convergance_score_threshold = 150

## Run GA
GA(pop_size, mutation_rate, num_generations, fitness_func)



