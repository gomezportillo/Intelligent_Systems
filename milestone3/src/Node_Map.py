class Node_Map:
    """Class repressenting a node in our graph"""   

    def __init__(self, k, lat=0, lon=0):
        self.key = k
        self.latitud = lat
        self.longitud = lon
        self.ady_list = []

    def add_node(self, ady_node):
        self.ady_list.append(ady_node)

    def __repr__(self):
        return "Node map " + str(self.key)

    def toString(self):
        ady_nodes = '\n'
        
        if self.ady_list:
            for item in self.ady_list:
                ady_nodes += (str(item.toString()) + "\n")
        else: 
            ady_nodes = "Empty list"
                
        return "Node #" + str(self.key) + ", latitud: " + str(self.latitud) + ", longitud: " + str(self.longitud) + "\nAdyacent nodes: " + ady_nodes


