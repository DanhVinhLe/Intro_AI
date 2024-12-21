import osmnx as ox 
import networkx as nx
import json
from math import radians, cos, sin, asin, sqrt
# Greedy Best First Search
# heuristic function to estimate the cost from the current node to the goal node
def heuristic(graph, node, end_node):
    node_x, node_y = graph.nodes[node]['x'], graph.nodes[node]['y']
    goal_x, goal_y = graph.nodes[end_node]['x'], graph.nodes[end_node]['y']
    lon1, lat1, lon2, lat2 = map(radians, [node_x, node_y, goal_x, goal_y])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371000
    return c * r

def greedy_best_first_search(graph, start_node, end_node, heuristic):
    open_list = [(start_node, 0)]
    came_from = {start_node: None} # to reconstruct the path
    dist = {start_node: 0} # cost from the start node to the current node

    while open_list:
        current, _ = min(open_list, key=lambda x: x[1])
        open_list = [node for node in open_list if node[0] != current]

        if current == end_node:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, dist[end_node]

        for neighbor in graph.neighbors(current):
            if neighbor not in came_from:
                weight = graph[current][neighbor][0].get('length', 1)
                heuris = heuristic(graph, neighbor, end_node)
                open_list.append((neighbor, heuris))
                came_from[neighbor] = current
                dist[neighbor] = dist[current] + weight

    return None, None