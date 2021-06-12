from random import choice

import numpy as np
from networkx import Graph

from graph.GraphCriteria import GraphCriteria
from graph.GraphGenerator import GraphGenerator
from graph.GraphParser import GraphParser
from graph.GraphVisualisation import GraphVisualization


def getLowestPossibleColor(colors_used, adj, size):
    unavailable_colors = []
    for i in adj:
        if colors_used[i] != 0:
            unavailable_colors.append(colors_used[i])
    for j in range(1, size):
        if j not in unavailable_colors:
            return j


def solve(graph: Graph):
    size = max(graph.adj) + 1
    collored_V = np.array(np.zeros(size), np.int32)
    picked = []
    for i in range(0, size + 1):
        picked.append(i)
    for n, nbrs in graph.adj.items():
        random = choice(picked)
        index = picked.index(random)
        picked.pop(index)
        collored_V[n] = getLowestPossibleColor(collored_V, list(nbrs), size)
    return max(collored_V), collored_V


if __name__ == '__main__':
    criteria = GraphCriteria(100, 0.7)
    g = GraphGenerator.generate(g)
    cost, solution = solve(g)
    print(cost)
