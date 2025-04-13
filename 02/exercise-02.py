#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import math

PI = math.pi
ETA95 = 1.96

def func_points(function) -> ([float], [float]):
    x = np.linspace(-3, 3, 1000)
    y = []
    for v in x:
        y.append(function(v))
    return x, y

def weird_function(x: float) -> float:
    return x**2 * math.sin(x * PI)**2

def weird_integral(x: float) -> float:
    return ((4 * PI**3 * x**3 - 6 * PI * x * math.cos(2 * PI * x)
            + (3 - 6 * PI**2 * x**2) * math.sin(2 * PI * x))
            / (24 * PI**3) + 4.424009112268247) / 8.8480182

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
    return float(stat_calculated[r0]), float(stat_calculated[r + 1 - r0])

def es3median(arr_sorted):
    es3quantile(arr_sorted, 0.5)

def es3mean(arr):
    n = len(arr)
    mean = float(np.mean(arr))
    std_dev_mean = float(np.std(arr))
    error_mean = ETA95 * std_dev_mean / math.sqrt(n)
    print("Mean", mean, "+-", error_mean,
          "with CI", (mean - error_mean, mean + error_mean),
          "\n\tand with bootstrap CI", bootstrap_procedure(arr, 25, 0.95, np.mean))

def es3quantile(arr_sorted, q):
    n = len(arr_sorted)
    quant = np.quantile(arr_sorted, q)
    low = math.floor(n * q - ETA95 * math.sqrt(n * q * (1 - q)))
    up = math.ceil(n * q + ETA95 * math.sqrt(n * q * (1 - q)) + 1)
    ci_boot = bootstrap_procedure(arr_sorted, 25, 0.95, lambda arr: np.quantile(arr, q))

    if q == 0.5:
        print("The median is ", end="")
    else:
        print("The", q, "quantile is ", end="")
    print(quant, "with CI", (arr_sorted[low], arr_sorted[up]),
          "\n\tand with bootstrap CI", ci_boot)

def es4(samples):
    n = 200
    correct = 0
    for subset in np.reshape(samples, (100, n)):
        mean = float(np.mean(subset))
        std_dev = float(np.std(subset))
        err = ETA95 * std_dev / math.sqrt(n)
        if (mean - err) <= 0 <= (mean + err):
            correct += 1
    print("True mean is in interval ", correct, "% of the times")

def main():
    #### Subpoint 1
    y_upper_bound = 6.36 # obtained with WolframAlpha
    samples = []
    n = 20000
    for _ in range(n):
        samples.append(sampling_weird(-3, 3, y_upper_bound))

    #### Subpoint 3
    sub_sample = samples[:200]
    sub_sample.sort()
    print("Over 200 cases:")
    es3median(sub_sample)
    es3mean(sub_sample)
    es3quantile(sub_sample, 0.9)

    ### Subpoint 4
    es4(samples)

    ### Subpoint 2
    fig, ax = plt.subplots(1, 2)

    bins=80
    ax[0].hist(samples, label="Experimental Distribution", bins=bins, density=True)
    x_distr, y_distr = func_points(lambda x: weird_function(x) / 8.8480182)
    ax[0].plot(x_distr, y_distr, label="Expected Distribution")

    ax[1].ecdf(samples, label="Experimental CDF")
    x_int, y_int = func_points(weird_integral)
    ax[1].plot(x_int, y_int, label="Expected CDF")

    ax[0].legend()
    ax[1].legend()
    plt.show()

if __name__ == "__main__":
    main()
