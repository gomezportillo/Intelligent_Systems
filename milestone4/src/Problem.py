#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Usage: python {0} <node>"

import math
import sys
import datetime
import heapq

from State import State
from State_Space import State_Space
from Node_Tree import Node_Tree
from Adyacent_Node import Adyacent_Node
from Node_Map import Node_Map
from auxiliary_functions import distance_on_unit_sphere
from auxiliary_functions import Searching_Strategies

class Problem:
    
    def __init__(self, state_space, initial_state): 
        self.state_space = state_space
        self.initial_state = initial_state
        self.hash_table = {}
    

    def build_hash_table(self):
        
        with open('data/map.osm') as f: #reading the .osm file
            lines = f.readlines()
    
        n_nodes = 0
        n_conex = 0
        we_are_in_ways_section = False
        tmpList = []
        current_city = ""
    
        for i in range(0, len(lines) - 1): #building the hash table
    
            if (lines[i].find("<way") != -1): 
                we_are_in_ways_section = True
        
            if (lines[i].find("<node") != -1):
                tokenized_line = lines[i].split('"')
                n_nodes += 1
                self.hash_table[tokenized_line[1]] = Node_Map(tokenized_line[1], tokenized_line[15], tokenized_line[17])
        
        
            if ((lines[i].find("<nd ref=") != -1) and (lines[i - 1].find("<nd ref=") != -1)):
                previous_line = lines[i - 1].split('"')
                current_line = lines[i].split('"')
                tmpList.append((previous_line[1], current_line[1]))
                n_conex += 1
            
            
            if ((we_are_in_ways_section) and (lines[i].find("name") != -1)):
                current_line = lines[i].split('"')
                current_city = current_line[3]
                
                for node, ady_node in tmpList:           
                    self.hash_table[node].add_node(Adyacent_Node(ady_node, current_city, 
                                                                distance_on_unit_sphere(self.hash_table[node], 
                                                                self.hash_table[ady_node])))

                    self.hash_table[ady_node].add_node(Adyacent_Node(node, current_city, 
                                                                    distance_on_unit_sphere(self.hash_table[ady_node], 
                                                                    self.hash_table[node])))
                
                tmpList = []
                
            #sys.stdout.write("\r" + str(int(round((float(i)/len(lines))*100))) + "% of the data imported from the .osm file")
            
        print "Analysis of the .osm file: lines: " + str(i) + ", nodes: " + str(n_nodes) + ", connections: " + str(n_conex)
        
        try: #preguntar si esto lo deberiamos seguir haciendo
            self.hash_table[self.initial_state.node_map.key]
        except:
            print "Node "+ sys.argv[1] +" not available on this map" 
            sys.exit(0)
        
    def isGoal(self, state):
       return len(state.objetive_nodes) == 0


