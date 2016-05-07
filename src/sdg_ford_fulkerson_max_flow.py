__author__ = 'lucasgagnon'
__all__ = ['stm_min_cut', 'breadth_first_search_path']

import networkx as nx
from collections import deque
import sys

def sdg_min_cut(G, u, v):
    """
    Computes minimum u, v cut using Ford-Fulkerson Algorithm, from
    "Computing the minimum cut and maximum flow of undirected graphs" by
    Schroeder, Jonatan and Guedes, ALP and Duarte Jr, Elias P.
    :param G: graph
    :param u: source vertex
    :param v: sink vertex
    :return: partition of vertices of G, S1 and S2, as well as the corresponding max flow.
    """
    D = G.to_directed()
    max_flow = 0
    path_queue, flow = breadth_first_search_path(D, u, v)
    while flow != -1:
        max_flow += flow
        predecessor = path_queue.popleft()
        while len(path_queue) != 0:
            successor = path_queue.popleft()
            if D[predecessor][successor]['weight'] == flow:
                D.remove_edge(predecessor, successor)
                D.remove_edge(successor, predecessor)
            else:
                D[predecessor][successor]['weight'] -= flow
                D[successor][predecessor]['weight'] += flow
            predecessor = successor
        path_queue, flow = breadth_first_search_path(D, u, v)
    S1 = nx.node_connected_component(D.to_undirected(), u)
    S2 = {v for v in G.nodes_iter() if v not in S1}
    return S1, S2, max_flow



def breadth_first_search_path(D, u, v):
    """
    implementation of BFS for above max flow algorihtm
    :param D: digraph
    :param u: source
    :param v: searched-for vertex
    :return: path from u to v, in queue form, as well as the minimum weight of that path
    """
    queue = deque([u])
    tree = {}
    found = False
    while not found and len(queue) != 0:
        current = queue.popleft()
        for vertex in D.neighbors(current):
            if vertex not in tree:
                tree[vertex] = current
                queue.append(vertex)
            if vertex == v:
                found = True
                break
    if not found:
        return deque(), -1
    else:
        child = v
        path_queue = deque([child])
        parent = tree[child]
        min_weight = D[parent][child]['weight']
        path_queue.append(parent)
        while parent != u:
            child = parent
            parent = tree[child]
            if D[parent][child]['weight'] < min_weight:
                min_weight = D[parent][child]['weight']
            path_queue.append(parent)
        return path_queue, min_weight