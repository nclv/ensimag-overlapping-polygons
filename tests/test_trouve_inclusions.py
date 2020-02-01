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


@pytest.mark.parametrize("file", POLY_FILES)
def test_compare_functions(file, functions=TROUVE_INCLUSIONS_FUNCTIONS):
    polygones = read_instance(file)
    assert all(
        [
            function1(polygones) == function2(polygones)
            for function1, function2 in zip(functions, functions[1:])
        ]
    )
