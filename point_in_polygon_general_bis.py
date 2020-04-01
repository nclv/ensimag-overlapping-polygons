#!/usr/bin/env python3
"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""
import sys
from tycat import read_instance
from pprint import pprint
from collections import defaultdict
from point_in_polygon import crossing_number_v3_sec, winding_number


def trouve_inclusions_bis(polygones):
    nombre_polygones = len(polygones)
    results = [-1] * nombre_polygones

    max_y = lambda poly: max(point.coordinates[1] for point in poly.points)
    min_y = lambda poly: min(point.coordinates[1] for point in poly.points)

    delim = [(min_y(polygon), max_y(polygon)) for polygon in polygones]
    # quadrants = [polygon.bounding_quadrant for polygon in polygones]
    # tri des polygones % valeur de y maximale
    sorted_y = sorted(enumerate(polygones), key=lambda couple: delim[couple[0]][1])
    
    # le prétraitement qui suis permet de grouper les polygones susceptibles de s'intersecter
    done = []
    # y_lines contient les possibles polygones s'intersectant avec la ligne
    y_lines = defaultdict(list)
    for indice_poly_1, polygon1 in sorted_y:
        if indice_poly_1 in done:
            continue
        line_ordo = delim[indice_poly_1][1]  # on prend le max sur y (cohérent avec le tri)
        y_lines[line_ordo] += [(indice_poly_1, polygon1)]
        for indice_poly_2, polygon2 in sorted_y:
            # si le polygone ne peut pas cross la ligne
            if delim[indice_poly_2][1] < line_ordo or line_ordo < delim[indice_poly_2][0]:
                continue
            if indice_poly_2 not in done:
                done.append(indice_poly_2)
            if (indice_poly_2, polygon2) not in y_lines[line_ordo]:
                y_lines[line_ordo].append((indice_poly_2, polygon2))
    
    # pprint(y_lines)

    for _, poly_list in y_lines.items():
        nombre_poly = len(poly_list)
        poly_list.sort(key=lambda couple: couple[1].absolute_area)
        # pprint(sorted_poly_list)
        for i in range(nombre_poly):
            polygon1 = poly_list[i]
            indice_poly1 = polygon1[0]
            if results[indice_poly1] != -1:
                continue
            for j in range(i + 1, nombre_poly):
                polygon2 = poly_list[j]
                indice_poly2 = polygon2[0]
                # faire les courbes avec et sans pour les fichiers du type 512/256...
                # très peu efficace sans
                # if not quadrants[indice_poly1].intersect_2(quadrants[indice_poly2]):
                #     continue
                if crossing_number_v3_sec(polygon2[1], polygon1[1].points[0]):
                    results[indice_poly1] = indice_poly2
                    # print(indice_poly1, indice_poly2)
                    break
    
    return results



def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        inclusion = trouve_inclusions_bis(polygones)
        print(inclusion)

if __name__ == "__main__":
    main()
