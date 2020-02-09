#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""


import sys
import itertools
import multiprocessing
import numpy as np
from point_in_polygon import crossing_number, crossing_number_v2, crossing_number_v3, crossing_number_v4, crossing_number_v5
from tycat import read_instance, print_polygons


def trouve_inclusions_sorted(
    polygones, is_point_in_polygon=crossing_number
):
    """Renvoie le vecteur des inclusions

    La ieme case contient l'indice du polygone contenant le ieme polygone (-1 si aucun).
    Le programme fonctionne si les polygones sont triés du plus grand au plus petit dans le fichier .poly

    Parameters:
        polygones (list): Liste de Polygones
        is_point_in_polygon (function): //

    Returns:
        results (list) : Liste des inclusions.

    """

    # IMPROVE
    # list(permutations(range(len(polygones)), 2)) to get indexes
    # list(permutations(enumerate(polygones), 2)) to get everything, or
    # list((i,j) for ((i,_),(j,_)) in itertools.permutations(enumerate(polygones), 2)) to get indexes

    # IMPORTANT : non fonctionnel sur generated_from_examples_4.poly
    # sans enumerate l'ordre n'est pas respecté
    sorted_polygones = sorted(
        enumerate(polygones), key=lambda couple: couple[1].absolute_area, reverse=True
    )
    # trier les polygones revient à modifier l'ordre défini dans le fichier .poly, le enumerate permet de conserver cet ordre
    n = len(polygones)
    results = [-1] * n
    # combination_indexes = list(itertools.permutations(range(n), 2))
    # permutations('ABCD', 2) => AB AC AD BA BC BD CA CB CD DA DB DC
    combination_indexes = []
    append = combination_indexes.append
    for indice, (polygon1, polygon2) in enumerate(
        itertools.permutations(sorted_polygones, 2)
    ):
        append((polygon1[0], polygon2[0]))
        if is_point_in_polygon(polygon2[1], polygon1[1].points[0]):
            results[combination_indexes[indice][0]] = combination_indexes[indice][1]
            # print(results[combination_indexes[indice][0]])

    return results


def trouve_inclusions(polygones, is_point_in_polygon=crossing_number_v4):
    """Renvoie le vecteur des inclusions

    La ieme case contient l'indice du polygone contenant le ieme polygone (-1 si aucun).

    Parameters:
        polygones (list): Liste de Polygones
        is_point_in_polygon (function): //

    Returns:
        results (list) : Liste des inclusions.

    """
    n = len(polygones)
    results = [-1] * n

    for indice, (polygon1, polygon2) in enumerate(
        itertools.permutations(enumerate(polygones), 2)
    ):
        if is_point_in_polygon(polygon2[1], polygon1[1].points[0]):
            indice_poly1, indice_poly2 = (
                polygon1[0],
                polygon2[0],
            )
            if results[indice_poly1] == -1 or (
                polygones[results[indice_poly1]].absolute_area
                > polygones[indice_poly2].absolute_area
            ):
                results[indice_poly1] = indice_poly2

    return results




def trouve_inclusions_multiprocessing(split_polygone, results, polygones):
    """Renvoie le vecteur des inclusions

    La ieme case contient l'indice du polygone contenant le ieme polygone (-1 si aucun).

    Parameters:
        polygones (list): Liste de Polygones
        is_point_in_polygon (function): //

    Returns:
        results (list) : Liste des inclusions.

    """
    for indice, (polygon1, polygon2) in enumerate(split_polygone):
        if crossing_number_v5(polygon2[1], polygon1[1].points[0]):
            indice_poly1, indice_poly2 = (
                polygon1[0],
                polygon2[0],
            )
            if results[indice_poly1] == -1 or (
                polygones[results[indice_poly1]].absolute_area
                > polygones[indice_poly2].absolute_area
            ):
                results[indice_poly1] = indice_poly2
                # print(results[combination_indexes[indice][0]])


# aucun gain de temps car les opérations dans la boucle sont déjà peu coûteuses
def main_multiprocessing():
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        n = len(polygones)

        results = multiprocessing.Array('i', [-1] * n)

        # # creating new process
        # p1 = multiprocessing.Process(target=trouve_inclusions_multiprocessing, args=(polygones, results))
        # p1.start()
        # p1.join()

        processes = []
        count = 2 # multiprocessing.cpu_count()
        split_polygones = np.array_split(list(itertools.permutations(enumerate(polygones), 2)), count)

        for split_polygone in split_polygones:
            _process = multiprocessing.Process(target=trouve_inclusions_multiprocessing, args=(split_polygone, results, polygones))
            processes.append(_process)
            _process.start()

        for _process in processes:
            _process.join()

        print(results[:])


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        inclusions = trouve_inclusions(polygones)
        print(inclusions)


if __name__ == "__main__":
    main()
    # main_multiprocessing()
