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
