import osmnx as ox 
import numpy as np 
import networkx as nx

graph_file = 'map/map_trucbach.graphml'
graph = ox.load_graphml(graph_file)

def nearest_node(G, point, k):
    """_summary_

    Args:
        G (graph): graph object, map of the area
        point ([x, y]): coordinates of the point to find the nearest node
        k (int): number of nearest nodes to find

    Returns:
        list: list of k nearest nodes
    """
    nodes = np.array([[G.nodes[n]['x'], G.nodes[n]['y']] for n in G.nodes])
    distances = np.linalg.norm(nodes - np.array(point), axis=1)
    nearest_indices = distances.argsort()[:k]
    nearest_nodes = [list(G.nodes)[i] for i in nearest_indices]
    nearest_distances = distances[nearest_indices]
    # for i in range(k):
    #     print(f"Node: {nearest_nodes[i]}, Distance: {nearest_distances[i]}")
    return nearest_nodes, nearest_distances
