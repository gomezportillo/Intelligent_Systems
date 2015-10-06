with open('map.osm') as f:
    lines = f.readlines()
for i in range(0,len(lines)-1):
    if(not lines[i].find("<node") == -1):
        solucion = lines[i].split('"')
        print "IDNodo: " + solucion[1] + " || Latitud:  " + solucion[15] + " || Longitud:  " + solucion[17]
print i
