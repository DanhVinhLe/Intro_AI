import tkinter as tk
from tkinter import *
from tkinter import messagebox
import osmnx as ox
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import pickle
import heapq
# Step 1: Load the graph
place_name = "Truc Bach, Ba Dinh, Hanoi, Vietnam"
graph_file = 'map/map_trucbach.graphml'

# Check if the graph file exists
graph = ox.load_graphml(graph_file)
# Initialize global variables
image_path = "map/bg.png"

# Step 2: Define GUI application
class MapApp:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Shortest Path Finder")
        self.root.state("zoomed")
        self.selected_points = []
        self.start_node = None
        self.end_node = None
        self.route = None
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.background_image = mpimg.imread(image_path)
        # Plot the initial graph
        

        # Create a label to show node selection
        self.info_label = tk.Label(root, text="Select two points on the map", font=("Arial", 12))
        self.info_label.pack(side=tk.TOP, pady=10)

        # Create buttons
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_selection)
        self.reset_button.pack(side=tk.BOTTOM, padx=10)
        self.quit_button = tk.Button(root, text="Exit", command=self.root.quit)
        self.quit_button.pack(side=tk.TOP, padx=10)
        self.find_button = tk.Button(root, text="Find Route", command=self.calculate_route)
        self.find_button.pack(side=tk.BOTTOM, padx=10)
        # Embed the canvas in the GUI
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Connect matplotlib events to Tkinter
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.plot_graph()
        self.root.mainloop()
        
    def plot_graph(self):
        """Plot the graph in the matplotlib figure."""
        self.ax.clear()
        self.ax.imshow(self.background_image, extent=[105.83469, 105.85153, 21.03979, 21.05118])
        ox.plot_graph(graph, ax=self.ax, show=False, close=False, bgcolor="lightgray", edge_color='none', node_size=0)
        if self.route:
            ox.plot_graph_route(
                graph,
                self.route,
                route_color="red",
                route_linewidth=3,
                bgcolor="lightgray",
                ax=self.ax,
                show=False,
                close=False,
            )
        x_start, y_start = self.selected_points[0] if len(self.selected_points) > 0 else (None, None)
        x_end, y_end = self.selected_points[1] if len(self.selected_points) > 1 else (None, None)
        if self.start_node:
            self.ax.plot([x_start, graph.nodes[self.start_node]['x']], [y_start, graph.nodes[self.start_node]['y']], c="purple", linestyle="--", linewidth=3)
        if self.end_node:
            self.ax.plot([x_end, graph.nodes[self.end_node]['x']], [y_end, graph.nodes[self.end_node]['y']], c="purple", linestyle="--", linewidth=3)
        self.ax.scatter(x_start, y_start, c="green", s=50, zorder=5)
        self.ax.scatter(x_end, y_end, c="blue", s=50, zorder=5)
        self.canvas.draw()

    def on_click(self, event):
        """Handle click events to capture coordinates."""
        if event.xdata is None or event.ydata is None:
            return  # Ignore clicks outside the grap

        # Add the selected node to the points
        self.selected_points.append((event.xdata, event.ydata))
        print(f"Selected points: {event.xdata}, {event.ydata}")

        # Plot the selected node immediately
        self.ax.scatter(event.xdata, event.ydata, c="blue", s=50, zorder=5)
        self.canvas.draw()

    def calculate_route(self):
        """Calculate and display the shortest route."""
        if len(self.selected_points) < 2:
            messagebox.showwarning("Selection Error", "Please select two points before calculating.")
            return
        self.start_node = ox.distance.nearest_nodes(graph, self.selected_points[0][0], self.selected_points[0][1])
        self.end_node = ox.distance.nearest_nodes(graph, self.selected_points[1][0], self.selected_points[1][1])
        self.route = nx.shortest_path(graph, source=self.start_node, target=self.end_node, weight="length")
        self.plot_graph()
    def reset_selection(self):
        """Reset the map and clear selections."""
        self.selected_points = []
        self.start_node = None
        self.end_node = None
        self.route = None
        self.info_label.config(text="Select two points on the map")
        self.plot_graph()  # Redraw the map without the route


# Step 3: Run the application
root = tk.Tk()
app = MapApp(root)

