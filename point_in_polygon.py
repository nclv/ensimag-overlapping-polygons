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
        if y_coord[i] < ordo <= y_coord[j] or y_coord[j] < ordo <= y_coord[i]:
            if x_coord[i] + (ordo - y_coord[i]) / (y_coord[j] - y_coord[i]) * (x_coord[j] - x_coord[i]) < absc:
                nombre_impair_de_noeuds = not nombre_impair_de_noeuds
        j = i

    return nombre_impair_de_noeuds

# gain de 4sec sur crossing_number pour generated_from_examples_6.poly
# eliminates calculations on sides that are entirely to the right of the test point
def crossing_number_v2(polygon, point):
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
        if y_coord[i] < ordo <= y_coord[j] or y_coord[j] < ordo <= y_coord[i] and (x_coord[i] <= absc or x_coord[j] <= absc):
            if x_coord[i] + (ordo - y_coord[i]) / (y_coord[j] - y_coord[i]) * (x_coord[j] - x_coord[i]) < absc:
                nombre_impair_de_noeuds = not nombre_impair_de_noeuds
        j = i

    return nombre_impair_de_noeuds


# gain de 2sec sur crossing_number_v2 pour generated_from_examples_6.poly
def crossing_number_v3(polygon, point):
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
        if y_coord[i] < ordo <= y_coord[j] or y_coord[j] < ordo <= y_coord[i] and (x_coord[i] <= absc or x_coord[j] <= absc):
            # xor plus rapide que ^=
            nombre_impair_de_noeuds = (not nombre_impair_de_noeuds) != (
                not x_coord[i] + (ordo - y_coord[i]) / (y_coord[j] - y_coord[i]) * (x_coord[j] - x_coord[i]) < absc)
        j = i

    return nombre_impair_de_noeuds


def crossing_number_v3_bis(polygon, point):
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
    indice = 0
    sommet0 = points[-1].coordinates
    sommet1 = points[indice].coordinates
    y0_test = sommet1[1] < ordo <= sommet0[1]
    nombre_impair_de_noeuds = False

    for _ in range(len(points) - 1):
        y1_test = sommet0[1] < ordo <= sommet1[1]
        if y0_test or y1_test and (sommet1[0] <= absc or sommet0[0] <= absc):
            # xor plus rapide que ^=
            nombre_impair_de_noeuds = (not nombre_impair_de_noeuds) != (
                not sommet1[0] + (ordo - sommet1[1]) / (sommet0[1] - sommet1[1]) * (sommet0[0] - sommet1[0]) < absc)
        y0_test = y1_test
        sommet0 = sommet1
        indice += 1
        sommet1 = points[indice].coordinates

    return nombre_impair_de_noeuds


# plus rapide de 3sec par rapport à v5
def crossing_number_v4(polygon, point):
    absc, ordo = point.coordinates
    points = polygon.points
    sommet0 = points[-1].coordinates
    y0_test = sommet0[1] >= ordo
    indice = 0
    sommet1 = points[indice].coordinates
    nombre_impair_de_noeuds = False

    for _ in range(len(points) - 1):
        y1_test = sommet1[1] >= ordo
        if y0_test != y1_test:
            x0_test = sommet0[0] >= absc
            if x0_test != (sommet1[0] >= absc):
                nombre_impair_de_noeuds = (
                    not nombre_impair_de_noeuds) != (not x0_test)
            else:
                nombre_impair_de_noeuds = (not nombre_impair_de_noeuds) != (
                    not sommet1[0] - (sommet1[1] - ordo) * (sommet0[0] - sommet1[0]) / (sommet0[1]-sommet1[1]) >= absc)
        y0_test = y1_test
        sommet0 = sommet1
        indice += 1
        sommet1 = points[indice].coordinates

    return nombre_impair_de_noeuds


def crossing_number_v5(polygon, point):
    absc, ordo = point.coordinates
    points = polygon.points
    sommet0 = points[-1].coordinates
    y0_test = sommet0[1] >= ordo
    indice = 0
    sommet1 = points[indice].coordinates
    nombre_impair_de_noeuds = False

    for _ in range(len(points) - 1):
        y1_test = sommet1[1] >= ordo
        if y0_test != y1_test:
            nombre_impair_de_noeuds = (not nombre_impair_de_noeuds) != (not ((sommet1[1] - ordo) * (sommet0[0] - sommet1[0]) >= (sommet1[0] - absc) * (sommet0[1] - sommet1[1])) == y1_test)
        y0_test = y1_test
        sommet0 = sommet1
        indice += 1
        sommet1 = points[indice].coordinates

    return nombre_impair_de_noeuds
