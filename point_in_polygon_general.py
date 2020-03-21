import sys
from pprint import pprint
from tycat import read_instance, read_instance_v3
from itertools import combinations, islice, cycle
from collections import Counter, defaultdict


def couples(iterable):
    """
    iterate on all couples of given iterable.
    this will wrap around last element.
    """
    return zip(iterable, islice(cycle(iterable), 1, None))

def absolute_area(polygone):
    return abs(sum(cross_product(p1, p2) for p1, p2 in couples(polygone)) / 2)

def cross_product(p1, p2):
    return -p1[1] * p2[0] + p1[0] * p2[1]

def crossing_number_global(segments, ordo):
    """Renvoie si le point est dans le polygone.

    Si le point est exactement sur le bord du polygone, cette fonction peut retourner True ou False.

    Parameters:
        polygon (Polygon): //
        point (Point): //

    Returns:
        boolean : True if point in polygon

    """
    indice = 0
    nombre_de_points = len(segments)
    d = []

    while indice < nombre_de_points:
        segment = segments[indice]
        sommet0 = segment[1][0]
        sommet1 = segment[1][1]
        # test de hauteur
        if (sommet0[1] >= ordo > sommet1[1] or sommet1[1] >= ordo > sommet0[1]): # and (sommet1[0] <= absc or sommet0[0] <= absc):
            # le membre de gauche est la coordonnée de l'intersection du segment
            # avec la droite y
            inter = sommet1[0] + (ordo - sommet1[1]) / (sommet0[1] - sommet1[1]) * (sommet0[0] - sommet1[0])
            #if (sommet1[0] <= inter or sommet0[0] <= inter):
            # if inter < absc:
            #     # print("intersection")
            # poly = ligne[0]
            segment_numero_poly = segment[0]
            # if poly != segment_numero_poly: # on ne compte pas les intersections avec d'autres segments du même polygone
            d.append((segment_numero_poly, inter))
        indice += 1

    return sorted(d, key=lambda couple: couple[1], reverse=True) # nécessaire


def get_segments(polygones):
    segments = []
    # poly_indices = []
    # dictionnaire ce clé y et de valeur les points sur y
    y_points = defaultdict(list)
    for indice, polygon in enumerate(polygones):
        # poly_indices.append(indice)
        for segment in polygon.segments():
            segment_coord = []
            points = segment.endpoints
            for point in points:
                coord = point.coordinates
                segment_coord.append(coord)
            first_point = points[0].coordinates
            #segments.append((indice, sorted(segment_coord, key=lambda p: p[1])))
            segments.append((indice, segment_coord))
            # on ne veut pas de polygones en doublons
            for value in y_points[first_point[1]]:
                if value[0] == indice:
                    break
            else:
                y_points[first_point[1]].append((indice, first_point[0]))

    return segments, y_points

def choose_y(y_points, nombre_polygones):
    y_points_needed = defaultdict(list)
    poly_found = set()
    # on ne garde que les lignes avec le plus de points
    # on veut tous les polygones
    for ligne, value in sorted(y_points.items(), key=lambda x: len(x[1]), reverse=True):
        # print(ligne, value)
        # poly_indices, point = zip(*value)
        if len(poly_found) == nombre_polygones:
            break
        for indice, point in value:
            if indice not in poly_found:
                # poly_found.update(set(poly_indices))
                poly_found.add(indice)
                # print(poly_found)
                y_points_needed[ligne].append((indice, point))
    return y_points_needed

def trouve_inclusions_general(polygones):
    """problème avec 1
    ligne qui passe par 3 sommets (2 polygones carré gauche et grand milieu)

    """

    ### TEST des QUADRANTS ###
    #quadrants = [polygon.bounding_quadrant() for polygon in polygones]
    # on ne test pas les autres polygones
    poly_indices, _ = zip(*sorted(enumerate(polygones), key=lambda couple: couple[1].absolute_area))
    number_couples = set(combinations(poly_indices, 2)) # attention, combinations renvoie un générateur

    # print(number_couples)
    # for indice_poly1, indice_poly2 in number_couples:
    #     if not quadrants[indice_poly1].intersect_2(quadrants[indice_poly2]):
    #         continue

    nombre_polygones = len(polygones)
    results = [-1] * nombre_polygones
    # get all segments
    segments, y_points = get_segments(polygones)

    # segments.sort(key=lambda couple: couple[1][0][1]) # tri selon les y croissants
    # pprint(y_points)
    # print(len(y_points))

    # for indice, polygon in enumerate(polygones):
    #     # poly_indices.append(indice)
    #     segments_polygon = list(couples(polygon))
    #     # segments.extend(segments_polygon) # on a pas l'indice
    #     for segment in segments_polygon:
    #         segments.append((indice, segment))
    #     for segment in segments_polygon:
    #         first_point = segment[0]
    #         # on ne veut pas de polygones en doublons
    #         for value in y_points[first_point[1]]:
    #             if value[0] == indice:
    #                 break
    #         else:
    #             y_points[first_point[1]].append((indice, first_point[0]))


    # pprint(y_points)
    # pprint(segments)
    y_points_needed = choose_y(y_points, nombre_polygones)
    # pprint(y_points_needed)
    # print(len(y_points_needed))

    for ligne, value in y_points_needed.items():
        # print(f"y = {ligne}")
        liste_intersections = crossing_number_global(segments, ligne)
        if not liste_intersections: continue
        # pprint(liste_intersections)
        for poly_number, abscisse in value:
            less_inter = [couple for couple in liste_intersections if couple[1] > abscisse]
            #less_inter = liste_intersections
            if not less_inter: continue
            # print(f"Intersections de segments avec {poly_number} sur y = {ligne}")
            # pprint(less_inter)
            count = Counter(couple[0] for couple in less_inter)
            for indice, intersection_number in count.items():
                if (poly_number, indice) not in number_couples: # nécessaire
                    continue
                ### TEST des QUADRANTS ### trop long
                # if not quadrants[indice].intersect_2(quadrants[poly_number]):
                #     continue

                if intersection_number % 2 == 1:
                    # print(f"Polygone {poly_number} in {indice}")
                    results[poly_number] = indice
    return results


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        # polygones = read_instance_v3(fichier)
        inclusions = trouve_inclusions_general(polygones)
        print(inclusions)


if __name__ == "__main__":
    main()
