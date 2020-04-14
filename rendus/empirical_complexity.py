#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
empirical_complexity.py : Calcule la complexité empirique par une régression.
"""

import sys
from collections import defaultdict
from pprint import pprint
from time import perf_counter_ns

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt


mpl.style.use("seaborn")


def perform_time_measurement(function, arguments, max_appels):
    """See https://github.com/NicovincX2/python-tools/blob/7129461f1a1c96871e864c0b3e97d982c4e0baae/measuring-code-execution-time.md
    """
    times = []
    for nombre_appels in range(1, max_appels):
        times.append(call_n_times(function, arguments, nombre_appels))

    # Process elapsed times
    return [end - start for start, end in zip(times, times[1:])]


def call_n_times(function, arguments, n):
    start = perf_counter_ns()
    for _ in range(n):
        function(*arguments)
    return start


def convert_ns(nanos):
    s = nanos // (10 ** (3 * 3))
    nanos %= 10 ** (3 * 3)
    millis = nanos // (10 ** (3 * 2))
    nanos %= 10 ** (3 * 2)
    micros = nanos // (10 ** (3 * 1))
    nanos %= 10 ** (3 * 1)

    return s, millis, micros, nanos


def empirical_complexity(functions_list, pip_functions, argument_function):

    # on aura max_appels - 2 mesures temporelles dans times
    # on a de 1 à max_appels - 1 mesures temporelles cumulées
    # et on récupère l'écart entre deux mesures successives
    max_appels = 9
    times = defaultdict(list)
    values = range(1, max_appels - 1)

    for pip_function in pip_functions:
        temp_times = defaultdict(list)
        for function in functions_list:
            elapsed_time = perform_time_measurement(
                function, [argument_function, pip_function], max_appels
            )
            assert len(elapsed_time) == len(range(1, max_appels - 1))
            print(elapsed_time)
            # le temps d'exécution est la pente de la droite
            m, p = np.polyfit(values, elapsed_time, 1)
            print("The execution time is:", convert_ns(m))
            times[(function.__name__, pip_function.__name__)].extend(
                [m, p, elapsed_time]
            )
            temp_times[(function.__name__, pip_function.__name__)].extend(
                [m, p, elapsed_time]
            )
        # affichage pour une fonction donnée des courbes des pip_functions
        affichages_multiples(values, temp_times)

    return values, times


def affichage(values, elapsed_time, functions_names, trend, colormap):
    # fig = plt.figure()

    c = next(colormap)
    plt.plot(values, elapsed_time, "o", color=c, label=f"{functions_names}")
    plt.plot(values, np.poly1d(trend)(values), color=c)
    plt.ylabel("Temps écoulé (ns)")
    plt.xlabel("Nombre d'appels")


    # plt.legend()
    # plt.savefig(f"plots/{functions_names[0]}{functions_names[1]}")


def affichages_multiples(values, times):
    colormap = iter(plt.cm.rainbow(np.linspace(0, 1, len(times))))
    # pprint(times)
    for functions_names, (m, p, elapsed_time) in times.items():
        affichage(values, elapsed_time, functions_names, (m, p), colormap)

    plt.ylabel("Temps écoulé (ns)")
    plt.xlabel("Nombre d'appels")
    plt.legend()
    # plt.show()
    plt.savefig(f"rendus/tests4/{sys.argv[1][15:-4]}")


def main():
    from algos_trouve_inclusions import (
        trouve_inclusions_sorted1,
        trouve_inclusions_sorted2,
        trouve_inclusions,
        trouve_inclusions_groupy1,
        trouve_inclusions_groupy2
    )
    from algos_pip import (
        crossing_number,
        crossing_number_v2,
        crossing_number_v3,
        crossing_number_v3_sec,
        crossing_number_v3_segments,
        crossing_number_v5,
        winding_number,
    )
    from tycat import read_instance

    pip_functions = [
        # crossing_number,
        # crossing_number_v2,
        # crossing_number_v3,
        crossing_number_v3_sec,
        # crossing_number_v3_segments,
        # crossing_number_v5,
        # winding_number,
    ]
    functions_list = [
        # trouve_inclusions,
        trouve_inclusions_sorted1,
        # trouve_inclusions_sorted2,
        trouve_inclusions_groupy1,
        # trouve_inclusions_groupy2, n'utilise pas les pip_functions
    ]
    polygones = read_instance(sys.argv[1])

    values, times = empirical_complexity(functions_list, pip_functions, polygones)

    # affichages_multiples(values, times)


if __name__ == "__main__":
    main()
