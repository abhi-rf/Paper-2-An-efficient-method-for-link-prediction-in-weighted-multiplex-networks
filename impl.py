import networkx as nx
from pprint import pprint
import random
from data_class import Node,Layer

node_path = "dataset/CS-Aarhus_nodes.txt"
layer_path = "dataset/CS-Aarhus_layers.txt"
edge_path = "dataset/CS-Aarhus_edges.txt"
layers = ["lunch","facebook","coauthor","leisure","work"]

def add_nodes():
    
    with open(node_path,'r') as f:
        nodes = []
        G = nx.Graph()
        for line in f:
            number = 0
            node_label = ""
            i = 1
            for word in line.split():
                if(i==1):
                    number = word
                    i = i+1
                else:
                    node_label = word
            G.add_node(number, label = node_label)
    
    return G
                
def create_graphs():
    graphs = []
    for i in range(5):
        G = add_nodes()
        graphs.append(G)
        
      
    with open(edge_path,'r') as f:
        for line in f:
            i = 0
            k = 0
            u = 0
            v = 0
            wt = 1
            for info in ((line.split())):
                #print((int(info)))
                if(i==0):
                    k = int(info) - 1
                elif(i==1):
                    u = int(info)
                elif(i==2):
                    v = int(info)
                elif(i==3):
                    wt = int(info)
                i+=1
            graphs[k].add_edge(u,v,weight = wt) 
       
    return graphs
                                   


if __name__ == "__main__":
    
    empty_graph = add_nodes()
    graphs = create_graphs()
    print(len(graphs[3].edges()))
    
    