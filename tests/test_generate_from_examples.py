#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
test_generate_from_examples.py : //
"""


import config
import pytest

from generate_from_examples import generator
from utils import tous_entiers_croissante


@pytest.mark.parametrize("number", [(2), (3), (4)])
def test_polygones_increasing_indexes(number):
    generator(number=number)
    with open(f"generated_from_examples_{number}.poly", 'r') as file:
        suite = [int(ligne.split()[0]) for ligne in file]
        assert tous_entiers_croissante(suite) == True
