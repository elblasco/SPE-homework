#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

RANGE = 1000000

if __name__ == "__main__":
    vals_exp: list = []
    vals_uni: list = []


    rng = np.random.default_rng()
    for _ in range(RANGE):
        vals_exp.append(rng.exponential(1))
        vals_uni.append(rng.uniform(0, 5))


    print(np.mean(vals_exp))
    print(np.mean(vals_uni))
    greater = sum(1 for i in range(RANGE) if vals_exp[i] > vals_uni[i])
    print(greater / RANGE)


    fig, ax = plt.subplots()
    line1 = ax.hist(vals_exp, linewidth=0.5, edgecolor="darkblue", bins=40, label='Exponential R.V.')
    line2 = ax.hist(vals_uni, linewidth=0.5, edgecolor="darkorange", bins=40, label='Uniform R.V.', alpha=0.7)
    ax.legend()
    plt.show()
