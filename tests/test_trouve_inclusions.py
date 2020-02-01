#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
test_trouve_inclusions.py : //
"""


import config
import pytest

from tycat import read_instance
from utils import get_files_matching_ext
from main import trouve_inclusions, trouve_inclusions_sorted


TROUVE_INCLUSIONS_FUNCTIONS = (trouve_inclusions, trouve_inclusions_sorted)
POLY_FILES = get_files_matching_ext(".poly", ["generated.poly"])
TESTS_INCLUSIONS = [
    ("10x10.poly", [-1, 0]),
    ("e2.poly", [1, -1, 0, 0]),
    ("e20.poly", [-1, 0, 1, 1]),
    ("e21.poly", [-1, 0, 1, 2]),
    ("e3.poly", [-1, 0, 1, 1, -1, 4, 5, 5]),
]


@pytest.mark.parametrize("file", POLY_FILES)
def test_compare_functions(file, functions=TROUVE_INCLUSIONS_FUNCTIONS):
    polygones = read_instance(file)
    assert all(
        [
            function1(polygones) == function2(polygones)
            for function1, function2 in zip(functions, functions[1:])
        ]
    )


@pytest.mark.parametrize("file, expected", TESTS_INCLUSIONS)
def test_inclusions(expected, file, function=trouve_inclusions_sorted):
    assert function(read_instance(file)) == expected
