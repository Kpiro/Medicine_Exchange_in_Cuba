import sys
from typing import List, Tuple

def total_cost(mask: int, curr: int, m: int, cost: List[List[int]], memo: List[List[int]], path: List[List[int]], cicle: List[int]) -> int:
    n = (m + 1) // 2

    # Caso base: si todos los productos fueron entregados, devolver el costo de regresar al origen (0)
    if mask == (1 << m) - 1:
        path[curr][mask] = 0
        return cost[curr][0]

    # Si el resultado ya está en la memoización, devolverlo
    if memo[curr][mask] != -1:
        return memo[curr][mask]

    ans = sys.maxsize
    next_city = -1

    # Intentar visitar cada lugar que no ha sido visitado aún
    for i in range(m):
        city = i if i < n else ((i % n) + 1)

        if ((mask & (1 << i)) == 0 and i < n) or (mask & (1 << i)) == 0 and i >= n and (mask & (1 << city)) != 0 and (mask & (1 << cicle[city])) != 0:
            # Si se visita un lugar para entregar el producto, el producto tiene que haber sido recogido antes
            # Si se visita un lugar para recoger un producto, no puede haber sido visitado
            new_cost = cost[curr][i] + total_cost(mask | (1 << i), i, m, cost, memo, path, cicle)
            if new_cost < ans:
                ans = new_cost
                next_city = i

    # Almacenar el siguiente lugar en la ruta
    path[curr][mask] = next_city

    memo[curr][mask] = ans
    return ans


def best_delivery(cost: List[List[int]], pickup_place: List[int]) -> Tuple[int, List[int]]:
    n = len(cost)
    m = 2 * n - 1
    new_cost = [[0] * m for _ in range(m)]

    # Duplicar la matriz de entrada para representar las recogidas y entregas de productos
    for i in range(m):
        for j in range(m):
            r = i if i < n else i % n + 1
            c = j if j < n else j % n + 1
            new_cost[i][j] = cost[r][c]

    memo = [[-1] * (1 << m) for _ in range(m)]
    path = [[-1] * (1 << m) for _ in range(m)]

    # Comenzar desde el origen, y solo el lugar 0 está visitado inicialmente (máscara = 1)
    min_cost = total_cost(1, 0, m, new_cost, memo, path, pickup_place)

    # Reconstruir la ruta
    route = []
    mask = 1
    curr_city = 0
    route.append(curr_city)

    while True:
        next_city = path[curr_city][mask]
        route.append(next_city)
        mask |= (1 << next_city)
        if next_city == 0:
            break
        curr_city = next_city

    return min_cost, route


if __name__ == "__main__":
    cost = [
        [0, 3, 4, 2, 7],
        [3, 0, 4, 6, 3],
        [4, 4, 0, 5, 8],
        [2, 6, 5, 0, 6],
        [7, 3, 8, 6, 0]
    ]
    pickup_place = [-1, 2, 4, 1, 3]

    min_cost, route = best_delivery(cost, pickup_place)
    print(f"Costo mínimo: {min_cost}")
    print("Ruta:", end=" ")
    for city in route:
        r = city if city < len(cost) else city % len(cost) + 1
        print(r, end=" ")
    print()