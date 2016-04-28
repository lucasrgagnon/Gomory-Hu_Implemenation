__author__ = 'lucasgagnon'

import networkx as nx
from gomory_hu import *
from sdg_ford_fulkerson_max_flow import *

G = nx.Graph()
G.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f'])
G.add_edges_from([('a', 'b', {'weight' : 10}), ('a', 'f', {'weight' : 8}),('b', 'c', {'weight' : 4}), \
                  ('b', 'e', {'weight' : 2}), ('b', 'f', {'weight' : 3}), ('c', 'd', {'weight' : 5}), \
                  ('c', 'e', {'weight' : 4}), ('c', 'f', {'weight' : 2}), ('d', 'e', {'weight' : 7}), \
                  ('d', 'f', {'weight' : 2}), ('e', 'f', {'weight' : 3})])



T = gomory_hu_tree(G)


print("NODES:")

for node in T.nodes_iter():
    print(node)
    print(T.node[node]['graph'].nodes())

print()
print("EDGES:")

for edge in T.edges_iter(data=True):
    print(edge)
