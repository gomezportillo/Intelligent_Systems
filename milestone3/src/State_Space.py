from State import State
from Node_Map import Node_Map

class State_Space: #hacer un constructor con los limites geograficos del mapa
    '''Class repressenting the state space of our problem'''

    def __init__(self, boundary_coordinates):
        self.latitute_range = (boundary_coordinates[0],boundary_coordinates[2])
        self.longitud_range = (boundary_coordinates[1],boundary_coordinates[3])
        #self.latitute_range = boundary_coordinates[0:2] El codigo que pienso que funcionaria es el de arriba, este es el viejo
        #self.longitud_range = boundary_coordinates[2:4]

    def getSuccessors(self, prev_state, hash_table):
        
        successors_list = []
        ady_list = hash_table[prev_state.node_map.key].ady_list[:]
        
        for adyacent_node in ady_list:
            action = adyacent_node.street_name            
            cost = adyacent_node.distance

            current_state = State(hash_table[adyacent_node.key]) #crea un estado con los datos del nodo
            
            for objetive_node in prev_state.objetive_nodes: 
                #anyadimos la lista de nodos objetivos del padre al hijo (eliminando este, si existe)            
                if objetive_node <> current_state.node_map.key:
                    current_state.objetive_nodes.append(objetive_node)
                
            successors_list.append((action, current_state, cost))

        return successors_list

    def isValid(self, node):
        
        if not isinstance(node_map, Node_Map): 
            raise TypeError                
        
        vertical_check = latitude_range[0] < node.latitude and node.latitude < latitude_range[1]
        horizontal_check = longitud_range[0] < node.longitud and node.longitud < longitud_range[1]

        return vertical_check and horizontal_check
        
