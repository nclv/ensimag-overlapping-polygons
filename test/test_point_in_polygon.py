#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_point_in_polygon.py : //
"""

import config
import pytest


from tycat import read_instance
from point_in_polygon import crossing_number


TESTS_2_POLY = [(crossing_number, "10x10.poly", True)]


@pytest.mark.parametrize("function, file, expected", TESTS_2_POLY)
def test_point_in_polygon(function, expected, file):
    """on vérifie qu'un point du polygone est inclut dans l'autre polygone"""
    polygones = read_instance(file)
    assert len(polygones) == 2
    assert function(polygones[0], polygones[1].points[0]) == expected


@pytest.mark.parametrize("function, file, expected", TESTS_2_POLY)
def test_all_points_in_polygon(function, expected, file):
    """on vérifie que tous les points du polygone sont inclus dans l'autre polygone"""
    polygones = read_instance(file)
    assert len(polygones) == 2
    for point in polygones[1].points:
        assert function(polygones[0], point) == expected
