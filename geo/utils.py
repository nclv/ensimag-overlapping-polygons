#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
utils.py : //
"""


def almostEqual(x, y, EPSILON=1e-5):
    return abs(x - y) < EPSILON
