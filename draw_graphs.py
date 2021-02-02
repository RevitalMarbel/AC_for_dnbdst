import pickle
import networkx as nx
import matplotlib.pyplot as plt

def draw_from_pickle(fileName, draw=True):
    plt.figure(figsize=(8,4))
    # fig, ax = plt.subplots()
    G_obj = nx.read_gpickle(fileName)
    G=G_obj.vg
    pos=dict(G.nodes(data="pos", default=(0,0)))
    #pos = dict(G.nodes(data="pos", default=(0,0)))
   # pos=G.nodes["pos"]
    nx.draw_networkx_labels(G, pos, font_size=5, font_color='r')
    nx.draw_networkx_edges(G, pos, nodelist=G.nodes, alpha=0.4)
    nx.draw_networkx_nodes(G, pos, nodelist=list(pos.keys()), node_size=60)
    #nx.draw_networkx_edges(G, pos, edgelist=edgeList, edge_color='r', width=2)  # highlight elist
    # ,cmap=plt.cm.Reds_r, with_labels = True)
    # plt.draw()
    laat_min = min(pos.items(), key=lambda x: x[1])
    lat_max = max(pos.items(), key=lambda x: x[1])
    #        lon_min = min(self.pos.items(), key=lambda x: x[2])
    #        lon_max = max(self.pos.items(), key=lambda x: x[2])
    #        plt.set_xlim(laat_min, lat_max)
    # plt.grid(axis='y', linestyle='-')
    # plt.grid(True, which='both',axis='both')
    if draw == True:
        plt.show()
    else:
        plt.savefig(fileName+"_output" + '.png')


def draw_from_pos(G, fileName="", draw=True):
    plt.figure(figsize=(8,4))
    # fig, ax = plt.subplots()
    pos=dict(G.nodes(data="pos", default=(0,0)))
    weights = [G[u][v]['ph']/100 for u, v in G.edges()]
    nx.draw_networkx_labels(G, pos, font_size=5, font_color='r')
    nx.draw_networkx_edges(G, pos, nodelist=G.nodes, width=weights  , alpha=0.4)
    nx.draw_networkx_nodes(G, pos, nodelist=list(pos.keys()), node_size=60)
    #nx.draw_networkx_edges(G, pos, edgelist=edgeList, edge_color='r', width=2)  # highlight elist
    # ,cmap=plt.cm.Reds_r, with_labels = True)
    # plt.draw()
    laat_min = min(pos.items(), key=lambda x: x[1])
    lat_max = max(pos.items(), key=lambda x: x[1])
    #        lon_min = min(self.pos.items(), key=lambda x: x[2])
    #        lon_max = max(self.pos.items(), key=lambda x: x[2])
    #        plt.set_xlim(laat_min, lat_max)
    # plt.grid(axis='y', linestyle='-')
    # plt.grid(True, which='both',axis='both')
    if draw == True:
        plt.show()

    else:
        plt.savefig(fileName+"_output" + '.png')


def plot_lat_lon_in_time(lat_l,lon_l, index):
    import pylab as plt
    plt.plot([i for i in range(len(lat_l))],[lat_l[i][index] for i in range(len(lat_l))], label='lat')
    plt.plot([i for i in range(len(lat_l))], [lon_l[i][index] for i in range(len(lon_l))],label='long')
    plt.show()

