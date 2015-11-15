class State_Space:
    '''Class repressenting the state space of our problem'''
    def getSuccessors(self, state, hash_table):
        return hash_table[str(state.id_state)].ady_list[:]

    def isValid(self, state): pass
    def isGoal(self, state): pass

