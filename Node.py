class Adyacent_Node:
  key = 0
  distance = 0
  
  def __init__(self, k, d):
    self.key = k
    self.distance = d
  
  def toString(self):
    return str(self.key) + " " + str(self.distance)

  
class Node:
  
  latitud = 0
  longitud = 0
  ady_list = []
  
  def __init__(self, lat, lon):
    self.latitud = lat
    self.longitud = lon
    
  def add_node(self, numb):
    self.ady_list.append(numb)

  def toString(self):
    return str(self.latitud) + " " + str(self.longitud)

    
nodo = {}

nodo['1234'] = Node(3,4)  

nodo['1234'].add_node(Adyacent_Node(2,3))
  
print nodo['1234'].ady_list #imprime el puntero a memoria, no los objetos 
print nodo['1234'].toString()