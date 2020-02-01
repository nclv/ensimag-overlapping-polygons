#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
generate_from_examples.py: //
"""


import numpy as np


NUMBER=10


def generator(number=10, example_file="e2.poly", n=7):
    """Génération d'un fichier .poly.

    Parameters:
        n (int) : gère l'espacement entre les motifs, variable selon example_file.
        number (int): le nombre de lignes du fichier .poly produit.

    """
    with open(example_file, "r") as file:
        points = np.array([list(map(int, ligne.split())) for ligne in file])
        increment = max(np.bincount(points[:, 0]))
        for column in range(1, 3):
            for i in range(1, number):
                temp = points.copy()
                temp[:, 0] = temp[:, 0] + increment + i - 1
                temp[:, column] = temp[:, column] + n * i
                #print(temp)
                points = np.append(points, temp, axis=0)
                increment += 1

    np.savetxt(f"generated_from_examples_{number}.poly", points, fmt='%i')
