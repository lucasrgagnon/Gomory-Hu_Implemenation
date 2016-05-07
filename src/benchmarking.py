__author__ = 'lucasgagnon'

import time
import networkx as nx
import csv
import os
from gomory_hu import *


def gnp_survey_benchmark(path, n_array, p_array):
    with open(path, 'w', newline='\n') as f:
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
                start = time.time()
                gh = gomory_hu_tree(G)
                end = time.time()
                t = end-start
                ########## END TIMING ##########
                list.append(t)
                print("Completed trial n = " + str(n) + ", p = " + str(p) + ".")
                print("Time = " + str(t))
                nx.write_adjlist(G, 'Graph(' + str(n) + "," + str(p) + ").csv")
                nx.write_adjlist(gh, 'Gomory_Hu(' + str(n) + "," + str(p) + ").csv")
                print()
            w.writerow(list)

def averaging_small_benchmark(path, n_array,  reps):
    with open(path, 'w', newline='\n') as f:
        w = csv.writer(f)
        w.writerow(["Graph Size"] + [str(i) for i in n_array])
        list = ["Average Time"]
        for n in n_array:
            time_sum = 0
            for i in range(reps):
                G = nx.gnp_random_graph(n, 0.5)
                for (i, j) in G.edges_iter():
                    G[i][j]['weight'] = 1
                ############ TIMING ############
                start = time.time()
                gomory_hu_tree(G)
                end = time.time()
                ########## END TIMING ##########
                t = end - start
                time_sum += t
            list.append(str(time_sum / reps))
            print("Completed case n = " + str(n) + ", average = " + str(time_sum / reps))
        w.writerow(list)




os.chdir('../')
os.chdir('data')

gnp_survey_benchmark('benchmarking.csv', [10, 30, 50, 70 , 100, 500, 1000], [0.2, 0.4, 0.5, 0.6, 0.8])
averaging_small_benchmark('average_small_case_benchmarking.csv', [5, 10, 15, 20, 25, 30], 1000)
averaging_small_benchmark('average_med_case_benchmarking.csv', [40, 45, 50, 55, 60, 65, 70], 1000)
averaging_small_benchmark('average_large_case_benchmarking.csv', [75, 90, 100], 1000)