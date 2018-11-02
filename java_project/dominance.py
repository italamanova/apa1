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


def number_nodes(graph):
    pass


def define_dominators(graph, start_node):
    all_dominators = graph.nodes
    predecessor_dict = {}
    all_predecessors = {}
    dominators = {}

    for node in graph.nodes:
        if node != start_node:
            dominators.update({node: all_dominators})
        else:
            dominators.update({node: set([start_node])})

    for node in graph.nodes:
        all_predecessors.update({node: list(graph.predecessors(node))})
        current_predecessors = list(graph.predecessors(node))
        for item in current_predecessors:
            if item > node:
                current_predecessors.remove(item)
        predecessor_dict.update({node: current_predecessors})

    for item in predecessor_dict:
        for predecessor in predecessor_dict[item]:
            dominators[item] = dominators[item] & dominators[predecessor]
        dominators[item].add(item)

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
                idom = max(idom_set)
            else:
                idom = None
            _sdom = is_sdom(item, all_predecessors)
            dominance_tree.append([idom, item, _sdom])
    print('dominance_tree', dominance_tree)
    return dominance_tree


def add_cluster(edge, clusters):
    parent = edge[0]
    child = edge[1]
    if parent in clusters.keys():
        clusters[parent].append(child)
    else:
        clusters.update({parent: [child]})


def add_predecessor(_child, _parent, predecessor_dict):
    if _parent in predecessor_dict.keys():
        predecessor_dict[_child].append(_parent)
    else:
        predecessor_dict.update({_child: [_parent]})


def clustering(dominance_tree):
    clusters = {}

    for edge in dominance_tree:
        if edge[2]:
            add_cluster(edge, clusters)
        else:
            clusters.update({edge[1]: []})

    print('clusters1', clusters)

    keys = list(sorted(clusters.keys()))

    for key in keys:
        for value in clusters[key]:
            if value in keys and value != key:
                clusters[key].extend(clusters.pop(value))
                keys.remove(value)
    print('clusters2', clusters)


start_node = 1
dominators, all_predecessors = define_dominators(G, start_node)
dominance_tree = build_dom_tree(dominators, all_predecessors, start_node)
clustering(dominance_tree)

cluster1 = {1: [2], 3: [], 4: [5, 6], 7: [8, 9, 10, 11]}


def search_node(node, clusters):
    for item in clusters:
        if node in clusters[item]:
            return item
    return None


# TODO посчитать невых предков и рекурсивно запустить опять
def calculate_new_predecessors(clusters, old_predecessors):
    new_predecessors = {}
    for item in clusters:
        item_predecessors = old_predecessors[item]
        for pred in item_predecessors:
            new_parent_node = search_node(pred, clusters)
            # if new_parent_node != item:
            #     print(new_parent_node, item)
            add_predecessor(item, new_parent_node, new_predecessors)
    print('new_predecessors', new_predecessors)


dominance_tree_new = []

for edge in dominance_tree:
    parent = edge[0]
    child = edge[1]
    if parent in cluster1:
        if child not in cluster1[parent]:
            dominance_tree_new.append([parent, child])
            calculate_new_predecessors(cluster1, all_predecessors)

print('dominance_tree_new', dominance_tree_new)
