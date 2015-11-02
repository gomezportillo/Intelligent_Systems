#!/usr/bin/python

class State:
    '''Class repressenting a state of our problem'''
    def __init__(self, id_state):
        self.id_state=id_state

    def __repr__(self):
        return self.id_state

