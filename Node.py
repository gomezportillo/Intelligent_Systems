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
    self.ady_list = self.ady_list.append(numb)
    
  
x = Node(1,2)

x.add_node(3) #imprime None, que ni significa 'lista vacia'

print x.ady_list   
    