import osmnx as ox 
import networkx as nx
import json


def bfs(graph, start_node, end_node):
    queue = [(start_node, [start_node])]
    visited = set()

    while queue:
        current_node, path = queue.pop(0)
        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == end_node:
            path_length = sum(graph[path[i]][path[i + 1]][0].get('length') for i in range(len(path) - 1))
            return path, path_length

        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None, None