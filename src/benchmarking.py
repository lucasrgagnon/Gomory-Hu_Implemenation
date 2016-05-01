__author__ = 'lucasgagnon'

import timeit
import networkx as nx
import csv
import os
from gomory_hu import *

os.chdir('../')
os.chdir('data')

p_array = [0.2, 0.4, 0.5, 0.6, 0.8]
n_array = [10, 30, 50, 70 , 100, 500, 1000]
with open('benchmarking.csv', 'w', newline='\n') as f:
    w = csv.writer(f)
    w.writerow(['n', 'p = 0.2', 'p = 0.4', 'p = 0.5', 'p = 0.6', 'p = 0.8'])
    for n in n_array:
        list = [str(n)]
        for p in p_array:
            print("Starting trial n = " + str(n) + ", p = " + str(p) + ".")
            G = nx.gnp_random_graph(n, p)
            for (i, j) in G.edges_iter():
                G[i][j]['weight'] = 1
            print("Calling GH algorithm")
            ############ TIMING ############
            start = timeit.timeit()
            gh = gomory_hu_tree(G)
            end = timeit.timeit()
            ########## END TIMING ##########
            list.append(start - end)
            print("Completed trial n = " + str(n) + ", p = " + str(p) + ".")
            print("Time = " + str(start-end))
            nx.write_adjlist(G, 'Graph(' + str(n) + "," + str(p) + ").csv")
            nx.write_adjlist(gh, 'Gomory_Hu(' + str(n) + "," + str(p) + ").csv")
            print()
        w.writerow(list)
