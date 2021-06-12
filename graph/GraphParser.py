from networkx import Graph
import networkx as nx


class GraphParser:

    @staticmethod
    def parseToFile(name, graph: Graph, destination="./"):
        file = open(destination + "/" + name + ".txt", "w")
        file.write(str(max(graph.adj)))
        file.write("\n")
        for n, nbrs in graph.adj.items():
            for nbr, eattr in nbrs.items():
                file.write(f"{n + 1} {nbr + 1}")
                file.write("\n")
        file.close()

    @staticmethod
    def parseFromFile(path):
        size =0
        file = open(path)
        lines = []
        while True:
            line = file.readline()
            if not line:
                break
            lines.append(line)

        graph = nx.Graph()
        for i in range(1, len(lines)):
            col1, col2 = str(lines[i]).replace("e ", "").split(" ")
            col1 = int(col1) - 1
            col2 = int(col2) - 1
            if size < col1:
                size = col1
            elif size < col2:
                size = col2

            graph.add_edge(col1, col2)
        file.close()
        return graph
