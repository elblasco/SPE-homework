#!/usr/bin/env pyton3

import csv

# noinspection PyUnresolvedReferences
import matplotlib.pyplot as plt
# noinspection PyUnresolvedReferences
import numpy as np

csv_reader = csv.reader(open('../output/board_time.csv', mode='r'))

arrival_times_h: list = []
board_times_min: list = []
lines: list = []

next(csv_reader)

for line in csv_reader:
    arrival_times_h.append(float(line[0]))
    lines.append(line[2].strip())
    board_times_min.append(float(line[3]))

filtered: list = [
    (board_times_min, arrival_times_h),
    zip(*[(time, arrival) for time, arrival, line in zip(board_times_min, arrival_times_h, lines) if line == "U1"]),
    zip(*[(time, arrival) for time, arrival, line in zip(board_times_min, arrival_times_h, lines) if line == "U2"]),
    zip(*[(time, arrival) for time, arrival, line in zip(board_times_min, arrival_times_h, lines) if line == "U3"]),
    zip(*[(time, arrival) for time, arrival, line in zip(board_times_min, arrival_times_h, lines) if line == "U4"]),
    zip(*[(time, arrival) for time, arrival, line in zip(board_times_min, arrival_times_h, lines) if line == "U6"]),
]

names = [
    "General Board Time (minutes)",
    "Board Time U1 (minutes)",
    "Board Time U2 (minutes)",
    "Board Time U3 (minutes)",
    "Board Time U4 (minutes)",
    "Board Time U6 (minutes)",
]

fig, ax = plt.subplots(3, 4)
for i in range(3):
    for j in range(2):
        el = j * 3 + i
        times, arrival_times = filtered[el]
        ax[i][2 * j].hist(times, bins=40, label=names[el])
        ax[i][2 * j + 1].plot(arrival_times, times, label=(names[el] + " over hours"))

        mean = np.mean(times)
        ax[i][2 * j].axvline(x=mean, color='r', linestyle='dashed', label="Mean (minutes)")
        ax[i][2 * j + 1].axhline(y=mean, color='r', linestyle='dashed', label="Mean (minutes)")
        print(names[el], mean)

        ax[i][2 * j].legend(loc="upper right")
        ax[i][2 * j + 1].legend(loc="upper right")
plt.show()
