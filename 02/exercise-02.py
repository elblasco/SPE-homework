#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import math


def weird_function(x: float) -> float:
    return (x**2) * math.sin(x * math.pi)**2


def weird_integral(x: float) -> float:
    return (((4 * math.pi**3 * x**3 - 6 * math.pi * x * math.cos(2 * math.pi * x) + (3 - 6 * math.pi**2 * x**2) * math.sin(2 * math.pi * x))/(24 * math.pi**3) + 4.424009112268247) /8.8480182)


def sampling_weird(a: int, b: int, M: int) -> float:
    while True:
        X = np.random.uniform(a, b, 1)[0]
        U = np.random.uniform(0, M, 1)[0]
        if U <= weird_function(X):
            return X


def bootstrap_procedure(array, r0, gamma, st_func):
    R = math.ceil(2*r0/(1-gamma))-1
    stat_calculated = []
    for _ in range(R):
        draws = np.random.choice(array, len(array))
        stat_calculated.append(st_func(draws))
    stat_calculated.sort()
    return (stat_calculated[r0], stat_calculated[R+1-r0])


if __name__ == "__main__":
    #### Punti 1 e 2
    x_upper_bound: int = 3
    x_lower_bound: int = -3
    # obtained with WolframAlpha
    y_upper_bound: float = 6.36
    samples: list = []
    for _ in range(20000):
        samples.append(
            sampling_weird(x_lower_bound, x_upper_bound, y_upper_bound)
        )

    #### Punto 3
    n = 20000
    sub_sample = samples[:n]
    sub_sample.sort()
    exact_median: float = (sub_sample[int((n/2)-1)] + sub_sample[int(n/2)]) / 2
    eta: float = 1.96
    low: int = math.floor(n/2 - eta/2 * math.sqrt(n))
    up: int = math.ceil(n/2 + eta/2 * math.sqrt(n) + 1)
    print("Median", exact_median, "[", sub_sample[low], ";", sub_sample[up], "]")

    print(bootstrap_procedure(sub_sample, 25, 0.95, lambda arr: (arr[int((n/2)-1)] + arr[int(n/2)]) / 2))

    #### Punto 4
    y = []
    x = []
    for X in np.linspace(-3, 3, 1000):
        x.append(X)
        y.append(weird_integral(X))
    # fig, ax = plt.subplots()
    # ax.ecdf(samples)
    # plt.plot(x, y)
    # plt.show()
