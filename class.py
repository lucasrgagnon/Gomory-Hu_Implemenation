__author__ = 'lucasgagnon'


import networkx as nx
import heapq


def dijkstra(D, u):
    queue = heapq()
    tree = {u : (None, 0)}
    for node in D.neighbors(u):
        heapq.heappush(queue, (D[u][node]['weight'], (u, node)))
    (weight, (parent, child)) = queue.pop()
    while len(tree) <= D.number_of_nodes() and len(queue) != 0:
        tree[child] = (parent, tree[parent][1] + weight)
        for node in D.neighbors(child):
            heapq.heappush(queue, (D[child][node]['weight'], (u, node)))
        while child in tree and len(queue) != 0:
            (weight, (parent, child)) = queue.pop()
    return tree