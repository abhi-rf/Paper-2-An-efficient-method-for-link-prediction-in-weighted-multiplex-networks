# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 22:15:28 2018

@author: Dell
"""

class Node:

    def __init__(self, number = None, label = None):
            self.number = number
            self.label = label


class Edge:

    def __init__(self, i = None, j = None, score = None, isMissing = 1):
            self.i = i
            self.j = j
            self.score = score
            self.edge_tuple = tuple([i,j])
            self.isMissing = isMissing

    def __str__(self):
        return "%d --> %d : %.3f -- %d" % (self.i, self.j, self.score, self.isMissing)

    def __repr__(self):
        return str(self)

class Layer:

    def __init__(self, graph, weight):
            self.graph = graph
            self.weight = weight
