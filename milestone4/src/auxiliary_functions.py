#!/usr/bin/env python

import math, sys

class Searching_Strategies:
    BFS = 0
    DFS = 1
    DLS = 2
    IDS = 3
    UC = 4
    AStar = 5


def distance_on_unit_sphere(coord1, coord2):
    """ Method for comuting the distance, in meters, from two different geografical coordinates
    """
    degrees_to_radians = math.pi / 180.0
    phi1 = (90.0 - float(coord1.latitud)) * degrees_to_radians
    phi2 = (90.0 - float(coord2.latitud)) * degrees_to_radians
    theta1 = float(coord1.longitud) * degrees_to_radians
    theta2 = float(coord2.longitud) * degrees_to_radians
    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) + math.cos(phi1) * math.cos(phi2))
    
    return math.acos(cos) * 6371000

