#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import combinations, permutations


def trouve_inclusions_sorted1(polygones, pip_function):
    poly_couples = sorted(
        enumerate(polygones), key=lambda couple: couple[1].absolute_area
    )
    quadrants = [polygon.bounding_quadrant for polygon in polygones]
    nombre_polygones = len(polygones)
    results = [-1] * nombre_polygones
    if nombre_polygones < 2:
        return [-1]

    for i in range(nombre_polygones):
        polygon1 = poly_couples[i]
        indice_poly1 = polygon1[0]
        for j in range(i + 1, nombre_polygones):
            polygon2 = poly_couples[j]
            indice_poly2 = polygon2[0]
            if not quadrants[indice_poly1].intersect_2(quadrants[indice_poly2]):
                continue
            if pip_function(polygon2[1], min(polygon1[1].points)):
                results[indice_poly1] = indice_poly2
                # print(indice_poly1, indice_poly2)
                break

    return results


def trouve_inclusions_sorted2(polygones, pip_function):
    poly_couples = combinations(
        sorted(enumerate(polygones), key=lambda couple: couple[1].absolute_area), 2
    )
    quadrants = [polygon.bounding_quadrant for polygon in polygones]
    nombre_polygones = len(polygones)
    results = [-1] * nombre_polygones
    if nombre_polygones < 2:
        return [-1]

    for polygon1, polygon2 in poly_couples:
        indice_poly1, indice_poly2 = (
            polygon1[0],
            polygon2[0],
        )
        if results[indice_poly1] != -1:
            continue
        if not quadrants[indice_poly1].intersect_2(quadrants[indice_poly2]):
            continue
        if pip_function(polygon2[1], polygon1[1].points[0]):
            results[indice_poly1] = indice_poly2
            # print(indice_poly1, indice_poly2)

    return results


def trouve_inclusions(polygones, pip_function):
    results = [-1] * len(polygones)
    areas = [polygon.absolute_area for polygon in polygones]

    for polygon1, polygon2 in permutations(enumerate(polygones), 2):
        indice_poly1, indice_poly2 = (
            polygon1[0],
            polygon2[0],
        )
        if areas[indice_poly2] < areas[indice_poly1]:
            continue
        elif pip_function(polygon2[1], polygon1[1].points[0]):
            if results[indice_poly1] == -1 or (
                areas[results[indice_poly1]] > areas[indice_poly2]
            ):
                results[indice_poly1] = indice_poly2
                # print(indice_poly1, indice_poly2)

    return results
