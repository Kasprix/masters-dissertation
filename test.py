
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

from framework_and_tree import create_framework



list_of_objects = create_framework(3)
attack_list = []

for x in list_of_objects:
    if len(x.attacked_by) == 0:
      attack_list.append((x.name))
    else:
      for y in x.attacked_by:
        attack_list.append((x.name, y.name))
        print (x.name, "is attacked by", y.name)

print("\n", attack_list, "\n")

print(list_of_objects)