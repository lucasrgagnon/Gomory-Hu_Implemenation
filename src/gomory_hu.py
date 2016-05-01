__author__ = 'lucasgagnon'
__all__ = ['gomory_hu_tree', 'condense_nodes']

import networkx as nx
import sys
import random
import sdg_ford_fulkerson_max_flow



def gomory_hu_tree(Graph, min_cut_alg = sdg_ford_fulkerson_max_flow.sdg_min_cut):
    gh_tree = nx.Graph()
    tree_labels = label_generator(0)
    if not (nx.is_connected(Graph)):
        comps = nx.connected_components(Graph)
        oldcomp = next(comps)
        for comp in comps:
            v1 = oldcomp[0]
            v2 = comp[0]
            Graph.add_edge(v1, v2, weight = 0)
            oldcomp = comp
    parent_label = next(tree_labels)
    G = Graph
    gh_tree.add_node(parent_label, graph=G)
    complete = False
    while not complete:
        v1, v2 = select_random_nodes(G)
        (S1, S2, cut) = min_cut_alg(G, v1, v2)
        G1 = G.copy()
        G2 = G.copy()
        g1_label = next(tree_labels)
        g2_label = next(tree_labels)
        condense_nodes(G, G1, S2, g2_label)
        condense_nodes(G, G2, S1, g1_label)
        gh_tree.add_node(g1_label, graph=G1)
        gh_tree.add_node(g2_label, graph=G2)
        gh_tree.add_edge(g1_label, g2_label, weight=cut)
        for vertex in gh_tree.neighbors(parent_label):
            if vertex in G1:
                gh_tree.add_edge(vertex, g1_label, weight = gh_tree[vertex][parent_label]['weight'])
            else:
                gh_tree.add_edge(vertex, g2_label, weight = gh_tree[vertex][parent_label]['weight'])
        gh_tree.remove_node(parent_label)
        found = False
        count = 0
        for part in gh_tree.nodes_iter():
            if 'graph' not in gh_tree.node[part]:
                gh_tree.node[part]['graph'] = nx.Graph()
                gh_tree.node[part]['count'] = count
            elif real_gh_node_size(gh_tree.node[part]['graph']) > 1:
                parent_label = part
                G = gh_tree.node[part]['graph']
                found = True
                break
            count += 1
        if not found:
            complete = True
    return gh_tree


def condense_nodes(G, H, S, v):
    """
    :param G:
    :param H:
    :param S:
    :param v:
    :return:
    """
    H.add_node(v)
    cut_weight = 0
    for vertex in G.nodes_iter():
        if vertex in S:
            for neighbor in H.neighbors(vertex):
                if neighbor not in S:
                    if neighbor not in H.neighbors(v):
                        H.add_edge(v, neighbor, weight=H[vertex][neighbor]['weight'])
                    else:
                        H[v][neighbor]['weight'] += H[vertex][neighbor]['weight']
            H.remove_node(vertex)
    return


def select_random_nodes(G):
    v1, v2 = 0, 0
    while v1 == v2 or (type(v1) == str and v1[0] == "_") or (type(v2) ==  str and v2[0] == "_"):
        v1 = random.choice(G.nodes())
        v2 = random.choice(G.nodes())
    return v1, v2


def label_generator(start):
    label = start
    while True:
        yield "_" + str(label)
        label += 1


def real_gh_node_size(G):
    count = 0
    for node in G.nodes_iter():
        if type(node) == str:
            if node[0] != "_":
                count += 1
        else:
            count += 1
    return count
