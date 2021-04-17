from graph.Graph import Graph


class GraphUtils:

    @staticmethod
    def has_edge(graph: Graph, v1, v2):
        return graph.matrix[v1][v2] == 1 and graph.matrix[v2][v1] == 1

    @staticmethod
    def add_edge(graph: Graph, v1, v2):
        graph.matrix[v1][v2] = 1
        graph.matrix[v2][v1] = 1
        return graph

    # d = 2m / n(n-1)
    # d = density
    # Min(d) = 0.0, Max(d) = 1.0
    # m = number of edges
    # n = number of vertex
    @staticmethod
    def calculate_density(edge_count, vertex_number):
        return (edge_count * 2) / ((vertex_number) * vertex_number - 1)
