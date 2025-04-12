#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import math


def weird_function(x: float) -> float:
    return (x**2) * math.sin(x * math.pi)**2


def weird_integral(x: float) -> float:
    return ((4 * math.pi ** 3 * x ** 3 - 6 * math.pi * x * math.cos(2 * math.pi * x) + (3 - 6 * math.pi ** 2 * x ** 2) * math.sin(2 * math.pi * x)) / (24 * math.pi ** 3) + 4.424009112268247) /8.8480182


def sampling_weird(a: float, b: float, upper: float) -> float:
    while True:
        x = float(np.random.uniform(a, b, 1)[0])
        u = float(np.random.uniform(0, upper, 1)[0])
        if u <= weird_function(x):
            return x


def bootstrap_procedure(array, r0: int, gamma: float, st_func):
    r = math.ceil(2*r0/(1-gamma))-1
    stat_calculated = []
    for _ in range(r):
        draws = np.random.choice(array, len(array))
        stat_calculated.append(st_func(draws))
    stat_calculated.sort()
    return stat_calculated[r0], stat_calculated[r + 1 - r0]


def main():
    #### Punti 1 e 2
    y_upper_bound = 6.36 # obtained with WolframAlpha
    samples = []
    for _ in range(20000):
        samples.append(sampling_weird(-3, 3, y_upper_bound))

    #### Punto 3
    n = 20000
    sub_sample = samples[:n]
    sub_sample.sort()
    exact_median = np.median(sub_sample)
    eta = 1.96
    low = math.floor(n/2 - eta/2 * math.sqrt(n))
    up = math.ceil(n/2 + eta/2 * math.sqrt(n) + 1)
    print("Median", exact_median, "[", sub_sample[low], ";", sub_sample[up], "]")
    print(bootstrap_procedure(sub_sample, 25, 0.95, lambda arr: np.median(arr)))

    #### Punto 4
    x = np.linspace(-3, 3, 1000)
    y = []
    for v in x:
        y.append(weird_integral(v))

    fig, ax = plt.subplots()
    ax.ecdf(samples, label="experimental")
    plt.plot(x, y, label="expected")
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()