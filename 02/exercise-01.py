#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

def main():
    poisson_lambda: int = 200
    poisson_time: int = 1000
    poisson_arrivals: int = poisson_time * poisson_lambda
    n_uni = poisson_arrivals

    # Drawing the values
    uni_vals = np.random.uniform(0, poisson_time, n_uni)
    exp_vals = np.random.exponential(1 / poisson_lambda, poisson_arrivals)

    # Calculating time from inter arrival times
    curr_sum = 0
    uni_vals2 = []
    for l in exp_vals:
        curr_sum += l
        if curr_sum <= poisson_time:
            uni_vals2.append(curr_sum)
    print("Kept ", len(uni_vals2), "/", len(uni_vals))

    # Calculating inter arrival time from times
    exp_vals2 = []
    uni_vals.sort()
    old = 0
    for l in uni_vals:
        exp_vals2.append(l - old)
        old = l

    # Creating the plot
    fig, ax = plt.subplots(3, 1)
    uniform_range = (min(min(uni_vals), min(uni_vals2)), max(max(uni_vals), max(uni_vals2)))
    exponential_range = (min(min(exp_vals), min(exp_vals2)), max(max(exp_vals), max(exp_vals2)))

    ax[0].hist(uni_vals, label='uniform', range=uniform_range, bins=40, edgecolor='red', alpha=1, hatch='//', histtype="step")
    ax[0].hist(uni_vals2, label='from_exp', range=uniform_range, bins=40, edgecolor='green', alpha=1, hatch='\\\\', histtype="step")
    ax[1].hist(exp_vals2, label='from_uni', bins=40, edgecolor='red', alpha=1, hatch='//', range=exponential_range, histtype="step")
    ax[1].hist(exp_vals, label='exp', bins=40, edgecolor='green', alpha=1, hatch='\\\\', range=exponential_range, histtype="step")
    ax[2].hist(exp_vals2, label='from_uni', log=True, bins=40, edgecolor='red', alpha=1, hatch='//', range=exponential_range, histtype="step")
    ax[2].hist(exp_vals, label='exp', log=True, bins=40, edgecolor='green', alpha=1, hatch='\\\\', range=exponential_range, histtype="step")
    ax[0].legend()
    ax[1].legend()
    ax[2].legend()
    plt.show()

if __name__ == "__main__":
    main()