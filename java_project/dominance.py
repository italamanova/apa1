import networkx as nx
import matplotlib.pyplot as plt

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
G.add_edge(9, 1)
G.add_edge(8, 3)
G.add_edge(10, 7)
G.add_edge(7, 4)
G.add_edge(4, 3)


# print(dir(G))

# for node in G.nodes:
#     print(node, list(G.predecessors(node)))


# print(sorted(nx.immediate_dominators(G, 1).items()))

T = nx.dfs_tree(G,1)
print(T.edges())
print(dir(T))

print(T.nodes)




# res = G.predecessors('b')
# print(list(res))
# print(G.pred['b'])