#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
polygones_generator.py : générateur de polygones
"""


import random
from geo.polygon import Polygon
from geo.point import Point


def main():
    """main function"""
    nombre_de_points = 100
    coordonnees_des_points = 100

    polygones = []
    for _ in range(100):
        points = []
        for _ in range(random.randrange(nombre_de_points)):
            coordinates = [random.randrange(coordonnees_des_points), random.randrange(coordonnees_des_points)]
            points.append(Point(coordinates))
        polygon = Polygon(points)

        # on ajoute le polygone si aucun de ses segments ne s'intersecte avec un segment déjà existant
        failed = any(polygon.intersect(other_polygon) for other_polygon in polygones)

        if not failed:
            polygones.append(polygon)

if __name__=="__main__":
    main()
