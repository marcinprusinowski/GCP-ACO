from random import choice

import numpy as np
import networkx as nx

from graph.GraphCriteria import GraphCriteria


class GraphGenerator:

    @staticmethod
    def calculate_density(edge_count, vertex_number):
        return (edge_count * 2) / ((vertex_number) * vertex_number - 1)

    @staticmethod
    def generate(criteria: GraphCriteria):
        graph = nx.Graph()
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

            if not graph.has_edge(current_vertex, next_vertex_value):
                graph.add_edge(current_vertex, next_vertex_value)
                current_vertex = next_vertex_value
                edge_count += 1
                current_density = GraphGenerator.calculate_density(edge_count, graph_size)

        return graph