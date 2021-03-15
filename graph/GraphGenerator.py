import numpy as np

from graph import Graph, GraphCriteria
from graph.GraphUtils import GraphUtils


class GraphGenerator:

    @staticmethod
    def generate(graph: Graph, criteria: GraphCriteria):
        edge_count = 0
        current_density = 0.0
        graph_size = graph.size

        current_vertex = np.random.randint(graph_size)

        while current_density < criteria.density:
            next_vertex = np.random.randint(graph_size)
            if not GraphUtils.has_edge(graph, current_vertex, next_vertex):
                GraphUtils.add_edge(graph, current_vertex, next_vertex, criteria.loops)
                current_vertex = next_vertex
                edge_count += 1
                current_density = GraphUtils.calculate_density(edge_count, graph_size)