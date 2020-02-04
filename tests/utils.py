#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
utils.py: //
"""

import glob


def get_files_matching_ext(extension, exceptions):
    """Renvoie les fichier d'extension ext."""
    return [file for file in glob.glob(f"*{extension}") if file not in exceptions]


def tous_entiers_croissante(liste):
    if len(liste) > 1 :
        precedent = liste[0]
        for element in liste:
            if element != precedent and element != precedent + 1:
                return False
            precedent = element
    return True


def iterate(iterable, n):
    first = []
    for second in iterable:
        first.append(second)
        if len(first) == n:
            yield first
            first = []
    yield first


def check_result(liste):
    assert liste[0] == 1
    first_element = liste[1:5]
    n1, n2, c1, c2 = 3, 4, 0, 0
    for indice, element in enumerate(iterate(liste[1:], 4)):
        el = first_element[1]
        if indice == n1 + 8 * c1:
            c1 += 1
            assert element == [-1, el + 4 * indice, el + 4 * indice + 7, (el + 4 * indice) + 1]
        elif indice == n2 + 8 * c2:
            c2 += 1
            assert element == [-1, el + 4 * (indice - 1), el + 4 * (indice - 1) + 3, (el + 4 * indice) + 5]
        else:
            print(element, [-1, el + 4 * indice, el + 4 * indice, (el + 4 * indice) + 5], indice)
            if indice == 24: el +=
            assert element == [-1, el + 4 * indice, el + 4 * indice, (el + 4 * indice) + 5]


if __name__ == "__main__":
    a = [1, -1, 0, 0, 5, -1, 4, 4, 9, -1, 8, 8, 13, -1, 12, 19, 13, -1, 12, 15, 21, -1, 20, 20, 25, -1, 24, 24, 29, -1, 28, 28, 33, -1, 32, 32, 37, -1, 36, 36, 41, -1, 40, 40, 45, -1, 44, 51, 45, -1, 44, 47, 53, -1, 52, 52, 57, -1, 56, 56, 61, -1, 60, 60, 65, -1, 64, 64, 69, -1, 68, 68, 73, -1, 72, 72, 77, -1, 76, 83, 77, -1, 76, 79, 85, -1, 84, 84, 89, -1, 88, 88, 93, -1, 92, 92, 97, -1, 96, 131, 101, -1, 100, 135, 105, -1, 104, 139, 109, -1, 108, 115, 109, -1, 108, 111, 117, -1, 116, 151, 121, -1, 120, 155, 125, -1, 124, 159, 97, -1, 96, 99, 101, -1, 100, 103, 105, -1, 104, 107, 109, -1, 108, 111, 109, -1, 108, 111, 117, -1, 116, 119, 121, -1, 120, 123, 125, -1, 124, 127, 161, -1, 160, 160, 165, -1, 164, 164, 169, -1, 168, 168, 173, -1, 172, 179, 173, -1, 172, 175, 181, -1, 180, 180, 185, -1, 184, 184, 189, -1, 188, 188, 193, -1, 192, 192, 197, -1, 196, 196, 201, -1, 200, 200, 205, -1, 204, 211, 205, -1, 204, 207, 213, -1, 212, 212, 217, -1, 216, 216, 221, -1, 220, 220, 225, -1, 224, 224, 229, -1, 228, 228, 233, -1, 232, 232, 237, -1, 236, 243, 237, -1, 236, 239, 245, -1, 244, 244, 249, -1, 248, 248, 253, -1, 252, 252]
    check_result(a)
