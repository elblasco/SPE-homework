#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import math


def weird_function(x: float) -> float:
    return (x**2) * math.sin(x * math.pi)**2


def weird_integral(x: float) -> float:
    return ((4 * math.pi ** 3 * x ** 3 - 6 * math.pi * x * math.cos(2 * math.pi * x)
            + (3 - 6 * math.pi ** 2 * x ** 2) * math.sin(2 * math.pi * x))
            / (24 * math.pi ** 3) + 4.424009112268247) /8.8480182


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
    n = 200
    sub_sample = samples[:n]
    print("Over 200 cases:")

    #### Punto 3 Median
    sub_sample.sort()
    exact_median = np.median(sub_sample)
    eta = 1.96
    low = math.floor(n/2 - eta/2 * math.sqrt(n))
    up = math.ceil(n/2 + eta/2 * math.sqrt(n) + 1)
    print("Median", exact_median, "[", sub_sample[low], ";", sub_sample[up], "]")
    print(bootstrap_procedure(sub_sample, 25, 0.95, np.median))

    #### Punto 3 Median
    quant_90 = np.quantile(sub_sample, 0.9)
    low90 = math.floor(n * 0.9 - eta * math.sqrt(n * 0.9 * (1 - 0.9)))
    up90 = math.ceil(n * 0.9 + eta/2 * math.sqrt(n * 0.9 * (1 - 0.9)) + 1)
    print("Median", quant_90, "[", sub_sample[low90], ";", sub_sample[up90], "]")
    print(bootstrap_procedure(sub_sample, 25, 0.95, lambda arr: np.quantile(arr, 0.9)))

    #### Punto 3 Mean
    mean = float(np.mean(sub_sample))
    std_dev_mean = float(np.std(sub_sample))
    error_mean = eta * std_dev_mean / math.sqrt(n)
    #quant_90 = np.quantile(sub_sample, 0.9)
    #low90 = math.floor(n * 0.9 - eta * math.sqrt(n * 0.9 * (1 - 0.9)))
    #up90 = math.ceil(n * 0.9 + eta/2 * math.sqrt(n * 0.9 * (1 - 0.9)) + 1)
    print("Mean", mean, "+-", error_mean, "[", (mean - error_mean), ";", (mean + error_mean), "]")
    print(bootstrap_procedure(sub_sample, 25, 0.95, np.mean))

    ### Punto 4
    correct200 = 0
    for set200 in np.reshape(samples, (100, 200)):
        mean200 = float(np.mean(set200))
        std_dev_mean_200 = float(np.std(set200))
        error_mean200 = eta * std_dev_mean_200 / math.sqrt(n)
        low_mean200 = mean200 - error_mean200
        high_mean200 = mean200 + error_mean200
        if low_mean200 <= 0 <= high_mean200:
            correct200 += 1
    print("True mean is in interval ", correct200, "% of the times")


    ### Plot
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