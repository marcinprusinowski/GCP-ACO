import networkx as nx
import matplotlib.pyplot as plt
from networkx import Graph


class GraphVisualization:
    def __init__(self, graph: Graph):
        # visual is a list which stores all
        # the set of edges that constitutes a
        # graph
        self.visual = []
        for n, nbrs in graph.adj.items():
            for nbr, eattr in nbrs.items():
                self.visual.append([n+1, nbr+1])

    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()
