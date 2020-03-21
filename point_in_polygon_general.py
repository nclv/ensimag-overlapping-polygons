import sys
from pprint import pprint
from tycat import read_instance
from itertools import groupby, combinations
from collections import Counter, defaultdict


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

    while indice < nombre_de_points:
        segment = polygon[indice]
        sommet0 = segment[1][0]
        sommet1 = segment[1][1]
        # test de hauteur et on ne garde que le point en dessous
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
                #d.append([poly, segment_numero_poly, inter])
            d.append((segment_numero_poly, inter))
        indice += 1

    return sorted(d, key=lambda couple: couple[1])


def trouve_inclusions_general(polygones):
    """problème avec 1
    ligne qui passe par 3 sommets (2 polygones carré gauche et grand milieu)

    """

    ### TEST des QUADRANTS ###
    quadrants = [polygon.bounding_quadrant() for polygon in polygones]
    areas = [polygon.absolute_area for polygon in polygones]
    # on ne test pas les autres polygones
    poly_couples, _ = zip(*sorted(enumerate(polygones), key=lambda couple: couple[1].absolute_area))
    number_couples = set(combinations(poly_couples, 2)) # attention, combinations renvoie un générateur
    nombre_polygones = len(polygones)

    results = [-1] * nombre_polygones
    # get all segments
    segments = []
    # dictionnaire ce clé y et de valeur les points sur y
    y_points = defaultdict(list)
    # sorted(enumerate(polygones), key=lambda couple: couple[1].absolute_area) ?
    for indice, polygon in enumerate(polygones):
        for segment in polygon.segments():
            segment_coord = []
            points = segment.endpoints
            for point in points:
                coord = point.coordinates
                segment_coord.append(coord)
            first_point = points[0].coordinates
            segments.append((indice, sorted(segment_coord, key=lambda p: p[1])))
            # on ne veut pas de polygones en doublons
            for value in y_points[first_point[1]]:
                if value[0] == indice:
                    break
            else:
                y_points[first_point[1]].append((indice, first_point[0]))
    segments.sort(key=lambda couple: couple[1][0][1]) # tri selon les y croissants
    # pprint(y_points)

    y_points_needed = defaultdict(list)
    poly_found = set()
    # on ne garde que les lignes avec le plus de points
    # on veut tous les polygones
    for ligne, value in sorted(y_points.items(), key=lambda x: len(x[1]), reverse=True):
        # print(ligne, value)
        poly_indices, _ = zip(*value)
        if len(poly_found) == nombre_polygones:
            break
        for indice in poly_indices:
            if indice not in poly_found:
                poly_found.update(set(poly_indices))
                # print(poly_found)
                y_points_needed[ligne] = value
    # pprint(y_points_needed)

    for ligne, value in y_points_needed.items():
        # print(f"y = {ligne}")
        liste_intersections = crossing_number_global(segments, ligne)
        if not liste_intersections: continue
        # pprint(liste_intersections)
        for poly_number, abscisse in value:
            less_inter = [couple for couple in liste_intersections if couple[1] < abscisse]
            if not less_inter: continue
            # print(f"Intersections de segments avec {poly_number} sur y = {ligne}")
            # pprint(less_inter)
            count = Counter(couple[0] for couple in less_inter)
            for indice, intersection_number in count.items():
                if (poly_number, indice) not in number_couples:
                    continue
                ### TEST des QUADRANTS ###
                if not quadrants[indice].intersect_2(quadrants[poly_number]):
                    continue

                if intersection_number % 2 == 1:
                    # print(f"Polygone {poly_number} in {indice}")
                    results[poly_number] = indice
    return results

    # # pprint(segments)
    # # on garde un segment par polygone
    # nombre_polygones = len(polygones)
    # set_poly = set(range(nombre_polygones))
    # segments_clip = []
    # taille_segments_clip = 0
    # for s in segments:
    #     poly_indice = s[0]
    #     if poly_indice in set_poly:
    #         segments_clip.append(s)
    #         set_poly.remove(poly_indice)
    #         taille_segments_clip += 1
    #     if taille_segments_clip == nombre_polygones:
    #         break
    # pprint(segments_clip)
    # # on extrait les y
    # # on extrait les point sur les lignes y
    # set_y_clip, set_x_clip = [], []
    # for s in segments_clip:
    #     point = s[1][0]
    #     y = point[1]
    #     x = point[0]
    #     if y not in set_y_clip:
    #         set_y_clip.append(y)
    #     set_x_clip.append((s[0], x))
    # print(set_y_clip)
    # print(set_x_clip)
    #
    # results = [-1] * len(polygones)
    # for ligne in set_y_clip: # remplacer par set_y
    #     print(f"y = {ligne}")
    #     liste_intersections = crossing_number_global(segments, ligne)
    #     pprint(liste_intersections)
    #     if not liste_intersections: continue
    #     # si d'autres points sont sur la même ligne
    #     for poly_number, absc in set_x_clip: # remplacer par liste_x
    #         # print(poly_number, absc)
    #         less_inter = [couple for couple in liste_intersections if couple[1] < absc and couple[0] != poly_number]
    #         if not less_inter: continue
    #         print(f"Intersections de segments avec {poly_number} sur y = {ligne}")
    #         pprint(less_inter)
    #         count = Counter(couple[0] for couple in less_inter)
    #         # filtered_count = {poly: True if count[poly] % 2 == 1 else False for poly in count}
    #         # print(filtered_count)
            # for indice, intersection_number in count.items():
            #     if poly_number == indice:
            #         continue
            #     if (poly_number, indice) not in number_couples:
            #         continue
            #     ### TEST des QUADRANTS ###
            #     if not quadrants[indice].intersect_2(quadrants[poly_number]):
            #         continue
            #
            #     if intersection_number % 2 == 1:
            #         print(f"Polygone {poly_number} in {indice}")
            #         # on a tracé une droite horizontale partant d'un point de poly_number
            #         # on a trouvé un nombre impair d'intersections avec des segments de indice
            #         # if results[poly_number] != -1:
            #         #     # print(areas[results[poly_number]], areas[indice])
            #         #     if areas[results[poly_number]] > areas[indice]:
            #         #         results[poly_number] = indice
            #         # else:
            #         results[poly_number] = indice
    #
    # return results
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
