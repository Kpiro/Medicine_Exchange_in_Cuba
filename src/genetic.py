import numpy as np
import random

def duplicate_matrix(input_matrix):
    """
    Dada una matriz de distancias de tamaño (N+1)×(N+1), donde:
       - índice 0: depósito,
       - índices 1..N: ciudades (punto de recogida),
    genera una nueva matriz de tamaño (2N+1)×(2N+1) que duplica cada ciudad para representar
    también el punto de entrega.

    En la nueva matriz se tiene:
       - índice 0: depósito,
       - índices 1..N: nodos de recogida,
       - índices N+1..2N: nodos de entrega.

    Se asume que la ubicación de recogida y de entrega de una ciudad es la misma,
    de modo que, por ejemplo, la distancia entre la recogida y la entrega de la misma ciudad
    (en la diagonal correspondiente) es 0.
    """
    # Número de ciudades (sin contar el depósito)
    n = input_matrix.shape[0] - 1  
    new_size = 2 * n + 1
    new_matrix = np.zeros((new_size, new_size))
    
    # Copiar las distancias relacionadas con el depósito (índice 0)
    # Desde el depósito a los nodos de recogida (1..n) y entrega (n+1..2n)
    for i in range(1, n+1):
        new_matrix[0, i] = input_matrix[0, i]   # depósito -> recogida i
        new_matrix[0, i+n] = input_matrix[0, i]   # depósito -> entrega i

        new_matrix[i, 0] = input_matrix[i, 0]     # recogida i -> depósito
        new_matrix[i+n, 0] = input_matrix[i, 0]     # entrega i -> depósito
    
    # Para cada par de ciudades (i y j, 1<=i,j<=n), se copian las distancias
    # en las 4 combinaciones:
    #   - recogida i a recogida j
    #   - recogida i a entrega j
    #   - entrega i a recogida j
    #   - entrega i a entrega j
    for i in range(1, n+1):
        for j in range(1, n+1):
            new_matrix[i, j]         = input_matrix[i, j]  # recogida i -> recogida j
            new_matrix[i, j+n]       = input_matrix[i, j]  # recogida i -> entrega j
            new_matrix[i+n, j]       = input_matrix[i, j]  # entrega i -> recogida j
            new_matrix[i+n, j+n]     = input_matrix[i, j]  # entrega i -> entrega j

    # El valor del depósito a sí mismo (posición [0,0]) se mantiene
    new_matrix[0, 0] = input_matrix[0, 0]
    
    return new_matrix

def is_valid(route, pickup):
    # La recogida se produce antes que la entrega
    n = len(pickup)
    for i in range(1,n+1):
        if route.index(i) > route.index(i+n):
            return False

    # No se puede entregar un producto a una ciudad si antes no se ha recogido el producto en la ciudad correspondiente
    for city in route:
        if city > n and route.index(pickup[city-n-1]) > route.index(city):
            return False

    return True

# Calcular la distancia total de una ruta
def calculate_distance(route, distance_matrix, pickup):
    distance = distance_matrix[route[0], route[1]] + sum(distance_matrix[route[i], route[i + 1]] for i in range(1,len(route) - 1)) + distance_matrix[route[-1], route[0]]
    if not is_valid(route, pickup):
        distance *= 2
    return distance

# Generar una ruta aleatoria
def generate_route(num_cities):
    route = list(range(1,num_cities+1))
    random.shuffle(route)
    return [0] + route + [0]

# Generar la población inicial
def generate_population(population_size, num_cities):
    return [generate_route(num_cities) for _ in range(population_size)]

# Selección por torneo
def selection(population, distance_matrix, pickup, k=3):
    tournament = random.sample(population, k)
    tournament.sort(key=lambda route: calculate_distance(route, distance_matrix, pickup))
    return tournament[0]

# Cruce de orden (OX)
def crossover(parent1, parent2):
    size = len(parent1)
    parent1 = parent1[1:size-1]
    parent2 = parent2[1:size-1]

    size -= 2
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
    return [0] + route + [0]

# Algoritmo genético principal
def genetic_algorithm(distance_matrix, pickup, population_size=100, generations=500, mutation_rate=0.1):
    distance_matrix = duplicate_matrix(distance_matrix)
    num_cities = len(distance_matrix)-1 # 2*n ciudades, n de recogidas y n de entregas
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

# Prueba del algoritmo
def main():
    distance_matrix = np.array([
        [0,  2,  9, 10, 7],
        [2,  0,  6,  4, 3],
        [9,  6,  0,  8, 5],
        [10, 4,  8,  0, 6],
        [7,  3,  5,  6, 0]
    ], dtype=float)
    pickup = [4,1,2,3]
    
    best_route, best_distance = genetic_algorithm(distance_matrix, pickup)
    print("Mejor ruta encontrada:", best_route)
    print("Distancia total:", best_distance)

if __name__ == "__main__":
    main()
