import osmnx as ox 
import networkx as nx
import json
place_name = "Truc Bach, Ba Dinh, Hanoi, Vietnam"
graph_file = 'map/map_trucbach.graphml'

graph = ox.load_graphml(graph_file)
nodes = list(graph.nodes())
dist = {node: {node: float('inf') for node in nodes} for node in nodes}
next_node = {node: {node: None for node in nodes} for node in nodes}

for u, v, data in graph.edges(data=True):
    dist[u][v] = data.get('length')
    next_node[u][v] = v

for node in nodes:
    dist[node][node] = 0
def floyd_warshall(nodes):

    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

floyd_warshall(nodes)
all_paths = {}

# Iterate through all pairs of nodes
for start_node in nodes:
    for end_node in nodes:
        if start_node == end_node or next_node[start_node][end_node] is None:
            continue
        else:
            path = [start_node]
            st, en = start_node, end_node
            while st != en:
                st = next_node[st][en]
                path.append(st)
            all_paths[f"{start_node}-{end_node}"] = path
            
with open('all_paths.json', 'w') as f:
    json.dump(all_paths, f)
