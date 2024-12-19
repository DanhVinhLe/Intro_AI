import osmnx as ox

place_name = "Trúc Bạch, Ba Đình, Hà Nội, Vietnam"
graph = ox.graph_from_bbox(21.05118, 21.03979, 105.85153, 105.83469, network_type="all")

# Lưu bản đồ dưới dạng tệp GraphML
ox.save_graphml(graph, filepath="map_trucbach.graphml")