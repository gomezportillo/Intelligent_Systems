#!/usr/bin/env python
"Usage: python {0} <node>"

import math
import sys
import bisect
import datetime
import heapq

from State import State
from State_Space import State_Space
from Node_Tree import Node_Tree
from Adyacent_Node import Adyacent_Node
from Node_Map import Node_Map
from auxiliary_methods import distance_on_unit_sphere

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
            
        print "Analysis of the .som file:\nLines: " + str(i) + " | Nodes: " + str(n_nodes) + " | Connections: " + str(n_conex) + "\n"
        
        try:
            print self.hash_table[self.initial_state.node_map.key].toString()
        except:
            print "Node "+ sys.argv[1] +" not available on this map" 
            sys.exit(0)
        
 
    def expand_frontier(self):
        
        self.frontier = []
        initial_node = Node_Tree(self.initial_state)        
    
        heapq.heappush(self.frontier, initial_node)
        timestamp1 = datetime.datetime.now()

        while True: #while successor.objetive_nodes <> empty
            prev_node = heapq.heappop(self.frontier)
            successors_list = self.state_space.getSuccessors(prev_node.state, self.hash_table)

            for successor in successors_list: #successor[0]=action, successor[1]=state, successor[2]=cost
                #if successor[1].objetive_nodes is empty we have found a solution
                      #Node_Tree(state, cost, street, depth, parent)
                node = Node_Tree(successor[1], prev_node.cost+successor[2], successor[0], prev_node.depth+1, prev_node.state.node_map)

                heapq.heappush(self.frontier, node)
    
                if len(self.frontier)%10000 == 0:
                    print datetime.datetime.now() - timestamp1
                    print "Size of frontier: "+ str(len(self.frontier))
                    timestamp1 = datetime.datetime.now()


    def isGoal(self, state):
        return self.state_space.isGoal(state)          


