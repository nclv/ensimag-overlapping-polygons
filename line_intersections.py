
from geo.utils import clip_line_by_polygon
from itertools import combinations
from tycat import read_instance
import sys


# U = [[0,0], [1,0], [1,1], [0,1]]
# line = [[-1, 0.5], [2, 0.5]]
# print(clip_line_by_polygon(line, U))
# 2

def trouve_inclusions_lines(polygones):
    poly_couples = combinations(sorted(enumerate(polygones), key=lambda couple: couple[1].absolute_area), 2)
    # OR presort by first quadrant scalar ?
    quadrants = [polygon.bounding_quadrant() for polygon in polygones]
    # poly_couples_filtered = [couple for couple in poly_couples if quadrants[couple[0][0]].intersect_2(quadrants[couple[1][0]])]
    results = [-1] * len(polygones)

    for polygon1, polygon2 in poly_couples:
        indice_poly1, indice_poly2 = (
            polygon1[0],
            polygon2[0],
        )
        if not quadrants[indice_poly1].intersect_2(quadrants[indice_poly2]):
            continue
        point = polygon2[1].points[0].coordinates
        if clip_line_by_polygon([point, [999.0, point[1]]], [point.coordinates for point in polygon1[1].points]) % 2 == 0:
            if results[indice_poly1] == -1:
                results[indice_poly1] = indice_poly2
                # print(indice_poly1, indice_poly2)

    return results

def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        inclusions = trouve_inclusions_lines(polygones)
        print(inclusions)


if __name__ == "__main__":
    main()
