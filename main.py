#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""


import sys
import multiprocessing
from itertools import permutations, combinations
from more_itertools import chunked
from operator import attrgetter

from geo.quadrant import Quadrant
from point_in_polygon import (
    crossing_number,
    crossing_number_v2,
    crossing_number_v3,
    crossing_number_v3_bis,
    crossing_number_v3_sec,
    crossing_number_v4,
    crossing_number_v5,
)
from tycat import read_instance, read_instance_v2, print_polygons


def trouve_inclusions_sorted(polygones, is_point_in_polygon=crossing_number_v3_sec):
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

    # trier les polygones revient à modifier l'ordre défini dans le fichier .poly, le enumerate permet de conserver cet ordre
    results = [-1] * len(polygones)
    sorted_polygones = combinations(sorted(enumerate(polygones), key=lambda couple: couple[1].absolute_area), 2)

    for polygon1, polygon2 in sorted_polygones:
        indice_poly1, indice_poly2 = (
            polygon1[0],
            polygon2[0],
        )
        if is_point_in_polygon(polygon2[1], polygon1[1].points[0]):
            if results[indice_poly1] == -1:
                results[indice_poly1] = indice_poly2
                # print(indice_poly1, indice_poly2)

    return results


def trouve_inclusions(polygones, is_point_in_polygon=crossing_number_v3_sec):
    """Renvoie le vecteur des inclusions

    La ieme case contient l'indice du polygone contenant le ieme polygone (-1 si aucun).

    Parameters:
        polygones (list): Liste de Polygones
        is_point_in_polygon (function): //

    Returns:
        results (list) : Liste des inclusions.

    """
    results = [-1] * len(polygones)
    areas = [polygon.absolute_area for polygon in polygones]

    for polygon1, polygon2 in permutations(enumerate(polygones), 2):
        indice_poly1, indice_poly2 = (
            polygon1[0],
            polygon2[0],
        )
        if areas[indice_poly2] < areas[indice_poly1]:
            continue
        elif is_point_in_polygon(polygon2[1], polygon1[1].points[0]):
            if results[indice_poly1] == -1 or (
                areas[results[indice_poly1]] > areas[indice_poly2]
            ):
                results[indice_poly1] = indice_poly2
                # print(indice_poly1, indice_poly2)

    return results


# aucun improvement
def trouve_inclusions_diviser(polygones):
    results = [-1] * len(polygones)
    rectangle = Quadrant.empty_quadrant(2)
    for polygone in polygones:
        rectangle.update(polygone.bounding_quadrant())
    trouve_inclusions_rec(polygones, results, rectangle)
    return results


def trouve_inclusions_rec(polygones, results, rectangle):
    sous_rectangles = rectangle.divide()
    sous_polygones = []
    for sous_rectangle in sous_rectangles:
        gardes = []
        for polygone in polygones:
            if sous_rectangle.intersect(polygone.bounding_quadrant()):
                gardes.append(polygone)
            sous_polygones.append(polygones)

    taille_initiale = len(polygones)
    for split_polygones, rectangle in zip(sous_polygones, sous_rectangles):
        if len(split_polygones) > taille_initiale / 2 or len(split_polygones) < 10:
            trouve_inclusions(
                split_polygones, results
            )  # modifier trouve_inclusions pour avoir results en paramètres, il faut aussi modifier les tests
        else:
            trouve_inclusions_rec(split_polygones, results, rectangle)


def trouve_inclusions_multiprocessing(split_polygone, results, polygones):
    """Renvoie le vecteur des inclusions

    La ieme case contient l'indice du polygone contenant le ieme polygone (-1 si aucun).

    Parameters:
        polygones (list): Liste de Polygones
        is_point_in_polygon (function): //

    Returns:
        results (list) : Liste des inclusions.

    """
    for (polygon1, polygon2) in split_polygone:
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
                #  print(results[combination_indexes[indice][0]])


def send_theo(polygones):
    import socket
    import time

    TEMPS = 0.2
    port = 34587
    hote = "90.127.103.170"
    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion.connect((hote, port))
    time.sleep(1)
    for poly in polygones:
        k = 0
        while len(poly.points[k:]) > 20:
            connexion.send(str(poly.points[k : k + 20]).encode("utf-8"))
            k += 20
            time.sleep(TEMPS)
        connexion.send(str(poly.points[k:]).encode("utf-8"))
        time.sleep(TEMPS)
        connexion.send(b"next")
        time.sleep(TEMPS)
    connexion.send(b"end")
    connexion.close()


#  aucun gain de temps car les opérations dans la boucle sont déjà peu coûteuses
def main_multiprocessing():
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        n = len(polygones)

        results = multiprocessing.Array("i", [-1] * n)

        # # creating new process
        # p1 = multiprocessing.Process(target=trouve_inclusions_multiprocessing, args=(polygones, results))
        # p1.start()
        # p1.join()

        processes = []
        count = 2  #  multiprocessing.cpu_count()
        split_polygones = chunked(permutations(enumerate(polygones), 2), count)
        for split_polygone in split_polygones:
            _process = multiprocessing.Process(
                target=trouve_inclusions_multiprocessing,
                args=(split_polygone, results, polygones),
            )
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
        #  polygones = read_instance_v2(fichier)
        #  inclusions = trouve_inclusions_diviser(polygones)
        # send_theo(polygones)
        inclusions = trouve_inclusions_sorted(polygones)
        print(inclusions)


if __name__ == "__main__":
    main()
    #  main_multiprocessing()
