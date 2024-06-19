import random
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
from gurobi_optimods import datasets
from gurobi_optimods.min_cost_flow import min_cost_flow_scipy 

with open('data.txt', 'r') as file:
    # Читаем строки из файла
    lines = file.readlines()
    matrix = []
    for line in lines:
        
        row = list(map(int, line.split()))
       
        matrix.append(row)

# Выводим матрицу
print(matrix[1][1])


num_vertices = random.randint(matrix[1][0], matrix[1][1])
num_edges = random.randint(matrix[2][0], matrix[2][1])

graph_with_weights = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]

# Заполнение графа случайными весами
for _ in range(num_edges):
    vertex1 = random.randint(0, num_vertices-1)
    vertex2 = random.randint(0, num_vertices-1)
    while vertex2 == vertex1:
        vertex2 = random.randint(0, num_vertices-1)
    weight = random.randint(matrix[3][0], matrix[3][1])  # Генерация случайного веса от 1 до 100
    graph_with_weights[vertex1][vertex2] = weight
    graph_with_weights[vertex2][vertex1] = weight  # Граф невзвешенный, поэтому делаем его симметричным

# Вывод графа с весами
for row in graph_with_weights:
    print(row)

graph = csr_matrix(graph_with_weights)
print("Максимальный поток:",maximum_flow(graph, 0, 1).flow_value)

graph, capacities, cost, demands = datasets.simple_graph_scipy()
obj, sol = min_cost_flow_scipy(graph, capacities, cost, demands, verbose=False)
print("Поток минимальной стоимости:", sol)