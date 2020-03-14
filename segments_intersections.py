#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from geo.segment import Segment
from geo.point import Point
from collections import Counter
from pprint import pprint
from tycat import read_instance
import sys


def trouve_intersections(
    couples_indice_segment, couples_indice_ligne, quadrants, areas
):
    # on tri les endpoints dans la classe segment
    # on tri les segments selon y
    mapping_lignes = []
    couples_indice_segment_tries = sorted(
        couples_indice_segment, key=lambda couple: couple[1].endpoints[0].coordinates[1]
    )
    for ligne_indice, ligne in couples_indice_ligne:
        crossing_segments = []
        for poly_indice, segment in couples_indice_segment_tries:
            # c'est ici que l'on peut améliorer les perfs
            if poly_indice != ligne_indice:
                if not quadrants[ligne_indice].intersect_2(quadrants[poly_indice]):
                    continue
                if areas[poly_indice] < areas[ligne_indice]:
                    continue
                if segment.intersect(ligne):
                    crossing_segments.append(poly_indice)
        mapping_lignes.append((ligne_indice, crossing_segments))
    return mapping_lignes


def point_in_polygon(mapping_lignes):
    results = [-1] * len(mapping_lignes)
    for poly_number, crossings in mapping_lignes:
        for indice, intersection_number in Counter(crossings).items():
            if intersection_number % 2 == 1:
                # print(f"Polygone {poly_number} in {indice}")
                results[poly_number] = indice
    return results


def get_segments(polygones):
    max_length = 9999.0
    couples_indice_segment = []
    couples_indice_ligne = []
    quadrants = [polygon.bounding_quadrant() for polygon in polygones]
    areas = [polygon.absolute_area for polygon in polygones]
    for indice, polygone in sorted(
        enumerate(polygones), key=lambda couple: couple[1].absolute_area
    ):
        point = polygone.points[0].coordinates
        couples_indice_ligne.append(
            (
                indice,
                Segment([Point([point[0], point[1]]), Point([max_length, point[1]])]),
            )
        )
        for segment in polygone.segments():
            couples_indice_segment.append((indice, segment))
    return couples_indice_segment, couples_indice_ligne, quadrants, areas


def trouve_inclusions_segments(polygones):
    couples_indice_segment, couples_indice_ligne, quadrants, areas = get_segments(
        polygones
    )
    mapping_lignes = trouve_intersections(
        couples_indice_segment, couples_indice_ligne, quadrants, areas
    )
    # pprint(mapping_lignes)
    return point_in_polygon(mapping_lignes)


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        inclusions = trouve_inclusions_segments(polygones)
        print(inclusions)


if __name__ == "__main__":
    main()
