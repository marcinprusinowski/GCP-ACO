from graph.GraphCriteria import GraphCriteria
from graph.GraphGenerator import GraphGenerator
from graph.GraphParser import GraphParser

if __name__ == '__main__':
    criteria = GraphCriteria(100, 0.6, False)
    graph = GraphGenerator.generate(criteria)
    GraphParser.parseToFile("test", graph)
