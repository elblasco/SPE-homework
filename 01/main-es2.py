#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, ceil, floor
from random import choices

if __name__ == "__main__":
    extracted_exp: list = []
    extracted_uni: list = []
    rng: np.random.Generator = np.random.default_rng()

    RANGE = 1000000
    for _ in range(RANGE):
        extracted_exp.append(
            rng.exponential(1)
        )
        extracted_uni.append(
            rng.uniform(0, 5)
        )

    greater = sum(
        1
        for i in range(RANGE)
        if extracted_exp[i] > extracted_uni[i]
    )

    print(np.mean(extracted_exp))
    print(np.mean(extracted_uni))
    print(greater / RANGE)

    fig, ax = plt.subplots()
    ax.hist(extracted_exp)
    ax.hist(extracted_uni)
    plt.show()



