import datetime
import csv
import math
from copy import copy, deepcopy
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
import datetime
from networkx.utils import open_file

import pickle


def AB_DCST(G,times=1, s=50 , nue=0.01,enahncmentFactor=0.6, isFirst=True, oldGraph=None, p=None,i=None,d=None, numOfAnts=0):
    if not nx.is_connected(G.vg):
        print("not connected")
    res = []
    cost_b=math.inf
    steps_with_no_improvement=0

    #G.init_diff(oldGraph)
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
            G.move_all()
            if step== (s/3):
                G.update_phermones(nue)
            #print("move all")

#           #print(G.ants)
        #G.print_phermones_level()
        #print("update phermons")
        #G.update_phermones(nue)
        #print("construct tree")
        T = G.treeConstruct(buttomPhermonesnum=0)
        t_cost = visibilityGraph_for_AC.cost(T)
        #print("cost ", cost_b, t_cost)
        if cost_b > t_cost:
            cost_b = t_cost
            B=T
            Go=G
            steps_with_no_improvement=0
            G.phermon_enjancement( enahncmentFactor=nue)
        else:
            steps_with_no_improvement=steps_with_no_improvement+1
        nue=- 0.01
        if steps_with_no_improvement>3:
            G.phermon_enjancement(enahncmentFactor=enahncmentFactor)

            steps_with_no_improvement = 0
            print("evaporate")
        res.append( cost_b)
        #res.append([i, G.sum_phermones()])
    return B,res,Go

def test_GraphDegree(filename, minDegree=3 ):
    # load graphs list (created by TleHandler)
    f = open(filename, 'rb')
    gl = pickle.load(f)
    f.close()
    # create res list - every entry is a list of results by ac algorithm
    res_list = []
    # create a list of graph results from AC
    graphs_list = []
    sum_list = []
    node_list = []
    #take the first graph mst
    mst = nx.minimum_spanning_tree(gl[0].vg, weight='weight')
    mst_edges = set(mst.edges())
    draw_graphs.draw_from_pos(mst, fileName="mst" + str(gl[0]), draw=False, nodelist=node_list, edge_list=[])

    #compute the edge diff between the states
    for i in range(1, len(gl)):
        mst = nx.minimum_spanning_tree(gl[i].vg, weight='weight')
        edges = set(mst.edges())
        mst_edges = edges - mst_edges.intersection(edges)
        print("diff" + str(i), mst_edges)
        # draw_graphs.draw_from_pos(g.vg, fileName="gl[0].vg", draw=False)
        draw_graphs.draw_from_pos(mst, fileName="mst" + str(gl[i]), draw=False, nodelist=node_list, edge_list=mst_edges)
        mst_edges = edges

    #shows the degree of the nodes
    for u in mst.nodes():
        neighbors = nx.neighbors(mst, u)
        sum = 0
        for n in neighbors:
            sum = sum + 1
        if sum > minDegree:
            sum_list.append(sum)
            node_list.append(u)
    print(sum_list)
    print(node_list)
    print(visibilityGraph_for_AC.cost(mst) / 100000)
    labels = node_list
    draw_graphs.draw_from_pos(mst, fileName="mst", draw=False, nodelist=node_list)
    plt.show()

    #compute the grpah npdes degre histogram for nodes over minDegree
    hist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hist_label = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    for i in sum_list:
        hist[i] += 1

    print(sum_list, hist)
    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars
    plt.bar(hist_label, hist)
    plt.show()

def test_AC_on_grapf_list(filename, times, s):
    f = open(filename, 'rb')
    gl = pickle.load(f)
    f.close()
    # create res list - every entry is a list of results by ac algorithm
    res_list = []
    graphs_list = []
    mst_cost_list=[]
    time_list=[]
    Go = None
    for g in gl:
        time1=  datetime.datetime.now()
        b, res, Go = AB_DCST(g,times=times, s=s, isFirst=False, oldGraph=Go, numOfAnts=100)
        time2 = datetime.datetime.now()
        timediff=time2-time1
        timediff=int(timediff.total_seconds() * 1000)
        time_list.append(timediff)
        print("res:", res)
        graphs_list.append(b)
        mst = nx.minimum_spanning_tree(g.vg, weight='weight')
        cost = visibilityGraph_for_AC.cost(mst)
        mst_cost_list.append([cost for i in range(len(res))])
        res_list.append(res)
    header=['graph number', 'number of nodes', 'time','initial cost', 'final cost', 'mst_cost' ]
    data = []
    for i in range(0,len(graphs_list)):
        graph_length=len(graphs_list[i])
        draw_graphs.draw_from_pos(graphs_list[i], fileName="res"+str(i), draw=False)
        plt.show()
        X = np.arange(0, len(res_list[i]), 1)
        plt.plot(X,res_list[i],'b--')
        plt.plot( X, mst_cost_list[i], 'r--')
        print(res_list[i])
        print(mst_cost_list[i])
        plt.show()
        temp_data=[str(i), str(graph_length),str(time_list[i]) , str(res_list[i][0]), str(res_list[i][len(res_list[i])-1]),str(mst_cost_list[i][0])]
        data.append(temp_data)
    #write results to file

    with open(filename+'res.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write multiple rows
        writer.writerows(data)
        f.close()

def test_AC_on_grapf_list_with_next_step_optimation(filename,times, s):
    f = open(filename, 'rb')
    gl = pickle.load(f)
    f.close()
    # create res list - every entry is a list of results by ac algorithm
    res_list = []
    # create a list of graph results from AC
    graphs_list = []
    Go = None
    #get normal MST




    #go AC on the first graph

    b, res, Go = AB_DCST(gl[0])

    res_list.append(res)
    #try optimize the next steps
    for i in range(1, len(gl)):
        b, res, Go = AB_DCST(gl[i], isFirst=False, oldGraph=Go, numOfAnts=20)
        res_list.append(res)
        graphs_list.append(b)
    #plot the graphs and the res lists
    for i in range(0, len(graphs_list)):
        draw_graphs.draw_from_pos(graphs_list[i], fileName="55", draw=False)
        plt.plot(res_list[i], 'r--')


def main():
    test_AC_on_grapf_list("distances_2_1_nodes_vg_graphs_200",times=5, s=50 )


   #get a list of graphs from file take the first place just for sports
    # f = open("distances_5_0.4_nodes_vg_graphs" , 'rb')
    # gl_n = pickle.load(f)
    # f.close()
    #graphs_list = []

    # r = open("distances_5_0.4_nodes_vg_graphs" , 'rb')
    # gl = pickle.load(r)
    # r.close()



    #plt.show()

    #plt.plot(res_list, 'r--')

    #draw_graphs.draw_from_pos(g.vg)
    #print(g.vg.edges)
    #print(g.sum_phermones(), "sum phermones before")


    #normal AC as we know it
    # res_list=[]
    # graphs_list=[]
    # Go=None
    # for g in gl:
    #     b,res,Go=AB_DCST(g,isFirst=False, oldGraph=Go, numOfAnts=0)
    #     print("res:",res)
    #     graphs_list.append(Go)
    #     res_list.append(res)

   # my way:
   #  res_list_new = []

   #first time
    # b, res ,Go= AB_DCST(gl_n[0])
    #
    # res_list_new.append(res)
    #
    # for i in range(1,len(gl_n)):
    #     b, res,Go = AB_DCST(gl_n[i], isFirst=False, oldGraph=Go, numOfAnts=20 )
    #     res_list_new.append(res)



    #draw_graphs.draw_from_pos(b)

    #print(g.sum_phermones(), "sum phermones after1")

    #b1,res1 = AB_DCST(gl[1])

    #draw_graphs.draw_from_pos(b1)



    #print(g.sum_phermones(), "sum phermones after1")
    #print(gl[1].sum_phermones(), "sum phermones after2")


   #
   #  columns = 3
   #  rows = 2
   #
   #  for i in range(0, len(graphs_list)):
   #      draw_graphs.draw_from_pos(graphs_list[i].vg, fileName="55", draw=False)
   #  #plt.show()
   #
   #  plt.plot(res_list, 'r--')
   # # plt.plot(res_list_new, 'b--')
   #
   #
   #  #plt.plot(res, 'g--')
   #
   #  plt.show()
   #  print(res )

if __name__ == "__main__":
    main()