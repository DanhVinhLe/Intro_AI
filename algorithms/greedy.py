import osmnx as ox 
import networkx as nx
import json
place_name = "Truc Bach, Ba Dinh, Hanoi, Vietnam"
graph_file = 'map/map_trucbach.graphml'

graph = ox.load_graphml(graph_file)
# Greedy Best First Search
# heuristic function to estimate the cost from the current node to the goal node
def heuristic(node, end_node):
    node_x, node_y = graph.nodes[node]['x'], graph.nodes[node]['y']
    goal_x, goal_y = graph.nodes[end_node]['x'], graph.nodes[end_node]['y']
    return ((node_x - goal_x) ** 2 + (node_y - goal_y) ** 2) ** 0.5

def greedy_best_first_search(graph, start_node, end_node):
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
                heuris = heuristic(neighbor, end_node)
                open_list.append((neighbor, heuris))
                came_from[neighbor] = current
                dist[neighbor] = dist[current] + weight

    return None, None