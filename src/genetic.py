import numpy as np
import random

# Calcular la distancia total de una ruta
def calculate_distance(route, distance_matrix):
    return sum(distance_matrix[route[i], route[i + 1]] for i in range(len(route) - 1)) + distance_matrix[route[-1], route[0]]

# Generar una ruta aleatoria
def generate_route(num_cities):
    route = list(range(num_cities))
    random.shuffle(route)
    return route

# Generar la población inicial
def generate_population(population_size, num_cities):
    return [generate_route(num_cities) for _ in range(population_size)]

# Selección por torneo
def selection(population, distance_matrix, k=3):
    tournament = random.sample(population, k)
    tournament.sort(key=lambda route: calculate_distance(route, distance_matrix))
    return tournament[0]

# Cruce de orden (OX)
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[start:end] = parent1[start:end]
    remaining = [city for city in parent2 if city not in child]
    idx = 0
    for i in range(size):
        if child[i] == -1:
            child[i] = remaining[idx]
            idx += 1
    return child

# Mutación por intercambio
def mutation(route, mutation_rate=0.1):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route

# Algoritmo genético principal
def genetic_algorithm(distance_matrix, population_size=100, generations=500, mutation_rate=0.1):
    num_cities = len(distance_matrix)
    population = generate_population(population_size, num_cities)
    
    for _ in range(generations):
        new_population = []
        for _ in range(population_size // 2):
            parent1 = selection(population, distance_matrix)
            parent2 = selection(population, distance_matrix)
            child1 = mutation(crossover(parent1, parent2), mutation_rate)
            child2 = mutation(crossover(parent2, parent1), mutation_rate)
            new_population.extend([child1, child2])
        
        population = sorted(new_population, key=lambda route: calculate_distance(route, distance_matrix))[:population_size]
    
    best_route = population[0]
    best_distance = calculate_distance(best_route, distance_matrix)
    return best_route, best_distance

# Prueba del algoritmo
def main():
    num_cities = 10
    distance_matrix = np.random.randint(10, 100, size=(num_cities, num_cities))
    np.fill_diagonal(distance_matrix, 0)
    
    best_route, best_distance = genetic_algorithm(distance_matrix)
    print("Mejor ruta encontrada:", best_route)
    print("Distancia total:", best_distance)

if __name__ == "__main__":
    main()
