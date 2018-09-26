from graphviz import Digraph


def draw_graph(graph_file_path, edges_dict):
    name = 'pictures/graph.gv'
    g = Digraph('G', filename=name)
    for parent in edges_dict:
        for child in edges_dict.get(parent):
            g.edge(parent.name, child.name)
    g.view()



