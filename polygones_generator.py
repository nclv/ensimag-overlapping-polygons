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
    nombre_de_points = 100
    coordonnees_des_points = 10
    limit = random.randrange(2, nombre_de_points)

    polygones = [Polygon([Point([1, 2]), Point([2, 4]), Point([-1, 2])])]
    for _ in range(3):
        points = [Point([random.randrange(coordonnees_des_points), random.randrange(coordonnees_des_points)])]
        segments = []
        for _ in range(limit):
            # on ajoute le polygone si aucun de ses segments ne s'intersecte avec un segment déjà existant
            point = Point([random.randrange(coordonnees_des_points), random.randrange(coordonnees_des_points)])
            print(points, segments)
            failed = is_failed(polygones, segments, points, point)

            if not failed:
                segment = Segment([points[-1], point])
                if point not in points: points.append(point)
                if segment not in segments: segments.append(segment)

        if len(points) > 2:
            polygon = Polygon(points)
            if polygon.area() != 0:
                polygones.append(polygon)

    with open("generated.poly", 'w') as file:
        for indice, polygone in enumerate(polygones):
            for point in polygone.points:
                file.write(f"{indice} {point.coordinates[0]} {point.coordinates[1]}\n")

def is_failed(polygones, segments, points, point):
    for polygon in polygones:
        for segment in list(polygon.segments()) + segments:
            if segment.intersect(Segment([points[-1], point])):
                return True

if __name__=="__main__":
    main()
    assert Segment([Point([1, 1]), Point([-1, -1])]).intersect(Segment([Point([-1, 1]), Point([1, -1])])) is True
