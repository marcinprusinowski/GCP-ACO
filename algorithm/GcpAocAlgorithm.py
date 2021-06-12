import random

import networkx as nx
import numpy as np

from graph.GraphCriteria import GraphCriteria
from graph.GraphGenerator import GraphGenerator


class Ant:

    def __init__(self, alpha=1, beta=1):
        self.graph = None
        self.colors = {}
        self.start = None
        self.visited = []
        self.unvisited = []
        self.alpha = alpha
        self.beta = beta
        self.distance = 0
        self.number_colisions = 0
        self.colors_available = []
        self.colors_assigned = []

    def initialize(self, g, colors, start=None):
        self.colors_available = sorted(colors.copy())

        keys = [n for n in g_nodes_int]
        self.colors_assigned = {key: None for key in keys}

        if start is None:
            self.start = random.choice(g_nodes_int)
        else:
            self.start = start

        self.visited = []
        self.unvisited = g_nodes_int.copy()

        if len(self.visited) == 0:
            self.assign_color(self.start, self.colors_available[0])
        return self

    def assign_color(self, node, color):
        self.colors_assigned[node] = color
        self.visited.append(node)
        self.unvisited.remove(node)

    def colorize(self):
        len_unvisited = len(self.unvisited)
        tabu_colors = []
        # assign color to each unvisited node
        for i in range(len_unvisited):
            next = self.next_candidate()
            tabu_colors = []
            # add colors of neighbours to tabu list
            for j in range(number_nodes):
                if adj_matrix[next, j] == 1:
                    tabu_colors.append(self.colors_assigned[j])
            # assign color with the smallest number that is not tabu
            for k in self.colors_available:
                if k not in tabu_colors:
                    self.assign_color(next, k)
                    break
        # save distance of the current solution
        self.distance = len(set(self.colors_assigned.values()))

    def dsat(self, node=None):
        if node is None:
            node = self.start
        col_neighbors = []
        for j in range(number_nodes):
            if adj_matrix[node, j] == 1:
                col_neighbors.append(self.colors_assigned[j])
        return len(set(col_neighbors))

    def si(self, node, adj_node):
        return phero_matrix[node, adj_node]

    def next_candidate(self):
        if len(self.unvisited) == 0:
            candidate = None
        elif len(self.unvisited) == 1:
            candidate = self.unvisited[0]
        else:
            max_value = 0
            heuristic_values = []
            candidates = []
            candidates_available = []
            for j in self.unvisited:
                heuristic_values.append((self.si(self.start, j) ** self.alpha) * (self.dsat(j) ** self.beta))
                candidates.append(j)
            max_value = max(heuristic_values)
            for i in range(len(candidates)):
                if heuristic_values[i] >= max_value:
                    candidates_available.append(candidates[i])
            candidate = random.choice(candidates_available)
        self.start = candidate
        return candidate

    def pheromone_trail(self):
        phero_trail = np.zeros((number_nodes, number_nodes), float)
        for i in g_nodes_int:
            for j in g_nodes_int:
                if self.colors_assigned[i] == self.colors_assigned[j]:
                    phero_trail[i, j] = 1
        return phero_trail


# initiate a selection of colors for the coloring and compute the min. number of colors needed for a proper coloring
def init_colors(g):
    # grundy (max degree+1)
    colors = []
    grundy = len(nx.degree_histogram(g))
    for c in range(grundy):
        colors.append(c)
    return colors


# create a pheromone matrix with init pheromone values: 1 if nodes not adjacent, 0 if adjacent
def init_pheromones(g):
    phero_matrix = np.ones((number_nodes, number_nodes), float)
    for node in g:
        for adj_node in g.neighbors(node):
            phero_matrix[node, adj_node] = 0
    return phero_matrix


# calculate the adjacency matrix of the graph
def adjacency_matrix(g):
    adj_matrix = np.zeros((number_nodes, number_nodes), int)
    for node in g_nodes_int:
        for adj_node in g.neighbors(node):
            adj_matrix[node, adj_node] = 1
    return adj_matrix


# creates ants colony based on given number
def create_colony():
    ants = []
    ants.extend([Ant().initialize(g, colors) for i in range(number_ants)])
    return ants


# apply given decay to pheromone matrix
def apply_decay():
    for node in g_nodes_int:
        for adj_node in g_nodes_int:
            phero_matrix[node, adj_node] = phero_matrix[node, adj_node] * (1 - phero_decay)


# select colony's best solution
# update pheromone_matrix according to the elite ( best )  solution
# return elite ( best ) solution (coloring) with its distance (number of used colors)
def update_elite():
    global phero_matrix
    # select elite
    best_dist = 0
    elite_ant = None
    for ant in ants:
        if (best_dist == 0):
            best_dist = ant.distance
            elite_ant = ant
        elif (ant.distance < best_dist):
            best_dist = ant.distance
            elite_ant = ant
    # update global phero_matrix
    elite_phero_matrix = elite_ant.pheromone_trail()
    phero_matrix = phero_matrix + elite_phero_matrix
    return elite_ant.distance, elite_ant.colors_assigned


# input_graph - a networkx graph to be colored (node coloring)
# num_ants - number of ants in the colony
# iter - number of iterations to be performed
# a - relative importance of elite pheromones
# b - relative importance of heuristic value (DSAT)
# decay - evaporation of pheromones after each iteration
def solve(input_graph, num_ants=20, iter=20, a=1, b=3, decay=0.3):
    global g
    global number_nodes
    global g_nodes_int
    global number_ants
    global alpha
    global beta
    global phero_decay
    global adj_matrix
    global phero_matrix
    global colors
    global ants

    # params
    g = input_graph
    number_ants = num_ants
    number_iterations = iter
    alpha = a  # relative importance of pheromone (si_ij)
    beta = b  # relative importance of heuristic value (n_ij)
    phero_decay = decay  # rate of pheromone decay

    # results
    final_solution = {}  # coloring of the graph
    final_costs = 0  # number of colors in the solution
    iterations_needed = 0

    # init
    number_nodes = max(g.adj) + 1
    g_nodes_int = []
    for node in g.nodes():
        g_nodes_int.append(node)
    g_nodes_int = list(map(int, sorted(g_nodes_int)))
    adj_matrix = adjacency_matrix(g)
    colors = init_colors(g)
    phero_matrix = init_pheromones(g)

    # ACO_GCP daemon
    for i in range(number_iterations):
        # create colony
        ants = []
        ants = create_colony()
        # let colony find solutions
        count = 1
        for ant in ants:
            ant.colorize()
        # apply decay rate
        apply_decay()
        # select elite and update si_matrix
        elite_dist, elite_sol = update_elite()
        # estimate global solution so far
        if final_costs == 0:
            final_costs = elite_dist
            final_solution = elite_sol
            iterations_needed = i + 1
        elif elite_dist < final_costs:
            final_costs = elite_dist
            final_solution = elite_sol
            iterations_needed = i + 1
        print(final_costs)
    return final_costs, final_solution, iterations_needed


g = None  # graph to be colored
number_nodes = 0
g_nodes_int = []
number_ants = 0
alpha = 0
beta = 0
phero_decay = 0
adj_matrix = np.zeros((number_nodes, number_nodes), int)
phero_matrix = np.ones((number_nodes, number_nodes), float)
colors = []
ants = []

if __name__ == '__main__':
    criteria = GraphCriteria(200, 0.7)
    g = GraphGenerator.generate(criteria)
    cost, solution, iterations = solve(g)
    print(iterations)













