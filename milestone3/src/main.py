#!/usr/bin/env python
"Usage: python {0} <node>"

from State import State
from Node_Tree import Node_Tree
from Node_Map import Node_Map
from State_Space import State_Space
from Problem import Problem
from auxiliary_functions import Searching_Strategies
import sys

if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(0)

if __name__ == "__main__":      
    
    #initial_state = State(Node_Map(sys.argv[1]))   
    #initial_state.objetive_nodes.append((-1, -2)) #The frontier will never find this node, thus will never stop expanding
    
    #boundary_coordinates = (-3.9719000, 38.9650000, -3.8847000, 39.0062000)
    #p = Problem(State_Space(boundary_coordinates), initial_state)
    p = Problem(State_Space((-3.9719000, 38.9650000, -3.8847000, 39.0062000)), State(Node_Map(sys.argv[1]), [-1,-2]))
    
    p.build_hash_table()
    #p.expand_frontier()
    path = p.search(Searching_Strategies.BFS)
    print "Path: " + str(path)
        













