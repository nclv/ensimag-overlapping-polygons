import sys
from pprint import pprint
from tycat import read_instance, read_instance_v3
from itertools import combinations, islice, cycle
from collections import Counter, defaultdict, OrderedDict
from operator import itemgetter


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

def crossing_number_global(segments, ordo, value, min_x, mapping):#, poly_number, number_couples):
    """Renvoie si le point est dans le polygone.

    Si le point est exactement sur le bord du polygone, cette fonction peut retourner True ou False.

    Parameters:
        polygon (Polygon): //
        point (Point): //

    Returns:
        boolean : True if point in polygon

    """
    # on choisi d'ajouter les points correspondants à des extrémités
    # sinon on peut passer à côté d'un polygone sur cette ligne
    # mais cela rajoute aussi des éléments inutiles dans la liste d
    interup, interdown = [], []
    pprint(mapping)

    for poly_indice, points in segments:
        # après affectation results[poly_number] = indice
        # lsq ligne indice, il ne faut pas prendre les segments de poly_number
        # for result in results:
        #     if result == poly_indice:
        #         continue
        # (value[0], poly_indice)
        # if (poly_number, poly_indice) not in number_couples:
        #     continue
        # print(poly_indice)
        counter = 0
        nombre_de_points = len(points)
        sommet0 = points[-1]
        y0, x0 = sommet0[1], sommet0[0]
        # permet de savoir l'orientation relative de deux segments
        while counter < nombre_de_points:
            sommet1 = points[counter]
            y1, x1 = sommet1[1], sommet1[0]
            # print(y_0, y_1, sommet0, sommet1)
            
            # on compte seulement la traversée dans un sens
            # if y0 == ordo:
            #     if x0 < x1:
            #         d.append((poly_indice, x0))
            #     elif x0 == x1 and y0 < y1:
            #         d.append((poly_indice, x0))
            # if y1 == ordo:
            #     if x0 > x1:
            #         d.append((poly_indice, x1))
            #     elif x0 == x1 and y0 < y1:
            #         d.append((poly_indice, x1))
            
            # (y0 >= ordo > y1 or y1 >= ordo > y0) n'ajoute que les traits qui traversent et ceux qui sont au dessus
            # (y0 > ordo >= y1 or y1 > ordo >= y0) n'ajoute que les traits qui traversent et ceux qui sont en dessous
            if (y0 >= ordo > y1 or y1 >= ordo > y0):# or (y0 > ordo >= y1 or y1 > ordo >= y0):# and (x1 <= max_x or x0 <= max_x): # la deuxième condition apporte un petit gain
            #if sommet0[1] != sommet1[1]:
                # le membre de gauche est la coordonnée de l'intersection du segment
                # avec la droite y
                inter = x1 + (ordo - y1) / (y0 - y1) * (x0 - x1)
                #if (sommet1[0] <= inter or sommet0[0] <= inter):
                # if inter < absc:
                #     # print("intersection")
                # poly = ligne[0]
                # segment_numero_poly = segment[0]
                # if inter < max_x:
                # if poly != segment_numero_poly: # on ne compte pas les intersections avec d'autres segments du même polygone
                # print("Polygone avec intersection :", poly_indice)
                # if inter >= min_x and
                #print(sommet0[1], sommet1[1])
                #if not (poly_indice, inter) in d:
                    #print(inter)
                interup.append((poly_indice, inter))
            if (y0 > ordo >= y1 or y1 > ordo >= y0):
                inter = x1 + (ordo - y1) / (y0 - y1) * (x0 - x1)
                interdown.append((poly_indice, inter))
            y0, x0 = y1, x1
            sommet0 = sommet1
            counter += 1

    return sorted(interup, key=lambda couple: mapping[couple[0]]), sorted(interdown, key=lambda couple: mapping[couple[0]]) # nécessaire


def get_segments(sorted_polygones):
    # les segments du fichier des polygones sont déjà triés
    # ie. points d'un même polygone à la suite des autres
    # on a besoin de trier car on enlève des éléments ensuite
    segments = []
    mapping = dict()
    # poly_indices = []
    # dictionnaire ce clé y et de valeur les points sur y
    y_points = defaultdict(list)
    nombre_poly_sur_y = defaultdict(int)
    for indice, (poly_number, polygon) in enumerate(sorted_polygones):

        mapping[poly_number] = indice
        # print(compteur)
        # poly_indices.append(indice)
        points = []
        for segment in polygon.segments():
            # segment_coord = []
            # points = segment.endpoints
            # for point in points:
            #     coord = point.coordinates
            #     segment_coord.append(coord)
            # first_point = points[0].coordinates
            # # on a besoin que du premier point
            # #segments.append((indice, sorted(segment_coord, key=lambda p: p[1])))
            # segments.append((indice, segment_coord))
            # en fait on a besoin que du premier point
            first_point = segment.endpoints[0].coordinates
            second_point = segment.endpoints[1].coordinates
            #segments[indice].append(first_point)
            points.append(first_point)
            # on ne veut pas de polygones en doublons
            y_points[second_point[1]].append((poly_number, second_point[0]))
            y_points[first_point[1]].append((poly_number, first_point[0]))
        segments.append((poly_number, points))

    for ligne, value in y_points.items():
        seen = set()
        for indice_poly, absc in value:
            if indice_poly not in seen:
                seen.add(indice_poly)
                nombre_poly_sur_y[ligne] += 1

    return segments, y_points, nombre_poly_sur_y, mapping

def choose_y(y_points, nombre_polygones, nombre_poly_sur_y):
    y_points_needed = defaultdict(list)
    poly_found = set()
    # on ne garde que les lignes avec le plus de points
    # on veut tous les polygones
    for ligne, value in sorted(y_points.items(), key=lambda couple: nombre_poly_sur_y[couple[0]], reverse=True):
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
    
    sorted_polygones = sorted(enumerate(polygones), key=lambda couple: couple[1].absolute_area)
    nombre_polygones = len(polygones)
    results = [-1] * nombre_polygones
    # get all segments
    segments, y_points, nombre_poly_sur_y, mapping = get_segments(sorted_polygones)
    pprint(y_points)
    pprint(segments)
    y_points_needed = choose_y(y_points, nombre_polygones, nombre_poly_sur_y)
    pprint(y_points_needed)

    liste_poly_done = []
    for ligne, value in y_points_needed.items():
        print(liste_poly_done)
        for num_poly, _ in value:
            if num_poly in liste_poly_done:
                break
        else:
            value = y_points[ligne]
            value.sort(key=lambda couple: couple[1])
            print(f"y = {ligne}, {value}")
            min_x = min(value, key=itemgetter(1))[1]
            # print(max_x)
            polygones_a_tester, _ = zip(*segments)
            pprint(polygones_a_tester)         
            # pprint(segments)
            interup, interdown = crossing_number_global(segments, ligne, value, min_x, mapping)
            if not interup and not interdown: continue
            print("intersections")
            pprint(interup)
            pprint(interdown)
            liste_intersections = interdown
            nombre_intersections = len(liste_intersections)

            compteur = defaultdict(int)
            # x1 = liste_intersections[0][1]
            # for indice_poly2, x2 in liste_intersections[1:]:
            #     if x2 > x1:
            #         compteur[indice_poly2] += 1
            # print("compteur", compteur)
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
                if results[indice_poly1] != -1:
                    continue
                for j in range(i + 1, nombre_intersections):
                    inter2 = liste_intersections[j]
                    indice_poly2 = inter2[0]
                    # on construit le compteur au premier tour
                    if inter2[1] > inter1[1]:
                        compteur[indice_poly2] += 1
                print(compteur)
                # on réduit le compteur
                first = None
                for indice, intersection_number in compteur.items():
                    if first is None: first = indice
                    print(first)
                    if intersection_number % 2 == 1:
                        print(f"Polygone {indice_poly1} in {indice}")
                        # lsq ligne indice, il ne faut pas prendre les segments de poly_number
                        results[indice_poly1] = indice
                        liste_poly_done.append(first)
                        break
    
    return results
                
                # if not quadrants[indice_poly1].intersect_2(quadrants[indice_poly2]):
                #     continue
                # if is_point_in_polygon(polygon2[1], polygon1[1].points[0]):
                #     results[indice_poly1] = indice_poly2
                #     # print(indice_poly1, indice_poly2)
                #     break

def old_trouve_inclusions_general(polygones):
    """problème avec 1
    ligne qui passe par 3 sommets (2 polygones carré gauche et grand milieu)

    """

    ### TEST des QUADRANTS ###
    quadrants = [polygon.bounding_quadrant for polygon in polygones]
    # on ne test pas les autres polygones
    sorted_polygones = sorted(enumerate(polygones), key=lambda couple: couple[1].absolute_area)
    #poly_indices, _ = zip(*sorted_polygones)
    #number_couples = set(combinations(poly_indices, 2)) # attention, combinations renvoie un générateur

    # print(number_couples)
    # for indice_poly1, indice_poly2 in number_couples:
    #     if not quadrants[indice_poly1].intersect_2(quadrants[indice_poly2]):
    #         continue

    nombre_polygones = len(polygones)
    results = [-1] * nombre_polygones
    # get all segments
    segments, y_points, nombre_poly_sur_y, mapping = get_segments(sorted_polygones)

    # segments.sort(key=lambda couple: couple[1][0][1]) # tri selon les y croissants
    pprint(y_points)
    
    #pprint(mapping)
    #pprint(nombre_poly_sur_y)
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
    pprint(segments)
    nombre_segments = len(segments)
    y_points_needed = choose_y(y_points, nombre_polygones, nombre_poly_sur_y)
    pprint(y_points_needed)
    # print(len(y_points_needed))
    liste_poly_done = []
    for ligne, value in y_points_needed.items():
        print(liste_poly_done)
        for num_poly, _ in value:
            if num_poly in liste_poly_done:
                break
        else:
            value = y_points[ligne]
            value.sort(key=lambda couple: couple[1])
            print(f"y = {ligne}, {value}")
            min_x = min(value, key=itemgetter(1))[1]
            # print(max_x)
            polygones_a_tester, _ = zip(*segments)
            pprint(polygones_a_tester)
            # pprint(segments)
            liste_intersections = crossing_number_global(segments, ligne, value, min_x, mapping)#, value, number_couples)
            if not liste_intersections: continue
            print("intersections")
            pprint(liste_intersections)
            #pprint(list(combinations(liste_intersections, 2)))

            compteur = defaultdict(int)
            c, sup = 0, len(liste_intersections) - 1
            done = False
            for (numero_poly1, interx1), (numero_poly2, interx2) in combinations(liste_intersections, 2):
                # already done
                if results[numero_poly1] != -1:
                    c += 1
                    continue
                # cas 0 in 0
                if numero_poly1 == numero_poly2:
                    c += 1
                    continue
                if not done and interx2 > interx1:
                    # print(c, sup)
                    # print((numero_poly1, interx1), (numero_poly2, interx2))
                    compteur[numero_poly2] += 1
                    #print(compteur)
                c += 1
                if c == sup or done:
                    sup -= 1
                    c = 0
                    done = True # flag de la première création du compteur
                    if compteur:
                        print(compteur)
                        # on réduit le compteur tout en continuant à l'incrémenter
                        first = None
                        for indice, intersection_number in compteur.items():
                            if first is None: first = indice
                            print(first)
                            if intersection_number % 2 == 1:
                                print(f"Polygone {numero_poly1} in {indice}")
                                # lsq ligne indice, il ne faut pas prendre les segments de poly_number
                                results[numero_poly1] = indice
                                liste_poly_done.append(first)
                                break
                        compteur.pop(first)
    # pprint(y_points_needed)
        # polygones_a_tester = []
        # for poly_number, abscisse in value:
        #     if not segments: break
        #     segments.pop(avancee)
        # # for poly_number, abscisse in value:
        # #     liste_intersections = crossing_number_global(segments, ligne, max_x, poly_number, number_couples)
        #     #print(poly_number)
        #     # pprint(segments)
        #     # polygones_a_tester = []
        #     # for count, (indice_poly, liste_segments) in enumerate(segments):
        #     #     # print(indice_poly, count)
        #     #     if count == nombre_segments - 1:
        #     #         break
        #     #     if indice_poly == poly_number:
        #     #         polygones_a_tester, _ = zip(*segments[count + 1:])
        #     #         break
        #     # if not polygones_a_tester: break
        #     if not polygones_a_tester:
        #         polygones_a_tester, _ = zip(*segments)
        #
        #     pprint(polygones_a_tester)
        #     #liste_intersections = crossing_number_global(segment_a_tester, ligne, max_x)
        #     #pprint(liste_intersections)
        #     # print(f"may be in polygone {poly_number}")
        #     #less_inter = [couple for couple in liste_intersections if couple[0] in polygones_a_tester and couple[1] < abscisse]# and (poly_number, couple[0]) in number_couples]
        #     #if not less_inter: continue
        #     #print(f"Intersections de segments avec {poly_number} sur y = {ligne}")
        #     #pprint(less_inter)
        #     #count = Counter(couple[0] for couple in less_inter)
        #     count = Counter(couple[0] for couple in liste_intersections if couple[0] in polygones_a_tester and couple[1] > abscisse)
        #
        #     # on ne retest pas ERREUR
        #     # for poly_numb in polygones_a_tester:
        #     # del segments[poly_number]
        #     for indice, intersection_number in count.items():
        #         # if (poly_number, indice) not in number_couples: # nécessaire
        #         #     continue
        #         ### TEST des QUADRANTS ### trop long
        #         # if not quadrants[indice].intersect_2(quadrants[poly_number]):
        #         #     continue
        #
        #         if intersection_number % 2 == 1:
        #             print(f"Polygone {poly_number} in {indice}")
        #             # lsq ligne indice, il ne faut pas prendre les segments de poly_number
        #             results[poly_number] = indice
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
