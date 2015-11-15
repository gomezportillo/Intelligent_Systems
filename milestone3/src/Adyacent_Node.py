#!/usr/bin/env python

class Adyacent_Node:
    """ Class repressenting an adyacent node to another, giving its node and the distance
    """
    def __init__(self, k, street, dist):
        self.key = k
        self.street_name = street
        self.distance = dist
    
    def __repr__(self):
        return str(self.key)    
       
    def toString(self):
        return str(self.key) + " " + str(self.street_name) + " " + str(self.distance)

