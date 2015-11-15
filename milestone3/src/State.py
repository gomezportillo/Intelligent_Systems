from Node_Map import Node_Map

class State:
    '''Class repressenting a state of our problem'''

    def __init__(self, node_map, objetives):

        if not isinstance(node_map, Node_Map): 
            raise TypeError
        
        self.node_map=node_map
        self.objetive_nodes = objetives

    def __repr__(self):
        return self.node

