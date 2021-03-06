from Node_Map import Node_Map

class State:
    '''Class repressenting a state of our problem'''

    def __init__(self, node_map):

        if not isinstance(node_map, Node_Map): 
            raise TypeError

        self.node_map=node_map #map node
        self.objetive_nodes = [] #list with the ID of the nodes we are looking for

    def __repr__(self):
        return self.node

