#!/usr/bin/env pyton3

import csv

# noinspection PyUnresolvedReferences
import matplotlib.pyplot as plt
# noinspection PyUnresolvedReferences
import numpy as np

csv_reader = csv.reader(open('../output/delay.csv', mode='r'))

time_percentage: list = []
lines: list = []

next(csv_reader)

for line in csv_reader:
    real_time = float(line[1])
    expected_time = float(line[0])
    if real_time > expected_time:
        time_rap = real_time / expected_time - 1.0
    else:
        time_rap = 1.0 - expected_time / real_time

    time_percentage.append(time_rap)
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
    "Totals % delay over average (logarithm % and value)",
    "U1 % delay over average (logarithm % and value)",
    "U2 % delay over average (logarithm % and value)",
    "U3 % delay over average (logarithm % and value)",
    "U4 % delay over average (logarithm % and value)",
    "U6 % delay over average (logarithm % and value)",
]

fig, ax = plt.subplots(2, 3)
fig.set_size_inches(20, 15)

for i in range(2):
    for j in range(3):
        el = i * 3 + j
        ax[i][j].hist(filtered[el], bins=60, label=names[el], log=True)

        mean = np.mean(filtered[el])
        ax[i][j].axvline(x=mean, color='r', linestyle='dashed', label="Mean")
        ax[i][j].legend(loc="upper right")

        print(names[el], mean)

fig.savefig('./img/delay/delay.svg')
