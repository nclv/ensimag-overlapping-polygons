#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
algos_trouve_inclusions.py : Ensemble des programmes de recherche d'inclusions entre polygones.
Seul l'algorithme trouve_inclusions_groupy2 ne prend pas de pip_function en paramètre.
Il dépend de la fonction crossing_number_global présente dans ce fichier.
"""


from itertools import combinations, permutations
from collections import defaultdict


def trouve_inclusions_sorted1(polygones, pip_function):
    poly_couples = sorted(
        enumerate(polygones), key=lambda couple: couple[1].absolute_area
    )
    quadrants = [polygon.bounding_quadrant for polygon in polygones]
    nombre_polygones = len(polygones)
    results = [-1] * nombre_polygones
    if nombre_polygones < 2:
        return [-1]

    for i in range(nombre_polygones - 1):
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


def trouve_inclusions_groupy1(polygones, pip_function):
    nombre_polygones = len(polygones)
    results = [-1] * nombre_polygones

    max_y = lambda poly: max(point.coordinates[1] for point in poly.points)
    min_y = lambda poly: min(point.coordinates[1] for point in poly.points)

    delim = [(min_y(polygon), max_y(polygon)) for polygon in polygones]
    quadrants = [polygon.bounding_quadrant for polygon in polygones]
    # tri des polygones % valeur de y maximale
    sorted_y = sorted(enumerate(polygones), key=lambda couple: delim[couple[0]][1])

    # le prétraitement qui suit permet de grouper les polygones susceptibles de s'intersecter
    done = []
    nombre_poly_done = 0
    # y_lines contient les possibles polygones s'intersectant avec la ligne
    y_lines = defaultdict(list)
    for indice_poly_1, _ in sorted_y:
        if nombre_poly_done == nombre_polygones:
            break
        if indice_poly_1 in done:
            continue
        line_ordo = delim[indice_poly_1][1]  
        # on prend le max sur y du polygone (cohérent avec le tri)
        for indice_poly_2, polygon2 in sorted_y:
            # la ligne ne traverse pas le polygone
            if (
                delim[indice_poly_2][1] < line_ordo
                or line_ordo < delim[indice_poly_2][0]
            ):
                continue
            # la ligne traverse le polygone et c'est la première fois qu'on voit le polygone
            if indice_poly_2 not in done:
                done.append(indice_poly_2)
                nombre_poly_done += 1
            y_lines[line_ordo].append((indice_poly_2, polygon2))

    # pprint(y_lines)

    # on évite de reboucler sur des polygones déjà traités
    seen = []
    for _, poly_list in y_lines.items():
        nombre_poly = len(poly_list)
        poly_list.sort(key=lambda couple: couple[1].absolute_area)
        # pprint(poly_list)
        for i in range(nombre_poly - 1):
            polygon1 = poly_list[i]
            indice_poly1 = polygon1[0]
            if indice_poly1 in seen:
                break
            seen.append(indice_poly1)
            # print(seen)
            # print("1", indice_poly1)
            for j in range(i + 1, nombre_poly):
                polygon2 = poly_list[j]
                indice_poly2 = polygon2[0]
                # print("2", indice_poly2)
                # faire les courbes avec et sans pour les fichiers du type 512/256...
                # très peu efficace sans
                if not quadrants[indice_poly1].intersect_2(quadrants[indice_poly2]):
                    continue
                # ici le min % aux abscisses
                if pip_function(polygon2[1], min(polygon1[1].points)):
                    results[indice_poly1] = indice_poly2
                    # print(indice_poly1, indice_poly2)
                    break
    return results


def crossing_number_global(segments, ordo, mapping, delim):
    """Renvoie si le point est dans le polygone.

    Si le point est exactement sur le bord du polygone, cette fonction peut retourner True ou False.

    Parameters:
        polygon (Polygon): //
        point (Point): //

    Returns:
        boolean : True if point in polygon

    """
    interup = []
    interdown = []

    for poly_indice, points in segments:
        counter = 0
        nombre_de_points = len(points)
        sommet0 = points[-1]
        x0, y0 = sommet0.coordinates
        while counter < nombre_de_points:
            sommet1 = points[counter]
            x1, y1 = sommet1.coordinates
            if y0 >= ordo > y1 or y1 >= ordo > y0:
                inter = x1 + (ordo - y1) / (y0 - y1) * (x0 - x1)
                interup.append((poly_indice, inter))
            if y0 > ordo >= y1 or y1 > ordo >= y0:
                inter = x1 + (ordo - y1) / (y0 - y1) * (x0 - x1)
                interdown.append((poly_indice, inter))
            y0, x0 = y1, x1
            sommet0 = sommet1
            counter += 1

    return (
        sorted(interup, key=lambda couple: mapping[couple[0]]),
        sorted(interdown, key=lambda couple: mapping[couple[0]]),
    )  # nécessaire ici de trier


def compute_intersections(liste_intersections, results, liste_poly_done):
    nombre_intersections = len(liste_intersections)

    indices_lst = []
    value = liste_intersections[0][0]
    for i in range(nombre_intersections):
        new_value = liste_intersections[i][0]
        if new_value != value:
            indices_lst.append(i - 1)
            value = new_value
    # print(indices_lst)

    for i in indices_lst:
        compteur = defaultdict(int)
        inter1 = liste_intersections[i]
        indice_poly1 = inter1[0]
        if indice_poly1 in liste_poly_done:
            continue
        for j in range(i + 1, nombre_intersections):
            inter2 = liste_intersections[j]
            indice_poly2 = inter2[0]
            if inter2[1] > inter1[1]:
                compteur[indice_poly2] += 1
        # print(compteur)
        liste_poly_done.append(indice_poly1)
        # print(liste_poly_done)
        for indice, intersection_number in compteur.items():
            if intersection_number % 2 == 1:
                # print(f"Polygone {indice_poly1} in {indice}")
                # lsq ligne indice, il ne faut pas prendre les segments de poly_number
                results[indice_poly1] = indice
                break
    return results, liste_poly_done


def trouve_inclusions_groupy2(polygones):
    nombre_polygones = len(polygones)
    results = [-1] * nombre_polygones

    sorted_polygones = sorted(
        enumerate(polygones), key=lambda couple: couple[1].absolute_area
    )
    mapping = {
        poly_number: indice for indice, (poly_number, _) in enumerate(sorted_polygones)
    }

    max_y = lambda poly: max(point.coordinates[1] for point in poly.points)
    min_y = lambda poly: min(point.coordinates[1] for point in poly.points)
    delim = [(min_y(polygon), max_y(polygon)) for polygon in polygones]

    # le prétraitement qui suis permet de grouper les polygones susceptibles de s'intersecter
    # tri des polygones % valeur de y maximale
    sorted_y = sorted(enumerate(polygones), key=lambda couple: delim[couple[0]][1])
    done = []
    nombre_poly_done = 0
    # y_lines contient les possibles polygones s'intersectant avec la ligne
    y_points_needed = defaultdict(list)
    for indice_poly_1, _ in sorted_y:
        if nombre_poly_done == nombre_polygones:
            break
        if indice_poly_1 in done:
            continue
        line_ordo = delim[indice_poly_1][1]  
        # on prend le max sur y (cohérent avec le tri)
        for indice_poly_2, polygon2 in sorted_y:
            # si le polygone ne peut pas cross la ligne
            if (
                delim[indice_poly_2][1] < line_ordo
                or line_ordo < delim[indice_poly_2][0]
            ):
                continue
            if indice_poly_2 not in done:
                done.append(indice_poly_2)
                nombre_poly_done += 1
            y_points_needed[line_ordo].append((indice_poly_2, polygon2.points))

    # pprint(y_points_needed)

    liste_poly_done = []
    # cela doit rester un set, mais on peut plus facilement repérer les erreurs avec une liste
    liste_poly_done.append(sorted_polygones[-1][0])
    for ligne, value in y_points_needed.items():
        # on ne passe ici qu'une fois (y = 1) pour les fichiers overlapping_square)
        interup, interdown = crossing_number_global(value, ligne, mapping, delim)
        # print("intersections")
        # pprint(interup)
        # pprint(interdown)

        if interup:
            results, liste_poly_done = compute_intersections(
                interup, results, liste_poly_done
            )
        # gain sans interdown
        if interdown and interdown != interup:
            results, liste_poly_done = compute_intersections(
                interdown, results, liste_poly_done
            )

    return results

