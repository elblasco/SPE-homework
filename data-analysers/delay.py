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
    time_percentage.append(float(line[1]) / float(line[0]))
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
    "Totals delay",
    "Delay U1",
    "Delay U2",
    "Delay U3",
    "Delay U4",
    "Delay U6",
]

fig, ax = plt.subplots(2, 3)
for i in range(2):
    for j in range(3):
        el = i * 3 + j
        ax[i][j].hist(filtered[el], bins=40, label=names[el])

        mean = np.mean(filtered[el])
        ax[i][j].axvline(x=mean, color='r', linestyle='dashed', label="Mean")
        ax[i][j].legend(loc="upper right")

        print(names[el], mean)
plt.show()
