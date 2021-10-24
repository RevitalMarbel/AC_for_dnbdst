import random
from networkx.utils import open_file

import pickle
import networkx as nx
import matplotlib.pyplot as plt
import math
#class that represent the visibility graph for a given data in a specific time period
#parameter: nodes: a list of nodes
#nodes=[id, lat, lon, alt]
import collections
#from matplotlib import pyplot as plt

#this dictionary holds the edges list (with its weight) for each time
import distance_functions
from distance_functions import get_area_from_distances_file

edges_by_time={}
object_by_time={}

#method: 0 for vg, 1 for robust.
class VG:
    def __init__(self, nodes, names,dist_file_name, max_neighbors,  minDist, maxDist=500, upp_bound=500,  time=0, initPher=1, ratio=1, method=0):
        self.nodes=nodes
        self.time=int(time)
        self.names=names

        self.ants={}
        self.ants[1]=1

        #max edge cost
        self.max_cost=0
        #min edge cost
        self.min_cost=0


        self.initPher=initPher
        self.max_neighbors=max_neighbors
        self.maxP=0
        self.minP=0
        self.minDist=minDist
        G= nx.Graph()
        pos={}
        alt={}
        name={}
        visited={}
        index={}
        #add nodes by id
        for i in range(len(nodes)):
            #G.add_node(i[0])
            G.add_node(names[i])
        #add location as pos:
        for i in range(len(nodes)):
            if(nodes[i][1])>180:
                pos[names[i]] = (nodes[i][1]-360, nodes[i][2])
            else:
                pos[names[i]]=(nodes[i][1],nodes[i][2])
        #add altitude as alt
        for i in range(len(nodes)):
            alt[names[i]] = nodes[i][3]
        #add names to to self dict
        for i in range(len(nodes)):
            name[names[i]] = names[i]

        for i in range(len(nodes)):
            visited[names[i]] = 'no'

        for i in range(len(nodes)):
            index[names[i]] = i


        #print(names)
        #print(G.nodes)
        nx.set_node_attributes(G, index, 'index')
        nx.set_node_attributes(G, name, 'name')
        nx.set_node_attributes(G, pos, 'pos')
        nx.set_node_attributes(G, alt, 'alt')
        nx.set_node_attributes(G, visited, 'visited')
        self.vg=G
        self.pos=pos

        #self.robust_list=get_area_from_distances_file(dist_file_name, tresh=minDist)
        self.distances=distance_functions.get_distance_from_distances_file(dist_file_name, time)
        print(self.distances)
#        print(self.distances['24_61'])
        #print(self.distances)
        #print(len(self.distances.values ()), "distances")
        #print(len(self.robust_list.values()), "robust_list")
        #print(self.robust_list)
        #basicly - add the edges according the vg mindist factor
        #self.compute_vg()

        #print('567_624', self.dists)
        if method==1:
            self.compute_vg_for_robust( upperBound= upp_bound, ratio=ratio)
        if method==0:
            self.compute_vg()

       #self.init_ants()
        edges_by_time[time]=self.vg
        object_by_time[time] = self
        # assign each ant to a node for AC algorithm


        #assign phermodne level to each edge
        #self.init_phermones()

    def draw_graph(self, ant=False, edgeList=[], draw=False, name="stam"):
        plt.figure(figsize=(16, 8))
        #fig, ax = plt.subplots()
        nx.draw_networkx_labels(self.vg, self.pos,font_size=5,font_color='r')
        #nx.draw_networkx_edges(self.vg, self.pos, nodelist=self.nodes[0], alpha=0.4)
        nx.draw_networkx_nodes(self.vg, self.pos, nodelist=list(self.pos.keys()),node_size=60)
        nx.draw_networkx_edges(self.vg, self.pos, edgelist=list(self.vg.edges()), edge_color='b', width=2)  # highlight elist
        #if ant:
            #nx.draw_networkx_nodes(self.vg, self.pos, nodelist=[self.ants[1],self.ants[197], self.ants[41]],node_size=50, node_color='red')
                               #,cmap=plt.cm.Reds_r, with_labels = True)
        #plt.draw()
        laat_min= min(self.pos.items(), key=lambda x: x[1])
        lat_max = max(self.pos.items(), key=lambda x: x[1])
#       lon_min = min(self.pos.items(), key=lambda x: x[2])
#       lon_max = max(self.pos.items(), key=lambda x: x[2])
#       plt.set_xlim(laat_min, lat_max)
        #plt.grid(axis='y', linestyle='-')
        #plt.grid(True, which='both',axis='both')
        if draw==True:
            plt.show()
        else:
            plt.savefig(name+'.png')

    def draw_Tree(self, Tree, edgeList=[], draw=False, name=""):
            plt.figure(figsize=(16, 8))
            # fig, ax = plt.subplots()
            nx.draw_networkx_labels(self.vg, self.pos, font_size=5, font_color='r')
            nx.draw_networkx_edges(Tree, self.pos, nodelist=self.nodes[0], alpha=0.4)
            nx.draw_networkx_nodes(self.vg, self.pos, nodelist=list(self.pos.keys()), node_size=60)
            nx.draw_networkx_edges(Tree, self.pos, edgelist=edgeList, edge_color='r', width=2)  # highlight elist
            # if ant:
            # nx.draw_networkx_nodes(self.vg, self.pos, nodelist=[self.ants[1],self.ants[197], self.ants[41]],node_size=50, node_color='red')
            # ,cmap=plt.cm.Reds_r, with_labels = True)
            # plt.draw()
            laat_min = min(self.pos.items(), key=lambda x: x[1])
            lat_max = max(self.pos.items(), key=lambda x: x[1])
            #        lon_min = min(self.pos.items(), key=lambda x: x[2])
            #        lon_max = max(self.pos.items(), key=lambda x: x[2])
            #        plt.set_xlim(laat_min, lat_max)
            # plt.grid(axis='y', linestyle='-')
            # plt.grid(True, which='both',axis='both')
            if draw == True:
                plt.show()
            else:
                plt.savefig(name + '.png')

    def distance4(self,lat1, lat2, lon1, lon2, ratio):

        R = 6373.0+550

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = (R * c)/ratio
        return distance

    def ang_distance4(self, lat1, lat2, lon1, lon2, ratio):
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)
        lon1 = math.radians(lon1)
        lon2 = math.radians(lon2)

        d=math.atan2(math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1),math.sin(lon2 - lon1) * math.cos(lat2))
        d=math.degrees(d)
        d=math.fabs(d)
        return d/ratio

    def ang_distance(self, node1, node2, ratio=1):
        p1 = self.vg.nodes[node1]['pos']
        p2 = self.vg.nodes[node2]['pos']
        return self.ang_distance4(p1[0], p2[0], p1[1], p2[1], ratio)

    def distance(self, node1, node2, ratio=1):
        p1=self.vg.nodes[node1]['pos']
        p2 = self.vg.nodes[node2]['pos']

        return self.distance4(p1[0], p2[0],p1[1],p2[1],ratio)

    def isLOS(dist, tresh):
        if (dist < tresh):
            return True
        return False

    #i is always smaller than j
    def compute_edges_robust(self):
        for u, v, a in self.vg.edges(data=True):
            if(u<v):
                self.vg[u][v]["robust"]=self.compute_edge_robust(u,v)
            else:
                self.vg[u][v]["robust"] = self.compute_edge_robust(v, u)

    def compute_edge_robust(self, i,j):

        if str(i)+"_"+str(j) in  self.robust_list:
            #print(str(i)+"_"+str(j), self.dists[str(i) + "_" + str(j)])
            robust=self.robust_list[str(i) + "_" + str(j)]
        else:
            #print(str(i) + "_" + str(j), -1)
            robust=-1
        return robust

    def compute_vg_for_robust_2(self, upperBound, ratio=1):
        max=0
        min=1
        if (len(edges_by_time) == 0): #first time
            diff_c = 0
            for key, value in self.robust_list.items():
                if float(value)< upperBound/ratio:
                    e=key.split("_")
                    #print(e[1], e[0])
                    e0=int(e[0])
                    e1 = int(e[1])
                    if(key  in self.distances):
                        d = self.distances[key]
                        self.vg.add_edge(e0, e1, weight=d, robust=float(value), ph=self.initPher, update=0, diff=diff_c)
                        max = self.vg[e0][e1]['weight']
                        min = self.vg[e0][e1]['weight']
                    else:
                        print(-1, key)

        else:
            for key, value in self.robust_list.items():
                if float(value)< upperBound/ratio:
                    e=key.split("_")
                    e0 = int(e[0])
                    e1 = int(e[1])
                    if (key in self.distances):
                        d = self.distances[key]
                        self.vg.add_edge(e0, e1, weight=d, robust=float(value), ph=self.initPher, update=0, diff=d)
                        max = self.vg[e0][e1]['weight']
                        min = self.vg[e0][e1]['weight']
                    else:
                        print(-1, key)


        for w in self.vg.edges.data('weight'):
            w=w[2]
            if max<w:
                max=w
            if min>w:
                min=w
        self.max_cost=max
        self.min_cost=min
        #iso=list(nx.isolates(self.vg))
        #print(iso)
        #self.ants=[x for x in self.ants if x not in iso]

        #update the initial phermones level for each edge
        for w in self.vg.edges.data():
            w=w[2]
            w['ph']=(self.max_cost-w['weight'])+(self.max_cost-self.min_cost)/3

        # self.vg.remove_nodes_from(iso)

    def compute_vg_for_robust(self, upperBound,ratio=1):
        min = 0
        max = 1
        for i in self.vg.nodes:
            for j in self.vg.nodes:
                if (self.vg.nodes[i]["index"]<  self.vg.nodes[j]["index"]):
                        r = self.robust_list[str(i) + "_" + str(j)]
                        d = self.distances[str(i) + "_" + str(j)]
                       # d=self.distance(i,j, ratio)
                        if r!=-1:
                                #r=d
                            if (len(edges_by_time) > 0):
                                diff_c = 0
                                if (r < upperBound / ratio):
                                    self.vg.add_edge(i, j, weight=d ,robust=r, ph=self.initPher, update=0, diff=diff_c)
                                    max = self.vg[i][j]['weight']
                                    min = self.vg[i][j]['weight']
                            else:  # first time ....

                                if (r < upperBound / ratio):
                                    self.vg.add_edge(i, j, weight=d,robust=r, ph=self.initPher, update=0, diff=d)
                                    max = self.vg[i][j]['weight']
                                    min = self.vg[i][j]['weight']
        for w in self.vg.edges.data('weight'):
            w=w[2]
            if max<w:
                max=w
            if min>w:
                min=w
        self.max_cost=max
        self.min_cost=min
        #iso=list(nx.isolates(self.vg))
        #print(iso)
        #self.ants=[x for x in self.ants if x not in iso]

        #update the initial phermones level for each edge
        for w in self.vg.edges.data():
            w=w[2]
            w['ph']=(self.max_cost-w['weight'])+(self.max_cost-self.min_cost)/3

        # self.vg.remove_nodes_from(iso)

    def  compute_vg(self, ratio=1, func=0):  # 0 for regular distance and 1 for ang_distance
        min=0
        max=1
        for i in self.vg.nodes:
            for j in self.vg.nodes:
                if(self.vg.nodes[i]["index"]<  self.vg.nodes[j]["index"]):# and  'str(i)+"_"+str(j)' in self.distances.keys()):
                    if(func==0):
                        #d= self.distance(i,j, ratio)
                        #print(i, j)
                        d=self.distances[str(i)+"_"+str(j)]

                        if (len(edges_by_time)>0):
                          #  diff_c = d - edges_by_time[self.time - 1][i][j]['weight']
                            diff_c=0
                            #if(d>minDist/ratio):
                                #self.vg.add_edge(i, j, weight=math.inf, ph=self.initPher, update=0, diff=math.inf)
                                #min = self.vg[i][j]['weight']
                            if(float(d)<=self.minDist/ratio and float(d)>5000):
                                #print(" d", d, " ",self.minDist/ratio)
                                self.vg.add_edge(i,j,weight=d, ph=0, update=0, diff=diff_c)
                                max = self.vg[i][j]['weight']
                                min = self.vg[i][j]['weight']
                        else: #first time ....
                           # if (d > minDist / ratio):
                               # self.vg.add_edge(i, j, weight=math.inf, ph=self.initPher, update=0, diff=math.inf)
                               #min = self.vg[i][j]['weight']
                            if (d <= self.minDist / ratio and float(d)>5000):
                                self.vg.add_edge(i, j, weight=d, ph=0, update=0, diff=0)
                                max = self.vg[i][j]['weight']
                                min = self.vg[i][j]['weight']
                    else:
                        d = self.ang_distance(i, j, ratio)
                        #print(d, minDist, ratio)
                        if (len(edges_by_time) > 0):
                            #  diff_c = d - edges_by_time[self.time - 1][i][j]['weight']
                            diff_c = 0
                            # if (d > minDist / ratio):
                            #     self.vg.add_edge(i, j, weight=math.inf, ph=self.initPher, update=0, diff=math.inf)
                            #     min = self.vg[i][j]['weight']
                            if (d <= self.minDist / ratio):
                                self.vg.add_edge(i, j, weight=d, ph=self.initPher, update=0, diff=diff_c)
                                max = self.vg[i][j]['weight']
                        else:  # first time ....
                            # if (d > minDist / ratio):
                            #     self.vg.add_edge(i, j, weight=math.inf, ph=self.initPher, update=0, diff=math.inf)
                            #     min = self.vg[i][j]['weight']
                            if (d <= self.minDist / ratio):
                                self.vg.add_edge(i, j, weight=d, ph=self.initPher, update=0, diff=d)
                                max = self.vg[i][j]['weight']
            #remove isolated nodes- the graph must be connected

        for w in self.vg.edges.data('weight'):
            w=w[2]
            if max<w:
                max=w
            if min>w:
                min=w
        self.max_cost=max
        self.min_cost=min
        #iso=list(nx.isolates(self.vg))
        #print(iso)
        #self.ants=[x for x in self.ants if x not in iso]

        #update the initial phermones level for each edge
        for w in self.vg.edges.data():
            w=w[2]
            w['ph']=(self.max_cost-w['weight'])+(self.max_cost-self.min_cost)/3

        # self.vg.remove_nodes_from(iso)

    def init_phermones(self, old=None):
        #if(old== None):
            for e in self.vg.edges(data=True):
                M=self.max_cost
                m=self.min_cost
                #print(e)
                c=e[2]['weight']
                #e[2]['ph']=(M-c)+(M-m)/3
                e[2]['ph'] = 0
                #e[2]['ph']=1/c
                e[2]['update']=0
                #print(e[2]['weight'],e[2]['ph'] )
        # else:
        #     for e in self.vg.edges(data=True):
        #         e[2]['ph'] =old.vg.edges[e[0], e[1]]['ph']
        #         e[2]['update'] = 0

    def   init_ants(self, old=None, numOfAnts=0):
        self.ants={}
        if(old ==None):
            for i in self.vg.nodes:
               self.ants[i]=i
        else:
            for i in self.vg.nodes:
                self.ants[i] = old.ants[i]
            #edges = sorted(self.vg.edges.data('diff'))
            edges = sorted([i for i in self.vg.edges.data('diff')], key=lambda item:item[2])
            #edges = {k for k in sorted(self.vg.edges.data('diff'), key=lambda item: item[2], reverse=True)}
            edges=edges[:numOfAnts ]
            #plant ants adjecent to the first 5 edges with low diff
            for e in edges:
                r=random.randrange(len(self.ants))
                self.ants[r]=e[0]


    def move(self, ant_num,node):
        #print("ant", node)
        n=self.vg.neighbors(node)
        # for i in n:
        #  print(i, type(i))
        #if len(list(n))>0:
        edgesCose={}
        for i in n:
                edgesCose[i]=(self.vg[node][i]['weight'])
        edgesCose = {k: v for k, v in sorted(edgesCose.items(), key=lambda item: item[1], reverse=True)}
        #edgesCose=collections.OrderedDict(sorted(edgesCose.items()))


                #choose the next neighbor
        if(len(edgesCose)<1):
                    #print(edgesCose, "empty")
                print(" empty")
        else:
            k=self.wheel(edgesCose)
            e_cost=self.vg[node][k]['weight']
            self.vg[node][k]['update']=self.vg[node][k]['update']+1/e_cost
            self.ants[ant_num]=k



    def old_move(self, ant_num,node):
        #print("ant", node)
        n=self.vg.neighbors(node)
        # for i in n:
        #  print(i, type(i))
        #if len(list(n))>0:
        edgesCose={}
        for i in n:
                edgesCose[i]=(self.vg[node][i]['weight'])
        edgesCose = {k: v for k, v in sorted(edgesCose.items(), key=lambda item: item[1], reverse=True)}
        #edgesCose=collections.OrderedDict(sorted(edgesCose.items()))

        for i in range(5):
                #choose the next neighbor
                if(len(edgesCose)<1):
                    #print(edgesCose, "empty")
                    print(" empty")
                else:
                    k=self.wheel(edgesCose)
                    #print(k)
                    #print(self.vg.nodes[k])
                    if self.vg.nodes[k]['visited']=='no':
                            self.vg.nodes[k]['visited']='yes'
                            self.vg[node][k]['update']=self.vg[node][k]['update']+1
                            #move the ant to the new node
                            #print(k)
                            self.ants[ant_num]=k
                            #print('ant', node, 'moved to',k)
                            break

    #assume the costs is sorted dict
    #this fuction returns the key (neighbor) tht was choosen randomly with respect to its weight
    def wheel(self, costs):
        #this dict is the prob array
        costs=self.normalize(costs)
        accumulative={}
        sum=0
        for k,v in costs.items():
            accumulative[k]=sum+v
            sum+=v
        r= random.random()
        for k,v in costs.items():
            if r<v:
                return k
        return k


    #data is a dictionary, the items needs to be normalized
    def normalize(self, data):
       # print(data)
        minn= min(data.items())[1]
        maxx=max(data.items())[1]
        res={}
        if minn==maxx:
            for k, v in data.items():
                res[k] = 0.5
        else:
            for k, v in data.items():
                res[k]= (v-minn)/(maxx-minn)
        return res

#the value is the node wehre the ant is at.
    def move_all(self):
        for k, v in self.ants.items():
            self.move(ant_num=k, node=v)
        for k,v in self.ants.items():
            self.vg.nodes[v]['visited']='no'

    def update_edge_phermone(self,P, IP ,nue=0.01):
        #P=cuurent phermones, IP= new calculation
        new_p=(1-nue)*P+nue*IP
        # if(new_p!=P):
        #     print("new", new_p, "old", P)
        return new_p

    def old_update_edge_phermone(self,P, number_of_updates, IP ,nue):
        new_p=(1-nue)*(P)+number_of_updates*IP
        # if(new_p!=P):
        #     print("new", new_p, "old", P)
        return new_p

    def update_phermones(self, nue=0.5):

        for e in self.vg.edges(data=True):
                IP=e[2]['update']
                u=self.update_edge_phermone(e[2]['ph'], IP, nue)
                e[2]['ph'] =u

    def old_update_phermones(self, nue=0.5):
        self.maxP=1000*((self.max_cost-self.min_cost)+(self.max_cost-self.min_cost)/3)
        #self.maxP = 1000 * ((self.max_cost - self.min_cost) + (self.max_cost - self.min_cost) / 3)

        self.minP=(self.max_cost-self.min_cost)/3
        for e in self.vg.edges(data=True):
            #print(e[2])
            #e=e[2]
            if e[2]['update']>0:
                IP=(self.max_cost-e[2]['weight'])+(self.max_cost-self.min_cost)/3
                u=self.update_edge_phermone(e[2]['ph'], e[2]['update'], IP, nue)
                #print(e[2]['update'])
             #   if u>self.maxP:
              #      e[2]['ph']=self.maxP-IP
               # else:
                #    if u<self.minP:
                 #       e[2]['ph']=self.minP+IP
                  #  else:
                e[2]['ph'] =u

    def print_phermones_level(self):

        #print( self.vg.edges.data('ph'))
        res=sorted([i[2] for i in self.vg.edges.data('ph')], reverse=True)
        print(res)

    def sum_phermones(self):
        sum=0
        for i in self.vg.edges.data('ph'):
            sum=sum+i[2]

        return sum

    def treeConstruct(self, buttomPhermonesnum=0):

        edges = self.vg.edges.data()
        #phermones = sorted([i[2] for i in self.vg.edges.data('ph')], reverse=True)

        #print("phermoes" ,phermones )

        costs = {}

        # remove buttom of list
        for i in list(edges):
                costs[(i[0], i[1])] = i[2]['ph']

        srt_phermones = {k: v for k, v in sorted(costs.items(), key=lambda item: item[1],reverse=True)}

        # costs = collections.OrderedDict(sorted(costs.items()))
        #print(srt_phermones.items())


        T = nx.Graph()
        #print(srt_phermones.items())
        for k,v in srt_phermones.items():
            # print(k[0])
            if not T.has_node(k[0]):
                T.add_node(k[0], pos=self.vg.nodes[k[0]]['pos'])
            if not T.has_node(k[1]):
                T.add_node(k[1], pos=self.vg.nodes[k[1]]['pos'])
            if (k[1] not in nx.algorithms.components.node_connected_component(T, k[0])):
                if (len(list(T.neighbors(k[0]))) < self.max_neighbors and len(list(T.neighbors(k[1]))) < self.max_neighbors):
                    T.add_edge(k[0], k[1], weight=self.vg[k[0]][k[1]]['weight'], ph=self.vg[k[0]][k[1]]['ph'])
        if (nx.algorithms.components.is_connected(T)):
            print("connected")
        return T

    def treeConstruct1(self, buttomPhermonesnum=0):

        # create a new edge dict for construction

        topPhermones = self.vg.edges.data()

        # print(topPhermones)
        # sort by phermones level decending order

        phermones = sorted([i[2] for i in self.vg.edges.data('ph')], reverse=True)

        # print("phermoes" ,phermones )

        phermones = phermones[:len(phermones) - buttomPhermonesnum]

        # print("ph",phermones)
        costs = {}

        # remove buttom of list
        for i in list(topPhermones):
            if i[2]['ph'] in phermones:
                # if i in phermones:
                costs[(i[0], i[1])] = i[2]['weight']
                # costs[i[2]['weight']] = (i[0],i[1])

        costs = {k: v for k, v in sorted(costs.items(), key=lambda item: item[1])}
        # costs = collections.OrderedDict(sorted(costs.items()))
        # print(costs.items())
        T = nx.Graph()
        for k, v in costs.items():
            # print(k[0])
            if not T.has_node(k[0]):
                T.add_node(k[0], pos=self.vg.nodes[k[0]]['pos'])
            if not T.has_node(k[1]):
                T.add_node(k[1], pos=self.vg.nodes[k[1]]['pos'])
            if (k[1] not in nx.algorithms.components.node_connected_component(T, k[0])):
                if (len(list(T.neighbors(k[0]))) < self.max_neighbors and len(
                        list(T.neighbors(k[1]))) < self.max_neighbors):
                    T.add_edge(k[0], k[1], weight=v, ph=self.vg[k[0]][k[1]]['ph'])
        if (nx.algorithms.components.is_connected(T)):
            print("connected")
        return T

    def phermon_enjancement(self, enahncmentFactor):
        for e in self.vg.edges.data('ph'):
            curr=self.vg[e[0]][e[1]]['ph']
            orig = 1/self.vg[e[0]][e[1]]['weight']

            self.vg[e[0]][e[1]]['ph'] =curr*enahncmentFactor+(1-enahncmentFactor)*orig


    def old_phermon_enjancement(self, T, enahncmentFactor=1.5):
        for e in T.edges.data('ph'):
            t=enahncmentFactor*T[e[0]][e[1]]['ph']
            IP = (self.max_cost -  T[e[0]][e[1]]['weight']) + (self.max_cost - self.min_cost) / 3
            if t>self.maxP:
                self.vg[e[0]][e[1]]['ph'] =self.maxP- IP
            else:
                if t<self.minP:
                    self.vg[e[0]][e[1]]['ph'] = self.minP + IP

        #return G


    #init diff parameter on edges, recieve also the last time graph
    def init_diff(self,prev):
        if prev!=None:
            for e in self.vg.edges(data=True) :
               # print(e)
               # print(prev.vg.edges[e[0],e[1]])
               if prev.vg.has_edge(e):
                    e[2]['diff']=e[2]['weight']-prev.vg.edges[e[0],e[1]]['weight']
                #e[2]['ph']=prev.vg.edges[e[0],e[1]]['ph']


    # p is the current phermones, i is the cost and d is the diff in time
    def update_phermones_time(self,p, i,d,prev):
        for e in self.vg.edges(data=True):
            #print("old", e[2])
            #e[2]['ph']=i*e[2]['ph']-d*e[2]['diff']+p*(prev.vg.edges[e[0],e[1]]['ph'])
            e[2]['ph']=i*e[2]['ph']-d*(e[2]['diff']*(prev.vg.edges[e[0],e[1]]['ph']))
            # print("new ", e[2])



def cost(G):
    cosst=0
    for i in G.edges.data('weight'):
        cosst+=i[2]
    return cosst
    #sum=0
    #print("check cost")
    # for n, (dist, path) in nx.all_pairs_dijkstra(G,weight='weight'):
    #     for k in dist:
    #         sum+=dist[k]
  #  print("sum",sum)
    return cosst

def draw_G(G,pos , edgeList=[], draw=False, name=""):
    plt.figure(figsize=(16, 8))
    # fig, ax = plt.subplots()
    nx.draw_networkx_labels(G, pos, font_size=5, font_color='r')
    nx.draw_networkx_edges(G, pos, nodelist=G.nodes, alpha=0.4)
    nx.draw_networkx_nodes(G, pos, nodelist=list(pos.keys()), node_size=60)
    nx.draw_networkx_edges(G, pos, edgelist=edgeList, edge_color='r', width=2)  # highlight elist
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
        plt.savefig(name + '.png')

        # C={topPhermones[]}
        #
        # edgesCose = collections.OrderedDict(sorted(edgesCose.values()))
        #
        # #sort by phermones:
        # phermones =sorted(self.vg.edges.data('ph'))
        # #remove last elements
        # phermones = phermones[:len(phermones) - topPhermonesnum]
        # C = collections.OrderedDict(sorted(phermones.items()))
        #
        # phermones = self.vg.edges.data('weight')
        # #C = collections.OrderedDict(sorted(C.items()))

def CreateVGFromFile(node_f_name, names_f_name, disances_f_name ,method, md, num_of_sats=600 ,max_neighbors=4, time=0 , initPher=1, ratio=1):
    file1 = open(node_f_name, 'rb')
    nodes = pickle.load(file1)
    file1.close()

    file2 = open(names_f_name, 'rb')
    names = pickle.load(file2)
    file2.close()
    gList=[]

    for i in range(len(nodes)):
        nodes[i] = nodes[i][:num_of_sats]
        names[i] = names[i][:num_of_sats]
        G= VG(nodes[i], names[i], disances_f_name,minDist=md, max_neighbors=4, time=i, initPher=initPher, ratio=ratio, method=method)
        gList.append(G)
        print("graph: ", i, " created", len(names[i]), "nodes")

    #create a list of graphs in file
    if method==0:
        file_out = open(node_f_name+"_vg_graphs_"+str(num_of_sats), 'ab')
        pickle.dump(gList, file_out)
        file_out.close()
        print("file created",node_f_name+"_vg_graphs")
    if method == 1:
        file_out = open(node_f_name + "_vgr_graphs", 'ab')
        pickle.dump(gList, file_out)
        file_out.close()
        print("file created", node_f_name + "_vgr_graphs")


def main():
    CreateVGFromFile()

if __name__ == "__main__":
    main()