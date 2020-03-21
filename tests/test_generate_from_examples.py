#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
test_generate_from_examples.py : //
"""


import config
import pytest
import os.path

from generate_from_examples import generator
from utils import tous_entiers_croissante


@pytest.mark.parametrize("number", [(2**1), (2**2), (2**4), (2**6), (2**7), (2**8), (2**9)])
def test_polygones_increasing_indexes(number):
    """Vérification de l'odre des indices de chaque polygone"""

    filename = config.TESTS_PATH + f"generated_from_examples_{number}.poly"

    if not os.path.exists(filename):
        print("Files generation...")
        generator(number=number, path=config.TESTS_PATH)

    with open(filename, 'r') as file:
        suite = [int(ligne.split()[0]) for ligne in file]
        assert tous_entiers_croissante(suite) == True
