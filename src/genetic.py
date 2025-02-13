import numpy as np
import random

def duplicate_matrix(input_matrix):
    n = input_matrix.shape[0] - 1
    new_size = 2 * n + 1
    new_matrix = np.zeros((new_size, new_size))
    
    # Copiar las distancias relacionadas con el depósito
    new_matrix[0, 1:n + 1] = input_matrix[0, 1:n + 1]
    new_matrix[0, n + 1:2 * n + 1] = input_matrix[0, 1:n + 1]
    new_matrix[1:n + 1, 0] = input_matrix[1:n + 1, 0]
    new_matrix[n + 1:2 * n + 1, 0] = input_matrix[1:n + 1, 0]
    
    # Copiar las distancias entre ciudades
    new_matrix[1:n + 1, 1:n + 1] = input_matrix[1:n + 1, 1:n + 1]
    new_matrix[1:n + 1, n + 1:2 * n + 1] = input_matrix[1:n + 1, 1:n + 1]
    new_matrix[n + 1:2 * n + 1, 1:n + 1] = input_matrix[1:n + 1, 1:n + 1]
    new_matrix[n + 1:2 * n + 1, n + 1:2 * n + 1] = input_matrix[1:n + 1, 1:n + 1]
    
    # Mantener el valor del depósito a sí mismo
    new_matrix[0, 0] = input_matrix[0, 0]
    
    return new_matrix

def is_valid(route, pickup):
    n = len(pickup)
    route_positions = {city: idx for idx, city in enumerate(route)}
    
    # La recogida se produce antes que la entrega
    for i in range(1, n + 1):
        if route_positions[i] > route_positions[i + n]:
            return False

    # No se puede entregar un producto a una ciudad si antes no se ha recogido el producto en la ciudad correspondiente
    for city in route:
        if city > n and route_positions[pickup[city - n - 1]] > route_positions[city]:
            return False

    return True

def calculate_distance(route, distance_matrix, pickup):
    distance = distance_matrix[route[0], route[1]] + sum(distance_matrix[route[i], route[i + 1]] for i in range(1, len(route) - 1)) + distance_matrix[route[-1], route[0]]
    if not is_valid(route, pickup):
        distance *= 2
    return distance

def generate_route(num_cities):
    route = np.random.permutation(num_cities) + 1
    return [0] + route.tolist() + [0]

def generate_population(population_size, num_cities):
    return [generate_route(num_cities) for _ in range(population_size)]

def selection(population, distance_matrix, pickup, k=3):
    tournament = random.sample(population, k)
    return min(tournament, key=lambda route: calculate_distance(route, distance_matrix, pickup))

def crossover(parent1, parent2):
    size = len(parent1) - 2
    start, end = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[start:end] = parent1[start + 1:end + 1]
    remaining = [city for city in parent2[1:-1] if city not in child]
    idx = 0
    for i in range(size):
        if child[i] == -1:
            child[i] = remaining[idx]
            idx += 1
    return [0] + child + [0]

def mutation(route, mutation_rate=0.1):
    if random.random() < mutation_rate:
        i, j = random.sample(range(1, len(route) - 1), 2)
        route[i], route[j] = route[j], route[i]
    return route

def genetic_algorithm(distance_matrix, pickup, population_size=75, generations=375, mutation_rate=0.1):
    distance_matrix = duplicate_matrix(distance_matrix)
    num_cities = len(distance_matrix) - 1
    population = generate_population(population_size, num_cities)
    
    for _ in range(generations):
        new_population = []
        for _ in range(population_size // 2):
            parent1 = selection(population, distance_matrix, pickup)
            parent2 = selection(population, distance_matrix, pickup)
            child1 = mutation(crossover(parent1, parent2), mutation_rate)
            child2 = mutation(crossover(parent2, parent1), mutation_rate)
            new_population.extend([child1, child2])
        
        population = sorted(new_population, key=lambda route: calculate_distance(route, distance_matrix, pickup))[:population_size]
    
    best_route = population[0]
    best_distance = calculate_distance(best_route, distance_matrix, pickup)
    return best_route, best_distance

def main():
    distance_matrix = np.array([
        [0,  2,  9, 10, 7],
        [2,  0,  6,  4, 3],
        [9,  6,  0,  8, 5],
        [10, 4,  8,  0, 6],
        [7,  3,  5,  6, 0]
    ], dtype=float)
    pickup = [4, 1, 2, 3]
    
    best_route, best_distance = genetic_algorithm(distance_matrix, pickup)
    print("Mejor ruta encontrada:", best_route)
    print("Distancia total:", best_distance)

if __name__ == "__main__":
    main()