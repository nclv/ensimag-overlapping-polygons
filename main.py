#!/usr/bin/env python3
"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""
import sys
import itertools
import point_in_polygon
from tycat import read_instance, print_polygons


def trouve_inclusions(polygones):
    """Renvoie le vecteur des inclusions

    La ieme case contient l'indice du polygone contenant le ieme polygone (-1 si aucun).

    Parameters:
        polygones (list): Liste de Polygones

    Returns:
        results (list) : Liste des inclusions.

    """

    # IMPROVE
    # list(combinations(range(len(polygones)), 2)) to get indexes
    # list(combinations(enumerate(polygones), 2)) to get everything, or
    # list((i,j) for ((i,_),(j,_)) in itertools.combinations(enumerate(a), 2)) to get indexes

    n = len(polygones)
    results = [-1] * n
    combination_indexes = list(itertools.combinations(range(n), 2))
    # print(results, combination_indexes)

    for indice, (polygon1, polygon2) in enumerate(itertools.combinations(polygones, 2)):
        point = polygon1.points[0]
        is_point_in_polygon = point_in_polygon.crossing_number(polygon2, point)
        # print(is_point_in_polygon)
        if is_point_in_polygon:
            results[combination_indexes[indice][0]] = combination_indexes[indice][1]
        else:
            results[combination_indexes[indice][1]] = combination_indexes[indice][0]

    return results


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        # print_polygons(polygones)
        inclusions = trouve_inclusions(polygones)
        print(inclusions)


if __name__ == "__main__":
    main()
