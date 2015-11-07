#!/usr/bin/env python
"Usage: python {0} <node>"

from State import State
from Node_Tree import Node_Tree
from Node_Map import Node_Map
from State_Space import State_Space
from Problem import Problem

import sys

if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(1)

if __name__ == "__main__":      

    initial_state = State(Node_Map(sys.argv[1]))   
    initial_state.objetive_nodes.append((-1)) #The frontier will never find this node, thus will never stop expanding

    p = Problem(State_Space(), initial_state)
    p.build_hash_table()
    p.expand_frontier()
        

