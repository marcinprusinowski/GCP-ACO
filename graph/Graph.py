import numpy as np


class Graph:
    def __init__(self, size):
        self.size = size
        self.matrix = np.array(np.zeros((size, size), np.int32))