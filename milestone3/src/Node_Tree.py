#!/usr/bin/env python

from State import State
from random import randint

class Node_Tree:
    """ Class repressenting the node object we will be inserting in our frontier
    """
    def __init__(self, s, c=0, a=None, d=0, p=None, v=0):

        if not isinstance(p, Node_Tree) and p is not None: 
            raise TypeError
        
        self.state = s
        self.cost = c
        self.action = a
        self.depth = d
        self.parent = p
        self.value = v

    def __lt__(self, other):
        if isinstance(other, Node_Tree): 
            return self.value < other.value
        else:
            raise TypeError

    def __gt__(self, other):
        if isinstance(other, Node_Tree): 
            return self.value > other.value
        else:
            raise TypeError

    def __repr__(self):
        return "Node #" +str(self.state.node_map.key) + ", value: " + str(self.value) + ", street: " + str(self.action)

