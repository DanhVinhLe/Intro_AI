import osmnx as ox 
import networkx as nx
import json

def dfs(graph, start_node, goal, path=None, visited=None):
    # path is the path from the start node to the current node 
    if path is None:
        path = []
    if visited is None:
        visited = set()
    
    path.append(start_node)
    visited.add(start_node)
    if start_node == goal:
        return path
    
    for neighbor in graph.neighbors(start_node):
        if neighbor not in visited:
            result = dfs(graph, neighbor, goal, path, visited)
            if result is not None:
                return result
    path.pop() # backtrack
    return None