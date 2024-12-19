import osmnx as ox 
import networkx as nx
import numpy as np

def bellman_ford(graph, start_node, end_node):
    # Initialize distances from source to all other nodes as infinity
    distance = {node: float('inf') for node in graph.nodes}
    distance[start_node] = 0
    predecessor = {node: None for node in graph.nodes}

    # Relax edges |V| - 1 times
    for _ in range(len(graph.nodes) - 1):
        for u, v, data in graph.edges(data=True):
            weight = data.get('length')
            if distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                predecessor[v] = u
    if distance[end_node] == float('inf'):
        return None, None
    path = []
    current_node = end_node
    while current_node is not None:
        path.append(current_node)
        current_node = predecessor[current_node]
    path.reverse()

    return path, distance[end_node]
