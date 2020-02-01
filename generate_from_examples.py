#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
generate_from_examples.py: //
"""


import numpy as np


EXAMPLE_FILE = "e2.poly"
N = 7
NUMBER = 10 # le nombre de lignes


with open(EXAMPLE_FILE, "r") as file:
    points = np.array([list(map(int, ligne.split())) for ligne in file])
    increment = max(np.bincount(points[:, 0]))
    for column in range(1, 3):
        for i in range(1, NUMBER):
            temp = points.copy()
            temp[:, 0] = temp[:, 0] + increment + i - 1
            temp[:, column] = temp[:, column] + N * i
            #print(temp)
            points = np.append(points, temp, axis=0)
            increment += 1

np.savetxt("generated_from_examples.poly", points, fmt='%i')
