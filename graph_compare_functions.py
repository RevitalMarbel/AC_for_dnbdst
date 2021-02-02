import pickle
import networkx as nx
import matplotlib.pyplot as plt
import draw_graphs

def main():
    file1 = "100 5_4"
    file2 = "100 5_3"

if __name__ == "__main__":
    main()
def graph_difference(g1_file_name, g2_file_name):
    G1_obj = nx.read_gpickle(g1_file_name)
    G1 = G1_obj.vg
    G2_obj = nx.read_gpickle(g2_file_name)
    G2 = G2_obj.vg
    out=nx.algorithms.operators.binary.symmetric_difference(G1, G2)
    print(G2.edges)
    print(G1.edges)
    return out

def graph_difference(G1,G2):
    G = nx.algorithms.operators.binary.symmetric_difference(G1, G2)
    size=G.size(weight="weight")
    return size




