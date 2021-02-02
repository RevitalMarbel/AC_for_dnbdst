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


ratio=1
T_thresh=1000
d_tresh=0.5
import matplotlib.lines as mlines
#import geocoder
#import geocoder
 #"10/01/2017"
res=[]
#falcons=65
falcons=1
seperations=5
trees=[]
def open_distaces_file(name, sats):
    f = open(name+".csv", "w")
    f.write("time")
    for i in range(1,len(sats)-falcons,seperations):
        for j in range(i+1,len(sats)-falcons,seperations):
            f.write(","+str(i)+"_"+str(j))
            distances[str(i)+"_"+str(j)]=[]
    f.write("\n")
    f.close()

#stas is a list of sats
def write_distences_to_file(name, sats, time):
    f = open(name+".csv", "a")
    f.write(str(time))

    for i in range(1,len(sat_lat)-falcons,seperations):
        for j in range(i+1,len(sat_lat)-falcons,seperations):
            #d = ephem.separation(sats[i], sats[j])
            #d=math.degrees(float(d))
            d=distance_functions.distance4(sat_lat[i],sat_lat[j], sat_lon[i],sat_lon[j])
            distances[str(i)+"_"+str(j)].append(d)

            f.write(","+str(d))

    f.write("\n")
    f.close()
    print("wrote line to file")



#ant colony algorithm as sugested here :https://dl.acm.org/doi/abs/10.1145/1143997.1144000
def AB_DCST(G, s=1, nue=0.5):
    cost_b=math.inf
    steps_with_no_improvement=0
    B=nx.Graph()
    for i in range(1):
        for step in range(s):
            if step== (s/3) or step== (2*s/3):
                G.update_phermones(nue)
            print("move all")
            G.move_all()
        print("update phermons")
        G.update_phermones()
        print("construct tree")
        T = G.treeConstruct(buttomPhermonesnum=7000)
        t_cost = visibilityGraph_for_AC.cost(T)
        print("cost ", cost_b, t_cost)
        if cost_b > t_cost:
            cost_b = t_cost
            B=T

            steps_with_no_improvement=0
        else:
            steps_with_no_improvement=+1
        B = G.phermon_enjancement(T)
        nue=- 0.01
        if steps_with_no_improvement>10:
            B = G.phermon_enjancement(T,enahncmentFactor=0.2)
            print("evaporate")
        res.append([i, T, cost_b])
    return B




from datetime import datetime, timedelta
now=datetime.today()
import urllib.request

GPS_list = 'http://www.celestrak.com/NORAD/elements/gps-ops.txt'
StarLink_list = 'http://www.celestrak.com/NORAD/elements/starlink.txt'
GPS2_list = 'http://www.tle.info/data/gps-ops.txt'
GLONASS_list = 'http://www.celestrak.com/NORAD/elements/glo-ops.txt'
GLONASS2_list = 'http://www.tle.info/data/glo-ops.txt'

import ephem

observer = ephem.Observer()
r=3
sep=2
num_of_sat=20
jumps=1
distances={}
t_sat_lat, t_sat_lon =  [], []
for q in range(0,r):


    f_name="distances_"+str(r)+"_"+str(sep)

    sat_lat, sat_lon, sat_name = [], [],[]
    nodes = []
    sats=[]
    #TimeNow = datetime.datetime.now()
    lastHourDateTime = now - timedelta(minutes=sep*q)
    #print(lastHourDateTime)
    observer.date = lastHourDateTime
    observer.lat=0
    observer.lon=0
    counter=0
    with urllib.request.urlopen(StarLink_list) as url:

            tles = url.readlines()
            #print(tles)
            tles = [item.strip() for item in tles]
            tles = [(tles[i],tles[i+1],tles[i+2]) for i in range(0,len(tles)-2,3)]

            s=""
            c=0
            for tle in tles:
                if (counter < num_of_sat * jumps):
                    counter = +jumps
                    try:

                        sat = ephem.readtle(tle[0].decode("utf-8") , tle[1].decode("utf-8") , tle[2].decode("utf-8") )
                        sats.append(sat)
                        rt, ra, tt, ta, st, sa = observer.next_pass(sat)

                        if rt is not None and st is not None:
                            sat.compute(observer)

                            text = tle[0].decode("utf-8")
                            if "FALCON" not in text:
                                text_temp=[int(s) for s in text.split('-' or ' ') if s.isdigit()]
                                if(len(text_temp) >0):
                                  #  print(text_temp)
                                    text=text_temp[0]

                                    sat_lat.append(np.rad2deg(sat.sublat))
                                    sat_lon.append(np.rad2deg(sat.sublong))
                                    nodes.append([c,sat_lat[c],sat_lon[c],1])
                                    c+=1

                                    sat_name.append(text)

                    except ValueError as e:
                        print(e)
                #print(len(sats),"length")
                #s = ephem.separation(sats[0], sats[1])
        ###################    write distances_to_file    (next 3 lines)#################################
                # if(q==0):
                #     open_distaces_file(f_name, sats)
                # write_distences_to_file(f_name,sats,lastHourDateTime)

            t_sat_lat.append(sat_lat)
            t_sat_lon.append(sat_lon)
            #print(math.degrees(float(s)), "seperation", s ,"degrees")

    print(nodes)
    print(sat_name)
    G=visibilityGraph_for_AC.VG(nodes, sat_name,dist_file_name="distances_5_2" ,time= q,minDist=T_thresh, ratio=ratio)

    #nx.write_gpickle(G, str(num_of_sat)+" "+str(jumps)+"_"+str(q))

    T= G.vg
    print("'tree" ,T.edges)
    st=nx.algorithms.minimum_spanning_tree(T, weight="robust" ,algorithm="kruskal" )
    trees.append(T)

  #  T=AB_DCST(G)
    print("done")
    #edgeList = [e for e in T.edges]
    #G.draw_graph(ant=False, edgeList=edgeList, draw=True, name="")

    plt.show()
draw_graphs.plot_lat_lon_in_time(t_sat_lat,t_sat_lon, 3)
dist=[]


Treefile = open('treePickle', 'ab')
pickle.dump(trees, Treefile)
Treefile.close()


dbfile = open('distancesPickle1', 'ab')
pickle.dump(distances, dbfile)
dbfile.close()
#res= distance_functions.get_function_from_distances_file(dbfile)

#
# for i in range(0,r):
#     G=visibilityGraph_for_AC.object_by_time[i]
#     G_t=nx.shortest_path(G.vg, source=1173, target=1043,weight='diff',method='dijkstra')
#     dist.append(G.ang_distance(1173,1043))
#     edgeList= [(G_t[e],G_t[e+1]) for e in range(len(G_t)-1)]
#
# t=np.linspace(0,r,r)
# dist=np.array(dist)






#########################unmark to plot###############################

#G.draw_graph(ant=True)
#plt.plot([i[0] for i in res ], [i[2] for i in res])
#plt.show()





    # poss=dict(T.nodes(data='pos'))
    # print(poss)
    # #G1=nx.algorithms.sparsifiers.spanner(G.vg, 25000, weight='weight', seed=None)
    # nx.draw(T, pos=poss,node_size=80)
    #
    #
    #
    # #plot not as graph:
    # print(sat_lat[0], sat_lon[0], sat_lat[1], sat_lon[1])
    # fig, ax = plt.subplots(figsize = (8,7))
    # ax.scatter(sat_lat, sat_lon, zorder=1, alpha= 0.2, c='b', s=10)
    # ax.set_title('starlink sattlites'+str(datetime.datetime.now()))
    # #
    # # for i in range(len(sat_lat)):
    # #     for j in range(len(sat_lon)):
    # #         d= distance(sat_lat[i], sat_lat[j], sat_lon[i], sat_lon[j])
    # #         if(isLOS(d)):
    # #             ax.plot([sat_lat[i], sat_lat[j]],[sat_lon[i], sat_lon[j]])
    # #
    # plt.show()