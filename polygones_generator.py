#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
polygones_generator.py : générateur de polygones
"""


import random
from geo.polygon import Polygon
from geo.segment import Segment
from geo.point import Point


def main():
    """main function"""
    nombre_de_points = 10
    coordonnees_des_points = 10
    limit = random.randrange(2, nombre_de_points)

    polygones = [Polygon([Point([1, 2]), Point([2, 4]), Point([-1, 2])])]
    for _ in range(1000):
        points = [Point([random.randrange(coordonnees_des_points), random.randrange(coordonnees_des_points)])]
        segments = []
        for indice in range(limit):
            # on ajoute le polygone si aucun de ses segments ne s'intersecte avec un segment déjà existant
            point = Point([random.randrange(coordonnees_des_points), random.randrange(coordonnees_des_points)])
            if indice == limit - 1:
                point = points[0]
            # print(points)
            failed = []
            for polygon in polygones:
                for segment in polygon.segments():
                    segments.append(Segment([points[-1], point]))
                    for other_segment in segments:
                        if segment.intersect(other_segment):
                            failed.append(True)
                            segments.pop()
            if not failed:
                points.append(point)


        if len(points) > 2:
            polygon = Polygon(points)
            if polygon.area() != 0:
                polygones.append(polygon)

    with open("generated.poly", 'w') as file:
        polygones.pop()
        for indice, polygone in enumerate(polygones):
            for point in polygone.points:
                file.write(f"{indice} {point.coordinates[0]} {point.coordinates[1]}\n")

if __name__=="__main__":
    main()
    assert Segment([Point([1, 1]), Point([-1, -1])]).intersect(Segment([Point([-1, 1]), Point([1, -1])])) is True
