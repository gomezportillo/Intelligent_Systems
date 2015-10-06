class Adyacent_Node:
  key = 0
  distance = 0
  '''estamos trabajando en ello'''
  
class Node:
  latitud = 0
  longitud = 0
  ady_list = []
  
  def __init__(self, lat, lon):
    self.latitud = lat
    self.longitud = lon
    
  def add_node(self, numb):
    self.ady_list.append(numb)
    
nodo = {}

nodo['1234'] = Node(3,4)  

nodo['1234'].add_node(10)
  
print nodo['1234'].ady_list