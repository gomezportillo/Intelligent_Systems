from State import State
from random import randint

class Node_Tree:
    '''Class repressenting the node object we will be inserting in our frontier'''   
 
    def __init__(self, s, c=0, a=None, d=0, p=None):
        self.state = s
        self.cost = c
        self.value = randint(0,100000)
        self.action = a
        self.depth = d
        self.parent = p

    def __lt__(self, other):
        if isinstance(other, Node_Tree): 
            return int(self.value) < int(other.value)
        else:
            raise TypeError

    def __repr__(self):
        return "Node tree " +str(self.state.node_map) + ", value: " + str(self.value)

