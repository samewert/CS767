import csv
import networkx as nx
import matplotlib.pyplot as plt

def readGraphFromCsv(filename):
    graph = nx.DiGraph()
    with open(filename, 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            parentNode = row[0]
            childNodes = row[1:]
            for child in childNodes:
                child = child.strip()
                # child = child.replace('Node','')
                # parentNode = parentNode.replace('Node', '')
                graph.add_edge(parentNode, child)
    return graph

def calculatePageRank(graph):
    pagerank = nx.pagerank(graph)
    return pagerank

def drawGraph(graph, pagerank):
    nodeSizes = [pagerank[node] * 3000 for node in graph.nodes()]
    pos = nx.spectral_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=nodeSizes, node_color='skyblue', font_size=8, font_weight='bold')
    plt.savefig('graphVisualization.png')
    plt.show()


if __name__ == "__main__":
    filename = 'csv/graph.csv'
    graph = readGraphFromCsv(filename)
    pagerank = calculatePageRank(graph)
    print(pagerank)
    for rank in pagerank:
        print('{} = {}'.format(rank, pagerank[rank]))
    drawGraph(graph, pagerank)
