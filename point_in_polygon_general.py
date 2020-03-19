import sys
from pprint import pprint
from tycat import read_instance
from itertools import groupby
from collections import defaultdict


def crossing_number_global(polygon, point):
    """Renvoie si le point est dans le polygone.

    Si le point est exactement sur le bord du polygone, cette fonction peut retourner True ou False.

    Parameters:
        polygon (Polygon): //
        point (Point): //

    Returns:
        boolean : True if point in polygon

    """

    absc, ordo = point
    indice = 0
    nombre_de_points = len(polygon)
    d = defaultdict(int)

    while indice < nombre_de_points:
        sommet0 = polygon[indice][1][0]
        sommet1 = polygon[indice][1][1]
        if (sommet0[1] >= ordo > sommet1[1] or sommet1[1] >= ordo > sommet0[1]) and (sommet1[0] <= absc or sommet0[0] <= absc):
            # xor plus rapide que ^=
            if sommet1[0] + (ordo - sommet1[1]) / (sommet0[1] - sommet1[1]) * (sommet0[0] - sommet1[0]) < absc:
                d[polygon[indice][0]] += 1
        indice += 1

    return d


def trouve_inclusions_general(polygones):

    # get all segments
    segments = []
    for indice, polygon in enumerate(polygones):
        for segment in polygon.segments():
            segment_coord = []
            for point in segment.endpoints:
                coord = point.coordinates
                segment_coord.append(coord)
            segments.append((indice, sorted(segment_coord, key=lambda p: p[1])))
    segments.sort(key=lambda couple: couple[1][0][1]) # tri selon les y croissants
    # on veut une liste de y
    # pour chaque y on veut un xmin
    points = [(min(groupe, key=lambda couple: couple[1][0][0])[1][0][0], k) for k, groupe in groupby(segments, lambda couple: couple[1][0][1])]
    pprint(points)
    # on va boucler sur cette liste précédemment affichée et appliquer crossing_number_global
    for point in points:
        d = crossing_number_global(segments, point)
        print(d)

    pprint(segments)




def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        inclusions = trouve_inclusions_general(polygones)
        print(inclusions)


if __name__ == "__main__":
    main()
