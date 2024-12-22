import osmnx as ox 
import networkx as nx
import heapq
import itertools
from math import radians, cos, sin, asin, sqrt
def heuristic(graph, node, goal):
    # Calculate the great-circle distance between two points on the Earth, haversine formula
    node_x, node_y = graph.nodes[node]['x'], graph.nodes[node]['y']
    goal_x, goal_y = graph.nodes[goal]['x'], graph.nodes[goal]['y']
    lon1, lat1, lon2, lat2 = map(radians, [node_x, node_y, goal_x, goal_y])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371000
    return c * r

def a_star(graph, start_node, end_node, heuristic):
    open_set = []
    c = itertools.count()
    heapq.heappush(open_set, (0, next(c), start_node))  # Priority queue initialized with start node

    came_from = {}  # To reconstruct the path
    g_score = {node: float('inf') for node in graph.nodes}  # Cost from start to each node
    g_score[start_node] = 0
    f_score = {node: float('inf') for node in graph.nodes}  # Estimated total cost from start to end, heuristic + g_score
    f_score[start_node] = heuristic(graph, start_node, end_node)

    # To store enqueued nodes and their distances to avoid recomputation
    enqueued = {}

    while open_set:
        _, _, current = heapq.heappop(open_set)  # Node with the lowest f_score

        if current == end_node:
            # Reconstruct the path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1], g_score[end_node]

        for neighbor in graph.neighbors(current):
            weight = graph[current][neighbor][0].get('length', 1)
            tentative_g_score = g_score[current] + weight
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(graph, neighbor, end_node)

                if neighbor not in enqueued or tentative_g_score < enqueued[neighbor]:
                    enqueued[neighbor] = tentative_g_score
                    heapq.heappush(open_set, (f_score[neighbor], next(c), neighbor))

    return None, None