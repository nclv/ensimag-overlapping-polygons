#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
polygones_generator.py : générateur de polygones
"""


from random import seed, random
from geo.polygon import Polygon
from geo.segment import Segment
from geo.point import Point


def random_coordinates_generator(nombre):
    seed(1)
    for _ in range(nombre):
        yield [random(), random()]

def random_points_generator(nombre):
    return map(Point, random_coordinates_generator(NOMBRE))

def main():
    NOMBRE = 100
    segments = [] # contient des listes de deux points
    for new_pointa, new_pointb in zip(random_points_generator(NOMBRE), random_points_generator(NOMBRE)):
        new_segment = [new_pointa, new_pointb]
        for indice in range(len(segments)):
            pointc, pointd = segments[i]
            if Segment(new_segment).intersect(Segment([pointc, pointd])):
                # si intersection, on swap les points
                new_segment = [new_pointa, pointc]
                segments[indice] = [new_pointb, pointd]
            segments.append(new_segment) # on ajoute le segment dans tous les cas

def old_main():
    """main function"""
    nombre_de_points = 100
    coordonnees_des_points = 10
    limit = random.randrange(2, nombre_de_points)

    polygones = [Polygon([Point([1, 2]), Point([2, 4]), Point([-1, 2])])]
    for _ in range(3):
        points = [
            Point(
                [
                    random.randrange(coordonnees_des_points),
                    random.randrange(coordonnees_des_points),
                ]
            )
        ]
        segments = []
        for _ in range(limit):
            # on ajoute le polygone si aucun de ses segments ne s'intersecte avec un segment déjà existant
            point = Point(
                [
                    random.randrange(coordonnees_des_points),
                    random.randrange(coordonnees_des_points),
                ]
            )
            print(points, segments)
            failed = is_failed(polygones, segments, points, point)

            if not failed:
                segment = Segment([points[-1], point])
                if point not in points:
                    points.append(point)
                if segment not in segments:
                    segments.append(segment)

        if len(points) > 2:
            polygon = Polygon(points)
            if polygon.area() != 0:
                polygones.append(polygon)

    with open("generated.poly", "w") as file:
        for indice, polygone in enumerate(polygones):
            for point in polygone.points:
                file.write(f"{indice} {point.coordinates[0]} {point.coordinates[1]}\n")


def is_failed(polygones, segments, points, point):
    for polygon in polygones:
        for segment in list(polygon.segments()) + segments:
            if segment.intersect(Segment([points[-1], point])):
                return True


if __name__ == "__main__":
    main()
    assert (
        Segment([Point([1, 1]), Point([-1, -1])]).intersect(
            Segment([Point([-1, 1]), Point([1, -1])])
        )
        is True
    )
