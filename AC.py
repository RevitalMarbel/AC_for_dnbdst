import datetime

import math

import draw_graphs
import visibilityGraph
import os
import sys
import time
from scipy import fft
import re
import numpy as np
import networkx as nx
import pylab as plt
import visibilityGraph_for_AC
import distance_functions
from networkx.utils import open_file

import pickle


def AB_DCST(G,times=1, s=1 , nue=0.5,enahncmentFactor=1.5, isFirst=True, oldGraph=None, p=None,i=None,d=None, numOfAnts=0):
    res = []
    cost_b=math.inf
    steps_with_no_improvement=0
    G.init_diff(oldGraph)
    G.init_ants(oldGraph, numOfAnts)
    G.init_phermones(oldGraph)
    Go=G
    # if(isFirst==False):
    #
    #     G.update_phermones_time(p=p, i=i,d=d, prev=oldGraph)
        #print(G.sum_phermones(), "init 2")
    B=nx.Graph()
    for i in range(times):
        for step in range(s):
            #if step== (s/3) or step== (2*s/3):
            G.update_phermones(nue)
            #print("move all")

            G.move_all()
#           #print(G.ants)
        #G.print_phermones_level()
        #print("update phermons")
        G.update_phermones(nue)
        print("construct tree")
        T = G.treeConstruct(buttomPhermonesnum=0)
        t_cost = visibilityGraph_for_AC.cost(T)
        print("cost ", cost_b, t_cost)
        if cost_b > t_cost:
            cost_b = t_cost
            B=T
            Go=G
            steps_with_no_improvement=0
            G.phermon_enjancement(T, enahncmentFactor=enahncmentFactor)
        else:
            steps_with_no_improvement=steps_with_no_improvement+1
        nue=- 0.01
        if steps_with_no_improvement>5:
            G.phermon_enjancement(T,enahncmentFactor=nue)
            steps_with_no_improvement = 0
            print("evaporate")
        res.append([i, cost_b])
        #res.append([i, G.sum_phermones()])
    return B,res,Go


def main():

   #get a list of graphs from file take the first place just for sports
    f = open("distances_5_1_nodes_vg_graphs" , 'rb')
    gl_n = pickle.load(f)
    f.close()

    r = open("distances_5_1_nodes_vg_graphs" , 'rb')
    gl = pickle.load(r)
    r.close()



    #draw_graphs.draw_from_pos(g.vg)
    #print(g.vg.edges)
    #print(g.sum_phermones(), "sum phermones before")


    #normal AC as we know it
    res_list=[]
    graphs_list=[]
    Go=None
    for g in gl:
        b,res,Go=AB_DCST(g,isFirst=False, oldGraph=Go, p=0, i=1 , d=0, numOfAnts=0)
        graphs_list.append(Go)
        res_list.append(res[len(res)-1])

   # my way:
    res_list_new = []

   #first time
    b, res ,Go= AB_DCST(gl_n[0])

    res_list_new.append(res[len(res) - 1])

    for i in range(1,len(gl_n)):
        b, res,Go = AB_DCST(gl_n[i], isFirst=False, oldGraph=Go, p=0, i=1 , d=0, numOfAnts=20 )
        res_list_new.append(res[len(res)-1])



    #draw_graphs.draw_from_pos(b)

    #print(g.sum_phermones(), "sum phermones after1")

    #b1,res1 = AB_DCST(gl[1])

    #draw_graphs.draw_from_pos(b1)



    #print(g.sum_phermones(), "sum phermones after1")
    #print(gl[1].sum_phermones(), "sum phermones after2")






    columns = 3
    rows = 2

    for i in range(0, 5):
        draw_graphs.draw_from_pos(graphs_list[i].vg, fileName="1", draw=False)
    #plt.show()
    plt.plot(res_list, 'r--')
    plt.plot(res_list_new, 'b--')


    #plt.plot(res, 'g--')

    plt.show()
    print(res )

if __name__ == "__main__":
    main()