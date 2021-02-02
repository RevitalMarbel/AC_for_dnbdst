import networkx as nx
import matplotlib.pyplot as plt
import math
#class that represent the visibility graph for a given data in a specific time period
#parameter: nodes: a list of nodes
#nodes=[id, lat, lon, alt]

class VG:
    def __init__(self, nodes,names, time=0 ):
        self.nodes=nodes
        self.time=time
        self.names=names
        G= nx.Graph()
        pos={}
        alt={}
        name={}
        #add nodes by id
        for i in nodes:
            G.add_node(i[0])
        #add location as pos:
        for i in nodes:
            pos[i[0]]=(i[1],i[2])
        for i in nodes:
            alt[i[0]] = (i[3])
        for i in names:
            name[i[0]] = (i[3])
        nx.set_node_attributes(G, name, 'name')
        nx.set_node_attributes(G, pos, 'pos')
        nx.set_node_attributes(G, alt, 'alt')
        self.vg=G
        self.pos=pos

    def draw_graph(self):
        plt.figure(figsize=(8, 8))
        #fig, ax = plt.subplots()
        nx.draw_networkx_edges(self.vg, self.pos, nodelist=self.nodes[0], alpha=0.4)
        nx.draw_networkx_nodes(self.vg, self.pos, nodelist=list(self.pos.keys()),
                               node_size=80)
                               #,cmap=plt.cm.Reds_r, with_labels = True)
        #plt.draw()
        laat_min= min(self.pos.items(), key=lambda x: x[1])
        lat_max = max(self.pos.items(), key=lambda x: x[1])
#        lon_min = min(self.pos.items(), key=lambda x: x[2])
#        lon_max = max(self.pos.items(), key=lambda x: x[2])
#        plt.set_xlim(laat_min, lat_max)
        #plt.grid(axis='y', linestyle='-')
        #plt.grid(True, which='both',axis='both')

        plt.show()

    def distance4(self,lat1, lat2, lon1, lon2):

        R = 6373.0

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance

    def distance(self, node1, node2):
        p1=self.vg.nodes[node1]['pos']
        p2 = self.vg.nodes[node2]['pos']

        return self.distance4(p1[0], p2[0],p1[1],p2[1])

    def isLOS(dist, tresh=1500):
        if (dist < tresh):
            return True
        return False

    def compute_vg(self, minDist):
        for i in range(len(self.nodes)):
            for j in range(i+1, len(self.nodes)):
                d= self.distance(i,j)
                if(d<minDist):
                    self.vg.add_edge(i,j,weight=d)



