#! /usr/bin/env python

#import Node

class Adyacent_Node:
	"""Class repressenting an adyacent node to another, giving its node and the distance""" 
	key = 0
	distance = 0
  
	def __init__(self, k, d):
		self.key = k
		self.distance = d
  
	def toString(self):
		return str(self.key) + " " + str(self.distance)

  
class Node:
	"""Class repressenting a node in our graph"""
	key = 0
	latitud = 0
	longitud = 0
	ady_list = []
  
	def __init__(self, k, lat, lon):
		self.key = k
		self.latitud = lat
		self.longitud = lon
    
	def add_node(self, numb):
		self.ady_list.append(numb)

	def toString(self):
		return "Node #" + str(self.key) + ", latitud: " +str(self.latitud) + ", longitud: " + str(self.longitud)

##### SUPPORT #####

import math

def distance_on_unit_sphere(lat1, long1, lat2, long2):

	degrees_to_radians = math.pi/180.0
	phi1 = (90.0 - float(lat1))*degrees_to_radians
	phi2 = (90.0 - float(lat2))*degrees_to_radians
	theta1 = float(long1)*degrees_to_radians
	theta2 = float(long2)*degrees_to_radians
	cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
	arc = math.acos( cos ) * 6371000
	
	return arc

##### MAIN #####

n_nodes = 0
n_conex = 0
HT = {} #hash table

with open('map.osm') as f:
	lines = f.readlines()

for i in range(0,len(lines)-1):
	if (lines[i].find("<node") != -1):
		tokenized_line = lines[i].split('"')
		n_nodes += 1
		print "IDNode: " + tokenized_line[1] + " || Latitud:  " + tokenized_line[15] + " || Longitud:  " + tokenized_line[17]
		
		HT[tokenized_line[1]] = Node(tokenized_line[1], tokenized_line[15], tokenized_line[17])

      
	if ((lines[i].find("<nd ref=") != -1) and (lines[i-1].find("<nd ref=") != -1)):
		previous_line = lines[i-1].split('"')
		current_line = lines[i].split('"')
		print previous_line[1] + "-->" + current_line[1]
		n_conex += 1
      
print "Lineas: " + str(i) + " || Nodos: "+str(n_nodes) + " || Conexiones: " + str(n_conex)

#impresion de prueba
print HT['818781140'].toString()

#solo queda guardar los nodos adyacentes a traves de la hashkey y computar la distancia (lo acabo mañana en un ratillo)
#http://www.johndcook.com/blog/python_longitude_latitude/

#A mi me da: Lineas: 39516 || Nodos: 10702 || Conexiones: 12023

