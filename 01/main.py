#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from random import choices

RANGE = 100000

def compute_mean(values, probs):
    return sum(v * p for v, p in zip(values, probs))

def compute_var(values,  probs):
    squared = map(lambda x: x**2, values)
    return compute_mean(squared, probs) - compute_mean(values, probs)**2

if __name__ == "__main__":
    choice_mean = [-2, 4, 10, 15]
    choice_var = [2, 1, 3, 2]
    choice_prob = [0.15, 0.25, 0.35, 0.25]
    vals = []
    rng = np.random.default_rng()


    print("EXPECTED ARE:")
    expected_mean = compute_mean(choice_mean, choice_prob)

    expected_var = (compute_var(choice_mean, choice_prob)
        + compute_mean(choice_var, choice_prob))

    print(expected_mean)
    print(expected_var)


    print("COMPUTING...")
    for _ in range(RANGE):
        mu, sigma = choices(list(zip(choice_mean, choice_var)), choice_prob)[0]
        vals.append(rng.normal(mu, sigma))
    print(np.mean(vals))
    print(np.var(vals))


    fig, ax = plt.subplots()
    ax.hist(vals, linewidth=0.5, edgecolor="white", bins=40)
    plt.show()
