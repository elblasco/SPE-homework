#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    poisson_lambda: int = 200
    poisson_time: int = 1000
    poisson_arrivals: int = poisson_time * poisson_lambda
    uniform_values: list = np.random.uniform(0, poisson_time, poisson_arrivals)
    exponential_values: list = np.random.exponential(
        1 / poisson_lambda, poisson_arrivals
    )
    exponential_values2: list = []
    uniform_values2: list = []
    sam: int = 0
    for l in exponential_values:
        sam += l
        if(sam <= poisson_time):
            uniform_values2.append(sam)

    print(len(uniform_values2))
    print(len(uniform_values))
    uniform_values.sort()
    old: int = uniform_values[0]
    for l in uniform_values:
        exponential_values2.append(l - old)
        old = l

    # plot:
    uniform_range = (min(min(uniform_values), min(uniform_values2)), max(max(uniform_values), max(uniform_values2)))
    exponential_range = (min(min(exponential_values), min(exponential_values2)), max(max(exponential_values), max(exponential_values2)))
    fig, ax = plt.subplots(2, 1)
    ax[0].hist(uniform_values, bins=40, alpha=0.5, label='uniform1', range=uniform_range) 
    ax[0].hist(uniform_values2, bins=40, alpha=0.5, label='uniform2',  range=uniform_range)
    ax[0].legend()
    ax[1].hist(exponential_values, bins=40, alpha=0.5, label='exp1',  range=exponential_range)
    ax[1].hist(exponential_values2, bins=40, alpha=0.5, label='exp2', range=exponential_range)
    ax[1].legend()
    plt.show()
