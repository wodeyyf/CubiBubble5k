import os
import networkx as nx
import numpy as np
from node2vec import  Node2Vec

path = "C:\\Users\\HanLi\\Desktop\\Arch_Research\\Ecadia\\GNN\\processed_data"
Gs = []
for i in range(1,2):
    G = nx.read_gml(path+"\\data_1\\Gs_1_{}.gml".format(i))
    G.remove_edges_from(nx.selfloop_edges(G))
    Gs.append(G)
G = Gs[0]
node2vec = Node2Vec(G, dimensions=16, walk_length=5, num_walks=200, p=0.5, q=2, workers=4)
# Learn the node embeddings
model = node2vec.fit(window=10, min_count=1, batch_words=4)
embeddings = {}
for node in G.nodes():
    embeddings[node] = model.wv[str(node)]
print(embeddings)