#! /usr/bin/env python
with open('map.osm') as f:
    lines = f.readlines()
r = 0
s= 0
for i in range(0,len(lines)-1):
    if(not lines[i].find("<node") == -1):
        solucion = lines[i].split('"')
	r = r +1
        print "IDNodo: " + solucion[1] + " || Latitud:  " + solucion[15] + " || Longitud:  " + solucion[17]
    if((not lines[i].find("<nd ref=") == -1) and (not lines[i-1].find("<nd ref=")==-1)):
        solucionmenos1 = lines[i-1].split('"')
        solucion=lines[i].split('"')
        print solucionmenos1[1] + "-->" + solucion[1]
        s = s +1
print "Lineas: " + str(i) + " || Nodos: "+str(r) + " || Conexiones: " + str(s)
