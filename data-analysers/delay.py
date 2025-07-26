#!/usr/bin/env pyton3

import csv
import math
import os

# noinspection PyUnresolvedReferences
import matplotlib.pyplot as plt
# noinspection PyUnresolvedReferences
import numpy as np

os.makedirs("./img/delay", exist_ok=True)
csv_reader = csv.reader(open('../output/delay.csv', mode='r'))

QUANTILES = [0.9, 0.99, 0.999]
colours = ['green', 'orange', 'purple']

time_percentage: list = []
lines: list = []

next(csv_reader)

for line in csv_reader:
    real_time = float(line[1])
    expected_time = float(line[0])
    if real_time > expected_time: # Ignore if a train is ahead of its schedule
        time_percentage.append(real_time - expected_time)
        lines.append(line[2].strip())

filtered: list = [
    time_percentage,
    [time for time, line in zip(time_percentage, lines) if line == "U1"],
    [time for time, line in zip(time_percentage, lines) if line == "U2"],
    [time for time, line in zip(time_percentage, lines) if line == "U3"],
    [time for time, line in zip(time_percentage, lines) if line == "U4"],
    [time for time, line in zip(time_percentage, lines) if line == "U6"],
]

names = [
    "Total delay",
    "U1 delay",
    "U2 delay",
    "U3 delay",
    "U4 delay",
    "U6 delay",
]

for i in range(2):
    for j in range(3):
        fig, ax = plt.subplots(1, 1)
        fig.set_size_inches(7, 4)
        el = i * 3 + j
        ax.hist(filtered[el], bins=80, label=names[el], density=True)

        mean = np.mean(filtered[el])

        quantiles = np.quantile(filtered[el], QUANTILES, method="inverted_cdf")

        for (idx,perc) in enumerate(QUANTILES):
            ax.axvline(x=quantiles[idx], linestyle='dashed', label=f"{perc} quantile", color=colours[idx])

        ax.axvline(x=mean, color='r', linestyle='dashed', label="Mean")

        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Normalised distribution")
        ax.legend(loc="upper right")

        fig.savefig(f'./img/delay/delay-{names[el]}.svg')
        print(names[el], mean)