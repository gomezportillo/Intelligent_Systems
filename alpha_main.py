#! /usr/bin/env python

# import Node

class Adyacent_Node:
    """Class repressenting an adyacent node to another, giving its node and the distance"""
    key = 0
    street_name = ""
    distance = 0

    def __init__(self, k, d):
        self.key = k
        self.distance = d

    def setCity(self, c):
        self.street_name = c
    
    def toString(self):
        return str(self.key) + " " + str(self.street_name) + " " + str(self.distance)


class Node:
    """Class repressenting a node in our graph"""
    key = 0
    latitud = 0
    longitud = 0

    def __init__(self, k, lat, lon):
        self.key = k
        self.latitud = lat
        self.longitud = lon
        self.ady_list = []

    def add_node(self, numb):
        self.ady_list.append(numb)

    def toString(self):
        line = ''
        print self.ady_list[0].toString()
        for item in self.ady_list:
            line += (str(item.toString()) + "\n")
        return "Node #" + str(self.key) + ", latitud: " + str(self.latitud) + ", longitud: " + str(self.longitud) + "\nAdyacent nodes:\n" + line


##### SUPPORT #####

import math


def distance_on_unit_sphere(line1, line2):
    lat1 = line1.latitud
    lat2 = line2.latitud
    long1 = line1.longitud
    long2 = line2.longitud
    degrees_to_radians = math.pi / 180.0
    phi1 = (90.0 - float(lat1)) * degrees_to_radians
    phi2 = (90.0 - float(lat2)) * degrees_to_radians
    theta1 = float(long1) * degrees_to_radians
    theta2 = float(long2) * degrees_to_radians
    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) + math.cos(phi1) * math.cos(phi2))
    arc = math.acos(cos) * 6371000

    return arc


##### MAIN #####

n_nodes = 0
n_conex = 0
HT = {}  # hash table
tmpHT = {} #tmp hash table
we_are_in_ways_section = False
current_city = ""

with open('map.osm') as f:
    lines = f.readlines()

for i in range(0, len(lines) - 1):
    
    if (lines[i].find("<way") != -1): #los nodos tb tienen la etiqueta <tag k="name" v=" para el nombre
        we_are_in_ways_section = True
    
    if (lines[i].find("<node") != -1): #guarda cada nodo en la tabla hash 
        tokenized_line = lines[i].split('"')
        n_nodes += 1
        print "IDNode: " + tokenized_line[1] + " || Latitud:  " + tokenized_line[15] + " || Longitud:  " + \
              tokenized_line[17]

        HT[tokenized_line[1]] = Node(tokenized_line[1], tokenized_line[15], tokenized_line[17])


    if ((lines[i].find("<nd ref=") != -1) and (lines[i - 1].find("<nd ref=") != -1)): #busca nodos adyacentes
        previous_line = lines[i - 1].split('"')
        current_line = lines[i].split('"')
        tmpHT[previous_line[1]] = Adyacent_Node(current_line[1], distance_on_unit_sphere(HT[previous_line[1]], HT[current_line[1]]))
        print previous_line[1] + "-->" + current_line[1]
        n_conex += 1
    
    #the thing is que no sabemos el nodo del que es adyacente un Nodo_Adyacente, solo su id y la distancia
    #entonces hay que guardar el nodo del que viene en algun sitio, y luego recuperarlo
    #guardandolo en tmpHT deberia valer, pero luego no se como recuperarlo 
    #(ese for id_node, ady_node podría tener la magia)    
    if ((we_are_in_ways_section) and (lines[i].find("<tag k=\"name\" v="))): #si estamos en los ways y encuentra una etiqueta nombre
        current_line = lines[i].split('"')
        current_city = current_line[2] #pillamos el nombre de la ciudad de la que hemos guardado los nodos antes
        #print current_city
        
        for id_node, ady_node in tmpHT.iteritems(): #http://stackoverflow.com/questions/8023306/get-key-by-value-in-dictionary
            HT[id_node] = (ady_node.setCity(current_city)) #pero no va
        
        del tmpHT
        

print "Lineas: " + str(i) + " || Nodos: " + str(n_nodes) + " || Conexiones: " + str(n_conex)



# impresion de prueba
# print HT['3753271185'].add_node(Adyacent_Node(2,"mata", 3))
print HT['803292473'].toString()