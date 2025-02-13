from itertools import compress
import random
import time
import matplotlib.pyplot as plt

from data import *

def initial_population(individual_size, population_size):
    return [[random.choice([True, False]) for _ in range(individual_size)] for _ in range(population_size)]

def fitness(items, knapsack_max_capacity, individual):
    total_weight = sum(compress(items['Weight'], individual))
    if total_weight > knapsack_max_capacity:
        return 0
    return sum(compress(items['Value'], individual))

def population_best(items, knapsack_max_capacity, population):
    best_individual = None
    best_individual_fitness = -1
    for individual in population:
        individual_fitness = fitness(items, knapsack_max_capacity, individual)
        if individual_fitness > best_individual_fitness:
            best_individual = individual
            best_individual_fitness = individual_fitness
    return best_individual, best_individual_fitness

def genetic_algorithm(items, knapsack_max_capacity, population, n_selection, n_elite):
    population_size = len(population)
    individual_size = len(items)
    fitnesses = [fitness(items, knapsack_max_capacity, individual) for individual in population]

    new_population = []
    while len(new_population) < population_size:
        # Selection
        selected_indices = random.choices(range(population_size), weights=fitnesses, k=n_selection)
        selected_population = [population[i] for i in selected_indices]

        # Crossover
        offspring = []
        for i in range(0, n_selection, 2):
            parent1 = selected_population[i]
            parent2 = selected_population[i + 1]
            crossover_point = random.randint(1, individual_size - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            offspring.append(child1)
            offspring.append(child2)

        # Mutation
        for i in range(len(offspring)):
            for j in range(individual_size):
                if random.random() < 0.2:
                    offspring[i][j] = not offspring[i][j]

        # Elitism
        elite_population = sorted(population, key=lambda ind: fitness(items, knapsack_max_capacity, ind), reverse=True)[:n_elite]

        # New population
        new_population.extend(elite_population + offspring)

    return new_population



items, knapsack_max_capacity = get_big()
print(items)

population_size = 100
generations = 200
n_selection = 96
n_elite = 4

start_time = time.time()
best_solution = None
best_fitness = 0
population_history = []
best_history = []
population = initial_population(len(items), population_size)
for _ in range(generations):
    population_history.append(population)

    # TODO: implement genetic algorithm
    population = genetic_algorithm(items, knapsack_max_capacity, population, n_selection, n_elite)

    best_individual, best_individual_fitness = population_best(items, knapsack_max_capacity, population)
    if best_individual_fitness > best_fitness:
        best_solution = best_individual
        best_fitness = best_individual_fitness
    best_history.append(best_fitness)

end_time = time.time()
total_time = end_time - start_time
print('Best solution:', list(compress(items['Name'], best_solution)))
print('Best solution value:', best_fitness)
print('Time: ', total_time)

# plot generations
x = []
y = []
top_best = 10
for i, population in enumerate(population_history):
    plotted_individuals = min(len(population), top_best)
    x.extend([i] * plotted_individuals)
    population_fitnesses = [fitness(items, knapsack_max_capacity, individual) for individual in population]
    population_fitnesses.sort(reverse=True)
    y.extend(population_fitnesses[:plotted_individuals])
plt.scatter(x, y, marker='.')
plt.plot(best_history, 'r')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()
