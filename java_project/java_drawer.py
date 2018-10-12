import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')
from graphviz import Digraph


def draw_graph(graph_file_path, edges_dict):
    name = 'pictures/graph.gv'
    g = Digraph('G', filename=name)
    for parent in edges_dict:
        for child in edges_dict.get(parent):
            g.edge(parent.name, child.name)
    g.view()


def draw_call_graph(call_graph_list):
    name = 'pictures/call_graph.gv'
    g = Digraph('G', filename=name)
    for node in call_graph_list:
        g.edge('%s' % node[0], '%s' % node[1])
    g.view()


def draw_plot(wmc, rfc):
    fig = plt.figure()

    for key, value in wmc.items():
        x = value
        y = rfc[key]
        plt.plot(x, y, 'bo')
        plt.text(x * (1 + 0.02), y * (1 + 0.02), key, fontsize=8)

    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    plt.xlabel('WMC')
    plt.ylabel('RFC')
    plt.title('Metrics')
    fig.savefig('pictures/plot.png')
