#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_point_in_polygon.py : //
"""

import config
import pytest


from tycat import read_instance
from point_in_polygon import crossing_number


TESTS = [(crossing_number, True)]


@pytest.mark.parametrize("function, expected", TESTS)
def test_point_in_polygon(function, expected):
    polygones = read_instance("e2.poly")
    assert function(polygones[1], polygones[0].points[0]) == expected


@pytest.mark.parametrize("function, expected", TESTS)
def test_all_points_in_polygon(function, expected):
    polygones = read_instance("e2.poly")
    for point in polygones[0].points:
        assert function(polygones[1], point) == expected
