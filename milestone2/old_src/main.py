#!/usr/bin/env python
"Usage: python {0} <node>"

import math
import sys
import bisect
import datetime

from State import State
from State_Space import State_Space
from Node_Tree import Node_Tree
from Adyacent_Node import Adyacent_Node
from Node import Node


def distance_on_unit_sphere(coord1, coord2):
    """Method for comuting the distance, in meters, from two different geografical coordinates"""
    degrees_to_radians = math.pi / 180.0
    phi1 = (90.0 - float(coord1.latitud)) * degrees_to_radians
    phi2 = (90.0 - float(coord2.latitud)) * degrees_to_radians
    theta1 = float(coord1.longitud) * degrees_to_radians
    theta2 = float(coord2.longitud) * degrees_to_radians
    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) + math.cos(phi1) * math.cos(phi2))
    return math.acos(cos) * 6371000


if __name__ == "__main__":  
    
    HT = {}  # hash table
    
    if len(sys.argv) != 2:
        print(__doc__.format(__file__))
        sys.exit(1)    
        
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
            HT[tokenized_line[1]] = Node(tokenized_line[1], tokenized_line[15], tokenized_line[17])
    
    
        if ((lines[i].find("<nd ref=") != -1) and (lines[i - 1].find("<nd ref=") != -1)):
            previous_line = lines[i - 1].split('"')
            current_line = lines[i].split('"')
            tmpList.append((previous_line[1], current_line[1]))
            n_conex += 1
        
        
        if ((we_are_in_ways_section) and (lines[i].find("name") != -1)):
            current_line = lines[i].split('"')
            current_city = current_line[3]
            
            for node, ady_node in tmpList:           
                HT[node].add_node(Adyacent_Node(ady_node, current_city, distance_on_unit_sphere(HT[node], HT[ady_node])))
                HT[ady_node].add_node(Adyacent_Node(node, current_city, distance_on_unit_sphere(HT[ady_node], HT[node])))
            
            del tmpList
            tmpList = []
            
        #sys.stdout.write("\r" + str(int(round((float(i)/len(lines))*100))) + "% of the data imported from the .osm file")
        
    print "Analysis of the .som file:\nLines: " + str(i) + " | Nodes: " + str(n_nodes) + " | Connections: " + str(n_conex) + "\n"
    
    try:
        print HT[sys.argv[1]].toString()
    except:
        print "Node "+ sys.argv[1] +" not available on this map" 
        sys.exit(0)
    
    
    frontier = []
    state_space = State_Space()
    
    initial_node = Node_Tree(str(sys.argv[1]))
    bisect.insort(frontier, initial_node) # https://docs.python.org/2/library/bisect.html
    timestamp1 = datetime.datetime.now()
    
    while True:    
        prev_node = frontier.pop(0)
        ady_list = state_space.getSuccessors(prev_node.state, HT)

        for item in ady_list:
        
            node = Node_Tree(item.key, prev_node.depth+1, item.street_name, prev_node.cost+item.distance, prev_node.state.id_state)
            bisect.insort(frontier, node)

            if len(frontier)%50000 == 0:
                print datetime.datetime.now() - timestamp1
                #timestamp1 = datetime.datetime.now()
                print "Size of frontier: "+ str(len(frontier))
                
