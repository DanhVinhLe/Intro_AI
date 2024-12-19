import osmnx as ox 
import networkx as nx
import heapq
import numpy as np


def dijkstra(graph, start_node, end_node):
    distances = {node: float('infinity') for node in graph.nodes()}
    distances[start_node] = 0
    priority_queue = [(0, start_node)]
    previous_nodes = {node: None for node in graph.nodes()}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, attributes in graph[current_node].items():
            distance = current_distance + attributes[0].get('length')
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    if distances[end_node] == float('infinity'):
        return None, None
    path = []
    current_node = end_node
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path.reverse()
    return path, distances[end_node]


