import networkx as nx
from docplex.mp.model import Model

def enumerate_cycles(graph, L):
    cycles = []
    for cycle in nx.simple_cycles(graph):
        if len(cycle) <= L:
            cycles.append(cycle)
    return cycles

# Ejemplo de construccion del grafo dirigido
G = nx.DiGraph()
G.add_edge('A', 'B', weight=10)
G.add_edge('B', 'C', weight=5)
G.add_edge('C', 'A', weight=7)
G.add_edge('B', 'D', weight=3)
G.add_edge('D', 'B', weight=4)

L = 20  # Longitud maxima permitida para un ciclo
cycles = enumerate_cycles(G, L)

# Creacion del modelo CPLEX mediante DOCplex
mdl = Model("CycleCover")

cycle_vars = {}
cycle_weights = {}
for i, cycle in enumerate(cycles):
    # Calcular el peso del ciclo: suma de los pesos de las aristas del ciclo
    weight = sum(G[u][v]['weight'] for u, v in zip(cycle, cycle[1:] + [cycle[0]]))
    cycle_vars[i] = mdl.binary_var(name=f"cycle_{i}")
    cycle_weights[i] = weight

# Funcion objetivo: maximizar la suma de pesos de los ciclos seleccionados
mdl.maximize(mdl.sum(cycle_weights[i] * cycle_vars[i] for i in cycle_vars))

# Restriccion: cada nodo puede pertenecer a lo sumo a un ciclo seleccionado
for node in G.nodes():
    mdl.add_constraint(
        mdl.sum(cycle_vars[i] for i, cycle in enumerate(cycles) if node in cycle) <= 1,
        ctname=f"node_{node}"
    )

solution = mdl.solve(log_output=True)
if solution:
    print(solution)
    for i, cycle in enumerate(cycles):
        if cycle_vars[i].solution_value > 0.5:
            print("Selected cycle:", cycle, "with weight", cycle_weights[i])
