import copy
import sys

import networkx as nx

G = nx.DiGraph()

G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 5)
G.add_edge(4, 6)
G.add_edge(5, 7)
G.add_edge(6, 7)
G.add_edge(7, 8)
G.add_edge(8, 9)
G.add_edge(8, 10)
G.add_edge(10, 11)
G.add_edge(9, 1)
G.add_edge(8, 3)
G.add_edge(10, 7)
G.add_edge(7, 4)
G.add_edge(4, 3)



######### DOMINANCE TREE #############

def define_dominators(graph, start_node):
    all_dominators = graph.nodes
    predecessor_dict = {}
    all_predecessors = {}
    dominators = {}

    for node in graph.nodes:
        if node != start_node:
            dominators.update({node: set(all_dominators)})
        else:
            dominators.update({node: set([start_node])})

    for node in graph.nodes:
        all_predecessors.update({node: list(graph.predecessors(node))})
        current_predecessors = list(graph.predecessors(node))
        predecessor_dict.update({node: current_predecessors})

    for item in predecessor_dict:
        for predecessor in predecessor_dict[item]:
            dominators[item] = dominators[item] & dominators[predecessor]
        dominators[item].add(item)

    print('\n')
    print('all_predecessors', all_predecessors)
    print('dominators', dominators)
    print()
    return dominators, all_predecessors


def is_sdom(node, all_predecessors):
    if len(all_predecessors[node]) == 1:
        return True
    return False


def build_dom_tree(dominators, all_predecessors, start_node):
    dominance_tree = []
    for item in dominators:
        if item != start_node:
            idom_set = dominators[item]
            idom_set.remove(item)
            if idom_set:
                idom = list(idom_set)[-1]
            else:
                idom = None
            _sdom = is_sdom(item, all_predecessors)
            dominance_tree.append([idom, item, _sdom])
    print('dominance_tree', dominance_tree)
    return dominance_tree


#############################################


############### CLUSTERING ##################


def add_predecessor(_child, _parent, predecessor_dict):
    if _parent in predecessor_dict.keys():
        predecessor_dict[_child].append(_parent)
    else:
        predecessor_dict.update({_child: [_parent]})


def search_node(node, clusters):
    for item in clusters:
        if node in clusters[item]:
            return item
    return None


def calculate_new_graph(clusters, old_predecessors):
    helper_structure = copy.deepcopy(clusters)
    for item in helper_structure:
        helper_structure[item].append(item)

    helper_structure_of_cluster = {}
    for item in helper_structure:
        for node in helper_structure[item]:
            helper_structure_of_cluster.update({node: item})

    new_graph = nx.DiGraph()
    for item in helper_structure:
        helper_structure_item = helper_structure[item]
        for node in helper_structure_item:
            old_predecessors_items = old_predecessors[node]
            for old_predecessors_item in old_predecessors_items:
                if old_predecessors_item not in helper_structure_item:
                    try:
                        new_graph.add_edge(helper_structure_of_cluster[old_predecessors_item], item)
                    except Exception:
                        sys.exit(1)
    return new_graph


def add_cluster(edge, clusters):
    parent = edge[0]
    child = edge[1]
    if parent in clusters.keys():
        clusters[parent].append(child)
    else:
        clusters.update({parent: [child]})


def clustering(dominance_tree, start_node):
    clusters = {}

    clusters.update({start_node: []})
    for edge in dominance_tree:
        if edge[2]:
            add_cluster(edge, clusters)
        else:
            clusters.update({edge[1]: []})

    keys = list(clusters.keys())
    for key in keys:
        for value in clusters[key]:
            if value in keys and value != key:
                clusters[key].extend(clusters.pop(value))
                keys.remove(value)

    return clusters


#############################################

def process_graph(graph, start_node):
    while len(graph.nodes) > 1:
        dominators, all_predecessors = define_dominators(graph, start_node)
        dominance_tree = build_dom_tree(dominators, all_predecessors, start_node)
        cluster = clustering(dominance_tree, start_node)
        print('cluster', cluster)
        graph = calculate_new_graph(cluster, all_predecessors)


process_graph(G, 1)