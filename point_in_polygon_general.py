import sys
from pprint import pprint
from tycat import read_instance
from itertools import groupby, combinations
from collections import Counter


def crossing_number_global(polygon, ligne):
    """Renvoie si le point est dans le polygone.

    Si le point est exactement sur le bord du polygone, cette fonction peut retourner True ou False.

    Parameters:
        polygon (Polygon): //
        point (Point): //

    Returns:
        boolean : True if point in polygon

    """
    ordo = ligne
    indice = 0
    nombre_de_points = len(polygon)
    d = []
    poly_rencontree = set()

    while indice < nombre_de_points:
        segment = polygon[indice]
        sommet0 = segment[1][0]
        sommet1 = segment[1][1]
        if (sommet0[1] >= ordo > sommet1[1] or sommet1[1] >= ordo > sommet0[1]): # and (sommet1[0] <= absc or sommet0[0] <= absc):
            # le membre de gauche est la coordonnée de l'intersection du segment
            # avec la droite y
            inter = sommet1[0] + (ordo - sommet1[1]) / (sommet0[1] - sommet1[1]) * (sommet0[0] - sommet1[0])
            # if inter < absc:
            #     # print("intersection")
            # poly = ligne[0]
            segment_numero_poly = segment[0]
            # if poly != segment_numero_poly: # on ne compte pas les intersections avec d'autres segments du même polygone
                #d.append([poly, segment_numero_poly, inter])
            d.append((segment_numero_poly, inter))
            poly_rencontree.add(segment_numero_poly)
        indice += 1

    return sorted(d, key=lambda couple: couple[1]), poly_rencontree


def trouve_inclusions_general(polygones):
    """problème avec 1
    Intersections de segments avec 2 sur y = 464.0
    [(6, 152.4122965641953),
     (0, 222.98805970149255),
     (5, 435.40579710144925),
     (5, 532.0769230769231),
     (0, 648.1726618705036),
     (7, 730.4929006085192),
     (7, 854.7898832684825),
     (1, 911.6978417266187)]
    Polygone 2 in 6 # okay
    Polygone 2 in 1 # okay

    3 bleufonce/vert, 6 bleuclair/bleu, 1 vert/rouge

    """

    ### TEST des QUADRANTS ###
    quadrants = [polygon.bounding_quadrant() for polygon in polygones]
    areas = [polygon.absolute_area for polygon in polygones]
    # on ne test pas les autres polygones
    poly_couples, _ = zip(*sorted(enumerate(polygones), key=lambda couple: couple[1].absolute_area))
    number_couples = set(combinations(poly_couples, 2)) # attention, combinations renvoie un générateur

    # get all segments
    segments = []
    liste_x = []
    set_y = set()
    set_poly = set(range(len(polygones)))
    # sorted(enumerate(polygones), key=lambda couple: couple[1].absolute_area) ?
    for indice, polygon in enumerate(polygones):
        for segment in polygon.segments():
            segment_coord = []
            for point in segment.endpoints:
                coord = point.coordinates
                segment_coord.append(coord)
                set_y.add(coord[1])
                # if indice in set_poly:
                #     set_y.add(coord[1])
                #     set_poly.remove(indice)
            segments.append((indice, sorted(segment_coord, key=lambda p: p[1])))
        liste_x.append((indice, polygon.points[0].coordinates[0]))
    segments.sort(key=lambda couple: couple[1][0][1]) # tri selon les y croissants
    # print(liste_x)
    # print(set_y)
    # pprint(segments)

    results = [-1] * len(polygones)
    for ligne in set_y:
        print(f"y = {ligne}")
        liste_intersections, poly_rencontree = crossing_number_global(segments, ligne)
        # pprint(liste_intersections)
        # pprint(poly_rencontree)
        for poly_number, absc in filter(lambda couple: couple[0] in poly_rencontree, liste_x):
            # print(absc)
            less_inter = list(filter(lambda couple: couple[1] < absc and couple[0] != poly_number, liste_intersections))
            print(f"Intersections de segments avec {poly_number} sur y = {ligne}")
            pprint(less_inter)
            count = Counter(couple[0] for couple in less_inter)
            # filtered_count = {poly: True if count[poly] % 2 == 1 else False for poly in count}
            # print(filtered_count)
            for indice, intersection_number in count.items():
                if poly_number == indice:
                    continue
                if (poly_number, indice) not in number_couples:
                    continue
                ### TEST des QUADRANTS ###
                if not quadrants[indice].intersect_2(quadrants[poly_number]):
                    continue

                if intersection_number % 2 == 1:
                    print(f"Polygone {poly_number} in {indice}")
                    # on a tracé une droite horizontale partant d'un point de poly_number
                    # on a trouvé un nombre impair d'intersections avec des segments de indice
                    if results[poly_number] != -1:
                        # print(areas[results[poly_number]], areas[indice])
                        if areas[results[poly_number]] > areas[indice]:
                            results[poly_number] = indice
                    else:
                        results[poly_number] = indice

    return results
    # # on veut une liste de y
    # # de points dans chaque polygones
    # points = [(list(groupe), k) for k, groupe in groupby(segments, lambda couple: couple[1][0][1])]
    # pprint(points)
    # # ça passe sur mes premiers tests mais ce n'est pas la solution
    # # passe pas test 6
    # # TODO : faire un choix de polygone pour l'incrémentation lorqu'on en a plusieurs pour différentes lignes
    # # on enlève les lignes avec un point d'un polygone déjà sur une autre ligne
    # added, y = set(), set()
    # points_clip = []
    # for y_value, x in points:
    #     for yv in y_value:
    #         if yv[0] not in added and x not in y:
    #             points_clip.append([yv, x])
    #             added.add(yv[0])
    #             y.add(x)
    #         elif yv[0] not in added:
    #             points_clip.append([yv, x])
    #             added.add(yv[0])
    #             y.add(x)
    # pprint(points_clip)
    # # on va boucler sur cette liste précédemment affichée et appliquer crossing_number_global
    # liste_intersections = []
    # for point in points_clip:
    #     print(f"Ligne y = {point[1]}, point du polygone {point[0][0]}")
    #     # liste des coordonnées des intersections de chaque segment avec la droite y
    #     # l'abscisse du point n'est pas nécessaire dans point
    #     liste_intersections.append(sorted(crossing_number_global(segments, point)))
    #     print(liste_intersections)
    #     # for poly_number, crossings in d.items():
    #     #     g_d[poly_number] += crossings
    #
    # for absc in liste_x:
    #     for ligne in liste_intersections:
    #         new_list = list(filter(lambda x: x < absc, ligne))
    #         print(new_list)
    #
    # results = [-1] * len(polygones)
    # for poly_number, crossings in g_d.items():
    #     for indice, intersection_number in Counter(crossings).items():
    #         if intersection_number % 2 == 1:
    #             # print(f"Polygone {poly_number} in {indice}")
    #             results[poly_number] = indice

    # return results





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
