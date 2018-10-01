from graphviz import Digraph


def draw_graph(graph_file_path, edges_dict):
    name = 'pictures/graph.gv'
    g = Digraph('G', filename=name)
    for parent in edges_dict:
        for child in edges_dict.get(parent):
            g.edge(parent.name, child.name)
    g.view()


def draw_call_graph(graph_file_path, call_graph_dict):
    name = 'pictures/call_graph.gv'
    g = Digraph('G', filename=name)
    for node in call_graph_dict:
        for node_child in call_graph_dict.get(node):
            g.edge('%s()' % node, '%s()' % node_child)
    g.view()



