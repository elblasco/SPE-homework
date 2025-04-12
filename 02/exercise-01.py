#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def main():
    poisson_lambda: int = 200
    poisson_time: int = 1000
    poisson_arrivals: int = poisson_time * poisson_lambda

    uni_vals = np.random.uniform(0, poisson_time, poisson_arrivals)
    exp_vals = np.random.exponential(1 / poisson_lambda, poisson_arrivals)

    # Calculating time from inter arrival times
    sam = 0
    uni_vals2 = []
    for l in exp_vals:
        sam += l
        if sam <= poisson_time:
            uni_vals2.append(sam)
    print("Kept ", len(uni_vals2), "/", len(uni_vals))

    # Calculating inter arrival time from times
    exp_vals2 = []
    uni_vals.sort()
    old = uni_vals[0]
    for l in uni_vals:
        exp_vals2.append(l - old)
        old = l

    # plot:
    uniform_range = (min(min(uni_vals), min(uni_vals2)), max(max(uni_vals), max(uni_vals2)))
    exponential_range = (min(min(exp_vals), min(exp_vals2)), max(max(exp_vals), max(exp_vals2)))

    fig, ax = plt.subplots(2, 1)

    ax[0].hist(uni_vals, bins=40, alpha=0.5, label='uniform1', range=uniform_range)
    ax[0].hist(uni_vals2, bins=40, alpha=0.5, label='uniform2',  range=uniform_range)
    ax[1].hist(exp_vals, bins=40, alpha=0.5, label='exp1',  range=exponential_range)
    ax[1].hist(exp_vals2, bins=40, alpha=0.5, label='exp2', range=exponential_range)

    ax[0].legend()
    ax[1].legend()
    plt.show()

if __name__ == "__main__":
    main()