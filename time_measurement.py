#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
time_measurement.py : //
"""


from time import perf_counter_ns
import os.path

from main import trouve_inclusions
from tycat import read_instance
from generate_from_examples import generator


def bench(preparation, a_mesurer, repetitions=30):
    temps = []
    for _ in range(repetitions):
        entree = preparation
        debut = perf_counter_ns()
        a_mesurer(entree)
        fin = perf_counter_ns()
        temps.append(fin - debut)
    return temps


def perf_test(a_mesurer):
    # augmenter le range de number si besoin, descendre à 6 pour avoir des résultats corrects et un temps réduit d'exécution
    for number in range(1, 6):
        filename = f"generated_from_examples_{number}.poly"
        if not os.path.exists(filename):
            print("Files generation...")
            generator(number=number)
        preparation = read_instance(filename)
        for temps in bench(preparation, a_mesurer):
            print(number, temps)


def main():
    perf_test(trouve_inclusions)
    # perf_test(trouve_inclusions_sorted)


if __name__=="__main__":
    main()
