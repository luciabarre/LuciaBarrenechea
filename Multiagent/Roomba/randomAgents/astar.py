import networkx as nx
import matplotlib.pyplot as plt

def a_star_search(graph, start, goal):
    path = nx.astar_path(graph, start, goal)
    return path

# Create a graph
G = nx.Graph()

# Add nodes and edges to the graph using coordinate values
# coordinates = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
coordinates = [(0, 0),
(2, 1),
(3, 2),
(4, 3),
(5, 3)]
G.add_nodes_from(coordinates)
G.add_edges_from([(coordinates[i], coordinates[i + 1]) for i in range(len(coordinates) - 1)])

# Define start and goal nodes
start_node = (5, 3)
goal_node = (0, 0)

# Find the A* p
path = a_star_search(G, start_node, goal_node)
print("A* Path:", path)
# Visualize the graph and path
# pos = dict((n, n) for n in G.nodes())
# nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue')
# nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red', node_size=700)
# plt.show()

