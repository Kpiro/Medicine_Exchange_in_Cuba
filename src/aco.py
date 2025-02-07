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

def is_valid_next_city(next_city, route, interactions, n):
    """
    Verifica si el nodo candidato next_city se puede agregar a la ruta, cumpliendo:
    
    - Si next_city es un nodo de recogida (1 <= next_city <= n): siempre es válido.
    
    - Si next_city es un nodo de entrega (n+1 <= next_city <= 2*n):
         * Se requiere que el punto de recogida asociado ya esté en la ruta.
         * La pareja “impuesta” por interactions se interpreta así: para un nodo de entrega d,
           definimos j = d - n (es decir, la orden asociada) y se espera que se haya visitado el nodo:
               required_pickup = interactions[j-1] + 1
           (se asume que interactions es 0-indexado y que los nodos de recogida son 1...n).
    """
    # Si el nodo es de recogida, no hay restricción.
    if next_city <= n:
        return True
    else:
        # next_city es un nodo de entrega.
        # Identificamos la orden: j = next_city - n, con j en 1..n.
        j = next_city - n  
        # El arreglo interactions (0-indexado) indica que para la orden j se requiere haber visitado
        # el nodo de recogida: interactions[j-1] + 1.
        required_pickup = interactions[j - 1] + 1  
        # La restricción se cumple si el nodo required_pickup ya está en la ruta.
        return (required_pickup in route)

def construct_route(distance_matrix, pheromone, alpha, beta, interactions):
    """
    Construye una ruta (ciclo hamiltoniano) para una hormiga que respeta las restricciones
    de recogida y entrega, según el arreglo interactions.
    
    Se asume que la matriz de distancias corresponde a una instancia duplicada:
       - Nodo 0: depósito.
       - Nodos 1 a n: puntos de recogida.
       - Nodos n+1 a 2*n: puntos de entrega.
       
    El arreglo interactions (de longitud n) se interpreta de la siguiente forma:
       para cada i en 0..n-1, interactions[i] = k significa que la mercancía recogida en el nodo (k+1)
       debe entregarse en el nodo (i + n + 1).
    
    Antes de agregar un nodo candidato a la ruta, se verifica (usando is_valid_next_city) que se cumplan:
      1. Si se trata de un nodo de entrega, su correspondiente punto de recogida ya fue visitado.
      2. Si se impone una restricción de intercambio (array interactions), se verifica que se haya visitado
         el nodo indicado.
    """
    total_nodes = len(distance_matrix)       # total_nodes = 2*n + 1
    n = (total_nodes - 1) // 2                # cantidad de ciudades (en modo pickup)
    
    route = [0]  # Inicia en el depósito.
    # Inicialmente, los nodos disponibles son 1 hasta 2*n (pickup y delivery)
    unvisited = list(range(1, total_nodes))
    
    # Para el primer movimiento, solo se permiten nodos de recogida (1 <= city <= n),
    # ya que no se puede entregar sin recoger.
    valid_candidates = [city for city in unvisited if city <= n]
    if not valid_candidates:
        valid_candidates = unvisited  # (por si acaso, aunque en principio debería haber al menos uno)
    current = random.choice(valid_candidates)
    route.append(current)
    unvisited.remove(current)
    
    while unvisited:
        # Filtrar candidatos válidos según las restricciones.
        valid_candidates = []
        for city in unvisited:
            if is_valid_next_city(city, route, interactions, n):
                valid_candidates.append(city)
                
        # Si ninguno de los candidatos restantes es válido, se opta por forzar la elección
        # (esto generará una solución inviable que luego podrá ser penalizada).
        if not valid_candidates:
            valid_candidates = unvisited
        
        probabilities = []
        for city in valid_candidates:
            # La probabilidad es proporcional a (feromona^alpha)*(heurística^beta)
            # donde la heurística es 1/distance
            pher = pheromone[current][city] ** alpha
            distance = distance_matrix[current][city]
            # Evitar división por cero
            if distance == 0:
                distance = 1e-10
            heuristic = (1.0 / distance) ** beta
            probabilities.append(pher * heuristic)
        probabilities = np.array(probabilities, dtype=float)
        probabilities /= probabilities.sum()
        # Seleccionar la siguiente ciudad de forma aleatoria según las probabilidades calculadas
        next_city = random.choices(valid_candidates, weights=probabilities)[0]
        route.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    # Regresar al depósito para cerrar el ciclo.
    route.append(0)
    return route

def route_length(route, distance_matrix):
    """
    Calcula la longitud total del ciclo (ruta) recorriendo todas las ciudades
    y volviendo al punto de inicio.
    """
    length = 0
    n = len(route)
    for i in range(n):
        length += distance_matrix[route[i]][route[(i + 1) % n]]
    return length

def aco_tsp(distance_matrix, interactions, num_ants=20, num_iterations=100, alpha=1, beta=2, evaporation_rate=0.5, Q=100):
    """
    Implementación clásica del algoritmo de colonia de hormigas para el TSP.

    Parámetros:
      - distance_matrix: Matriz (numpy.array) de distancias entre ciudades.
      - num_ants: Número de hormigas por iteración.
      - num_iterations: Número de iteraciones a ejecutar.
      - alpha: Exponente que pondera la influencia de la feromona.
      - beta: Exponente que pondera la influencia de la heurística (inversa de la distancia).
      - evaporation_rate: Tasa de evaporación de la feromona en cada iteración (0 < evaporacion < 1).
      - Q: Constante usada para depositar feromona (se suele usar Q / distancia).
      
    Retorna:
      - best_route: La mejor ruta (lista de índices de ciudades) encontrada.
      - best_length: La longitud de la mejor ruta.
    """
    n = len(distance_matrix)-1
    distance_matrix = duplicate_matrix(distance_matrix)
    # Inicializar la matriz de feromonas con un valor pequeño y constante
    pheromone = np.ones((2*n+1, 2*n+1))
    
    best_route = None
    best_length = float('inf')
    
    for iteration in range(num_iterations):
        routes = []
        lengths = []
        
        # Cada hormiga construye una ruta
        for ant in range(num_ants):
            route = construct_route(distance_matrix, pheromone, alpha, beta, interactions)
            length = route_length(route, distance_matrix)
            routes.append(route)
            lengths.append(length)
            
            if length < best_length:
                best_length = length
                best_route = route
        
        # Evaporación de la feromona: se reduce la feromona en todas las aristas.
        pheromone *= (1 - evaporation_rate)
        
        # Actualización de feromonas: cada hormiga deposita feromona de forma inversamente proporcional
        # a la longitud de su ruta.
        for route, length in zip(routes, lengths):
            delta_pheromone = Q / length
            for i in range(n):
                from_city = route[i]
                to_city = route[(i + 1) % n]  # Conecta de vuelta al inicio al final
                pheromone[from_city][to_city] += delta_pheromone
                pheromone[to_city][from_city] += delta_pheromone  # Si el grafo es simétrico
        
        # print(f"Iteración {iteration+1}/{num_iterations} - Mejor longitud: {best_length:.2f}")
    
    return best_route, best_length

# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo: 5 ciudades con una matriz de distancias simétrica.
    distance_matrix = np.array([
        [0,  2,  9, 10, 7],
        [2,  0,  6,  4, 3],
        [9,  6,  0,  8, 5],
        [10, 4,  8,  0, 6],
        [7,  3,  5,  6, 0]
    ], dtype=float)
    interactions = [4,1,2,3]
    best_route, best_length = aco_tsp(distance_matrix, interactions,
                                      num_ants=20,
                                      num_iterations=100,
                                      alpha=1,
                                      beta=2,
                                      evaporation_rate=0.5,
                                      Q=100)
    
    print("\nMejor ruta encontrada:", best_route)
    print("Longitud de la mejor ruta:", best_length)
