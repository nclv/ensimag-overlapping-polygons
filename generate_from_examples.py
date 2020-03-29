#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
generate_from_examples.py: //
"""


import numpy as np
from pprint import pprint


NUMBER = 10


def generator(number=10, example_file="tests/polyfiles/e2.poly", n=7, path=""):
    """Génération d'un fichier .poly.

    Parameters:
        n (int) : gère l'espacement entre les motifs, variable selon example_file.
        number (int): le nombre de lignes du fichier .poly produit.

    """
    with open(example_file, "r") as file:
        points = np.array([list(map(int, ligne.split())) for ligne in file])
        save_points = points.copy()
        increment = max(np.bincount(points[:, 0]))
        save_increment = increment
        for column in range(1, 3):
            # print(column, increment)
            for i in range(1, number):
                # print(increment)
                temp = save_points.copy()
                temp[:, 0] = temp[:, 0] + increment
                temp[:, column] = temp[:, column] + n * i
                points = np.append(points, temp, axis=0)
                increment += save_increment

    np.savetxt(path + f"generated_from_examples_{number}.poly", points, fmt='%i')


def generator2(number=4, example_file="tests/polyfiles/1bis.poly", path=""):
    with open(example_file, "r") as file:
        points = np.array([list(map(int, ligne.split())) for ligne in file])
        save_points = points.copy()
        for i in range(2, number + 1):
            temp = save_points.copy()
            temp[:, 0] = temp[:, 0] + i
            for column in range(1, 3):
                temp[:, column] = temp[:, column] * i
            points = np.append(points, temp, axis=0)

    np.savetxt(path + f"generate_{number}.poly", points, fmt='%i')

if __name__ == '__main__':
    # for i in range(1, 8):
    #     generator(number=i)
    generator2(number=50000, path="tests/polyfiles/")
