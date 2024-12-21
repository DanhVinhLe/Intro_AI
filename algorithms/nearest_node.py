import osmnx as ox 
import numpy as np 
import networkx as nx
from math import radians, cos, sin, asin, sqrt
# graph_file = 'map/map_trucbach.graphml'
# graph = ox.load_graphml(graph_file)
def heuristic(graph, node, goal):
    # Calculate the great-circle distance between two points on the Earth, haversine formula
    node_x, node_y = graph.nodes[node]['x'], graph.nodes[node]['y']
    goal_x, goal_y = goal[0], goal[1]
    lon1, lat1, lon2, lat2 = map(radians, [node_x, node_y, goal_x, goal_y])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371000
    return c * r
def nearest_node(G, point, k, heuristic):
    """_summary_

    Args:
        G (graph): graph object, map of the area
        point ([x, y]): coordinates of the point to find the nearest node
        k (int): number of nearest nodes to find
        heuristic (function): haversine formula to calculate the distance between two points
    Returns:
        list: list of k nearest nodes
    """
    nodes = np.array([[G.nodes[n]['x'], G.nodes[n]['y']] for n in G.nodes])
    distances = np.array([heuristic(G,n, point) for n in G.nodes])
    nearest_indices = distances.argsort()[:k]
    nearest_nodes = [list(G.nodes)[i] for i in nearest_indices]
    nearest_distances = distances[nearest_indices]
    # for i in range(k):
    #     print(f"Node: {nearest_nodes[i]}, Distance: {nearest_distances[i]}")
    return nearest_nodes, nearest_distances

