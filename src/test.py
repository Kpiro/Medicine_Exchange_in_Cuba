import random
import numpy as np
import matplotlib.pyplot as plt
from tsp import best_delivery
from aco import aco_tsp
from genetic import genetic_algorithm

def create_matrix(n: int):
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n): 
            value = random.randint(1, 50)
            matrix[i][j] = value
            matrix[j][i] = value 
    return matrix

def create_pickup(n: int):
    arr = list(range(1,n+1))
    random.shuffle(arr)
    return arr
    
def test(iter: int):
    tsp_arr = []
    aco_arr = []
    genetic_arr = []

    for i in range(3,iter+1):
        matrix = create_matrix(i)
        pickup = create_pickup(i-1)
        cost_tsp, _ = best_delivery(matrix, [-1] + pickup)
        sum_aco = 0
        for j in range(30):
            _, cost_aco = aco_tsp(np.array(matrix, dtype=float), pickup)
            sum_aco += cost_aco
        cost_aco = sum_aco//30
        sum_genetic = 0
        for j in range(30):
            _, cost_genetic = genetic_algorithm(np.array(matrix, dtype=float), pickup)
            sum_genetic += cost_genetic
        cost_genetic = sum_genetic//30
        
        tsp_arr.append((i,cost_tsp))
        aco_arr.append((i,int(cost_aco)))
        genetic_arr.append((i,int(cost_genetic)))

    # Extraer los valores de x e y para cada array
    x1, y1 = zip(*tsp_arr)  # Desempaquetar las tuplas en dos listas separadas
    x2, y2 = zip(*aco_arr)
    x3, y3 = zip(*genetic_arr)

    # Crear el gráfico
    plt.plot(x1, y1, marker='o', label='TSP')  # Graficar array1
    plt.plot(x2, y2, marker='s', label='ACO')  # Graficar array2
    plt.plot(x3, y3, marker='^', label='AG')  # Graficar array3

    # Añadir etiquetas y título
    plt.xlabel('Clientes')
    plt.ylabel('Costo mínimo de la ruta')
    plt.title('TSP vs ACO y AG')
    plt.legend()  # Mostrar leyenda

    # Mostrar el gráfico
    plt.show()

    print(tsp_arr)
    print(aco_arr)
    print(genetic_arr)

test(12)