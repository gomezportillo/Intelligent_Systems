#!/usr/bin/env python
"Usage: python {0} <node>"

from State import State
from Node_Tree import Node_Tree
from State_Space import State_Space
from Problem import Problem

import sys

if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(1)

if __name__ == "__main__":  
    
    p = Problem(State_Space(), State(Node_Tree(str(sys.argv[1]))))
    p.build_hash_table()
    p.expand_frontier()
        

