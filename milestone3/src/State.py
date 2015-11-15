#!/usr/bin/env python

from Node_Map import Node_Map

class State:
    """ Class repressenting a state of our problem
    """

    def __init__(self, node_map, objetives = None):

        if not isinstance(node_map, Node_Map): 
            raise TypeError        
        self.node_map=node_map

        if objetives is None:
            self.objetive_nodes = []
        else:
            self.objetive_nodes = objetives

        
    def __repr__(self):
        return str(self.node_map)

