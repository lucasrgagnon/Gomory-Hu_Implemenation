__author__ = 'lucasgagnon'

import networkx as nx
from gomory_hu import gomory_hu_tree
from gomory_hu import real_gh_node_size
from stm_ford_fulkerson_max_flow import *

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6])
G.add_edges_from([(1, 2, {'weight' : 100}), (1, 3, {'weight' : 1}),(2, 3, {'weight' : 2}), (2, 4, {'weight' : 100}), (2, 5, {'weight' : 1}), \
                  (3, 4, {'weight' : 3}), (4, 5, {'weight' : 1}), (4, 6, {'weight' : 1}), (5, 6, {'weight' : 10})])



T = gomory_hu_tree(G)
print(type(T))
for node in T.nodes_iter():
    if type(node) == nx.classes.graph.Graph:
        print("Graph")
    else:
        print(node)
    print(T.node[node])
    if 'graph' in T.node[node]:
        print(T.node[node]['graph'].nodes())
        print(real_gh_node_size(T.node[node]['graph']))

print()
print("EDGES:")
print()

for edge in T.edges_iter():
    print(edge)
    print(T.get_edge_data(T, edge))

