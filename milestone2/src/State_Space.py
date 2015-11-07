from State import State

class State_Space:
    '''Class repressenting the state space of our problem'''

    def getSuccessors(self, prev_state, hash_table):#si lo que queremos es un nodo, no tiene sentido que te lo devuelva
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

    def isGoal(self, state):
        if len(state.objetive_nodes) == 0:
            return True
        else:
            return False

    def isValid(self, state): pass

