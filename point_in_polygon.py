#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
point_in_polygon.py : Ensemble de programmes permettant de savoir si un point est contenu dans un polygone.
"""


def crossing_number(polygon, point):
    """Renvoie si le point est dans le polygone.

    Si le point est exactement sur le bord du polygone, cette fonction peut retourner True ou False.

    Parameters:
        polygon (Polygon): //
        point (Point): //

    Returns:
        boolean : True if point in polygon

    """
    absc, ordo = point.coordinates
    points = polygon.points
    # IMPROVE
    x_coord, y_coord = zip(*[point.coordinates for point in points])
    nombre_de_points = len(points)
    nombre_impair_de_noeuds = False

    j = nombre_de_points - 1

    for i in range(nombre_de_points):
        if (y_coord[i] < ordo <= y_coord[j]) or (y_coord[j] < ordo <= y_coord[i]):
            if (x_coord[i] + (ordo - y_coord[i]) / (y_coord[j] - y_coord[i]) * (x_coord[j] - x_coord[i]) < absc):
                nombre_impair_de_noeuds = not nombre_impair_de_noeuds
        j = i

    return nombre_impair_de_noeuds
