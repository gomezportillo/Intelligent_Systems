import bisect

class Node:
    def __init__(self, s, d, c, a, p):
        self.state = s
        self.depth = d
        self.cost = c
        #self.value = randint(0,10000)
        self.action = a
        self.parent = p

    def __init__(self, state):
        self.state = state
        self.depth = 0
        self.cost = 0
        #self.value = randint(0,100)
        self.action = None
        self.parent = None

    def __lt__(self, other):
        return self.state < other.state

    def __repr__(self):
        return "Nodo: " + str(self.state)


lista = []
n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n4 = Node(4)

bisect.insort(lista, n3)
print(lista)
bisect.insort(lista, n2)
bisect.insort(lista, n4)
bisect.insort(lista, n1)
print(lista)
print("Que rotos estais, chavales")



