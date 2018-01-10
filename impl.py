import networkx as nx
from pprint import pprint
import random
from data_class import Node,Layer,Edge

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
            

#Algorithm 1          
def likelihood(G,H):
    GH = nx.intersection(G,H)
    prob = len(GH.edges())
    prob = prob/(len(H.edges()))
    
    
def link_in_predictor_layer(j,layer):
    if(j in layer.edges()):
        return 1
    else:
        return 0
    
    
             
def assign_likelihood(graphs,target):
    predictor = []
    for i in range(len(graphs)):
        if(i!=target):
            predictor.append(graphs[i])
   
    weight = [0,0,0,0]
    
    for i in range(len(predictor)):
        weight[i] = likelihood(target,predictor[i])
        
    U = []
    for i in target.nodes():
        for j in target.nodes():
            if(i!=j):
                edge_object = Edge(i,j,0)
                e = tuple([edge_object.i,edge_object.j])
                U.append(e)
               
                
    for j in U:
        if(j not in target.edges()):
            j.score = 0
            for i in len(predictor):
                j.score = j.score + weight[i]*link_in_predictor_layer(tuple([j.i,j.j]),predictor[i])
                
                
    

if __name__ == "__main__":
    
    empty_graph = add_nodes()
    graphs = create_graphs()
    print(type(list(graphs[3].edges())[1]))
    print()
    
    