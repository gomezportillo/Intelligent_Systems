#! /usr/bin/env python

import math
import sys
import bisect
from random import randint
import datetime
from time import time

class State:
    def __init__(self, id_state):
        self.id_state=id_state
        #lista de estados por los que tiene que pasar. el resto va en la clase state space

    def __repr__(self):
        return self.id_state
        
    def getSuccessors(self, HT): #ESTO VA EN LA CLASE ESTATE SPACE
        return HT[str(self.id_state)].ady_list[:]

    def isValid(self): pass
    def isGoal(self): pass       
        

class Node_Tree: #lo que metes en la frontera, primo
    
    def __init__(self, s, d=0, c=0, a=None, p=None):
        self.state = State(s)
        self.depth = d
        self.cost = c
        self.value = randint(0,1000000)
        self.action = a
        self.parent = p

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return self.state.id_state + " " + str(self.value)


########################### HITO 1
class Adyacent_Node:
    """Class repressenting an adyacent node to another, giving its node and the distance"""
   
    def __init__(self, k, street, d):
        self.key = k
        self.street_name = street
        self.distance = d
    
    def __repr__(self):
        return str(self.key)    
       
    def toString(self):
        return str(self.key) + " " + str(self.street_name) + " " + str(self.distance)


class Node:
    """Class repressenting a node in our graph"""
   
    def __init__(self, k, lat, lon):
        self.key = k
        self.latitud = lat
        self.longitud = lon
        self.ady_list = []

    def add_node(self, ady_node):
        self.ady_list.append(ady_node)

    def __repr__(self):
        return str(self.key)

    def toString(self):
        ady_nodes = '\n'
        
        if len(self.ady_list)>0:
            for item in self.ady_list:
                ady_nodes += (str(item.toString()) + "\n")
        else: 
            ady_nodes = "Empty list"
                
        return "Node #" + str(self.key) + ", latitud: " + str(self.latitud) + ", longitud: " + str(self.longitud) + "\nAdyacent nodes: " + ady_nodes


##### SUPPORT #####




def distance_on_unit_sphere(line1, line2):
    """Method for comuting the distance (in meters) from two different geografical coordinates"""
    degrees_to_radians = math.pi / 180.0
    phi1 = (90.0 - float(line1.latitud)) * degrees_to_radians
    phi2 = (90.0 - float(line2.latitud)) * degrees_to_radians
    theta1 = float(line1.longitud) * degrees_to_radians
    theta2 = float(line2.longitud) * degrees_to_radians
    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) + math.cos(phi1) * math.cos(phi2))
    arc = math.acos(cos) * 6371000

    return arc


##### MAIN #####

n_nodes = 0
n_conex = 0
HT = {}  # hash table
tmpList = [] #tmp list to store nores while we get the name of the street
we_are_in_ways_section = False #variable for distinguishing whether we are on the node or in the way "zone"
current_city = ""

if len(sys.argv) != 2:
    print "Error on number of arguments. Use ./"+sys.argv[0].split("/")[-1]+" <node ID>"
    sys.exit(1)    
    
with open('data/map.osm') as f:
    lines = f.readlines()

for i in range(0, len(lines) - 1):
    
    if (lines[i].find("<way") != -1): 
        we_are_in_ways_section = True
    
    if (lines[i].find("<node") != -1):
        tokenized_line = lines[i].split('"')
        n_nodes += 1
        #print "IDNode: " + tokenized_line[1] + " || Latitud:  " + tokenized_line[15] + " || Longitud:  " + \
        tokenized_line[17]

        HT[tokenized_line[1]] = Node(tokenized_line[1], tokenized_line[15], tokenized_line[17])


    if ((lines[i].find("<nd ref=") != -1) and (lines[i - 1].find("<nd ref=") != -1)):
        previous_line = lines[i - 1].split('"')
        current_line = lines[i].split('"')
        tmpList.append((previous_line[1], current_line[1]))
        #print previous_line[1] + "-->" + current_line[1]
        n_conex += 1
    
    
    if ((we_are_in_ways_section) and (lines[i].find("name") != -1)):
        current_line = lines[i].split('"')
        current_city = current_line[3]
        #print current_city
        
        for node, ady_node in tmpList:
                        
            HT[node].add_node(Adyacent_Node(ady_node, current_city, distance_on_unit_sphere(HT[node], HT[ady_node])))
            HT[ady_node].add_node(Adyacent_Node(node, current_city, distance_on_unit_sphere(HT[ady_node], HT[node])))
        
        del tmpList
        tmpList = []
        
    #sys.stdout.write("\r" + str(int(round((float(i)/len(lines))*100))) + "% of the data imported from the .osm file")
    

print "\nLines: " + str(i) + " || Nodes: " + str(n_nodes) + " || Connections: " + str(n_conex) + "\n"


try:
    print HT[sys.argv[1]].toString()
except:
    print "Node "+ sys.argv[1] +" not available on this map" 
    sys.exit(0)

## de aqui pa arriba es lo del hito 1
frontier = []

n_init = Node_Tree(str(sys.argv[1]))
ady = n_init.state.getSuccessors(HT)
bisect.insort(frontier, n_init)
timestamp1 = datetime.datetime.now()
print "Segundos desde los anteriores 10.000 nodos guardados en la frontera"

while(1):    
    prev_node = frontier[0]
    frontier = frontier[1:]

    ady = prev_node.state.getSuccessors(HT)   

    for item in ady:

        node = Node_Tree(item.key, prev_node.depth+1, prev_node.cost+item.distance, item.street_name, prev_node.state.id_state)
        bisect.insort(frontier, node)

        if len(frontier)%10000 == 0: 
            print datetime.datetime.now() - timestamp1
            timestamp1 = datetime.datetime.now()
            print "Size of frontier: "+ str(len(frontier))

#print frontier