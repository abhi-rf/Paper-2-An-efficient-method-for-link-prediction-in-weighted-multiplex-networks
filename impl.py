import networkx as nx
from pprint import pprint
import random
import operator
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

def get_predictors(graphs):
    predictors = []
    for graph in graphs:
        predictors.append(Layer(graph, 0))

    return predictors

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

def layer_likelihood(target, predictor):
    count = 0
    for j in target.edges():
        (x, y) = j
        if((x, y) in predictor.edges() or (y, x) in predictor.edges()):
            count+=1

    prob = count/(len(predictor.edges()))
    return prob

def calculate_edge_scores(target, predictors, missing_edges_list, missing_edges_scores, non_exist_scores):
    node_list = list(target.nodes())
    node_len = len(node_list)
    edges_list = list(target.edges())

    # pprint(edges_list)


    for i in range(0, node_len - 1):
        for j in range(i, node_len - 1):
            x = node_list[i]
            y = node_list[j]

            if (x, y) not in edges_list and (y, x) not in edges_list:
                score = 0
                for layer in predictors:
                    score += (score + (layer.weight * link_in_predictor_layer((x, y), layer.graph)))

                if (x, y) in missing_edges_list or (y, x) in missing_edges_list:
                    missing_edges_scores.append(Edge(x, y, score, 1))
                else:
                    non_exist_scores.append(Edge(x, y, score, 0))

def link_in_predictor_layer(edge, layer_graph):
    (x, y) = edge
    if((x, y) in layer_graph.edges() or (y, x) in layer_graph.edges()):
        return 1
    else:
        return 0

def calculate_auc(n, missing_edges_scores, non_exist_scores):
    beta = 0
    gamma = 0

    missing_len = len(missing_edges_scores) - 1
    non_exist_len = len(non_exist_scores) - 1

    for i in range(int(n)):
        missing_index = random.randint(0, missing_len)
        non_exist_index = random.randint(0, non_exist_len)

        missing_score = missing_edges_scores[missing_index].score
        non_exist_score = non_exist_scores[non_exist_index].score

        if missing_score > non_exist_score:
            beta += 1
        elif missing_score == non_exist_score:
            gamma += 1

    # Note gamma was multiplied by 0.5 because of the previous paper.
    # Note multiplying by 0.5 unusually high auc
    return (beta + (0.5) * gamma) / n


def calculate_precision(delta, missing_edges_scores, non_exist_scores):
    merged_list = missing_edges_scores + non_exist_scores
    merged_list.sort(key = operator.attrgetter('score', 'isMissing'), reverse = True)

    epsilon = 0

    for i in range(int(delta)):
        if merged_list[i] in missing_edges_scores:
            epsilon += 1

    return epsilon / delta


if __name__ == "__main__":

    for target_index in range(5):
        empty_graph = add_nodes()
        graphs = create_graphs()

        target = graphs.pop(target_index)
        # pprint(graphs)

        predictors = get_predictors(graphs)

        for layer in predictors:
            layer.weight = layer_likelihood(target, layer.graph)

        # pprint(len(target.edges()))
        missing_edges_list = remove_edges(target, len(target.edges()) / 10)
        # pprint(len(target.edges()))

        missing_edges_scores = []
        non_exist_scores = []

        calculate_edge_scores(target, predictors, missing_edges_list, missing_edges_scores, non_exist_scores)

        # pprint(missing_edges_scores)
        # pprint(non_exist_scores)

        auc = calculate_auc(1000, missing_edges_scores, non_exist_scores)
        precision = calculate_precision(20, missing_edges_scores, non_exist_scores)

        print("Layer %d : \n\tAUC : %.3f\n\tPre : %.3f" %(target_index + 1, auc, precision))
