from random import choice

import numpy as np

from graph.Graph import Graph
from graph.GraphCriteria import GraphCriteria
from graph.GraphUtils import GraphUtils


class GraphGenerator:

    @staticmethod
    def generate(criteria: GraphCriteria):
        graph = Graph(criteria.size)
        edge_count = 0
        current_density = 0.0
        graph_size = criteria.size

        unvisited = []
        for i in range(0, graph_size):
            nested_arr = []
            for j in range(0, graph_size):
                nested_arr.append(j)
            unvisited.append(nested_arr)

        current_vertex = np.random.randint(graph_size)

        while current_density < criteria.density:
            visited = unvisited[current_vertex]
            next_vertex_value = choice(visited)
            next_vertex_index = visited.index(next_vertex_value)

            if next_vertex_value:
                visited.pop(next_vertex_index)

            if not criteria.loops and current_vertex == next_vertex_value:
                continue

            if not GraphUtils.has_edge(graph, current_vertex, next_vertex_value):
                GraphUtils.add_edge(graph, current_vertex, next_vertex_value)
                current_vertex = next_vertex_value
                edge_count += 1
                current_density = GraphUtils.calculate_density(edge_count, graph_size)

        return graph