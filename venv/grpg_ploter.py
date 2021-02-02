import numpy as np
import networkx as nx
import pylab as plt
import visibilityGraph_for_AC
from networkx.utils import open_file



# G = nx.read_gpickle('/Users/revital/PycharmProjects/DynamicTSP/test/g2020-09-07 17/12/14.697944_4')
# print(G.vg.nodes)
# poss=dict(G.vg.nodes(data='pos'))
#
# nx.draw(G.vg, pos=poss,node_size=80)
# plt.show()


#for old test:
# import os
# dir='/Users/revital/PycharmProjects/DynamicTSP/benchMark1/'
# for filename in os.listdir(dir):
#     if filename.startswith('g'):
#         G = nx.read_gpickle(dir+filename)
#         print(G.edges(data='weight'))
#         poss = dict(G.nodes(data='pos'))
#         print(dir+filename)
#         G_t = nx.shortest_path(G, source=1364, target=31, weight='weight', method='dijkstra')
#         print(G_t)
#         edgeList = [(G_t[e], G_t[e + 1]) for e in range(len(G_t) - 1)]
#         #G.draw_graph( edgeList= edgeList,draw=False, name=dir+'res/'+filename)
#         #nx.draw(G, pos=poss, node_size=80)
#         visibilityGraph_for_AC.draw_G(G,poss , edgeList=edgeList, draw=False, name=dir+'res/'+filename)
#         plt.savefig(dir+'res/'+filename+'_sp.png')
#     else:
#         continue



import os
dir='/Users/revital/PycharmProjects/DynamicTSP/bm8/'
for filename in os.listdir(dir):
    if filename.startswith('g'):
        G = nx.read_gpickle(dir+filename)
        #G.compute_vg(5000,1000)
        poss = dict(G.vg.nodes(data='pos'))
        print(dir+filename)
        G_t = nx.shortest_path(G.vg, source=1156, target=1243, weight='weight', method='dijkstra')
        print(G_t)
        edgeList = [(G_t[e], G_t[e + 1]) for e in range(len(G_t) - 1)]
        G.draw_graph( edgeList= edgeList,draw=False, name=dir+'res/'+filename+"22")
        #nx.draw(G, pos=poss, node_size=80)
        #plt.savefig(dir+'res/'+filename+'_sp.png')
    else:
        continue
