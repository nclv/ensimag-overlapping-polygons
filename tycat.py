#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from geo.tycat import tycat
from geo.polygon import Polygon
from geo.point import Point
from itertools import groupby


def print_polygons(polygons):
    print("we have", len(polygons), "polygons")
    tycat(*(poly.segments() for poly in polygons))


def read_instance(fname):
    with open(fname, "rt") as file:
        points = (tuple(map(float, ligne.split())) for ligne in file)
        # create polygons from [(l, x, y)]
        return [
            (int(indice), Polygon([Point(p[1:]) for p in poly_points]))
            for indice, poly_points in groupby(points, key=lambda t: t[0])
        ]


def read_instance_v2(filename):
    with open(filename, "rt") as file:
        points = (tuple(map(float, ligne.split())) for ligne in file)
        for indice, poly_points in groupby(points, key=lambda t: t[0]):
            yield int(indice), Polygon([Point(p[1:]) for p in poly_points])


def main():
    if len(sys.argv) <= 1:
        return

    for poly_file in sys.argv[1:]:
        print(poly_file)
        polys = read_instance(poly_file)
        print_polygons(polys)


if __name__ == "__main__":
    main()
