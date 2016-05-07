__author__ = 'lucasgagnon'
__all__ = ['gomory_hu_tree', 'condense_nodes']

import networkx as nx
import random
import sdg_ford_fulkerson_max_flow

def min_k_cut(G, k):
    """
    Finds an approximate minimum k-cut on a graph G using the Gomory-Hu algorithm
    :param G: graph
    :param k: desired number of components
    :return: set partition of vertices in G, int cut weight
    """
    if k > len(G):
        return None
    gh = gomory_hu_tree(G)
    edge_list = list(gh.edges_iter(data='weight'))
    sorted_edges = sorted(edge_list, key = lambda x: x[2], reverse=True)
    cut = 0
    for i in range(0, k):
        edge = sorted(i)
        cut += edge[2]
        gh.remove_edge(edge[0], edge[1])
    partition = set
    for component in gh.connected_components:
        part = set()
        for vertex in component:
            for subvertex in gh.node[vertex]['graph'].nodes_iter():
                part.add(subvertex)
        partition.add(part)
    return(partition, cut)

def gomory_hu_tree(Graph, min_cut_alg = sdg_ford_fulkerson_max_flow.sdg_min_cut):
    """
    Computes the Gomory-Hu minimum cut tree for a graph G, using a min flow/max cut
    algorithm which defaults to sdg_ford_fulkerson_max_flow.
    :param Graph: Graph
    :param min_cut_alg: Algorithm
    :return: Networkx Graph,
    """
    gh_tree = nx.Graph()
    tree_labels = label_generator(0)
    if not (nx.is_connected(Graph)):
        comps = nx.connected_components(Graph)
        oldcomp = next(comps)
        v1 = oldcomp.pop()
        for comp in comps:
            v2 = comp.pop()
            Graph.add_edge(v1, v2, weight = 0)
            v1 = v2
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
    Condenses vertices into a single vertex, as is required by the Gomory-Hu algorithm
    :param G: Read-Only graph
    :param H: Copy of G which will have nodes condensed
    :param S: Set of vertices NOT to condense
    :param v: label of vertex to condense others into
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


def select_random_nodes(G):
    """
    Selects random nodes of a graph
    :param G: Graph
    :return: two distinct vertices of G, chosen at random
    """
    v1, v2 = 0, 0
    if len(G) <= 1:
        return None
    while v1 == v2 or (type(v1) == str and v1[0] == "_") or (type(v2) ==  str and v2[0] == "_"):
        v1 = random.choice(G.nodes())
        v2 = random.choice(G.nodes())
    return v1, v2


def label_generator(start):
    """
    Returns a generatos for labels of vertices in the Gomory-Hu tree.
    Labels begin with underscore "_" to signify their operational, but
    not descriptive function (users should not interact with them).
    :param start:
    :return: label, beginning with _ and followed by increasing integers
    """
    label = start
    while True:
        yield "_" + str(label)
        label += 1


def real_gh_node_size(G):
    """
    Returns the number of non-placeholder vertices in a graph G.
    Placeholder vertices are vertices created in the condensation process,
    and signify connections of a graph/vertex of a Gomory-Hu tree to other
    raph/vertex.
    :param G: Graph
    :return: int number of non-placeholder vertices in G
    """
    count = 0
    for node in G.nodes_iter():
        if type(node) == str:
            if node[0] != "_":
                count += 1
        else:
            count += 1
    return count
