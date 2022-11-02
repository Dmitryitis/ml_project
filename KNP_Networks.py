import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def weight(n):
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            if np.random.randint(0, 2) == 1:
                matrix[i][j] = matrix[j][i] = np.random.randint(10, 100)
    return matrix


if __name__ == '__main__':
    n = 10
    k = 3
    matrix = weight(n)
    print(matrix)
    G = nx.Graph(matrix)
    pos = nx.spring_layout(G)
    edges = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edges)
    nx.draw(G, pos)
    plt.show()

    sort_weight = sorted(item[2] for item in G.edges.data('weight'))

    remove_edges = []

    for item in sort_weight[-k:]:
        for (u, v, wt) in G.edges.data('weight'):
            if item == wt:
                remove_edges.append((u,v))
                break

    for edge in remove_edges:
        G.remove_edge(edge[0],edge[1])


    nx.draw_networkx_edge_labels(G, pos, edges)
    nx.draw(G, pos)
    plt.show()