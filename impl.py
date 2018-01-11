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
                    number = int(word)
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

def remove_edges(graph, n):
    missing_edges_list = []
    edges_list = list(graph.edges())
    edges_len = len(edges_list)
    remove_list = []
    while (n > 0):
        rand_int = random.randint(0, edges_len - 1)
        if (rand_int not in remove_list):
            n -= 1
            remove_list.append(rand_int)

    for remove_index in remove_list:
        graph.remove_edge(*(edges_list[remove_index]))
        missing_edges_list.append(edges_list[remove_index])

    return missing_edges_list

def likelihood(target, predictor):
    count = 0
    for j in target.edges():
        (x, y) = j
        if((x, y) in predictor.edges() or (y, x) in predictor.edges):
            count+=1

    prob = count/(len(predictor.edges()))
    return prob


def link_in_predictor_layer(edge, layer):
    (x, y) = edge
    if((x, y) in layer.edges() or (y, x) in layer.edges()):
        return 1
    else:
        return 0



def assign_likelihood(graphs, target, missing_edges_list):
    predictor = []
    for i in range(len(graphs)):
        if(graphs[i]!=target):
            predictor.append(Layer(graphs[i], 0))

    for i in range(len(predictor)):
        predictor[i].weight = likelihood(target,predictor[i].graph)

    nodes_list = list(target.nodes())

    U = []
    for i in len(nodes_list):
        for j in (i + 1, len(nodes_list)):
            x = nodes_list[i]
            y = nodes_list[j]
            edge_object = Edge(i,j,0)
            U.append(edge_object)


    for j in U:
        if(j.edge_tuple not in target.edges()):
            j.score = 0
            for i in range(len(predictor)):
                j.score = j.score + weight[i]*link_in_predictor_layer(j.edge_tuple,predictor[i])




if __name__ == "__main__":

    target_index = 1
    empty_graph = add_nodes()
    graphs = create_graphs()
    pprint(len(graphs[target_index].edges()))
    missing_edges_list = remove_edges(graphs[target_index], len(graphs[target_index].edges()) / 10)
    pprint(len(graphs[target_index].edges()))
    pprint(missing_edges_list)
    # assign_likelihood(graphs, graphs[target_index])
