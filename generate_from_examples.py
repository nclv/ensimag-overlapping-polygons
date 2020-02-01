#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
generate_from_examples.py: //
"""


import numpy as np


EXAMPLE_FILE = "e2.poly"
N = 8


with open(EXAMPLE_FILE, "r") as file:
    points = np.array([list(map(float, ligne.split())) for ligne in file])
    for i in range(10):
        points = np.append(points, points + N * i, axis=0)

np.savetxt("generated_from_examples.poly", points, fmt='%i')
