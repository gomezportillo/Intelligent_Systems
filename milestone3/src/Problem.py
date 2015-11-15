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
            
        print "Analysis of the .som file:\nLines: " + str(i) + " | Nodes: " + str(n_nodes) + " | Connections: " + str(n_conex) + "\n"
        
        try:
            print self.hash_table[self.initial_state.node_map.key]
        except:
            print "Node "+ sys.argv[1] +" not available on this map" 
            sys.exit(0)
        
 
    def expand_frontier(self):
        
        self.frontier = []
        initial_node = Node_Tree(self.initial_state)        
    
        heapq.heappush(self.frontier, initial_node)
        timestamp1 = datetime.datetime.now()

        while True: 

            prev_node = heapq.heappop(self.frontier)
            successors_list = self.state_space.getSuccessors(prev_node.state, self.hash_table)

            for successor in successors_list: #successor[0]=action, successor[1]=state, successor[2]=cost
                node = Node_Tree(successor[1], prev_node.cost+successor[2], successor[0], prev_node.depth+1, 
                                 prev_node.state.node_map, randint(0,100000))

                heapq.heappush(self.frontier, node)
    
                if len(self.frontier)%100000==0: 
                    #if len(self.frontier)>10: #para imprimirlo en orden
                    #    while(len(self.frontier)):
                    #    print heapq.heappop(self.frontier)
                    #    sys.exit(0)

                    print datetime.datetime.now() - timestamp1
                    print "Size of frontier: "+ str(len(self.frontier))
                    #timestamp1 = datetime.datetime.now()

    def isGoal(self, state):
       return len(state.objetive_nodes) == 0

    def search(self, strategy, max_depth=10000, incr_depth=1):
        
        current_depth = incr_depth
        solution = None
        
        while not solution and current_depth <= max_depth:
            solution = self.bounded_search(strategy, current_depth)
            current_depth = current_depth + incr_depth

        return solution


    def bounded_search(self, strategy, max_depth=10000):

        self.frontier = []
        initial_node = Node_Tree(self.initial_state)
        heapq.heappush(self.frontier, initial_node)
        solution = False

        while not solution and len(self.frontier) <> 0:
            current_node = heapq.heappop(self.frontier)

            if self.isGoal(current_node.state):
                solution = True

            else:
                successors_list = self.state_space.getSuccessors(current_node.state, self.hash_table) #aka LS
                successor_nodes = self.create_nodes(successors_list, current_node, max_depth, strategy) #aka LN

                for node in successor_nodes:
                    heapq.heappush(self.frontier, node)
    
        if solution:
            return self.create_solution(current_node)
        else:
            return None 


    def create_nodes(self, successors_list, parent_node, max_depth, strategy): #en este metodo pasa la magia

        successor_nodes = []
        
        for succ in successors_list:

            state = succ[1]              
            cost = parent_node.cost + succ[2]
            street = succ[0]
            depth = parent_node.depth + 1
            parent = parent_node
            value = 0

            if strategy == Searching_Strategies.BFS:
                value = parent_node.depth + 1

            elif strategy == Searching_Strategies.DFS:
                value = -(parent_node.depth + 1)

            elif strategy == Searching_Strategies.DLS:
                value = -(parent_node.depth + 1)

            elif strategy == Searching_Strategies.IDS:
                value = -(parent_node.depth + 1)

            elif strategy == Searching_Strategies.UC:
                value = cost

            current_succesor = Node_Tree(state, cost, street, depth, parent, value)                 

            successor_nodes.append(current_succesor)

        return successor_nodes
        


    def create_solution(self, final_node): #ir tirando de parents hasta llegar al nodo incial, parent=null
        
        current_node = final_node
        stack = [current_node]

        while current_node.parent is not None:
            stack.append(current_node.parent)
            current_node = current_node.parent

        return stack




