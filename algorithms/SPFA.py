import osmnx as ox 
import networkx as nx
import numpy as np
place_name = "Truc Bach, Ba Dinh, Hanoi, Vietnam"
graph_file = 'map/map_trucbach.graphml'

graph = ox.load_graphml(graph_file)


def spfa(graph, start_node, end_node):
    nodes = list(graph.nodes())
    dist = {node: float('inf') for node in nodes}
    in_queue = {node: False for node in graph.nodes}
    dist[start_node] = 0
    queue = [start_node]
    in_queue[start_node] = True
    prev_node = {node: None for node in nodes}
    while queue:
        u = queue.pop(0)
        in_queue[u] = False
        for v in graph.neighbors(u):
            weight = graph[u][v][0].get('length', 1)
            if dist[v] > dist[u] + weight:
                dist[v] = dist[u] + weight
                prev_node[v] = u
                if not in_queue[v]:
                    in_queue[v] = True
                    queue.append(v)
    if dist[end_node] == float('inf'):
        return None, None
    path = [end_node]
    en = end_node
    while en != start_node:
        en = prev_node[en]
        path.append(en)
    return path[::-1], dist[end_node]

source_node = list(graph.nodes)[1]  # Example source node
target_node = list(graph.nodes)[109]  # Example target node
path, shortest_distance = spfa(graph, source_node, target_node)
print(f"The shortest distance from node {source_node} to node {target_node} is {shortest_distance} km")