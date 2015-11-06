
class State:
    '''Class repressenting a state of our problem'''

    def __init__(self, node):
        self.node=node
        self.objetive_nodes = []

    def __repr__(self):
        return self.node

