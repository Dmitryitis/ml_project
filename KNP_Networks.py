import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def draw_graph(matrix_shortest_way, begin_matrix, n):
    result_graph = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if matrix_shortest_way[i][j] != -1:
                result_graph[i][j] = matrix_shortest_way[i][j] * begin_matrix[i][j]
            else:
                result_graph[i][j] = -1

    G = nx.Graph(result_graph)
    pos = nx.spring_layout(G)
    edges = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edges)
    nx.draw(G, pos)
    plt.show()

def make_begin_edge(matrix_shortest_way):
    minim = begin_matrix[0][1]
    i_min, j_min = 0, 1
    for i in range(n):
        for j in range(i + 1, n):
            if minim > begin_matrix[i][j] and begin_matrix[i][j] != 0:
                minim = begin_matrix[i][j]
                i_min, j_min = i, j
    matrix_shortest_way[i_min][j_min] = matrix_shortest_way[j_min][i_min] = 1
    matrix_shortest_way[i_min][i_min] = matrix_shortest_way[j_min][j_min] = -1
    return matrix_shortest_way

def make_other_edges(matrix_shortest_way):
    minim = None
    i_min, j_min = 0, 1
    for i in range(n):
        if matrix_shortest_way[i][i] == -1:
            for j in range(n):
                if matrix_shortest_way[j][j] == 0:
                    if minim is None or (minim > begin_matrix[i][j] and begin_matrix[i][j] != 0):
                        minim = begin_matrix[i][j]
                        i_min, j_min = i, j
    matrix_shortest_way[i_min][j_min] = matrix_shortest_way[j_min][i_min] = 1
    matrix_shortest_way[i_min][i_min] = matrix_shortest_way[j_min][j_min] = -1
    return matrix_shortest_way

def divide_into_clusters(matrix_shortest_way):
    maxim = 0
    i_max, j_max = -1, -1
    for i in range(n):
        for j in range(i + 1, n):
            if matrix_shortest_way[i][j] == 1:
                if begin_matrix[i][j] > maxim:
                    maxim = begin_matrix[i][j]
                    i_max, j_max = i, j
    matrix_shortest_way[i_max][j_max] = 0
    matrix_shortest_way[j_max][i_max] = 0
    return matrix_shortest_way

def knp(matrix, n, k):
    matrix_shortest_way = np.zeros((n, n))
    matrix_shortest_way = make_begin_edge(matrix_shortest_way)
    for i in range(n - 2):
        matrix_shortest_way = make_other_edges(matrix_shortest_way)

    print("Вывод кратчайшего пути в графе")
    print(matrix_shortest_way)


    print("Вывод графа кратчайшего пути")
    result_graph = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if matrix_shortest_way[i][j] != -1:
                result_graph[i][j] = matrix_shortest_way[i][j] * begin_matrix[i][j]
            else:
                result_graph[i][j] = -1

    G = nx.Graph(result_graph)
    pos = nx.spring_layout(G)
    edges = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edges)
    nx.draw(G, pos)
    plt.show()


    for i in range(k - 1):
        matrix_shortest_way = divide_into_clusters(matrix_shortest_way)

    print("Путь в графе с разделением на кластеры")
    print(matrix_shortest_way)

    draw_graph(matrix_shortest_way, matrix, n)


n, k = 5, 2
begin_matrix = np.zeros((n, n))

for i in range(n):
    for j in range(i + 1, n):
        if i == 3:
            begin_matrix[i][j] = begin_matrix[j][i] = 0
        else:
            begin_matrix[i][j] = begin_matrix[j][i] = np.random.randint(1, 100)
print("Начальная матрица пути")
print(begin_matrix)

G = nx.Graph(begin_matrix)
pos = nx.spring_layout(G)
edges = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edges)
nx.draw(G, pos)
plt.show()

knp(begin_matrix, n, k)