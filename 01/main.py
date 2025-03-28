#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, ceil, floor
from random import choices

if __name__ == "__main__":
    random_values: list = [(-2, sqrt(2)), (4, 1), (10, sqrt(3)), (15, sqrt(2))]
    probability_vector: list = [0.15, 0.25, 0.35, 0.25]
    extracted_values: list = []
    rng: np.random.Generator = np.random.default_rng()
    for _ in range(2000000):
        mu, sigma = choices(
            random_values, probability_vector, k=1
        )[0]
        extracted_values.append(
            rng.normal(mu, sigma, 1)[0]
        )
    print(np.mean(extracted_values))
    print(np.var(extracted_values))
    bins = np.linspace(ceil(min(extracted_values)),
                       floor(max(extracted_values)),
                       40)  # fixed number of bins
    fig, ax = plt.subplots()
    ax.hist(extracted_values, linewidth=0.5, edgecolor="white", bins=bins)
    plt.show()
