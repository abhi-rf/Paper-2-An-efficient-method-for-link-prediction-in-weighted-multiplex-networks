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

    def __init__(self, i = None, j = None, score = None):
            self.i = i
            self.j = j
            self.score = score

class Layer:

    def __init__(self, number = None, name = None):
            self.number = number
            self.name = name
