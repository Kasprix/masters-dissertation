
import os
import networkx as nx
import matplotlib.pyplot as plt
from framework_and_tree import create_framework


# Function is called to make a visual representation of the Argumentation Framework
def display_framework_tree(framework):


  # Initiates Graph
  G = nx.DiGraph()

  attack_list = []

  # Gets all attack relations between the argument agents
  for x in framework:
      if len(x.attacked_by) == 0:
        next
      else:
        for y in x.attacked_by:
          # Other way around for the display so arrows point correctly (x.name, y.name gives the inverse direction)
          attack_list.append((y.name, x.name))
          print (x.name, "is attacked by", y.name)

  print("\n", attack_list, "\n")


  # Adds all the edge relationships between the arguments
  G.add_edges_from(attack_list)
  black_edges = [edge for edge in G.edges()]


  # separate calls to draw nodes and edges
  pos = nx.spring_layout(G, scale = 2)
  nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size = 200)

  nx.draw_networkx_labels(G, pos)
  nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=True)


  # Update, location will be called in the GUI
  plt.savefig("graphs/Graph.png", format="PNG")
  plt.clf()


