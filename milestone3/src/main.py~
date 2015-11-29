#!/usr/bin/env python
# -*- coding: utf-8 -*-
"Usage: python {0} <node> <latMin> <longMin> <latMax> <longMax> <objetive_node1>...<objetive_nodeN>"

from State import State
from Node_Tree import Node_Tree
from Node_Map import Node_Map
from State_Space import State_Space
from Problem import Problem
from auxiliary_functions import Searching_Strategies
import sys


if len(sys.argv) < 7:
    print(__doc__.format(__file__))
    sys.exit(0)

if __name__ == "__main__":

    print "Looking for nodes " + str(sys.argv[6:])

    initial_state = State(Node_Map(sys.argv[1]), sys.argv[6:])

    boundary_coordinates = (sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    p = Problem(State_Space(boundary_coordinates), initial_state)

    p.build_hash_table()

    path = p.search(Searching_Strategies.UC)
    if len(path)==0:
        print "Path not found"
        sys.exit(0)
    print "Path found! Path saved in data/solution.out"
    sys.stdout = open('data/solution.out','w')
    print "Final path to " + str(sys.argv[6:])
    while (len(path)>0):
        print path.pop()



