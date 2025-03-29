#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, ceil, floor
from random import choices

if __name__ == "__main__":
    extracted_exp: list = []
    extracted_uni: list = []
    rng: np.random.Generator = np.random.default_rng()

    RANGE = 10000000
    for _ in range(RANGE):
        extracted_exp.append(
            rng.exponential(1)
        )
        extracted_uni.append(
            rng.uniform(0, 5)
        )

    greater = 0
    for i in range(RANGE):
        if (extracted_exp[i] > extracted_uni[i]):
            greater = greater + 1

    print(greater / RANGE)



