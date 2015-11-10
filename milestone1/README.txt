#######################################################
###################  DOCUMENTATION  ###################
#######################################################

Python program to generate a graph into a hash table from a .osm file and work within it

####### AUTHORS

Juan Garrido Arcos 
    - juan.garrido3@alu.uclm.es
    
Pedro-Manuel Gómez-Portillo López 
    - pedromanuel.gomezportillo@alu.uclm.es

####### MANUAL

Should you want to execute this program, a Makefile has been writen for 
this purpose.

Being at the root directory of this project, execute $make:
    - build: to download the .osm file of the map of Ciudad Real    
    - test: for executing the program with a right node
    - test_error: for executing the program with an invalid node
    - clean: for removing the map you have previously downloaded

    
Should you want to look for a specific node on this program, being at
the root directory, execute:

    $./src/main.py <node id>

being <node id> the id of the node you want to look for
