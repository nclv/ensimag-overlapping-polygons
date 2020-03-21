#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
from utils import get_files_matching_ext
from main import trouve_inclusions_sorted
from tycat import read_instance

POLY_FILES = get_files_matching_ext(".poly")

for poly_file in POLY_FILES:
    # print(poly_file)
    polygones = read_instance(poly_file)
    inclusions = trouve_inclusions_sorted(polygones)
    np.savetxt(poly_file + ".result", inclusions, fmt="%i", newline=", ")
